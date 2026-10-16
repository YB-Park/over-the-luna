#!/usr/bin/env node
// P1b: small practical code-edit comparison. Real file modifications happen
// ONLY in isolated GitHub Actions runner temp fixtures. No git pushes/tools.
import { CopilotClient } from "@github/copilot-sdk";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const root=process.cwd();
const fixture=path.join(root,"qualification","experiments","gpt6_luna","fixture.py");
const diagnostic=process.env.DIAGNOSTIC_ONLY==="1";
const cases=diagnostic?["risk_idempotency"]:["broad_contract","risk_idempotency"];
let strategies=[
  {name:"luna",id:"gpt-6-luna",provider:"copilot"},
  {name:"haiku",id:"claude-haiku-5.5",provider:"copilot"},
  {name:"sol",id:"gpt-6.1-sol",provider:"openai"},
  {name:"sonnet",id:"claude-sonnet-5.5",provider:"copilot"}
];
if(diagnostic)strategies=strategies.filter(x=>x.name==="luna"||x.name==="sol");
const allowed={
  broad_contract:new Set(["src/exporter.py","tests/test_exporter.py"]),
  risk_idempotency:new Set(["src/ledger.py","tests/test_ledger.py"])
};
if (!process.env.GITHUB_TOKEN||!process.env.OPENAI_API_KEY)throw new Error("Action secrets unavailable");
if (!fs.existsSync(fixture))throw new Error("Previously validated qualification fixture unavailable");
function py(args) {
 const p=spawnSync("python",[fixture,...args],{encoding:"utf8",timeout:15000});
 return {ok:p.status===0,text:p.stdout??"",stderr:(p.stderr??"").slice(0,250)};
}
function snapshot(dir) {
 const results={};
 function walk(base) {
   for (const d of fs.readdirSync(base,{withFileTypes:true})) {
     if(d.name==="__pycache__" || d.name===".git")continue;
     const file=path.join(base,d.name);
     if(d.isDirectory())walk(file);
     else if (d.isFile() && !d.name.endsWith(".pyc"))
       results[path.relative(dir,file).split(path.sep).join("/")]=fs.readFileSync(file,"utf8");
   }
 }
 walk(dir);
 return results;
}
function usage(ev) {
 const d=ev.data??{};
 return {model:String(d.model??"unknown"),isByok:!!d.isByok,
   inputTokens:d.inputTokens??null,outputTokens:d.outputTokens??null,
   cacheReadTokens:d.cacheReadTokens??null,
   nanoAiu:d.copilotUsage?.totalNanoAiu??null};
}
const records=[];
let interrupted=false;
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,useLoggedInUser:false});
try {
 await client.start();
 for(const testcase of cases) {
  for(const arm of strategies) {
   const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-edit-"+testcase+"-"+arm.name+"-"));
   const taskFile=path.join(work,"TASK.txt");
   const preparation=py(["prepare","--case",testcase,"--root",work,"--task-file",taskFile]);
   if(!preparation.ok)throw new Error("Fixture preparation failed, no paid run should proceed");
   const initial=snapshot(work);
   const permissionAudit=[];
   const config={
     model:arm.id,reasoningEffort:"low",
     workingDirectory:work,
     tools:[],
     availableTools:["view","read_file","edit","edit_file","apply_patch","grep","glob"],
     onPermissionRequest:(req)=>{
       let decision={kind:"reject",feedback:"No shell, network, or external tools allowed."};
       if(req.managedApprovalRequired)decision={kind:"no-result"};
       else if(req.kind==="read")decision={kind:"approve-once"};
       else if(req.kind==="write"){
         const file=String(req.fileName??"");
         const full=path.resolve(work,file);
         const rel=path.relative(work,full).split(path.sep).join("/");
         decision=allowed[testcase].has(rel)?
           {kind:"approve-once"}:
           {kind:"reject",feedback:"Writes restricted to the two permitted fixture paths."};
       } else if(req.kind==="custom-tool" && ["view","read_file","edit","edit_file","apply_patch","grep","glob"].includes(req.toolName))
         decision={kind:"approve-once"};
       if(diagnostic)permissionAudit.push({kind:String(req.kind??"unknown"),tool:String(req.toolName??"none"),fileBase:req.fileName?path.basename(String(req.fileName)):"none",decision:decision.kind});
       return decision;
     }
   };
   if(arm.provider==="openai")
     config.provider={type:"openai",baseUrl:"https://api.openai.com/v1",wireApi:"responses",apiKey:process.env.OPENAI_API_KEY};
   const session=await client.createSession(config);
   const usageLog=[],events=[];
   session.on(ev=>{
      if(ev.type==="assistant.usage")usageLog.push(usage(ev));
      if(diagnostic && (ev.type==="assistant.tool_call"||ev.type.startsWith("tool.")))events.push({type:ev.type,tool:String(ev.data?.toolName??ev.data?.name??ev.data?.tool?.name??"unknown").slice(0,70)});
   });
   const task=fs.readFileSync(taskFile,"utf8").trim();
   const start=Date.now();
   let error=null;
   let answerPreview=null;
   try{
     const response=await session.sendAndWait({prompt:
       "Implement the following small Python change IN THE CURRENT WORKING DIRECTORY. Read source files as needed, edit only the stated implementation and focused test paths. Do not modify other files, run shell commands, use network tools, or access git history. Finish with a brief explanation of the change, without claiming hidden test results.\n\nTASK:\n"+task+
       "\n\nALLOWED MODIFIED PATHS: "+[...allowed[testcase]].join(", ")
     },110000);
     if(diagnostic)answerPreview=String(response?.data?.content??"").slice(0,500);
   }catch(e){error=String(e?.message??"runtime error").slice(0,180);}
   const elapsedMs=Date.now()-start;
   try{await session.disconnect();}catch{}
   const modified=snapshot(work);
   const paths=[...new Set([...Object.keys(initial),...Object.keys(modified)])].filter(p=>initial[p]!==modified[p]);
   const unexpected=paths.filter(p=>!allowed[testcase].has(p));
   const graded=py(["hidden","--case",testcase,"--root",work]);
   let grade={};
   try{grade=JSON.parse(graded.text.trim());}catch{grade={pass:false,failures:["missing hidden grade"]};}
   const observed=usageLog.map(x=>x.model);
   const modelObserved=observed.includes(arm.id);
   const pass=!error && graded.ok && grade.pass===true && unexpected.length===0 && modelObserved;
   const record={case:testcase,arm:arm.name,requestedModel:arm.id,pass,
      hiddenPass:graded.ok&&grade.pass===true,
      hiddenFailures:(grade.failures??[]).map(x=>String(x).slice(0,180)),
      changedPaths:paths,unexpectedPaths:unexpected,
      modelObserved,observedModels:[...new Set(observed)],
      elapsedMs,usage:usageLog,error,...(diagnostic?{permissionAudit,toolEvents:events,answerPreview}:{})};
   records.push(record);
   const tokenIn=usageLog.reduce((a,x)=>a+(x.inputTokens??0),0);
   const tokenOut=usageLog.reduce((a,x)=>a+(x.outputTokens??0),0);
   console.log("IMPLEMENT_RESULT",JSON.stringify({case:testcase,model:arm.name,pass,hiddenPass:record.hiddenPass,changedPaths:paths,unexpectedPaths:unexpected,observedModels:record.observedModels,inputTokens:tokenIn,outputTokens:tokenOut,elapsedMs,error:error?"RUNTIME_ERROR":null}));
   if(diagnostic)console.log("IMPLEMENT_DIAGNOSTIC",JSON.stringify({case:testcase,arm:arm.name,permissionAudit,toolEvents:events,answerPreview}));
   if(error || !modelObserved){interrupted=true;break;}
  }
  if(interrupted)break;
 }
}finally{try{await client.stop();}catch{}}
const summary=strategies.map(m=>{
 const rows=records.filter(r=>r.arm===m.name);
 return {arm:m.name,finished:rows.length,correct:rows.filter(r=>r.pass).length,totalElapsedMs:rows.reduce((n,r)=>n+r.elapsedMs,0),inputTokens:rows.flatMap(r=>r.usage).reduce((n,u)=>n+(u.inputTokens??0),0),outputTokens:rows.flatMap(r=>r.usage).reduce((n,u)=>n+(u.outputTokens??0),0)};
});
const result={time:"2026-10-16",method:diagnostic?"1 existing implementation case × 2 models, tool-permission diagnostic":"2 existing, external hidden implementation cases × 4 model-only strategies, tool-based edits",summary,records,interrupted};
fs.writeFileSync(process.env.RESULT_PATH??"/tmp/implementation-result.json",JSON.stringify(result,null,2));
console.log("IMPLEMENT_SUMMARY",JSON.stringify({summary,interrupted,total:records.length}));
if(interrupted||records.length!==cases.length*strategies.length) {
 console.error("IMPLEMENT_RUN_INCOMPLETE: environment problem or missing arm; don't rank models");
 process.exitCode=1;
}

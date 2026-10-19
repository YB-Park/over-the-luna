#!/usr/bin/env node
// P12: single public two-arm DIRECT Main edit; NOT a Host subagent/Council test.
import { CopilotClient } from "@github/copilot-sdk";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
const repo=process.cwd();
const artifacts=process.env.ARTIFACT_DIR||path.join(os.tmpdir(),"otl-p12");
const model="gpt-6-luna",pluginId="over-the-luna-next";
const allowed=["scripts/role_trace_accounting.py","tests/test_role_trace_accounting.py"];
const seed=[...allowed,"tests/fixtures/p5_role_accounting.json",
            "scripts/p5_fixture_provenance.py"];
const tools=["view","read_file","grep","glob","edit_file","apply_patch"];
const prompt=[
 "Fix a real defect in this public research repository.",
 "In scripts/role_trace_accounting.py, _pair_lifecycle currently counts",
 "two same-named events with absent or invalid toolCallId values as a pair.",
 "Require a nonempty string toolCallId on both matching events. Preserve",
 "genuine identity matches, mismatches, different role names and duplicates.",
 "Add a negative regression to tests/test_role_trace_accounting.py.",
 "Modify only that test and scripts/role_trace_accounting.py.",
 "No shell, network, subagent, other model or git mutation tools are available.",
 "An external independent grader will run tests. Do not claim you ran tests.",
 "Implement directly without delegation."
].join(" ");
if(!process.env.GITHUB_TOKEN)throw Error("No Actions Copilot authorization");
const manifest=JSON.parse(fs.readFileSync(path.join(repo,"plugin.json"),"utf8"));
if(manifest.name!==pluginId||manifest.version!=="2.0.0-rc.2")throw Error("PLUGIN_MISMATCH");
fs.mkdirSync(artifacts,{recursive:true});
function populate(work){
 for(const rel of seed){
   const dst=path.join(work,rel);
   fs.mkdirSync(path.dirname(dst),{recursive:true});
   fs.copyFileSync(path.join(repo,rel),dst);
 }
}
function snapshot(work){
 return new Map(seed.map(rel=>[rel,fs.readFileSync(path.join(work,rel),"utf8")]));
}
function permission(req,work,record){
 let result={kind:"reject",feedback:"P12 allows public reads and two scoped edits only"};
 if(req.managedApprovalRequired)result={kind:"no-result"};
 else if(req.kind==="read")result={kind:"approve-once"};
 else if(req.kind==="write"){
   const rel=path.relative(work,path.resolve(work,String(req.fileName||"")))
     .replaceAll(path.sep,"/");
   if(allowed.includes(rel))result={kind:"approve-once"};
 }
 record.push({kind:String(req.kind||"unknown"),decision:result.kind});
 return result;
}
function grade(work,changed){
 const r=spawnSync("python",[path.join(repo,"scripts/p12_direct_grader.py"),
            "--work",work,"--changed",...changed],
   {cwd:work,encoding:"utf8",timeout:105000,
    env:{PATH:process.env.PATH||"",HOME:os.tmpdir(),LANG:"C.UTF-8",
         PYTHONDONTWRITEBYTECODE:"1"}});
 try{return JSON.parse(r.stdout.trim().split("\n").at(-1));}
 catch{return {pass:false,checks:{grader_execution_valid:false}};}
}
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,
  useLoggedInUser:false,enableConfigDiscovery:false});
const summary={schema:1,test:"P12 public toolCallId lifecycle defect",model,
  interpretation:"DIRECT SDK only, NOT named Host subagent",arms:[]};
let invalid=false;
try{
 await client.start();
 for(const mode of ["sdk_default","rc2_actual_plugin"]){
   const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-p12-"+mode+"-"));
   populate(work);
   const before=snapshot(work),usage=[],events=[],audit=[];
   let session,error=null,pluginLoaded=false,mainSelected=false;
   const start=Date.now();
   try{
     session=await client.createSession({
       model,reasoningEffort:"low",workingDirectory:work,
       pluginDirectories:mode==="rc2_actual_plugin"?[repo]:[],
       availableTools:tools,enableSessionStore:false,
       onPermissionRequest:r=>permission(r,work,audit)
     });
     const plugins=await session.rpc.plugins.list();
     pluginLoaded=(plugins.plugins||[]).some(x=>x.name===pluginId&&x.enabled!==false);
     if(mode==="rc2_actual_plugin"){
       if(!pluginLoaded)throw Error("PLUGIN_NOT_LOADED");
       const list=await session.rpc.agent.list();
       const main=(list.agents||[]).find(a=>a.displayName==="Over the Luna Next"&&
           String(a.name).startsWith(pluginId+":"));
       if(!main)throw Error("MAIN_NOT_FOUND");
       await session.rpc.agent.select({name:main.name});
       const current=await session.rpc.agent.getCurrent();
       mainSelected=(current.agent?.name??current.name)===main.name;
       if(!mainSelected)throw Error("MAIN_NOT_SELECTED");
     }else if(pluginLoaded)throw Error("DEFAULT_CONTAMINATED");
     session.on(e=>{
       if(e.type==="assistant.usage"){
         const d=e.data||{};
         usage.push({model:String(d.model||"unknown"),inputTokens:d.inputTokens??null,
           outputTokens:d.outputTokens??null,copilotNanoAiu:d.copilotUsage?.totalNanoAiu??null});
       }
       if(e.type==="assistant.tool_call"||e.type.startsWith("tool.")||
          e.type.startsWith("subagent.")){
         events.push({type:e.type,name:String(e.data?.toolName||
             e.data?.name||e.data?.agentName||"").slice(0,64)});
       }
     });
     await session.sendAndWait({prompt},100000);
   }catch(ex){
     const msg=String(ex?.message||"");
     error=/timeout/i.test(msg)?"timeout":
       /policy|permission|model|auth|plugin/i.test(msg)?"environment_or_policy":"runtime_error";
     invalid=true;
   }finally{try{await session?.disconnect()}catch{}}
   const after=snapshot(work);
   const changed=[...before.keys()].filter(x=>before.get(x)!==after.get(x)).sort();
   const grading=grade(work,changed);
   const modelObserved=usage.some(x=>x.model===model);
   const acceptance=grading.pass&&modelObserved&&!error&&
     (mode==="sdk_default"||pluginLoaded&&mainSelected);
   const rec={mode,accepted:acceptance,grade:grading,pluginLoaded,mainSelected,
     durationMs:Date.now()-start,modelObserved,error,changedPaths:changed,
     usage,toolStarts:events.filter(e=>e.type==="tool.execution_start")
       .map(e=>e.name),namedSubagentEvents:events.filter(e=>
       e.type.startsWith("subagent.")).length,
     permissions:audit.reduce((o,e)=>{
       const k=e.kind+":"+e.decision;o[k]=(o[k]||0)+1;return o;},{})
   };
   summary.arms.push(rec);
   const out=path.join(artifacts,mode);
   fs.mkdirSync(out,{recursive:true});
   for(const rel of allowed)fs.copyFileSync(path.join(work,rel),
     path.join(out,path.basename(rel)));
   console.log("P12_ARM",JSON.stringify({mode,accepted:acceptance,
     checks:grading.checks,changedPaths:changed,
     inputTokens:usage.reduce((n,x)=>n+(x.inputTokens||0),0),
     durationMs:rec.durationMs,error}));
   if(error||!modelObserved)break;
 }
}finally{
 try{await client.stop()}catch{}
 fs.writeFileSync(path.join(artifacts,"summary.json"),JSON.stringify(summary,null,2));
}
if(summary.arms.length!==2||invalid)process.exitCode=1;

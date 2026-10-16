#!/usr/bin/env node
// Small, one-shot P1 decision experiment: does a strong reviewer buy anything?
// Three strategies, five fixtures with independent executable oracle.
// No model tools (except mixed strategy's single task delegation); no mutations.
// Stop if a model/provider request fails; never silently replace requested models.
import { CopilotClient } from "@github/copilot-sdk";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const base=path.dirname(new URL(import.meta.url).pathname);
const cases=JSON.parse(fs.readFileSync(path.join(base,"review_cases.json"),"utf8"));
const grade=spawnSync("python", [path.join(base,"review_oracle.py")],{encoding:"utf8",timeout:10000});
if(grade.status!==0)throw new Error("Independent fixture oracle failed; no paid runs authorized");
const expected=JSON.parse(grade.stdout.trim());
const key=process.env.OPENAI_API_KEY;
const gh=process.env.GITHUB_TOKEN;
if (!key||!gh) throw new Error("Missing credentials for paired experiment");
const strategies=["luna_alone","luna_sol_review","sol_alone"];
const children=[];
const client=new CopilotClient({gitHubToken:gh,useLoggedInUser:false});
const rawRecords=[];
let interrupted=false;
function verdictFrom(text) {
  const match=text.match(/^VERDICT:\s*(PASS|MUST-FIX)\s*$/im);
  return match?match[1]:"FORMAT_FAILURE";
}
function usageCapture(ev) {
  const v=ev?.data??{};
  return {
    model:String(v.model??"unknown"),isByok:!!v.isByok,
    inputTokens:v.inputTokens??null,outputTokens:v.outputTokens??null,
    cacheReadTokens:v.cacheReadTokens??null,
    durationMs:v.duration??null,
    copilotNanoAiu:v.copilotUsage?.totalNanoAiu??null,
  };
}
function rootInstruction(strategy) {
 const common="You are a strict code-reviewer. Only identify acceptance-critical correctness errors supported by the given proposed implementation. Do not demand unnecessary changes. Return exactly two lines: VERDICT: PASS or VERDICT: MUST-FIX, then CAUSE: <one concise precise reason>. Do not invent missing source code. No tools except an expressly required named reviewer.";
 if(strategy==="luna_sol_review")return common+" First independently inspect the candidate, then invoke the named sol-review leaf using the task tool EXACTLY ONCE. Send it the acceptance criteria and proposed code. Incorporate the leaf evidence, but you as Main own the final verdict.";
 return common+" Reply directly; do not delegate.";
}
function promptText(item,strategy) {
 return rootInstruction(strategy)+"\n\nACCEPTANCE:\n"+item.requirements+"\n\nPROPOSED IMPLEMENTATION:\n```python\n"+item.candidate+"\n```";
}
function makeSessionConfig(strategy) {
 const config={
    model:strategy==="sol_alone"?"gpt-6.1-sol":"gpt-6-luna",
    reasoningEffort:"low",
    tools:[],
    availableTools:strategy==="luna_sol_review"?["task"]:[],
    onPermissionRequest:(req)=> {
       if(strategy==="luna_sol_review" && (req.kind==="custom-tool"||req.kind==="mcp") && req.toolName==="task" && !req.managedApprovalRequired) return {kind:"approve-once"};
       return {kind:"reject",feedback:"Read-only benchmark: no file/network/shell tools."};
    },
 };
 if(strategy==="sol_alone") {
   config.provider={type:"openai",baseUrl:"https://api.openai.com/v1",apiKey:key,wireApi:"responses"};
 }
 if(strategy==="luna_sol_review") {
   config.providers=[{name:"openai-sol",type:"openai",wireApi:"responses",baseUrl:"https://api.openai.com/v1",apiKey:key}];
   config.models=[{provider:"openai-sol",id:"gpt-6.1-sol",wireModel:"gpt-6.1-sol",modelId:"gpt-6.1-sol",maxOutputTokens:1400}];
   config.customAgents=[{
      name:"sol-review",description:"Independent critical review of the provided Python proposed patch against the stated acceptance contract.",
      prompt:"You are an independent, read-only correctness reviewer. Analyze ONLY the acceptance requirements and proposed code passed to you. Return exactly VERDICT: PASS or VERDICT: MUST-FIX and a concise CAUSE describing the most important concrete evidence. Do not use tools.",
      model:"openai-sol/gpt-6.1-sol",reasoningEffort:"low",tools:[],infer:true,
   }];
 }
 return config;
}
try {
 await client.start();
 for (const item of cases) {
   for (const strategy of strategies) {
     const config=makeSessionConfig(strategy);
     const session=await client.createSession(config);
     const usages=[];const lifecycle=[];
     session.on(ev=>{
       if(ev.type==="assistant.usage")usages.push(usageCapture(ev));
       if(["subagent.started","subagent.completed","subagent.failed"].includes(ev.type))lifecycle.push({event:ev.type,agent:String(ev.data?.agentName??"unknown"),model:String(ev.data?.model??"unknown")});
     });
     const start=Date.now();
     let text="",exception=null;
     try{
       const out=await session.sendAndWait({prompt:promptText(item,strategy)},90000);
       text=String(out?.data?.content??"");
     } catch(e) {exception=String(e?.message??"runtime exception").slice(0,120);}
     const actual=verdictFrom(text);
     const delegated=lifecycle.some(x=>x.event==="subagent.started"&&x.model==="openai-sol/gpt-6.1-sol") &&
       lifecycle.some(x=>x.event==="subagent.completed"&&x.model==="openai-sol/gpt-6.1-sol");
     const routeOk=strategy!=="luna_sol_review" || delegated;
     const modelSeen=strategy==="sol_alone"?"gpt-6.1-sol":"gpt-6-luna";
     const seen=usages.some(u=>u.model===modelSeen);
     const correctness=actual===expected[item.name] && routeOk && seen && !exception;
     const record={case:item.name,expected:expected[item.name],strategy,verdict:actual,correct:correctness,modelUsagePresent:seen,routeOk,elapsedMs:Date.now()-start,usage:usages,lifecycle,error:exception,explanationPreview:text.split("\n").filter(x=>/^CAUSE:/i.test(x)).map(x=>x.slice(0,250))[0]??null};
     rawRecords.push(record);
     const tokens=usages.reduce((a,x)=>({in:a.in+(x.inputTokens??0),out:a.out+(x.outputTokens??0)}),{in:0,out:0});
     console.log("REVIEW_RESULT",JSON.stringify({case:item.name,strategy,verdict:actual,expected:expected[item.name],correct:correctness,routeOk,observedModels:[...new Set(usages.map(u=>u.model))],inputTokens:tokens.in,outputTokens:tokens.out,elapsedMs:record.elapsedMs,error:exception?"ERR":"none"}));
     try{await session.disconnect();}catch{}
     if(exception || !seen || !routeOk){interrupted=true;break;}
   }
   if(interrupted)break;
 }
} finally {
 try {await client.stop();}catch{}
}
const summary=strategies.map(s=>{
  const rows=rawRecords.filter(r=>r.strategy===s);
  return {strategy:s,finished:rows.length,correct:rows.filter(r=>r.correct).length,wrong:rows.filter(r=>!r.correct).map(r=>r.case),totalMs:rows.reduce((sum,r)=>sum+r.elapsedMs,0),observedModels:[...new Set(rows.flatMap(r=>r.usage.map(u=>u.model)))],totalInputTokens:rows.flatMap(r=>r.usage).reduce((n,u)=>n+(u.inputTokens??0),0),totalOutputTokens:rows.flatMap(r=>r.usage).reduce((n,u)=>n+(u.outputTokens??0),0),copilotNanoAiuReported:rows.flatMap(r=>r.usage).reduce((n,u)=>n+(u.copilotNanoAiu??0),0)};
});
const result={timestamp:"2026-10-16",design:"P1 miniature paired review; 5 deterministic cases; no statistical significance claim",cases:cases.map(x=>x.name),summary,records:rawRecords,interrupted};
fs.writeFileSync(process.env.RESULT_PATH??"/tmp/review-result.json",JSON.stringify(result,null,2));
console.log("REVIEW_SUMMARY",JSON.stringify({summary,interrupted,totalRuns:rawRecords.length}));
if(interrupted || rawRecords.length!==cases.length*strategies.length) {
 console.error("EXPERIMENT_INCOMPLETE: treat missing arms as UNKNOWN, not performance failure");
 process.exitCode=1;
}

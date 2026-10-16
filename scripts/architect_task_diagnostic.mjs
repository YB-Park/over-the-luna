#!/usr/bin/env node
// One actual plugin Main-to-Architect diagnostic; public code only.
import {CopilotClient} from "@github/copilot-sdk";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
const repo=process.cwd();
const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-arch-task-"));
for(const file of ["plugin.json","scripts/validate_release.py","scripts/package_release.py"]){
 const dest=path.join(work,file);
 fs.mkdirSync(path.dirname(dest),{recursive:true});
 fs.copyFileSync(path.join(repo,file),dest);
}
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,
 useLoggedInUser:false,enableConfigDiscovery:false});
const result={mainSelected:false,taskCalls:0,architectStarted:false,
 architectCompleted:false,taskResults:[],permissionDecisions:[],
 lifecycle:[],models:[],error:null};
let session;
try{
 await client.start();
 session=await client.createSession({
  model:"gpt-6-luna",workingDirectory:work,
  pluginDirectories:[repo],availableTools:["task","view","grep","glob"],
  reasoningEffort:"low",enableSessionStore:false,
  onPermissionRequest:req=>{
   const kind=String(req.kind||"unknown");
   const tool=String(req.toolName||"");
   const allowed=kind==="read"||(kind==="custom-tool"&&tool==="task");
   const response=req.managedApprovalRequired?{kind:"no-result"}:
      allowed?{kind:"approve-once"}:
      {kind:"reject",feedback:"Only public fixture reads and named Architect task are allowed."};
   result.permissionDecisions.push({kind,tool,decision:response.kind});
   return response;
  }
 });
 const listing=await session.rpc.agent.list();
 const main=(listing.agents||[]).find(x=>x.name==="over-the-luna-next:over-the-luna-next");
 const child=(listing.agents||[]).find(x=>x.name==="over-the-luna-next:next-architect");
 if(!main||!child)throw Error("EXPECTED_AGENTS_NOT_REGISTERED");
 await session.rpc.agent.select({name:main.name});
 const cur=await session.rpc.agent.getCurrent();
 result.mainSelected=(cur.agent?.name||cur.name)===main.name;
 if(!result.mainSelected)throw Error("MAIN_SELECTION_NOT_CONFIRMED");
 session.on(ev=>{
  if(ev.type==="tool.execution_start"&&ev.data?.toolName==="task")
   result.taskCalls++;
  if(ev.type==="tool.execution_complete"&&result.taskCalls>result.taskResults.length){
   const payload=ev.data?.result??ev.data?.output??ev.data??{};
   const str=String(JSON.stringify(payload)).slice(0,1400);
   result.taskResults.push(str);
  }
  if(ev.type.startsWith("subagent.")){
   const name=String(ev.data?.agentName??ev.data?.agentDisplayName??"");
   result.lifecycle.push({type:ev.type,name,model:String(ev.data?.model??"unknown")});
   if(ev.type==="subagent.started"&&name.includes("next-architect"))
      result.architectStarted=true;
   if(ev.type==="subagent.completed"&&name.includes("next-architect"))
      result.architectCompleted=true;
  }
  if(ev.type==="assistant.usage")result.models.push(String(ev.data?.model??"unknown"));
 });
 await session.sendAndWait({prompt:
   "Execute a single actual named subagent delegation. You are selected "+
   "Over the Luna Next Main. Use task exactly once to delegate to "+
   "Next Architect (qualified ID over-the-luna-next:next-architect). "+
   "Ask it to read the public scripts/validate_release.py and "+
   "scripts/package_release.py and explain their shared PACKAGE_FILES "+
   "contract and why it prevents symlink release leakage. Do not read "+
   "those files yourself before delegation. Do not edit, use shell, "+
   "invoke other agents or external services. If task cannot use the "+
   "named agent, quote the exact tool error instead of claiming success."
 },90000);
 console.log("ARCH_ACTIVATION",JSON.stringify(result).slice(0,8500));
 if(result.architectStarted&&result.architectCompleted)
  console.log("ACTUAL_ARCHITECT_PASS");
 else console.log("ACTUAL_ARCHITECT_UNVERIFIED: see actual task result and lifecycle");
}catch(err){
 result.error=String(err?.message||"runtime error").slice(0,400);
 console.error("ARCH_ACTIVATION_ERROR",result.error);
 process.exitCode=1;
}finally{
 try{await session?.disconnect()}catch{}
 try{await client.stop()}catch{}
 if(process.env.RESULT_PATH)fs.writeFileSync(process.env.RESULT_PATH,JSON.stringify(result,null,2));
}

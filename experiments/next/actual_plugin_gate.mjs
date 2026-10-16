#!/usr/bin/env node
// Product P3: does Copilot SDK load and activate the actual checked-in
// Over the Luna Next plugin? Metadata MUST pass before ONE small inference.
// This is not a VS Code Agent Host test.
import { CopilotClient } from "@github/copilot-sdk";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const repo=process.cwd();
const plugin=path.join(repo,"experiments/next/candidate-plugin");
const manifest=JSON.parse(fs.readFileSync(path.join(plugin,"plugin.json"),"utf8"));
if(manifest.name!=="over-the-luna-next") throw new Error("MANIFEST_GATE_FAIL");
const work=fs.mkdtempSync(path.join(os.tmpdir(),"otl-plugin-load-"));
fs.writeFileSync(path.join(work,"PUBLIC_CONTRACT.md"),"Acceptance marker: PLUGIN_ACTIVATION_742\nThe plugin candidate must be active, not a copied prompt.\n");
const model="gpt-6-luna";
const client=new CopilotClient({gitHubToken:process.env.GITHUB_TOKEN,useLoggedInUser:false,enableConfigDiscovery:false});
const telemetry={loadedPlugin:false,selectedAgent:false,observedModel:false,readCalls:0,toolCalls:[],sessionAnswerAccepted:false};
let session;
try{
 await client.start();
 session=await client.createSession({
   model,reasoningEffort:"low",workingDirectory:work,
   pluginDirectories:[plugin],availableTools:["view","read_file","grep","glob"],
   enableSessionStore:false,
   onPermissionRequest:req=>{
     const kind=String(req.kind??"unknown");
     const tool=String(req.toolName??"");
     telemetry.toolCalls.push({kind,tool:tool.slice(0,50)});
     if(req.managedApprovalRequired)return {kind:"no-result"};
     if(kind==="read")return {kind:"approve-once"};
     return {kind:"reject",feedback:"Read-only plugin loading gate. No writes, shell, custom tools or external effects."};
   },
 });
 const result=await session.rpc.plugins.list();
 const plugins=Array.isArray(result?.plugins)?result.plugins:[];
 const p=plugins.find(x=>x.name===manifest.name && x.enabled!==false);
 telemetry.loadedPlugin=!!p;
 console.log("PLUGIN_REGISTRY",JSON.stringify({loaded:telemetry.loadedPlugin,
    names:plugins.map(x=>String(x.name).slice(0,70)),sourcePresent:!!p}));
 if(!p) throw new Error("PLUGIN_NOT_LOADED_STOP_BEFORE_INFERENCE");
 const agents=await session.rpc.agent.list();
 const list=Array.isArray(agents?.agents)?agents.agents:[];
 const match=list.find(x=>String(x.name??"").toLowerCase().includes("over-the-luna-next")||
   String(x.displayName??"").includes("Over the Luna Next"));
 console.log("AGENT_REGISTRY",JSON.stringify({count:list.length,
   candidates:list.map(x=>({name:String(x.name??""),displayName:String(x.displayName??"")})).slice(0,25),
   matched:!!match}));
 if(!match || !match.name)throw new Error("AGENT_NOT_DISCOVERED_STOP_BEFORE_INFERENCE");
 const selected=await session.rpc.agent.select({name:match.name});
 const current=await session.rpc.agent.getCurrent();
 const currentName=String(current?.agent?.name??current?.current?.name??current?.name??current?.agentName??"");
 const selectedName=String(selected?.agent?.name??selected?.name??match.name);
 telemetry.selectedAgent=currentName===match.name;
 console.log("AGENT_SELECTION",JSON.stringify({requested:match.name,selectedName,currentName,confirmed:telemetry.selectedAgent}));
 if(!telemetry.selectedAgent)throw new Error("ACTIVE_AGENT_MISMATCH_STOP_BEFORE_INFERENCE");

 session.on(ev=>{
  if(ev.type==="assistant.usage" && ev.data?.model===model) telemetry.observedModel=true;
  if(ev.type==="assistant.tool_call"||ev.type.startsWith("tool."))
    telemetry.toolCalls.push({event:ev.type,tool:String(ev.data?.toolName??ev.data?.name??"").slice(0,70)});
 });
 const ans=await session.sendAndWait({prompt:
   "You are in a minimal public test directory. Read the file PUBLIC_CONTRACT.md using a read tool; state the exact marker from the file. Then give one line exactly PLUGIN_CHECK_DONE. Do not modify files, run shell commands, call subagents or invent findings."
 },75000);
 const answer=String(ans?.data?.content??"");
 telemetry.sessionAnswerAccepted=answer.includes("PLUGIN_ACTIVATION_742")&&answer.includes("PLUGIN_CHECK_DONE");
 telemetry.readCalls=telemetry.toolCalls.filter(x=>x.kind==="read").length;
 console.log("PLUGIN_ACTUAL_EXECUTION",JSON.stringify({modelObserved:telemetry.observedModel,
   markerAccepted:telemetry.sessionAnswerAccepted,readPermissionCalls:telemetry.readCalls,
   events:telemetry.toolCalls.map(x=>x.event??x.kind).slice(0,25)}));
 if(!telemetry.observedModel||!telemetry.sessionAnswerAccepted||telemetry.readCalls===0)
   throw new Error("ACTUAL_PLUGIN_TASK_INCONCLUSIVE");
 console.log("ACTUAL_PLUGIN_SDK_PASS: registered, selected, read and responded using gpt-6-luna");
}catch(e){
  console.error("PLUGIN_GATE_FAILED:",String(e?.message??"runtime failure").slice(0,180));
  process.exitCode=1;
}finally{
 if(session)try{await session.disconnect()}catch{}
 try{await client.stop()}catch{}
 const destination=process.env.RESULT_PATH;
 if(destination)fs.writeFileSync(destination,JSON.stringify(telemetry,null,2));
}

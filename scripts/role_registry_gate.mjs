#!/usr/bin/env node
// No-inference, no-pricing, SDK plugin/agent registration gate.
// Tests runtime metadata for the declared role topology; does not
// attempt provider availability, model execution or effective Host policy.
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { CopilotClient } from "@github/copilot-sdk";

const names=[
 "Over the Luna Next",
 "Next Architect",
 "Next Reviewer",
 "Next Skeptic",
 "Next Researcher",
 "Next Recovery",
 "Next Sol Specialist",
 "Next Sonnet Specialist",
];
const pluginName="over-the-luna-next";
const home=process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(home,"plugin.json"),"utf8"));
if(manifest.name!==pluginName || manifest.version!=="2.0.0-rc.2")
 throw new Error("plugin identity/version mismatch");
const temp=fs.mkdtempSync(path.join(os.tmpdir(),"otl-rc2-registry-"));
const client=new CopilotClient({
 gitHubToken:process.env.GITHUB_TOKEN,useLoggedInUser:false,
 enableConfigDiscovery:false
});
let session;
const result={registry:{},agentNames:[],mainSelected:false,modelInferenceCalls:0};
try {
 await client.start();
 session=await client.createSession({
   model:"gpt-6-luna",
   workingDirectory:temp,
   pluginDirectories:[home],
   availableTools:["view"],
   enableSessionStore:false,
   onPermissionRequest:()=>({kind:"reject"}),
 });
 // NO session.send / sendAndWait. This gate produces zero LLM inference.
 const plugins=await session.rpc.plugins.list();
 const loaded=(plugins.plugins??[]).find(x=>x.name===pluginName&&x.enabled!==false);
 result.registry={name:pluginName,loaded:!!loaded};
 if(!loaded)throw new Error("PLUGIN_NOT_REGISTERED");
 const entries=await session.rpc.agent.list();
 const agents=(entries.agents??[]).filter(x=>
   String(x.name??"").startsWith(pluginName+":"));
 result.agentNames=agents.map(x=>String(x.displayName??"")).sort();
 // Metadata only: inspect what the SDK actually registers for the two
 // essential collaborator roles, without checking model catalogue or inference.
 const selectedRoles=agents.filter(x=>["Next Architect","Next Reviewer"].includes(x.displayName));
 console.log("ROLE_METADATA",JSON.stringify(selectedRoles.map(x=>({
   name:String(x.name??""),displayName:String(x.displayName??""),
   fields:Object.keys(x).sort(),
   model:x.model??null,
   infer:x.infer??null,
   tools:Array.isArray(x.tools)?x.tools:null,
   userInvocable:x.userInvocable??null
 }))));
 const missing=names.filter(n=>!result.agentNames.includes(n));
 const extra=result.agentNames.filter(n=>!names.includes(n));
 console.log("ROLE_REGISTRY",JSON.stringify({loaded:!!loaded,
   count:result.agentNames.length,agentNames:result.agentNames,missing,extra}));
 if(missing.length||extra.length||agents.length!==names.length)
   throw new Error("ROLE_REGISTRY_MISMATCH");
 const main=agents.find(x=>x.displayName==="Over the Luna Next");
 await session.rpc.agent.select({name:main.name});
 const current=await session.rpc.agent.getCurrent();
 const active=String(current?.agent?.name??current?.current?.name??current?.name??"");
 result.mainSelected=active===main.name;
 console.log("MAIN_SELECTION",JSON.stringify({active,expected:main.name,match:result.mainSelected}));
 if(!result.mainSelected)throw new Error("MAIN_SELECTION_MISMATCH");
 console.log("RC2_ROLE_REGISTRY_PASS: actual plugin and 8 role identities registered; no inference called");
} catch (err) {
 console.error("RC2_ROLE_REGISTRY_FAIL",String(err?.message||err).slice(0,230));
 process.exitCode=1;
} finally {
 try{if(session)await session.disconnect()}catch{}
 try{await client.stop()}catch{}
 if(process.env.RESULT_PATH)fs.writeFileSync(process.env.RESULT_PATH,JSON.stringify(result,null,2));
}

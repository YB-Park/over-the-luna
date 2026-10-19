#!/usr/bin/env node
// P16: native VS Code Host plugin discovery, zero inference or chat turns.
// Only sanitized booleans, role counts and error categories may leave runner.
import fs from "node:fs";
import path from "node:path";
import {pathToFileURL} from "node:url";
import {randomUUID} from "node:crypto";
import {setTimeout as wait} from "node:timers/promises";
const ROOT="ahp-root://",CLIENT="otl-p16-public-plugin-probe";
const ROLES=["Next Architect","Next Reviewer","Next Skeptic","Next Researcher",
             "Next Recovery","Next Sol Specialist","Next Sonnet Specialist",
             "Over the Luna Next"].sort();
function pluginEvidence(state,uri) {
  const p=Array.isArray(state?.customizations)?
    state.customizations.find(x=>x.type==="plugin"&&x.uri===uri):null;
  const children=Array.isArray(p?.children)?p.children:[];
  const found=children.filter(x=>x.type==="agent").map(x=>x.name).sort();
  return {pluginObserved:!!p,loadState:p?.load?.kind||"ABSENT",
    roleCount:found.length,exactRoles:found.length===ROLES.length&&
     ROLES.every((x,i)=>x===found[i]),
    architectFound:found.includes("Next Architect"),
    mainFound:found.includes("Over the Luna Next")};
}
function selfTest() {
  const good=pluginEvidence({customizations:[{type:"plugin",uri:"file:///public",
    load:{kind:"loaded"},children:ROLES.map(name=>({type:"agent",name}))}]},"file:///public");
  if(!good.exactRoles||good.roleCount!==8||!good.architectFound)throw Error("valid_roles_missing");
  if(pluginEvidence({customizations:[]},"file:///public").pluginObserved)throw Error("phantom_plugin");
  if(pluginEvidence({customizations:[{type:"plugin",uri:"file:///public",
    children:ROLES.slice(1).map(name=>({type:"agent",name}))}]},"file:///public").exactRoles)
    throw Error("incomplete_roles_accepted");
  console.log("P16_NATIVE_PLUGIN_PREFLIGHT_PASS");
}
async function endpoint(dir) {
  const folder=path.join(dir,"agent-host","local-endpoint","entries");
  for(let i=0;i<125;i++){
    try {
      const e=fs.readdirSync(folder).filter(s=>/^[a-f0-9]{64}\.json$/.test(s))
        .flatMap(s=>{try{return [JSON.parse(fs.readFileSync(path.join(folder,s),"utf8"))]}
                    catch{return []}}).filter(x=>x.schemaVersion===2&&
                    x.type==="standalone"&&x.endpoint?.type==="tcp"&&
                    x.endpoint.host==="127.0.0.1"&&x.endpoint.port>0&&
                    typeof x.connectionToken==="string"&&x.connectionToken.length>0);
      if(e.length===1)return e[0];
      if(e.length>1)throw Error("multiple_hosts");
    }catch(e){if(e.message==="multiple_hosts")throw e}
    await wait(1000);
  }
  throw Error("host_not_published");
}
async function client(entry) {
  const s=new WebSocket("ws://127.0.0.1:"+entry.endpoint.port+"/?tkn="+
                        encodeURIComponent(entry.connectionToken));
  await new Promise((res,rej)=>{
    const timer=setTimeout(()=>rej(Error("connect_timeout")),15000);
    s.addEventListener("open",()=>{clearTimeout(timer);res()},{once:true});
    s.addEventListener("error",()=>{clearTimeout(timer);rej(Error("transport_failed"))},{once:true});
  });
  let serial=0;
  const pending=new Map(),observed=[];
  s.addEventListener("message",event=>{
    let m;try{m=JSON.parse(String(event.data))}catch{return}
    if(typeof m.id==="number"&&pending.has(m.id)){
      const {done,timer}=pending.get(m.id);pending.delete(m.id);
      clearTimeout(timer);done(m);return;
    }
    if(m.method==="action"&&m.params?.channel===observed.session) {
      const t=m.params?.action?.type;
      if(["session/activeClientSet","session/customizationsChanged",
           "session/customizationUpdated"].includes(t))observed.push(t);
    }
  });
  function rpc(method,params,timeoutMs=30000) {
    const id=++serial;
    return new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{pending.delete(id);reject(Error("rpc_timeout"))},timeoutMs);
      pending.set(id,{done:resolve,timer});
      s.send(JSON.stringify({jsonrpc:"2.0",id,method,params}));
    }).then(value=>{
      if(value?.error)throw Error("rpc_code_"+String(Number.isInteger(value.error.code)?value.error.code:0));
      return value.result;
    });
  }
  return {s,rpc,observed};
}
async function main() {
  if(process.argv.includes("--self-test"))return selfTest();
  const userData=process.env.P16_USER_DATA_DIR;
  if(!userData||!path.isAbsolute(userData))throw Error("missing_public_runner");
  const c=await client(await endpoint(userData)),session="ahp-session:/"+randomUUID();
  // VS Code contract: file: is CLIENT-owned; this public checkout is HOST-local.
  const pluginUri=pathToFileURL(process.cwd()).href.replace(/^file:/,"vscode-agent-host-file:");
  const metrics={schema:1,realHost:true,modelTurns:0,ahpInitialized:false,
    copilotAdvertised:false,sessionCreated:false,sessionSubscribed:false,
    pluginPublished:false,pluginObserved:false,loadState:"ABSENT",
    roleCount:0,exactRoles:false,architectFound:false,mainFound:false,
    receivedCustomizationActions:0,sessionLifecycle:"UNKNOWN",
    verdict:"INCONCLUSIVE"};
  try {
    const init=await c.rpc("initialize",{channel:ROOT,clientId:CLIENT,
      protocolVersions:["1.0.0","0.10.0","0.9.0"],
      initialSubscriptions:[ROOT]},20000);
    metrics.ahpInitialized=init.protocolVersion==="1.0.0";
    const root=init.snapshots?.find(x=>x.resource===ROOT)?.state;
    metrics.copilotAdvertised=root?.agents?.some(x=>x.provider==="copilotcli")===true;
    if(!metrics.copilotAdvertised)throw Error("copilot_not_advertised");
    await c.rpc("createSession",{channel:session,provider:"copilotcli",
      workingDirectories:[pathToFileURL(process.cwd()).href]},60000);
    metrics.sessionCreated=true;
    c.observed.session=session;
    const first=await c.rpc("subscribe",{channel:session},15000);
    metrics.sessionSubscribed=!!first?.snapshot;
    metrics.sessionLifecycle=first?.snapshot?.state?.lifecycle||"UNKNOWN";
    const plugin={type:"plugin",id:"otl-p16-"+randomUUID(),
      uri:pluginUri,name:"over-the-luna-next",nonce:"p16-1",
      enablement:[{kind:"global",enabled:true}]};
    await c.rpc("dispatchAction",{channel:session,clientSeq:1,
      action:{type:"session/activeClientSet",activeClient:{
        clientId:CLIENT,displayName:"P16 Public Probe",tools:[],
        customizations:[plugin]}}},20000);
    metrics.pluginPublished=true;
    for(let i=0;i<50;i++){
      const s=await c.rpc("subscribe",{channel:session},15000);
      const e=pluginEvidence(s?.snapshot?.state,pluginUri);
      Object.assign(metrics,e);
      if(metrics.exactRoles||metrics.loadState==="error"||
         metrics.loadState==="degraded")break;
      await wait(1000);
    }
    metrics.receivedCustomizationActions=c.observed.length;
    metrics.verdict=metrics.exactRoles?"HOST_PLUGIN_EIGHT_ROLES_REGISTERED":
      "PLUGIN_ROLES_NOT_VERIFIED";
    await c.rpc("disposeSession",{channel:session},10000);
  }catch(e){
    const message=String(e.message||"");
    metrics.verdict=/^rpc_code_-?\d+$/.test(message)?message:
      ["copilot_not_advertised","rpc_timeout"].includes(message)?message:"SETUP_OR_PLUGIN_BLOCK";
  }finally{try{c.s.close()}catch{}}
  if(process.env.P16_RESULT_PATH)fs.writeFileSync(process.env.P16_RESULT_PATH,
    JSON.stringify(metrics,null,2)+"\n",{mode:0o600});
  console.log("P16_NATIVE_PLUGIN_OBSERVATION",JSON.stringify(metrics));
  if(!metrics.exactRoles)process.exitCode=1;
}
try{await main()}catch(e){
  console.error("P16_NATIVE_PLUGIN_INCONCLUSIVE",
    ["host_not_published","multiple_hosts","missing_public_runner"].includes(String(e.message))?
      e.message:"transport_or_setup_failure");
  process.exitCode=1;
}

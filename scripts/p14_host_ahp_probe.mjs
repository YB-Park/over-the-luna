#!/usr/bin/env node
// P14: zero-model read-only connection to the actual VS Code AHP Host.
// Never log bearer tokens, endpoint URLs or session content.
import fs from "node:fs";
import path from "node:path";
import {setTimeout as delay} from "node:timers/promises";
const ROOT="ahp-root://";
const VERSIONS=["0.7.0","0.6.0","0.5.0","0.4.0","0.3.0"];
function safeEntries(registry) {
  if(!Array.isArray(registry)) throw Error("invalid_registry");
  return registry.filter(x=>x&&x.schemaVersion===2&&x.type==="standalone"&&
    Number.isSafeInteger(x.pid)&&x.pid>0&&typeof x.instanceId==="string"&&
    x.endpoint?.type==="tcp"&&["127.0.0.1","localhost","::1"].includes(x.endpoint.host)&&
    Number.isInteger(x.endpoint.port)&&x.endpoint.port>0&&x.endpoint.port<65536&&
    typeof x.connectionToken==="string"&&x.connectionToken.length>0);
}
function rootInfo(snapshots) {
  const item=Array.isArray(snapshots)?snapshots.find(s=>s?.resource===ROOT):undefined;
  const state=item?.state??item?.snapshot?.state;
  const agents=Array.isArray(state?.agents)?state.agents:[];
  return {rootSnapshotObserved:!!item,providerCount:agents.length,
    copilotAdvertised:agents.some(a=>
      a?.provider==="copilot"||a?.id==="copilot"||a?.name==="copilot")};
}
function selfTest() {
  const e={schemaVersion:2,type:"standalone",pid:123,instanceId:"x",
    endpoint:{type:"tcp",host:"127.0.0.1",port:12345},connectionToken:"PRIVATE"};
  if(safeEntries([e]).length!==1)throw Error("valid_guard_failed");
  if(safeEntries([{...e,endpoint:{...e.endpoint,host:"0.0.0.0"}},
      {...e,connectionToken:""}, {...e,schemaVersion:1}]).length)
    throw Error("unsafe_endpoint_admitted");
  if(!rootInfo([{resource:ROOT,state:{agents:[{provider:"copilot"}]}}]).copilotAdvertised)
    throw Error("root_projection_failed");
  if(rootInfo([]).copilotAdvertised)throw Error("spurious_provider");
  console.log("P14_PROBE_SELFTEST_PASS");
}
async function findEntry(base) {
  const dir=path.join(base,"agent-host","local-endpoint","entries");
  for(let i=0;i<125;i++) {
    try {
      const entries=fs.readdirSync(dir).filter(s=>/^[0-9a-f]{64}\.json$/.test(s))
        .flatMap(s=>{try{return [JSON.parse(fs.readFileSync(path.join(dir,s),"utf8"))]}
                    catch{return []}});
      const candidates=safeEntries(entries);
      if(candidates.length===1)return candidates[0];
      if(candidates.length>1)throw Error("ambiguous_host");
    }catch(e){if(e.message==="ambiguous_host")throw e;}
    await delay(1000);
  }
  throw Error("host_endpoint_not_published");
}
async function initialize(e) {
  const hostname=e.endpoint.host==="::1"?"[::1]":e.endpoint.host;
  const url="ws://"+hostname+":"+e.endpoint.port+"/?tkn="+encodeURIComponent(e.connectionToken);
  const socket=new WebSocket(url);
  return await new Promise((resolve,reject)=>{
    let done=false;
    const timeout=setTimeout(()=>finish(new Error("ahp_initialize_timeout")),12000);
    function finish(error,value) {
      if(done)return; done=true; clearTimeout(timeout);
      try{socket.close()}catch{}
      if(error)reject(error);else resolve(value);
    }
    socket.addEventListener("error",()=>finish(new Error("ahp_transport_error")));
    socket.addEventListener("close",()=>finish(new Error("ahp_closed_before_initialize")));
    socket.addEventListener("open",()=>socket.send(JSON.stringify({
      jsonrpc:"2.0",id:1,method:"initialize",
      params:{channel:ROOT,clientId:"otl-public-p14-audit",
        protocolVersions:VERSIONS,initialSubscriptions:[ROOT]}
    })));
    socket.addEventListener("message",message=>{
      let json;
      try{json=JSON.parse(String(message.data))}catch{return}
      if(json.id!==1)return;
      if(json.error)return finish(new Error("ahp_initialize_rpc_error"));
      if(typeof json.result?.protocolVersion!=="string")
        return finish(new Error("invalid_ahp_initialize_result"));
      finish(null,{protocolVersion:json.result.protocolVersion,...rootInfo(json.result.snapshots)});
    });
  });
}
async function main() {
  if(process.argv.includes("--self-test"))return selfTest();
  const directory=process.env.P14_USER_DATA_DIR;
  if(!directory||!path.isAbsolute(directory))throw Error("missing_runner_user_data");
  const result=await initialize(await findEntry(directory));
  const publicResult={schema:1,mode:"REAL_VSCODE_AGENT_HOST_AHP_NO_MODEL",
    connection:"AHP_INITIALIZE_COMPLETED",...result,
    hostNamedRoleHandbackProven:false,readOnlyPolicyVerified:false,
    modelRequests:0};
  if(process.env.P14_RESULT_PATH)
    fs.writeFileSync(process.env.P14_RESULT_PATH,
      JSON.stringify(publicResult,null,2)+"\n",{mode:0o600});
  console.log("P14_AHP_OBSERVATION",JSON.stringify(publicResult));
}
try{await main()}catch(e){
  const c=String(e?.message||"unknown");
  const known=["missing_runner_user_data","host_endpoint_not_published",
    "ambiguous_host","ahp_initialize_timeout","ahp_transport_error",
    "ahp_closed_before_initialize","ahp_initialize_rpc_error",
    "invalid_ahp_initialize_result"];
  console.error("P14_HOST_GATE_INCONCLUSIVE",known.includes(c)?c:"probe_runtime_error");
  process.exitCode=1;
}

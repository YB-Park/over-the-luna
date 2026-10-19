#!/usr/bin/env node
// P15: authentic VS Code Agent Host session creation (ZERO model messages).
// No secrets, user content, session IDs, or AHP bearer tokens in output.
import fs from "node:fs";
import path from "node:path";
import {pathToFileURL} from "node:url";
import {randomUUID} from "node:crypto";
import {setTimeout as delay} from "node:timers/promises";

const ROOT="ahp-root://";
const versions=["1.0.0","0.10.0","0.9.0"];
function safeRegistry(x) {
  return x&&x.schemaVersion===2&&x.type==="standalone"&&
    x.endpoint?.type==="tcp"&&["127.0.0.1","localhost"].includes(x.endpoint.host)&&
    Number.isInteger(x.endpoint.port)&&x.endpoint.port>0&&x.endpoint.port<65536&&
    typeof x.connectionToken==="string"&&x.connectionToken.length>0;
}
function hasCopilot(snapshots) {
  const root=Array.isArray(snapshots)?snapshots.find(s=>s?.resource===ROOT):undefined;
  const agents=root?.state?.agents;
  return Array.isArray(agents)&&agents.some(a=>a?.provider==="copilotcli");
}
function test() {
  const example={schemaVersion:2,type:"standalone",
    endpoint:{type:"tcp",host:"127.0.0.1",port:1234},connectionToken:"SECRET"};
  if(!safeRegistry(example)||safeRegistry({...example,endpoint:{type:"tcp",host:"0.0.0.0",port:1234}}))
    throw Error("unsafe_endpoint_policy");
  if(!hasCopilot([{resource:ROOT,state:{agents:[{provider:"copilotcli"}]}}])||
      hasCopilot([{resource:ROOT,state:{agents:[{provider:"claude"}]}}]))
    throw Error("provider_id_mismatch");
  console.log("P15_SESSION_PROBE_SELFTEST_PASS");
}
async function findHost(userData) {
  const folder=path.join(userData,"agent-host","local-endpoint","entries");
  for(let i=0;i<125;i++){
    try {
      const matches=fs.readdirSync(folder).filter(n=>/^[0-9a-f]{64}\.json$/.test(n))
        .flatMap(n=>{try{return [JSON.parse(fs.readFileSync(path.join(folder,n),"utf8"))]}
                      catch{return []}}).filter(safeRegistry);
      if(matches.length===1)return matches[0];
      if(matches.length>1)throw Error("ambiguous_host");
    }catch(e){if(e.message==="ambiguous_host")throw e;}
    await delay(1000);
  }
  throw Error("host_unavailable");
}
class Ahp {
  constructor(ws) {
    this.ws=ws;this.pending=new Map();this.counter=0;this.outcome=null;
    ws.addEventListener("message",e=>{
      let m;try{m=JSON.parse(String(e.data))}catch{return}
      if(Number.isInteger(m.id)&&this.pending.has(m.id)){
        const h=this.pending.get(m.id);this.pending.delete(m.id);clearTimeout(h.timer);
        h.resolve(m);return;
      }
      if(m.method==="action"&&m.params?.channel===this.sessionUri) {
        const t=m.params.action?.type;
        if(t==="session/ready"||t==="session/creationFailed")this.outcome=t;
      }
    });
  }
  rpc(method,params,ms=30000) {
    const id=++this.counter;
    return new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{
        this.pending.delete(id);reject(Error("rpc_timeout"));
      },ms);
      this.pending.set(id,{resolve,timer});
      this.ws.send(JSON.stringify({jsonrpc:"2.0",id,method,params}));
    });
  }
}
async function connect(entry) {
  const url="ws://"+entry.endpoint.host+":"+entry.endpoint.port+
    "/?tkn="+encodeURIComponent(entry.connectionToken);
  const ws=new WebSocket(url);
  await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(Error("connection_timeout")),10000);
    ws.addEventListener("open",()=>{clearTimeout(timer);resolve()},{once:true});
    ws.addEventListener("error",()=>{clearTimeout(timer);reject(Error("connection_failed"))},{once:true});
  });
  return new Ahp(ws);
}
function checkReply(m) {
  if(m.error) {
    const code=Number.isInteger(m.error.code)?m.error.code:0;
    throw Error("rpc_code_"+code);
  }
  return m.result;
}
async function main() {
  if(process.argv.includes("--self-test"))return test();
  if(!process.env.P15_USER_DATA_DIR||!path.isAbsolute(process.env.P15_USER_DATA_DIR))
    throw Error("invalid_runner_user_data");
  const entry=await findHost(process.env.P15_USER_DATA_DIR);
  const client=await connect(entry);
  const summary={schema:1,runtime:"VS_CODE_AGENT_HOST_AHP",
    modelRequests:0,namedDelegationObserved:false,selectedPluginConfirmed:false,
    copilotAdvertised:false,sessionCreated:false,sessionReady:false,
    disposition:"INCONCLUSIVE"};
  try{
    const init=checkReply(await client.rpc("initialize",{
      channel:ROOT,clientId:"otl-p15-public-gate",
      protocolVersions:versions,initialSubscriptions:[ROOT]
    },25000));
    summary.ahpVersion=init.protocolVersion;
    summary.copilotAdvertised=hasCopilot(init.snapshots);
    if(!summary.copilotAdvertised)throw Error("copilot_not_advertised");
    const session="ahp-session:/"+randomUUID();
    client.sessionUri=session;
    checkReply(await client.rpc("createSession",{
      channel:session,provider:"copilotcli",
      workingDirectories:[pathToFileURL(process.cwd()).href]
    },80000));
    summary.sessionCreated=true;
    const subscribed=checkReply(await client.rpc("subscribe",{channel:session},16000));
    summary.sessionSubscribed=!!subscribed?.snapshot;
    const lifecycle=subscribed?.snapshot?.state?.lifecycle;
    summary.initialLifecycle=["creating","ready","failed"].includes(lifecycle)?
      lifecycle:"UNKNOWN";
    if(lifecycle==="ready")summary.sessionReady=true;
    if(lifecycle==="failed"){
      const code=subscribed?.snapshot?.state?.creationError?.code;
      summary.failureCode=Number.isInteger(code)?code:null;
    }
    else if(lifecycle==="failed")summary.disposition="SESSION_FAILED";
    if(!summary.sessionReady&&!summary.disposition.startsWith("SESSION_FAILED")){
      for(let i=0;i<32;i++){
        if(client.outcome==="session/ready"){summary.sessionReady=true;break;}
        if(client.outcome==="session/creationFailed"){summary.disposition="SESSION_FAILED";break;}
        await delay(1000);
      }
    }
    if(summary.sessionReady)summary.disposition="HOST_COPILOT_SESSION_READY_NO_MODEL";
    else if(summary.disposition==="INCONCLUSIVE")summary.disposition="SESSION_NOT_READY";
    try{checkReply(await client.rpc("disposeSession",{channel:session},10000))}
    catch{summary.disposeUnverified=true}
  }catch(e){
    const message=String(e.message||"");
    summary.disposition=/^rpc_code_-?\d+$/.test(message)?message:
      ["copilot_not_advertised","rpc_timeout","connection_failed",
       "connection_timeout"].includes(message)?message:"UNCLASSIFIED_BLOCK";
  }finally{
    try{client.ws.close()}catch{}
  }
  if(process.env.P15_RESULT_PATH)fs.writeFileSync(process.env.P15_RESULT_PATH,
    JSON.stringify(summary,null,2)+"\n",{mode:0o600});
  console.log("P15_HOST_SESSION_OBSERVATION",JSON.stringify(summary));
  if(!summary.sessionReady)process.exitCode=1;
}
try{await main()}catch(e){
  const x=String(e?.message||"");
  console.error("P15_HOST_SESSION_INCONCLUSIVE",
    ["ambiguous_host","host_unavailable","invalid_runner_user_data"].includes(x)?x:"setup_or_transport_failed");
  process.exitCode=1;
}

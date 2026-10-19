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
function coarseChatErrorCategory(errorType) {
  if(typeof errorType!=="string"||errorType.length>128)return "UNKNOWN";
  if(/auth|login|credential|unauthoriz|forbidden/i.test(errorType))
    return "AUTH_OR_CREDENTIAL";
  if(/quota|rate.?limit|usage.?limit/i.test(errorType))
    return "QUOTA_OR_RATE";
  if(/model|provider/i.test(errorType))
    return "MODEL_OR_PROVIDER";
  if(/permission|policy|denied/i.test(errorType))
    return "PERMISSION_POLICY";
  return "OTHER_UNCLASSIFIED";
}
function catalogEvidence(root) {
  const copilot=Array.isArray(root?.agents)?
    root.agents.find(x=>x?.provider==="copilotcli"):undefined;
  const models=Array.isArray(copilot?.models)?copilot.models:[];
  const usable=models.filter(x=>x?.policyState!=="disabled");
  return {copilotModelCount:models.length,
    lunaExactAdvertised:usable.some(x=>x?.id==="gpt-6-luna"),
    lunaNamedInPicker:usable.some(x=>typeof x?.name==="string"&&
      /GPT.?6.*Luna/i.test(x.name)),
    autoModelAdvertised:usable.some(x=>x?.id==="auto"),
    hasDisabledModels:models.some(x=>x?.policyState==="disabled"),
    protectedResourceCount:Array.isArray(copilot?.protectedResources)?
      copilot.protectedResources.length:0};
}
function taskNamesArchitect(action) {
  // AHP task arguments arrive in toolCallReady.toolInput; Delta is partial.
  const value=action?.toolInput??action?.input??action?.arguments??
    action?.parameters??action?.content;
  const text=typeof value==="string"?value:JSON.stringify(value??{});
  return /next[-_ .]architect|over-the-luna-next:next-architect/i.test(text);
}
function taskReturnedPublicEvidence(result) {
  if(result?.success!==true)return false;
  const text=JSON.stringify(result?.content??[]);
  return text.includes("scripts/validate_release.py")&&
    text.includes("scripts/package_release.py")&&
    /EVIDENCE|RELATIONSHIPS|WORK_SET/.test(text);
}
function selfTest() {
  const good=pluginEvidence({customizations:[{type:"plugin",uri:"file:///public",
    load:{kind:"loaded"},children:ROLES.map(name=>({type:"agent",name}))}]},"file:///public");
  if(!good.exactRoles||good.roleCount!==8||!good.architectFound)throw Error("valid_roles_missing");
  if(pluginEvidence({customizations:[]},"file:///public").pluginObserved)throw Error("phantom_plugin");
  if(pluginEvidence({customizations:[{type:"plugin",uri:"file:///public",
    children:ROLES.slice(1).map(name=>({type:"agent",name}))}]},"file:///public").exactRoles)
    throw Error("incomplete_roles_accepted");
  if(coarseChatErrorCategory("AUTH_REQUIRED")!=="AUTH_OR_CREDENTIAL"||
     coarseChatErrorCategory("modelUnavailable")!=="MODEL_OR_PROVIDER"||
     coarseChatErrorCategory("arbitrary-user-string")!=="OTHER_UNCLASSIFIED")
    throw Error("error_category_policy");
  const catalog=catalogEvidence({agents:[{provider:"copilotcli",
    models:[{id:"gpt-6-luna",name:"GPT-6 Luna",policyState:"enabled"},
            {id:"auto",name:"Auto",policyState:"unconfigured"}],
    protectedResources:[{}]}]});
  if(!catalog.lunaExactAdvertised||!catalog.autoModelAdvertised||
     catalog.protectedResourceCount!==1)throw Error("catalog_projection_failed");
  if(catalogEvidence({agents:[]}).lunaExactAdvertised||
     catalogEvidence({agents:[{provider:"copilotcli",
       models:[{id:"gpt-6-luna",policyState:"disabled"}]}]}).lunaExactAdvertised)
    throw Error("model_policy_leak");
  if(!taskNamesArchitect({toolInput:{agent_type:"over-the-luna-next:next-architect"}})||
      taskNamesArchitect({toolInput:{agent_type:"next-reviewer"}}))
    throw Error("task_selection_contract");
  const publicPacket={success:true,content:[
    "EVIDENCE: scripts/validate_release.py; scripts/package_release.py"]};
  if(!taskReturnedPublicEvidence(publicPacket)||
      taskReturnedPublicEvidence({success:false,content:publicPacket.content})||
      taskReturnedPublicEvidence({success:true,content:["Fake Main said all tests pass"]}))
    throw Error("independent_packet_contract");
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
async function oneAuthenticArchitectTurn(c,state,pluginUri,metrics) {
  const root=state?.customizations?.find(x=>x.type==="plugin"&&x.uri===pluginUri);
  const main=root?.children?.find(x=>x.type==="agent"&&x.name==="Over the Luna Next");
  const architect=root?.children?.find(x=>x.type==="agent"&&x.name==="Next Architect");
  const chat=state?.defaultChat;
  const result={attempt:"REAL_HOST_NAMED_ARCHITECT_SINGLE_TURN",
    modelRequested:"gpt-6-luna",turnSubmitted:false,
    namedTaskArgObserved:false,taskStarted:false,taskStartedCount:0,taskCompleted:false,
    taskSucceeded:false,returnedSourcePacket:false,mainTurnCompleted:false,
    copilotAuthChallengeObserved:false,chatErrorObserved:false,
    chatErrorCategory:"NONE",
    roleAgentUriVerified:!!main?.uri&&!!architect?.uri,
    status:"INCONCLUSIVE"};
  if(!main?.uri||!architect?.uri||typeof chat!=="string"||
     !chat.startsWith("ahp-chat:")) {
    result.status="MISSING_NATIVE_AGENT_OR_DEFAULT_CHAT";
    return result;
  }
  const turnId=randomUUID();
  await c.rpc("subscribe",{channel:chat},15000);
  const startedIds=new Set();
  const completeIds=new Set();
  let mainText="";
  let finish;
  const stop=new Promise(resolve=>{finish=resolve});
  let ended=false;
  function resolveStop(reason) {if(!ended){ended=true;finish(reason)}}
  function onMessage(e) {
    let m;try{m=JSON.parse(String(e.data))}catch{return}
    if(m.method==="auth/required") {
      result.copilotAuthChallengeObserved=true;
      resolveStop("AUTH_REQUIRED");
      return;
    }
    if(m.method!=="action")return;
    const a=m.params?.action;
    if(m.params?.channel===c.observed.session&&a?.type==="session/creationFailed") {
      resolveStop("SESSION_CREATION_FAILED");return;
    }
    if(m.params?.channel!==chat||!a)return;
    const type=a.type;
    if(type==="chat/toolCallStart"&&a.toolName==="task") {
      result.taskStarted=true;
      result.taskStartedCount++;
      if(result.taskStartedCount>1){resolveStop("UNBOUNDED_TASK_FANOUT");return;}
      if(typeof a.toolCallId==="string")startedIds.add(a.toolCallId);
    }
    if((type==="chat/toolCallDelta"||type==="chat/toolCallReady")
       &&startedIds.has(a.toolCallId)) {
      if(taskNamesArchitect(a))result.namedTaskArgObserved=true;
    }
    if(type==="chat/toolCallComplete"&&startedIds.has(a.toolCallId)) {
      completeIds.add(a.toolCallId);
      result.taskCompleted=true;
      result.taskSucceeded=a.result?.success===true;
      result.returnedSourcePacket=taskReturnedPublicEvidence(a.result);
    }
    if(type==="chat/responsePart") {
      const part=a.part?.content;
      if(typeof part==="string")mainText=(mainText+part).slice(-18000);
    }
    if(type==="chat/delta"&&typeof a.content==="string")
      mainText=(mainText+a.content).slice(-18000);
    if(type==="chat/error"){
      result.chatErrorObserved=true;
      result.chatErrorCategory=coarseChatErrorCategory(a.part?.error?.errorType);
      resolveStop("CHAT_ERROR");
    }
    if(type==="chat/turnComplete"&&a.turnId===turnId) {
      result.mainTurnCompleted=true;resolveStop("TURN_COMPLETE");
    }
  }
  c.s.addEventListener("message",onMessage);
  try {
    const prompt=[
      "Read-only investigation of the PUBLIC over-the-luna repo.",
      "As Over the Luna Next Main, invoke the named Next Architect leaf ONCE",
      "to determine the relationships between scripts/validate_release.py,",
      "scripts/package_release.py, and the release ZIP allowlist.",
      "Return the leaf's separate DECISION, EVIDENCE, RELATIONSHIPS,",
      "WORK_SET and UNCERTAINTIES with real public source paths.",
      "No file edits, shell, network, extra leaves, provider changes or push.",
      "If named delegation is blocked, say INCONCLUSIVE; never fabricate handback."
    ].join(" ");
    await c.rpc("dispatchAction",{channel:chat,clientSeq:2,
      action:{type:"chat/turnStarted",turnId,startedAt:new Date().toISOString(),
        message:{text:prompt,origin:{kind:"user"},
          agent:{uri:main.uri},model:{id:"gpt-6-luna"}}}},25000);
    result.turnSubmitted=true;
    metrics.modelTurns=1;
    const outcome=await Promise.race([stop,wait(100000).then(()=> "OBSERVATION_TIMEOUT")]);
    // Main's own summary cannot prove that an independent task returned evidence.
    // Only the actual successful task result can satisfy this gate.
    result.mainMentionedPublicPaths=mainText.includes("scripts/validate_release.py")&&
       mainText.includes("scripts/package_release.py");
    result.status=outcome;
    if(result.taskStartedCount===1&&result.taskCompleted&&result.taskSucceeded&&result.namedTaskArgObserved&&
       result.returnedSourcePacket&&result.mainTurnCompleted)
      result.status="NAMED_ARCHITECT_COMPLETED_WITH_SOURCE_EVIDENCE";
  }catch(e) {
    const msg=String(e.message||"");
    result.status=/^rpc_code_-?\d+$/.test(msg)?msg:"TURN_RUNTIME_OR_POLICY_FAILURE";
  }finally{c.s.removeEventListener("message",onMessage)}
  return result;
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
    catalog:{copilotModelCount:0,lunaExactAdvertised:false,
      lunaNamedInPicker:false,autoModelAdvertised:false,
      hasDisabledModels:false,protectedResourceCount:0},
    verdict:"INCONCLUSIVE"};
  try {
    const init=await c.rpc("initialize",{channel:ROOT,clientId:CLIENT,
      protocolVersions:["1.0.0","0.10.0","0.9.0"],
      initialSubscriptions:[ROOT]},20000);
    metrics.ahpInitialized=init.protocolVersion==="1.0.0";
    const root=init.snapshots?.find(x=>x.resource===ROOT)?.state;
    metrics.copilotAdvertised=root?.agents?.some(x=>x.provider==="copilotcli")===true;
    if(!metrics.copilotAdvertised)throw Error("copilot_not_advertised");
    if(process.env.P18_MODEL_PREFLIGHT_ONLY==="true") {
      metrics.catalog=catalogEvidence(root);
      for(let i=0;i<10;i++) {
        if(metrics.catalog.lunaExactAdvertised)break;
        await wait(1000);
        const sub=await c.rpc("subscribe",{channel:ROOT},15000);
        metrics.catalog=catalogEvidence(sub?.snapshot?.state);
      }
      metrics.verdict=metrics.catalog.lunaExactAdvertised?
        "HOST_ADVERTISES_EXACT_LUNA":"HOST_DOES_NOT_ADVERTISE_EXACT_LUNA";
    } else {
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
    let mostRecentState=first?.snapshot?.state;
    for(let i=0;i<50;i++){
      const s=await c.rpc("subscribe",{channel:session},15000);
      mostRecentState=s?.snapshot?.state;
      const e=pluginEvidence(s?.snapshot?.state,pluginUri);
      Object.assign(metrics,e);
      if(metrics.exactRoles||metrics.loadState==="error"||
         metrics.loadState==="degraded")break;
      await wait(1000);
    }
    metrics.receivedCustomizationActions=c.observed.length;
    metrics.verdict=metrics.exactRoles?"HOST_PLUGIN_EIGHT_ROLES_REGISTERED":
      "PLUGIN_ROLES_NOT_VERIFIED";
    if(metrics.exactRoles&&process.env.P17_DELEGATE_ONCE==="true") {
      // Fail closed: selected user model must be advertised by the real Host.
      // Plugin registration alone cannot authorize a paid model turn.
      const listing=await c.rpc("subscribe",{channel:ROOT},15000);
      metrics.catalog=catalogEvidence(listing?.snapshot?.state);
      if(!metrics.catalog.lunaExactAdvertised) {
        metrics.delegation={attempt:"REAL_HOST_NAMED_ARCHITECT_SINGLE_TURN",
          modelRequested:"gpt-6-luna",turnSubmitted:false,
          status:"BLOCKED_MODEL_NOT_ADVERTISED"};
        metrics.verdict="BLOCKED_MODEL_NOT_ADVERTISED";
      } else {
        metrics.delegation=await oneAuthenticArchitectTurn(c,mostRecentState,
          pluginUri,metrics);
        metrics.verdict=metrics.delegation.status;
      }
    }
    await c.rpc("disposeSession",{channel:session},10000);
    }
  }catch(e){
    const message=String(e.message||"");
    metrics.verdict=/^rpc_code_-?\d+$/.test(message)?message:
      ["copilot_not_advertised","rpc_timeout"].includes(message)?message:"SETUP_OR_PLUGIN_BLOCK";
  }finally{try{c.s.close()}catch{}}
  if(process.env.P16_RESULT_PATH)fs.writeFileSync(process.env.P16_RESULT_PATH,
    JSON.stringify(metrics,null,2)+"\n",{mode:0o600});
  console.log("P16_NATIVE_PLUGIN_OBSERVATION",JSON.stringify(metrics));
  if(process.env.P18_MODEL_PREFLIGHT_ONLY==="true") {
    if(!metrics.ahpInitialized||!metrics.copilotAdvertised)process.exitCode=1;
  }else if(!metrics.exactRoles||
      (process.env.P17_DELEGATE_ONCE==="true"&&
       metrics.delegation?.status!=="NAMED_ARCHITECT_COMPLETED_WITH_SOURCE_EVIDENCE"))
    process.exitCode=1;
}
try{await main()}catch(e){
  console.error("P16_NATIVE_PLUGIN_INCONCLUSIVE",
    ["host_not_published","multiple_hosts","missing_public_runner"].includes(String(e.message))?
      e.message:"transport_or_setup_failure");
  process.exitCode=1;
}

import{s as Ue,a as qe,m as je,t as L,i as g,c,S as $,b as U,d as C,e as V,f as pe,g as _,h as Ae,j as v,k as d,l as Fe,n as ze,r as Ne,o as Re,p as J,u as ge,q as B,v as Be,w as H,x as me,y as He,z as Oe,A as z,B as We,I as Xe,C as K,F as G,D as Z,E as Ve,G as Je,H as Ze,J as Ge,K as Ee,L as Qe,M as Ke,N as Ye,O as et,P as tt,Q as st,R as nt,T as at,U as T,V as ot,W as rt,X as q,Y as lt,Z as it,_ as ct,$ as dt,a0 as ut}from"./vendor-LFOJg3vZ.js";(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const n of document.querySelectorAll('link[rel="modulepreload"]'))s(n);new MutationObserver(n=>{for(const a of n)if(a.type==="childList")for(const l of a.addedNodes)l.tagName==="LINK"&&l.rel==="modulepreload"&&s(l)}).observe(document,{childList:!0,subtree:!0});function o(n){const a={};return n.integrity&&(a.integrity=n.integrity),n.referrerPolicy&&(a.referrerPolicy=n.referrerPolicy),n.crossOrigin==="use-credentials"?a.credentials="include":n.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function s(n){if(n.ep)return;n.ep=!0;const a=o(n);fetch(n.href,a)}})();const pt="modulepreload",gt=function(e,t){return new URL(e,t).href},ee={},j=function(t,o,s){if(!o||o.length===0)return t();const n=document.getElementsByTagName("link");return Promise.all(o.map(a=>{if(a=gt(a,s),a in ee)return;ee[a]=!0;const l=a.endsWith(".css"),p=l?'[rel="stylesheet"]':"";if(!!s)for(let u=n.length-1;u>=0;u--){const m=n[u];if(m.href===a&&(!l||m.rel==="stylesheet"))return}else if(document.querySelector(`link[href="${a}"]${p}`))return;const r=document.createElement("link");if(r.rel=l?"stylesheet":pt,l||(r.as="script",r.crossOrigin=""),r.href=a,document.head.appendChild(r),l)return new Promise((u,m)=>{r.addEventListener("load",u),r.addEventListener("error",()=>m(new Error(`Unable to preload CSS for ${a}`)))})})).then(()=>t()).catch(a=>{const l=new Event("vite:preloadError",{cancelable:!0});if(l.payload=a,window.dispatchEvent(l),!l.defaultPrevented)throw a})},mt=C('<div class="loading loading-spinner">'),ft=C('<button><span class="truncate rounded-none">'),fe=e=>{const[t,o]=Ue(e,["class","loading","icon"]);return(()=>{const s=ft(),n=s.firstChild;return qe(s,je({get class(){return L("btn flex items-center",t.loading?"btn-disabled":t.class)}},o),!1,!0),g(s,c($,{get when(){return t.loading},get children(){return mt()}}),n),g(n,()=>e.icon||e.children),U(()=>n.classList.toggle("flex-1",!t.icon)),s})()},ht=C('<div><div class="collapse-title pr-4 text-xl font-medium after:!top-8"></div><div>'),Ws=e=>{const{title:t,onCollapse:o}=e,s=()=>{const a="collapse-open",l="collapse-close";return e.isOpen?a:l},n=()=>{const a="opacity-100",l="opacity-0";return e.isOpen?a:l};return(()=>{const a=ht(),l=a.firstChild,p=l.nextSibling;return l.$$click=()=>o(!e.isOpen),g(l,t),g(p,c($,{get when(){return e.isOpen},get children(){return pe(()=>e.children)()}})),U(i=>{const r=L(s(),"collapse collapse-arrow select-none border-secondary bg-base-200 shadow-md"),u=L(n(),"collapse-content grid grid-cols-2 gap-2 transition-opacity duration-1000 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5");return r!==i._v$&&_(a,i._v$=r),u!==i._v$2&&_(p,i._v$2=u),i},{_v$:void 0,_v$2:void 0}),a})()};V(["click"]);const vt=["acid","aqua","autumn","black","bumblebee","business","cmyk","coffee","corporate","cupcake","cyberpunk","dark","dim","dracula","emerald","fantasy","forest","garden","halloween","lemonade","light","lofi","luxury","night","nord","pastel","retro","sunset","synthwave","valentine","winter","wireframe"];var P=(e=>(e.Overview="/overview",e.Proxies="/proxies",e.Rules="/rules",e.Conns="/conns",e.Log="/logs",e.Config="/config",e.Setup="/setup",e))(P||{});const yt=10,Xs={title:{align:"center",style:{color:"gray",fontSize:"16px"}},chart:{toolbar:{show:!1},zoom:{enabled:!1},animations:{easing:"linear"}},noData:{text:"Loading..."},legend:{showForSingleSeries:!0,fontSize:"16px",labels:{colors:"gray"},itemMargin:{horizontal:32}},dataLabels:{enabled:!1},grid:{yaxis:{lines:{show:!1}}},stroke:{curve:"smooth"},tooltip:{enabled:!1},xaxis:{range:yt,labels:{show:!1},axisTicks:{show:!1}},yaxis:{labels:{style:{colors:"gray",fontSize:"13px"},formatter:e=>Ae(e).toString()}}};var Y=(e=>(e[e.NOT_CONNECTED=-1]="NOT_CONNECTED",e[e.MEDIUM=200]="MEDIUM",e[e.HIGH=500]="HIGH",e))(Y||{}),he=(e=>(e[e.NOT_CONNECTED=-1]="NOT_CONNECTED",e[e.MEDIUM=800]="MEDIUM",e[e.HIGH=1500]="HIGH",e))(he||{}),ve=(e=>(e.OFF="off",e.DOTS="dots",e.BAR="bar",e.Auto="auto",e))(ve||{}),I=(e=>(e.NATURAL="orderNatural",e.LATENCY_ASC="orderLatency_asc",e.LATENCY_DESC="orderLatency_desc",e.NAME_ASC="orderName_asc",e.NAME_DESC="orderName_desc",e))(I||{}),O=(e=>(e.EN="en-US",e.ZH="zh-CN",e))(O||{}),ye=(e=>(e.Details="details",e.Close="close",e.ID="ID",e.Type="type",e.Process="process",e.Host="host",e.SniffHost="sniffHost",e.Rule="rules",e.Chains="chains",e.DlSpeed="dlSpeed",e.ULSpeed="ulSpeed",e.Download="dl",e.Upload="ul",e.ConnectTime="connectTime",e.SourceIP="sourceIP",e.SourcePort="sourcePort",e.Destination="destination",e.InboundUser="inboundUser",e))(ye||{});const te=200,be=Object.values(ye),bt={...Object.fromEntries(be.map(e=>[e,!0])),ID:!1};var k=(e=>(e.XS="xs",e.SM="sm",e.MD="md",e.LG="lg",e))(k||{}),wt=(e=>(e.Global="global",e.Rule="rule",e.Direct="direct",e))(wt||{}),we=(e=>(e.Info="info",e.Error="error",e.Warning="warning",e.Debug="debug",e.Silent="silent",e))(we||{});const xt=[200,300,500,800,1e3],Pt=xt[0],Ct={add:"Add",overview:"Overview",proxies:"Proxies",proxiesSettings:"Proxies Settings",rules:"Rules",connections:"Connections",connectionsSettings:"Connections Settings",connectionsDetails:"Connections Details",logs:"Logs",logsSettings:"Logs Settings",config:"Config",upload:"Upload",download:"Download",uploadTotal:"Upload Total",downloadTotal:"Download Total",activeConnections:"Active Connections",memoryUsage:"Memory Usage",traffic:"Traffic",memory:"Memory",down:"Down",up:"Up",proxyProviders:"Proxy Providers",ruleProviders:"Rule Providers",search:"Search",ID:"ID",type:"Type",name:"Name",process:"Process",host:"Host",sniffHost:"Sniff Host",chains:"Chains",connectTime:"Time",dlSpeed:"DL Speed",ulSpeed:"UL Speed",dl:"DL",ul:"UL",sourceIP:"Source IP",sourcePort:"Source Port",destination:"Destination",inboundUser:"Inbound User",close:"Close",reset:"Reset",dnsQuery:"DNS Query",dots:"Dots",bar:"Bar",auto:"Auto",off:"Off",proxiesPreviewType:"Proxies preview type",urlForIPv6SupportTest:"URL for IPv6 support test",urlForLatencyTest:"URL for latency test",autoCloseConns:"Automatically Close connections",useTwemoji:"Use Twemoji Mozilla Font",autoSwitchTheme:"Automatically switch theme",favDayTheme:"Favorite light theme",favNightTheme:"Favorite dark theme",renderInTwoColumns:"Render in two columns",updateGEODatabases:"Update GEO Databases",restartCore:"Restart Core",upgradeCore:"Upgrade Core",proxiesSorting:"Proxies Sorting",orderNatural:"Original order in config file",orderLatency_asc:"By latency from low to high",orderLatency_desc:"By latency from high to low",orderName_asc:"By name alphabetically (A-Z)",orderName_desc:"By name alphabetically (Z-A)",ms:"ms",updated:"Updated",tableSize:"Table size",logLevel:"Log Level",info:"info",silent:"silent",debug:"debug",warning:"warning",error:"error",logMaxRows:"Log Maximum Reserved Rows",xs:"Extra small size",sm:"Small size",md:"Normal size",lg:"Large size",switchEndpoint:"Switch Endpoint",switchLanguage:"Switch Language",latencyTestTimeoutDuration:"Latency Test Timeout Duration",all:"All",sequence:"Sequence",payload:"Payload",details:"Details",endpointURL:"Endpoint URL",secret:"Secret",global:"Global",rule:"Rule",direct:"Direct",active:"Active",closed:"Closed",sort:"Sort",hideUnAvailableProxies:"Hide UnAvailable Proxies",reloadConfig:"Reload Config",flushFakeIP:"Flush Fake-IP",tagClientSourceIPWithName:"Tag Client Source IP With Name",tag:"Tag",coreConfig:"Core Config",xdConfig:"XD Config",version:"Version",expire:"Expire",noExpire:"Null",allowLan:"Allow Lan",enableTunDevice:"Enable TUN Device",tunModeStack:"TUN Mode Stack",tunDeviceName:"TUN Device Name",interfaceName:"Interface Name",en:"English",zh:"Chinese",port:"{{ name }} Port"},$t={add:"添加",overview:"概览",proxies:"代理",proxiesSettings:"代理设置",rules:"规则",connections:"连接",connectionsSettings:"连接设置",connectionsDetails:"连接详情",logs:"日志",logsSettings:"日志设置",config:"配置",upload:"上传",download:"下载",uploadTotal:"上传总量",downloadTotal:"下载总量",activeConnections:"活动连接",memoryUsage:"内存使用情况",traffic:"流量",memory:"内存",down:"下载",up:"上传",proxyProviders:"代理提供者",ruleProviders:"规则提供者",search:"搜索",ID:"ID",type:"类型",name:"名字",process:"进程",host:"主机",sniffHost:"嗅探域名",chains:"链路",connectTime:"连接时间",dlSpeed:"下载速度",ulSpeed:"上传速度",dl:"下载量",ul:"上传量",sourceIP:"源地址",sourcePort:"源端口",destination:"目标地址",inboundUser:"入站用户",close:"关闭",reset:"重置",dnsQuery:"DNS 查询",dots:"点阵",bar:"条形",auto:"自适应",off:"关闭",proxiesPreviewType:"节点组预览样式",urlForIPv6SupportTest:"测试 IPv6 支持链接",urlForLatencyTest:"测速链接",autoCloseConns:"自动断开连接",useTwemoji:"使用 Twemoji Mozilla 字体",autoSwitchTheme:"自动切换主题",favDayTheme:"浅色主题偏好",favNightTheme:"深色主题偏好",renderInTwoColumns:"双列渲染",updateGEODatabases:"更新 GEO 数据库",restartCore:"重启核心",upgradeCore:"更新核心",proxiesSorting:"节点排序",orderNatural:"原配置文件中的排序",orderLatency_asc:"按延迟从低到高",orderLatency_desc:"按延迟从高到低",orderName_asc:"按名称字母排序 (A-Z)",orderName_desc:"按名称字母排序 (Z-A)",ms:"毫秒",updated:"更新于",tableSize:"表格大小",logLevel:"日志等级",info:"信息",silent:"静默",debug:"调试",warning:"警告",error:"错误",logMaxRows:"日志最大保留行数",xs:"超小尺寸",sm:"小尺寸",md:"正常尺寸",lg:"超大尺寸",switchEndpoint:"切换后端",switchLanguage:"切换语言",latencyTestTimeoutDuration:"测速超时时间",all:"全部",sequence:"序列号",payload:"内容",details:"详情",endpointURL:"后端地址",secret:"密钥",global:"全局",rule:"规则",direct:"直连",active:"活动",closed:"已关闭",sort:"排序",hideUnAvailableProxies:"隐藏不可用节点",reloadConfig:"重载配置",flushFakeIP:"清空 Fake-IP",tagClientSourceIPWithName:"为客户端源 IP 地址添加名称标记",tag:"标记",coreConfig:"核心配置",xdConfig:"XD 配置",version:"版本",expire:"到期时间",noExpire:"不限时",allowLan:"允许局域网访问",enableTunDevice:"开启 TUN 转发",tunModeStack:"TUN 模式堆栈",tunDeviceName:"TUN 设备名称",interfaceName:"接口名称",en:"英文",zh:"中文",port:"{{ name }} 端口"},xe={[O.EN]:Ct,[O.ZH]:$t},[St,Vs]=v(d(Reflect.has(xe,navigator.language)?navigator.language:O.EN),{name:"lang",storage:localStorage}),[Tt,Dt]=Fe(e=>[ze(()=>Re(xe[e.locale]),Ne)]),Pe=()=>Dt(),[Js,Zs]=v(d(ve.Auto),{name:"proxiesPreviewType",storage:localStorage}),[Gs,Es]=v(d(I.NATURAL),{name:"proxiesOrderingType",storage:localStorage}),[Qs,Ks]=v(d(!1),{name:"hideUnAvailableProxies",storage:localStorage}),[Ys,en]=v(d(!0),{name:"renderProxiesInTwoColumns",storage:localStorage}),[W,tn]=v(d("https://www.gstatic.com/generate_204"),{name:"urlForLatencyTest",storage:localStorage}),[E,sn]=v(d("https://api-ipv6.ip.sb/ip"),{name:"urlForIPv6SupportTest",storage:localStorage}),[Lt,nn]=v(d(!1),{name:"autoCloseConns",storage:localStorage}),[It,an]=v(d(!0),{name:"useTwemoji",storage:localStorage}),[kt,on]=v(d(!1),{name:"autoSwitchTheme",storage:localStorage}),[Mt,rn]=v(d("nord"),{name:"favDayTheme",storage:localStorage}),[_t,ln]=v(d("sunset"),{name:"favNightTheme",storage:localStorage}),[cn,dn]=v(d(k.XS),{name:"connectionsTableSize",storage:localStorage}),[un,pn]=v(d(bt),{name:"connectionsTableColumnVisibility",storage:localStorage}),[gn,mn]=v(d(be),{name:"connectionsTableColumnOrder",storage:localStorage}),[fn,hn]=v(d([]),{name:"clientSourceIPTags",storage:localStorage}),[vn,yn]=v(d(k.XS),{name:"logsTableSize",storage:localStorage}),[bn,wn]=v(d(we.Info),{name:"logLevel",storage:localStorage}),[xn,Pn]=v(d(Pt),{name:"logMaxRows",storage:localStorage}),Cn=e=>{let t="table-xs";switch(e){case k.XS:t="table-xs";break;case k.SM:t="table-sm";break;case k.MD:t="table-md";break;case k.LG:t="table-lg";break}return t},[R,$n]=v(d(5e3),{name:"latencyTestTimeoutDuration",storage:localStorage}),Ut=()=>W().startsWith("https"),D=()=>Ut()?he:Y,[qt,Ce]=d([]),[$e,jt]=d(null),Sn=()=>{const[e,t]=d([]),[o,s]=d([]),[n,a]=d(!1);return J(()=>{var p;const l=(p=$e())==null?void 0:p.connections;l&&ge(()=>{const i=Se(l,o());if(At(o()),!n()){const r=Ft(i,qt());s(i),t(r.slice(-te))}Ce(r=>r.slice(-(i.length+te)))})}),{closedConnections:e,activeConnections:o,paused:n,setPaused:a}},Se=(e,t)=>{const o=new Map;return t.forEach(s=>o.set(s.id,s)),e.map(s=>{const n=o.get(s.id);return!n||!B.isNumber(n.download)||!B.isNumber(n.upload)?{...s,downloadSpeed:0,uploadSpeed:0}:{...s,downloadSpeed:s.download-n.download,uploadSpeed:s.upload-n.upload}})},At=e=>{Ce(t=>B.unionWith(t,e,(o,s)=>o.id===s.id))},Ft=(e,t)=>B.differenceWith(t,e,(o,s)=>o.id===s.id),Tn=()=>w().delete("connections"),zt=e=>w().delete(`connections/${e}`),[Dn,se]=d(!1),[Ln,ne]=d(!1),[In,ae]=d(!1),[kn,oe]=d(!1),[Mn,re]=d(!1),_n=async()=>{const e=w();se(!0);try{await e.put("configs",{searchParams:{force:!0},json:{path:"",payload:""}})}catch{}se(!1)},Un=async()=>{const e=w();ae(!0);try{await e.post("cache/fakeip/flush")}catch{}ae(!1)},qn=async()=>{const e=w();ne(!0);try{await e.post("configs/geo")}catch{}ne(!1)},jn=async()=>{const e=w();oe(!0);try{await e.post("upgrade")}catch{}oe(!1)},An=async()=>{const e=w();re(!0);try{await e.post("restart")}catch{}re(!1)},Fn=()=>w().get("configs").json(),zn=async(e,t,o)=>{try{await w().patch("configs",{json:{[e]:t}}).json(),await o()}catch(s){Be.error(s.message)}},Nn=async()=>{const e=w(),{version:t}=await e.get("version").json();return t},Nt=()=>w().get("providers/proxies").json(),Rt=()=>w().get("proxies").json(),le=e=>w().put(`providers/proxies/${e}`),Te=e=>w().get(`providers/proxies/${e}/healthcheck`,{timeout:5*1e3}).json(),Bt=(e,t)=>w().put(`proxies/${e}`,{body:JSON.stringify({name:t})}),ie=(e,t,o,s)=>{const n=w();return t!==""?Te(t).then(a=>({delay:a[e]})):n.get(`proxies/${e}/delay`,{searchParams:{url:o,timeout:s}}).json()},ce=(e,t,o)=>w().get(`group/${e}/delay`,{searchParams:{url:t,timeout:o}}).json(),Rn=()=>w().get("rules").json(),Bn=()=>w().get("providers/rules").json(),Hn=e=>w().put(`providers/rules/${e}`),On=async e=>{const t="https://api.github.com/repos/MetaCubeX/mihomo",o=/(alpha|beta|meta)-?(\w+)/.exec(e);if(!o)return!1;const s=o[1],n=o[2];if(s==="meta"){const{assets:a}=await H.get(`${t}/releases/latest`).json();return!a.some(({name:p})=>p.includes(n))}if(s==="alpha"){const{assets:a}=await H.get(`${t}/releases/tags/Prerelease-Alpha`).json();return!a.some(({name:p})=>p.includes(n))}return!1},Wn=e=>e.includes("sing-box"),Xn=e=>/^https?/.test(e)?e:`${window.location.protocol}//${e}`,N=()=>{const[e,t]=d({}),o=(n,a)=>{t({...e(),[n]:a})};return{map:e,set:o,setWithCallback:async(n,a)=>{o(n,!0);try{await a()}catch{}o(n,!1)}}},Ht=(e="")=>{const t=e.toLowerCase();return t.includes("shadowsocks")?t.replace("shadowsocks","ss"):t==="hysteria"?"hy":t==="wireguard"?"wg":t},Ot=(e="")=>{const t=e.toLowerCase();return!["selector","direct","reject","urltest","loadbalance","fallback","relay"].includes(t)},Vn=(e,t,o,s)=>o===I.NATURAL?e:e.sort((n,a)=>{if(s!=null&&s.has(n)&&!(s!=null&&s.has(a)))return-1;if(s!=null&&s.has(a)&&!(s!=null&&s.has(n)))return 1;const l=t[n],p=t[a];switch(o){case I.LATENCY_ASC:return l===D().NOT_CONNECTED?1:p===D().NOT_CONNECTED?-1:l-p;case I.LATENCY_DESC:return l===D().NOT_CONNECTED?1:p===D().NOT_CONNECTED?-1:p-l;case I.NAME_ASC:return n.localeCompare(a);case I.NAME_DESC:return a.localeCompare(n);default:return 0}}),Jn=(e,t,o,s)=>s?e.filter(n=>o!=null&&o.has(n)?!0:t[n]!==D().NOT_CONNECTED):e,{map:Wt,set:Xt}=N(),{map:Vt,setWithCallback:Jt}=N(),{map:Zt,setWithCallback:Gt}=N(),{map:Et,setWithCallback:Qt}=N(),{map:Kt,setWithCallback:Yt}=N(),[es,de]=d(!1),[ts,ss]=d([]),[ns,as]=d(new Set),[ue,os]=d([]),[De,Q]=d({}),[Le,F]=d({}),[Ie,rs]=d({}),ls=e=>{var p;const t={...Ie()},o={...De()},s={...Le()},n=(i,r,u=!0)=>{var h,y,x,b;const m=(h=i.extra)==null?void 0:h[r];if(Array.isArray(m)){const f=(y=m.at(-1))==null?void 0:y.delay;if(f)return f}if(u)return(b=(x=i.history)==null?void 0:x.at(-1))==null?void 0:b.delay},a={};e.forEach(i=>{const{udp:r,xudp:u,type:m,now:h,name:y,provider:x=""}=i;if(t[i.name]={udp:r,xudp:u,type:m,now:h,name:y,provider:x},!h)o[i.name]=n(i,W())||D().NOT_CONNECTED;else if(o[h]!==void 0)o[i.name]=o[h];else{const f=a[h]??new Set;f.add(i.name),a[h]=f}const b=(n(i,E(),!1)??0)>0;s[i.name]=b});const l=Object.keys(a).filter(i=>o[i]!==void 0);for(;l.length>0;){const i=l.shift(),r=o[i];for(const u of((p=a[i])==null?void 0:p.values())??[])o[u]=r,l.push(u)}me(()=>{rs(t),Q(o),F(s)})},X=()=>{const e=async()=>{const[{providers:r},{proxies:u}]=await Promise.all([Nt(),Rt()]),m=[...u.GLOBAL.all??[],"GLOBAL"],h=Object.values(u).filter(b=>{var f;return(f=b.all)==null?void 0:f.length}).sort((b,f)=>m.indexOf(b.name)-m.indexOf(f.name)),y=Object.values(r).filter(b=>b.name!=="default"&&b.vehicleType!=="Compatible"),x=[...Object.values(u),...y.flatMap(b=>b.proxies.filter(f=>!(f.name in u)).map(f=>({...f,provider:b.name})))];me(()=>{ss(h),as(new Set(["DIRECT","REJECT",...h.map(b=>b.name)])),os(y),ls(x)})},t=async(r,u)=>{await Bt(r.name,u),await e(),Lt()&&ge(()=>{var h;const m=Se(((h=$e())==null?void 0:h.connections)??[],[]);m.length>0&&m.forEach(({id:y,chains:x})=>{x.includes(r.name)&&zt(y)})})},o=async(r,u)=>{const m=E();if(!m||m.length===0){F({});return}let h=!1;try{const{delay:y}=await ie(r,u,m,R());h=y>0}catch{h=!1}F(y=>({...y,[r]:h}))},s=async r=>{const u=E();if(!u||u.length===0){F({});return}const m=await ce(r,u,R()),h=Object.fromEntries(Object.entries(m).map(([y,x])=>[y,x>0]));F(y=>({...y,...h}))};return{collapsedMap:Wt,setCollapsedMap:Xt,proxyIPv6SupportMap:Le,proxyLatencyTestingMap:Vt,proxyGroupLatencyTestingMap:Zt,proxyProviderLatencyTestingMap:Et,updatingMap:Kt,isAllProviderUpdating:es,proxies:ts,proxyGroupNames:ns,proxyProviders:ue,proxyLatencyTest:async(r,u)=>{Jt(r,async()=>{const{delay:m}=await ie(r,u,W(),R());Q(h=>({...h,[r]:m}))}),await o(r,u)},proxyGroupLatencyTest:async r=>{Gt(r,async()=>{const u=await ce(r,W(),R());Q(m=>({...m,...u})),await e()}),await s(r)},latencyMap:De,proxyNodeMap:Ie,fetchProxies:e,selectProxyInGroup:t,updateProviderByProviderName:r=>Yt(r,async()=>{try{await le(r)}catch{}await e()}),updateAllProvider:async()=>{de(!0);try{await Promise.allSettled(ue().map(r=>le(r.name))),await e()}finally{de(!1)}},proxyProviderLatencyTest:r=>Qt(r,async()=>{await Te(r),await e()})}},[is,Zn]=v(d(""),{name:"selectedEndpoint",storage:localStorage}),[cs,Gn]=v(d([]),{name:"endpointList",storage:localStorage}),w=()=>{const e=M();if(!e)return H.create({});const t=new Headers;return e.secret&&t.set("Authorization",`Bearer ${e.secret}`),H.create({prefixUrl:e.url,headers:t})},M=()=>cs().find(({id:e})=>e===is()),ds=()=>{var e;return(e=M())==null?void 0:e.secret},us=()=>{var e;return new URL(((e=M())==null?void 0:e.url)??"").origin.replace("http","ws")},ps=(e,t={})=>{const o=new URLSearchParams(t);o.set("token",ds()??"");const s=He(`${us()}/${e}?${o.toString()}`),n=Oe(s,"message");return z(()=>{var l;return n()?JSON.parse((l=n())==null?void 0:l.data):null})},[gs,ke]=v(d("sunset"),{name:"theme",storage:localStorage}),ms=C('<li class="tooltip tooltip-bottom">'),fs=C('<div class="drawer drawer-end w-auto sm:ml-auto"><input id=themes type=checkbox class=drawer-toggle><div class="drawer-content flex items-center"><label for=themes class="btn btn-circle btn-primary drawer-button btn-sm"></label></div><div class="drawer-side overflow-x-hidden"><label for=themes class=drawer-overlay></label><ul class="menu gap-2 rounded-l-box bg-base-300 p-2">'),hs=C('<li class="btn btn-xs">'),vs=C('<div class="navbar-center hidden lg:flex"><ul class="menu menu-horizontal menu-lg gap-2 p-0">'),ys=C('<ul class="navbar z-50 flex w-auto items-center justify-center bg-base-300 px-4 shadow-lg"><div class="navbar-start gap-4"><div class="drawer w-auto lg:hidden"><input id=navs type=checkbox class=drawer-toggle><div class="drawer-content flex items-center"><label for=navs class="btn btn-circle drawer-button btn-sm"></label></div><div class=drawer-side><label for=navs class=drawer-overlay></label><ul class="menu min-h-full w-2/5 gap-2 rounded-r-box bg-base-300 pt-20"></ul></div></div></div><div class=navbar-end><div class="flex items-center gap-2">'),bs=C("<li>"),ws=({href:e,tooltip:t,children:o})=>(()=>{const s=ms();return Z(s,"data-tip",t),g(s,c(K,{class:"rounded-box",href:e,children:o})),s})(),xs=()=>(()=>{const e=fs(),t=e.firstChild,o=t.nextSibling,s=o.firstChild,n=o.nextSibling,a=n.firstChild,l=a.nextSibling;return g(s,c(Ve,{})),g(l,c(G,{each:vt,children:p=>(()=>{const i=hs();return i.$$click=()=>ke(p),Z(i,"data-theme",p),g(i,p),i})()})),e})(),Ps=()=>{const[e]=Pe(),t=()=>[{href:P.Overview,name:e("overview"),icon:c(Je,{})},{href:P.Proxies,name:e("proxies"),icon:c(Ze,{})},{href:P.Rules,name:e("rules"),icon:c(Ge,{})},{href:P.Conns,name:e("connections"),icon:c(Ee,{})},{href:P.Log,name:e("logs"),icon:c(Qe,{})},{href:P.Config,name:e("config"),icon:c(Ke,{})}],o=We(),[s,n]=d(!1);return(()=>{const a=ys(),l=a.firstChild,p=l.firstChild,i=p.firstChild,r=i.nextSibling,u=r.firstChild,m=r.nextSibling,h=m.firstChild,y=h.nextSibling,x=l.nextSibling,b=x.firstChild;return i.addEventListener("change",f=>n(f.target.checked)),g(u,c(Xe,{})),g(y,c(G,{get each(){return t()},children:({href:f,name:A})=>(()=>{const S=bs();return S.$$click=()=>n(!1),g(S,c(K,{href:f,children:A})),S})()})),g(l,c(Ls,{}),null),g(a,c($,{get when(){return o.pathname!==P.Setup},get children(){const f=vs(),A=f.firstChild;return g(A,c(G,{get each(){return t()},children:({href:S,name:Me,icon:_e})=>c(ws,{href:S,tooltip:Me,children:_e})})),f}}),x),g(b,c(xs,{})),U(()=>i.checked=s()),a})()};V(["click"]);const Cs=C('<span class="badge badge-sm p-px"><span class=scale-75>IPv6'),$s=e=>{const{proxyIPv6SupportMap:t}=X(),o=z(()=>t()[e.name]===!0);return c($,{get when(){return o()},get children(){return Cs()}})},Ss=C("<span>"),Ts=e=>{const[t]=Pe(),{latencyMap:o}=X(),[s,n]=d(""),a=z(()=>o()[e.name]);return J(()=>{n("text-success"),a()>D().HIGH?n("text-error"):a()>D().MEDIUM&&n("text-warning")}),c($,{get when(){return z(()=>typeof a()=="number")()&&a()!==Y.NOT_CONNECTED},get children(){const l=Ss();return g(l,a,null),g(l,()=>t("ms"),null),U(()=>_(l,`whitespace-nowrap text-xs ${s()}`)),l}})},Ds=C('<div class="text-md flex items-center gap-1 whitespace-nowrap font-bold uppercase sm:text-xl"><span>(</span><a class="text-primary transition-transform hover:rotate-90 hover:scale-125"href=https://github.com/metacubex/metacubexd target=_blank>xd</a><span>)'),Ls=()=>(()=>{const e=Ds(),t=e.firstChild;return g(e,c(K,{class:"bg-gradient-to-br from-primary to-secondary bg-clip-text text-transparent",get href(){return M()?"/":"/setup"},children:"metacube"}),t),e})(),Is=C('<div class="sticky bottom-0 z-50 flex items-center justify-end bg-base-100 bg-opacity-80 p-4 backdrop-blur"><div class="flex justify-end gap-2">'),ks=C('<dialog class="modal modal-bottom sm:modal-middle"><div class="modal-box p-0"><div><div class="flex items-center gap-4 text-xl font-bold"><span></span></div></div><div class=p-4></div></div><form method=dialog class=modal-backdrop><button>'),Ms="sticky bottom-0 z-50 flex items-center justify-end bg-base-100 bg-opacity-80 p-4 backdrop-blur",En=e=>{let t;return(()=>{const o=ks(),s=o.firstChild,n=s.firstChild,a=n.firstChild,l=a.firstChild,p=n.nextSibling;return Ye(i=>{var r;return(t=i)&&((r=e.ref)==null?void 0:r.call(e,i))},o),s.$$contextmenu=i=>i.preventDefault(),g(a,()=>e.icon,l),g(l,()=>e.title),g(n,c(fe,{class:"btn-circle btn-sm",onClick:()=>t==null?void 0:t.close(),get icon(){return c(et,{size:20})}}),null),g(p,pe(()=>e.children)),g(s,c($,{get when(){return e.action},get children(){const i=Is(),r=i.firstChild;return g(r,()=>e.action),i}}),null),U(()=>_(n,L(Ms,"top-0 justify-between"))),o})()};V(["contextmenu"]);const _s=C('<div><div class="flex items-center justify-between gap-2"><span class="break-all text-left text-sm"></span><span class="flex items-center gap-1"></span></div><div class="flex items-center justify-between gap-1"><div></div><div class=text-xs>'),Qn=e=>{const{proxyLatencyTest:t,proxyLatencyTestingMap:o}=X(),{proxyName:s,isSelected:n,onClick:a}=e,{proxyNodeMap:l}=X(),p=z(()=>l()[s]),i=()=>{var r,u,m;return Ot((r=p())==null?void 0:r.type)?(u=p())!=null&&u.xudp?"xudp":(m=p())!=null&&m.udp?"udp":null:null};return(()=>{const r=_s(),u=r.firstChild,m=u.firstChild,h=m.nextSibling,y=u.nextSibling,x=y.firstChild,b=x.nextSibling;return tt(r,"click",a,!0),Z(r,"title",s),g(m,s),g(h,c($s,{get name(){return e.proxyName}}),null),g(h,c(fe,{class:"btn-circle btn-ghost h-auto min-h-0 w-auto",get icon(){return c(st,{size:20,get class(){return L(o()[s]&&"animate-pulse text-success")}})},onClick:f=>{f.stopPropagation(),t(s,p().provider)}}),null),g(x,()=>{var f;return Ht((f=p())==null?void 0:f.type)},null),g(x,c($,{get when(){return i()},get children(){return` :: ${i()}`}}),null),g(b,c(Ts,{get name(){return e.proxyName}})),U(f=>{const A=L("card card-bordered tooltip-bottom flex flex-col justify-between gap-1 border-neutral-focus bg-neutral p-2 text-neutral-content",n&&"border-primary bg-primary-content text-primary",a&&"cursor-pointer"),S=L("text-xs text-slate-500",n&&"text-primary");return A!==f._v$&&_(r,f._v$=A),S!==f._v$2&&_(x,f._v$2=S),f},{_v$:void 0,_v$2:void 0}),r})()};V(["click"]);const Us=C('<div><div class="flex-1 overflow-y-auto p-2 sm:p-4"><div class=pb-8>'),qs=q(()=>j(()=>import("./Setup-HWZnBjuc.js"),__vite__mapDeps([0,1]),import.meta.url)),js=q(()=>j(()=>import("./Overview-laqXJF4U.js"),__vite__mapDeps([2,1]),import.meta.url)),As=q(()=>j(()=>import("./Connections-EzywPjCl.js"),__vite__mapDeps([3,1,4,5,6]),import.meta.url)),Fs=q(()=>j(()=>import("./Logs-2yQWvdrn.js"),__vite__mapDeps([7,1,4,5]),import.meta.url)),zs=q(()=>j(()=>import("./Proxies-9GSyO1UU.js"),__vite__mapDeps([8,1,6,5]),import.meta.url)),Ns=q(()=>j(()=>import("./Rules-AYnQLyWT.js"),__vite__mapDeps([9,1,6]),import.meta.url)),Rs=q(()=>j(()=>import("./Config-PXl5tFeh.js"),__vite__mapDeps([10,1,5]),import.meta.url)),Bs=()=>{const e=ps("connections");return J(()=>jt(e())),null},Hs=()=>{const e=nt();return J(()=>{kt()&&ke(e()?_t():Mt())}),c(Tt,{get locale(){return St()},get children(){const t=Us(),o=t.firstChild,s=o.firstChild;return g(t,c(Ps,{}),o),g(s,c(at,{get children(){return[c($,{get when(){return M()},get children(){return[c(T,{get path(){return P.Overview},component:js}),c(T,{get path(){return P.Proxies},component:zs}),c(T,{get path(){return P.Rules},component:Ns}),c(T,{get path(){return P.Conns},component:As}),c(T,{get path(){return P.Log},component:Fs}),c(T,{get path(){return P.Config},component:Rs}),c(T,{path:"*",get element(){return c(ot,{get href(){return P.Overview}})}})]}}),c(T,{get path(){return M()?P.Setup:"*"},component:qs})]}}),null),g(s,c($,{get when(){return M()},get children(){return c(Bs,{})}}),null),g(t,c(rt,{position:"bottom-center"}),null),U(n=>{const a=L("relative flex h-screen flex-col overscroll-y-none subpixel-antialiased",It()?"font-twemoji":"font-no-twemoji"),l=gs();return a!==n._v$&&_(t,n._v$=a),l!==n._v$2&&Z(t,"data-theme",n._v$2=l),n},{_v$:void 0,_v$2:void 0}),t}})};lt.extend(it);ct(()=>c(ut,{get source(){return dt()},get children(){return c(Hs,{})}}),document.getElementById("root"));export{Qs as $,wn as A,fe as B,yt as C,Xs as D,Pn as E,xt as F,vn as G,bn as H,xn as I,nn as J,tn as K,we as L,En as M,$n as N,sn as O,Es as P,I as Q,Ks as R,en as S,k as T,Zs as U,ve as V,Lt as W,W as X,R as Y,E as Z,Gs as _,is as a,Ys as a0,Js as a1,D as a2,Ts as a3,X as a4,Jn as a5,Vn as a6,Ws as a7,Qn as a8,Rn as a9,vt as aA,ln as aB,Mt as aC,_t as aD,It as aE,On as aF,Fn as aG,Bn as aa,Hn as ab,N as ac,St as ad,Nn as ae,Wn as af,w as ag,zn as ah,Dn as ai,_n as aj,Ln as ak,qn as al,In as am,Un as an,kn as ao,jn as ap,Mn as aq,An as ar,P as as,wt as at,O as au,an as av,Vs as aw,on as ax,kt as ay,rn as az,Zn as b,ps as c,M as d,cs as e,be as f,bt as g,dn as h,fn as i,hn as j,cn as k,$e as l,qt as m,Sn as n,ye as o,zt as p,gn as q,un as r,Gn as s,Xn as t,Pe as u,Tn as v,mn as w,pn as x,Cn as y,yn as z};
function __vite__mapDeps(indexes) {
  if (!__vite__mapDeps.viteFileDeps) {
    __vite__mapDeps.viteFileDeps = ["./Setup-HWZnBjuc.js","./vendor-LFOJg3vZ.js","./Overview-laqXJF4U.js","./Connections-EzywPjCl.js","./index-015NyoQc.js","./ConfigTitle-hXjZ_Yxi.js","./global-Epb9UJLf.js","./Logs-2yQWvdrn.js","./Proxies-9GSyO1UU.js","./Rules-AYnQLyWT.js","./Config-PXl5tFeh.js"]
  }
  return indexes.map((i) => __vite__mapDeps.viteFileDeps[i])
}
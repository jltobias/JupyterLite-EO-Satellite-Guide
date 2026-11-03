/* Original MIT-licensed research/AOI teaching lab. No asset downloads or orbit predictions. */
"use strict";
(()=>{
 const $=id=>document.getElementById(id),G=window.EOGeometry,O=window.EOOrbits;
 const catalog=window.EO_CATALOG,config=window.EO_GEOMETRY,presets=config.presets,discovery=window.EO_DISCOVERY;
 const esc=v=>String(v??"Not curated").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 const params=new URLSearchParams(location.search),initial=window.EO_INITIAL_SWATH||{};
 const requested=params.get("mission")||initial.mission||"landsat-8";
 const preset=id=>presets.find(p=>p.id===id),satellite=id=>catalog.satellites.find(s=>s.id===id);
 function forResearch(p){if(!p)return p;const concept=state.research.concepts.find(t=>p.measurement_overrides?.[t.id]);if(!concept)return p;const override=p.measurement_overrides[concept.id];return {...p,...override,sources:[...new Set([...p.sources,...override.sources])]};}
 const defaultBox=initial.bbox||[-76,39,-74,41],urlBox=params.get("bbox")?.split(",").map(Number);
 const state={p:preset(requested)||preset("landsat-8"),bbox:G.validBox(urlBox)?urlBox:defaultBox,
  phase:{node:-45,argument:0},time:0,hours:6,playing:false,view:[0,0,1200,600],drawing:false,start:null,
  research:EOResearch.resolve(""),intervals:[],items:[],query:null,request:null,active:null};
 for(const key of ["node","argument"]){const v=Number(params.get(key));if(params.has(key)&&Number.isFinite(v)&&Math.abs(v)<=360)state.phase[key]=v;}
 if([6,12,24].includes(Number(params.get("hours"))))state.hours=Number(params.get("hours"));
 state.time=Math.max(0,Math.min(state.hours*3600,Number(params.get("t"))||0));
 $("lab-question").value=(params.get("q")??initial.question??"").slice(0,500);$("duration").value=String(state.hours);
 if(params.has("from"))$("archive-start").value=params.get("from");if(params.has("until"))$("archive-end").value=params.get("until");
 const xy=p=>[1200*(p.lon+180)/360,600*(90-p.lat)/180];
 function line(points){let out="",last=null;for(const p of points){const [x,y]=xy(p);out+=(last===null||Math.abs(p.lon-last)>180?"M":"L")+x.toFixed(2)+","+y.toFixed(2);last=p.lon;}return out;}
 function polygon(ring){if(!Array.isArray(ring)||!ring.length||ring.length>100000)return "";const raw=ring.map(p=>Array.isArray(p)?{lon:p[0],lat:p[1]}:p),limits=raw.reduce((a,p)=>[Math.min(a[0],p.lon),Math.max(a[1],p.lon)],[Infinity,-Infinity]),span=limits[1]-limits[0];
  const globalRectangle=span>=359&&new Set(raw.map(p=>p.lon)).size<=2;
  const unwrapped=[];let last=raw[0].lon;
  for(const p of raw){let lon=p.lon;if(!globalRectangle){while(lon-last>180)lon-=360;while(lon-last< -180)lon+=360;}unwrapped.push({lon,lat:p.lat});last=lon;}
  return [-1200,0,1200].map(shift=>unwrapped.map((p,i)=>{const [x,y]=xy(p);return `${i?"L":"M"}${(x+shift).toFixed(2)},${y.toFixed(2)}`;}).join("")+"Z").join("");}
 function geometryPath(g){if(!g)return "";const polygons=g.type==="Polygon"?[g.coordinates]:g.type==="MultiPolygon"?g.coordinates:[];return polygons.map(p=>p.map(polygon).join("")).join("");}
 $("study-land").setAttribute("d",window.EO_LAND.features.map(f=>{
  const polygons=f.geometry.type==="Polygon"?[f.geometry.coordinates]:f.geometry.coordinates;
  return polygons.map(p=>p.map(r=>r.map((p,i)=>{const [x,y]=xy({lon:p[0],lat:p[1]});return `${i?"L":"M"}${x.toFixed(2)},${y.toFixed(2)}`;}).join("")+"Z").join("")).join("");
 }).join(""));
 for(let lon=-150;lon<=150;lon+=30){const x=(lon+180)/360*1200;$("study-graticule").insertAdjacentHTML("beforeend",`<path d="M${x} 0V600" stroke="#80a7b5" opacity=".13"/>`);}
 for(let lat=-60;lat<=60;lat+=30){const y=(90-lat)/180*600;$("study-graticule").insertAdjacentHTML("beforeend",`<path d="M0 ${y}H1200" stroke="#80a7b5" opacity=".13"/>`);}
 function sourceLinks(ids){return [...new Set(ids)].map(id=>{const s=catalog.sources[id];return s?`<p class="small"><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.publisher)} · ${esc(s.title)} ↗</a></p>`:"";}).join("");}
 const clock=t=>{const n=Math.round(t),h=Math.floor(n/3600),m=Math.floor(n%3600/60),s=n%60;return `T+${[h,m,s].map(v=>String(v).padStart(2,"0")).join(":")}`;};
 const number=n=>Number(n).toLocaleString(undefined,{maximumFractionDigits:1});
 function fields(){["west","south","east","north"].forEach((id,i)=>$(id).value=String(Math.round(state.bbox[i]*10000)/10000));}
 function save(name,value){const u=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:"application/json"})),a=document.createElement("a");a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
 async function copy(value){try{await navigator.clipboard.writeText(value);$("lab-status").textContent="Copied.";}catch{$("lab-status").textContent=`Copy this value: ${value}`;}}
 function clearObserved(message="No provider request for these settings."){
  state.request?.abort();state.request=null;state.items=[];state.query=null;state.active=null;
  $("observed-footprints").innerHTML="";$("footprint-rows").innerHTML="";$("save-footprints").disabled=true;$("fetch-footprints").disabled=!$("route").value;$("archive-status").textContent=message;
 }
 function setView(view){state.view=view;$("study-map").setAttribute("viewBox",view.join(" "));renderInstant();}
 function zoomBox(){const [w,s,e,n]=state.bbox,a=xy({lon:w,lat:n}),b=xy({lon:e,lat:s});let width=Math.max(80,(b[0]-a[0])*1.8),height=Math.max(60,(b[1]-a[1])*1.8);if(width/height>2)height=width/2;else width=height*2;width=Math.min(1200,width);height=Math.min(600,height);setView([Math.max(0,Math.min(1200-width,(a[0]+b[0]-width)/2)),Math.max(0,Math.min(600-height,(a[1]+b[1]-height)/2)),width,height]);}
 function renderCandidates(){const ids=$("lab-question").value.trim()?[...state.research.platforms]:presets.map(p=>p.id);
  $("candidate-rows").innerHTML=ids.filter(id=>satellite(id)).map(id=>{const s=satellite(id),p=forResearch(preset(id));return `<tr data-candidate="${esc(id)}" class="${id===state.p.id?"active":""}"><td><b>${esc(s.name)}</b><small>${esc(p?.label||s.sensors.map(i=>i.name).join(" / "))}</small></td><td style="--orbit-color:${O.color(s)}"><i class="orbit-dot" aria-hidden="true"></i>${esc(s.orbit.class)}</td><td>${esc(p?.sampling||"Nominal geometry / sampling not curated for this lab")}</td><td>${esc(p?.temporal||s.orbit.temporal_note)}</td><td><button data-use="${esc(id)}" ${p?"":"disabled"}>${p?"Use geometry":"Geometry uncurated"}</button></td></tr>`;}).join("");
 }
 function renderMissionOptions(){const ids=state.research.platforms,matched=presets.filter(p=>ids.has(p.id)),other=presets.filter(p=>!ids.has(p.id));
  $("mission").innerHTML=(matched.length?`<optgroup label="Research candidates">${matched.map(p=>`<option value="${p.id}">${esc(forResearch(p).label)}</option>`).join("")}</optgroup>`:"")+`<optgroup label="Other nominal geometry examples">${other.map(p=>`<option value="${p.id}">${esc(forResearch(p).label)}</option>`).join("")}</optgroup>`;
  $("mission").value=state.p.id;
 }
 function routes(){const direct=discovery.routes.filter(r=>r.id===state.p.route);$("route").innerHTML=direct.map(r=>`<option value="${r.id}">${esc(r.label)}</option>`).join("");$("fetch-footprints").disabled=!direct.length;renderArchiveLinks();}
 function currentRoute(){return discovery.routes.find(r=>r.id===$("route").value);}
 function renderArchiveLinks(){const r=currentRoute();$("archive-links").innerHTML=r?`<p><b>${esc(r.label)}</b> · ${esc(r.format)} · ${esc(r.access_note)}</p><p>Catalog: <code>${esc(r.endpoint)}</code><br>Collection: <code>${esc(r.collection)}</code></p><button id="copy-catalog">Copy catalog URL</button><a href="https://jltobias.github.io/JupyterLite-STAC-Browser/explorer/" target="_blank" rel="noopener">Open JupyterLite STAC Browser ↗</a><p>In that Browser choose Custom HTTPS URL, paste the catalog URL, connect, select this collection and paste the same bbox/dates. A collection URL alone does not advertise search there.</p>`:"No curated collection route for this example.";}
 function renderPixels(){const p=state.p,m=G.metrics(p,state.bbox),color=O.color(p.orbit),widthKm=30*p.pixel_x_m/1000,heightKm=20*p.pixel_y_m/1000;
  const scale=Math.min(270/(30*p.pixel_x_m),140/(20*p.pixel_y_m)),cw=p.pixel_x_m*scale,ch=p.pixel_y_m*scale,w=30*cw,h=20*ch;
  let lines="";for(let x=0;x<=30;x++)lines+=`<path d="M${20+x*cw} 15V${15+h}"/>`;for(let y=0;y<=20;y++)lines+=`<path d="M20 ${15+y*ch}H${20+w}"/>`;
  $("pixel-view").innerHTML=`<rect x="20" y="15" width="${w}" height="${h}" fill="${color}" fill-opacity=".12"/><g stroke="${color}" stroke-width=".5" opacity=".75">${lines}</g><path d="M20 166H${20+w}" stroke="#fff"/><text x="20" y="183">30 cells across = ${esc(number(widthKm))} km</text><text x="${37+w}" y="40">20 cells</text><text x="${37+w}" y="57">${esc(number(heightKm))} km</text>`;
  $("pixel-note").textContent=`${p.sampling} Over this box: roughly ${number(m.columns)} × ${number(m.rows)} cells at that spacing (${number(m.cells)} total), using a local rectangular approximation at the box center. This is a sampling illustration, not acquired pixels or a file-size estimate.`;
 }
 function renderTimeline(){const p=state.p,color=O.color(p.orbit),width=560;
  const spans=p.kind==="geo"?Array.from({length:Math.floor(state.hours*60/p.cadence_minutes)+1},(_,i)=>{const x=20+i*p.cadence_minutes*60/(state.hours*3600)*width;return `<path d="M${x} 22V48" stroke="${color}" stroke-width="3"/>`;}):state.intervals.map(([a,b])=>`<rect x="${20+a/(state.hours*3600)*width}" y="25" width="${Math.max(2,(b-a)/(state.hours*3600)*width)}" height="20" fill="${color}"/>`);
  $("opportunity-view").innerHTML=`<path d="M20 35H580" stroke="#617c90"/>${spans.join("")}<path id="time-cursor" d="M20 12V58" stroke="#fff" stroke-width="2"/><text x="20" y="73">T+0</text><text x="510" y="73">T+${state.hours} hours</text>`;
  $("opportunity-note").textContent=p.kind==="geo"?"Ticks illustrate the stated scan interval only. They are not actual scan times; daylight, regional scheduling, clouds and QA are not simulated.":`${state.intervals.length} approximate proximity interval(s) in this arbitrary-phase model. Distance-to-box is sampled every 10 seconds; this is not rigorous sensor access, measured revisit or a forecast.`;
 }
 function updateScene(){const p=state.p,color=O.color(p.orbit),b=state.bbox,a=xy({lon:b[0],lat:b[3]}),z=xy({lon:b[2],lat:b[1]});
  $("study-box").setAttribute("x",a[0]);$("study-box").setAttribute("y",a[1]);$("study-box").setAttribute("width",z[0]-a[0]);$("study-box").setAttribute("height",z[1]-a[1]);
  const points=[];if(p.kind!=="geo")for(let t=0;t<=state.hours*3600;t+=60)points.push(G.point(p,t,state.phase));
  $("ground-track").setAttribute("d",line(points));$("ground-track").setAttribute("stroke",color);$("current-swath").setAttribute("fill",color+"44");$("current-swath").setAttribute("stroke",color);$("track-key").style.background=color;
  $("geo-key").hidden=p.kind!=="geo";$("align-pass").disabled=p.kind==="geo";
  if(p.kind==="geo"){
   const horizon=G.visibleGeo(p,b).horizon,circle=[];for(let br=0;br<=360;br+=3)circle.push(G.destination({lon:p.longitude_deg,lat:0},br,horizon*Math.PI/180*G.R));
   const e=p.envelope,top=xy({lon:e[0],lat:e[3]}),bottom=xy({lon:e[2],lat:e[1]});
   $("geo-envelope").innerHTML=`<path d="${polygon(circle)}" fill="${color}0c" stroke="${color}" stroke-width="1" vector-effect="non-scaling-stroke"/><rect x="${top[0]}" y="${top[1]}" width="${bottom[0]-top[0]}" height="${bottom[1]-top[1]}" fill="none" stroke="#fff" stroke-dasharray="6 5" vector-effect="non-scaling-stroke"/>`;
  }else $("geo-envelope").innerHTML="";
  state.intervals=G.opportunities(p,b,state.phase,state.hours);
  const m=G.metrics(p,b);$("study-metrics").innerHTML=[["Nominal orbit",`${O.code(p.orbit)} · ${number(p.altitude_km)} km`],["Circular model period",`${number(G.period(p)/60)} min`],[p.kind==="geo"?"Regional scan":"Nominal swath",p.kind==="geo"?"North America":`${number(p.swath_km)} km`],["Approximate study box",`${number(m.width)} × ${number(m.height)} km`]].map(([k,v])=>`<div class="metric">${esc(k)}<strong>${esc(v)}</strong></div>`).join("");
  $("model-time").max=String(state.hours*3600);$("model-time").value=String(state.time);
  $("time-context").innerHTML=`<p>${esc(p.temporal)}</p><p><b>Different quantities:</b> orbit period ${esc(number(G.period(p)/60))} min; ground-track repeat ${p.repeat_days?esc(p.repeat_days)+" days":"not applicable / not specified"}; ${p.cadence_minutes?"stated scan interval "+p.cadence_minutes+" min":"usable revisit is not calculated by this model"}.</p>`;
  $("mission-note").textContent=(state.research.concepts.length&&!state.research.platforms.has(p.id)?"This geometry example is outside the current curated research matches. ":"")+p.limitations;
  $("geometry-sources").innerHTML=sourceLinks(p.sources);$("model-assumptions").textContent=config.model;
  renderPixels();renderTimeline();renderCandidates();renderInstant();
 }
 function renderInstant(){const p=state.p,q=G.point(p,state.time,state.phase),[x,y]=xy(q);$("model-satellite").setAttribute("transform",`translate(${x},${y}) scale(${state.view[2]/1200})`);
  $("model-satellite").querySelector("text").textContent=p.kind==="geo"?"GEO SUBPOINT · MODEL":"MODEL SUBPOINT";
  $("current-swath").setAttribute("d",polygon(G.strip(p,state.time,state.phase)));$("time-label").value=clock(state.time);$("model-time").value=String(state.time);
  const cursor=20+state.time/(state.hours*3600)*560;$("time-cursor")?.setAttribute("d",`M${cursor} 12V58`);
  if(p.kind==="geo"){
   const v=G.visibleGeo(p,state.bbox),inEnvelope=G.overlap(state.bbox,p.envelope);
   $("area-assessment").textContent=`GEO stays fixed relative to Earth in this model. Box center is ${v.center?"inside":"outside"} the spherical-Earth geometric horizon; ${inEnvelope?"the box intersects":"the box is outside"} the advertised TEMPO collection envelope. Neither test establishes instrument coverage, daylight, QA or a valid retrieval. Inspect observed footprints below.`;
  }else{
   const hit=state.intervals.some(([a,b])=>state.time>=a&&state.time<=b);
   $("area-assessment").textContent=`${clock(state.time)} · Model subpoint ${number(q.lon)}°, ${number(q.lat)}°. ${hit?"Within":"Outside"} the half-swath distance-to-box threshold. The shaded strip is a simplified 60-second nadir segment. Real viewing geometry, steering, terrain and acquisition planning are omitted. Inspect observed footprints below.`;
  }
 }
 function applyBox(){const b=["west","south","east","north"].map(id=>$(id).value.trim()===""?NaN:Number($(id).value));if(!G.validBox(b)){$("box-error").textContent="Enter finite W,S,E,N coordinates with west < east and south < north, within ±180°/±90°. Split date-line areas.";return false;}
  $("box-error").textContent="";if(b.some((v,i)=>v!==state.bbox[i])){state.bbox=b;clearObserved();updateScene();}return true;}
 let questionTimer=null;
 function applyQuestion(keep=false){clearTimeout(questionTimer);state.research=EOResearch.resolve($("lab-question").value);const matches=presets.filter(p=>state.research.platforms.has(p.id));
  if(!keep&&matches.length)state.p=matches[0];state.p=forResearch(preset(state.p.id));renderMissionOptions();
  $("question-summary").textContent=!$("lab-question").value.trim()?"Choose a question to connect measurements to candidate missions, or compare the nominal geometry examples.":state.research.concepts.length?`${state.research.platforms.size} candidate platforms; ${matches.length} have geometry presets here. ${state.research.concepts.map(t=>t.caution).join(" ")}`:"No curated concept matches this wording. The displayed geometry is a teaching example, not an inferred answer.";
  $("back-to-research").href=(location.protocol==="file:"?"eo-explorer.html":"https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/")+"?q="+encodeURIComponent($("lab-question").value);clearObserved();routes();updateScene();state.question=$("lab-question").value;
 }
 $("lab-question-form").addEventListener("submit",e=>{e.preventDefault();applyQuestion();});
 $("lab-question").addEventListener("input",()=>{clearTimeout(questionTimer);questionTimer=setTimeout(()=>applyQuestion(),300);});
 document.querySelectorAll("[data-topic]").forEach(b=>b.addEventListener("click",()=>{$("lab-question").value=b.dataset.topic;applyQuestion();}));
 $("mission").addEventListener("change",()=>{state.p=forResearch(preset($("mission").value));state.playing=false;$("play").textContent="▶ Play model";$("play").setAttribute("aria-pressed","false");clearObserved();routes();updateScene();});
 $("candidate-rows").addEventListener("click",e=>{const b=e.target.closest("[data-use]");if(b&&preset(b.dataset.use)){$("mission").value=b.dataset.use;$("mission").dispatchEvent(new Event("change"));}});
 $("apply-bbox").addEventListener("click",applyBox);$("zoom-box").addEventListener("click",zoomBox);$("world-view").addEventListener("click",()=>setView([0,0,1200,600]));
 $("align-pass").addEventListener("click",()=>{if(!applyBox())return;const phase=G.align(state.p,state.bbox);if(!phase){$("lab-status").textContent="The model subpoint cannot reach the box-center latitude. A wide swath may still intersect part of the area; use a different box or compare another mission.";return;}state.phase=phase;state.time=0;$("lab-status").textContent="Illustrative phase aligned to this box at T+0. This is not a real pass prediction.";updateScene();});
 $("duration").addEventListener("change",()=>{state.hours=Number($("duration").value);state.time=Math.min(state.time,state.hours*3600);updateScene();});
 $("model-time").addEventListener("input",()=>{state.time=Number($("model-time").value);renderInstant();});
 $("restart-model").addEventListener("click",()=>{state.time=0;renderInstant();});
 let previous=null;
 function frame(now){if(state.playing){if(previous!==null)state.time=(state.time+Math.min(.1,(now-previous)/1000)*Number($("speed").value))%(state.hours*3600);renderInstant();}previous=now;requestAnimationFrame(frame);}
 $("play").addEventListener("click",()=>{state.playing=!state.playing;$("play").textContent=state.playing?"Ⅱ Pause model":"▶ Play model";$("play").setAttribute("aria-pressed",String(state.playing));previous=null;});
 const map=$("study-map");
 function mapPoint(e){const point=map.createSVGPoint();point.x=e.clientX;point.y=e.clientY;const local=point.matrixTransform(map.getScreenCTM().inverse());return {lon:Math.max(-180,Math.min(180,local.x/1200*360-180)),lat:Math.max(-90,Math.min(90,90-local.y/600*180))};}
 $("draw-bbox").addEventListener("click",()=>{state.drawing=!state.drawing;map.classList.toggle("drawing",state.drawing);$("draw-bbox").setAttribute("aria-pressed",String(state.drawing));$("lab-status").textContent=state.drawing?"Drag a rectangle on the map. Typed bounds remain available.":"Drawing canceled.";});
 map.addEventListener("pointerdown",e=>{if(!state.drawing)return;state.start=mapPoint(e);map.setPointerCapture(e.pointerId);$("draw-preview").removeAttribute("hidden");});
 map.addEventListener("pointermove",e=>{if(!state.start)return;const p=mapPoint(e),a=xy(state.start),b=xy(p),r=$("draw-preview");r.setAttribute("x",Math.min(a[0],b[0]));r.setAttribute("y",Math.min(a[1],b[1]));r.setAttribute("width",Math.abs(a[0]-b[0]));r.setAttribute("height",Math.abs(a[1]-b[1]));});
 function finishDraw(e,cancel=false){if(!state.start)return;const p=mapPoint(e),a=state.start;state.start=null;$("draw-preview").setAttribute("hidden","");state.drawing=false;map.classList.remove("drawing");$("draw-bbox").setAttribute("aria-pressed","false");if(!cancel){const b=[Math.min(a.lon,p.lon),Math.min(a.lat,p.lat),Math.max(a.lon,p.lon),Math.max(a.lat,p.lat)];if(G.validBox(b)&&b[2]-b[0]>.05&&b[3]-b[1]>.05){state.bbox=b;fields();clearObserved();updateScene();$("lab-status").textContent="Study area updated. The model phase is unchanged; align a demonstration pass explicitly if desired.";}}}
 map.addEventListener("pointerup",e=>finishDraw(e));map.addEventListener("pointercancel",e=>finishDraw(e,true));
 function studyBrief(){if(state.question!==$("lab-question").value)applyQuestion();return {profile:"eo-study-area/1",question:state.question,concepts:state.research.concepts.map(t=>t.id),candidate_platforms:[...state.research.platforms],bbox:state.bbox,crs:"OGC:CRS84",mission:state.p.id,nominal_preset:state.p,model:{phase:state.phase,hours:state.hours,elapsed_seconds:state.time,assumptions:config.model},archive_dates:{start:$("archive-start").value,end:$("archive-end").value},route:currentRoute()||null,qualification:"Research planning and illustrative geometry, not a pass prediction, acquired-data receipt or FieldWork import.",catalog_snapshot:catalog.verified};}
 $("save-study").addEventListener("click",()=>{if(applyBox())save("eo-study-area.json",studyBrief());});
 $("copy-bbox").addEventListener("click",()=>{if(applyBox())void copy(state.bbox.map(v=>Math.round(v*1e5)/1e5).join(","));});
 $("share-study").addEventListener("click",()=>{if(!applyBox())return;if(state.question!==$("lab-question").value)applyQuestion();const u=new URL("https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/swaths.html");for(const [k,v] of Object.entries({q:state.question,mission:state.p.id,bbox:state.bbox.join(","),node:state.phase.node,argument:state.phase.argument,hours:state.hours,t:Math.round(state.time),from:$("archive-start").value,until:$("archive-end").value}))u.searchParams.set(k,String(v));void copy(u.href);});
 function safeURL(value,base){if(typeof value!=="string"||!value.trim())return null;try{const u=new URL(value,base);if(u.protocol!=="https:"||u.username||u.password||[...u.searchParams.keys()].some(k=>/token|signature|credential|api_key/i.test(k)))return null;return u.href;}catch{return null;}}
 function itemPlatform(item){const v=item.properties?.platform;return Array.isArray(v)?v.join(", "):String(v||"Not supplied");}
 function platformMatches(item){let p=itemPlatform(item).toLowerCase().replace(/[^a-z0-9]/g,"");if(p==="is40e")p="intelsat40e";return p===state.p.id.replace(/[^a-z0-9]/g,"");}
 function itemURL(item){return safeURL(item.links?.find(l=>l.rel==="self")?.href,state.query.url)||state.query.collection_url+"/items/"+encodeURIComponent(item.id);}
 function highlightItem(index){state.active=index;document.querySelectorAll("[data-observed]").forEach(e=>e.classList.toggle("active",e.dataset.observed===String(index)));}
 function renderObserved(){
  $("observed-footprints").innerHTML=state.items.map((item,i)=>`<path class="footprint" data-observed="${i}" d="${geometryPath(item.geometry)}" fill-rule="evenodd" tabindex="0" role="button" aria-label="Observed STAC footprint ${esc(item.id)}"><title>${esc(item.id)} · ${esc(itemPlatform(item))}</title></path>`).join("");
  $("footprint-rows").innerHTML=state.items.map((item,i)=>`<tr class="footprint-row" data-observed="${i}"><td><button data-footprint="${i}">${esc(item.id)}</button></td><td>${esc(itemPlatform(item))}<small>${platformMatches(item)?"Matches selected platform":"Other / unspecified platform; inspect metadata"}</small></td><td>${esc(item.properties?.datetime||item.properties?.start_datetime||"Not supplied")}</td><td><a href="${esc(itemURL(item))}" target="_blank" rel="noopener">Original Item metadata ↗</a></td></tr>`).join("");
  $("save-footprints").disabled=!state.items.length;
 }
 for(const id of ["observed-footprints","footprint-rows"]){$(id).addEventListener("pointerover",e=>{const row=e.target.closest("[data-observed]");if(row)highlightItem(row.dataset.observed);});$(id).addEventListener("focusin",e=>{const row=e.target.closest("[data-observed]");if(row)highlightItem(row.dataset.observed);});$(id).addEventListener("click",e=>{const row=e.target.closest("[data-observed]");if(row)highlightItem(row.dataset.observed);});}
 async function readBounded(response){if(!response.body)throw new Error("Provider response has no body");const reader=response.body.getReader(),chunks=[];let size=0;for(;;){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>6_000_000){await reader.cancel();throw new Error("Metadata response exceeded the 6 MB limit");}chunks.push(value);}const bytes=new Uint8Array(size);let offset=0;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length;}return JSON.parse(new TextDecoder().decode(bytes));}
 function validDate(value){return /^\d{4}-\d{2}-\d{2}$/.test(value)&&!isNaN(Date.parse(value))&&new Date(value).toISOString().slice(0,10)===value;}
 $("fetch-footprints").addEventListener("click",async()=>{if(!applyBox())return;const r=currentRoute(),start=$("archive-start").value,end=$("archive-end").value;if(!r)return;if(!validDate(start)||!validDate(end)||end<start){$("archive-status").textContent="Choose valid archive dates with From on or before Until.";return;}
  clearObserved("Requesting public Item metadata only…");const controller=new AbortController();state.request=controller;$("fetch-footprints").disabled=true;
  const u=new URL(r.collection_url.replace(/\/$/,"")+"/items");u.searchParams.set("bbox",state.bbox.join(","));u.searchParams.set("datetime",`${start}T00:00:00Z/${end}T23:59:59Z`);u.searchParams.set("limit","10");
  const timer=setTimeout(()=>controller.abort(),25000);
  try{const response=await fetch(u.href,{credentials:"omit",headers:{Accept:"application/geo+json,application/json"},signal:controller.signal});if(!response.ok)throw new Error(`Provider HTTP ${response.status}`);const data=await readBounded(response);if(state.request!==controller)return;
   if(data.type!=="FeatureCollection"||!Array.isArray(data.features))throw new Error("Provider did not return a STAC ItemCollection");
   state.items=data.features.slice(0,10).filter(f=>f&&f.type==="Feature"&&f.id&&f.properties&&typeof f.properties==="object");state.query={url:u.href,collection:r.collection,collection_url:r.collection_url,bbox:[...state.bbox],start,end,retrieved:new Date().toISOString()};renderObserved();
   const matching=state.items.filter(platformMatches).length,geometryCount=state.items.filter(item=>["Polygon","MultiPolygon"].includes(item.geometry?.type)).length;$("archive-status").textContent=`${state.items.length} Item metadata record(s), ${geometryCount} polygon footprint(s); ${matching} explicitly name the selected platform. This is a bounded archive sample, not complete coverage or a future acquisition forecast. No data assets requested.`;
  }catch(error){if(state.request===controller)$("archive-status").textContent=error.name==="AbortError"?"Metadata request timed out or was canceled. Retry or continue in the provider browser.":`${error.message}. Provider CORS, access or availability may prevent metadata retrieval; the teaching model remains available.`;}
  finally{clearTimeout(timer);if(state.request===controller){state.request=null;$("fetch-footprints").disabled=false;}}
 });
 $("save-footprints").addEventListener("click",()=>{if(!state.query)return;save("eo-study-footprints.geojson",{type:"FeatureCollection",features:state.items.map(item=>({type:"Feature",id:item.id,geometry:item.geometry,properties:{platform:itemPlatform(item),datetime:item.properties?.datetime||null,collection:item.collection||state.query.collection,source:itemURL(item),selected_platform_match:platformMatches(item)}})),provenance:state.query,qualification:"STAC metadata footprints only; no assets, valid-pixel masks or scientific QA have been obtained."});});
 $("archive-links").addEventListener("click",e=>{if(e.target.closest("#copy-catalog"))void copy(currentRoute().endpoint);});
 $("route").addEventListener("change",()=>{clearObserved();renderArchiveLinks();});for(const id of ["archive-start","archive-end"])$(id).addEventListener("change",()=>clearObserved());
 $("lab-fullscreen").addEventListener("click",async()=>{if(document.body.classList.contains("lab-window")){if(document.fullscreenElement)await document.exitFullscreen();document.body.classList.remove("lab-window");$("lab-fullscreen").textContent="Full screen";return;}document.body.classList.add("lab-window");$("lab-fullscreen").textContent="Exit full screen";try{if(document.fullscreenEnabled)await document.documentElement.requestFullscreen();}catch{/* Viewport layout remains available. */}});
 document.addEventListener("fullscreenchange",()=>{if(!document.fullscreenElement){document.body.classList.remove("lab-window");$("lab-fullscreen").textContent="Full screen";}});
 document.addEventListener("keydown",e=>{if(e.key==="Escape"){state.drawing=false;state.start=null;map.classList.remove("drawing");$("draw-preview").setAttribute("hidden","");$("draw-bbox").setAttribute("aria-pressed","false");if(document.fullscreenElement)void document.exitFullscreen().catch(()=>{});document.body.classList.remove("lab-window");$("lab-fullscreen").textContent="Full screen";}});
 window.addEventListener("pagehide",()=>state.request?.abort());
 fields();applyQuestion(params.has("mission")||Boolean(initial.mission));if(!preset(requested))$("lab-status").textContent=`No nominal geometry preset for ${satellite(requested)?.name||requested}; showing a clearly labeled Landsat 8 teaching example. No orbit or swath has been inferred for the requested record.`;
 requestAnimationFrame(frame);
})();

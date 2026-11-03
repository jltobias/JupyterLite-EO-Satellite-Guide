/* Original MIT-licensed UI. All catalog strings are escaped before HTML use. */
"use strict";
(() => {
  const catalog = window.EO_CATALOG;
  const land = window.EO_LAND;
  const discovery = window.EO_DISCOVERY;
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? "Unknown / not curated").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const families = {multispectral:{label:"Multispectral",color:"#60dfc4",symbol:"square"},radar:{label:"Radar",color:"#bb9cf5",symbol:"diamond"},hyperspectral:{label:"Hyperspectral",color:"#f29d81",symbol:"hexagon"},weather:{label:"Weather radiometry",color:"#84b7f6",symbol:"circle"},ocean:{label:"Ocean colour",color:"#f2d879",symbol:"triangle"},atmosphere:{label:"Atmospheric chemistry",color:"#ffcf91",symbol:"cross"},other:{label:"STAC metadata discovery",color:"#b6c8d4",symbol:"octagon"}};
  const orbitModel=window.EOOrbits;
  const state = {selected:null,pins:new Set(),brush:null,ascending:true,sorted:false,page:0,view:[0,0,1200,650],research:window.EOResearch.resolve("")};
  const pageSize=13;
  const orbitCode=s=>orbitModel.code(s);
  const pageList=()=>visible().slice(state.page*pageSize,(state.page+1)*pageSize);
  const workspace = {active:false,native:false,scrollY:0,focus:null};
  const filters = ["search","agency","type","orbit","status","property","application"];
  const svgNS = "http://www.w3.org/2000/svg";
  const byId = id => catalog.satellites.find(s => s.id === id);
  const sources = ids => `<span class="source-links">${[...new Set(ids)].map(id => { const s=catalog.sources[id]; return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer" title="${esc(s.title)}">[${esc(id)}] ↗</a>`; }).join(" ")}</span>`;
  const altitude = s => s.orbit.altitude_km == null ? "Unknown / not curated" : `${s.orbit.altitude_km.toLocaleString()} km (nominal)`;
  function optionList(id, values) { $(id).insertAdjacentHTML("beforeend", [...new Set(values)].sort().map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join("")); }
  optionList("agency",catalog.satellites.map(s=>s.agency));
  $("type").insertAdjacentHTML("beforeend",Object.entries(families).map(([k,v])=>`<option value="${k}">${v.label}</option>`).join(""));
  optionList("orbit",catalog.satellites.map(s=>s.orbit.class));
  $("orbit").insertAdjacentHTML("beforeend",'<option value="all-leo">All LEO (including SSO)</option><option value="other-leo">Other LEO (excluding SSO)</option>');
  optionList("status",catalog.satellites.map(s=>s.status));
  optionList("property",catalog.satellites.flatMap(s=>s.sensors.flatMap(i=>i.observes)));
  $("application").insertAdjacentHTML("beforeend",catalog.applications.map(a=>`<option value="${a.id}">${esc(a.name)}</option>`).join(""));
  function visible() {
    const q=$("search").value.trim().toLowerCase();
    const matches=catalog.satellites.filter(s=>(!$("question").value.trim()||!$("research-only").checked||state.research.platforms.has(s.id))&&(!q||JSON.stringify(s).toLowerCase().includes(q))&&(!$("agency").value||s.agency===$("agency").value)&&(!$("type").value||s.type===$("type").value)&&orbitModel.matches(s,$("orbit").value)&&(!$("status").value||s.status===$("status").value)&&(!$("property").value||s.sensors.some(i=>i.observes.includes($("property").value)))&&(!$("application").value||catalog.applications.find(a=>a.id===$("application").value).satellites.includes(s.id)));
    return state.sorted?matches.sort((a,b)=>state.ascending?a.name.localeCompare(b.name):b.name.localeCompare(a.name)):matches;
  }
  function pathForLand() {
    const polygons=land.features.flatMap(f=>f.geometry.type==="Polygon"?[f.geometry.coordinates]:f.geometry.coordinates);
    return polygons.map(p=>p.map(ring=>ring.map(([lon,lat],i)=>`${i?"L":"M"}${(180+(lon+180)/360*840).toFixed(2)},${(180+(90-lat)/180*310).toFixed(2)}`).join("")+"Z").join("")).join("");
  }
  $("land").setAttribute("d",pathForLand());
  for(let lon=-150;lon<=150;lon+=30){const x=180+(lon+180)/360*840;$("graticule").insertAdjacentHTML("beforeend",`<path d="M${x} 180V490" stroke="#82b1bf" opacity=".12"/>`);}
  for(let lat=-60;lat<=60;lat+=30){const y=180+(90-lat)/180*310;$("graticule").insertAdjacentHTML("beforeend",`<path d="M180 ${y}H1020" stroke="#82b1bf" opacity=".12"/>`);}
  function shape(type) {
    if(type==="radar")return '<path d="M0 -8L8 0 0 8 -8 0Z"/>';
    if(type==="hyperspectral")return '<path d="M-8 0L-4 -7H4L8 0 4 7H-4Z"/>';
    if(type==="ocean")return '<path d="M0 -9L9 7H-9Z"/>';
    if(type==="weather")return '<circle r="7"/>';
    if(type==="atmosphere")return '<path d="M-3 -8H3V-3H8V3H3V8H-3V3H-8V-3H-3Z"/>';
    if(type==="other")return '<path d="M-3 -8H3L8 -3V3L3 8H-3L-8 3V-3Z"/>';
    return '<rect x="-6" y="-6" width="12" height="12"/>';
  }
  catalog.satellites.forEach(s=>{
    const g=document.createElementNS(svgNS,"g");g.setAttribute("class",`sat-node ${s.status}`);g.setAttribute("data-id",s.id);g.setAttribute("id",`node-${s.id}`);g.setAttribute("role","button");g.setAttribute("tabindex","0");g.setAttribute("aria-label",`${s.name}, ${families[s.type].label}, ${s.orbit.class}, ${s.status}. Open details.`);g.setAttribute("aria-pressed","false");g.setAttribute("transform",`translate(${s.display.x},${s.display.y})`);g.style.setProperty("--family",families[s.type].color);
    g.innerHTML=`<title>${esc(s.name)}: ${esc(s.sensors.map(i=>i.name).join(", "))}; ${esc(s.orbit.class)}. ${esc(s.record_kind||"curated mission")}</title><rect class="hit" x="-85" y="-28" width="170" height="76" rx="7"/><circle class="halo" r="22"/><g class="sat-glyph" stroke="var(--encoding)" stroke-width="1.3" fill="none"><path d="M-17 -7H-8V7H-17ZM8 -7H17V7H8ZM-8 0H8"/><g class="sensor-shape" fill="var(--encoding)" fill-opacity=".3">${shape(s.type)}</g></g><circle class="pin-marker" cx="20" cy="-18" r="4"/><text y="-30" text-anchor="middle" class="sat-orbit">${orbitCode(s)}</text><text y="39" text-anchor="middle" class="sat-label">${esc(s.name)}</text><text y="53" text-anchor="middle" class="sat-meta">${esc(s.agency)}</text>`;
    g.addEventListener("click",()=>select(s.id));g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select(s.id);}});g.addEventListener("pointerenter",()=>brush(s.id));g.addEventListener("pointerleave",()=>brush(null));g.addEventListener("focus",()=>brush(s.id));g.addEventListener("blur",()=>brush(null));$("satellites").append(g);
  });
  document.querySelectorAll(".sat-label").forEach(label=>{if(label.textContent.length>24)label.textContent=label.textContent.slice(0,22)+"…";});
  $("legend").innerHTML=Object.entries(families).map(([id,f])=>`<button data-family="${id}" aria-pressed="false" style="--family:${f.color}"><svg viewBox="-12 -12 24 24" aria-hidden="true">${shape(id)}</svg>${f.label}</button>`).join("")+'<span class="legend-note">Solid halo: operational source snapshot · dashed: retired · dotted: unverified · gold dot: pinned</span>';
  $("legend").addEventListener("click",e=>{const b=e.target.closest("button");if(b){$("type").value=$("type").value===b.dataset.family?"":b.dataset.family;state.page=0;render();}});
  $("orbit-key").innerHTML=orbitModel.types.map(t=>`<button data-orbit="${esc(t.filter)}" aria-pressed="false" style="--orbit-color:${t.color}" title="${esc(t.description)}"><i aria-hidden="true"></i>${esc(t.label)}</button>`).join("")+'<a href="../book/orbit-guide.html" target="_blank" rel="noopener">Orbit guide ↗</a>';
  $("orbit-key").addEventListener("click",e=>{const b=e.target.closest("[data-orbit]");if(b){$("orbit").value=$("orbit").value===b.dataset.orbit?"":b.dataset.orbit;state.page=0;render();}});
  function applyEncoding(){
    const mode=$("color-mode").value;document.body.dataset.colorMode=mode;
    catalog.satellites.forEach(s=>{const color=mode==="orbit"?orbitModel.color(s):families[s.type].color;
      for(const e of [$(`node-${s.id}`),$(`row-${s.id}`)])if(e){e.style.setProperty("--encoding",color);e.style.setProperty("--orbit-color",orbitModel.color(s));}
    });
    $("encoding-note").textContent=mode==="orbit"?"Color = orbit type · central shape = sensing family · outer gold highlight = research match.":"Color + central shape = sensing family · orbit labels and table swatches retain orbit information.";
  }
  $("color-mode").addEventListener("change",applyEncoding);
  function brush(id) {
    state.brush=id; syncHighlights();
    if(workspace.active&&id){
      // Scroll only the table pane when a short viewport cannot show every row.
      const row=$(`row-${id}`), pane=$("catalog").querySelector(".table-scroll");
      if(row){
        const r=row.getBoundingClientRect(),p=pane.getBoundingClientRect(),head=$("mission-table").tHead.getBoundingClientRect().height;
        if(r.top<p.top+head)pane.scrollTop-=p.top+head-r.top;
        else if(r.bottom>p.bottom)pane.scrollTop+=r.bottom-p.bottom;
      }
    }
  }
  function syncHighlights() {
    document.querySelectorAll(".sat-node,.mission-row").forEach(e=>{const id=e.dataset.id;e.classList.toggle("is-brushed",id===state.brush);e.classList.toggle("is-selected",id===state.selected);e.classList.toggle("pinned",state.pins.has(id));if(e.classList.contains("sat-node"))e.setAttribute("aria-pressed",String(id===state.selected));});
    document.querySelectorAll("[data-select]").forEach(e=>e.setAttribute("aria-expanded",String(e.dataset.select===state.selected)));
    const active=byId(state.brush||state.selected);
    $("brush-readout").textContent=active?`${active.name} · ${orbitCode(active)} / ${active.orbit.class} · ${families[active.type].label}`:"Hover or focus a satellite or row to link the views.";
  }
  function workspacePanel(name,open) {
    document.body.classList.toggle(`workspace-${name}-open`,open);
    $(`workspace-${name}`).setAttribute("aria-expanded",String(open));
  }
  function endWorkspace() {
    if(!workspace.active)return;
    workspace.active=false;workspace.native=false;
    document.body.classList.remove("workspace-mode","workspace-filters-open","workspace-details-open","workspace-compare-open","workspace-research-open");
    ["filters","details","compare","research"].forEach(name=>$(`workspace-${name}`).setAttribute("aria-expanded","false"));
    $("fullscreen").setAttribute("aria-pressed","false");
    workspace.focus?.focus({preventScroll:true});
    window.scrollTo(0,workspace.scrollY);
  }
  async function exitWorkspace() {
    if(document.fullscreenElement===$("poster")){
      try{await document.exitFullscreen();}catch{/* Window-fit layout can still be exited. */}
    }
    endWorkspace();
  }
  $("fullscreen").addEventListener("click",async()=>{
    if(workspace.active)return;
    workspace.scrollY=window.scrollY;workspace.focus=document.activeElement;workspace.active=true;
    document.body.classList.add("workspace-mode");
    $("fullscreen").setAttribute("aria-pressed","true");
    $("exit-workspace").textContent="Exit workspace";
    setView([0,0,1200,650]);
    if(document.fullscreenEnabled&&$("poster").requestFullscreen){
      try{await $("poster").requestFullscreen();}catch{/* Retain the same fit-to-window workspace when fullscreen is unavailable. */}
    }
    if(workspace.active){
      $("exit-workspace").focus({preventScroll:true});
      $("announcement").textContent="Linked workspace open. The constellation and mission table share this view. Escape exits.";
    }
  });
  $("exit-workspace").addEventListener("click",exitWorkspace);
  document.addEventListener("fullscreenchange",()=>{
    if(document.fullscreenElement===$("poster")){
      if(!workspace.active){void document.exitFullscreen();return;}
      workspace.native=true;$("exit-workspace").textContent="Exit full screen";
    }else if(workspace.native){endWorkspace();}
  });
  ["filters","details","compare","research"].forEach(name=>{
    $(`workspace-${name}`).addEventListener("click",()=>{
      const open=$(`workspace-${name}`).getAttribute("aria-expanded")!=="true";
      workspacePanel(name,open);
      if(name==="details"&&open)$("inspector").querySelector("button")?.focus({preventScroll:true});
    });
  });
  $("workspace-close-comparison").addEventListener("click",()=>{workspacePanel("compare",false);$("workspace-compare").focus({preventScroll:true});});
  function pin(id) {
    const active=document.activeElement, fromRows=!!active?.closest("#rows"), fromInspector=!!active?.closest("#inspector");
    state.pins.has(id)?state.pins.delete(id):state.pins.add(id);renderRows();renderComparison();if(state.selected)renderInspector();syncHighlights();
    if(fromRows)$("rows").querySelector(`[data-pin="${id}"]`)?.focus({preventScroll:true});
    if(fromInspector)$("inspector").querySelector(`[data-pin="${id}"]`)?.focus({preventScroll:true});
    $("announcement").textContent=`${byId(id).name} ${state.pins.has(id)?"pinned":"unpinned"}. ${state.pins.size} missions pinned.`;
  }
  function setView(v) { state.view=v;$("constellation").setAttribute("viewBox",v.join(" ")); }
  function select(id) {
    if(state.selected===id){closeDetail();return;}
    state.selected=id;renderInspector();syncHighlights();
    const s=byId(id),position=$(`node-${id}`).transform.baseVal.consolidate().matrix;if(!workspace.active)setView([Math.max(0,Math.min(320,position.e-440)),Math.max(0,Math.min(170,position.f-240)),880,480]);
    $("announcement").textContent=workspace.active?`${s.name} selected in both views. Use Details for sensor metadata.`:`${s.name} selected. Details and sources are open. Use Overview to restore the atlas.`;
  }
  const initialInspector=$("inspector").innerHTML;
  function closeDetail() {state.selected=null;$("inspector").innerHTML=initialInspector;workspacePanel("details",false);setView([0,0,1200,650]);syncHighlights();}
  function renderInspector() {
    const s=byId(state.selected);if(!s)return;
    const sensorHTML=s.sensors.map(i=>`<details class="sensor"><summary>${esc(i.name)} · unfold sensor</summary><div class="sensor-content"><p>${esc(i.method)}</p><h4>Observed properties</h4><p>${esc(i.observes.join(" · "))}</p><h4>Spatial resolution / sampling</h4><p>${esc(i.spatial)}</p><h4>Spectral characteristics</h4><p>${esc(i.spectral)}</p><h4>Coverage</h4><p>${esc(i.coverage)}</p>${sources(i.sources)}<h4>Data products</h4>${i.products.map(p=>`<details class="product"><summary>${esc(p.name)}</summary><p><b>${esc(p.level)}</b></p><p>${esc(p.note)}</p><p><a target="_blank" rel="noopener noreferrer" href="${esc(p.access)}">Open data access ↗</a></p>${sources(p.sources)}</details>`).join("")}</div></details>`).join("");
    const applications=catalog.applications.filter(a=>a.satellites.includes(s.id));
    $("inspector").innerHTML=`<div class="detail-head"><span class="eyebrow">PLATFORM / EVIDENCE</span><button data-close aria-label="Close satellite details">× Close</button></div><h3 class="detail-name">${esc(s.name)}</h3><span class="badge ${s.status}">${esc(s.status)}</span><p class="detail-purpose">${esc(s.purpose)}</p><button class="pin-button" data-pin="${s.id}" aria-pressed="${state.pins.has(s.id)}">${state.pins.has(s.id)?"✓ Pinned for comparison":"+ Pin for comparison"}</button><dl class="facts"><div><dt>Operator</dt><dd>${esc(s.agency)}</dd></div><div><dt>Region</dt><dd>${esc(s.region)}</dd></div><div><dt>Orbit</dt><dd>${esc(s.orbit.class)}</dd></div><div><dt>Altitude</dt><dd>${altitude(s)}</dd></div><div><dt>Launch</dt><dd>${esc(s.launch)}</dd></div><div><dt>Mission end</dt><dd>${s.end?esc(s.end):"Not recorded"}</dd></div></dl><p class="detail-note">${esc(s.orbit.temporal_note)}</p><p class="detail-note">${esc(s.status_note)}</p>${sensorHTML}<details class="evidence-groups"><summary>Evidence by field · verified ${esc(s.verified)}</summary>${Object.entries(s.evidence).map(([group,ids])=>`<p><b>${esc(group)}</b>${sources(ids)}</p>`).join("")}</details>${applications.map(a=>`<details class="pathway"><summary>${esc(a.name)} →</summary><h4>${esc(a.evidence_type)}</h4>${a.historical_platform?`<p><b>${esc(a.historical_platform)}</b></p>`:""}<ol>${a.chain.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>${a.design?`<p>${esc(a.design)}</p><p>${esc(a.finding)}</p>`:""}<p class="detail-note">${esc(a.limitations)}</p>${sources(a.sources)}</details>`).join("")}`;
    const routes=discovery.routes.filter(r=>r.platforms.includes(s.id));
    const hasGeometry=window.EO_GEOMETRY.presets.some(p=>p.id===s.id),studyURL=new URL("https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/swaths.html");if(hasGeometry)studyURL.searchParams.set("mission",s.id);if($("question").value)studyURL.searchParams.set("q",$("question").value);
    $("inspector").insertAdjacentHTML("beforeend",`<p>${hasGeometry?"":"Nominal swath geometry is not curated for this record. "}<a class="study-link" href="${esc(studyURL.href)}" target="_blank" rel="noopener">${hasGeometry?"Study this mission’s swath and study-area geometry":"Compare curated geometry examples"} ↗</a></p>`);
    $("inspector").insertAdjacentHTML("beforeend",`<p class="detail-note">Record: ${esc(s.record_kind||"curated spacecraft")}. ${s.stac_imported&&!s.sensor_curation?"Discovery metadata; instrument lists may describe a mixed collection. Specifications are not operator-verified.":"Selected instruments and source-backed teaching specifications."}</p>${routes.length?'<h4>Research data pathways</h4>'+routes.map(r=>`<p><a href="${esc(r.collection_url)}" target="_blank" rel="noopener">${esc(r.label)} ↗</a><br><small>${esc(r.access_note)}</small></p>`).join(""):""}${s.stac_collections?.length?`<details><summary>${s.stac_collections.length} STAC metadata mentions</summary><p class="detail-note">A mention is not proof of current operations or usable assets. Groupings and derived collections may overlap.</p>${s.stac_collections.map(r=>`<p><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.catalog)} / ${esc(r.id)}</a></p>`).join("")}</details>`:""}`);
  }
  $("inspector").addEventListener("click",e=>{if(e.target.closest("[data-close]")){const id=state.selected;closeDetail();document.getElementById(`node-${id}`)?.focus();}if(e.target.closest("[data-pin]"))pin(e.target.closest("[data-pin]").dataset.pin);if(e.target.closest("#start"))select("landsat-8");});
  function renderRows() {
    const list=pageList();
    $("rows").innerHTML=list.map(s=>{
      const orbitType=orbitCode(s);
      const orbitHeight=s.orbit.altitude_km==null?"not curated":`${s.orbit.altitude_km.toLocaleString()} km`;
      return `<tr class="mission-row${state.research.platforms.has(s.id)?" research-match":""}" data-id="${s.id}" id="row-${s.id}">
        <td><button class="pin-button" data-pin="${s.id}" aria-label="${state.pins.has(s.id)?"Unpin":"Pin"} ${esc(s.name)}" aria-pressed="${state.pins.has(s.id)}">${state.pins.has(s.id)?"✓":"+ Pin"}</button></td>
        <td><button class="row-select" data-select="${s.id}" aria-expanded="${s.id===state.selected}" aria-controls="inspector">${esc(s.name)}</button><small>${esc(s.sensors.map(i=>i.name).join(" / "))}</small></td>
        <td>${esc(s.agency)}<small>${esc(s.region)}</small></td>
        <td style="--family:${families[s.type].color}"><i class="family-dot" aria-hidden="true"></i>${families[s.type].label}</td>
        <td title="${esc(s.orbit.class)}; ${esc(altitude(s))}"><i class="orbit-swatch" aria-hidden="true"></i><span class="orbit-long">${esc(s.orbit.class)}</span><span class="orbit-short">${orbitType} · ${orbitHeight}</span><small>${altitude(s)}</small></td>
        <td><span class="attribute-text">${esc(s.sensors.map(i=>i.spatial).join("; "))}</span></td>
        <td><span class="attribute-text">${esc(s.orbit.temporal_note)}</span></td>
        <td><span class="badge ${s.status}">${esc(s.status)}</span><small>Verified ${s.verified}</small>${sources(s.evidence.mission)}</td>
      </tr>`;
    }).join("");
    // Preserve complete qualifiers in tooltips while compact workspace cells use one line.
    $("rows").querySelectorAll("td:not([title])").forEach(cell=>cell.title=cell.textContent.trim());
    $("no-results").hidden=list.length>0;
    applyEncoding();
    syncHighlights();
  }
  $("rows").addEventListener("click",e=>{const p=e.target.closest("[data-pin]"),s=e.target.closest("[data-select]");if(p)pin(p.dataset.pin);else if(s){select(s.dataset.select);s.setAttribute("aria-expanded",String(state.selected===s.dataset.select));}});
  $("rows").addEventListener("pointerover",e=>{const r=e.target.closest("tr");if(r)brush(r.dataset.id);});
  $("rows").addEventListener("pointerleave",()=>brush(null));
  $("rows").addEventListener("focusin",e=>{const r=e.target.closest("tr");if(r)brush(r.dataset.id);});
  $("rows").addEventListener("focusout",e=>{if(!$("rows").contains(e.relatedTarget))brush(null);});
  function renderComparison() {
    const ss=[...state.pins].map(byId);$("pin-count").textContent=`${ss.length} pinned`;$("workspace-pin-count").textContent=`(${ss.length})`;$("clear-pins").disabled=!ss.length;
    if(ss.length<2){$("comparison-content").innerHTML='<p class="section-note">Pin at least two missions using the index or a satellite detail panel. Pins remain when filters change.</p>';return;}
    const fields=[["Status",s=>esc(s.status)+`<small>${esc(s.status_note)}</small>`],["Operator",s=>esc(s.agency)],["Orbit / altitude",s=>`${esc(s.orbit.class)} · ${altitude(s)}`],["What is measured?",s=>esc(s.sensors.map(i=>`${i.name}: ${i.observes.join(", ")}`).join("; "))],["Spatial context",s=>esc(s.sensors.map(i=>`${i.name}: ${i.spatial}`).join("; "))],["Temporal context",s=>esc(s.orbit.temporal_note)],["Spectral / method",s=>esc(s.sensors.map(i=>`${i.method}; ${i.spectral}`).join("; "))],["Coverage",s=>esc(s.sensors.map(i=>i.coverage).join("; "))],["Products",s=>esc(s.sensors.flatMap(i=>i.products.map(p=>`${p.name} (${p.level})`)).join("; "))],["Evidence",s=>sources(s.sources)]];
    $("comparison-content").innerHTML=`<p class="comparison-tip">Compare measurement meanings before numbers. Optical reflectance, thermal radiance and radar backscatter are different quantities. These fields are aligned for interpretation; there is no universal "best satellite" ranking. Missing values mean not curated.</p><div class="table-scroll"><table class="comparison-table"><caption class="sr-only">Comparison of pinned satellites, including hidden filtered selections</caption><thead><tr><th scope="col">Attribute</th>${ss.map(s=>`<th scope="col">${esc(s.name)} <button data-remove="${s.id}" aria-label="Unpin ${esc(s.name)}">×</button></th>`).join("")}</tr></thead><tbody>${fields.map(([label,fn])=>`<tr><th scope="row">${label}</th>${ss.map(s=>`<td>${fn(s)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  }
  $("comparison-content").addEventListener("click",e=>{const b=e.target.closest("[data-remove]");if(b)pin(b.dataset.remove);});
  $("clear-pins").addEventListener("click",()=>{state.pins.clear();renderRows();renderComparison();if(state.selected)renderInspector();syncHighlights();});
  function render() {
    const matches=visible();state.page=Math.min(state.page,Math.max(0,Math.ceil(matches.length/pageSize)-1));
    const page=pageList(),ids=new Set(page.map(s=>s.id));state.brush=null;
    if(state.selected&&!ids.has(state.selected))closeDetail();
    document.querySelectorAll(".sat-node").forEach(e=>{const shown=ids.has(e.dataset.id),match=state.research.platforms.has(e.dataset.id);e.classList.toggle("filtered",!shown);e.setAttribute("tabindex",shown?"0":"-1");e.setAttribute("aria-hidden",String(!shown));e.classList.toggle("research-match",match);e.classList.toggle("research-muted",!!$("question").value.trim()&&!match);});
    const slots=catalog.satellites.slice(0,pageSize).map(s=>s.display);
    page.forEach((s,i)=>{const p=slots[i];$(`node-${s.id}`).setAttribute("transform",`translate(${p.x},${p.y})`);});
    document.querySelectorAll("[data-family]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.family===$("type").value)));
    document.querySelectorAll("[data-orbit]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.orbit===$("orbit").value)));
    $("orbit-explanation").textContent=orbitModel.types.find(t=>t.filter===$("orbit").value)?.description||"SSO is a near-polar LEO subtype. Select All LEO to include SSO, or click a color to filter both views. Paths are schematic.";
    $("count").textContent=`${matches.length} MATCHES · ${ids.size} IN VIEW`;
    $("page-status").textContent=`${matches.length?state.page*pageSize+1:0}–${Math.min(matches.length,(state.page+1)*pageSize)} of ${matches.length} · map + table`;
    $("page-prev").disabled=state.page===0;$("page-next").disabled=(state.page+1)*pageSize>=matches.length;
    renderRows();$("rows").querySelectorAll("tr").forEach(row=>row.classList.toggle("research-match",state.research.platforms.has(row.dataset.id)));
  }
  filters.forEach(id=>$(id).addEventListener(id==="search"?"input":"change",()=>{state.page=0;render();}));
  $("reset").addEventListener("click",()=>{filters.forEach(id=>$(id).value="");state.page=0;closeDetail();render();});
  $("page-prev").addEventListener("click",()=>{state.page--;closeDetail();render();});
  $("page-next").addEventListener("click",()=>{state.page++;closeDetail();render();});
  $("overview").addEventListener("click",()=>setView([0,0,1200,650]));
  function zoom(factor){const [x,y,w,h]=state.view,nw=Math.max(420,Math.min(1200,w*factor)),nh=nw*650/1200;setView([Math.max(0,Math.min(1200-nw,x+(w-nw)/2)),Math.max(0,Math.min(650-nh,y+(h-nh)/2)),nw,nh]);}
  $("zoom-in").addEventListener("click",()=>zoom(.8));$("zoom-out").addEventListener("click",()=>zoom(1.25));
  document.addEventListener("keydown",e=>{if(e.key==="Escape"){if(workspace.active){e.preventDefault();void exitWorkspace();return;}const id=state.selected;closeDetail();if(id)document.getElementById(`node-${id}`)?.focus();}});
  $("sort-name").addEventListener("click",()=>{state.sorted=true;state.ascending=!state.ascending;state.page=0;$("sort-name").parentElement.setAttribute("aria-sort",state.ascending?"ascending":"descending");render();});
  $("print").addEventListener("click",()=>{setView([0,0,1200,650]);window.print();});
  window.addEventListener("beforeprint",()=>setView([0,0,1200,650]));
  $("export").addEventListener("click",()=>{
    // Prefix spreadsheet formula initiators so curated text remains inert in Excel.
    const csv=value=>'"'+String(value??"").replace(/^[=+@\-]/,"'$&").replace(/"/g,'""')+'"';
    const records=[["satellite","agency","status","orbit","altitude_km","spatial_context","temporal_context","verified","sources"],...visible().map(s=>[s.name,s.agency,s.status,s.orbit.class,s.orbit.altitude_km,s.sensors.map(i=>i.spatial).join("; "),s.orbit.temporal_note,s.verified,s.sources.map(id=>catalog.sources[id].url).join(" ")])];
    const url=URL.createObjectURL(new Blob(["\ufeff"+records.map(r=>r.map(csv).join(",")).join("\r\n")],{type:"text/csv;charset=utf-8"}));const a=document.createElement("a");a.href=url;a.download="eo-satellite-catalog.csv";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  $("scope").textContent=catalog.scope;
  $("snapshot-count").textContent=`${catalog.satellites.length} platform / constellation records · ${Object.keys(families).length} sensing families · no live tracking`;
  function saveJSON(name,value){const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function brief(){return {profile:"eo-research-brief/1",question:$("question").value.trim(),created:new Date().toISOString(),catalog_snapshot:catalog.verified,concepts:state.research.concepts.map(t=>t.id),platforms:[...state.research.platforms].filter(id=>byId(id)),routes:discovery.routes.filter(r=>state.research.routes.includes(r.id)),qualifications:state.research.concepts.map(t=>t.caution),source:"https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/",fieldwork:"Planning metadata only. Not a FieldWork workflow, raster handoff or acquired-data receipt."};}
  function runResearch(){
    state.research=window.EOResearch.resolve($("question").value);state.page=0;
    const {concepts,platforms,routes}=state.research;
    const matches=catalog.satellites.filter(s=>platforms.has(s.id));
    $("research-results").innerHTML=!$("question").value.trim()?'<p>Enter a question or choose an example to highlight potential measurement pathways.</p>':!concepts.length?'<p>No curated measurement pathway matches this wording. Try a named measurement such as NO₂, aerosol, surface temperature or surface water. A missing match does not mean data do not exist.</p>':`<h3>${matches.length} candidate platforms · ${concepts.map(t=>esc(t.label)).join(" + ")}</h3><p><a href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/swaths.html?q=${encodeURIComponent($("question").value)}" target="_blank" rel="noopener">Compare these candidates over your study area ↗</a></p>${concepts.map(t=>`<p>${esc(t.chain)}</p><p class="research-caution">${esc(t.caution)}</p>${sources(t.sources)}`).join("")}${discovery.routes.filter(r=>routes.includes(r.id)).map(r=>`<article class="data-route"><b>${esc(r.label)}</b><p>${esc(r.measurement)} · ${esc(r.format)} · ${esc(r.access_note)}</p><p>Catalog URL: <code>${esc(r.endpoint)}</code><br>Collection: <code>${esc(r.collection)}</code></p><p><a href="${esc(r.collection_url)}" target="_blank" rel="noopener">Inspect collection ↗</a><button data-copy-route="${esc(r.id)}">Copy catalog URL</button></p><small>Metadata checked ${esc(r.verified)}. ${esc(r.note)}</small></article>`).join("")}<p>Gold highlights indicate potential relevance. Other filters still apply; clear them if matching missions are hidden. Each page shows up to 13 records in both views.</p>`;
    ["export-question","research-notebook","share-question"].forEach(id=>$(id).disabled=!concepts.length);
    render();
  }
  $("topic-examples").innerHTML=["NO₂","Aerosols","Surface heat","Vegetation","Flooding","Coastal water"].map(q=>`<button data-question="${esc(q)}">${esc(q)}</button>`).join("");
  $("topic-examples").addEventListener("click",e=>{const b=e.target.closest("[data-question]");if(b){$("question").value=b.dataset.question;runResearch();}});
  $("research-form").addEventListener("submit",e=>{e.preventDefault();runResearch();});
  $("question").addEventListener("input",runResearch);
  $("research-only").addEventListener("change",()=>{state.page=0;render();});
  $("clear-research").addEventListener("click",()=>{$("question").value="";$("handoff-status").textContent="";runResearch();});
  async function copyText(value){try{await navigator.clipboard.writeText(value);$("handoff-status").textContent="Copied. Paste into the destination's URL field.";}catch{$("handoff-status").textContent=`Copy this value: ${value}`;}}
  $("research-results").addEventListener("click",e=>{const b=e.target.closest("[data-copy-route]");if(b)void copyText(discovery.routes.find(r=>r.id===b.dataset.copyRoute).endpoint);});
  $("share-question").addEventListener("click",()=>{const u=new URL("https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/explorer/");u.searchParams.set("q",$("question").value.trim());void copyText(u.href);});
  $("export-question").addEventListener("click",()=>saveJSON("eo-research-brief.json",brief()));
  $("research-notebook").addEventListener("click",()=>{
    const b=brief();const code='import json\nfrom eo_guide import search_stac\nbrief = json.loads('+JSON.stringify(JSON.stringify(b))+')\nroute = brief["routes"][0]\n# EDIT your study area and dates, then run. This requests metadata, not assets.\nitems = await search_stac(route, bbox=[-76, 39, -74, 41], start="2025-07-01", end="2025-07-07", limit=3)\nprint("Collection:", route["collection"], "Items:", len(items.get("features", [])))\nitems';
    saveJSON("research-stac-handoff.ipynb",{nbformat:4,nbformat_minor:5,metadata:{kernelspec:{display_name:"Python (Pyodide)",language:"python",name:"python3"}},cells:[{id:"question",cell_type:"markdown",metadata:{},source:["# Research → STAC metadata\n",b.question,"\n\nUpload this notebook to the Global EO Guide JupyterLite Lab. Review the brief, edit the area/dates and run. `eo_guide.py` is bundled there. Provider CORS/access restrictions may apply. Inspect units, QA, licensing and asset availability before analysis.\n",...b.qualifications.map(x=>"\n"+x)]},{id:"search",cell_type:"code",metadata:{},execution_count:null,outputs:[],source:[code]}]});
    $("handoff-status").innerHTML='Notebook saved. <a href="https://jltobias.github.io/JupyterLite-EO-Satellite-Guide/lab/index.html" target="_blank" rel="noopener">Open this Guide’s Lab ↗</a>, upload the notebook, edit area/dates, then Run All.';
  });
  $("sources").innerHTML=Object.entries(catalog.sources).map(([id,s])=>`<p class="source-entry" id="source-${esc(id)}"><b>[${esc(id)}]</b> ${esc(s.publisher)}. <a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a>. ${s.published?`Published ${esc(s.published)}. `:""}Accessed ${esc(s.accessed)}. ${s.locators?esc(s.locators):""}${s.license?` ${esc(s.license)}.`:""}</p>`).join("");
  $("question").value=(new URLSearchParams(location.search).get("q")||window.EO_INITIAL_QUESTION||"").slice(0,500);
  runResearch();renderComparison();
})();

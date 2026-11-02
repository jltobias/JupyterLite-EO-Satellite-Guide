/* Original MIT-licensed UI. All catalog strings are escaped before HTML use. */
"use strict";
(() => {
  const catalog = window.EO_CATALOG;
  const land = window.EO_LAND;
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? "Unknown / not curated").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const families = {multispectral:{label:"Multispectral",color:"#60dfc4",symbol:"square"},radar:{label:"Radar",color:"#bb9cf5",symbol:"diamond"},hyperspectral:{label:"Hyperspectral",color:"#f29d81",symbol:"hexagon"},weather:{label:"Weather radiometry",color:"#84b7f6",symbol:"circle"},ocean:{label:"Ocean colour",color:"#f2d879",symbol:"triangle"}};
  const state = {selected:null,pins:new Set(),brush:null,ascending:true,view:[0,0,1200,650]};
  const filters = ["search","agency","type","orbit","status","property","application"];
  const svgNS = "http://www.w3.org/2000/svg";
  const byId = id => catalog.satellites.find(s => s.id === id);
  const sources = ids => `<span class="source-links">${[...new Set(ids)].map(id => { const s=catalog.sources[id]; return `<a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer" title="${esc(s.title)}">[${esc(id)}] ↗</a>`; }).join(" ")}</span>`;
  const altitude = s => s.orbit.altitude_km == null ? "Unknown / not curated" : `${s.orbit.altitude_km.toLocaleString()} km (nominal)`;
  function optionList(id, values) { $(id).insertAdjacentHTML("beforeend", [...new Set(values)].sort().map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join("")); }
  optionList("agency",catalog.satellites.map(s=>s.agency));
  $("type").insertAdjacentHTML("beforeend",Object.entries(families).map(([k,v])=>`<option value="${k}">${v.label}</option>`).join(""));
  optionList("orbit",catalog.satellites.map(s=>s.orbit.class));
  optionList("status",catalog.satellites.map(s=>s.status));
  optionList("property",catalog.satellites.flatMap(s=>s.sensors.flatMap(i=>i.observes)));
  $("application").insertAdjacentHTML("beforeend",catalog.applications.map(a=>`<option value="${a.id}">${esc(a.name)}</option>`).join(""));
  function visible() {
    const q=$("search").value.trim().toLowerCase();
    return catalog.satellites.filter(s=>(!q||JSON.stringify(s).toLowerCase().includes(q))&&(!$("agency").value||s.agency===$("agency").value)&&(!$("type").value||s.type===$("type").value)&&(!$("orbit").value||s.orbit.class===$("orbit").value)&&(!$("status").value||s.status===$("status").value)&&(!$("property").value||s.sensors.some(i=>i.observes.includes($("property").value)))&&(!$("application").value||catalog.applications.find(a=>a.id===$("application").value).satellites.includes(s.id))).sort((a,b)=>state.ascending?a.name.localeCompare(b.name):b.name.localeCompare(a.name));
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
    return '<rect x="-6" y="-6" width="12" height="12"/>';
  }
  catalog.satellites.forEach(s=>{
    const g=document.createElementNS(svgNS,"g");g.setAttribute("class",`sat-node ${s.status}`);g.setAttribute("data-id",s.id);g.setAttribute("id",`node-${s.id}`);g.setAttribute("role","button");g.setAttribute("tabindex","0");g.setAttribute("aria-label",`${s.name}, ${families[s.type].label}, ${s.orbit.class}, ${s.status}. Open details.`);g.setAttribute("aria-pressed","false");g.setAttribute("transform",`translate(${s.display.x},${s.display.y})`);g.style.setProperty("--family",families[s.type].color);
    g.innerHTML=`<title>${esc(s.name)}: ${esc(s.sensors.map(i=>i.name).join(", "))}</title><rect class="hit" x="-85" y="-28" width="170" height="76" rx="7"/><circle class="halo" r="22"/><g stroke="${families[s.type].color}" stroke-width="1.3" fill="none"><path d="M-17 -7H-8V7H-17ZM8 -7H17V7H8ZM-8 0H8"/><g fill="${families[s.type].color}" fill-opacity=".22">${shape(s.type)}</g></g><circle class="pin-marker" cx="20" cy="-18" r="4"/><text y="39" text-anchor="middle" class="sat-label">${esc(s.name)}</text><text y="53" text-anchor="middle" class="sat-meta">${esc(s.agency)}</text>`;
    g.addEventListener("click",()=>select(s.id));g.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select(s.id);}});g.addEventListener("pointerenter",()=>brush(s.id));g.addEventListener("pointerleave",()=>brush(null));g.addEventListener("focus",()=>brush(s.id));g.addEventListener("blur",()=>brush(null));$("satellites").append(g);
  });
  $("legend").innerHTML=Object.entries(families).map(([id,f])=>`<button data-family="${id}" aria-pressed="false" style="--family:${f.color}"><i aria-hidden="true"></i>${f.label} · ${f.symbol}</button>`).join("")+'<span class="legend-note">Solid ring: operational source snapshot · dashed: retired · dotted: unverified status · gold dot: pinned</span>';
  $("legend").addEventListener("click",e=>{const b=e.target.closest("button");if(b){$("type").value=$("type").value===b.dataset.family?"":b.dataset.family;render();}});
  function brush(id) { state.brush=id; syncHighlights(); }
  function syncHighlights() {
    document.querySelectorAll(".sat-node,.mission-row").forEach(e=>{const id=e.dataset.id;e.classList.toggle("is-brushed",id===state.brush);e.classList.toggle("is-selected",id===state.selected);e.classList.toggle("pinned",state.pins.has(id));if(e.classList.contains("sat-node"))e.setAttribute("aria-pressed",String(id===state.selected));});
    document.querySelectorAll("[data-select]").forEach(e=>e.setAttribute("aria-expanded",String(e.dataset.select===state.selected)));
  }
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
    const s=byId(id);setView([Math.max(0,Math.min(320,s.display.x-440)),Math.max(0,Math.min(170,s.display.y-240)),880,480]);
    $("announcement").textContent=`${s.name} selected. Details and sources are open. Use Overview to restore the atlas.`;
  }
  const initialInspector=$("inspector").innerHTML;
  function closeDetail() {state.selected=null;$("inspector").innerHTML=initialInspector;setView([0,0,1200,650]);syncHighlights();}
  function renderInspector() {
    const s=byId(state.selected);if(!s)return;
    const sensorHTML=s.sensors.map(i=>`<details class="sensor"><summary>${esc(i.name)} · unfold sensor</summary><div class="sensor-content"><p>${esc(i.method)}</p><h4>Observed properties</h4><p>${esc(i.observes.join(" · "))}</p><h4>Spatial resolution / sampling</h4><p>${esc(i.spatial)}</p><h4>Spectral characteristics</h4><p>${esc(i.spectral)}</p><h4>Coverage</h4><p>${esc(i.coverage)}</p>${sources(i.sources)}<h4>Data products</h4>${i.products.map(p=>`<details class="product"><summary>${esc(p.name)}</summary><p><b>${esc(p.level)}</b></p><p>${esc(p.note)}</p><p><a target="_blank" rel="noopener noreferrer" href="${esc(p.access)}">Open data access ↗</a></p>${sources(p.sources)}</details>`).join("")}</div></details>`).join("");
    const applications=catalog.applications.filter(a=>a.satellites.includes(s.id));
    $("inspector").innerHTML=`<div class="detail-head"><span class="eyebrow">PLATFORM / EVIDENCE</span><button data-close aria-label="Close satellite details">× Close</button></div><h3 class="detail-name">${esc(s.name)}</h3><span class="badge ${s.status}">${esc(s.status)}</span><p class="detail-purpose">${esc(s.purpose)}</p><button class="pin-button" data-pin="${s.id}" aria-pressed="${state.pins.has(s.id)}">${state.pins.has(s.id)?"✓ Pinned for comparison":"+ Pin for comparison"}</button><dl class="facts"><div><dt>Operator</dt><dd>${esc(s.agency)}</dd></div><div><dt>Region</dt><dd>${esc(s.region)}</dd></div><div><dt>Orbit</dt><dd>${esc(s.orbit.class)}</dd></div><div><dt>Altitude</dt><dd>${altitude(s)}</dd></div><div><dt>Launch</dt><dd>${esc(s.launch)}</dd></div><div><dt>Mission end</dt><dd>${s.end?esc(s.end):"Not recorded"}</dd></div></dl><p class="detail-note">${esc(s.orbit.temporal_note)}</p><p class="detail-note">${esc(s.status_note)}</p>${sensorHTML}<details class="evidence-groups"><summary>Evidence by field · verified ${esc(s.verified)}</summary>${Object.entries(s.evidence).map(([group,ids])=>`<p><b>${esc(group)}</b>${sources(ids)}</p>`).join("")}</details>${applications.map(a=>`<details class="pathway"><summary>${esc(a.name)} →</summary><h4>${esc(a.evidence_type)}</h4>${a.historical_platform?`<p><b>${esc(a.historical_platform)}</b></p>`:""}<ol>${a.chain.map(x=>`<li>${esc(x)}</li>`).join("")}</ol>${a.design?`<p>${esc(a.design)}</p><p>${esc(a.finding)}</p>`:""}<p class="detail-note">${esc(a.limitations)}</p>${sources(a.sources)}</details>`).join("")}`;
  }
  $("inspector").addEventListener("click",e=>{if(e.target.closest("[data-close]")){const id=state.selected;closeDetail();document.getElementById(`node-${id}`)?.focus();}if(e.target.closest("[data-pin]"))pin(e.target.closest("[data-pin]").dataset.pin);if(e.target.closest("#start"))select("landsat-8");});
  function renderRows() {
    const list=visible();
    $("rows").innerHTML=list.map(s=>`<tr class="mission-row" data-id="${s.id}" id="row-${s.id}"><td><button class="pin-button" data-pin="${s.id}" aria-label="${state.pins.has(s.id)?"Unpin":"Pin"} ${esc(s.name)}" aria-pressed="${state.pins.has(s.id)}">${state.pins.has(s.id)?"✓":"+ Pin"}</button></td><td><button class="row-select" data-select="${s.id}" aria-expanded="${s.id===state.selected}" aria-controls="inspector">${esc(s.name)}</button><small>${esc(s.sensors.map(i=>i.name).join(" / "))}</small></td><td>${esc(s.agency)}<small>${esc(s.region)}</small></td><td style="--family:${families[s.type].color}"><i class="family-dot" aria-hidden="true"></i>${families[s.type].label}</td><td>${esc(s.orbit.class)}<small>${altitude(s)}</small></td><td>${esc(s.sensors.map(i=>i.spatial).join("; "))}</td><td>${esc(s.orbit.temporal_note)}</td><td><span class="badge ${s.status}">${esc(s.status)}</span><small>Verified ${s.verified}</small>${sources(s.evidence.mission)}</td></tr>`).join("");
    $("no-results").hidden=list.length>0;
    syncHighlights();
  }
  $("rows").addEventListener("click",e=>{const p=e.target.closest("[data-pin]"),s=e.target.closest("[data-select]");if(p)pin(p.dataset.pin);else if(s){select(s.dataset.select);s.setAttribute("aria-expanded",String(state.selected===s.dataset.select));}});
  $("rows").addEventListener("pointerover",e=>{const r=e.target.closest("tr");if(r)brush(r.dataset.id);});
  $("rows").addEventListener("pointerleave",()=>brush(null));
  $("rows").addEventListener("focusin",e=>{const r=e.target.closest("tr");if(r)brush(r.dataset.id);});
  $("rows").addEventListener("focusout",e=>{if(!$("rows").contains(e.relatedTarget))brush(null);});
  function renderComparison() {
    const ss=[...state.pins].map(byId);$("pin-count").textContent=`${ss.length} pinned`;$("clear-pins").disabled=!ss.length;
    if(ss.length<2){$("comparison-content").innerHTML='<p class="section-note">Pin at least two missions using the index or a satellite detail panel. Pins remain when filters change.</p>';return;}
    const fields=[["Status",s=>esc(s.status)+`<small>${esc(s.status_note)}</small>`],["Operator",s=>esc(s.agency)],["Orbit / altitude",s=>`${esc(s.orbit.class)} · ${altitude(s)}`],["What is measured?",s=>esc(s.sensors.map(i=>`${i.name}: ${i.observes.join(", ")}`).join("; "))],["Spatial context",s=>esc(s.sensors.map(i=>`${i.name}: ${i.spatial}`).join("; "))],["Temporal context",s=>esc(s.orbit.temporal_note)],["Spectral / method",s=>esc(s.sensors.map(i=>`${i.method}; ${i.spectral}`).join("; "))],["Coverage",s=>esc(s.sensors.map(i=>i.coverage).join("; "))],["Products",s=>esc(s.sensors.flatMap(i=>i.products.map(p=>`${p.name} (${p.level})`)).join("; "))],["Evidence",s=>sources(s.sources)]];
    $("comparison-content").innerHTML=`<p class="comparison-tip">Compare measurement meanings before numbers. Optical reflectance, thermal radiance and radar backscatter are different quantities. These fields are aligned for interpretation; there is no universal "best satellite" ranking. Missing values mean not curated.</p><div class="table-scroll"><table class="comparison-table"><caption class="sr-only">Comparison of pinned satellites, including hidden filtered selections</caption><thead><tr><th scope="col">Attribute</th>${ss.map(s=>`<th scope="col">${esc(s.name)} <button data-remove="${s.id}" aria-label="Unpin ${esc(s.name)}">×</button></th>`).join("")}</tr></thead><tbody>${fields.map(([label,fn])=>`<tr><th scope="row">${label}</th>${ss.map(s=>`<td>${fn(s)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  }
  $("comparison-content").addEventListener("click",e=>{const b=e.target.closest("[data-remove]");if(b)pin(b.dataset.remove);});
  $("clear-pins").addEventListener("click",()=>{state.pins.clear();renderRows();renderComparison();if(state.selected)renderInspector();syncHighlights();});
  function render() {
    const ids=new Set(visible().map(s=>s.id));state.brush=null;
    if(state.selected&&!ids.has(state.selected))closeDetail();
    document.querySelectorAll(".sat-node").forEach(e=>e.classList.toggle("filtered",!ids.has(e.dataset.id)));
    document.querySelectorAll("[data-family]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.family===$("type").value)));
    $("count").textContent=`${ids.size} / ${catalog.satellites.length} PLATFORMS`;renderRows();
  }
  filters.forEach(id=>$(id).addEventListener(id==="search"?"input":"change",render));
  $("reset").addEventListener("click",()=>{filters.forEach(id=>$(id).value="");closeDetail();render();});
  $("overview").addEventListener("click",()=>setView([0,0,1200,650]));
  function zoom(factor){const [x,y,w,h]=state.view,nw=Math.max(420,Math.min(1200,w*factor)),nh=nw*650/1200;setView([Math.max(0,Math.min(1200-nw,x+(w-nw)/2)),Math.max(0,Math.min(650-nh,y+(h-nh)/2)),nw,nh]);}
  $("zoom-in").addEventListener("click",()=>zoom(.8));$("zoom-out").addEventListener("click",()=>zoom(1.25));
  document.addEventListener("keydown",e=>{if(e.key==="Escape"){const id=state.selected;closeDetail();if(id)document.getElementById(`node-${id}`)?.focus();}});
  $("sort-name").addEventListener("click",()=>{state.ascending=!state.ascending;$("sort-name").parentElement.setAttribute("aria-sort",state.ascending?"ascending":"descending");renderRows();});
  $("print").addEventListener("click",()=>{setView([0,0,1200,650]);window.print();});
  window.addEventListener("beforeprint",()=>setView([0,0,1200,650]));
  $("export").addEventListener("click",()=>{
    // Prefix spreadsheet formula initiators so curated text remains inert in Excel.
    const csv=value=>'"'+String(value??"").replace(/^[=+@\-]/,"'$&").replace(/"/g,'""')+'"';
    const records=[["satellite","agency","status","orbit","altitude_km","spatial_context","temporal_context","verified","sources"],...visible().map(s=>[s.name,s.agency,s.status,s.orbit.class,s.orbit.altitude_km,s.sensors.map(i=>i.spatial).join("; "),s.orbit.temporal_note,s.verified,s.sources.map(id=>catalog.sources[id].url).join(" ")])];
    const url=URL.createObjectURL(new Blob(["\ufeff"+records.map(r=>r.map(csv).join(",")).join("\r\n")],{type:"text/csv;charset=utf-8"}));const a=document.createElement("a");a.href=url;a.download="eo-satellite-catalog.csv";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  $("scope").textContent=catalog.scope;
  $("sources").innerHTML=Object.entries(catalog.sources).map(([id,s])=>`<p class="source-entry" id="source-${esc(id)}"><b>[${esc(id)}]</b> ${esc(s.publisher)}. <a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a>. ${s.published?`Published ${esc(s.published)}. `:""}Accessed ${esc(s.accessed)}. ${s.locators?esc(s.locators):""}${s.license?` ${esc(s.license)}.`:""}</p>`).join("");
  render();renderComparison();
})();

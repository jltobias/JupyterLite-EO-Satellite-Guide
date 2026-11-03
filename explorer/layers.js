/* Original browsing groups. These are display layers, not agency ownership claims. */
"use strict";
window.EOLayers=(()=>{
 const records=window.EO_CATALOG.satellites;
 const statusLabels={operational:"Active / operational",retired:"Retired",commissioning:"Commissioning",planned:"Planned / approved",considered:"Considered",cancelled:"Cancelled",failed:"Launch failed",unverified:"Unverified"};
 const definitions=[['sentinel','Sentinel + hosted instruments'],['landsat','Landsat'],['goes','GOES'],['noaa','NOAA / JPSS / TIROS'],['metop','Metop'],['meteosat','Meteosat / MTG'],['fengyun','Fengyun (FY)'],['japan-weather','Himawari / GMS / MTSAT'],['dmsp','DMSP'],['planet','Planet / SkySat / RapidEye'],['spot-pleiades','SPOT / Pléiades'],['worldview','WorldView / GeoEye'],['radarsat','RADARSAT'],['cosmo-skymed','COSMO-SkyMed'],['terrasar','TerraSAR / TanDEM / PAZ'],['isro-imaging','IRS / Cartosat / Resourcesat / Oceansat'],['russian-eo','Meteor / Resurs / Kanopus'],['jason','Jason / TOPEX / SARAL'],['cbers','CBERS'],['alos','ALOS'],['other','Other mission families']];
 function familyOf(s){
  const id=s.id;
  if(s.mission_families?.includes('sentinel'))return 'sentinel';
  if(s.mission_families?.includes('landsat'))return 'landsat';
  if(/^goes(?:-|$)/.test(id))return 'goes';
  if(/^(?:noaa|jpss|tiros)(?:-|$)/.test(id)||id==='suomi-npp')return 'noaa';
  if(/^metop(?:-|$)/.test(id))return 'metop';
  if(/^(?:meteosat|mtg|msg|mfg)(?:-|$)/.test(id))return 'meteosat';
  if(/^(?:fy|fengyun)(?:-|$)/.test(id))return 'fengyun';
  if(/^(?:himawari|gms|mtsat)(?:-|$)/.test(id))return 'japan-weather';
  if(/^dmsp(?:-|$)/.test(id))return 'dmsp';
  if(/^(?:planet|planetscope|skysat|rapideye|pelican|tanager|dove|flock)(?:-|$)/.test(id))return 'planet';
  if(/^(?:spot|pleiades)(?:-|$)/.test(id))return 'spot-pleiades';
  if(/^(?:worldview|geoeye)(?:-|$)/.test(id))return 'worldview';
  if(/^radarsat(?:-|$)/.test(id))return 'radarsat';
  if(/^cosmo-skymed(?:-|$)/.test(id))return 'cosmo-skymed';
  if(/^(?:terrasar|tandem|paz)(?:-|$)/.test(id))return 'terrasar';
  if(/^(?:irs|cartosat|resourcesat|oceansat)(?:-|$)/.test(id)||/^eos-0[1-9]$/.test(id))return 'isro-imaging';
  if(/^(?:meteor|resurs|kanopus)(?:-|$)/.test(id))return 'russian-eo';
  if(/^(?:jason|topex|saral)(?:-|$)/.test(id))return 'jason';
  if(/^cbers(?:-|$)/.test(id))return 'cbers';
  if(/^alos(?:-|$)/.test(id))return 'alos';
  return 'other';
 }
 const statuses=Object.entries(statusLabels).map(([id,label])=>({id,label,count:records.filter(s=>s.status===id).length}));
 const families=definitions.map(([id,label])=>({id,label,count:records.filter(s=>familyOf(s)===id).length}));
 return {statuses,families,familyOf};
})();

/* Original MIT-licensed, shared orbit taxonomy. SSO belongs to the LEO family. */
"use strict";
window.EOOrbits=(()=>{
  const types=window.EO_ORBITS.types;
  const byId=id=>types.find(t=>t.id===id);
  function kind(s){
    const c=typeof s==="string"?s:s.orbit.class;
    if(c==="Sun-synchronous LEO")return "sso";
    if(["LEO","Inclined LEO","Polar LEO"].includes(c))return "leo";
    if(c==="Geostationary")return "geo";
    if(c==="Highly elliptical")return "heo";
    if(c==="Sun-Earth L1 Lissajous")return "l1";
    return "unknown";
  }
  const category=s=>byId(kind(s));
  const matches=(s,value)=>!value||(value==="all-leo"?["sso","leo"].includes(kind(s)):value==="other-leo"?kind(s)==="leo":s.orbit.class===value);
  return {types,byId,kind,category,matches,code:s=>category(s).code,color:s=>category(s).color};
})();

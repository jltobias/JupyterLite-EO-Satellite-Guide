/* Original MIT-licensed spherical teaching geometry. No mission ephemerides. */
"use strict";
window.EOGeometry=(()=>{
 const R=6371,mu=398600.4418,day=86164.0905,rad=Math.PI/180,deg=180/Math.PI;
 const wrap=x=>((x+180)%360+360)%360-180;
 const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
 const period=p=>p.kind==="geo"?day:2*Math.PI*Math.sqrt((R+p.altitude_km)**3/mu);
 function point(p,t,phase={node:-45,argument:0}){
  if(p.kind==="geo")return {lon:p.longitude_deg,lat:0};
  const u=2*Math.PI*t/period(p)+(phase.argument||0)*rad,i=p.inclination_deg*rad;
  return {lon:wrap(Math.atan2(Math.sin(u)*Math.cos(i),Math.cos(u))*deg+(phase.node||0)-360*t/day),lat:Math.asin(Math.sin(u)*Math.sin(i))*deg};
 }
 function destination(p,bearing,km){const d=km/R,b=bearing*rad,lat=p.lat*rad,lon=p.lon*rad;
  const y=Math.asin(clamp(Math.sin(lat)*Math.cos(d)+Math.cos(lat)*Math.sin(d)*Math.cos(b),-1,1));
  const x=lon+Math.atan2(Math.sin(b)*Math.sin(d)*Math.cos(lat),Math.cos(d)-Math.sin(lat)*Math.sin(y));return {lon:wrap(x*deg),lat:y*deg};}
 function bearing(a,b){const d=wrap(b.lon-a.lon)*rad,l1=a.lat*rad,l2=b.lat*rad;return Math.atan2(Math.sin(d)*Math.cos(l2),Math.cos(l1)*Math.sin(l2)-Math.sin(l1)*Math.cos(l2)*Math.cos(d))*deg;}
 function distance(a,b){const l1=a.lat*rad,l2=b.lat*rad,dl=(b.lat-a.lat)*rad,dn=wrap(b.lon-a.lon)*rad;return 2*R*Math.asin(Math.sqrt(clamp(Math.sin(dl/2)**2+Math.cos(l1)*Math.cos(l2)*Math.sin(dn/2)**2,0,1)));}
 const center=b=>({lon:(b[0]+b[2])/2,lat:(b[1]+b[3])/2});
 function validBox(b){return Array.isArray(b)&&b.length===4&&b.every(Number.isFinite)&&b[0]>=-180&&b[2]<=180&&b[1]>=-90&&b[3]<=90&&b[0]<b[2]&&b[1]<b[3];}
 function align(p,b){const c=center(b),i=p.inclination_deg*rad;if(p.kind==="geo")return {node:0,argument:0};
  const ratio=Math.sin(c.lat*rad)/Math.sin(i);if(Math.abs(ratio)>1)return null;
  const u=Math.asin(ratio);return {argument:u*deg,node:wrap(c.lon-Math.atan2(Math.sin(u)*Math.cos(i),Math.cos(u))*deg)};}
 function strip(p,t,phase){if(p.kind==="geo")return [];
  const a=point(p,t,phase),b=point(p,t+60,phase),br=bearing(a,b),half=p.swath_km/2;
  return [destination(a,br-90,half),destination(a,br+90,half),destination(b,br+90,half),destination(b,br-90,half)];}
 function visibleGeo(p,b){const horizon=Math.acos(R/(R+p.altitude_km))*deg,c=center(b);
  const angle=q=>distance({lon:p.longitude_deg,lat:0},q)/R*deg;
  const points=[c,{lon:b[0],lat:b[1]},{lon:b[0],lat:b[3]},{lon:b[2],lat:b[1]},{lon:b[2],lat:b[3]}];
  return {center:angle(c)<=horizon,all:points.every(q=>angle(q)<=horizon),any:points.some(q=>angle(q)<=horizon),horizon};}
 function overlap(a,b){return a[0]<=b[2]&&a[2]>=b[0]&&a[1]<=b[3]&&a[3]>=b[1];}
 function opportunity(p,t,phase,b){const q=point(p,t,phase),relative=center(b).lon+wrap(q.lon-center(b).lon),near={lon:clamp(relative,b[0],b[2]),lat:clamp(q.lat,b[1],b[3])};
  // A conservative distance-to-box proxy, not rigorous sensor access geometry.
  return distance(q,near)<=p.swath_km/2;
 }
 function opportunities(p,b,phase,hours=6){if(p.kind==="geo")return [];
  const out=[];let active=null;for(let t=0;t<=hours*3600;t+=10){const hit=opportunity(p,t,phase,b);
   if(hit&&active===null)active=t;if(!hit&&active!==null){out.push([active,t]);active=null;}}
  if(active!==null)out.push([active,hours*3600]);return out;
 }
 function metrics(p,b){const c=center(b),width=R*(b[2]-b[0])*rad*Math.cos(c.lat*rad),height=R*(b[3]-b[1])*rad;
  const columns=Math.max(1,Math.ceil(width*1000/p.pixel_x_m)),rows=Math.max(1,Math.ceil(height*1000/p.pixel_y_m));return {width,height,columns,rows,cells:columns*rows};}
 return {R,period,point,strip,align,visibleGeo,overlap,opportunities,metrics,center,validBox,destination,distance};
})();

/* Original MIT-licensed deterministic research vocabulary resolver. No external requests. */
"use strict";
window.EOResearch = (() => {
  const normalize = text => String(text).normalize("NFKD").replace(/₂/g,"2").toLowerCase().replace(/[^a-z0-9.]+/g," ").trim();
  function resolve(question, profile=window.EO_DISCOVERY) {
    const q=` ${normalize(question)} `;
    let concepts=profile.topics.filter(t=>t.aliases.some(a=>q.includes(` ${normalize(a)} `)));
    // A named pollutant overrides its broad parent; it does not pull in every air-quality sensor.
    concepts=concepts.filter(t=>!concepts.some(c=>c.broader===t.id));
    return {concepts,platforms:new Set(concepts.flatMap(t=>t.platforms)),routes:[...new Set(concepts.flatMap(t=>t.routes))]};
  }
  return {normalize,resolve};
})();

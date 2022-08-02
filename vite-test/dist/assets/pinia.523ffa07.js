import{i as r}from"./vue-demi.b3a9cad9.js";import{af as p,r as f,ae as l}from"./@vue.6c4e534d.js";/*!
  * pinia v2.0.14
  * (c) 2022 Eduardo San Martin Morote
  * @license MIT
  */const u=Symbol();var o;(function(t){t.direct="direct",t.patchObject="patch object",t.patchFunction="patch function"})(o||(o={}));function _(){const t=p(!0),s=t.run(()=>f({}));let c=[],i=[];const a=l({install(e){a._a=e,e.provide(u,a),e.config.globalProperties.$pinia=a,i.forEach(n=>c.push(n)),i=[]},use(e){return!this._a&&!r?i.push(e):c.push(e),this},_p:c,_a:null,_e:t,_s:new Map,state:s});return a}export{_ as c};

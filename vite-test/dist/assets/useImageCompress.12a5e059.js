import{i as n}from"./image-conversion.4b22b246.js";import{r}from"./@vue.6c4e534d.js";async function f(a){var c,i;const e=r(),o=r(),u=r(),s=r();let t=null;if(/image/.test(a.type)&&a.size>1024*1024*2)try{t=await n.exports.compressAccurately(a,1024)}catch(l){s.value=l}try{e.value=await n.exports.filetoDataURL(t===null?a:t)}catch(l){s.value=l}return u.value=(c=e.value)==null?void 0:c.length,o.value=e.value,e.value=(i=e.value)==null?void 0:i.replace(/data:\w+\/\w+;base64,/,""),{dataUrl:e,size:u,error:s,realUrl:o}}export{f as u};

import{r as g,w,t as W,v as $,u as b,g as R,p as I}from"./@vue.6c4e534d.js";function P(e){return W()?($(e),!0):!1}var F;const E=typeof window<"u",S=e=>typeof e<"u",B=e=>typeof e=="boolean",K=e=>typeof e=="number",j=e=>typeof e=="string",T=()=>{};E&&((F=window==null?void 0:window.navigator)==null?void 0:F.userAgent)&&/iP(ad|hone|od)/.test(window.navigator.userAgent);function L(e,n){function o(...t){e(()=>n.apply(this,t),{fn:n,thisArg:this,args:t})}return o}function C(e,n={}){let o,t;return i=>{const s=b(e),a=b(n.maxWait);if(o&&clearTimeout(o),s<=0||a!==void 0&&a<=0)return t&&(clearTimeout(t),t=null),i();a&&!t&&(t=setTimeout(()=>{o&&clearTimeout(o),t=null,i()},a)),o=setTimeout(()=>{t&&clearTimeout(t),t=null,i()},s)}}function V(e,n=!0,o=!0){let t=0,r,i=!0;const s=()=>{r&&(clearTimeout(r),r=void 0)};return l=>{const c=b(e),d=Date.now()-t;if(s(),c<=0)return t=Date.now(),l();d>c&&(o||!i)?(t=Date.now(),l()):n&&(r=setTimeout(()=>{t=Date.now(),i=!0,s(),l()},c)),!o&&!r&&(r=setTimeout(()=>i=!0,c)),i=!1}}function z(e,n=200,o={}){return L(C(n,o),e)}function M(e,n=200,o={}){if(n<=0)return e;const t=g(e.value),r=z(()=>{t.value=e.value},n,o);return w(e,()=>r()),t}function q(e,n=200,o=!0,t=!0){return L(V(n,o,t),e)}function J(e,n,o={}){const{immediate:t=!0}=o,r=g(!1);let i=null;function s(){i&&(clearTimeout(i),i=null)}function a(){r.value=!1,s()}function l(...c){s(),r.value=!0,i=setTimeout(()=>{r.value=!1,i=null,e(...c)},b(n))}return t&&(r.value=!0,E&&l()),P(a),{isPending:r,start:l,stop:a}}function v(e){var n;const o=b(e);return(n=o==null?void 0:o.$el)!=null?n:o}const D=E?window:void 0;function _(...e){let n,o,t,r;if(j(e[0])?([o,t,r]=e,n=D):[n,o,t,r]=e,!n)return T;let i=T;const s=w(()=>v(n),l=>{i(),l&&(l.addEventListener(o,t,r),i=()=>{l.removeEventListener(o,t,r),i=T})},{immediate:!0,flush:"post"}),a=()=>{s(),i()};return P(a),a}function Q(e,n,o={}){const{window:t=D,ignore:r,capture:i=!0}=o;if(!t)return;const s=g(!0);let a;const l=u=>{t.clearTimeout(a);const f=v(e),p=u.composedPath();!f||f===u.target||p.includes(f)||!s.value||r&&r.length>0&&r.some(m=>{const h=v(m);return h&&(u.target===h||p.includes(h))})||n(u)},c=[_(t,"click",l,{passive:!0,capture:i}),_(t,"pointerdown",u=>{const f=v(e);s.value=!!f&&!u.composedPath().includes(f)},{passive:!0}),_(t,"pointerup",u=>{if(u.button===0){const f=u.composedPath();u.composedPath=()=>f,a=t.setTimeout(()=>l(u),50)}},{passive:!0})];return()=>c.forEach(u=>u())}const O=typeof globalThis<"u"?globalThis:typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},y="__vueuse_ssr_handlers__";O[y]=O[y]||{};O[y];var N=Object.getOwnPropertySymbols,A=Object.prototype.hasOwnProperty,G=Object.prototype.propertyIsEnumerable,H=(e,n)=>{var o={};for(var t in e)A.call(e,t)&&n.indexOf(t)<0&&(o[t]=e[t]);if(e!=null&&N)for(var t of N(e))n.indexOf(t)<0&&G.call(e,t)&&(o[t]=e[t]);return o};function X(e,n,o={}){const t=o,{window:r=D}=t,i=H(t,["window"]);let s;const a=r&&"ResizeObserver"in r,l=()=>{s&&(s.disconnect(),s=void 0)},c=w(()=>v(e),u=>{l(),a&&r&&u&&(s=new ResizeObserver(n),s.observe(u,i))},{immediate:!0,flush:"post"}),d=()=>{l(),c()};return P(d),{isSupported:a,stop:d}}var x;(function(e){e.UP="UP",e.RIGHT="RIGHT",e.DOWN="DOWN",e.LEFT="LEFT",e.NONE="NONE"})(x||(x={}));function Y(e,n,o,t={}){var r;const{passive:i=!1,eventName:s,deep:a=!1,defaultValue:l}=t,c=I(),d=o||(c==null?void 0:c.emit)||((r=c==null?void 0:c.$emit)==null?void 0:r.bind(c));let u=s;n||(n="modelValue"),u=s||u||`update:${n.toString()}`;const f=()=>S(e[n])?e[n]:l;if(i){const p=g(f());return w(()=>e[n],m=>p.value=m),w(p,m=>{(m!==e[n]||a)&&d(u,m)},{deep:a}),p}else return R({get(){return f()},set(p){d(u,p)}})}export{K as a,B as b,_ as c,v as d,J as e,q as f,Y as g,E as i,Q as o,M as r,P as t,X as u};

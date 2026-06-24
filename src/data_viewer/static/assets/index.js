var Je=Object.defineProperty;var Ye=(r,t,e)=>t in r?Je(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e;var d=(r,t,e)=>Ye(r,typeof t!="symbol"?t+"":t,e);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const o of document.querySelectorAll('link[rel="modulepreload"]'))a(o);new MutationObserver(o=>{for(const s of o)if(s.type==="childList")for(const n of s.addedNodes)n.tagName==="LINK"&&n.rel==="modulepreload"&&a(n)}).observe(document,{childList:!0,subtree:!0});function e(o){const s={};return o.integrity&&(s.integrity=o.integrity),o.referrerPolicy&&(s.referrerPolicy=o.referrerPolicy),o.crossOrigin==="use-credentials"?s.credentials="include":o.crossOrigin==="anonymous"?s.credentials="omit":s.credentials="same-origin",s}function a(o){if(o.ep)return;o.ep=!0;const s=e(o);fetch(o.href,s)}})();/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const Tt=globalThis,Kt=Tt.ShadowRoot&&(Tt.ShadyCSS===void 0||Tt.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Jt=Symbol(),ee=new WeakMap;let ge=class{constructor(t,e,a){if(this._$cssResult$=!0,a!==Jt)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(Kt&&t===void 0){const a=e!==void 0&&e.length===1;a&&(t=ee.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),a&&ee.set(e,t))}return t}toString(){return this.cssText}};const We=r=>new ge(typeof r=="string"?r:r+"",void 0,Jt),f=(r,...t)=>{const e=r.length===1?r[0]:t.reduce((a,o,s)=>a+(n=>{if(n._$cssResult$===!0)return n.cssText;if(typeof n=="number")return n;throw Error("Value passed to 'css' function must be a 'css' function result: "+n+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(o)+r[s+1],r[0]);return new ge(e,r,Jt)},Qe=(r,t)=>{if(Kt)r.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const e of t){const a=document.createElement("style"),o=Tt.litNonce;o!==void 0&&a.setAttribute("nonce",o),a.textContent=e.cssText,r.appendChild(a)}},ae=Kt?r=>r:r=>r instanceof CSSStyleSheet?(t=>{let e="";for(const a of t.cssRules)e+=a.cssText;return We(e)})(r):r;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const{is:Xe,defineProperty:Ze,getOwnPropertyDescriptor:ta,getOwnPropertyNames:ea,getOwnPropertySymbols:aa,getPrototypeOf:oa}=Object,J=globalThis,oe=J.trustedTypes,ra=oe?oe.emptyScript:"",Lt=J.reactiveElementPolyfillSupport,yt=(r,t)=>r,At={toAttribute(r,t){switch(t){case Boolean:r=r?ra:null;break;case Object:case Array:r=r==null?r:JSON.stringify(r)}return r},fromAttribute(r,t){let e=r;switch(t){case Boolean:e=r!==null;break;case Number:e=r===null?null:Number(r);break;case Object:case Array:try{e=JSON.parse(r)}catch{e=null}}return e}},Yt=(r,t)=>!Xe(r,t),re={attribute:!0,type:String,converter:At,reflect:!1,useDefault:!1,hasChanged:Yt};Symbol.metadata??(Symbol.metadata=Symbol("metadata")),J.litPropertyMetadata??(J.litPropertyMetadata=new WeakMap);let ct=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??(this.l=[])).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=re){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const a=Symbol(),o=this.getPropertyDescriptor(t,a,e);o!==void 0&&Ze(this.prototype,t,o)}}static getPropertyDescriptor(t,e,a){const{get:o,set:s}=ta(this.prototype,t)??{get(){return this[e]},set(n){this[e]=n}};return{get:o,set(n){const p=o==null?void 0:o.call(this);s==null||s.call(this,n),this.requestUpdate(t,p,a)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??re}static _$Ei(){if(this.hasOwnProperty(yt("elementProperties")))return;const t=oa(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(yt("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(yt("properties"))){const e=this.properties,a=[...ea(e),...aa(e)];for(const o of a)this.createProperty(o,e[o])}const t=this[Symbol.metadata];if(t!==null){const e=litPropertyMetadata.get(t);if(e!==void 0)for(const[a,o]of e)this.elementProperties.set(a,o)}this._$Eh=new Map;for(const[e,a]of this.elementProperties){const o=this._$Eu(e,a);o!==void 0&&this._$Eh.set(o,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const a=new Set(t.flat(1/0).reverse());for(const o of a)e.unshift(ae(o))}else t!==void 0&&e.push(ae(t));return e}static _$Eu(t,e){const a=e.attribute;return a===!1?void 0:typeof a=="string"?a:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){var t;this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),(t=this.constructor.l)==null||t.forEach(e=>e(this))}addController(t){var e;(this._$EO??(this._$EO=new Set)).add(t),this.renderRoot!==void 0&&this.isConnected&&((e=t.hostConnected)==null||e.call(t))}removeController(t){var e;(e=this._$EO)==null||e.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const a of e.keys())this.hasOwnProperty(a)&&(t.set(a,this[a]),delete this[a]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Qe(t,this.constructor.elementStyles),t}connectedCallback(){var t;this.renderRoot??(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostConnected)==null?void 0:a.call(e)})}enableUpdating(t){}disconnectedCallback(){var t;(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostDisconnected)==null?void 0:a.call(e)})}attributeChangedCallback(t,e,a){this._$AK(t,a)}_$ET(t,e){var s;const a=this.constructor.elementProperties.get(t),o=this.constructor._$Eu(t,a);if(o!==void 0&&a.reflect===!0){const n=(((s=a.converter)==null?void 0:s.toAttribute)!==void 0?a.converter:At).toAttribute(e,a.type);this._$Em=t,n==null?this.removeAttribute(o):this.setAttribute(o,n),this._$Em=null}}_$AK(t,e){var s,n;const a=this.constructor,o=a._$Eh.get(t);if(o!==void 0&&this._$Em!==o){const p=a.getPropertyOptions(o),c=typeof p.converter=="function"?{fromAttribute:p.converter}:((s=p.converter)==null?void 0:s.fromAttribute)!==void 0?p.converter:At;this._$Em=o;const h=c.fromAttribute(e,p.type);this[o]=h??((n=this._$Ej)==null?void 0:n.get(o))??h,this._$Em=null}}requestUpdate(t,e,a,o=!1,s){var n;if(t!==void 0){const p=this.constructor;if(o===!1&&(s=this[t]),a??(a=p.getPropertyOptions(t)),!((a.hasChanged??Yt)(s,e)||a.useDefault&&a.reflect&&s===((n=this._$Ej)==null?void 0:n.get(t))&&!this.hasAttribute(p._$Eu(t,a))))return;this.C(t,e,a)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:a,reflect:o,wrapped:s},n){a&&!(this._$Ej??(this._$Ej=new Map)).has(t)&&(this._$Ej.set(t,n??e??this[t]),s!==!0||n!==void 0)||(this._$AL.has(t)||(this.hasUpdated||a||(e=void 0),this._$AL.set(t,e)),o===!0&&this._$Em!==t&&(this._$Eq??(this._$Eq=new Set)).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var a;if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??(this.renderRoot=this.createRenderRoot()),this._$Ep){for(const[s,n]of this._$Ep)this[s]=n;this._$Ep=void 0}const o=this.constructor.elementProperties;if(o.size>0)for(const[s,n]of o){const{wrapped:p}=n,c=this[s];p!==!0||this._$AL.has(s)||c===void 0||this.C(s,void 0,n,c)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),(a=this._$EO)==null||a.forEach(o=>{var s;return(s=o.hostUpdate)==null?void 0:s.call(o)}),this.update(e)):this._$EM()}catch(o){throw t=!1,this._$EM(),o}t&&this._$AE(e)}willUpdate(t){}_$AE(t){var e;(e=this._$EO)==null||e.forEach(a=>{var o;return(o=a.hostUpdated)==null?void 0:o.call(a)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&(this._$Eq=this._$Eq.forEach(e=>this._$ET(e,this[e]))),this._$EM()}updated(t){}firstUpdated(t){}};ct.elementStyles=[],ct.shadowRootOptions={mode:"open"},ct[yt("elementProperties")]=new Map,ct[yt("finalized")]=new Map,Lt==null||Lt({ReactiveElement:ct}),(J.reactiveElementVersions??(J.reactiveElementVersions=[])).push("2.1.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const $t=globalThis,se=r=>r,Ot=$t.trustedTypes,ie=Ot?Ot.createPolicy("lit-html",{createHTML:r=>r}):void 0,ue="$lit$",K=`lit$${Math.random().toFixed(9).slice(2)}$`,ve="?"+K,sa=`<${ve}>`,ot=document,wt=()=>ot.createComment(""),_t=r=>r===null||typeof r!="object"&&typeof r!="function",Wt=Array.isArray,ia=r=>Wt(r)||typeof(r==null?void 0:r[Symbol.iterator])=="function",Vt=`[ 	
\f\r]`,xt=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,ne=/-->/g,de=/>/g,tt=RegExp(`>|${Vt}(?:([^\\s"'>=/]+)(${Vt}*=${Vt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),le=/'/g,ce=/"/g,be=/^(?:script|style|textarea|title)$/i,na=r=>(t,...e)=>({_$litType$:r,strings:t,values:e}),i=na(1),rt=Symbol.for("lit-noChange"),y=Symbol.for("lit-nothing"),pe=new WeakMap,et=ot.createTreeWalker(ot,129);function me(r,t){if(!Wt(r)||!r.hasOwnProperty("raw"))throw Error("invalid template strings array");return ie!==void 0?ie.createHTML(t):t}const da=(r,t)=>{const e=r.length-1,a=[];let o,s=t===2?"<svg>":t===3?"<math>":"",n=xt;for(let p=0;p<e;p++){const c=r[p];let h,m,g=-1,u=0;for(;u<c.length&&(n.lastIndex=u,m=n.exec(c),m!==null);)u=n.lastIndex,n===xt?m[1]==="!--"?n=ne:m[1]!==void 0?n=de:m[2]!==void 0?(be.test(m[2])&&(o=RegExp("</"+m[2],"g")),n=tt):m[3]!==void 0&&(n=tt):n===tt?m[0]===">"?(n=o??xt,g=-1):m[1]===void 0?g=-2:(g=n.lastIndex-m[2].length,h=m[1],n=m[3]===void 0?tt:m[3]==='"'?ce:le):n===ce||n===le?n=tt:n===ne||n===de?n=xt:(n=tt,o=void 0);const w=n===tt&&r[p+1].startsWith("/>")?" ":"";s+=n===xt?c+sa:g>=0?(a.push(h),c.slice(0,g)+ue+c.slice(g)+K+w):c+K+(g===-2?p:w)}return[me(r,s+(r[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),a]};class kt{constructor({strings:t,_$litType$:e},a){let o;this.parts=[];let s=0,n=0;const p=t.length-1,c=this.parts,[h,m]=da(t,e);if(this.el=kt.createElement(h,a),et.currentNode=this.el.content,e===2||e===3){const g=this.el.content.firstChild;g.replaceWith(...g.childNodes)}for(;(o=et.nextNode())!==null&&c.length<p;){if(o.nodeType===1){if(o.hasAttributes())for(const g of o.getAttributeNames())if(g.endsWith(ue)){const u=m[n++],w=o.getAttribute(g).split(K),j=/([.?@])?(.*)/.exec(u);c.push({type:1,index:s,name:j[2],strings:w,ctor:j[1]==="."?ca:j[1]==="?"?pa:j[1]==="@"?ha:Et}),o.removeAttribute(g)}else g.startsWith(K)&&(c.push({type:6,index:s}),o.removeAttribute(g));if(be.test(o.tagName)){const g=o.textContent.split(K),u=g.length-1;if(u>0){o.textContent=Ot?Ot.emptyScript:"";for(let w=0;w<u;w++)o.append(g[w],wt()),et.nextNode(),c.push({type:2,index:++s});o.append(g[u],wt())}}}else if(o.nodeType===8)if(o.data===ve)c.push({type:2,index:s});else{let g=-1;for(;(g=o.data.indexOf(K,g+1))!==-1;)c.push({type:7,index:s}),g+=K.length-1}s++}}static createElement(t,e){const a=ot.createElement("template");return a.innerHTML=t,a}}function pt(r,t,e=r,a){var n,p;if(t===rt)return t;let o=a!==void 0?(n=e._$Co)==null?void 0:n[a]:e._$Cl;const s=_t(t)?void 0:t._$litDirective$;return(o==null?void 0:o.constructor)!==s&&((p=o==null?void 0:o._$AO)==null||p.call(o,!1),s===void 0?o=void 0:(o=new s(r),o._$AT(r,e,a)),a!==void 0?(e._$Co??(e._$Co=[]))[a]=o:e._$Cl=o),o!==void 0&&(t=pt(r,o._$AS(r,t.values),o,a)),t}class la{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:a}=this._$AD,o=((t==null?void 0:t.creationScope)??ot).importNode(e,!0);et.currentNode=o;let s=et.nextNode(),n=0,p=0,c=a[0];for(;c!==void 0;){if(n===c.index){let h;c.type===2?h=new Ct(s,s.nextSibling,this,t):c.type===1?h=new c.ctor(s,c.name,c.strings,this,t):c.type===6&&(h=new ga(s,this,t)),this._$AV.push(h),c=a[++p]}n!==(c==null?void 0:c.index)&&(s=et.nextNode(),n++)}return et.currentNode=ot,o}p(t){let e=0;for(const a of this._$AV)a!==void 0&&(a.strings!==void 0?(a._$AI(t,a,e),e+=a.strings.length-2):a._$AI(t[e])),e++}}class Ct{get _$AU(){var t;return((t=this._$AM)==null?void 0:t._$AU)??this._$Cv}constructor(t,e,a,o){this.type=2,this._$AH=y,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=a,this.options=o,this._$Cv=(o==null?void 0:o.isConnected)??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return e!==void 0&&(t==null?void 0:t.nodeType)===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=pt(this,t,e),_t(t)?t===y||t==null||t===""?(this._$AH!==y&&this._$AR(),this._$AH=y):t!==this._$AH&&t!==rt&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):ia(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==y&&_t(this._$AH)?this._$AA.nextSibling.data=t:this.T(ot.createTextNode(t)),this._$AH=t}$(t){var s;const{values:e,_$litType$:a}=t,o=typeof a=="number"?this._$AC(t):(a.el===void 0&&(a.el=kt.createElement(me(a.h,a.h[0]),this.options)),a);if(((s=this._$AH)==null?void 0:s._$AD)===o)this._$AH.p(e);else{const n=new la(o,this),p=n.u(this.options);n.p(e),this.T(p),this._$AH=n}}_$AC(t){let e=pe.get(t.strings);return e===void 0&&pe.set(t.strings,e=new kt(t)),e}k(t){Wt(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let a,o=0;for(const s of t)o===e.length?e.push(a=new Ct(this.O(wt()),this.O(wt()),this,this.options)):a=e[o],a._$AI(s),o++;o<e.length&&(this._$AR(a&&a._$AB.nextSibling,o),e.length=o)}_$AR(t=this._$AA.nextSibling,e){var a;for((a=this._$AP)==null?void 0:a.call(this,!1,!0,e);t!==this._$AB;){const o=se(t).nextSibling;se(t).remove(),t=o}}setConnected(t){var e;this._$AM===void 0&&(this._$Cv=t,(e=this._$AP)==null||e.call(this,t))}}class Et{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,a,o,s){this.type=1,this._$AH=y,this._$AN=void 0,this.element=t,this.name=e,this._$AM=o,this.options=s,a.length>2||a[0]!==""||a[1]!==""?(this._$AH=Array(a.length-1).fill(new String),this.strings=a):this._$AH=y}_$AI(t,e=this,a,o){const s=this.strings;let n=!1;if(s===void 0)t=pt(this,t,e,0),n=!_t(t)||t!==this._$AH&&t!==rt,n&&(this._$AH=t);else{const p=t;let c,h;for(t=s[0],c=0;c<s.length-1;c++)h=pt(this,p[a+c],e,c),h===rt&&(h=this._$AH[c]),n||(n=!_t(h)||h!==this._$AH[c]),h===y?t=y:t!==y&&(t+=(h??"")+s[c+1]),this._$AH[c]=h}n&&!o&&this.j(t)}j(t){t===y?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class ca extends Et{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===y?void 0:t}}class pa extends Et{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==y)}}class ha extends Et{constructor(t,e,a,o,s){super(t,e,a,o,s),this.type=5}_$AI(t,e=this){if((t=pt(this,t,e,0)??y)===rt)return;const a=this._$AH,o=t===y&&a!==y||t.capture!==a.capture||t.once!==a.once||t.passive!==a.passive,s=t!==y&&(a===y||o);o&&this.element.removeEventListener(this.name,this,a),s&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e;typeof this._$AH=="function"?this._$AH.call(((e=this.options)==null?void 0:e.host)??this.element,t):this._$AH.handleEvent(t)}}class ga{constructor(t,e,a){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=a}get _$AU(){return this._$AM._$AU}_$AI(t){pt(this,t)}}const Rt=$t.litHtmlPolyfillSupport;Rt==null||Rt(kt,Ct),($t.litHtmlVersions??($t.litHtmlVersions=[])).push("3.3.2");const ua=(r,t,e)=>{const a=(e==null?void 0:e.renderBefore)??t;let o=a._$litPart$;if(o===void 0){const s=(e==null?void 0:e.renderBefore)??null;a._$litPart$=o=new Ct(t.insertBefore(wt(),s),s,void 0,e??{})}return o._$AI(r),o};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const at=globalThis;let b=class extends ct{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e;const t=super.createRenderRoot();return(e=this.renderOptions).renderBefore??(e.renderBefore=t.firstChild),t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=ua(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),(t=this._$Do)==null||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),(t=this._$Do)==null||t.setConnected(!1)}render(){return rt}};var he;b._$litElement$=!0,b.finalized=!0,(he=at.litElementHydrateSupport)==null||he.call(at,{LitElement:b});const qt=at.litElementPolyfillSupport;qt==null||qt({LitElement:b});(at.litElementVersions??(at.litElementVersions=[])).push("4.2.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const x=r=>(t,e)=>{e!==void 0?e.addInitializer(()=>{customElements.define(r,t)}):customElements.define(r,t)};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const va={attribute:!0,type:String,converter:At,reflect:!1,hasChanged:Yt},ba=(r=va,t,e)=>{const{kind:a,metadata:o}=e;let s=globalThis.litPropertyMetadata.get(o);if(s===void 0&&globalThis.litPropertyMetadata.set(o,s=new Map),a==="setter"&&((r=Object.create(r)).wrapped=!0),s.set(e.name,r),a==="accessor"){const{name:n}=e;return{set(p){const c=t.get.call(this);t.set.call(this,p),this.requestUpdate(n,c,r,!0,p)},init(p){return p!==void 0&&this.C(n,void 0,r,p),p}}}if(a==="setter"){const{name:n}=e;return function(p){const c=this[n];t.call(this,p),this.requestUpdate(n,c,r,!0,p)}}throw Error("Unsupported decorator location: "+a)};function $(r){return(t,e)=>typeof e=="object"?ba(r,t,e):((a,o,s)=>{const n=o.hasOwnProperty(s);return o.constructor.createProperty(s,a),n?Object.getOwnPropertyDescriptor(o,s):void 0})(r,t,e)}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function l(r){return $({...r,state:!0,attribute:!1})}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ma={CHILD:2},fa=r=>(...t)=>({_$litDirective$:r,values:t});class xa{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,a){this._$Ct=t,this._$AM=e,this._$Ci=a}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class Ht extends xa{constructor(t){if(super(t),this.it=y,t.type!==ma.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===y||t==null)return this._t=void 0,this.it=t;if(t===rt)return t;if(typeof t!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.it)return this._t;this.it=t;const e=[t];return e.raw=e,this._t={_$litType$:this.constructor.resultType,strings:e,values:[]}}}Ht.directiveName="unsafeHTML",Ht.resultType=1;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class Gt extends Ht{}Gt.directiveName="unsafeSVG",Gt.resultType=2;const Bt=fa(Gt),E="/api";async function I(r,t){const e=await fetch(r,t);if(!e.ok){const a=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(a.detail||`HTTP ${e.status}`)}return e.json()}async function ya(){return I(`${E}/stats`)}async function $a(r){return I(`${E}/categories`)}async function wa(r){const t=new URLSearchParams(Object.entries(r).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return I(`${E}/product-master?${t}`)}async function fe(r,t=7){return I(`${E}/sales-trend/${r}?days=${t}`)}async function _a(r){return I(`${E}/tracked-products?ids=${r.join(",")}`)}async function ka(r){return I(`${E}/config/${r}`)}async function Pa(){return{app_name:(await ka("settings")).data.app_name||"EcomAgent"}}async function za(r,t=7){return I(`${E}/product-trend/${r}?days=${t}`)}async function Sa(){return I(`${E}/amazon/top-by-category`)}async function Ca(){return I(`${E}/tiktok/top-by-category`)}async function Ta(r){const t=new URLSearchParams(Object.entries(r).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return I(`${E}/amazon/products?${t}`)}async function Aa(r){const t=new URLSearchParams(Object.entries(r).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return I(`${E}/tiktok/products?${t}`)}async function Oa(){return I(`${E}/cross-platform-analysis`)}var xe=Object.defineProperty,Ma=Object.getOwnPropertyDescriptor,Da=(r,t,e)=>t in r?xe(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,Qt=(r,t,e,a)=>{for(var o=a>1?void 0:a?Ma(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&xe(t,e,o),o},Ea=(r,t,e)=>Da(r,t+"",e);const Ia=[{group:"Main",items:[{id:"dashboard",icon:"grid",label:"数据概览"},{id:"product-master",icon:"box",label:"商品总库"},{id:"sourcing",icon:"package",label:"货源库"},{id:"assets",icon:"folder",label:"素材管理"},{id:"tracking",icon:"target",label:"商品追踪"},{id:"cross-platform",icon:"sync",label:"跨平台分析"}]},{group:"平台数据",items:[{id:"today-top",icon:"star",label:"今日TOP榜"},{id:"raw-data",icon:"database",label:"原始数据"}]},{group:"系统",items:[{id:"export",icon:"download",label:"数据导出"},{id:"translation-logs",icon:"file-text",label:"翻译日志"},{id:"settings",icon:"settings",label:"系统设置"}]}],ja={grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',box:'<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',package:'<line x1="16.5" y1="9.4" x2="7.5" y1="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/><line x1="12" y1="12" x2="7.5" y1="9.4"/>',target:'<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',sync:'<path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/>',star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',database:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',settings:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',"file-text":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',folder:'<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'};let Pt=class extends b{constructor(){super();d(this,"collapsed",!1);d(this,"appName",window.ecomagentAppName||"EcomAgent");d(this,"_currentPage","dashboard");this._loadAppName(),window.ecomagentOnPageChange&&window.ecomagentOnPageChange(t=>{this._currentPage=t,this.requestUpdate()}),window.ecomagentGetCurrentPage&&(this._currentPage=window.ecomagentGetCurrentPage())}async _loadAppName(){if(window.ecomagentAppName){this.appName=window.ecomagentAppName;return}try{const t=await Pa();this.appName=t.app_name,window.ecomagentAppName=t.app_name}catch(t){console.error("Failed to load app name:",t)}}_onNavClick(t){if(t==="sourcing"&&window.ecomagentNavigateDirectToSourcing){window.ecomagentNavigateDirectToSourcing();return}window.ecomagentNavigate&&window.ecomagentNavigate(t)}_onToggle(){this.collapsed=!this.collapsed,this.requestUpdate("collapsed")}render(){const t=this._currentPage,e=this.appName.charAt(0);return i`
      <div class="header">
        <div class="brand">
          <div class="logo">${e}</div>
          <div class="brand-text">
            <span class="brand-title">${this.appName}</span>
            <span class="brand-subtitle">数据可视化平台</span>
          </div>
        </div>
        <button class="toggle-btn" @click=${this._onToggle}>
          <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
      </div>
      <div class="nav-content">
        ${Ia.map(a=>i`
          <div class="nav-group">
            <div class="nav-group-header"><span class="nav-group-title">${a.group}</span></div>
            <ul class="nav-items">
              ${a.items.map(o=>i`
                <li class="nav-item ${t===o.id?"active":""}" @click=${()=>this._onNavClick(o.id)}>
                  <svg class="nav-icon" viewBox="0 0 24 24">${Bt(ja[o.icon])}</svg>
                  <span class="nav-label">${o.label}</span>
                </li>
              `)}
            </ul>
          </div>
        `)}
      </div>
    `}};Ea(Pt,"styles",f`
    :host { width: 258px; background: var(--panel); color: var(--text); padding: 14px 10px 12px; flex-shrink: 0; border-right: 1px solid var(--border); transition: width 0.2s ease; overflow: hidden; display: flex; flex-direction: column; }
    :host([collapsed]) { width: 60px; padding: 14px 6px 12px; }
    .header { display: flex; align-items: center; justify-content: space-between; padding: 14px 10px; border-bottom: 1px solid var(--border); margin-bottom: 12px; flex-shrink: 0; }
    :host([collapsed]) .header { justify-content: center; border-bottom: none; padding: 14px 0; }
    .brand { display: flex; align-items: center; gap: 10px; }
    :host([collapsed]) .brand { display: none; }
    .logo { width: 32px; height: 32px; background: var(--accent); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px; }
    .brand-text { display: flex; flex-direction: column; gap: 2px; }
    .brand-title { font-size: 15px; font-weight: 700; color: var(--text-strong); }
    .brand-subtitle { font-size: 10px; color: var(--muted); }
    .toggle-btn { width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: transparent; border: none; border-radius: 6px; cursor: pointer; color: var(--muted); transition: 0.15s ease; }
    .toggle-btn:hover { color: var(--text); background: var(--bg-hover); }
    .toggle-btn svg { width: 16px; height: 16px; stroke: currentColor; fill: none; stroke-width: 1.5; transition: transform 0.15s ease; }
    :host([collapsed]) .toggle-btn svg { transform: rotate(180deg); }
    .nav-content { flex: 1; overflow-y: auto; }
    .nav-group { margin-bottom: 8px; }
    .nav-group-header { padding: 8px 10px; margin-bottom: 4px; }
    :host([collapsed]) .nav-group-header { display: none; }
    .nav-group-title { font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
    .nav-items { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 4px; }
    .nav-item { padding: 8px 10px; cursor: pointer; border-radius: 8px; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 8px; color: var(--muted); border: 1px solid transparent; background: transparent; user-select: none; transition: 0.15s ease; }
    .nav-item:hover { background: var(--bg-hover); border-color: var(--border-hover); color: var(--text); }
    .nav-item.active { background: var(--accent-subtle); border-color: color-mix(in srgb, var(--accent) 25%, transparent); color: var(--accent); }
    :host([collapsed]) .nav-item { justify-content: center; padding: 8px 0; }
    .nav-icon { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
    :host([collapsed]) .nav-icon { display: block; }
    :host([collapsed]) .nav-label { display: none; }
  `);Qt([$({type:Boolean,reflect:!0})],Pt.prototype,"collapsed",2);Qt([l()],Pt.prototype,"appName",2);Pt=Qt([x("ea-sidebar")],Pt);var ye=Object.defineProperty,Ua=Object.getOwnPropertyDescriptor,Na=(r,t,e)=>t in r?ye(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,$e=(r,t,e,a)=>{for(var o=a>1?void 0:a?Ua(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&ye(t,e,o),o},Fa=(r,t,e)=>Na(r,t+"",e);const La={dashboard:{title:"数据概览",subtitle:"查看数据统计和概览"},"product-master":{title:"商品总库",subtitle:"统一管理所有平台商品"},sourcing:{title:"货源库",subtitle:"1688货源采集与管理"},assets:{title:"素材管理",subtitle:"生成和管理商品素材"},tracking:{title:"商品追踪",subtitle:"追踪特定商品的价格、销量变化"},"cross-platform":{title:"跨平台分析",subtitle:"对比分析不同平台数据"},"today-top":{title:"今日TOP榜",subtitle:"各平台热销产品排行"},"raw-data":{title:"原始数据",subtitle:"查看和搜索原始数据"},export:{title:"数据导出",subtitle:"导出数据为 CSV 或 Excel"},"translation-logs":{title:"翻译日志",subtitle:"翻译任务执行记录"},settings:{title:"系统设置",subtitle:"配置数据源和其他选项"},"product-trend":{title:"商品趋势",subtitle:"查看商品各维度数据随时间变化"}};let Mt=class extends b{constructor(){super(...arguments);d(this,"currentPage","dashboard")}toggleTheme(){const t=document.body,a=t.getAttribute("data-theme-mode")==="dark"?"light":"dark";t.setAttribute("data-theme-mode",a),localStorage.setItem("theme",a),this.requestUpdate()}render(){const{title:t,subtitle:e}=La[this.currentPage],a=document.body.getAttribute("data-theme-mode")!=="light";return i`
      <div>
        <div class="title">${t}</div>
        <div class="subtitle">${e}</div>
      </div>
      
      <div class="actions">
        <button class="icon-btn" @click=${this.toggleTheme} title="切换主题">
          ${a?i`
            <svg viewBox="0 0 24 24">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          `:i`
            <svg viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="4"></circle>
              <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>
            </svg>
          `}
        </button>
        
        <button class="icon-btn" @click=${()=>this.dispatchEvent(new Event("refresh"))} title="刷新数据">
          <svg viewBox="0 0 24 24">
            <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l5.64 5.64A9 9 0 0 0 20.49 15"></path>
          </svg>
        </button>
      </div>
    `}};Fa(Mt,"styles",f`
    :host {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }

    .title {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
    }

    .subtitle {
      font-size: 13px;
      color: var(--muted);
      margin-top: 2px;
    }

    .actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .icon-btn {
      width: 30px;
      height: 30px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid var(--border);
      border-radius: var(--radius-full);
      background: var(--bg-elevated);
      color: var(--muted);
      cursor: pointer;
      transition: var(--duration-fast) ease;
    }

    .icon-btn:hover {
      color: var(--text);
      background: var(--bg-hover);
    }

    .icon-btn svg {
      width: 14px;
      height: 14px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.75px;
    }
  `);$e([$({type:String})],Mt.prototype,"currentPage",2);Mt=$e([x("ea-header")],Mt);var we=Object.defineProperty,Va=Object.getOwnPropertyDescriptor,Ra=(r,t,e)=>t in r?we(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,Xt=(r,t,e,a)=>{for(var o=a>1?void 0:a?Va(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&we(t,e,o),o},qa=(r,t,e)=>Ra(r,t+"",e);let zt=class extends b{constructor(){super(...arguments);d(this,"currentPage","dashboard");d(this,"sidebarCollapsed",!1)}render(){return i`
      <ea-sidebar ?collapsed=${this.sidebarCollapsed}></ea-sidebar>
      <main class="main-content">
        <ea-header .currentPage=${this.currentPage}></ea-header>
        <div class="content-body"><slot></slot></div>
      </main>
    `}};qa(zt,"styles",f`
    :host { display: flex; min-height: 100vh; }
    .main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
    .content-body { animation: fadeIn 0.3s ease; }
    @media (max-width: 1024px) { :host { flex-direction: column; } .main-content { padding: 16px; } }
  `);Xt([$({type:String})],zt.prototype,"currentPage",2);Xt([l()],zt.prototype,"sidebarCollapsed",2);zt=Xt([x("ea-layout")],zt);var _e=Object.defineProperty,Ha=Object.getOwnPropertyDescriptor,Ga=(r,t,e)=>t in r?_e(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,X=(r,t,e,a)=>{for(var o=a>1?void 0:a?Ha(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&_e(t,e,o),o},ke=(r,t,e)=>Ga(r,t+"",e);let Dt=class extends b{constructor(){super(...arguments);d(this,"padding",16)}render(){return i`
      <slot name="header"></slot>
      <div class="card-content" style="--padding: ${this.padding}px">
        <slot></slot>
      </div>
    `}};ke(Dt,"styles",f`
    :host {
      display: block;
      background: var(--card);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
      transition: var(--duration-normal) var(--ease-out);
    }

    :host(:hover) {
      box-shadow: var(--shadow-md);
    }

    .card-content {
      padding: var(--padding, 16px);
    }

    ::slotted([slot="header"]) {
      padding: 12px 16px;
      background: var(--bg-accent);
      border-bottom: 1px solid var(--border);
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
    }
  `);X([$({type:Number})],Dt.prototype,"padding",2);Dt=X([x("ea-card")],Dt);let Y=class extends b{constructor(){super(...arguments);d(this,"label","");d(this,"value","-");d(this,"icon","");d(this,"desc","");d(this,"color","")}render(){return i`
      <div class="stat-header">
        <div>
          <div class="stat-label">${this.label}</div>
          <div class="stat-value ${this.color}">${this.value}</div>
          ${this.desc?i`<div class="stat-desc">${this.desc}</div>`:""}
        </div>
        ${this.icon?i`<span class="stat-icon">${this.icon}</span>`:""}
      </div>
      <slot></slot>
    `}};ke(Y,"styles",f`
    :host {
      display: block;
      background: var(--card);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--border);
      padding: 20px;
    }

    .stat-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 16px;
    }

    .stat-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .stat-icon {
      font-size: 24px;
    }

    .stat-value {
      font-size: 32px;
      font-weight: 700;
      color: var(--text-strong);
    }

    .stat-value.accent {
      color: var(--accent);
    }

    .stat-value.ok {
      color: var(--ok);
    }

    .stat-value.info {
      color: #00f2ea;
    }

    .stat-desc {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }

    .stat-footer {
      display: flex;
      justify-content: flex-end;
      align-items: flex-end;
      margin-top: 16px;
    }

    .stat-action {
      margin-left: auto;
    }
  `);X([$({type:String})],Y.prototype,"label",2);X([$({type:String})],Y.prototype,"value",2);X([$({type:String})],Y.prototype,"icon",2);X([$({type:String})],Y.prototype,"desc",2);X([$({type:String})],Y.prototype,"color",2);Y=X([x("ea-stat-card")],Y);var Pe=Object.defineProperty,Ba=Object.getOwnPropertyDescriptor,Ka=(r,t,e)=>t in r?Pe(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,G=(r,t,e,a)=>{for(var o=a>1?void 0:a?Ba(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Pe(t,e,o),o},Ja=(r,t,e)=>Ka(r,t+"",e);let U=class extends b{constructor(){super(...arguments);d(this,"stats",null);d(this,"loading",!0);d(this,"error","");d(this,"expandedPanel",null);d(this,"categories",{amazon:[],tiktok:[]});d(this,"categoriesLoading",!1);d(this,"fetchTaskStatus",{amazon:"",tiktok:""});d(this,"importStatus",{amazon:"",tiktok:""})}connectedCallback(){super.connectedCallback(),this.loadStats()}async loadStats(){this.loading=!0,this.error="";try{this.stats=await ya()}catch(t){this.error=t instanceof Error?t.message:String(t)}finally{this.loading=!1,this.requestUpdate()}}async _togglePanel(t){if(this.expandedPanel===t){this.expandedPanel=null;return}this.expandedPanel=t,this.requestUpdate(),(!this.categories[t]||this.categories[t].length===0)&&await this._loadCategories(t)}async _loadCategories(t){this.categoriesLoading=!0,this.requestUpdate();try{const a=await(await fetch(`/api/categories/${t}`)).json();this.categories={...this.categories,[t]:a.categories||[]},this.requestUpdate()}catch(e){console.error("加载类目失败:",e)}finally{this.categoriesLoading=!1,this.requestUpdate()}}async _refreshCategories(t){this.categoriesLoading=!0;try{const a=await(await fetch(`/api/categories/${t}/refresh`,{method:"POST"})).json();a.success?await this._loadCategories(t):alert(a.message||"刷新失败")}catch(e){alert(`刷新失败: ${e}`)}finally{this.categoriesLoading=!1}}async _toggleCategory(t,e,a){try{await fetch(`/api/categories/${e}/enabled?enabled=${a}`,{method:"PUT"}),this.categories={...this.categories,[t]:this.categories[t].map(o=>o.id===e?{...o,enabled:a?1:0}:o)}}catch(o){alert(`更新失败: ${o}`)}}async _startFetch(t){this.fetchTaskStatus={...this.fetchTaskStatus,[t]:"running"};try{const a=await(await fetch(`/api/tasks/${t}/fetch`,{method:"POST"})).json();a.success?alert(`${t} 抓取任务已启动`):(alert(a.message||"启动失败"),this.fetchTaskStatus={...this.fetchTaskStatus,[t]:""})}catch(e){alert(`启动失败: ${e}`),this.fetchTaskStatus={...this.fetchTaskStatus,[t]:""}}}async _importData(t){this.importStatus={...this.importStatus,[t]:"running"},this.requestUpdate();try{const a=await(await fetch("/api/tasks/data-import",{method:"POST"})).json();a.success?await this.loadStats():alert(a.message||"导入失败")}catch(e){alert(`导入失败: ${e}`)}finally{this.importStatus={...this.importStatus,[t]:""},this.requestUpdate()}}_renderFetchPanel(t){const e=this.expandedPanel===t,a=this.categories[t],o=this.categoriesLoading,s=this.fetchTaskStatus[t]==="running",n=a.filter(c=>c.today_status==="done").length,p=a.filter(c=>c.today_status==="pending").length;return i`
      <div class="fetch-panel ${e?"expanded":""}">
        <div class="fetch-header" @click=${()=>this._togglePanel(t)}>
          <div class="fetch-header-left">
            <svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
            <span class="fetch-header-title">数据抓取</span>
            ${a.length>0?i`
              <span class="fetch-header-badge">${a.length} 个类目 · 今日已抓 ${n} / 待抓 ${p}</span>
            `:""}
          </div>
        </div>

        <div class="fetch-content">
          ${o?i`<div class="empty-text">加载中...</div>`:""}

          ${!o&&a.length===0?i`
            <div class="empty-text">暂无类目数据,请点击「刷新类目」获取</div>
          `:""}

          ${!o&&a.length>0?i`
            <div class="category-list">
              ${a.map(c=>i`
                <div class="category-item">
                  <input
                    type="checkbox"
                    class="category-checkbox"
                    .checked=${c.enabled===1}
                    @change=${h=>this._toggleCategory(t,c.id,h.target.checked)}
                  >
                  <span class="category-name">${c.name}</span>
                  <span class="category-status ${c.today_status}">
                    ${c.today_status==="done"||c.today_status==="skipped"?`已抓 ${c.today_count||c.last_products_count||0} 个`:c.last_scraped_at?`上次: ${new Date(c.last_scraped_at).toLocaleDateString()}`:"未抓取"}
                  </span>
                </div>
              `)}
            </div>
          `:""}

          <div class="fetch-actions">
            <button @click=${()=>this._refreshCategories(t)} ?disabled=${o}>
              刷新类目
            </button>
            <button
              class="primary"
              @click=${()=>this._startFetch(t)}
              ?disabled=${s||a.filter(c=>c.enabled&&c.today_status==="pending").length===0}
            >
              ${s?"抓取中...":"开始抓取"}
            </button>
          </div>
        </div>
      </div>
    `}render(){if(this.loading)return i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;if(this.error)return i`
        <div class="error-box">
          <p>加载失败: ${this.error}</p>
          <button class="retry-btn" @click=${this.loadStats}>重试</button>
        </div>
      `;if(!this.stats)return i`<div class="error-box"><p>无数据</p></div>`;const{amazon:t,tiktok:e}=this.stats;return i`
      <h2>数据概览</h2>

      <div class="stats-grid">
        <div>
          <ea-stat-card
            label="Amazon"
            .value=${t.products.toLocaleString()}
            icon="📦"
            desc="商品总数"
            color="accent"
          >
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
              <span style="font-size: 13px; color: var(--muted);">今日新增: ${t.today.toLocaleString()}</span>
              <button class="update-btn amazon" @click=${()=>this._importData("amazon")} ?disabled=${this.importStatus.amazon==="running"}>
                ${this.importStatus.amazon==="running"?"导入中...":"更新数据"}
              </button>
            </div>
          </ea-stat-card>
          ${this._renderFetchPanel("amazon")}
        </div>

        <div>
          <ea-stat-card
            label="TikTok"
            .value=${e.products.toLocaleString()}
            icon="🎵"
            desc="商品总数"
            color="info"
          >
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
              <span style="font-size: 13px; color: var(--muted);">今日新增: ${e.today.toLocaleString()}</span>
              <button class="update-btn tiktok" @click=${()=>this._importData("tiktok")} ?disabled=${this.importStatus.tiktok==="running"}>
                ${this.importStatus.tiktok==="running"?"导入中...":"更新数据"}
              </button>
            </div>
          </ea-stat-card>
          ${this._renderFetchPanel("tiktok")}
        </div>
      </div>
    `}};Ja(U,"styles",f`
    :host { display: block; }
    h2 { font-size: 20px; font-weight: 700; color: var(--text-strong); margin-bottom: 24px; }
    .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; }
    .loading { text-align: center; padding: 48px; color: var(--muted); }
    .spinner { width: 40px; height: 40px; border: 2px solid var(--accent); border-top-color: transparent; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 16px; }
    .error-box { background: var(--danger-subtle); border: 1px solid var(--danger); border-radius: 8px; padding: 16px; color: var(--danger); margin-bottom: 24px; }
    .retry-btn { margin-top: 12px; padding: 8px 16px; background: var(--accent); color: white; border: none; border-radius: 6px; cursor: pointer; }
    .retry-btn:hover { background: var(--accent-hover); }
    .update-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: none;
    }
    .update-btn.amazon { background: var(--accent-subtle); color: var(--accent); border: 1px solid var(--accent); }
    .update-btn.amazon:hover { background: var(--accent); color: white; }
    .update-btn.tiktok { background: rgba(0, 242, 234, 0.1); color: #00f2ea; border: 1px solid #00f2ea; }
    .update-btn.tiktok:hover { background: #00f2ea; color: black; }
    .update-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    /* 数据抓取卡片 */
    .fetch-panel { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius-lg); margin-top: 8px; overflow: hidden; }
    .fetch-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; cursor: pointer; transition: background 0.15s ease; }
    .fetch-header:hover { background: var(--bg-hover); }
    .fetch-header-left { display: flex; align-items: center; gap: 8px; }
    .fetch-header-left svg { width: 16px; height: 16px; stroke: var(--muted); fill: none; stroke-width: 2; transition: transform 0.2s ease; }
    .fetch-panel.expanded .fetch-header-left svg { transform: rotate(90deg); }
    .fetch-header-title { font-size: 14px; font-weight: 500; color: var(--text); }
    .fetch-header-badge { font-size: 12px; color: var(--muted); }
    .fetch-content { display: none; padding: 16px; border-top: 1px solid var(--border); }
    .fetch-panel.expanded .fetch-content { display: block; }

    .category-list { max-height: 300px; overflow-y: auto; }
    .category-item { display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); }
    .category-item:last-child { border-bottom: none; }
    .category-checkbox { width: 16px; height: 16px; margin-right: 12px; accent-color: var(--accent); cursor: pointer; }
    .category-name { flex: 1; font-size: 13px; color: var(--text); }
    .category-status { font-size: 12px; color: var(--muted); }
    .category-status.done, .category-status.skipped { color: var(--ok); }
    .category-status.pending { color: var(--muted); }

    .fetch-actions { display: flex; gap: 8px; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border); }
    .fetch-actions button { padding: 8px 16px; border-radius: 6px; font-size: 13px; cursor: pointer; border: 1px solid var(--border); background: var(--bg-elevated); color: var(--text); }
    .fetch-actions button:hover { background: var(--bg-hover); }
    .fetch-actions button.primary { background: var(--accent); color: white; border-color: var(--accent); }
    .fetch-actions button.primary:hover { background: var(--accent-hover); }
    .fetch-actions button:disabled { opacity: 0.5; cursor: not-allowed; }
    .empty-text { text-align: center; color: var(--muted); padding: 24px; font-size: 13px; }

    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 768px) { .stats-grid { grid-template-columns: 1fr; } }
  `);G([l()],U.prototype,"stats",2);G([l()],U.prototype,"loading",2);G([l()],U.prototype,"error",2);G([l()],U.prototype,"expandedPanel",2);G([l()],U.prototype,"categories",2);G([l()],U.prototype,"categoriesLoading",2);G([l()],U.prototype,"fetchTaskStatus",2);G([l()],U.prototype,"importStatus",2);U=G([x("ea-dashboard")],U);var ze=Object.defineProperty,Ya=Object.getOwnPropertyDescriptor,Wa=(r,t,e)=>t in r?ze(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,it=(r,t,e,a)=>{for(var o=a>1?void 0:a?Ya(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&ze(t,e,o),o},Qa=(r,t,e)=>Wa(r,t+"",e);let V=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"product",null);d(this,"trendData",[]);d(this,"loading",!0);d(this,"metric","rating");d(this,"days",7)}connectedCallback(){super.connectedCallback(),this.ecomCode&&this.loadTrendData()}updated(t){t.has("ecomCode")&&this.ecomCode&&this.loadTrendData()}async loadTrendData(){if(this.ecomCode){this.loading=!0;try{const t=await za(this.ecomCode,this.days);this.product=t.product,this.trendData=t.trend||[]}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}}_onMetricChange(t){this.metric=t.target.value,this.requestUpdate()}_onDaysChange(t){const e=t.target.value;e!=="custom"&&(this.days=parseInt(e),this.loadTrendData())}_getMetricLabel(){switch(this.metric){case"price":return"价格";case"rating":return"评分";case"rank":return"排名"}}_renderChart(){if(this.trendData.length===0)return i`<div class="chart-empty">暂无数据</div>`;const t=this.trendData.map(s=>s[this.metric]).filter(s=>s!=null);if(t.length===0)return i`<div class="chart-empty">暂无${this._getMetricLabel()}数据</div>`;const e=Math.max(...t),a=Math.min(...t),o=e-a||1;return i`
      <div class="chart">
        ${this.trendData.map(s=>{const n=s[this.metric];if(n==null)return i`<div class="chart-bar" style="height:0"></div>`;const p=(n-a)/o*250+20;return i`
            <div class="chart-bar" style="height:${p}px">
              <span class="chart-bar-value">${this.metric==="rating"?n.toFixed(1):n}</span>
              <span class="chart-bar-label">${s.date.slice(5)}</span>
            </div>
          `})}
      </div>
    `}_renderTrend(t,e){if(t===null||e===null)return"-";const a=t-e;return Math.abs(a)<.01?"-":this.metric==="rank"?a<0?i`<span class="trend-up">↑${Math.abs(a).toFixed(0)}</span>`:i`<span class="trend-down">↓${Math.abs(a).toFixed(0)}</span>`:a>0?i`<span class="trend-up">↑${a.toFixed(2)}</span>`:i`<span class="trend-down">↓${Math.abs(a).toFixed(2)}</span>`}render(){return this.loading?i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.product?i`
      <div class="header">
        <a class="back-link" href="javascript:history.back()">← 返回</a>
        <h2>趋势分析</h2>
      </div>

      <div class="product-info">
        <div class="product-name">${this.product.name||this.product.short_name||"未知商品"}</div>
        <div class="product-meta">
          编码: ${this.product.ecom_code} | 平台: ${this.product.platform} | 
          分类: ${this.product.category||"-"}
        </div>
      </div>

      <div class="controls">
        <div class="control-group">
          <span class="control-label">指标:</span>
          <select class="select" .value=${this.metric} @change=${this._onMetricChange}>
            <option value="rating">评分</option>
            <option value="price">价格</option>
            <option value="rank">排名</option>
          </select>
        </div>
        <div class="control-group">
          <span class="control-label">时间区间:</span>
          <select class="select" .value=${String(this.days)} @change=${this._onDaysChange}>
            <option value="7">7天</option>
            <option value="15">15天</option>
            <option value="30">30天</option>
          </select>
        </div>
      </div>

      <div class="chart-container">
        <div class="chart-title">${this._getMetricLabel()}变化趋势</div>
        ${this._renderChart()}
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>日期</th>
              <th>价格</th>
              <th>评分</th>
              <th>排名</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            ${this.trendData.map((t,e)=>{const a=e<this.trendData.length-1?this.trendData[e+1]:null;return i`
                <tr>
                  <td>${t.date}</td>
                  <td>${t.price!==null?`$${t.price.toFixed(2)}`:"-"}</td>
                  <td>${t.rating!==null?t.rating.toFixed(1):"-"}</td>
                  <td>${t.rank!==null?t.rank:"-"}</td>
                  <td>${a?this._renderTrend(t[this.metric],a[this.metric]):"-"}</td>
                </tr>
              `})}
          </tbody>
        </table>
      </div>
    `:i`
        <div class="header">
          <a class="back-link" href="javascript:history.back()">← 返回</a>
        </div>
        <div style="text-align:center;padding:48px;color:var(--muted)">商品不存在</div>
      `}};Qa(V,"styles",f`
    :host { display: block; padding: 24px; }
    
    .header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 24px;
    }
    
    .back-link {
      color: var(--accent);
      text-decoration: none;
      font-size: 13px;
    }
    
    .back-link:hover { text-decoration: underline; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin: 0;
    }
    
    .product-info {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .product-name {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 8px;
    }
    
    .product-meta {
      font-size: 13px;
      color: var(--muted);
    }
    
    .controls {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
      flex-wrap: wrap;
      align-items: center;
    }
    
    .control-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .control-label {
      font-size: 13px;
      color: var(--muted);
    }
    
    .select {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
    }
    
    .select:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .chart-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
      margin-bottom: 24px;
    }
    
    .chart-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 16px;
    }
    
    .chart {
      height: 300px;
      display: flex;
      align-items: flex-end;
      gap: 4px;
      padding: 20px 0;
      border-bottom: 1px solid var(--border);
      position: relative;
    }
    
    .chart-bar {
      flex: 1;
      background: var(--accent);
      border-radius: 4px 4px 0 0;
      min-width: 20px;
      max-width: 60px;
      position: relative;
      transition: height 0.3s ease;
    }
    
    .chart-bar:hover {
      background: var(--accent-hover);
    }
    
    .chart-bar-label {
      position: absolute;
      bottom: -24px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 10px;
      color: var(--muted);
      white-space: nowrap;
    }
    
    .chart-bar-value {
      position: absolute;
      top: -20px;
      left: 50%;
      transform: translateX(-50%);
      font-size: 10px;
      color: var(--text);
      white-space: nowrap;
    }
    
    .chart-empty {
      height: 300px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
    }
    
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    th {
      background: var(--bg-accent);
      padding: 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    
    td {
      padding: 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .trend-up { color: var(--ok); }
    .trend-down { color: var(--danger); }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
  `);it([$({type:String})],V.prototype,"ecomCode",2);it([l()],V.prototype,"product",2);it([l()],V.prototype,"trendData",2);it([l()],V.prototype,"loading",2);it([l()],V.prototype,"metric",2);it([l()],V.prototype,"days",2);V=it([x("ea-product-trend")],V);var Se=Object.defineProperty,Xa=Object.getOwnPropertyDescriptor,Za=(r,t,e)=>t in r?Se(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,z=(r,t,e,a)=>{for(var o=a>1?void 0:a?Xa(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Se(t,e,o),o},to=(r,t,e)=>Za(r,t+"",e);let _=class extends b{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"platform","amazon");d(this,"category","");d(this,"categories",{amazon:[],tiktok:[],all:[]});d(this,"sortBy","total_sales");d(this,"sortOrder","desc");d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map);d(this,"previewImg",{show:!1,src:"",x:0,y:0})}async connectedCallback(){super.connectedCallback(),this.loadTracked(),await this.loadCategories(),this.loadData()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t)))}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadCategories(){try{if(this.categories=await $a(),!this.category){const t=this.platform==="amazon"?this.categories.amazon:this.categories.tiktok;t.length>0&&(this.category=t[0])}}catch(t){console.error("Failed to load categories",t)}}async loadData(){this.loading=!0;try{const t=await wa({page:this.page,limit:20,search:this.search,platform:this.platform,category:this.category,sort_by:this.sortBy||void 0,sort_order:this.sortOrder});this.products=t.data,this.pages=t.pagination.pages,this.loadSparklines(t.data)}catch(t){console.error("Failed to load products",t)}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async a=>{try{const o=await fe(a.ecom_code,7);this.sparklines.set(a.ecom_code,o.trend)}catch{this.sparklines.set(a.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_onPlatformChange(t){this.platform=t;const e=t==="amazon"?this.categories.amazon:this.categories.tiktok;this.category=e.length>0?e[0]:"",this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onInputChange(t,e){this[e]=t.target.value}_onCategoryChange(t){this.category=t.target.value,this.page=1,this.loadData()}_onSort(t){this.sortBy===t?this.sortOrder=this.sortOrder==="desc"?"asc":"desc":(this.sortBy=t,this.sortOrder="desc"),this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_toggleTrack(t){this.trackedIds.has(t)?this.trackedIds.delete(t):this.trackedIds.add(t),this.saveTracked(),this.requestUpdate()}async _resetTranslation(t){try{(await(await fetch(`/api/products/${t}/reset-translation`,{method:"POST"})).json()).success&&this.loadData()}catch(e){console.error("Reset translation failed:",e)}}_showTrendPage(t){const e={platform:this.platform,category:this.category,search:this.search,sortBy:this.sortBy,sortOrder:this.sortOrder,page:this.page,scrollY:window.scrollY};sessionStorage.setItem("product-master-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"product-master")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_showSourcingModal(t){window.ecomagentNavigateToSourcing(t)}async _open1688(t,e){if(t)try{const s=`${(await(await fetch(`/api/1688-search-url?keyword=${encodeURIComponent(t)}`)).json()).url}&ecom_code=${e}`;window.open(s,"_blank")}catch{const o=`https://s.1688.com/selloffer/offer_search.htm?keywords=${encodeURIComponent(t)}&ecom_code=${e}`;window.open(o,"_blank")}}_showImgPreview(t,e){this.previewImg={show:!0,src:e,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement()}_hideImgPreview(){this.previewImg={...this.previewImg,show:!1},this._updatePreviewElement()}_moveImgPreview(t){this.previewImg.show&&(this.previewImg={...this.previewImg,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement())}_updatePreviewElement(){let t=document.getElementById("global-img-preview");t||(t=document.createElement("img"),t.id="global-img-preview",t.style.cssText="position:fixed;z-index:9999;max-width:400px;max-height:400px;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.5);pointer-events:none;border:1px solid rgba(255,255,255,0.1);",document.body.appendChild(t)),this.previewImg.show?(t.src=this.previewImg.src,t.style.left=this.previewImg.x+"px",t.style.top=this.previewImg.y+"px",t.style.display="block"):t.style.display="none"}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return i`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=e.map(u=>u.value).filter(u=>u!=null);if(a.length<2)return i`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const o=Math.min(...a),n=Math.max(...a)-o||1,p=100,c=32,h=2,m=a.map((u,w)=>{const j=h+w/(a.length-1)*(p-h*2),mt=c-h-(u-o)/n*(c-h*2);return`${j},${mt}`}).join(" "),g=m+` ${h+(a.length-1)/(a.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return i`
      <div class="sparkline-container">
        <svg viewBox="0 0 ${p} ${c}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="grad-${t}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${g}" fill="url(#grad-${t})" />
          <polyline points="${m}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `}_renderSortHeader(t,e){const a=this.sortBy===e,o=a?this.sortOrder==="desc"?"▼":"▲":"⇅";return i`
      <th class="sortable ${a?"sorted":""}" @click=${()=>this._onSort(e)}>
        ${t} <span class="sort-icon">${o}</span>
      </th>
    `}_getCategoryOptions(){return this.platform==="amazon"?this.categories.amazon:this.platform==="tiktok"?this.categories.tiktok:[]}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),o=Math.min(this.pages,a+5-1);o-a<4&&(a=Math.max(1,o-5+1)),a>1&&(t.push(i`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),a>2&&t.push(i`<span style="color:var(--muted)">...</span>`));for(let s=a;s<=o;s++)t.push(i`
        <button class="page-btn ${s===this.page?"active":""}" @click=${()=>this._onPageChange(s)}>${s}</button>
      `);return o<this.pages&&(o<this.pages-1&&t.push(i`<span style="color:var(--muted)">...</span>`),t.push(i`<button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>`)),i`<div class="pagination">${t}</div>`}render(){if(this.loading)return i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=this._getCategoryOptions();return i`
      <!-- 平台切换 -->
      <div class="tabs">
        <button class="tab-btn ${this.platform==="amazon"?"active":""}" @click=${()=>this._onPlatformChange("amazon")}>Amazon</button>
        <button class="tab-btn ${this.platform==="tiktok"?"active":""}" @click=${()=>this._onPlatformChange("tiktok")}>TikTok</button>
      </div>

      <!-- 搜索过滤 -->
      <div class="toolbar">
        <div class="field-group">
          <label class="field-label">分类</label>
          <select class="select" @change=${this._onCategoryChange}>
            <option value="" ?selected=${!this.category}>全部分类</option>
            ${t.map(e=>i`<option value=${e} ?selected=${this.category===e}>${e}</option>`)}
          </select>
        </div>
        <div class="field-group">
          <label class="field-label">搜索</label>
          <input type="text" class="input search-input" placeholder="商品名称..." 
            .value=${this.search}
            @input=${e=>this._onInputChange(e,"search")}
            @keyup=${e=>e.key==="Enter"&&this._onSearch()}>
        </div>
        <button class="search-btn" @click=${this._onSearch}>🔍 搜索</button>
      </div>

      <!-- 商品列表 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width:50px">排名</th>
              <th style="width:64px">图片</th>
              <th style="width:20%">商品简称</th>
              <th>分类</th>
              ${this._renderSortHeader("价格","price")}
              ${this._renderSortHeader("评分","rating")}
              ${this._renderSortHeader("销量","sales_count")}
              ${this._renderSortHeader("总销售额","total_sales")}
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((e,a)=>i`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${(this.page-1)*20+a+1}</td>
                <td>
                  ${e.local_image_path||e.image_url?i`<img class="product-img" src=${e.local_image_path?`/images/${e.local_image_path}`:e.image_url||""} loading="lazy" 
                        @mouseenter=${o=>this._showImgPreview(o,e.local_image_path?`/images/${e.local_image_path}`:e.image_url||"")}
                        @mouseleave=${this._hideImgPreview}
                        @mousemove=${this._moveImgPreview} />`:i`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    <div class="product-name-row">
                      ${e.product_url?i`<a class="product-name product-link" href=${e.product_url} target="_blank" title=${e.name}>${e.short_name||e.name||"无名称"}</a>`:i`<span class="product-name" title=${e.name}>${e.short_name||e.name||"无名称"}</span>`}
                      ${e.translation_status==="translated"?i`<button class="retranslate-btn" @click=${()=>this._resetTranslation(e.ecom_code)} title="重新翻译">🔄</button>`:""}
                    </div>
                    <div class="product-code">
                      <button class="track-btn ${this.trackedIds.has(e.ecom_code)?"active":""}"
                        @click=${()=>this._toggleTrack(e.ecom_code)}
                        title=${this.trackedIds.has(e.ecom_code)?"取消追踪":"添加追踪"}
                      >${this.trackedIds.has(e.ecom_code)?"★":"☆"}</button>
                    </div>
                  </div>
                </td>
                <td title=${e.category}>${e.category||"-"}</td>
                <td>${e.price?`$${e.price.toFixed(2)}`:"-"}</td>
                <td>${e.rating?i`${e.rating.toFixed(1)} ⭐`:"-"}</td>
                <td><span class="sales-count">${this._formatSales(e.sales_count)}</span></td>
                <td>${e.total_sales?`$${this._formatSales(e.total_sales)}`:"-"}</td>
                <td class="sparkline-cell">${this._renderSparkline(e.ecom_code)}</td>
                <td>
                  <button class="action-btn" @click=${()=>this._showTrendPage(e.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${()=>this._showSourcingModal(e.ecom_code)} title="查看货源">货源</button>
                  <button class="action-btn" @click=${()=>window.open(e.product_url||"#","_blank")} title="查看详情">查看</button>
                  <button class="action-btn" @click=${()=>this._open1688(e.short_name||e.name,e.ecom_code)} title="1688搜索">1688</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pages>1?this._renderPagination():""}
      </div>
      
      <!-- 趋势模态框 -->
      ${this.showTrend?i`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${e=>e.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
      
      <!-- 图片预览浮框 -->
    `}};to(_,"styles",f`
    :host { display: block; }
    
    /* 模态框 */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      width: 90%; max-width: 900px; max-height: 90vh;
      overflow-y: auto; position: relative;
    }
    .modal-close {
      position: absolute; top: 12px; right: 12px;
      background: var(--bg-elevated); border: 1px solid var(--border);
      border-radius: var(--radius-sm); width: 28px; height: 28px;
      cursor: pointer; font-size: 16px; color: var(--muted);
      display: flex; align-items: center; justify-content: center; z-index: 10;
    }
    .modal-close:hover { color: var(--text); }
    
    /* 平台切换 */
    .tabs {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 4px;
      display: inline-flex;
      gap: 4px;
      margin-bottom: 16px;
    }
    .tab-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500;
      border: none; cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent; color: var(--muted);
    }
    .tab-btn.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    .tab-btn:hover:not(.active) { color: var(--text); }
    
    /* 统计卡片 */
    .stats-row {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }
    .stat-item {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .stat-value {
      font-size: 24px;
      font-weight: 700;
      color: var(--text-strong);
    }
    .stat-value.accent { color: var(--accent); }
    .stat-value.tiktok { color: #00f2ea; }
    .stat-value.ok { color: var(--ok); }
    .stat-label {
      font-size: 13px;
      color: var(--muted);
    }
    
    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 16px;
      margin-bottom: 24px;
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .field-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .field-label {
      font-size: 11px; font-weight: 600; color: var(--muted);
    }
    .input, .select {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px; background: var(--bg-elevated);
      color: var(--text); transition: var(--duration-fast) ease;
    }
    .input:focus, .select:focus {
      outline: none; border-color: var(--accent);
    }
    .input.search-input { width: 180px; }
    .select { width: 230px; }
    .search-btn {
      background: var(--accent); color: var(--accent-foreground);
      padding: 6px 16px; border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500; border: none;
      cursor: pointer; transition: var(--duration-fast) ease;
    }
    .search-btn:hover { background: var(--accent-hover); }
    
    /* 表格 */
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: var(--bg-accent); padding: 10px 12px;
      font-size: 11px; font-weight: 600; color: var(--muted);
      text-align: left; border-bottom: 1px solid var(--border);
      white-space: nowrap; user-select: none;
    }
    th.sortable { cursor: pointer; }
    th.sortable:hover { color: var(--text); }
    th .sort-icon { margin-left: 4px; font-size: 10px; opacity: 0.5; }
    th.sorted .sort-icon { opacity: 1; color: var(--accent); }
    td {
      padding: 10px 12px; font-size: 13px; color: var(--text);
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    /* 商品行 */
    .product-row td { padding: 12px; }
    .product-img {
      width: 56px; height: 56px;
      object-fit: cover; border-radius: 6px;
      flex-shrink: 0;
      background: var(--bg-elevated);
    }
    .product-img-placeholder {
      width: 56px; height: 56px;
      background: var(--bg-elevated); border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); font-size: 18px; flex-shrink: 0;
    }
    .product-info { min-width: 0; }
    .product-name-row {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .product-name {
      font-size: 13px; font-weight: 500; color: var(--text);
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      max-width: 200px;
    }
    .product-name:hover { color: var(--accent); }
    .product-code {
      font-size: 11px; color: var(--muted);
      margin-top: 2px;
    }
    
    .platform-badge {
      display: inline-block; padding: 2px 8px;
      border-radius: 4px; font-size: 11px; font-weight: 600;
    }
    .platform-amazon { background: var(--accent-subtle); color: var(--accent); }
    .platform-tiktok { background: rgba(0, 242, 234, 0.1); color: #00f2ea; }
    
    .product-link {
      color: var(--text); text-decoration: none;
    }
    .product-link:hover { text-decoration: underline; color: var(--accent); }
    
    .sales-count {
      font-weight: 600; font-variant-numeric: tabular-nums;
    }
    
    /* 迷你趋势图 */
    .sparkline-cell { width: 120px; }
    .sparkline-container {
      width: 100px; height: 32px; position: relative;
    }
    .sparkline-container svg {
      width: 100%; height: 100%;
    }
    
    /* 追踪按钮 */
    .track-btn {
      background: transparent; border: none;
      font-size: 14px; cursor: pointer;
      padding: 2px; line-height: 1;
      color: var(--muted); transition: color 0.15s;
    }
    .track-btn.active { color: #fbbf24; }
    .track-btn:hover { color: #fbbf24; }
    
    /* 重翻译按钮 */
    .retranslate-btn {
      background: transparent; border: none;
      font-size: 11px; cursor: pointer;
      padding: 2px 6px; line-height: 1;
      color: var(--muted); transition: color 0.15s;
      margin-left: 4px;
    }
    .retranslate-btn:hover { color: var(--accent); }
    
    /* 操作按钮 */
    .action-btn {
      padding: 4px 8px; border-radius: var(--radius-sm);
      font-size: 11px; cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated); color: var(--muted);
      margin-right: 4px;
    }
    .action-btn:hover {
      background: var(--bg-hover); color: var(--text);
    }
    
    /* 图片预览浮框 */
    .img-preview {
      position: fixed;
      z-index: 2000;
      max-width: 400px;
      max-height: 400px;
      border-radius: 8px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
      pointer-events: none;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 分页 */
    .pagination {
      display: flex; justify-content: center;
      gap: 8px; padding: 16px;
    }
    .page-btn {
      padding: 6px 12px; border: 1px solid var(--border);
      border-radius: 6px; background: var(--bg-elevated);
      color: var(--text); cursor: pointer; font-size: 13px;
    }
    .page-btn:hover { background: var(--bg-hover); }
    .page-btn.active {
      background: var(--accent); color: white;
      border-color: var(--accent);
    }
    
    .loading {
      text-align: center; padding: 48px; color: var(--muted);
    }
    .spinner {
      width: 32px; height: 32px;
      border: 2px solid var(--accent); border-top-color: transparent;
      border-radius: 50%; animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `);z([l()],_.prototype,"products",2);z([l()],_.prototype,"loading",2);z([l()],_.prototype,"page",2);z([l()],_.prototype,"pages",2);z([l()],_.prototype,"search",2);z([l()],_.prototype,"platform",2);z([l()],_.prototype,"category",2);z([l()],_.prototype,"categories",2);z([l()],_.prototype,"sortBy",2);z([l()],_.prototype,"sortOrder",2);z([l()],_.prototype,"trackedIds",2);z([l()],_.prototype,"showTrend",2);z([l()],_.prototype,"trendCode",2);z([l()],_.prototype,"sparklines",2);z([l()],_.prototype,"previewImg",2);_=z([x("ea-product-master")],_);var Ce=Object.defineProperty,eo=Object.getOwnPropertyDescriptor,ao=(r,t,e)=>t in r?Ce(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,nt=(r,t,e,a)=>{for(var o=a>1?void 0:a?eo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Ce(t,e,o),o},oo=(r,t,e)=>ao(r,t+"",e);let R=class extends b{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map)}connectedCallback(){super.connectedCallback(),this.loadTracked()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t))),this.loadData()}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadData(){if(this.loading=!0,this.trackedIds.size===0){this.products=[],this.loading=!1,this.requestUpdate();return}try{const t=await _a([...this.trackedIds]);this.products=t.products||[],this.loadSparklines(this.products)}catch(t){console.error("Load tracking error:",t),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async a=>{try{const o=await fe(a.ecom_code,7);this.sparklines.set(a.ecom_code,o.trend)}catch{this.sparklines.set(a.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_untrack(t){this.trackedIds.delete(t),this.saveTracked(),this.products=this.products.filter(e=>e.ecom_code!==t),this.requestUpdate()}_showTrendPage(t){const e={scrollY:window.scrollY};sessionStorage.setItem("tracking-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"tracking")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return i`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=e.map(u=>u.value).filter(u=>u!=null);if(a.length<2)return i`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const o=Math.min(...a),n=Math.max(...a)-o||1,p=100,c=32,h=2,m=a.map((u,w)=>{const j=h+w/(a.length-1)*(p-h*2),mt=c-h-(u-o)/n*(c-h*2);return`${j},${mt}`}).join(" "),g=m+` ${h+(a.length-1)/(a.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return i`
      <div class="sparkline-container">
        <svg viewBox="0 0 ${p} ${c}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="grad-track-${t}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${g}" fill="url(#grad-track-${t})" />
          <polyline points="${m}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `}render(){return this.loading?i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.products.length===0?i`
        <div class="empty-state">
          <div class="empty-icon">🎯</div>
          <p>暂无追踪商品</p>
          <p style="font-size: 12px; margin-top: 8px;">请在商品总库中点击 ☆ 按钮添加</p>
        </div>
      `:i`
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th style="width:50px">排名</th>
              <th style="width:64px">图片</th>
              <th style="width:20%">商品简称</th>
              <th>分类</th>
              <th>价格</th>
              <th>评分</th>
              <th>销量</th>
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((t,e)=>i`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${e+1}</td>
                <td>
                  ${t.local_image_path?i`<img class="product-img" src="/images/${t.local_image_path}" loading="lazy" />`:i`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    ${t.product_url?i`<a class="product-name product-link" href=${t.product_url} target="_blank" title=${t.name}>${t.short_name||t.name||"无名称"}</a>`:i`<span class="product-name" title=${t.name}>${t.short_name||t.name||"无名称"}</span>`}
                  </div>
                </td>
                <td title=${t.category}>${t.category||"-"}</td>
                <td>${t.price?`$${t.price.toFixed(2)}`:"-"}</td>
                <td>${t.rating?i`${t.rating.toFixed(1)} ⭐`:"-"}</td>
                <td><span class="sales-count">${this._formatSales(t.sales_count)}</span></td>
                <td class="sparkline-cell">${this._renderSparkline(t.ecom_code)}</td>
                <td>
                  <button class="action-btn" @click=${()=>this._showTrendPage(t.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${()=>window.open(t.product_url||"#","_blank")} title="查看详情">查看</button>
                  <button class="action-btn" style="color:var(--danger)" @click=${()=>this._untrack(t.ecom_code)} title="取消追踪">移除</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
      
      <!-- 趋势模态框 -->
      ${this.showTrend?i`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${t=>t.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
    `}};oo(R,"styles",f`
    :host { display: block; }
    
    /* 模态框 */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      width: 90%; max-width: 900px; max-height: 90vh;
      overflow-y: auto; position: relative;
    }
    .modal-close {
      position: absolute; top: 12px; right: 12px;
      background: var(--bg-elevated); border: 1px solid var(--border);
      border-radius: var(--radius-sm); width: 28px; height: 28px;
      cursor: pointer; font-size: 16px; color: var(--muted);
      display: flex; align-items: center; justify-content: center; z-index: 10;
    }
    .modal-close:hover { color: var(--text); }
    
    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 64px;
      color: var(--muted);
    }
    .empty-icon { font-size: 48px; margin-bottom: 16px; }
    
    /* 表格 */
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: var(--bg-accent); padding: 10px 12px;
      font-size: 11px; font-weight: 600; color: var(--muted);
      text-align: left; border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    td {
      padding: 10px 12px; font-size: 13px; color: var(--text);
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    /* 商品行 */
    .product-row td { padding: 12px; }
    .product-img {
      width: 56px; height: 56px;
      object-fit: cover; border-radius: 6px;
      flex-shrink: 0;
      background: var(--bg-elevated);
    }
    .product-img-placeholder {
      width: 56px; height: 56px;
      background: var(--bg-elevated); border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      color: var(--muted); font-size: 18px; flex-shrink: 0;
    }
    .product-info { min-width: 0; }
    .product-name {
      font-size: 13px; font-weight: 500; color: var(--text);
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      max-width: 200px; display: block;
    }
    .product-name:hover { color: var(--accent); }
    
    .platform-badge {
      display: inline-block; padding: 2px 8px;
      border-radius: 4px; font-size: 11px; font-weight: 600;
    }
    .platform-amazon { background: var(--accent-subtle); color: var(--accent); }
    .platform-tiktok { background: rgba(0, 242, 234, 0.1); color: #00f2ea; }
    
    .product-link {
      color: var(--text); text-decoration: none;
    }
    .product-link:hover { text-decoration: underline; color: var(--accent); }
    
    .sales-count {
      font-weight: 600; font-variant-numeric: tabular-nums;
    }
    
    /* 迷你趋势图 */
    .sparkline-cell { width: 120px; }
    .sparkline-container {
      width: 100px; height: 32px; position: relative;
    }
    .sparkline-container svg { width: 100%; height: 100%; }
    
    /* 追踪按钮 */
    .track-btn {
      background: transparent; border: none;
      font-size: 14px; cursor: pointer;
      padding: 2px; line-height: 1;
      color: #fbbf24; transition: color 0.15s;
    }
    .track-btn:hover { color: var(--muted); }
    
    /* 操作按钮 */
    .action-btn {
      padding: 4px 8px; border-radius: var(--radius-sm);
      font-size: 11px; cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated); color: var(--muted);
      margin-right: 4px;
    }
    .action-btn:hover {
      background: var(--bg-hover); color: var(--text);
    }
    
    .loading {
      text-align: center; padding: 48px; color: var(--muted);
    }
    .spinner {
      width: 32px; height: 32px;
      border: 2px solid var(--accent); border-top-color: transparent;
      border-radius: 50%; animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `);nt([l()],R.prototype,"products",2);nt([l()],R.prototype,"loading",2);nt([l()],R.prototype,"trackedIds",2);nt([l()],R.prototype,"showTrend",2);nt([l()],R.prototype,"trendCode",2);nt([l()],R.prototype,"sparklines",2);R=nt([x("ea-tracking")],R);var Te=Object.defineProperty,ro=Object.getOwnPropertyDescriptor,so=(r,t,e)=>t in r?Te(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,T=(r,t,e,a)=>{for(var o=a>1?void 0:a?ro(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Te(t,e,o),o},io=(r,t,e)=>so(r,t+"",e);let k=class extends b{constructor(){super(...arguments);d(this,"loading",!0);d(this,"saving",!1);d(this,"appName","");d(this,"country","马来西亚");d(this,"language","马来语");d(this,"proxyHost","127.0.0.1");d(this,"proxyPort",7890);d(this,"proxyEnabled",!0);d(this,"apiKeys",{google:"",volcano:"",xai:""});d(this,"openclawInstalled",!1);d(this,"openclawSettings",{amazon_fetch:{enabled:!0,schedule:"0 3 * * *",description:"每日凌晨 3:00 抓取 Amazon 数据"},translation_pipeline:{enabled:!0,interval_minutes:30,description:"每 30 分钟执行商品名称翻译"}});d(this,"editingField","");d(this,"editValue","")}async connectedCallback(){super.connectedCallback(),console.log("[Settings] connectedCallback called"),await this.loadConfig(),console.log("[Settings] loadConfig done, loading:",this.loading)}async loadConfig(){try{const t=await fetch("/api/config/settings");if(t.ok){const s=(await t.json()).data||{};this.appName=s.app_name||"",this.country=s.country||"马来西亚",this.language=s.language||"马来语";const n=s.proxy||{};this.proxyHost=n.host||"127.0.0.1",this.proxyPort=n.port||7890,this.proxyEnabled=n.enabled!==!1}const e=await fetch("/api/config/api_keys");if(e.ok){const s=(await e.json()).data||{};this.apiKeys={google:s.google||"",volcano:s.volcano||"",xai:s.xai||""}}const a=await fetch("/api/openclaw/settings");if(a.ok){const o=await a.json();o.data&&(this.openclawSettings=o.data)}try{const o=await fetch("/api/openclaw/check");if(o.ok){const s=await o.json();this.openclawInstalled=s.installed}}catch{}}catch(t){console.error("加载配置失败:",t)}this.loading=!1,this.requestUpdate()}_editField(t,e){this.editingField=t,this.editValue=e}_cancelEdit(){this.editingField="",this.editValue=""}async _saveField(t){this.saving=!0;try{t==="app_name"||t==="country"||t==="language"||t==="proxy_host"||t==="proxy_port"||t==="proxy_enabled"?(await fetch("/api/config/settings",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({app_name:this.appName,country:this.country,language:this.language,proxy:{host:this.proxyHost,port:this.proxyPort,enabled:this.proxyEnabled},[t]:this.editValue})})).ok&&(t==="app_name"&&(this.appName=this.editValue),t==="country"&&(this.country=this.editValue),t==="language"&&(this.language=this.editValue),t==="proxy_host"&&(this.proxyHost=this.editValue),t==="proxy_port"&&(this.proxyPort=parseInt(this.editValue)),t==="proxy_enabled"&&(this.proxyEnabled=this.editValue==="true")):(await fetch("/api/config/api_keys",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({...this.apiKeys,[t]:this.editValue})})).ok&&(this.apiKeys={...this.apiKeys,[t]:this.editValue})}catch(e){console.error("保存失败:",e),alert("保存失败")}this.saving=!1,this.editingField="",this.editValue=""}_maskKey(t){return!t||t.length<10?t||"未配置":t.substring(0,6)+"****"+t.substring(t.length-4)}async _toggleOpenclawTask(t){var a;const e=!((a=this.openclawSettings[t])!=null&&a.enabled);this.openclawSettings={...this.openclawSettings,[t]:{...this.openclawSettings[t],enabled:e}},this.requestUpdate();try{const o=await fetch("/api/openclaw/toggle",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({task_key:t,enabled:e})});if(o.ok){const s=await o.json();s.success?this._showToast(e?"已启用":"已禁用"):this._showToast(s.message||"操作失败","error")}}catch(o){console.error("操作失败:",o),this._showToast("操作失败","error")}}_showToast(t,e="success"){const a=document.createElement("div");a.style.cssText=`
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 12px 24px;
      background: ${e==="success"?"#10b981":"#ef4444"};
      color: white;
      border-radius: 8px;
      font-size: 14px;
      z-index: 9999;
      animation: fadeIn 0.3s ease;
    `,a.textContent=t,document.body.appendChild(a),setTimeout(()=>{a.style.animation="fadeOut 0.3s ease",setTimeout(()=>a.remove(),300)},2e3)}async _applyOpenclawSettings(){this._showToast("正在应用配置...","success");try{const t=await fetch("/api/openclaw/setup",{method:"POST"});if(t.ok){const e=await t.json();e.success?this._showToast(`配置已保存！请在终端运行以下命令应用定时任务:
python scripts/openclaw_config.py setup`,"success"):this._showToast(e.error||"配置失败","error")}}catch(t){console.error("应用配置失败:",t),this._showToast("应用配置失败","error")}}render(){var t,e,a,o;return console.log("[Settings] render, loading:",this.loading,"appName:",this.appName),this.loading?i`<div style="text-align:center;padding:40px;color:var(--muted)">加载中...</div>`:i`
      <h2>⚙️ 系统设置</h2>
      
      <!-- 基础设置 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">📱</span>
          <span class="section-title">基础设置</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">软件名称</span>
            <div class="field-value">
              ${this.editingField==="app_name"?i`
                    <input class="field-input" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} />
                    <button class="btn btn-primary" @click=${()=>this._saveField("app_name")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text">${this.appName||"未设置"}</span>
                    <button class="btn" @click=${()=>this._editField("app_name",this.appName)}>编辑</button>
                  `}
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">国家/地区</span>
            <div class="field-value">
              ${this.editingField==="country"?i`
                    <input class="field-input" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} placeholder="如：马来西亚、印尼、泰国..." />
                    <button class="btn btn-primary" @click=${()=>this._saveField("country")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text">${this.country||"未设置"}</span>
                    <button class="btn" @click=${()=>this._editField("country",this.country)}>编辑</button>
                  `}
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">语言</span>
            <div class="field-value">
              ${this.editingField==="language"?i`
                    <input class="field-input" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} placeholder="如：马来语、印尼语、泰语..." />
                    <button class="btn btn-primary" @click=${()=>this._saveField("language")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text">${this.language||"未设置"}</span>
                    <button class="btn" @click=${()=>this._editField("language",this.language)}>编辑</button>
                  `}
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 国家和语言配置用于生成素材时的文案语言选择
        </div>
      </div>
      
      <!-- 代理配置 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🌐</span>
          <span class="section-title">代理配置</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">启用代理</span>
            <div class="field-value">
              <label class="toggle-switch">
                <input
                  type="checkbox"
                  .checked=${this.proxyEnabled}
                  @change=${async()=>{this.proxyEnabled=!this.proxyEnabled,this.editValue=String(this.proxyEnabled),await this._saveField("proxy_enabled")}}
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          <div class="field-row">
            <span class="field-label">代理地址</span>
            <div class="field-value">
              ${this.editingField==="proxy_host"?i`
                    <input class="field-input" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} placeholder="127.0.0.1" />
                    <button class="btn btn-primary" @click=${()=>this._saveField("proxy_host")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text">${this.proxyHost}</span>
                    <button class="btn" @click=${()=>this._editField("proxy_host",this.proxyHost)}>编辑</button>
                  `}
            </div>
          </div>
          <div class="field-row">
            <span class="field-label">代理端口</span>
            <div class="field-value">
              ${this.editingField==="proxy_port"?i`
                    <input class="field-input" type="number" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} placeholder="7890" />
                    <button class="btn btn-primary" @click=${()=>this._saveField("proxy_port")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text">${this.proxyPort}</span>
                    <button class="btn" @click=${()=>this._editField("proxy_port",String(this.proxyPort))}>编辑</button>
                  `}
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 代理用于访问国外 API（Google、xAI 等），默认为 Clash 代理端口 7890
        </div>
      </div>
      
      <!-- API 密钥 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🔑</span>
          <span class="section-title">API 密钥</span>
        </div>
        <div class="section-body">
          <div class="field-row">
            <span class="field-label">Google API Key</span>
            <div class="field-value">
              ${this.editingField==="google"?i`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} />
                    <button class="btn btn-primary" @click=${()=>this._saveField("google")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.google)}</span>
                    <button class="btn" @click=${()=>this._editField("google",this.apiKeys.google)}>编辑</button>
                  `}
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">火山引擎 API Key</span>
            <div class="field-value">
              ${this.editingField==="volcano"?i`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} />
                    <button class="btn btn-primary" @click=${()=>this._saveField("volcano")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.volcano)}</span>
                    <button class="btn" @click=${()=>this._editField("volcano",this.apiKeys.volcano)}>编辑</button>
                  `}
            </div>
          </div>
          
          <div class="field-row">
            <span class="field-label">xAI API Key</span>
            <div class="field-value">
              ${this.editingField==="xai"?i`
                    <input class="field-input" type="password" .value=${this.editValue} @input=${s=>this.editValue=s.target.value} />
                    <button class="btn btn-primary" @click=${()=>this._saveField("xai")} ?disabled=${this.saving}>保存</button>
                    <button class="btn" @click=${this._cancelEdit}>取消</button>
                  `:i`
                    <span class="field-text api-key-masked">${this._maskKey(this.apiKeys.xai)}</span>
                    <button class="btn" @click=${()=>this._editField("xai",this.apiKeys.xai)}>编辑</button>
                  `}
            </div>
          </div>
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 API 密钥用于调用各类 AI 模型生成素材
        </div>
      </div>
      
      <!-- OpenClaw 辅助功能 -->
      <div class="section">
        <div class="section-header">
          <span class="section-icon">🔗</span>
          <span class="section-title">OpenClaw 辅助</span>
        </div>
        <div class="section-body">
          ${this.openclawInstalled?i`
                <!-- Amazon 每日抓取 -->
                <div class="field-row">
                  <div style="flex: 1;">
                    <span class="field-label">Amazon 每日抓取</span>
                    <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">
                      ${((t=this.openclawSettings.amazon_fetch)==null?void 0:t.description)||"每日凌晨 3:00 抓取 Amazon 数据"}
                    </div>
                  </div>
                  <div class="field-value">
                    <label class="toggle-switch">
                      <input 
                        type="checkbox" 
                        .checked=${((e=this.openclawSettings.amazon_fetch)==null?void 0:e.enabled)??!0}
                        @change=${()=>this._toggleOpenclawTask("amazon_fetch")}
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
                
                <!-- 商品翻译流水线 -->
                <div class="field-row">
                  <div style="flex: 1;">
                    <span class="field-label">商品名称翻译</span>
                    <div style="font-size: 12px; color: var(--muted); margin-top: 4px;">
                      ${((a=this.openclawSettings.translation_pipeline)==null?void 0:a.description)||"每 30 分钟执行商品名称翻译"}
                    </div>
                  </div>
                  <div class="field-value">
                    <label class="toggle-switch">
                      <input 
                        type="checkbox" 
                        .checked=${((o=this.openclawSettings.translation_pipeline)==null?void 0:o.enabled)??!0}
                        @change=${()=>this._toggleOpenclawTask("translation_pipeline")}
                      />
                      <span class="toggle-slider"></span>
                    </label>
                  </div>
                </div>
              `:i`
                <div style="text-align: center; padding: 20px; color: var(--muted);">
                  <p>⚠️ OpenClaw 未安装</p>
                  <p style="font-size: 12px; margin-top: 8px;">辅助功能需要 OpenClaw 支持</p>
                </div>
              `}
        </div>
        <div class="hint" style="padding: 0 20px 16px;">
          💡 辅助功能通过 OpenClaw 自动运行数据抓取和翻译
          ${this.openclawInstalled?i`<br /><span style="color: var(--primary); cursor: pointer;" @click=${this._applyOpenclawSettings}>[应用配置到 OpenClaw]</span>`:""}
        </div>
      </div>
    `}};io(k,"styles",f`
    :host { display: block; padding: 24px; max-width: 800px; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 24px;
    }
    
    .section {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      margin-bottom: 20px;
      overflow: hidden;
    }
    
    .section-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      background: var(--bg);
      border-bottom: 1px solid var(--border);
    }
    
    .section-icon {
      font-size: 20px;
    }
    
    .section-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--text);
    }
    
    .section-body {
      padding: 20px;
    }
    
    .field-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 0;
      border-bottom: 1px solid var(--border);
    }
    
    .field-row:last-child {
      border-bottom: none;
    }
    
    .field-label {
      font-size: 14px;
      color: var(--text);
    }
    
    .field-value {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .field-text {
      font-size: 14px;
      color: var(--muted);
      max-width: 300px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .field-input {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      min-width: 200px;
    }
    
    .field-input:focus {
      outline: none;
      border-color: var(--primary);
    }
    
    .btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
    }
    
    .btn:hover {
      background: var(--bg-hover);
    }
    
    .btn-primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }
    
    .btn-primary:hover {
      opacity: 0.9;
    }
    
    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    .api-key-masked {
      font-family: monospace;
      letter-spacing: 2px;
    }
    
    .hint {
      font-size: 12px;
      color: var(--muted);
      margin-top: 8px;
    }
    
    /* Toggle Switch 样式 */
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 48px;
      height: 26px;
    }
    
    .toggle-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    
    .toggle-slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      transition: .3s;
      border-radius: 26px;
      border: 2px solid #bbb;
    }
    
    .toggle-slider:before {
      position: absolute;
      content: "";
      height: 18px;
      width: 18px;
      left: 2px;
      bottom: 2px;
      background-color: white;
      transition: .3s;
      border-radius: 50%;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .toggle-switch input:checked + .toggle-slider {
      background-color: #10b981;
      border-color: #059669;
    }
    
    .toggle-switch input:checked + .toggle-slider:before {
      transform: translateX(22px);
    }
    
    /* Toast 动画 */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
      from { opacity: 1; transform: translateY(0); }
      to { opacity: 0; transform: translateY(10px); }
    }
  `);T([l()],k.prototype,"loading",2);T([l()],k.prototype,"saving",2);T([l()],k.prototype,"appName",2);T([l()],k.prototype,"country",2);T([l()],k.prototype,"language",2);T([l()],k.prototype,"proxyHost",2);T([l()],k.prototype,"proxyPort",2);T([l()],k.prototype,"proxyEnabled",2);T([l()],k.prototype,"apiKeys",2);T([l()],k.prototype,"openclawInstalled",2);T([l()],k.prototype,"openclawSettings",2);T([l()],k.prototype,"editingField",2);T([l()],k.prototype,"editValue",2);k=T([x("ea-settings")],k);var Ae=Object.defineProperty,no=Object.getOwnPropertyDescriptor,lo=(r,t,e)=>t in r?Ae(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,ut=(r,t,e,a)=>{for(var o=a>1?void 0:a?no(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Ae(t,e,o),o},co=(r,t,e)=>lo(r,t+"",e);let W=class extends b{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"amazonData",{});d(this,"tiktokData",{});d(this,"loading",!1);d(this,"pinnedCategories",new Set)}connectedCallback(){super.connectedCallback(),this._loadPinned(),this.loadData()}_loadPinned(){const t=localStorage.getItem("pinned-categories");t&&(this.pinnedCategories=new Set(JSON.parse(t)))}_savePinned(){localStorage.setItem("pinned-categories",JSON.stringify([...this.pinnedCategories]))}_togglePin(t){this.pinnedCategories.has(t)?this.pinnedCategories.delete(t):this.pinnedCategories.add(t),this._savePinned(),this.requestUpdate()}async loadData(){this.loading=!0;try{this.platform==="amazon"&&Object.keys(this.amazonData).length===0?this.amazonData=await Sa():this.platform==="tiktok"&&Object.keys(this.tiktokData).length===0&&(this.tiktokData=await Ca())}catch(t){console.error("Load top error:",t)}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.loadData()}_truncate(t,e=20){return t?t.length>e?t.substring(0,e)+"...":t:"-"}_renderRankChange(t,e){return e?i`<span class="new-badge">新</span>`:t==null?null:t>0?i`<span class="rank-change up">↑${t}</span>`:t<0?i`<span class="rank-change down">↓${Math.abs(t)}</span>`:null}_sortCategories(t){const e=t.filter(o=>this.pinnedCategories.has(o)),a=t.filter(o=>!this.pinnedCategories.has(o));return[...e,...a]}render(){const t=this.platform==="amazon"?this.amazonData:this.tiktokData,e=this._sortCategories(Object.keys(t));return i`
      <div class="tabs">
        <button class="tab-btn ${this.platform==="amazon"?"active":""}" @click=${()=>this._switchPlatform("amazon")}>Amazon</button>
        <button class="tab-btn ${this.platform==="tiktok"?"active":""}" @click=${()=>this._switchPlatform("tiktok")}>TikTok</button>
      </div>

      ${this.loading?i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:e.length===0?i`<div style="text-align:center;padding:48px;color:var(--muted)">暂无数据</div>`:i`
            <div class="categories-grid">
              ${e.map(a=>{const o=this.pinnedCategories.has(a);return i`
                  <div class="category-card ${o?"pinned":""}">
                    <div class="category-header">
                      <span>${a}</span>
                      <button 
                        class="pin-btn ${o?"pinned":""}" 
                        @click=${()=>this._togglePin(a)}
                        title=${o?"取消置顶":"置顶"}
                      >${o?"★":"☆"}</button>
                    </div>
                    <table>
                      <tbody>
                        ${(t[a]||[]).slice(0,15).map((s,n)=>i`
                          <tr style="cursor:pointer" @click=${()=>window.open(s.product_url||"#","_blank")}>
                            <td>
                              <div class="rank-cell">
                                <span class="rank">#${n+1}</span>
                                ${this._renderRankChange(s.rank_change,s.is_new)}
                              </div>
                            </td>
                            <td>
                              <a class="product-link" href=${s.product_url||"#"} target="_blank" title=${s.name}>
                                ${this._truncate(s.short_name||s.name)}
                              </a>
                            </td>
                            <td>${s.price?`$${s.price.toFixed(2)}`:"-"}</td>
                            <td>${s.rating?`${s.rating.toFixed(1)} ⭐`:"-"}</td>
                          </tr>
                        `)}
                      </tbody>
                    </table>
                  </div>
                `})}
            </div>
          `}
    `}};co(W,"styles",f`
    :host { display: block; }
    
    .tabs {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 4px;
      display: inline-flex;
      gap: 4px;
      margin-bottom: 24px;
    }
    
    .tab-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent;
      color: var(--muted);
    }
    
    .tab-btn.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    
    .categories-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
      gap: 16px;
    }
    
    .category-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    .category-card.pinned {
      border-color: var(--accent);
      box-shadow: 0 0 0 1px var(--accent);
    }
    
    .category-header {
      padding: 12px 16px;
      background: var(--bg-accent);
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .pin-btn {
      background: transparent;
      border: none;
      cursor: pointer;
      font-size: 16px;
      color: var(--muted);
      padding: 4px;
      transition: var(--duration-fast) ease;
    }
    
    .pin-btn:hover { color: var(--text); }
    .pin-btn.pinned { color: #fbbf24; }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    td {
      padding: 8px 12px;
      font-size: 12px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .rank-cell {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .rank {
      color: #00f2ea;
      font-weight: 600;
    }
    
    .rank-change {
      font-size: 10px;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 2px;
    }
    
    .rank-change.up { color: var(--ok); }
    .rank-change.down { color: var(--danger); }
    
    .new-badge {
      padding: 1px 4px;
      background: var(--ok);
      color: white;
      font-size: 9px;
      border-radius: 2px;
      font-weight: 500;
    }
    
    .product-link {
      color: var(--text-strong);
      text-decoration: none;
    }
    
    .product-link:hover { text-decoration: underline; }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
    
    @media (max-width: 768px) {
      .categories-grid { grid-template-columns: 1fr; }
    }
  `);ut([l()],W.prototype,"platform",2);ut([l()],W.prototype,"amazonData",2);ut([l()],W.prototype,"tiktokData",2);ut([l()],W.prototype,"loading",2);ut([l()],W.prototype,"pinnedCategories",2);W=ut([x("ea-today-top")],W);var Oe=Object.defineProperty,po=Object.getOwnPropertyDescriptor,ho=(r,t,e)=>t in r?Oe(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,Z=(r,t,e,a)=>{for(var o=a>1?void 0:a?po(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Oe(t,e,o),o},go=(r,t,e)=>ho(r,t+"",e);let F=class extends b{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"products",[]);d(this,"loading",!1);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"category","")}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){var t;this.loading=!0,console.log("=== RawData: Loading, platform:",this.platform);try{const e={page:this.page,limit:20,search:this.search,category:this.category},a=this.platform==="amazon"?await Ta(e):await Aa(e);console.log("=== RawData: Result:",a),this.products=a.data||[],this.pages=((t=a.pagination)==null?void 0:t.pages)||0}catch(e){console.error("=== RawData: Error:",e),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),o=Math.min(this.pages,a+5-1);o-a<4&&(a=Math.max(1,o-5+1));for(let s=a;s<=o;s++)t.push(i`
        <button class="page-btn ${s===this.page?"active":""}" @click=${()=>this._onPageChange(s)}>${s}</button>
      `);return i`<div class="pagination">${t}</div>`}render(){return i`
      <div class="tabs">
        <button class="tab-btn ${this.platform==="amazon"?"active":""}" @click=${()=>this._switchPlatform("amazon")}>Amazon</button>
        <button class="tab-btn ${this.platform==="tiktok"?"active":""}" @click=${()=>this._switchPlatform("tiktok")}>TikTok</button>
      </div>

      <div class="toolbar">
        <div class="toolbar-grid">
          <div>
            <label class="field-label">搜索关键词</label>
            <input type="text" class="input" placeholder="产品名称..." 
              .value=${this.search}
              @input=${t=>this.search=t.target.value}
              @keyup=${t=>t.key==="Enter"&&this._onSearch()}>
          </div>
          <div>
            <label class="field-label">分类</label>
            <input type="text" class="input" placeholder="分类..." 
              .value=${this.category}
              @input=${t=>this.category=t.target.value}
              @keyup=${t=>t.key==="Enter"&&this._onSearch()}>
          </div>
          <button class="search-btn" @click=${this._onSearch}>搜索</button>
        </div>
      </div>

      ${this.loading?i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:i`
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>产品简称</th>
                  <th>搜索关键词</th>
                  <th>${this.platform==="tiktok"?"TikTokShop ID":"分类"}</th>
                  ${this.platform==="tiktok"?i`<th>分类</th>`:""}
                  <th>价格</th>
                  <th>评分</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                ${this.products.map(t=>i`
                  <tr>
                    <td style="font-size:11px;color:var(--muted)">${t.id}</td>
                    <td class="truncate" title=${t.name}>${t.short_name||t.name||"-"}</td>
                    <td class="truncate" title=${t.search_keyword}>${t.search_keyword||"-"}</td>
                    ${this.platform==="tiktok"?i`<td style="font-size:11px;font-family:monospace">${t.tiktokshop_id||"-"}</td>`:""}
                    <td>${t.category||"-"}</td>
                    <td>${t.price?`$${t.price.toFixed(2)}`:"-"}</td>
                    <td>${t.rating?`${t.rating.toFixed(1)} ⭐`:"-"}</td>
                    <td>
                      <button class="action-btn" @click=${()=>window.open(t.product_url||"#","_blank")}>查看</button>
                    </td>
                  </tr>
                `)}
              </tbody>
            </table>
            ${this.pages>1?this._renderPagination():""}
          </div>
        `}
    `}};go(F,"styles",f`
    :host { display: block; }
    
    .tabs {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 4px;
      display: inline-flex;
      gap: 4px;
      margin-bottom: 24px;
    }
    
    .tab-btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent;
      color: var(--muted);
    }
    
    .tab-btn.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .toolbar-grid {
      display: grid;
      grid-template-columns: 1fr 1fr auto;
      gap: 12px;
      align-items: end;
    }
    
    .field-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      display: block;
      margin-bottom: 6px;
    }
    
    .input {
      width: 100%;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .input:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .search-btn {
      background: var(--accent);
      color: var(--accent-foreground);
      padding: 6px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
    }
    
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    th {
      background: var(--bg-accent);
      padding: 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    
    td {
      padding: 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .truncate {
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .action-btn {
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--muted);
    }
    
    .action-btn:hover {
      background: var(--bg-hover);
      color: var(--text);
    }
    
    .pagination {
      display: flex;
      justify-content: center;
      gap: 8px;
      padding: 16px;
    }
    
    .page-btn {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
      font-size: 13px;
    }
    
    .page-btn:hover { background: var(--bg-hover); }
    .page-btn.active {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
  `);Z([l()],F.prototype,"platform",2);Z([l()],F.prototype,"products",2);Z([l()],F.prototype,"loading",2);Z([l()],F.prototype,"page",2);Z([l()],F.prototype,"pages",2);Z([l()],F.prototype,"search",2);Z([l()],F.prototype,"category",2);F=Z([x("ea-raw-data")],F);var Me=Object.defineProperty,uo=Object.getOwnPropertyDescriptor,vo=(r,t,e)=>t in r?Me(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,It=(r,t,e,a)=>{for(var o=a>1?void 0:a?uo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Me(t,e,o),o},bo=(r,t,e)=>vo(r,t+"",e);let ht=class extends b{constructor(){super(...arguments);d(this,"stats",{amazon_hot_tiktok_not:0,tiktok_hot_amazon_not:0,both_hot:0});d(this,"items",[]);d(this,"loading",!1)}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=await Oa();this.stats=t.stats||this.stats,this.items=t.items||[]}catch(t){console.error("Load cross-platform error:",t)}finally{this.loading=!1}}render(){return i`
      <div class="header">
        <h2 style="font-size:20px;font-weight:700;color:var(--text-strong)">跨平台分析</h2>
        <button class="refresh-btn" @click=${this.loadData}>刷新分析</button>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">Amazon 火但 TikTok 未火</span>
            <span class="stat-icon">📈</span>
          </div>
          <div class="stat-value">${this.stats.amazon_hot_tiktok_not}</div>
          <div class="stat-desc">产品数量</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">TikTok 火但 Amazon 未火</span>
            <span class="stat-icon">📉</span>
          </div>
          <div class="stat-value">${this.stats.tiktok_hot_amazon_not}</div>
          <div class="stat-desc">产品数量</div>
        </div>
        
        <div class="stat-card">
          <div class="stat-header">
            <span class="stat-label">双平台都火</span>
            <span class="stat-icon">🔥</span>
          </div>
          <div class="stat-value">${this.stats.both_hot}</div>
          <div class="stat-desc">产品数量</div>
        </div>
      </div>

      ${this.loading?i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:i`
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>产品名称</th>
                  <th>Amazon 销量</th>
                  <th>TikTok 销量</th>
                  <th>差异分析</th>
                </tr>
              </thead>
              <tbody>
                ${this.items.length===0?i`<tr><td colspan="4" style="text-align:center;color:var(--muted)">暂无数据</td></tr>`:this.items.map(t=>i`
                    <tr>
                      <td>${t.name}</td>
                      <td>${t.amazon_sales??"-"}</td>
                      <td>${t.tiktok_sales??"-"}</td>
                      <td>${t.diff_analysis||"-"}</td>
                    </tr>
                  `)}
              </tbody>
            </table>
          </div>
        `}
    `}};bo(ht,"styles",f`
    :host { display: block; }
    
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }
    
    .refresh-btn {
      background: var(--accent);
      color: var(--accent-foreground);
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: none;
      cursor: pointer;
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
    }
    
    .stat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    
    .stat-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
    }
    
    .stat-icon {
      font-size: 24px;
    }
    
    .stat-value {
      font-size: 32px;
      font-weight: 700;
      color: var(--text-strong);
    }
    
    .stat-desc {
      font-size: 11px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    th {
      background: var(--bg-accent);
      padding: 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    
    td {
      padding: 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
    
    @media (max-width: 768px) {
      .stats-grid { grid-template-columns: 1fr; }
    }
  `);It([l()],ht.prototype,"stats",2);It([l()],ht.prototype,"items",2);It([l()],ht.prototype,"loading",2);ht=It([x("ea-cross-platform")],ht);var De=Object.defineProperty,mo=Object.getOwnPropertyDescriptor,fo=(r,t,e)=>t in r?De(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,Zt=(r,t,e,a)=>{for(var o=a>1?void 0:a?mo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&De(t,e,o),o},xo=(r,t,e)=>fo(r,t+"",e);let St=class extends b{constructor(){super(...arguments);d(this,"format","csv");d(this,"dateRange","all")}_export(t){console.log("Export:",{platform:t,format:this.format,dateRange:this.dateRange}),alert(`导出功能开发中...
平台: ${t}
格式: ${this.format}
时间范围: ${this.dateRange}`)}render(){return i`
      <h2 style="font-size:20px;font-weight:700;color:var(--text-strong);margin-bottom:24px">数据导出</h2>

      <div class="export-grid">
        <div class="export-card">
          <div class="export-header">
            <span class="export-icon">📊</span>
            <div>
              <div class="export-title">Amazon 数据</div>
              <div class="export-desc">导出 Amazon 所有产品数据</div>
            </div>
          </div>
          <div class="export-stats">
            <div class="stat-item">
              <div class="stat-value">327</div>
              <div class="stat-label">产品数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">1800</div>
              <div class="stat-label">销售记录</div>
            </div>
          </div>
          <button class="export-btn primary" @click=${()=>this._export("amazon")}>导出 Amazon 数据</button>
        </div>

        <div class="export-card">
          <div class="export-header">
            <span class="export-icon">🎵</span>
            <div>
              <div class="export-title">TikTok 数据</div>
              <div class="export-desc">导出 TikTok Shop 所有产品数据</div>
            </div>
          </div>
          <div class="export-stats">
            <div class="stat-item">
              <div class="stat-value">950</div>
              <div class="stat-label">产品数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">950</div>
              <div class="stat-label">销售记录</div>
            </div>
          </div>
          <button class="export-btn primary" @click=${()=>this._export("tiktok")}>导出 TikTok 数据</button>
        </div>
      </div>

      <div class="options-card">
        <div class="options-title">导出选项</div>
        
        <div class="option-row">
          <span class="option-label">导出格式</span>
          <select class="select" .value=${this.format} @change=${t=>this.format=t.target.value}>
            <option value="csv">CSV</option>
            <option value="excel">Excel</option>
          </select>
        </div>
        
        <div class="option-row">
          <span class="option-label">时间范围</span>
          <select class="select" .value=${this.dateRange} @change=${t=>this.dateRange=t.target.value}>
            <option value="all">全部</option>
            <option value="7d">近7天</option>
            <option value="30d">近30天</option>
          </select>
        </div>
      </div>

      <div style="margin-top:24px">
        <button class="export-btn" style="width:100%" @click=${()=>this._export("all")}>导出全部数据</button>
      </div>
    `}};xo(St,"styles",f`
    :host { display: block; }
    
    .export-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .export-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
    }
    
    .export-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    
    .export-icon {
      font-size: 24px;
    }
    
    .export-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .export-desc {
      font-size: 11px;
      color: var(--muted);
    }
    
    .export-stats {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
      padding: 12px;
      background: var(--bg-elevated);
      border-radius: var(--radius-sm);
    }
    
    .stat-item {
      text-align: center;
    }
    
    .stat-value {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .stat-label {
      font-size: 10px;
      color: var(--muted);
    }
    
    .export-btn {
      width: 100%;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      border: 1px solid var(--border);
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .export-btn:hover {
      background: var(--bg-hover);
      border-color: var(--accent);
    }
    
    .export-btn.primary {
      background: var(--accent);
      color: var(--accent-foreground);
      border-color: var(--accent);
    }
    
    .export-btn.primary:hover {
      background: var(--accent-hover);
    }
    
    .options-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
    }
    
    .options-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 16px;
    }
    
    .option-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid var(--border);
    }
    
    .option-row:last-child {
      border-bottom: none;
    }
    
    .option-label {
      font-size: 13px;
      color: var(--text);
    }
    
    .select {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    @media (max-width: 768px) {
      .export-grid { grid-template-columns: 1fr; }
    }
  `);Zt([l()],St.prototype,"format",2);Zt([l()],St.prototype,"dateRange",2);St=Zt([x("ea-export")],St);var Ee=Object.defineProperty,yo=Object.getOwnPropertyDescriptor,$o=(r,t,e)=>t in r?Ee(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,M=(r,t,e,a)=>{for(var o=a>1?void 0:a?yo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Ee(t,e,o),o},wo=(r,t,e)=>$o(r,t+"",e);let C=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"loading",!0);d(this,"product",{});d(this,"trend",[]);d(this,"details",[]);d(this,"pagination",{page:1,limit:20,total:0,pages:1});d(this,"timePreset","7");d(this,"customStart","");d(this,"customEnd","");d(this,"metric","");d(this,"currentPage",1);d(this,"tooltipData",{show:!1,x:0,y:0,date:"",value:null,index:0})}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=new URLSearchParams;this.timePreset==="custom"&&this.customStart&&this.customEnd?(t.set("start_date",this.customStart),t.set("end_date",this.customEnd)):t.set("days",this.timePreset),t.set("page",String(this.currentPage));const e=await fetch(`/api/product-trend/${this.ecomCode}?${t}`);if(!e.ok)throw new Error("Failed to load");const a=await e.json();this.product=a.product,this.trend=a.trend,this.details=a.details,this.pagination=a.pagination,this.metric||(this.product.platform==="amazon"?this.metric="rating":this.metric="sales_count")}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}_goBack(){const t=sessionStorage.getItem("trend-source-page")||"product-master";window.ecomagentNavigate(t);const e=sessionStorage.getItem("trend-source-state");e&&sessionStorage.setItem("restore-state",e)}_onTimePreset(t){this.timePreset=t,this.currentPage=1,this.loadData()}_onCustomDateChange(){this.customStart&&this.customEnd&&(this.timePreset="custom",this.currentPage=1,this.loadData())}_onMetricChange(t){this.metric=t,this.requestUpdate()}_onPageChange(t){this.currentPage=t,this.loadData()}_formatValue(t,e){if(t==null)return"-";if(e==="sales_count"){if(t>=1e4)return`${(t/1e3).toFixed(1)}K`;if(t>=1e3)return`${(t/1e3).toFixed(1)}K`}return e==="rating"?t.toFixed(1):e==="price"?`$${t.toFixed(2)}`:String(t)}_renderChart(){const t=this.trend;if(!t||t.length<1)return i`<div class="chart-empty">暂无数据</div>`;const e=t.map(v=>{const S=v[this.metric];return{...v,value:S??0,rawValue:S}}),a=800,o=320,s={top:20,right:40,bottom:50,left:70},n=a-s.left-s.right,p=o-s.top-s.bottom,c=e.map(v=>v.value),h=Math.min(...c),g=Math.max(...c)-h||1,u=v=>s.left+v/(t.length-1||1)*n,w=v=>s.top+p-(v-h)/g*p,j=e.map((v,S)=>`${u(S)},${w(v.value)}`).join(" L "),mt=`M ${j}`,He=`M ${s.left},${s.top+p} L ${j} L ${u(t.length-1)},${s.top+p} Z`,Ut=[],te=5;for(let v=0;v<=te;v++)Ut.push(h+g*v/te);const Ge=Math.ceil(t.length/7);let B="";return B+=`<defs>
      <linearGradient id="areaGradient" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ff5c5c" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#ff5c5c" stop-opacity="0.05" />
      </linearGradient>
    </defs>`,Ut.forEach(v=>{B+=`<line x1="${s.left}" y1="${w(v)}" x2="${a-s.right}" y2="${w(v)}" stroke="#444" stroke-width="1" stroke-dasharray="4,4"/>`}),B+=`<path d="${He}" fill="url(#areaGradient)"/>`,B+=`<path d="${mt}" fill="none" stroke="#ff5c5c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>`,e.forEach((v,S)=>{B+=`<circle cx="${u(S)}" cy="${w(v.value)}" r="4" fill="#ff5c5c" stroke="#1a1a1a" stroke-width="1"/>`}),Ut.forEach(v=>{const S=this._formatValue(v,this.metric);B+=`<text x="${s.left-10}" y="${w(v)+4}" text-anchor="end" fill="#aaa" font-size="11" font-family="system-ui, -apple-system, sans-serif" font-weight="500">${S}</text>`}),e.forEach((v,S)=>{if(S%Ge!==0&&S!==t.length-1)return;const Nt=v.date.slice(5);B+=`<text x="${u(S)}" y="${o-20}" text-anchor="middle" fill="#aaa" font-size="11" font-family="system-ui, -apple-system, sans-serif" font-weight="500">${Nt}</text>`}),i`
      <svg class="chart-svg" viewBox="0 0 ${a} ${o}" preserveAspectRatio="xMidYMid meet"
        @mousemove=${v=>{const S=v.currentTarget.getBoundingClientRect(),Nt=v.clientX-S.left,Be=S.width/a,Ke=Nt/Be-s.left,ft=Math.round(Ke/n*(t.length-1));if(ft>=0&&ft<t.length){const Ft=e[ft];this.tooltipData={show:!0,x:u(ft),y:w(Ft.value),date:Ft.date,value:Ft.rawValue,index:ft},this.requestUpdate()}}} @mouseleave=${()=>{this.tooltipData={...this.tooltipData,show:!1},this.requestUpdate()}}>
        ${Bt(B)}
        ${this.tooltipData.show?Bt(`<line class="tooltip-line" x1="${this.tooltipData.x}" y1="0" x2="${this.tooltipData.x}" y2="${o}" stroke="#ff5c5c" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/><circle class="tooltip-point" cx="${this.tooltipData.x}" cy="${this.tooltipData.y}" r="8" fill="#ff5c5c" stroke="#fff" stroke-width="3"/>`):null}
      </svg>
      
      <!-- Tooltip 浮框 -->
      ${this.tooltipData.show?i`
        <div class="tooltip" style="left:${this.tooltipData.x/800*100}%;top:${this.tooltipData.y/320*100}%;transform:translate(-50%,-130%)">
          <div class="tooltip-date">${this.tooltipData.date}</div>
          <div class="tooltip-value">
            <span class="tooltip-label">${this._getMetricLabel()}:</span>
            <span>${this._formatValue(this.tooltipData.value,this.metric)}</span>
          </div>
        </div>
      `:""}
    `}_getMetricLabel(){switch(this.metric){case"sales_count":return"销量";case"rank":return"排名";case"rating":return"评分";case"price":return"价格";default:return""}}_getMetricHint(){switch(this.metric){case"sales_count":return"显示商品每日销量变化趋势";case"rank":return"显示商品排名变化趋势";case"rating":return"显示商品评分变化趋势";case"price":return"显示商品价格变化趋势";default:return""}}_renderPagination(){const t=[];let a=Math.max(1,this.pagination.page-Math.floor(2.5)),o=Math.min(this.pagination.pages,a+5-1);o-a<4&&(a=Math.max(1,o-5+1)),a>1&&(t.push(i`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),a>2&&t.push(i`<span style="color:var(--muted)">...</span>`));for(let s=a;s<=o;s++)t.push(i`
        <button class="page-btn ${s===this.pagination.page?"active":""}" @click=${()=>this._onPageChange(s)}>${s}</button>
      `);return o<this.pagination.pages&&(o<this.pagination.pages-1&&t.push(i`<span style="color:var(--muted)">...</span>`),t.push(i`<button class="page-btn" @click=${()=>this._onPageChange(this.pagination.pages)}>${this.pagination.pages}</button>`)),i`<div class="pagination">${t}</div>`}render(){if(this.loading)return i`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=this.product.platform==="amazon"?[{key:"rank",label:"排名"},{key:"rating",label:"评分"},{key:"price",label:"价格"}]:[{key:"sales_count",label:"销量"},{key:"rating",label:"评分"},{key:"price",label:"价格"}],e=[{key:"7",label:"近7天"},{key:"15",label:"近15天"},{key:"30",label:"近1月"},{key:"90",label:"近3月"}];return i`
      <!-- 头部 -->
      <div class="header">
        <button class="back-btn" @click=${this._goBack}>
          <span>←</span>
          <span>返回</span>
        </button>
        <div>
          <span class="product-title">${this.product.short_name||this.product.name||"商品趋势"}</span>
        </div>
      </div>

      <!-- 时间选择 -->
      <div class="time-selector">
        <span class="time-label">时间范围：</span>
        <div class="time-tabs">
          ${e.map(a=>i`
            <button class="time-tab ${this.timePreset===a.key?"active":""}" @click=${()=>this._onTimePreset(a.key)}>${a.label}</button>
          `)}
        </div>
        <div class="date-inputs">
          <input type="date" class="date-input" .value=${this.customStart} @input=${a=>{this.customStart=a.target.value}} @change=${this._onCustomDateChange}>
          <span style="color:var(--muted)">至</span>
          <input type="date" class="date-input" .value=${this.customEnd} @input=${a=>{this.customEnd=a.target.value}} @change=${this._onCustomDateChange}>
          <button class="apply-btn" @click=${this._onCustomDateChange}>应用</button>
        </div>
      </div>

      <!-- 图表 -->
      <div class="chart-section">
        <div class="chart-header">
          <span class="chart-title">趋势图表</span>
          <div style="display:flex;align-items:center">
            <div class="metric-tabs">
              ${t.map(a=>i`
                <button class="metric-tab ${this.metric===a.key?"active":""}" @click=${()=>this._onMetricChange(a.key)}>${a.label}</button>
              `)}
            </div>
            <span class="metric-hint">${this._getMetricHint()}</span>
          </div>
        </div>
        <div class="chart-container">
          ${this._renderChart()}
        </div>
      </div>

      <!-- 详细表格 -->
      <div class="table-section">
        <div class="table-header">每日数据详情</div>
        <table>
          <thead>
            <tr>
              <th>日期</th>
              <th>简称</th>
              <th>关键词</th>
              <th>评分</th>
              <th>价格</th>
              <th>销量</th>
              <th>事件</th>
            </tr>
          </thead>
          <tbody>
            ${this.details.map(a=>i`
              <tr>
                <td>${a.date}</td>
                <td style="max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${a.short_name||""}>${a.short_name||"-"}</td>
                <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${a.search_keyword||""}>${a.search_keyword||"-"}</td>
                <td>${a.rating!=null?a.rating.toFixed(1):"-"}</td>
                <td>${a.price!=null?`$${a.price.toFixed(2)}`:"-"}</td>
                <td>${a.sales_count!=null?this._formatValue(a.sales_count,"sales_count"):"-"}</td>
                <td>${a.events?a.events.split(", ").map(o=>i`<span class="event-tag">${o}</span>`):"-"}</td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pagination.pages>1?this._renderPagination():""}
      </div>
    `}};wo(C,"styles",f`
    :host { display: block; }
    
    /* 头部 */
    .header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 24px;
    }
    .back-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 8px 16px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      color: var(--text);
      font-size: 13px;
      cursor: pointer;
      transition: var(--duration-fast) ease;
    }
    .back-btn:hover {
      background: var(--bg-hover);
      border-color: var(--accent);
    }
    .product-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-strong);
    }
    .product-code {
      font-size: 12px;
      color: var(--muted);
      margin-left: 8px;
    }
    
    /* 时间选择 */
    .time-selector {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }
    .time-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    .time-tabs {
      display: flex;
      gap: 4px;
      background: var(--bg-elevated);
      padding: 4px;
      border-radius: var(--radius-sm);
    }
    .time-tab {
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      background: transparent;
      color: var(--muted);
    }
    .time-tab.active {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    .time-tab:hover:not(.active) {
      color: var(--text);
    }
    .date-inputs {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .date-input {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    .date-input:focus {
      outline: none;
      border-color: var(--accent);
    }
    .apply-btn {
      padding: 6px 12px;
      background: var(--accent);
      color: var(--accent-foreground);
      border: none;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
    }
    .apply-btn:hover {
      background: var(--accent-hover);
    }
    
    /* 图表区域 */
    .chart-section {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 20px;
      margin-bottom: 24px;
    }
    .chart-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }
    .chart-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
    }
    .metric-tabs {
      display: flex;
      gap: 4px;
      background: var(--bg-elevated);
      padding: 4px;
      border-radius: var(--radius-sm);
    }
    .metric-tab {
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
      border: none;
      cursor: pointer;
      transition: all 0.3s ease;
      background: transparent;
      color: var(--muted);
    }
    .metric-tab.active {
      background: var(--accent);
      color: var(--accent-foreground);
      transform: scale(1.02);
    }
    .metric-tab:hover:not(.active) {
      color: var(--text);
      background: var(--bg-hover);
    }
    .metric-hint {
      font-size: 11px;
      color: var(--muted);
      margin-left: 8px;
    }
    
    .chart-container {
      width: 100%;
      aspect-ratio: 800 / 320;
      position: relative;
      background: var(--bg-elevated);
      border-radius: var(--radius-sm);
    }
    .chart-svg {
      width: 100%;
      height: 100%;
      display: block;
    }
    
    /* Tooltip 浮框 */
    .tooltip {
      position: absolute;
      background: rgba(26, 26, 30, 0.95);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 92, 92, 0.2);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
      pointer-events: none;
      white-space: nowrap;
      z-index: 100;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .tooltip-date {
      color: #888;
      font-size: 11px;
      margin-bottom: 4px;
    }
    .tooltip-value {
      color: #fff;
      font-weight: 500;
      font-size: 13px;
    }
    .tooltip-label {
      color: #ff5c5c;
      font-size: 11px;
      margin-right: 4px;
    }
    
    /* Tooltip 点动效 */
    .tooltip-point {
      transition: r 0.15s ease, stroke-width 0.15s ease;
    }
    .chart-empty {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: var(--muted);
      font-size: 14px;
    }
    
    /* 详细表格 */
    .table-section {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    .table-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
    }
    table { width: 100%; border-collapse: collapse; }
    th {
      background: var(--bg-accent);
      padding: 10px 12px;
      font-size: 11px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    td {
      padding: 10px 12px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    .event-tag {
      display: inline-block;
      padding: 2px 6px;
      background: var(--accent-subtle);
      color: var(--accent);
      border-radius: 4px;
      font-size: 11px;
      margin-right: 4px;
    }
    
    /* 分页 */
    .pagination {
      display: flex;
      justify-content: center;
      gap: 8px;
      padding: 16px;
    }
    .page-btn {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
      font-size: 13px;
    }
    .page-btn:hover { background: var(--bg-hover); }
    .page-btn.active {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
  `);M([$({type:String})],C.prototype,"ecomCode",2);M([l()],C.prototype,"loading",2);M([l()],C.prototype,"product",2);M([l()],C.prototype,"trend",2);M([l()],C.prototype,"details",2);M([l()],C.prototype,"pagination",2);M([l()],C.prototype,"timePreset",2);M([l()],C.prototype,"customStart",2);M([l()],C.prototype,"customEnd",2);M([l()],C.prototype,"metric",2);M([l()],C.prototype,"currentPage",2);M([l()],C.prototype,"tooltipData",2);C=M([x("ea-product-trend-page")],C);var Ie=Object.defineProperty,_o=Object.getOwnPropertyDescriptor,ko=(r,t,e)=>t in r?Ie(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,N=(r,t,e,a)=>{for(var o=a>1?void 0:a?_o(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Ie(t,e,o),o},Po=(r,t,e)=>ko(r,t+"",e);let O=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"sourcingList",[]);d(this,"loading",!0);d(this,"search","");d(this,"page",1);d(this,"pages",0);d(this,"total",0);d(this,"stats",{total:0,products_linked:0,today_count:0,last_updated:null});d(this,"showAssetManager",!1);d(this,"assetManagerItem",null)}connectedCallback(){super.connectedCallback(),this.loadStats(),this.loadSourcing()}async loadStats(){try{const t=await fetch("/api/sourcing/stats");this.stats=await t.json(),console.log("[Sourcing] stats:",this.stats)}catch(t){console.error("加载统计失败:",t)}}async loadSourcing(){var t,e;try{const a=new URLSearchParams;a.set("page",String(this.page)),a.set("limit","20"),this.search&&a.set("search",this.search),this.ecomCode&&a.set("ecom_code",this.ecomCode),console.log("[Sourcing] 请求:",`/api/sourcing/list?${a}`);const s=await(await fetch(`/api/sourcing/list?${a}`)).json();console.log("[Sourcing] 响应:",s),this.sourcingList=s.data||[],this.total=((t=s.pagination)==null?void 0:t.total)||0,this.pages=((e=s.pagination)==null?void 0:e.pages)||0,this.loading=!1,console.log("[Sourcing] loading 设为 false, 触发 requestUpdate"),this.requestUpdate()}catch(a){console.error("加载货源失败:",a),this.sourcingList=[],this.loading=!1,this.requestUpdate()}}_onSearch(t){t.key==="Enter"&&(this.page=1,this.loadSourcing())}_onPageChange(t){this.page=t,this.loadSourcing(),window.scrollTo({top:0,behavior:"smooth"})}_formatPrice(t){return t?`¥${t.toFixed(2)}`:"-"}_formatDate(t){if(!t)return"-";const e=new Date(t);return`${e.getMonth()+1}/${e.getDate()} ${e.getHours()}:${String(e.getMinutes()).padStart(2,"0")}`}async _deleteSourcing(t,e){if(confirm("确定删除此货源记录?"))try{await fetch(`/api/sourcing/${t}/${e}`,{method:"DELETE"}),await Promise.all([this.loadStats(),this.loadSourcing()])}catch(a){console.error("删除失败:",a)}}_openProduct(t){t&&window.open(t,"_blank")}_showAssetManager(t){console.log("[Sourcing] _showAssetManager called:",t),this.assetManagerItem=t,this.showAssetManager=!0,this.requestUpdate()}_closeAssetManager(){this.showAssetManager=!1,this.assetManagerItem=null,this.requestUpdate()}async _uploadToTikTok(t){console.log("[Sourcing] _uploadToTikTok called, item:",t);try{console.log("[Sourcing] Checking TikTok connection...");const a=await(await fetch("/api/tiktok/status")).json();if(console.log("[Sourcing] TikTok status:",a),!a.connected){console.log("[Sourcing] Chrome not running, starting...");const o=await fetch("/api/tiktok/ensure-chrome",{method:"POST"}),s=await o.json();if(console.log("[Sourcing] Ensure Chrome result:",s),!o.ok){alert("Failed to start Chrome. Please start manually.");return}if(await new Promise(p=>setTimeout(p,2e3)),(await fetch("/api/tiktok/open-login",{method:"POST"})).ok){alert(`Chrome started!
Please login to TikTok Shop, then click TikTok button again.`);return}}}catch(e){console.error("[Sourcing] Status check failed:",e),alert("Server connection failed");return}console.log("[Sourcing] 开始上传到 TikTok:",t.ecom_code);try{const a=await(await fetch(`/api/tiktok/upload/${t.ecom_code}`,{method:"POST"})).json();console.log("[Sourcing] 上传结果:",a),a.success?alert(`上传成功!
请在 TikTok Shop 后台检查草稿商品`):alert(`上传失败: ${a.message}`)}catch(e){console.error("[Sourcing] 上传失败:",e),alert("上传失败,请检查服务器连接")}}_renderModal(){return null}_renderAssetManager(){var t;return this.showAssetManager?i`
      <div class="modal-overlay" @click=${e=>{e.target===e.currentTarget&&this._closeAssetManager()}}>
        <div class="modal-content" style="max-width: 500px;">
          <asset-generator
            .ecomCode=${(t=this.assetManagerItem)==null?void 0:t.ecom_code}
            .item=${this.assetManagerItem}
            @close=${this._closeAssetManager}
          ></asset-generator>
        </div>
      </div>
    `:null}_renderPagination(){if(this.pages<=1)return null;const t=[],e=5;let a=Math.max(1,this.page-Math.floor(e/2)),o=Math.min(this.pages,a+e-1);o-a<e-1&&(a=Math.max(1,o-e+1)),t.push(i`
      <button class="page-btn" ?disabled=${this.page===1} @click=${()=>this._onPageChange(this.page-1)}>
        ‹
      </button>
    `);for(let s=a;s<=o;s++)t.push(i`
        <button class="page-btn ${s===this.page?"active":""}" @click=${()=>this._onPageChange(s)}>
          ${s}
        </button>
      `);return t.push(i`
      <button class="page-btn" ?disabled=${this.page===this.pages} @click=${()=>this._onPageChange(this.page+1)}>
        ›
      </button>
    `),i`
      <div class="pagination">
        <span class="page-info">共 ${this.total} 条</span>
        ${t}
      </div>
    `}render(){return console.log("[Sourcing] render called, loading=",this.loading,"list=",this.sourcingList.length),this.loading?i`<div class="loading-state">加载中...</div>`:i`
      <!-- 统计卡片 -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-value">${this.stats.total}</div>
          <div class="stat-label">货源总数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this.stats.products_linked}</div>
          <div class="stat-label">关联商品数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this.stats.today_count}</div>
          <div class="stat-label">今日采集</div>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="toolbar">
        <div class="field-group">
          <label class="field-label">搜索</label>
          <input type="text" class="search-input" placeholder="商品名称、店铺、offer ID..."
            .value=${this.search}
            @keydown=${this._onSearch}
            @change=${t=>this.search=t.target.value}
          >
        </div>
        <button class="search-btn" @click=${()=>{this.page=1,this.loadSourcing()}}>🔍 搜索</button>
        ${this.ecomCode?i`
          <div class="field-group">
            <label class="field-label">筛选</label>
            <div class="filter-tag">
              <span>${this.ecomCode}</span>
              <button class="filter-clear" @click=${()=>{this.ecomCode="",this.page=1,this.loadSourcing()}}>✕</button>
            </div>
          </div>
        `:""}
      </div>

      <!-- 货源列表 -->
      ${this.sourcingList.length===0?i`
        <div class="empty-state">
          <div class="empty-icon">📦</div>
          <div class="empty-title">暂无货源记录</div>
          <div class="empty-desc">点击商品库的「1688」按钮开始采集货源</div>
        </div>
      `:i`
        <div class="sourcing-table">
          <table>
            <thead>
              <tr>
                <th>商品</th>
                <th>价格</th>
                <th>起订量</th>
                <th>关联商品</th>
                <th>采集时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              ${this.sourcingList.map(t=>i`
                <tr>
                  <td>
                    <div class="product-cell">
                      <img
                        class="product-thumb"
                        src=${t.local_image_path?`/images/${t.local_image_path}`:t.image_url||'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50"><rect fill="%23ddd" width="50" height="50"/></svg>'}
                        onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2250%22 height=%2250%22><rect fill=%22%23ddd%22 width=%2250%22 height=%2250%22/></svg>'"
                      >
                      <div class="product-info">
                        <div class="product-title">${t.title||"无标题"}</div>
                        <div class="product-shop">${t.shop_name||"未知店铺"} · ${t.offer_id}</div>
                      </div>
                    </div>
                  </td>
                  <td class="price-cell">${this._formatPrice(t.price)}</td>
                  <td>${t.min_order||1}</td>
                  <td class="ecom-code-cell">${t.ecom_code}</td>
                  <td>${this._formatDate(t.collected_at)}</td>
                  <td>
                    <button class="action-btn action-btn-tiktok" @click=${()=>{console.log("[Sourcing] TikTok button clicked!"),this._uploadToTikTok(t)}}>
                      TK建品
                    </button>
                    <button class="action-btn action-btn-asset" @click=${()=>this._showAssetManager(t)}>
                      生成
                    </button>
                    <button class="action-btn action-btn-view" @click=${()=>this._openProduct(t.product_url)}>
                      素材
                    </button>
                    <button class="action-btn action-btn-delete" @click=${()=>this._deleteSourcing(t.ecom_code,t.offer_id)}>
                      删除
                    </button>
                  </td>
                </tr>
              `)}
            </tbody>
          </table>
        </div>

        ${this._renderPagination()}
      `}

      ${this._renderModal()}

      ${this._renderAssetManager()}
    `}};Po(O,"styles",f`
    :host {
      display: block;
    }

    /* 弹窗样式 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      animation: fadeIn 0.2s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    .modal-content {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 32px;
      max-width: 400px;
      width: 90%;
      text-align: center;
      animation: slideIn 0.3s ease;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }

    @keyframes slideIn {
      from { transform: translateY(-20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    .modal-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }

    .modal-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 8px;
    }

    .modal-desc {
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 24px;
      line-height: 1.6;
    }

    .modal-product {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .modal-product-thumb {
      width: 40px;
      height: 40px;
      object-fit: cover;
      border-radius: var(--radius-sm);
    }

    .modal-product-title {
      font-size: 13px;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .modal-buttons {
      display: flex;
      gap: 12px;
      justify-content: center;
    }

    .modal-btn {
      padding: 12px 24px;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .modal-btn-confirm {
      background: var(--primary);
      color: white;
      border: none;
    }

    .modal-btn-confirm:hover {
      opacity: 0.9;
      transform: translateY(-1px);
    }

    .modal-btn-cancel {
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
    }

    .modal-btn-cancel:hover {
      background: var(--bg-elevated);
    }

    /* 头部统计 */
    .stats-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 13px;
      color: var(--muted);
    }

    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 16px;
      margin-bottom: 24px;
      display: flex;
      gap: 12px;
      align-items: flex-end;
    }

    .field-group {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .field-label {
      font-size: 11px; font-weight: 600; color: var(--muted);
    }

    .search-input {
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px; background: var(--bg-elevated);
      color: var(--text); transition: var(--duration-fast) ease;
      width: 240px;
    }

    .search-input:focus {
      outline: none; border-color: var(--accent);
    }

    .search-btn {
      padding: 6px 16px; border-radius: var(--radius-sm);
      font-size: 13px; font-weight: 500; border: none;
      cursor: pointer; transition: var(--duration-fast) ease;
      background: var(--accent); color: var(--accent-foreground);
    }

    .search-btn:hover { background: var(--accent-hover); }

    /* 筛选标签 */
    .filter-tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      background: var(--accent);
      color: white;
      border-radius: var(--radius-sm);
      font-size: 13px;
    }

    .filter-clear {
      background: transparent;
      border: none;
      color: white;
      cursor: pointer;
      padding: 0;
      font-size: 14px;
      line-height: 1;
      opacity: 0.8;
    }

    .filter-clear:hover {
      opacity: 1;
    }

    /* 货源列表 */
    .sourcing-table {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
    }

    .sourcing-table table {
      width: 100%;
      border-collapse: collapse;
    }

    .sourcing-table th {
      text-align: left;
      padding: 12px 16px;
      background: var(--bg-elevated);
      font-weight: 500;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 1px solid var(--border);
    }

    .sourcing-table td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      font-size: 13px;
    }

    .sourcing-table tr:last-child td {
      border-bottom: none;
    }

    .sourcing-table tr:hover td {
      background: var(--bg);
    }

    .product-cell {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 300px;
    }

    .product-thumb {
      width: 50px;
      height: 50px;
      object-fit: cover;
      border-radius: var(--radius-sm);
      background: var(--bg-elevated);
      flex-shrink: 0;
    }

    .product-info {
      flex: 1;
      min-width: 0;
    }

    .product-title {
      font-size: 13px;
      color: var(--text);
      line-height: 1.4;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

    .product-shop {
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }

    .price-cell {
      color: #f5222d;
      font-weight: 600;
    }

    .ecom-code-cell {
      font-family: monospace;
      font-size: 12px;
      color: var(--primary);
    }

    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
      margin-right: 8px;
    }

    .action-btn-view {
      background: var(--primary);
      color: white;
      border: none;
    }

    .action-btn-view:hover {
      opacity: 0.9;
    }

    .action-btn-video, .action-btn-detail {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }

    .action-btn-video:hover, .action-btn-detail:hover {
      background: var(--bg);
      border-color: var(--primary);
    }

    .action-btn-asset {
      background: #722ed1;
      color: white;
      border: none;
    }

    .action-btn-asset:hover {
      opacity: 0.9;
    }

    .action-btn-tiktok {
      background: #ff0050;
      color: white;
      border: none;
    }

    .action-btn-tiktok:hover {
      opacity: 0.9;
    }

    .action-btn-delete {
      background: transparent;
      color: #f5222d;
      border: 1px solid #f5222d;
    }

    .action-btn-delete:hover {
      background: #fff1f0;
    }

    /* 分页 */
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 24px;
    }

    .page-btn {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--card);
      color: var(--text);
      font-size: 13px;
      cursor: pointer;
    }

    .page-btn:hover:not(:disabled) {
      border-color: var(--primary);
    }

    .page-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .page-btn.active {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }

    .page-info {
      font-size: 13px;
      color: var(--muted);
    }

    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--muted);
    }

    .empty-icon {
      font-size: 64px;
      margin-bottom: 16px;
    }

    .empty-title {
      font-size: 18px;
      color: var(--text);
      margin-bottom: 8px;
    }

    .empty-desc {
      font-size: 14px;
    }

    /* 加载状态 */
    .loading-state {
      text-align: center;
      padding: 60px;
      color: var(--muted);
    }
  `);N([$({type:String})],O.prototype,"ecomCode",2);N([l()],O.prototype,"sourcingList",2);N([l()],O.prototype,"loading",2);N([l()],O.prototype,"search",2);N([l()],O.prototype,"page",2);N([l()],O.prototype,"pages",2);N([l()],O.prototype,"total",2);N([l()],O.prototype,"stats",2);N([l()],O.prototype,"showAssetManager",2);N([l()],O.prototype,"assetManagerItem",2);O=N([x("ea-sourcing")],O);var je=Object.defineProperty,zo=Object.getOwnPropertyDescriptor,So=(r,t,e)=>t in r?je(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,dt=(r,t,e,a)=>{for(var o=a>1?void 0:a?zo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&je(t,e,o),o},Co=(r,t,e)=>So(r,t+"",e);const Ue="/api";async function Ne(r,t){const e=await fetch(r,t);if(!e.ok){const a=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(a.detail||`HTTP ${e.status}`)}return e.json()}async function To(r){const t=new URLSearchParams(Object.entries(r).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return Ne(`${Ue}/translation-logs?${t}`)}async function Ao(){return Ne(`${Ue}/translation-logs/stats`)}let q=class extends b{constructor(){super(...arguments);d(this,"logs",[]);d(this,"stats",null);d(this,"loading",!0);d(this,"page",1);d(this,"pages",0);d(this,"statusFilter","")}async connectedCallback(){super.connectedCallback(),await this.loadData()}async loadData(){this.loading=!0;try{const[t,e]=await Promise.all([To({page:this.page,limit:20,status:this.statusFilter||void 0}),Ao()]);this.logs=t.data,this.pages=t.pagination.pages,this.stats=e}catch(t){console.error("Failed to load translation logs:",t)}finally{this.loading=!1,this.requestUpdate()}}_onStatusFilter(t){this.statusFilter=t.target.value,this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_formatDateTime(t){return t?new Date(t).toLocaleString("zh-CN",{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit"}):"-"}_renderStatusBadge(t){return i`
      <span class="status-badge ${t}">
        <span class="status-dot"></span>
        ${{pending:"等待中",running:"运行中",completed:"已完成",failed:"失败"}[t]||t}
      </span>
    `}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),o=Math.min(this.pages,a+5-1);o-a<4&&(a=Math.max(1,o-5+1)),a>1&&t.push(i`
        <button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>
        ${a>2?i`<span style="color:var(--muted)">...</span>`:""}
      `);for(let s=a;s<=o;s++)t.push(i`
        <button class="page-btn ${s===this.page?"active":""}" @click=${()=>this._onPageChange(s)}>${s}</button>
      `);return o<this.pages&&t.push(i`
        ${o<this.pages-1?i`<span style="color:var(--muted)">...</span>`:""}
        <button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>
      `),i`<div class="pagination">${t}</div>`}render(){return i`
      <h2>翻译日志</h2>
      
      ${this.stats?i`
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon total">📋</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.total_tasks}</div>
              <div class="stat-label">总任务数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon success">✅</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.success_count}</div>
              <div class="stat-label">翻译成功</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon failed">❌</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.failed_count}</div>
              <div class="stat-label">翻译失败</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon pending">⏳</div>
            <div class="stat-content">
              <div class="stat-value">${this.stats.status_counts.pending||0}</div>
              <div class="stat-label">等待中</div>
            </div>
          </div>
        </div>
      `:""}
      
      <div class="toolbar">
        <select class="select" @change=${this._onStatusFilter}>
          <option value="">全部状态</option>
          <option value="pending" ?selected=${this.statusFilter==="pending"}>等待中</option>
          <option value="running" ?selected=${this.statusFilter==="running"}>运行中</option>
          <option value="completed" ?selected=${this.statusFilter==="completed"}>已完成</option>
          <option value="failed" ?selected=${this.statusFilter==="failed"}>失败</option>
        </select>
        <button class="btn btn-secondary" @click=${()=>this.loadData()}>刷新</button>
      </div>
      
      ${this.loading?i`
        <div class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      `:this.logs.length===0?i`
        <div class="table-container">
          <div class="empty-state">
            <div class="empty-icon">📝</div>
            <p>暂无翻译日志</p>
          </div>
        </div>
      `:i`
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>批次ID</th>
                <th>状态</th>
                <th>总数</th>
                <th>成功</th>
                <th>失败</th>
                <th>开始时间</th>
                <th>完成时间</th>
                <th>错误信息</th>
              </tr>
            </thead>
            <tbody>
              ${this.logs.map(t=>i`
                <tr>
                  <td style="font-family:var(--mono);font-size:12px">${t.batch_id}</td>
                  <td>${this._renderStatusBadge(t.status)}</td>
                  <td>${t.total_count}</td>
                  <td style="color:var(--ok)">${t.success_count}</td>
                  <td style="color:var(--danger)">${t.failed_count}</td>
                  <td>${this._formatDateTime(t.started_at)}</td>
                  <td>${this._formatDateTime(t.completed_at)}</td>
                  <td style="color:var(--danger);font-size:12px">${t.error_message||"-"}</td>
                </tr>
              `)}
            </tbody>
          </table>
          ${this.pages>1?this._renderPagination():""}
        </div>
      `}
    `}};Co(q,"styles",f`
    :host { display: block; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin-bottom: 24px;
    }
    
    /* 统计卡片 */
    .stats-row {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px 20px;
      flex: 1;
      display: flex;
      align-items: center;
      gap: 16px;
    }
    
    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }
    
    .stat-icon.total { background: var(--accent-subtle); color: var(--accent); }
    .stat-icon.success { background: var(--ok-subtle); color: var(--ok); }
    .stat-icon.failed { background: var(--danger-subtle); color: var(--danger); }
    .stat-icon.pending { background: var(--warning-subtle); color: var(--warning); }
    
    .stat-content { flex: 1; }
    
    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--text-strong);
    }
    
    .stat-label {
      font-size: 13px;
      color: var(--muted);
      margin-top: 2px;
    }
    
    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 12px 16px;
      margin-bottom: 24px;
      display: flex;
      gap: 12px;
      align-items: center;
    }
    
    .select {
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
    }
    
    .select:focus {
      outline: none;
      border-color: var(--accent);
    }
    
    .btn {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: none;
    }
    
    .btn-secondary {
      background: var(--bg-elevated);
      color: var(--text);
      border: 1px solid var(--border);
    }
    
    .btn-secondary:hover { background: var(--bg-hover); }
    
    /* 表格 */
    .table-container {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      overflow: hidden;
    }
    
    table { width: 100%; border-collapse: collapse; }
    
    th {
      background: var(--bg-accent);
      padding: 12px 16px;
      font-size: 12px;
      font-weight: 600;
      color: var(--muted);
      text-align: left;
      border-bottom: 1px solid var(--border);
      white-space: nowrap;
    }
    
    td {
      padding: 12px 16px;
      font-size: 13px;
      color: var(--text);
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--card-highlight); }
    
    /* 状态标签 */
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
    }
    
    .status-badge.pending {
      background: var(--warning-subtle);
      color: var(--warning);
    }
    
    .status-badge.running {
      background: var(--accent-subtle);
      color: var(--accent);
    }
    
    .status-badge.completed {
      background: var(--ok-subtle);
      color: var(--ok);
    }
    
    .status-badge.failed {
      background: var(--danger-subtle);
      color: var(--danger);
    }
    
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: currentColor;
    }
    
    .status-badge.running .status-dot {
      animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }
    
    /* 分页 */
    .pagination {
      display: flex;
      justify-content: center;
      gap: 8px;
      padding: 16px;
    }
    
    .page-btn {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg-elevated);
      color: var(--text);
      cursor: pointer;
      font-size: 13px;
    }
    
    .page-btn:hover { background: var(--bg-hover); }
    
    .page-btn.active {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    
    /* 空状态 */
    .empty-state {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    /* 加载状态 */
    .loading {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 12px;
    }
    
    @keyframes spin { to { transform: rotate(360deg); } }
  `);dt([l()],q.prototype,"logs",2);dt([l()],q.prototype,"stats",2);dt([l()],q.prototype,"loading",2);dt([l()],q.prototype,"page",2);dt([l()],q.prototype,"pages",2);dt([l()],q.prototype,"statusFilter",2);q=dt([x("ea-translation-logs")],q);var Fe=Object.defineProperty,Oo=Object.getOwnPropertyDescriptor,Mo=(r,t,e)=>t in r?Fe(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,L=(r,t,e,a)=>{for(var o=a>1?void 0:a?Oo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Fe(t,e,o),o},Do=(r,t,e)=>Mo(r,t+"",e);let D=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"item",null);d(this,"assets",{showcase:[],video:[],detail:[]});d(this,"loading",!0);d(this,"generating",!1);d(this,"generateType","");d(this,"showGenerateModal",!1);d(this,"taskInfo",null);d(this,"pollingTask",!1)}connectedCallback(){super.connectedCallback(),setTimeout(()=>this.loadAssets(),0)}updated(t){t.has("ecomCode")&&this.ecomCode&&this.loadAssets()}async loadAssets(){if(!this.ecomCode){this.loading=!1,this.assets={showcase:[],video:[],detail:[]},this.requestUpdate();return}this.loading=!0;try{const e=await(await fetch(`/api/assets/${this.ecomCode}`)).json();this.assets=e.assets||{showcase:[],video:[],detail:[]},console.log("[AssetManager] API response:",e)}catch(t){console.error("[AssetManager] 加载素材失败:",t)}this.loading=!1,this.requestUpdate()}_close(){this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}_showGenerateModal(t){console.log("[AssetManager] _showGenerateModal:",t),this.generateType=t,this.showGenerateModal=!0,this.taskInfo=null,this.requestUpdate()}_closeGenerateModal(){console.log("[AssetManager] _closeGenerateModal"),this.showGenerateModal=!1,this.generateType="",this.pollingTask=!1,this.requestUpdate()}async _startGenerate(){console.log("[AssetManager] _startGenerate called, generateType:",this.generateType),this.generating=!0,this.requestUpdate();try{let t="/api/assets/generate/image",e={ecom_code:this.ecomCode,asset_type:this.generateType};this.generateType==="video"&&(t="/api/assets/generate/video",e={ecom_code:this.ecomCode,duration:5,resolution:"480p"});const o=await(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json();o.success?(this.taskInfo={task_id:o.task_id,status:"pending",progress:0,message:"任务已提交..."},this.pollingTask=!0,this._pollTaskStatus(o.task_id)):(alert("生成任务提交失败: "+o.message),this.generating=!1)}catch(t){console.error("生成失败:",t),alert("生成失败，请检查服务器连接"),this.generating=!1}}async _pollTaskStatus(t){for(;this.pollingTask;)try{const a=await(await fetch(`/api/tasks/${t}`)).json();if(this.taskInfo=a,a.status==="success"||a.status==="failed"){this.pollingTask=!1,this.generating=!1,a.status==="success"?(await this.loadAssets(),this.showGenerateModal=!1):alert("生成失败: "+a.error);break}await new Promise(o=>setTimeout(o,2e3))}catch(e){console.error("轮询任务状态失败:",e),this.pollingTask=!1,this.generating=!1}}async _deleteAsset(t,e){if(confirm(`确定删除 ${t} 组 ${e}？`))try{(await fetch(`/api/assets/${this.ecomCode}/${t}/${e}`,{method:"DELETE"})).ok?await this.loadAssets():alert("删除失败")}catch(a){console.error("删除失败:",a)}}_previewAsset(t,e){const a=e.files||[];if(a.length!==0)if(t==="video"){const o=a.find(s=>s.includes("merged"));o&&window.open("/assets/"+o,"_blank")}else window.open("/assets/"+a[0],"_blank")}render(){var e;if(console.log("[AssetManager] render called, ecomCode:",this.ecomCode,"loading:",this.loading,"assets:",this.assets),this.loading)return i`
        <div class="asset-manager">
          <div style="text-align: center; padding: 40px; color: var(--muted);">
            加载中...
          </div>
        </div>
      `;const t={showcase:"展示图",video:"宣传视频",detail:"详情图"};return i`
      <div class="asset-manager">
        <div class="asset-header">
          <div class="asset-title">📁 素材管理</div>
          <button class="asset-close" @click=${this._close}>×</button>
        </div>
        
        <div style="font-size: 12px; color: var(--muted); margin-bottom: 16px;">
          商品: ${((e=this.item)==null?void 0:e.title)||this.ecomCode}
        </div>
        
        ${["showcase","video","detail"].map(a=>{var o,s;return i`
          <div class="asset-section">
            <div class="section-header">
              <div>
                <span class="section-title">${t[a]}</span>
                <span class="section-count">(${((o=this.assets[a])==null?void 0:o.length)||0}组)</span>
              </div>
              <button class="add-btn" @click=${()=>this._showGenerateModal(a)}>
                + 生成
              </button>
            </div>
            
            ${((s=this.assets[a])==null?void 0:s.length)>0?this.assets[a].map(n=>{var p;return i`
                <div class="asset-group">
                  <div class="group-index">组 ${n.group_index}</div>
                  <div class="group-files">${((p=n.files)==null?void 0:p.length)||0} 个文件</div>
                  <div class="group-actions">
                    <button class="preview-btn" @click=${()=>this._previewAsset(a,n)}>
                      预览
                    </button>
                    <button class="delete-btn" @click=${()=>this._deleteAsset(a,n.group_index)}>
                      删除
                    </button>
                  </div>
                </div>
              `}):i`<div class="empty-section">暂无素材</div>`}
          </div>
        `})}
      </div>
      
      ${this.showGenerateModal?i`
        <div class="gen-modal-overlay" @click=${a=>{a.target===a.currentTarget&&this._closeGenerateModal()}}>
          <div class="gen-modal">
            <div class="gen-modal-title">
              ${this.generateType==="video"?"🎬 生成宣传视频":this.generateType==="showcase"?"🖼️ 生成展示图":"📋 生成详情图"}
            </div>
            
            <div class="gen-option">
              <div class="gen-label">图片来源：</div>
              <div class="gen-radio-group">
                <label class="gen-radio">
                  <input type="radio" name="imageSource" value="sourcing" checked>
                  使用货源图片
                </label>
                <label class="gen-radio">
                  <input type="radio" name="imageSource" value="custom">
                  上传自定义图片
                </label>
              </div>
            </div>
            
            ${this.generateType==="video"?i`
              <div class="gen-option">
                <div class="gen-label">视频时长：</div>
                <select class="gen-select">
                  <option value="5">5 秒/段（共15秒）</option>
                  <option value="8">8 秒/段（共24秒）</option>
                </select>
              </div>
              
              <div class="gen-option">
                <div class="gen-label">分辨率：</div>
                <select class="gen-select">
                  <option value="480p">480p（更快）</option>
                  <option value="720p">720p（更清晰）</option>
                </select>
              </div>
            `:""}
            
            ${this.taskInfo?i`
              <div class="task-progress">
                <div class="task-status">
                  状态: ${this.taskInfo.status==="pending"?"等待中":this.taskInfo.status==="running"?"生成中...":this.taskInfo.status==="success"?"完成":"失败"}
                </div>
                <div class="task-bar">
                  <div class="task-bar-fill" style="width: ${this.taskInfo.progress}%"></div>
                </div>
                <div class="task-message">${this.taskInfo.message||""}</div>
              </div>
            `:""}
            
            <div class="gen-buttons">
              <button class="gen-cancel" @click=${this._closeGenerateModal} 
                ?disabled=${this.pollingTask}>
                取消
              </button>
              <button class="gen-confirm" @click=${this._startGenerate}
                ?disabled=${this.generating||this.pollingTask}>
                ${this.generating?"生成中...":"开始生成"}
              </button>
            </div>
          </div>
        </div>
      `:""}
    `}};Do(D,"styles",f`
    :host {
      display: block;
    }
    
    .asset-manager {
      padding: 20px;
      max-width: 600px;
    }
    
    .asset-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }
    
    .asset-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
    }
    
    .asset-close {
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--muted);
    }
    
    .asset-section {
      margin-bottom: 24px;
    }
    
    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    
    .section-title {
      font-size: 14px;
      font-weight: 500;
      color: var(--text);
    }
    
    .section-count {
      font-size: 12px;
      color: var(--muted);
    }
    
    .add-btn {
      padding: 6px 12px;
      font-size: 12px;
      border: 1px solid var(--primary);
      border-radius: var(--radius-sm);
      background: transparent;
      color: var(--primary);
      cursor: pointer;
    }
    
    .add-btn:hover {
      background: var(--primary);
      color: white;
    }
    
    .asset-group {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .group-index {
      font-size: 12px;
      color: var(--muted);
      min-width: 50px;
    }
    
    .group-files {
      font-size: 13px;
      color: var(--text);
      flex: 1;
    }
    
    .group-actions {
      display: flex;
      gap: 8px;
    }
    
    .preview-btn, .delete-btn {
      padding: 4px 8px;
      font-size: 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
    }
    
    .preview-btn {
      background: var(--primary);
      color: white;
      border: none;
    }
    
    .delete-btn {
      background: transparent;
      border: 1px solid #f5222d;
      color: #f5222d;
    }
    
    .empty-section {
      text-align: center;
      padding: 20px;
      color: var(--muted);
      font-size: 13px;
    }
    
    /* 生成弹窗 */
    .gen-modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1100;
    }
    
    .gen-modal {
      background: var(--card);
      border-radius: var(--radius-lg);
      padding: 24px;
      max-width: 400px;
      width: 90%;
    }
    
    .gen-modal-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 20px;
    }
    
    .gen-option {
      margin-bottom: 16px;
    }
    
    .gen-label {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .gen-radio-group {
      display: flex;
      gap: 16px;
    }
    
    .gen-radio {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
    }
    
    .gen-select {
      width: 100%;
      padding: 8px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
    }
    
    .gen-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 24px;
    }
    
    .gen-cancel, .gen-confirm {
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      cursor: pointer;
    }
    
    .gen-cancel {
      background: var(--bg);
      border: 1px solid var(--border);
      color: var(--text);
    }
    
    .gen-confirm {
      background: var(--primary);
      border: none;
      color: white;
    }
    
    .gen-confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    /* 任务进度 */
    .task-progress {
      padding: 16px;
      background: var(--bg);
      border-radius: var(--radius-md);
      margin-top: 16px;
    }
    
    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .task-bar {
      height: 4px;
      background: var(--border);
      border-radius: 2px;
      overflow: hidden;
    }
    
    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }
    
    .task-message {
      font-size: 12px;
      color: var(--muted);
      margin-top: 8px;
    }
  `);L([$({type:String})],D.prototype,"ecomCode",2);L([$({type:Object})],D.prototype,"item",2);L([l()],D.prototype,"assets",2);L([l()],D.prototype,"loading",2);L([l()],D.prototype,"generating",2);L([l()],D.prototype,"generateType",2);L([l()],D.prototype,"showGenerateModal",2);L([l()],D.prototype,"taskInfo",2);L([l()],D.prototype,"pollingTask",2);D=L([x("asset-manager")],D);var Le=Object.defineProperty,Eo=Object.getOwnPropertyDescriptor,Io=(r,t,e)=>t in r?Le(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,lt=(r,t,e,a)=>{for(var o=a>1?void 0:a?Eo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Le(t,e,o),o},jo=(r,t,e)=>Io(r,t+"",e);let H=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"item",null);d(this,"generateType","showcase");d(this,"generating",!1);d(this,"taskInfo",null);d(this,"pollingTask",!1)}_close(){this.dispatchEvent(new CustomEvent("close"))}async _startGenerate(){if(!this.ecomCode){alert("缺少商品编码");return}this.generating=!0;try{let t="/api/assets/generate/image";const e={ecom_code:this.ecomCode,asset_type:this.generateType};this.generateType==="video"&&(t="/api/assets/generate/video");const o=await(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json();o.success?(this.taskInfo={task_id:o.task_id,status:"pending",progress:0,message:"任务已提交..."},this.pollingTask=!0,this._pollTaskStatus(o.task_id)):(alert("生成任务提交失败: "+o.message),this.generating=!1)}catch(t){console.error("生成失败:",t),alert("生成失败,请检查服务器连接"),this.generating=!1}}async _pollTaskStatus(t){for(;this.pollingTask;)try{const a=await(await fetch(`/api/tasks/${t}`)).json();if(this.taskInfo=a,a.status==="success"||a.status==="failed"){this.pollingTask=!1,this.generating=!1,a.status==="success"?setTimeout(()=>{alert("生成成功!"),this._close()},500):alert("生成失败: "+a.error);break}await new Promise(o=>setTimeout(o,2e3))}catch(e){console.error("轮询任务状态失败:",e),this.pollingTask=!1,this.generating=!1}}render(){var e,a,o;const t=(e=this.item)!=null&&e.local_image_path?`/images/${this.item.local_image_path}`:(a=this.item)==null?void 0:a.image_url;return i`
      <div class="generator">
        <div class="gen-header">
          <div class="gen-title">生成素材</div>
          <button class="gen-close" @click=${this._close} ?disabled=${this.generating}>×</button>
        </div>

        <div class="product-info">
          ${t?i`<img class="product-thumb" src=${t} />`:""}
          <div style="flex:1; overflow: hidden;">
            <div class="product-name">${((o=this.item)==null?void 0:o.title)||this.ecomCode}</div>
            <div class="product-code">${this.ecomCode}</div>
          </div>
        </div>

        <div class="type-section">
          <div class="type-label">选择素材类型</div>
          <div class="type-options">
            <button
              class="type-option ${this.generateType==="showcase"?"active":""}"
              @click=${()=>{this.generateType="showcase",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🖼️</div>
              <div class="type-option-label">展示图</div>
              <div class="type-option-desc">9张营销图</div>
            </button>
            <button
              class="type-option ${this.generateType==="video"?"active":""}"
              @click=${()=>{this.generateType="video",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🎬</div>
              <div class="type-option-label">视频</div>
              <div class="type-option-desc">宣传视频</div>
            </button>
            <button
              class="type-option ${this.generateType==="detail"?"active":""}"
              @click=${()=>{this.generateType="detail",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">📋</div>
              <div class="type-option-label">详情图</div>
              <div class="type-option-desc">详情页图片</div>
            </button>
          </div>
        </div>

        ${this.taskInfo?i`
          <div class="task-progress">
            <div class="task-status">${this.taskInfo.message||"处理中..."}</div>
            <div class="task-bar">
              <div class="task-bar-fill" style="width: ${this.taskInfo.progress||0}%"></div>
            </div>
          </div>
        `:""}

        <div class="gen-actions">
          <button class="gen-btn gen-btn-cancel" @click=${this._close} ?disabled=${this.generating}>
            取消
          </button>
          <button class="gen-btn gen-btn-confirm" @click=${this._startGenerate} ?disabled=${this.generating}>
            ${this.generating?"生成中...":"开始生成"}
          </button>
        </div>
      </div>
    `}};jo(H,"styles",f`
    :host {
      display: block;
    }

    .generator {
      padding: 20px;
      min-width: 400px;
    }

    .gen-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }

    .gen-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
    }

    .gen-close {
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--muted);
      line-height: 1;
    }

    .gen-close:hover {
      color: var(--text);
    }

    .product-info {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .product-thumb {
      width: 48px;
      height: 48px;
      object-fit: cover;
      border-radius: var(--radius-sm);
    }

    .product-name {
      font-size: 13px;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      flex: 1;
    }

    .product-code {
      font-size: 11px;
      color: var(--muted);
    }

    .type-section {
      margin-bottom: 20px;
    }

    .type-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .type-options {
      display: flex;
      gap: 12px;
    }

    .type-option {
      flex: 1;
      padding: 16px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }

    .type-option:hover {
      border-color: var(--primary);
      background: var(--bg-hover);
    }

    .type-option.active {
      border-color: var(--primary);
      border-width: 2px;
      background: var(--primary);
      box-shadow: 0 0 0 2px rgba(var(--primary-rgb, 59, 130, 246), 0.3);
    }

    .type-option.active .type-option-label {
      color: white;
      font-weight: 600;
    }

    .type-option.active .type-option-desc {
      color: rgba(255, 255, 255, 0.8);
    }

    .type-option-icon {
      font-size: 24px;
      margin-bottom: 8px;
    }

    .type-option-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
      margin-bottom: 4px;
    }

    .type-option-desc {
      font-size: 11px;
      color: var(--muted);
    }

    .task-progress {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 20px;
    }

    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 12px;
    }

    .task-bar {
      height: 4px;
      background: var(--border);
      border-radius: 2px;
      overflow: hidden;
    }

    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }

    .gen-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }

    .gen-btn {
      padding: 10px 20px;
      font-size: 13px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s;
    }

    .gen-btn-cancel {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
    }

    .gen-btn-cancel:hover {
      border-color: var(--text);
      color: var(--text);
    }

    .gen-btn-confirm {
      background: var(--primary);
      border: none;
      color: white;
    }

    .gen-btn-confirm:hover {
      opacity: 0.9;
    }

    .gen-btn-confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `);lt([$({type:String})],H.prototype,"ecomCode",2);lt([$({type:Object})],H.prototype,"item",2);lt([l()],H.prototype,"generateType",2);lt([l()],H.prototype,"generating",2);lt([l()],H.prototype,"taskInfo",2);lt([l()],H.prototype,"pollingTask",2);H=lt([x("asset-generator")],H);var Ve=Object.defineProperty,Uo=Object.getOwnPropertyDescriptor,No=(r,t,e)=>t in r?Ve(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,A=(r,t,e,a)=>{for(var o=a>1?void 0:a?Uo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Ve(t,e,o),o},Fo=(r,t,e)=>No(r,t+"",e);let P=class extends b{constructor(){super(...arguments);d(this,"sourcingCode","");d(this,"item",null);d(this,"generateType","showcase");d(this,"generating",!1);d(this,"taskInfo",null);d(this,"pollingTask",!1);d(this,"uploadedImagePath","");d(this,"uploadedImagePreview","");d(this,"uploading",!1);d(this,"isDragging",!1);d(this,"sourcingList",[]);d(this,"videoDuration",5);d(this,"videoResolution","480p")}_close(){this.dispatchEvent(new CustomEvent("close"))}connectedCallback(){super.connectedCallback(),this.loadSourcingList()}async loadSourcingList(){try{const e=await(await fetch("/api/sourcing/list?limit=100")).json();console.log("[UploadGenerator] 货源列表:",e),this.sourcingList=e.data||[],this.requestUpdate(),console.log("[UploadGenerator] sourcingList 长度:",this.sourcingList.length)}catch(t){console.error("[UploadGenerator] 加载货源列表失败:",t)}}_handleDragOver(t){t.preventDefault(),this.isDragging=!0}_handleDragLeave(t){t.preventDefault(),this.isDragging=!1}_handleDrop(t){var a;t.preventDefault(),this.isDragging=!1;const e=(a=t.dataTransfer)==null?void 0:a.files;e&&e.length>0&&this._uploadFile(e[0])}_handleFileSelect(t){const a=t.target.files;a&&a.length>0&&this._uploadFile(a[0])}async _uploadFile(t){if(!t.type.startsWith("image/")){alert("请上传图片文件");return}if(t.size>10*1024*1024){alert("图片大小不能超过 10MB");return}this.uploading=!0;try{const e=new FormData;e.append("file",t);const o=await(await fetch("/api/assets/upload-image",{method:"POST",body:e})).json();o.success?(this.uploadedImagePath=o.path,this.uploadedImagePreview=o.url):alert("上传失败: "+o.message)}catch(e){console.error("上传失败:",e),alert("上传失败，请检查服务器连接")}this.uploading=!1}_clearImage(){this.uploadedImagePath="",this.uploadedImagePreview=""}async _startGenerate(){if(!this.uploadedImagePath){alert("请先上传图片");return}this.generating=!0;try{let t="/api/assets/generate/upload";const e={image_path:this.uploadedImagePath,asset_type:this.generateType,sourcing_code:this.sourcingCode||null};this.generateType==="video"&&(e.duration=this.videoDuration,e.resolution=this.videoResolution);const o=await(await fetch(t,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)})).json();o.success?(this.taskInfo={task_id:o.task_id,status:"pending",progress:0,message:"任务已提交..."},this.pollingTask=!0,this._pollTaskStatus(o.task_id)):(alert("生成任务提交失败: "+o.message),this.generating=!1)}catch(t){console.error("生成失败:",t),alert("生成失败，请检查服务器连接"),this.generating=!1}}async _pollTaskStatus(t){for(;this.pollingTask;)try{const a=await(await fetch(`/api/tasks/${t}`)).json();if(this.taskInfo=a,a.status==="success"||a.status==="failed"){this.pollingTask=!1,this.generating=!1,a.status==="success"?setTimeout(()=>{alert("生成成功!"),this._close()},500):alert("生成失败: "+a.error);break}await new Promise(o=>setTimeout(o,2e3))}catch(e){console.error("轮询任务状态失败:",e),this.pollingTask=!1,this.generating=!1}}render(){return i`
      <div class="generator">
        <div class="gen-header">
          <div class="gen-title">上传图片生成素材</div>
          <button class="gen-close" @click=${this._close} ?disabled=${this.generating}>×</button>
        </div>

        <!-- 上传区域 -->
        <div class="upload-section">
          <div class="upload-label">参考图片</div>
          ${this.uploadedImagePreview?i`
            <div class="upload-area has-image">
              <img class="preview-image" src=${this.uploadedImagePreview} />
              <div class="preview-actions">
                <button class="preview-btn" @click=${()=>{var t,e;return(e=(t=this.shadowRoot)==null?void 0:t.querySelector(".upload-input"))==null?void 0:e.click()}}>
                  更换图片
                </button>
                <button class="preview-btn" @click=${this._clearImage}>
                  清除
                </button>
              </div>
            </div>
          `:i`
            <div 
              class="upload-area ${this.isDragging?"dragging":""}"
              @click=${()=>{var t,e;return(e=(t=this.shadowRoot)==null?void 0:t.querySelector(".upload-input"))==null?void 0:e.click()}}
              @dragover=${this._handleDragOver}
              @dragleave=${this._handleDragLeave}
              @drop=${this._handleDrop}
            >
              <div class="upload-icon">📤</div>
              <div class="upload-text">${this.uploading?"上传中...":"拖拽图片到此处或点击上传"}</div>
              <div class="upload-hint">支持 JPG、PNG、WebP 格式，最大 10MB</div>
            </div>
          `}
          <input 
            class="upload-input"
            type="file"
            accept="image/*"
            @change=${this._handleFileSelect}
          />
        </div>

        <!-- 货源选择 -->
        <div class="sourcing-section">
          <div class="sourcing-label">关联货源（可选）</div>
          <select 
            class="sourcing-select"
            .value=${this.sourcingCode}
            @change=${t=>{this.sourcingCode=t.target.value}}
          >
            <option value="">不关联货源</option>
            ${this.sourcingList.map(t=>i`
              <option value=${t.sourcing_code}>${t.title||t.sourcing_code}</option>
            `)}
          </select>
        </div>

        <!-- 类型选择 -->
        <div class="type-section">
          <div class="type-label">选择素材类型</div>
          <div class="type-options">
            <button
              class="type-option ${this.generateType==="showcase"?"active":""}"
              @click=${()=>{this.generateType="showcase",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🖼️</div>
              <div class="type-option-label">展示图</div>
              <div class="type-option-desc">9张营销图</div>
            </button>
            <button
              class="type-option ${this.generateType==="video"?"active":""}"
              @click=${()=>{this.generateType="video",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">🎬</div>
              <div class="type-option-label">视频</div>
              <div class="type-option-desc">宣传视频</div>
            </button>
            <button
              class="type-option ${this.generateType==="detail"?"active":""}"
              @click=${()=>{this.generateType="detail",this.requestUpdate()}}
              ?disabled=${this.generating}
            >
              <div class="type-option-icon">📋</div>
              <div class="type-option-label">详情图</div>
              <div class="type-option-desc">详情页图片</div>
            </button>
          </div>
        </div>

        <!-- 视频参数 -->
        ${this.generateType==="video"?i`
          <div class="video-params">
            <div class="param-row">
              <div class="param-group">
                <div class="param-label">视频时长</div>
                <select 
                  class="param-select"
                  .value=${String(this.videoDuration)}
                  @change=${t=>{this.videoDuration=parseInt(t.target.value)}}
                >
                  <option value="3">3 秒</option>
                  <option value="5">5 秒</option>
                  <option value="10">10 秒</option>
                  <option value="15">15 秒</option>
                </select>
              </div>
              <div class="param-group">
                <div class="param-label">分辨率</div>
                <select 
                  class="param-select"
                  .value=${this.videoResolution}
                  @change=${t=>{this.videoResolution=t.target.value}}
                >
                  <option value="480p">480p</option>
                  <option value="720p">720p</option>
                  <option value="1080p">1080p</option>
                </select>
              </div>
            </div>
          </div>
        `:""}

        ${this.taskInfo?i`
          <div class="task-progress">
            <div class="task-status">${this.taskInfo.message||"处理中..."}</div>
            <div class="task-bar">
              <div class="task-bar-fill" style="width: ${this.taskInfo.progress||0}%"></div>
            </div>
          </div>
        `:""}

        <div class="gen-actions">
          <button class="gen-btn gen-btn-cancel" @click=${this._close} ?disabled=${this.generating}>
            取消
          </button>
          <button 
            class="gen-btn gen-btn-confirm" 
            @click=${this._startGenerate} 
            ?disabled=${this.generating||!this.uploadedImagePath}
          >
            ${this.generating?"生成中...":"开始生成"}
          </button>
        </div>
      </div>
    `}};Fo(P,"styles",f`
    :host {
      display: block;
    }

    .generator {
      padding: 24px;
      width: 500px;
      max-width: 90vw;
      box-sizing: border-box;
    }

    .gen-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }

    .gen-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
    }

    .gen-close {
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: var(--muted);
      line-height: 1;
    }

    .gen-close:hover {
      color: var(--text);
    }

    /* 上传区域 */
    .upload-section {
      margin-bottom: 24px;
    }

    .upload-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .upload-area {
      border: 2px dashed var(--border);
      border-radius: var(--radius-md);
      padding: 40px 20px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: var(--bg);
    }

    .upload-area:hover {
      border-color: var(--primary);
      background: var(--bg-hover);
    }

    .upload-area.dragging {
      border-color: var(--primary);
      background: rgba(var(--primary-rgb, 59, 130, 246), 0.1);
    }

    .upload-area.has-image {
      padding: 16px;
    }

    .upload-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    .upload-text {
      font-size: 14px;
      color: var(--text);
      margin-bottom: 8px;
    }

    .upload-hint {
      font-size: 12px;
      color: var(--muted);
    }

    /* 货源选择 */
    .sourcing-section {
      margin-bottom: 24px;
    }

    .sourcing-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .sourcing-select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      cursor: pointer;
    }

    .sourcing-select:focus {
      border-color: var(--primary);
      outline: none;
    }

    .upload-input {
      display: none;
    }

    .preview-image {
      max-width: 100%;
      max-height: 200px;
      border-radius: var(--radius-sm);
      object-fit: contain;
    }

    .preview-actions {
      margin-top: 12px;
      display: flex;
      gap: 8px;
      justify-content: center;
    }

    .preview-btn {
      padding: 6px 12px;
      font-size: 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--bg);
      color: var(--text);
    }

    .preview-btn:hover {
      background: var(--bg-hover);
    }

    /* 类型选择 */
    .type-section {
      margin-bottom: 24px;
    }

    .type-label {
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 12px;
    }

    .type-options {
      display: flex;
      gap: 12px;
    }

    .type-option {
      flex: 1;
      padding: 16px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
    }

    .type-option:hover {
      border-color: var(--primary);
      background: var(--bg-hover);
    }

    .type-option.active {
      border-color: var(--primary);
      background: var(--primary);
    }

    .type-option.active .type-option-label {
      color: white;
      font-weight: 600;
    }

    .type-option.active .type-option-desc {
      color: rgba(255, 255, 255, 0.8);
    }

    .type-option-icon {
      font-size: 24px;
      margin-bottom: 8px;
    }

    .type-option-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
      margin-bottom: 4px;
    }

    .type-option-desc {
      font-size: 11px;
      color: var(--muted);
    }

    /* 视频参数 */
    .video-params {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 24px;
    }

    .param-row {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .param-group {
      flex: 1;
    }

    .param-label {
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
    }

    .param-select {
      width: 100%;
      padding: 8px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg);
      color: var(--text);
      font-size: 13px;
    }

    /* 进度条 */
    .task-progress {
      background: var(--bg);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 20px;
    }

    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 12px;
    }

    .task-bar {
      height: 4px;
      background: var(--border);
      border-radius: 2px;
      overflow: hidden;
    }

    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }

    /* 操作按钮 */
    .gen-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }

    .gen-btn {
      padding: 10px 20px;
      font-size: 13px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: all 0.2s;
    }

    .gen-btn-cancel {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--muted);
    }

    .gen-btn-cancel:hover {
      border-color: var(--text);
      color: var(--text);
    }

    .gen-btn-confirm {
      background: var(--primary);
      border: none;
      color: white;
    }

    .gen-btn-confirm:hover {
      opacity: 0.9;
    }

    .gen-btn-confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `);A([$({type:String})],P.prototype,"sourcingCode",2);A([$({type:Object})],P.prototype,"item",2);A([l()],P.prototype,"generateType",2);A([l()],P.prototype,"generating",2);A([l()],P.prototype,"taskInfo",2);A([l()],P.prototype,"pollingTask",2);A([l()],P.prototype,"uploadedImagePath",2);A([l()],P.prototype,"uploadedImagePreview",2);A([l()],P.prototype,"uploading",2);A([l()],P.prototype,"isDragging",2);A([l()],P.prototype,"sourcingList",2);A([l()],P.prototype,"videoDuration",2);A([l()],P.prototype,"videoResolution",2);P=A([x("upload-generator")],P);var Re=Object.defineProperty,Lo=Object.getOwnPropertyDescriptor,Vo=(r,t,e)=>t in r?Re(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,vt=(r,t,e,a)=>{for(var o=a>1?void 0:a?Lo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&Re(t,e,o),o},Ro=(r,t,e)=>Vo(r,t+"",e);let Q=class extends b{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"searchQuery","");d(this,"assets",[]);d(this,"loading",!0);d(this,"showUploadModal",!1)}connectedCallback(){super.connectedCallback(),console.log("[AssetsPage] connectedCallback called"),this.ecomCode&&(this.searchQuery=this.ecomCode),this.loadAssets()}updated(t){t.has("ecomCode")&&this.ecomCode&&(this.searchQuery=this.ecomCode,this.loadAssets())}async loadAssets(){console.log("[AssetsPage] loadAssets called"),this.loading=!0,this.requestUpdate();try{const t=this.searchQuery?`/api/assets/list?search=${encodeURIComponent(this.searchQuery)}`:"/api/assets/list";console.log("[AssetsPage] fetching:",t);const a=await(await fetch(t)).json();console.log("[AssetsPage] response:",a),this.assets=a.assets||[]}catch(t){console.error("[AssetsPage] 加载素材失败:",t),this.assets=[]}this.loading=!1,console.log("[AssetsPage] loadAssets done, loading:",this.loading,"assets:",this.assets.length),this.requestUpdate()}_onSearch(t){t.key==="Enter"&&this.loadAssets()}_onSearchInput(t){const e=t.target;this.searchQuery=e.value}_openUploadModal(){this.showUploadModal=!0,this.requestUpdate(),console.log("[AssetsPage] _openUploadModal called, showUploadModal:",this.showUploadModal)}_closeUploadModal(){this.showUploadModal=!1,this.requestUpdate(),console.log("[AssetsPage] _closeUploadModal called, showUploadModal:",this.showUploadModal)}_openFolder(t,e,a){fetch(`/api/assets/open-folder/${t}/${e}/${a}`,{method:"POST"})}async _deleteAsset(t,e,a){if(confirm("确定删除该素材？"))try{(await fetch(`/api/assets/${t}/${e}/${a}`,{method:"DELETE"})).ok?await this.loadAssets():alert("删除失败")}catch(o){console.error("删除失败:",o)}}_previewImage(t){const e=document.createElement("div");e.className="preview-overlay",e.innerHTML=`
      <img class="preview-image" src="${t}" />
      <button class="preview-close">×</button>
    `,e.addEventListener("click",a=>{(a.target===e||a.target.classList.contains("preview-close"))&&e.remove()}),document.body.appendChild(e)}_formatTime(t){return t?new Date(t).toLocaleString("zh-CN",{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"}):"-"}_getTypeName(t){return{showcase:"展示图",video:"视频",detail:"详情图"}[t]||t}_getTypeIcon(t){return{showcase:"🖼️",video:"🎬",detail:"📋"}[t]||"📄"}render(){return i`
      <div class="assets-page">
        <div class="page-header">
          <h1 class="page-title">📁 素材管理</h1>
          <div class="header-actions">
            <div class="search-box">
              <span>🔍</span>
              <input 
                type="text" 
                placeholder="搜索货源名称或编码..." 
                .value=${this.searchQuery}
                @input=${this._onSearchInput}
                @keydown=${this._onSearch}
              />
            </div>
            <button class="generate-btn" @click=${()=>{console.log("[AssetsPage] 按钮被点击"),this._openUploadModal()}}>
              + 上传生成
            </button>
          </div>
        </div>

        ${this.loading?i`
          <div class="empty-state">
            <div class="empty-state-text">加载中...</div>
          </div>
        `:this.assets.length===0?i`
          <div class="empty-state">
            <div class="empty-state-icon">📁</div>
            <div class="empty-state-text">暂无素材，点击"生成素材"开始创建</div>
          </div>
        `:i`
          <table class="assets-table">
            <thead>
              <tr>
                <th style="width: 200px;">货源名称</th>
                <th style="width: 100px;">资源类型</th>
                <th style="width: 200px;">缩略图</th>
                <th>简介</th>
                <th style="width: 140px;">生成时间</th>
                <th style="width: 160px;">操作</th>
              </tr>
            </thead>
            <tbody>
              ${this.assets.map(t=>{var e,a;return i`
                <tr>
                  <td>
                    <div class="product-name">${t.title||"-"}</div>
                    <div class="product-code">${t.ecom_code}</div>
                  </td>
                  <td>
                    <span class="asset-type ${t.asset_type}">
                      ${this._getTypeIcon(t.asset_type)} ${this._getTypeName(t.asset_type)}
                    </span>
                  </td>
                  <td>
                    <div class="thumbnails">
                      ${(t.thumbnails||[]).slice(0,3).map(o=>i`
                        <img 
                          class="thumb" 
                          src="${o}" 
                          @click=${()=>this._previewImage(o)}
                        />
                      `)}
                      ${(((e=t.thumbnails)==null?void 0:e.length)||0)>3?i`
                        <div class="thumb-more">+${(((a=t.thumbnails)==null?void 0:a.length)||0)-3}</div>
                      `:""}
                    </div>
                  </td>
                  <td>-</td>
                  <td>
                    <div class="time">${this._formatTime(t.created_at)}</div>
                  </td>
                  <td>
                    <div class="actions">
                      <button 
                        class="action-btn" 
                        @click=${()=>this._openFolder(t.ecom_code,t.asset_type,t.group_index)}
                      >
                        文件
                      </button>
                      <button 
                        class="action-btn delete" 
                        @click=${()=>this._deleteAsset(t.ecom_code,t.asset_type,t.group_index)}
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              `})}
            </tbody>
          </table>
        `}
      </div>

      ${this.showUploadModal?i`
        <div class="modal-overlay" @click=${t=>{t.target===t.currentTarget&&this._closeUploadModal()}}>
          <div class="modal-content">
            <upload-generator
              @close=${this._closeUploadModal}
            ></upload-generator>
          </div>
        </div>
      `:""}
    `}};Ro(Q,"styles",f`
    :host {
      display: block;
    }
    
    .assets-page {
      padding: 24px;
    }
    
    .page-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }
    
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: var(--text);
    }
    
    .header-actions {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    
    .search-box {
      display: flex;
      align-items: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 8px 12px;
      gap: 8px;
      min-width: 300px;
    }
    
    .search-box input {
      border: none;
      background: transparent;
      color: var(--text);
      font-size: 14px;
      outline: none;
      flex: 1;
    }
    
    .search-box input::placeholder {
      color: var(--muted);
    }
    
    .generate-btn {
      padding: 8px 16px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    
    .generate-btn:hover {
      opacity: 0.9;
    }
    
    .assets-table {
      width: 100%;
      border-collapse: collapse;
      background: var(--bg);
      border-radius: var(--radius-md);
      overflow: hidden;
    }
    
    .assets-table th {
      text-align: left;
      padding: 12px 16px;
      font-size: 12px;
      font-weight: 500;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--border);
    }
    
    .assets-table td {
      padding: 16px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    
    .assets-table tr:last-child td {
      border-bottom: none;
    }
    
    .product-name {
      max-width: 200px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 14px;
      color: var(--text);
    }
    
    .product-code {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    .asset-type {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 500;
    }
    
    .asset-type.showcase {
      background: rgba(59, 130, 246, 0.1);
      color: #3b82f6;
    }
    
    .asset-type.video {
      background: rgba(239, 68, 68, 0.1);
      color: #ef4444;
    }
    
    .asset-type.detail {
      background: rgba(16, 185, 129, 0.1);
      color: #10b981;
    }
    
    .thumbnails {
      display: flex;
      gap: 4px;
      flex-wrap: wrap;
      max-width: 180px;
    }
    
    .thumb {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-sm);
      object-fit: cover;
      cursor: pointer;
      border: 1px solid var(--border);
    }
    
    .thumb:hover {
      border-color: var(--primary);
    }
    
    .thumb-more {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-sm);
      background: var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      color: var(--muted);
    }
    
    .time {
      font-size: 13px;
      color: var(--text);
    }
    
    .actions {
      display: flex;
      gap: 8px;
    }
    
    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
    }
    
    .action-btn:hover {
      background: var(--border);
    }
    
    .action-btn.delete {
      color: #ef4444;
      border-color: rgba(239, 68, 68, 0.3);
    }
    
    .action-btn.delete:hover {
      background: rgba(239, 68, 68, 0.1);
    }
    
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--muted);
    }
    
    .empty-state-icon {
      font-size: 48px;
      margin-bottom: 16px;
    }
    
    .empty-state-text {
      font-size: 14px;
    }
    
    /* 生成弹窗 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      padding: 24px;
      width: 100%;
      max-width: 500px;
      max-height: 80vh;
      overflow-y: auto;
    }
    
    .modal-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text);
      margin-bottom: 20px;
    }
    
    .form-group {
      margin-bottom: 16px;
    }
    
    .form-label {
      display: block;
      font-size: 13px;
      color: var(--muted);
      margin-bottom: 6px;
    }
    
    .form-select {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg);
      color: var(--text);
      font-size: 14px;
      outline: none;
    }
    
    .form-select:focus {
      border-color: var(--primary);
    }
    
    .type-options {
      display: flex;
      gap: 12px;
    }
    
    .type-option {
      flex: 1;
      padding: 12px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: transparent;
      cursor: pointer;
      text-align: center;
    }
    
    .type-option.active {
      border-color: var(--primary);
      background: rgba(var(--primary-rgb), 0.1);
    }
    
    .type-option-label {
      font-size: 14px;
      font-weight: 500;
      color: var(--text);
    }
    
    .type-option-desc {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    .modal-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
      margin-top: 24px;
    }
    
    .modal-btn {
      padding: 10px 20px;
      border-radius: var(--radius-md);
      font-size: 14px;
      cursor: pointer;
    }
    
    .modal-btn.cancel {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text);
    }
    
    .modal-btn.confirm {
      background: var(--primary);
      border: none;
      color: white;
    }
    
    .modal-btn.confirm:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    
    /* 任务进度 */
    .task-progress {
      padding: 16px;
      background: var(--border);
      border-radius: var(--radius-md);
      margin-top: 16px;
    }
    
    .task-status {
      font-size: 13px;
      color: var(--text);
      margin-bottom: 8px;
    }
    
    .task-bar {
      height: 4px;
      background: var(--muted);
      border-radius: 2px;
      overflow: hidden;
    }
    
    .task-bar-fill {
      height: 100%;
      background: var(--primary);
      transition: width 0.3s;
    }
    
    /* 图片预览 */
    .preview-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.9);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2000;
    }
    
    .preview-image {
      max-width: 90%;
      max-height: 90%;
      object-fit: contain;
    }
    
    .preview-close {
      position: absolute;
      top: 20px;
      right: 20px;
      background: white;
      border: none;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      font-size: 20px;
      cursor: pointer;
    }
  `);vt([$({type:String})],Q.prototype,"ecomCode",2);vt([l()],Q.prototype,"searchQuery",2);vt([l()],Q.prototype,"assets",2);vt([l()],Q.prototype,"loading",2);vt([l()],Q.prototype,"showUploadModal",2);Q=vt([x("ea-assets-page")],Q);var qe=Object.defineProperty,qo=Object.getOwnPropertyDescriptor,Ho=(r,t,e)=>t in r?qe(r,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):r[t]=e,jt=(r,t,e,a)=>{for(var o=a>1?void 0:a?qo(t,e):t,s=r.length-1,n;s>=0;s--)(n=r[s])&&(o=(a?n(t,e,o):n(o))||o);return a&&o&&qe(t,e,o),o},Go=(r,t,e)=>Ho(r,t+"",e);const bt=new Set;let st="dashboard";window.ecomagentNavigate=r=>{st=r,bt.forEach(t=>t(r))};window.ecomagentGetCurrentPage=()=>st;window.ecomagentOnPageChange=r=>{bt.add(r)};window.ecomagentOpenTrend=(r,t="product-master")=>{sessionStorage.setItem("trend-source-page",t),sessionStorage.setItem("trend-source-state",JSON.stringify({page:st,scrollY:window.scrollY})),st="product-trend",sessionStorage.setItem("trend-ecom-code",r),bt.forEach(e=>e("product-trend"))};window.ecomagentNavigateToSourcing=r=>{st="sourcing",r?sessionStorage.setItem("sourcing-ecom-code",r):sessionStorage.removeItem("sourcing-ecom-code"),bt.forEach(t=>t("sourcing"))};window.ecomagentNavigateDirectToSourcing=()=>{sessionStorage.removeItem("sourcing-ecom-code"),st="sourcing",bt.forEach(r=>r("sourcing"))};let gt=class extends b{constructor(){super();d(this,"_page",st);d(this,"_trendCode","");d(this,"_sourcingCode","");bt.add(t=>{this._page=t,t==="product-trend"&&(this._trendCode=sessionStorage.getItem("trend-ecom-code")||""),t==="sourcing"&&(this._sourcingCode=sessionStorage.getItem("sourcing-ecom-code")||""),this.requestUpdate()})}connectedCallback(){super.connectedCallback();const t=localStorage.getItem("theme")||"dark";document.body.setAttribute("data-theme-mode",t)}_renderPage(){switch(this._page){case"dashboard":return i`<ea-dashboard></ea-dashboard>`;case"settings":return i`<ea-settings></ea-settings>`;case"product-master":return i`<ea-product-master></ea-product-master>`;case"tracking":return i`<ea-tracking></ea-tracking>`;case"cross-platform":return i`<ea-cross-platform></ea-cross-platform>`;case"today-top":return i`<ea-today-top></ea-today-top>`;case"raw-data":return i`<ea-raw-data></ea-raw-data>`;case"export":return i`<ea-export></ea-export>`;case"product-trend":return i`<ea-product-trend-page ecomCode=${this._trendCode}></ea-product-trend-page>`;case"sourcing":return i`<ea-sourcing ecomCode=${this._sourcingCode}></ea-sourcing>`;case"translation-logs":return i`<ea-translation-logs></ea-translation-logs>`;case"assets":return i`<ea-assets-page ecomCode=${this._sourcingCode}></ea-assets-page>`;default:return i`<div style="padding:24px;color:var(--muted)">未知页面</div>`}}render(){return this._page==="product-trend"?i`
        <ea-layout currentPage=${this._page}>
          <div style="padding:24px">${this._renderPage()}</div>
        </ea-layout>
      `:i`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `}};Go(gt,"styles",f`:host { display: block; min-height: 100vh; }`);jt([l()],gt.prototype,"_page",2);jt([l()],gt.prototype,"_trendCode",2);jt([l()],gt.prototype,"_sourcingCode",2);gt=jt([x("ecomagent-app")],gt);console.log("EcomAgent UI loaded");

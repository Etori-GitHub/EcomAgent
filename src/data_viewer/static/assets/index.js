var Ae=Object.defineProperty;var Ee=(o,t,e)=>t in o?Ae(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e;var d=(o,t,e)=>Ee(o,typeof t!="symbol"?t+"":t,e);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const a of document.querySelectorAll('link[rel="modulepreload"]'))r(a);new MutationObserver(a=>{for(const i of a)if(i.type==="childList")for(const s of i.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&r(s)}).observe(document,{childList:!0,subtree:!0});function e(a){const i={};return a.integrity&&(i.integrity=a.integrity),a.referrerPolicy&&(i.referrerPolicy=a.referrerPolicy),a.crossOrigin==="use-credentials"?i.credentials="include":a.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function r(a){if(a.ep)return;a.ep=!0;const i=e(a);fetch(a.href,i)}})();/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const vt=globalThis,Dt=vt.ShadowRoot&&(vt.ShadyCSS===void 0||vt.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Mt=Symbol(),Rt=new WeakMap;let ee=class{constructor(t,e,r){if(this._$cssResult$=!0,r!==Mt)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(Dt&&t===void 0){const r=e!==void 0&&e.length===1;r&&(t=Rt.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),r&&Rt.set(e,t))}return t}toString(){return this.cssText}};const Oe=o=>new ee(typeof o=="string"?o:o+"",void 0,Mt),w=(o,...t)=>{const e=o.length===1?o[0]:t.reduce((r,a,i)=>r+(s=>{if(s._$cssResult$===!0)return s.cssText;if(typeof s=="number")return s;throw Error("Value passed to 'css' function must be a 'css' function result: "+s+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(a)+o[i+1],o[0]);return new ee(e,o,Mt)},Te=(o,t)=>{if(Dt)o.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const e of t){const r=document.createElement("style"),a=vt.litNonce;a!==void 0&&r.setAttribute("nonce",a),r.textContent=e.cssText,o.appendChild(r)}},Ht=Dt?o=>o:o=>o instanceof CSSStyleSheet?(t=>{let e="";for(const r of t.cssRules)e+=r.cssText;return Oe(e)})(o):o;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const{is:De,defineProperty:Me,getOwnPropertyDescriptor:Ie,getOwnPropertyNames:je,getOwnPropertySymbols:Ne,getPrototypeOf:Ue}=Object,j=globalThis,Bt=j.trustedTypes,Le=Bt?Bt.emptyScript:"",Ct=j.reactiveElementPolyfillSupport,ot=(o,t)=>o,bt={toAttribute(o,t){switch(t){case Boolean:o=o?Le:null;break;case Object:case Array:o=o==null?o:JSON.stringify(o)}return o},fromAttribute(o,t){let e=o;switch(t){case Boolean:e=o!==null;break;case Number:e=o===null?null:Number(o);break;case Object:case Array:try{e=JSON.parse(o)}catch{e=null}}return e}},It=(o,t)=>!De(o,t),Vt={attribute:!0,type:String,converter:bt,reflect:!1,useDefault:!1,hasChanged:It};Symbol.metadata??(Symbol.metadata=Symbol("metadata")),j.litPropertyMetadata??(j.litPropertyMetadata=new WeakMap);let K=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??(this.l=[])).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Vt){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const r=Symbol(),a=this.getPropertyDescriptor(t,r,e);a!==void 0&&Me(this.prototype,t,a)}}static getPropertyDescriptor(t,e,r){const{get:a,set:i}=Ie(this.prototype,t)??{get(){return this[e]},set(s){this[e]=s}};return{get:a,set(s){const p=a==null?void 0:a.call(this);i==null||i.call(this,s),this.requestUpdate(t,p,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Vt}static _$Ei(){if(this.hasOwnProperty(ot("elementProperties")))return;const t=Ue(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(ot("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(ot("properties"))){const e=this.properties,r=[...je(e),...Ne(e)];for(const a of r)this.createProperty(a,e[a])}const t=this[Symbol.metadata];if(t!==null){const e=litPropertyMetadata.get(t);if(e!==void 0)for(const[r,a]of e)this.elementProperties.set(r,a)}this._$Eh=new Map;for(const[e,r]of this.elementProperties){const a=this._$Eu(e,r);a!==void 0&&this._$Eh.set(a,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const r=new Set(t.flat(1/0).reverse());for(const a of r)e.unshift(Ht(a))}else t!==void 0&&e.push(Ht(t));return e}static _$Eu(t,e){const r=e.attribute;return r===!1?void 0:typeof r=="string"?r:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){var t;this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),(t=this.constructor.l)==null||t.forEach(e=>e(this))}addController(t){var e;(this._$EO??(this._$EO=new Set)).add(t),this.renderRoot!==void 0&&this.isConnected&&((e=t.hostConnected)==null||e.call(t))}removeController(t){var e;(e=this._$EO)==null||e.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const r of e.keys())this.hasOwnProperty(r)&&(t.set(r,this[r]),delete this[r]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Te(t,this.constructor.elementStyles),t}connectedCallback(){var t;this.renderRoot??(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(t=this._$EO)==null||t.forEach(e=>{var r;return(r=e.hostConnected)==null?void 0:r.call(e)})}enableUpdating(t){}disconnectedCallback(){var t;(t=this._$EO)==null||t.forEach(e=>{var r;return(r=e.hostDisconnected)==null?void 0:r.call(e)})}attributeChangedCallback(t,e,r){this._$AK(t,r)}_$ET(t,e){var i;const r=this.constructor.elementProperties.get(t),a=this.constructor._$Eu(t,r);if(a!==void 0&&r.reflect===!0){const s=(((i=r.converter)==null?void 0:i.toAttribute)!==void 0?r.converter:bt).toAttribute(e,r.type);this._$Em=t,s==null?this.removeAttribute(a):this.setAttribute(a,s),this._$Em=null}}_$AK(t,e){var i,s;const r=this.constructor,a=r._$Eh.get(t);if(a!==void 0&&this._$Em!==a){const p=r.getPropertyOptions(a),c=typeof p.converter=="function"?{fromAttribute:p.converter}:((i=p.converter)==null?void 0:i.fromAttribute)!==void 0?p.converter:bt;this._$Em=a;const h=c.fromAttribute(e,p.type);this[a]=h??((s=this._$Ej)==null?void 0:s.get(a))??h,this._$Em=null}}requestUpdate(t,e,r,a=!1,i){var s;if(t!==void 0){const p=this.constructor;if(a===!1&&(i=this[t]),r??(r=p.getPropertyOptions(t)),!((r.hasChanged??It)(i,e)||r.useDefault&&r.reflect&&i===((s=this._$Ej)==null?void 0:s.get(t))&&!this.hasAttribute(p._$Eu(t,r))))return;this.C(t,e,r)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:r,reflect:a,wrapped:i},s){r&&!(this._$Ej??(this._$Ej=new Map)).has(t)&&(this._$Ej.set(t,s??e??this[t]),i!==!0||s!==void 0)||(this._$AL.has(t)||(this.hasUpdated||r||(e=void 0),this._$AL.set(t,e)),a===!0&&this._$Em!==t&&(this._$Eq??(this._$Eq=new Set)).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var r;if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??(this.renderRoot=this.createRenderRoot()),this._$Ep){for(const[i,s]of this._$Ep)this[i]=s;this._$Ep=void 0}const a=this.constructor.elementProperties;if(a.size>0)for(const[i,s]of a){const{wrapped:p}=s,c=this[i];p!==!0||this._$AL.has(i)||c===void 0||this.C(i,void 0,s,c)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),(r=this._$EO)==null||r.forEach(a=>{var i;return(i=a.hostUpdate)==null?void 0:i.call(a)}),this.update(e)):this._$EM()}catch(a){throw t=!1,this._$EM(),a}t&&this._$AE(e)}willUpdate(t){}_$AE(t){var e;(e=this._$EO)==null||e.forEach(r=>{var a;return(a=r.hostUpdated)==null?void 0:a.call(r)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&(this._$Eq=this._$Eq.forEach(e=>this._$ET(e,this[e]))),this._$EM()}updated(t){}firstUpdated(t){}};K.elementStyles=[],K.shadowRootOptions={mode:"open"},K[ot("elementProperties")]=new Map,K[ot("finalized")]=new Map,Ct==null||Ct({ReactiveElement:K}),(j.reactiveElementVersions??(j.reactiveElementVersions=[])).push("2.1.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const it=globalThis,qt=o=>o,ft=it.trustedTypes,Gt=ft?ft.createPolicy("lit-html",{createHTML:o=>o}):void 0,re="$lit$",I=`lit$${Math.random().toFixed(9).slice(2)}$`,ae="?"+I,Fe=`<${ae}>`,q=document,st=()=>q.createComment(""),nt=o=>o===null||typeof o!="object"&&typeof o!="function",jt=Array.isArray,Re=o=>jt(o)||typeof(o==null?void 0:o[Symbol.iterator])=="function",zt=`[ 	
\f\r]`,at=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Jt=/-->/g,Wt=/>/g,H=RegExp(`>|${zt}(?:([^\\s"'>=/]+)(${zt}*=${zt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Yt=/'/g,Kt=/"/g,oe=/^(?:script|style|textarea|title)$/i,He=o=>(t,...e)=>({_$litType$:o,strings:t,values:e}),n=He(1),G=Symbol.for("lit-noChange"),f=Symbol.for("lit-nothing"),Xt=new WeakMap,B=q.createTreeWalker(q,129);function ie(o,t){if(!jt(o)||!o.hasOwnProperty("raw"))throw Error("invalid template strings array");return Gt!==void 0?Gt.createHTML(t):t}const Be=(o,t)=>{const e=o.length-1,r=[];let a,i=t===2?"<svg>":t===3?"<math>":"",s=at;for(let p=0;p<e;p++){const c=o[p];let h,b,u=-1,g=0;for(;g<c.length&&(s.lastIndex=g,b=s.exec(c),b!==null);)g=s.lastIndex,s===at?b[1]==="!--"?s=Jt:b[1]!==void 0?s=Wt:b[2]!==void 0?(oe.test(b[2])&&(a=RegExp("</"+b[2],"g")),s=H):b[3]!==void 0&&(s=H):s===H?b[0]===">"?(s=a??at,u=-1):b[1]===void 0?u=-2:(u=s.lastIndex-b[2].length,h=b[1],s=b[3]===void 0?H:b[3]==='"'?Kt:Yt):s===Kt||s===Yt?s=H:s===Jt||s===Wt?s=at:(s=H,a=void 0);const x=s===H&&o[p+1].startsWith("/>")?" ":"";i+=s===at?c+Fe:u>=0?(r.push(h),c.slice(0,u)+re+c.slice(u)+I+x):c+I+(u===-2?p:x)}return[ie(o,i+(o[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),r]};class dt{constructor({strings:t,_$litType$:e},r){let a;this.parts=[];let i=0,s=0;const p=t.length-1,c=this.parts,[h,b]=Be(t,e);if(this.el=dt.createElement(h,r),B.currentNode=this.el.content,e===2||e===3){const u=this.el.content.firstChild;u.replaceWith(...u.childNodes)}for(;(a=B.nextNode())!==null&&c.length<p;){if(a.nodeType===1){if(a.hasAttributes())for(const u of a.getAttributeNames())if(u.endsWith(re)){const g=b[s++],x=a.getAttribute(u).split(I),E=/([.?@])?(.*)/.exec(g);c.push({type:1,index:i,name:E[2],strings:x,ctor:E[1]==="."?qe:E[1]==="?"?Ge:E[1]==="@"?Je:$t}),a.removeAttribute(u)}else u.startsWith(I)&&(c.push({type:6,index:i}),a.removeAttribute(u));if(oe.test(a.tagName)){const u=a.textContent.split(I),g=u.length-1;if(g>0){a.textContent=ft?ft.emptyScript:"";for(let x=0;x<g;x++)a.append(u[x],st()),B.nextNode(),c.push({type:2,index:++i});a.append(u[g],st())}}}else if(a.nodeType===8)if(a.data===ae)c.push({type:2,index:i});else{let u=-1;for(;(u=a.data.indexOf(I,u+1))!==-1;)c.push({type:7,index:i}),u+=I.length-1}i++}}static createElement(t,e){const r=q.createElement("template");return r.innerHTML=t,r}}function X(o,t,e=o,r){var s,p;if(t===G)return t;let a=r!==void 0?(s=e._$Co)==null?void 0:s[r]:e._$Cl;const i=nt(t)?void 0:t._$litDirective$;return(a==null?void 0:a.constructor)!==i&&((p=a==null?void 0:a._$AO)==null||p.call(a,!1),i===void 0?a=void 0:(a=new i(o),a._$AT(o,e,r)),r!==void 0?(e._$Co??(e._$Co=[]))[r]=a:e._$Cl=a),a!==void 0&&(t=X(o,a._$AS(o,t.values),a,r)),t}class Ve{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:r}=this._$AD,a=((t==null?void 0:t.creationScope)??q).importNode(e,!0);B.currentNode=a;let i=B.nextNode(),s=0,p=0,c=r[0];for(;c!==void 0;){if(s===c.index){let h;c.type===2?h=new ut(i,i.nextSibling,this,t):c.type===1?h=new c.ctor(i,c.name,c.strings,this,t):c.type===6&&(h=new We(i,this,t)),this._$AV.push(h),c=r[++p]}s!==(c==null?void 0:c.index)&&(i=B.nextNode(),s++)}return B.currentNode=q,a}p(t){let e=0;for(const r of this._$AV)r!==void 0&&(r.strings!==void 0?(r._$AI(t,r,e),e+=r.strings.length-2):r._$AI(t[e])),e++}}class ut{get _$AU(){var t;return((t=this._$AM)==null?void 0:t._$AU)??this._$Cv}constructor(t,e,r,a){this.type=2,this._$AH=f,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=r,this.options=a,this._$Cv=(a==null?void 0:a.isConnected)??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return e!==void 0&&(t==null?void 0:t.nodeType)===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=X(this,t,e),nt(t)?t===f||t==null||t===""?(this._$AH!==f&&this._$AR(),this._$AH=f):t!==this._$AH&&t!==G&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Re(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==f&&nt(this._$AH)?this._$AA.nextSibling.data=t:this.T(q.createTextNode(t)),this._$AH=t}$(t){var i;const{values:e,_$litType$:r}=t,a=typeof r=="number"?this._$AC(t):(r.el===void 0&&(r.el=dt.createElement(ie(r.h,r.h[0]),this.options)),r);if(((i=this._$AH)==null?void 0:i._$AD)===a)this._$AH.p(e);else{const s=new Ve(a,this),p=s.u(this.options);s.p(e),this.T(p),this._$AH=s}}_$AC(t){let e=Xt.get(t.strings);return e===void 0&&Xt.set(t.strings,e=new dt(t)),e}k(t){jt(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let r,a=0;for(const i of t)a===e.length?e.push(r=new ut(this.O(st()),this.O(st()),this,this.options)):r=e[a],r._$AI(i),a++;a<e.length&&(this._$AR(r&&r._$AB.nextSibling,a),e.length=a)}_$AR(t=this._$AA.nextSibling,e){var r;for((r=this._$AP)==null?void 0:r.call(this,!1,!0,e);t!==this._$AB;){const a=qt(t).nextSibling;qt(t).remove(),t=a}}setConnected(t){var e;this._$AM===void 0&&(this._$Cv=t,(e=this._$AP)==null||e.call(this,t))}}class $t{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,r,a,i){this.type=1,this._$AH=f,this._$AN=void 0,this.element=t,this.name=e,this._$AM=a,this.options=i,r.length>2||r[0]!==""||r[1]!==""?(this._$AH=Array(r.length-1).fill(new String),this.strings=r):this._$AH=f}_$AI(t,e=this,r,a){const i=this.strings;let s=!1;if(i===void 0)t=X(this,t,e,0),s=!nt(t)||t!==this._$AH&&t!==G,s&&(this._$AH=t);else{const p=t;let c,h;for(t=i[0],c=0;c<i.length-1;c++)h=X(this,p[r+c],e,c),h===G&&(h=this._$AH[c]),s||(s=!nt(h)||h!==this._$AH[c]),h===f?t=f:t!==f&&(t+=(h??"")+i[c+1]),this._$AH[c]=h}s&&!a&&this.j(t)}j(t){t===f?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class qe extends $t{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===f?void 0:t}}class Ge extends $t{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==f)}}class Je extends $t{constructor(t,e,r,a,i){super(t,e,r,a,i),this.type=5}_$AI(t,e=this){if((t=X(this,t,e,0)??f)===G)return;const r=this._$AH,a=t===f&&r!==f||t.capture!==r.capture||t.once!==r.once||t.passive!==r.passive,i=t!==f&&(r===f||a);a&&this.element.removeEventListener(this.name,this,r),i&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e;typeof this._$AH=="function"?this._$AH.call(((e=this.options)==null?void 0:e.host)??this.element,t):this._$AH.handleEvent(t)}}class We{constructor(t,e,r){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=r}get _$AU(){return this._$AM._$AU}_$AI(t){X(this,t)}}const At=it.litHtmlPolyfillSupport;At==null||At(dt,ut),(it.litHtmlVersions??(it.litHtmlVersions=[])).push("3.3.2");const Ye=(o,t,e)=>{const r=(e==null?void 0:e.renderBefore)??t;let a=r._$litPart$;if(a===void 0){const i=(e==null?void 0:e.renderBefore)??null;r._$litPart$=a=new ut(t.insertBefore(st(),i),i,void 0,e??{})}return a._$AI(o),a};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const V=globalThis;let m=class extends K{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e;const t=super.createRenderRoot();return(e=this.renderOptions).renderBefore??(e.renderBefore=t.firstChild),t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=Ye(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),(t=this._$Do)==null||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),(t=this._$Do)==null||t.setConnected(!1)}render(){return G}};var te;m._$litElement$=!0,m.finalized=!0,(te=V.litElementHydrateSupport)==null||te.call(V,{LitElement:m});const Et=V.litElementPolyfillSupport;Et==null||Et({LitElement:m});(V.litElementVersions??(V.litElementVersions=[])).push("4.2.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const k=o=>(t,e)=>{e!==void 0?e.addInitializer(()=>{customElements.define(o,t)}):customElements.define(o,t)};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const Ke={attribute:!0,type:String,converter:bt,reflect:!1,hasChanged:It},Xe=(o=Ke,t,e)=>{const{kind:r,metadata:a}=e;let i=globalThis.litPropertyMetadata.get(a);if(i===void 0&&globalThis.litPropertyMetadata.set(a,i=new Map),r==="setter"&&((o=Object.create(o)).wrapped=!0),i.set(e.name,o),r==="accessor"){const{name:s}=e;return{set(p){const c=t.get.call(this);t.set.call(this,p),this.requestUpdate(s,c,o,!0,p)},init(p){return p!==void 0&&this.C(s,void 0,o,p),p}}}if(r==="setter"){const{name:s}=e;return function(p){const c=this[s];t.call(this,p),this.requestUpdate(s,c,o,!0,p)}}throw Error("Unsupported decorator location: "+r)};function A(o){return(t,e)=>typeof e=="object"?Xe(o,t,e):((r,a,i)=>{const s=a.hasOwnProperty(i);return a.constructor.createProperty(i,r),s?Object.getOwnPropertyDescriptor(a,i):void 0})(o,t,e)}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function l(o){return A({...o,state:!0,attribute:!1})}var se=Object.defineProperty,Ze=Object.getOwnPropertyDescriptor,Qe=(o,t,e)=>t in o?se(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,ne=(o,t,e,r)=>{for(var a=r>1?void 0:r?Ze(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&se(t,e,a),a},tr=(o,t,e)=>Qe(o,t+"",e);const er=[{group:"Main",items:[{id:"dashboard",icon:"grid",label:"数据概览"},{id:"product-master",icon:"box",label:"商品总库"},{id:"tracking",icon:"target",label:"商品追踪"},{id:"cross-platform",icon:"sync",label:"跨平台分析"}]},{group:"平台数据",items:[{id:"today-top",icon:"star",label:"今日TOP榜"},{id:"raw-data",icon:"database",label:"原始数据"}]},{group:"配置",items:[{id:"export",icon:"download",label:"数据导出"},{id:"settings",icon:"settings",label:"系统设置"}]}],rr={grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',box:'<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',target:'<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',sync:'<path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/>',star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',database:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',settings:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>'};let mt=class extends m{constructor(){super();d(this,"collapsed",!1);d(this,"_currentPage","dashboard");window.ecomagentOnPageChange&&window.ecomagentOnPageChange(t=>{this._currentPage=t,this.requestUpdate()}),window.ecomagentGetCurrentPage&&(this._currentPage=window.ecomagentGetCurrentPage())}_onNavClick(t){window.ecomagentNavigate&&window.ecomagentNavigate(t)}_onToggle(){this.collapsed=!this.collapsed,this.requestUpdate("collapsed")}render(){const t=this._currentPage;return n`
      <div class="header">
        <div class="brand">
          <div class="logo">E</div>
          <div class="brand-text">
            <span class="brand-title">EcomAgent</span>
            <span class="brand-subtitle">数据可视化平台</span>
          </div>
        </div>
        <button class="toggle-btn" @click=${this._onToggle}>
          <svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
      </div>
      <div class="nav-content">
        ${er.map(e=>n`
          <div class="nav-group">
            <div class="nav-group-header"><span class="nav-group-title">${e.group}</span></div>
            <ul class="nav-items">
              ${e.items.map(r=>n`
                <li class="nav-item ${t===r.id?"active":""}" @click=${()=>this._onNavClick(r.id)}>
                  <svg class="nav-icon" viewBox="0 0 24 24">${rr[r.icon]}</svg>
                  <span class="nav-label">${r.label}</span>
                </li>
              `)}
            </ul>
          </div>
        `)}
      </div>
    `}};tr(mt,"styles",w`
    :host { width: 258px; background: var(--panel); color: var(--text); padding: 14px 10px 12px; flex-shrink: 0; border-right: 1px solid var(--border); transition: width 0.2s ease; overflow: hidden; display: flex; flex-direction: column; }
    :host([collapsed]) { width: 60px; }
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
    :host([collapsed]) .nav-item { justify-content: center; padding: 8px; }
    .nav-icon { width: 18px; height: 18px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; }
    :host([collapsed]) .nav-label { display: none; }
  `);ne([A({type:Boolean,reflect:!0})],mt.prototype,"collapsed",2);mt=ne([k("ea-sidebar")],mt);var de=Object.defineProperty,ar=Object.getOwnPropertyDescriptor,or=(o,t,e)=>t in o?de(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,le=(o,t,e,r)=>{for(var a=r>1?void 0:r?ar(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&de(t,e,a),a},ir=(o,t,e)=>or(o,t+"",e);const sr={dashboard:{title:"数据概览",subtitle:"查看数据统计和概览"},"product-master":{title:"商品总库",subtitle:"统一管理所有平台商品"},tracking:{title:"商品追踪",subtitle:"追踪特定商品的价格、销量变化"},"cross-platform":{title:"跨平台分析",subtitle:"对比分析不同平台数据"},"today-top":{title:"今日TOP榜",subtitle:"各平台热销产品排行"},"raw-data":{title:"原始数据",subtitle:"查看和搜索原始数据"},export:{title:"数据导出",subtitle:"导出数据为 CSV 或 Excel"},settings:{title:"系统设置",subtitle:"配置数据源和其他选项"},"product-trend":{title:"商品趋势",subtitle:"查看商品各维度数据随时间变化"}};let xt=class extends m{constructor(){super(...arguments);d(this,"currentPage","dashboard")}toggleTheme(){const t=document.body,r=t.getAttribute("data-theme-mode")==="dark"?"light":"dark";t.setAttribute("data-theme-mode",r),localStorage.setItem("theme",r),this.requestUpdate()}render(){const{title:t,subtitle:e}=sr[this.currentPage],r=document.body.getAttribute("data-theme-mode")!=="light";return n`
      <div>
        <div class="title">${t}</div>
        <div class="subtitle">${e}</div>
      </div>
      
      <div class="actions">
        <button class="icon-btn" @click=${this.toggleTheme} title="切换主题">
          ${r?n`
            <svg viewBox="0 0 24 24">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          `:n`
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
    `}};ir(xt,"styles",w`
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
  `);le([A({type:String})],xt.prototype,"currentPage",2);xt=le([k("ea-header")],xt);var ce=Object.defineProperty,nr=Object.getOwnPropertyDescriptor,dr=(o,t,e)=>t in o?ce(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Nt=(o,t,e,r)=>{for(var a=r>1?void 0:r?nr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&ce(t,e,a),a},lr=(o,t,e)=>dr(o,t+"",e);let lt=class extends m{constructor(){super(...arguments);d(this,"currentPage","dashboard");d(this,"sidebarCollapsed",!1)}render(){return n`
      <ea-sidebar ?collapsed=${this.sidebarCollapsed}></ea-sidebar>
      <main class="main-content">
        <ea-header .currentPage=${this.currentPage}></ea-header>
        <div class="content-body"><slot></slot></div>
      </main>
    `}};lr(lt,"styles",w`
    :host { display: flex; min-height: 100vh; }
    .main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
    .content-body { animation: fadeIn 0.3s ease; }
    @media (max-width: 1024px) { :host { flex-direction: column; } .main-content { padding: 16px; } }
  `);Nt([A({type:String})],lt.prototype,"currentPage",2);Nt([l()],lt.prototype,"sidebarCollapsed",2);lt=Nt([k("ea-layout")],lt);const $="/api";async function _(o,t){const e=await fetch(o,t);if(!e.ok){const r=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(r.detail||`HTTP ${e.status}`)}return e.json()}async function cr(){return _(`${$}/stats`)}async function pr(o){return _(`${$}/categories`)}async function hr(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,r])=>[e,String(r)]));return _(`${$}/product-master?${t}`)}async function pe(o,t=7){return _(`${$}/sales-trend/${o}?days=${t}`)}async function ur(o){return _(`${$}/tracked-products?ids=${o.join(",")}`)}async function gr(){return _(`${$}/config/list`)}async function vr(o){return _(`${$}/config/${o}`)}async function br(o,t){return _(`${$}/config/${o}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:t})})}async function Zt(){return _(`${$}/config/backups/list`)}async function fr(o){return _(`${$}/config/backups/${o}/restore`,{method:"POST"})}async function mr(o){return _(`${$}/config/backups/${o}`,{method:"DELETE"})}async function xr(o,t=7){return _(`${$}/product-trend/${o}?days=${t}`)}async function yr(){return _(`${$}/amazon/top-by-category`)}async function $r(){return _(`${$}/tiktok/top-by-category`)}async function _r(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,r])=>[e,String(r)]));return _(`${$}/amazon/products?${t}`)}async function wr(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,r])=>[e,String(r)]));return _(`${$}/tiktok/products?${t}`)}async function kr(){return _(`${$}/cross-platform-analysis`)}var he=Object.defineProperty,Pr=Object.getOwnPropertyDescriptor,Sr=(o,t,e)=>t in o?he(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,F=(o,t,e,r)=>{for(var a=r>1?void 0:r?Pr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&he(t,e,a),a},ue=(o,t,e)=>Sr(o,t+"",e);let yt=class extends m{constructor(){super(...arguments);d(this,"padding",16)}render(){return n`
      <slot name="header"></slot>
      <div class="card-content" style="--padding: ${this.padding}px">
        <slot></slot>
      </div>
    `}};ue(yt,"styles",w`
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
  `);F([A({type:Number})],yt.prototype,"padding",2);yt=F([k("ea-card")],yt);let N=class extends m{constructor(){super(...arguments);d(this,"label","");d(this,"value","-");d(this,"icon","");d(this,"desc","");d(this,"color","")}render(){return n`
      <div class="stat-header">
        <div>
          <div class="stat-label">${this.label}</div>
          <div class="stat-value ${this.color}">${this.value}</div>
          ${this.desc?n`<div class="stat-desc">${this.desc}</div>`:""}
        </div>
        ${this.icon?n`<span class="stat-icon">${this.icon}</span>`:""}
      </div>
      <slot></slot>
    `}};ue(N,"styles",w`
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
  `);F([A({type:String})],N.prototype,"label",2);F([A({type:String})],N.prototype,"value",2);F([A({type:String})],N.prototype,"icon",2);F([A({type:String})],N.prototype,"desc",2);F([A({type:String})],N.prototype,"color",2);N=F([k("ea-stat-card")],N);var ge=Object.defineProperty,Cr=Object.getOwnPropertyDescriptor,zr=(o,t,e)=>t in o?ge(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,gt=(o,t,e,r)=>{for(var a=r>1?void 0:r?Cr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&ge(t,e,a),a},Ar=(o,t,e)=>zr(o,t+"",e);let J=class extends m{constructor(){super(...arguments);d(this,"stats",null);d(this,"loading",!0);d(this,"error","");d(this,"updating",null)}connectedCallback(){super.connectedCallback(),this.loadStats()}async loadStats(){this.loading=!0,this.error="";try{this.stats=await cr()}catch(t){this.error=t instanceof Error?t.message:String(t)}finally{this.loading=!1,this.requestUpdate()}}async _updatePlatform(t){this.updating=t;try{console.log(`开始抓取 ${t} 数据...`),await new Promise(e=>setTimeout(e,2e3)),alert(`${t} 数据抓取完成`),await this.loadStats()}catch(e){alert(`抓取失败: ${e}`)}finally{this.updating=null}}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;if(this.error)return n`
        <div class="error-box">
          <p>加载失败: ${this.error}</p>
          <button class="retry-btn" @click=${this.loadStats}>重试</button>
        </div>
      `;if(!this.stats)return n`<div class="error-box"><p>无数据</p></div>`;const{amazon:t,tiktok:e,product_master:r}=this.stats;return n`
      <h2>数据概览</h2>

      <h3>平台数据</h3>
      <div class="stats-grid">
        <ea-stat-card
          label="Amazon"
          .value=${t.products.toLocaleString()}
          icon="📦"
          desc="商品总数"
          color="accent"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-end;">
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${t.sales.toLocaleString()}<br>
              今日新增: ${t.today.toLocaleString()}
            </div>
            <button 
              class="update-btn amazon"
              ?disabled=${this.updating==="amazon"}
              @click=${()=>this._updatePlatform("amazon")}
            >${this.updating==="amazon"?"更新中...":"更新数据"}</button>
          </div>
        </ea-stat-card>

        <ea-stat-card
          label="TikTok"
          .value=${e.products.toLocaleString()}
          icon="🎵"
          desc="商品总数"
          color="info"
        >
          <div style="display:flex;justify-content:space-between;align-items:flex-end;">
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${e.sales.toLocaleString()}<br>
              今日新增: ${e.today.toLocaleString()}
            </div>
            <button 
              class="update-btn tiktok"
              ?disabled=${this.updating==="tiktok"}
              @click=${()=>this._updatePlatform("tiktok")}
            >${this.updating==="tiktok"?"更新中...":"更新数据"}</button>
          </div>
        </ea-stat-card>
      </div>

      <h3>商品总库</h3>
      <div class="master-grid">
        <ea-stat-card label="总商品数" .value=${r.total.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="Amazon" .value=${r.amazon.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="TikTok" .value=${r.tiktok.toLocaleString()} color="info"></ea-stat-card>
        <ea-stat-card label="今日新增" .value=${r.today.toLocaleString()} color="ok"></ea-stat-card>
      </div>
    `}};Ar(J,"styles",w`
    :host { display: block; }
    h2 { font-size: 20px; font-weight: 700; color: var(--text-strong); margin-bottom: 24px; }
    h3 { font-size: 16px; font-weight: 600; color: var(--text-strong); margin-bottom: 16px; }
    .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 32px; }
    .master-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
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
    .update-btn.amazon {
      background: var(--accent-subtle);
      color: var(--accent);
      border: 1px solid var(--accent);
    }
    .update-btn.amazon:hover { background: var(--accent); color: white; }
    .update-btn.tiktok {
      background: rgba(0, 242, 234, 0.1);
      color: #00f2ea;
      border: 1px solid #00f2ea;
    }
    .update-btn.tiktok:hover { background: #00f2ea; color: black; }
    .update-btn:disabled { opacity: 0.5; cursor: not-allowed; }
    @keyframes spin { to { transform: rotate(360deg); } }
    @media (max-width: 768px) { .stats-grid, .master-grid { grid-template-columns: 1fr; } }
  `);gt([l()],J.prototype,"stats",2);gt([l()],J.prototype,"loading",2);gt([l()],J.prototype,"error",2);gt([l()],J.prototype,"updating",2);J=gt([k("ea-dashboard")],J);var ve=Object.defineProperty,Er=Object.getOwnPropertyDescriptor,Or=(o,t,e)=>t in o?ve(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,W=(o,t,e,r)=>{for(var a=r>1?void 0:r?Er(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&ve(t,e,a),a},Tr=(o,t,e)=>Or(o,t+"",e);let T=class extends m{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"product",null);d(this,"trendData",[]);d(this,"loading",!0);d(this,"metric","rating");d(this,"days",7)}connectedCallback(){super.connectedCallback(),this.ecomCode&&this.loadTrendData()}updated(t){t.has("ecomCode")&&this.ecomCode&&this.loadTrendData()}async loadTrendData(){if(this.ecomCode){this.loading=!0;try{const t=await xr(this.ecomCode,this.days);this.product=t.product,this.trendData=t.trend||[]}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}}_onMetricChange(t){this.metric=t.target.value,this.requestUpdate()}_onDaysChange(t){const e=t.target.value;e!=="custom"&&(this.days=parseInt(e),this.loadTrendData())}_getMetricLabel(){switch(this.metric){case"price":return"价格";case"rating":return"评分";case"rank":return"排名"}}_renderChart(){if(this.trendData.length===0)return n`<div class="chart-empty">暂无数据</div>`;const t=this.trendData.map(i=>i[this.metric]).filter(i=>i!=null);if(t.length===0)return n`<div class="chart-empty">暂无${this._getMetricLabel()}数据</div>`;const e=Math.max(...t),r=Math.min(...t),a=e-r||1;return n`
      <div class="chart">
        ${this.trendData.map(i=>{const s=i[this.metric];if(s==null)return n`<div class="chart-bar" style="height:0"></div>`;const p=(s-r)/a*250+20;return n`
            <div class="chart-bar" style="height:${p}px">
              <span class="chart-bar-value">${this.metric==="rating"?s.toFixed(1):s}</span>
              <span class="chart-bar-label">${i.date.slice(5)}</span>
            </div>
          `})}
      </div>
    `}_renderTrend(t,e){if(t===null||e===null)return"-";const r=t-e;return Math.abs(r)<.01?"-":this.metric==="rank"?r<0?n`<span class="trend-up">↑${Math.abs(r).toFixed(0)}</span>`:n`<span class="trend-down">↓${Math.abs(r).toFixed(0)}</span>`:r>0?n`<span class="trend-up">↑${r.toFixed(2)}</span>`:n`<span class="trend-down">↓${Math.abs(r).toFixed(2)}</span>`}render(){return this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.product?n`
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
            ${this.trendData.map((t,e)=>{const r=e<this.trendData.length-1?this.trendData[e+1]:null;return n`
                <tr>
                  <td>${t.date}</td>
                  <td>${t.price!==null?`$${t.price.toFixed(2)}`:"-"}</td>
                  <td>${t.rating!==null?t.rating.toFixed(1):"-"}</td>
                  <td>${t.rank!==null?t.rank:"-"}</td>
                  <td>${r?this._renderTrend(t[this.metric],r[this.metric]):"-"}</td>
                </tr>
              `})}
          </tbody>
        </table>
      </div>
    `:n`
        <div class="header">
          <a class="back-link" href="javascript:history.back()">← 返回</a>
        </div>
        <div style="text-align:center;padding:48px;color:var(--muted)">商品不存在</div>
      `}};Tr(T,"styles",w`
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
  `);W([A({type:String})],T.prototype,"ecomCode",2);W([l()],T.prototype,"product",2);W([l()],T.prototype,"trendData",2);W([l()],T.prototype,"loading",2);W([l()],T.prototype,"metric",2);W([l()],T.prototype,"days",2);T=W([k("ea-product-trend")],T);var be=Object.defineProperty,Dr=Object.getOwnPropertyDescriptor,Mr=(o,t,e)=>t in o?be(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,P=(o,t,e,r)=>{for(var a=r>1?void 0:r?Dr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&be(t,e,a),a},Ir=(o,t,e)=>Mr(o,t+"",e);let y=class extends m{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"platform","amazon");d(this,"category","");d(this,"categories",{amazon:[],tiktok:[],all:[]});d(this,"sortBy","sales_count");d(this,"sortOrder","desc");d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map);d(this,"previewImg",{show:!1,src:"",x:0,y:0})}async connectedCallback(){super.connectedCallback(),this.loadTracked(),await this.loadCategories(),this.loadData()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t)))}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadCategories(){try{if(this.categories=await pr(),!this.category){const t=this.platform==="amazon"?this.categories.amazon:this.categories.tiktok;t.length>0&&(this.category=t[0])}}catch(t){console.error("Failed to load categories",t)}}async loadData(){this.loading=!0;try{const t=await hr({page:this.page,limit:20,search:this.search,platform:this.platform,category:this.category,sort_by:this.sortBy||void 0,sort_order:this.sortOrder});this.products=t.data,this.pages=t.pagination.pages,this.loadSparklines(t.data)}catch(t){console.error("Failed to load products",t)}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async r=>{try{const a=await pe(r.ecom_code,7);this.sparklines.set(r.ecom_code,a.trend)}catch{this.sparklines.set(r.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_onPlatformChange(t){this.platform=t;const e=t==="amazon"?this.categories.amazon:this.categories.tiktok;this.category=e.length>0?e[0]:"",this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onInputChange(t,e){this[e]=t.target.value}_onCategoryChange(t){this.category=t.target.value,this.page=1,this.loadData()}_onSort(t){this.sortBy===t?this.sortOrder=this.sortOrder==="desc"?"asc":"desc":(this.sortBy=t,this.sortOrder="desc"),this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_toggleTrack(t){this.trackedIds.has(t)?this.trackedIds.delete(t):this.trackedIds.add(t),this.saveTracked(),this.requestUpdate()}_showTrendPage(t){const e={platform:this.platform,category:this.category,search:this.search,sortBy:this.sortBy,sortOrder:this.sortOrder,page:this.page,scrollY:window.scrollY};sessionStorage.setItem("product-master-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"product-master")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_open1688(t){if(!t)return;const e=`https://s.1688.com/selloffer/offer_search.htm?keywords=${encodeURIComponent(t)}`;window.open(e,"_blank")}_showImgPreview(t,e){this.previewImg={show:!0,src:e,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement()}_hideImgPreview(){this.previewImg={...this.previewImg,show:!1},this._updatePreviewElement()}_moveImgPreview(t){this.previewImg.show&&(this.previewImg={...this.previewImg,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement())}_updatePreviewElement(){let t=document.getElementById("global-img-preview");t||(t=document.createElement("img"),t.id="global-img-preview",t.style.cssText="position:fixed;z-index:9999;max-width:400px;max-height:400px;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.5);pointer-events:none;border:1px solid rgba(255,255,255,0.1);",document.body.appendChild(t)),this.previewImg.show?(t.src=this.previewImg.src,t.style.left=this.previewImg.x+"px",t.style.top=this.previewImg.y+"px",t.style.display="block"):t.style.display="none"}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const r=e.map(g=>g.value).filter(g=>g!=null);if(r.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=Math.min(...r),s=Math.max(...r)-a||1,p=100,c=32,h=2,b=r.map((g,x)=>{const E=h+x/(r.length-1)*(p-h*2),et=c-h-(g-a)/s*(c-h*2);return`${E},${et}`}).join(" "),u=b+` ${h+(r.length-1)/(r.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return n`
      <div class="sparkline-container">
        <svg viewBox="0 0 ${p} ${c}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="grad-${t}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${u}" fill="url(#grad-${t})" />
          <polyline points="${b}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `}_renderSortHeader(t,e){const r=this.sortBy===e,a=r?this.sortOrder==="desc"?"▼":"▲":"⇅";return n`
      <th class="sortable ${r?"sorted":""}" @click=${()=>this._onSort(e)}>
        ${t} <span class="sort-icon">${a}</span>
      </th>
    `}_getCategoryOptions(){return this.platform==="amazon"?this.categories.amazon:this.platform==="tiktok"?this.categories.tiktok:[]}_renderPagination(){const t=[];let r=Math.max(1,this.page-Math.floor(2.5)),a=Math.min(this.pages,r+5-1);a-r<4&&(r=Math.max(1,a-5+1)),r>1&&(t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),r>2&&t.push(n`<span style="color:var(--muted)">...</span>`));for(let i=r;i<=a;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return a<this.pages&&(a<this.pages-1&&t.push(n`<span style="color:var(--muted)">...</span>`),t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>`)),n`<div class="pagination">${t}</div>`}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=this._getCategoryOptions();return n`
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
            ${t.map(e=>n`<option value=${e} ?selected=${this.category===e}>${e}</option>`)}
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
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((e,r)=>n`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${(this.page-1)*20+r+1}</td>
                <td>
                  ${e.local_image_path?n`<img class="product-img" src="/images/${e.local_image_path}" loading="lazy" 
                        @mouseenter=${a=>this._showImgPreview(a,`/images/${e.local_image_path}`)}
                        @mouseleave=${this._hideImgPreview}
                        @mousemove=${this._moveImgPreview} />`:n`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    ${e.product_url?n`<a class="product-name product-link" href=${e.product_url} target="_blank" title=${e.name}>${e.short_name||e.name||"无名称"}</a>`:n`<span class="product-name" title=${e.name}>${e.short_name||e.name||"无名称"}</span>`}
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
                <td>${e.rating?n`${e.rating.toFixed(1)} ⭐`:"-"}</td>
                <td><span class="sales-count">${this._formatSales(e.sales_count)}</span></td>
                <td class="sparkline-cell">${this._renderSparkline(e.ecom_code)}</td>
                <td>
                  <button class="action-btn" @click=${()=>this._showTrendPage(e.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${()=>window.open(e.product_url||"#","_blank")} title="查看详情">查看</button>
                  <button class="action-btn" @click=${()=>this._open1688(e.short_name||e.name)} title="1688搜索">1688</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pages>1?this._renderPagination():""}
      </div>
      
      <!-- 趋势模态框 -->
      ${this.showTrend?n`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${e=>e.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
      
      <!-- 图片预览浮框 -->
    `}};Ir(y,"styles",w`
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
    .product-name {
      font-size: 13px; font-weight: 500; color: var(--text);
      overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
      max-width: 200px; display: block;
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
  `);P([l()],y.prototype,"products",2);P([l()],y.prototype,"loading",2);P([l()],y.prototype,"page",2);P([l()],y.prototype,"pages",2);P([l()],y.prototype,"search",2);P([l()],y.prototype,"platform",2);P([l()],y.prototype,"category",2);P([l()],y.prototype,"categories",2);P([l()],y.prototype,"sortBy",2);P([l()],y.prototype,"sortOrder",2);P([l()],y.prototype,"trackedIds",2);P([l()],y.prototype,"showTrend",2);P([l()],y.prototype,"trendCode",2);P([l()],y.prototype,"sparklines",2);P([l()],y.prototype,"previewImg",2);y=P([k("ea-product-master")],y);var fe=Object.defineProperty,jr=Object.getOwnPropertyDescriptor,Nr=(o,t,e)=>t in o?fe(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Y=(o,t,e,r)=>{for(var a=r>1?void 0:r?jr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&fe(t,e,a),a},Ur=(o,t,e)=>Nr(o,t+"",e);let D=class extends m{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map)}connectedCallback(){super.connectedCallback(),this.loadTracked()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t))),this.loadData()}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadData(){if(this.loading=!0,this.trackedIds.size===0){this.products=[],this.loading=!1,this.requestUpdate();return}try{const t=await ur([...this.trackedIds]);this.products=t.products||[],this.loadSparklines(this.products)}catch(t){console.error("Load tracking error:",t),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async r=>{try{const a=await pe(r.ecom_code,7);this.sparklines.set(r.ecom_code,a.trend)}catch{this.sparklines.set(r.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_untrack(t){this.trackedIds.delete(t),this.saveTracked(),this.products=this.products.filter(e=>e.ecom_code!==t),this.requestUpdate()}_showTrendPage(t){const e={scrollY:window.scrollY};sessionStorage.setItem("tracking-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"tracking")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const r=e.map(g=>g.value).filter(g=>g!=null);if(r.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=Math.min(...r),s=Math.max(...r)-a||1,p=100,c=32,h=2,b=r.map((g,x)=>{const E=h+x/(r.length-1)*(p-h*2),et=c-h-(g-a)/s*(c-h*2);return`${E},${et}`}).join(" "),u=b+` ${h+(r.length-1)/(r.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return n`
      <div class="sparkline-container">
        <svg viewBox="0 0 ${p} ${c}" preserveAspectRatio="none">
          <defs>
            <linearGradient id="grad-track-${t}" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.15" />
              <stop offset="100%" stop-color="var(--accent)" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="${u}" fill="url(#grad-track-${t})" />
          <polyline points="${b}" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    `}render(){return this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.products.length===0?n`
        <div class="empty-state">
          <div class="empty-icon">🎯</div>
          <p>暂无追踪商品</p>
          <p style="font-size: 12px; margin-top: 8px;">请在商品总库中点击 ☆ 按钮添加</p>
        </div>
      `:n`
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
            ${this.products.map((t,e)=>n`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${e+1}</td>
                <td>
                  ${t.local_image_path?n`<img class="product-img" src="/images/${t.local_image_path}" loading="lazy" />`:n`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    ${t.product_url?n`<a class="product-name product-link" href=${t.product_url} target="_blank" title=${t.name}>${t.short_name||t.name||"无名称"}</a>`:n`<span class="product-name" title=${t.name}>${t.short_name||t.name||"无名称"}</span>`}
                  </div>
                </td>
                <td title=${t.category}>${t.category||"-"}</td>
                <td>${t.price?`$${t.price.toFixed(2)}`:"-"}</td>
                <td>${t.rating?n`${t.rating.toFixed(1)} ⭐`:"-"}</td>
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
      ${this.showTrend?n`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${t=>t.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
    `}};Ur(D,"styles",w`
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
  `);Y([l()],D.prototype,"products",2);Y([l()],D.prototype,"loading",2);Y([l()],D.prototype,"trackedIds",2);Y([l()],D.prototype,"showTrend",2);Y([l()],D.prototype,"trendCode",2);Y([l()],D.prototype,"sparklines",2);D=Y([k("ea-tracking")],D);var me=Object.defineProperty,Lr=Object.getOwnPropertyDescriptor,Fr=(o,t,e)=>t in o?me(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Q=(o,t,e,r)=>{for(var a=r>1?void 0:r?Lr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&me(t,e,a),a},Rr=(o,t,e)=>Fr(o,t+"",e);const Hr={google:"Google API Key",volcano:"火山引擎 API Key",xai:"xAI API Key",image_providers:"图片生成模型",default:"默认模型",available:"可用模型",flash_image:"Flash Image",model:"模型名称",aspect_ratios:"支持比例",resolutions:"支持分辨率",video_providers:"视频生成模型",grok:"Grok",max_duration:"最大时长(秒)",gemini:"Gemini 配置",temperature:"温度参数",max_output_tokens:"最大输出Token",triggers:"触发器列表",image:"生成图片",video:"生成视频",amazon:"亚马逊抓取",tiktok:"TikTok抓取",test:"测试模式",name:"名称",script:"脚本路径",keywords:"触发关键词",description:"描述",settings:"设置",cache_expire_minutes:"缓存过期时间(分钟)",case_sensitive:"区分大小写"},Br={api_keys:{title:"API 密钥",desc:"各平台 API 访问密钥",icon:"🔑"},models:{title:"模型配置",desc:"图片、视频生成模型参数",icon:"🤖"},triggers:{title:"触发器",desc:"命令关键词触发配置",icon:"⚡"}};let U=class extends m{constructor(){super(...arguments);d(this,"configs",[]);d(this,"backups",[]);d(this,"showBackups",!1);d(this,"loading",!0);d(this,"saving",null)}connectedCallback(){super.connectedCallback(),this.loadConfigs()}async loadConfigs(){this.loading=!0;try{const t=await gr(),e=await Zt(),r=[];for(const a of t.configs)if(!a.name.includes("template"))try{const i=await vr(a.name);r.push({name:a.name,filename:a.filename,data:i.data,modified:i.modified})}catch(i){console.error("Load config error:",a.name,i)}this.configs=r,this.backups=e.backups}catch(t){console.error("Failed to load configs:",t)}finally{this.loading=!1,this.requestUpdate()}}_getLabel(t){return Hr[t]||t}_getConfigInfo(t){return Br[t]||{title:t,desc:"",icon:"📄"}}_onFieldChange(t,e,r){const a=this.configs.find(i=>i.name===t);if(a){const i=e.split(".");let s=a.data;for(let p=0;p<i.length-1;p++)s=s[i[p]];s[i[i.length-1]]=r,this.requestUpdate()}}async _saveConfig(t){const e=this.configs.find(r=>r.name===t);if(e){this.saving=t;try{const r=JSON.stringify(e.data,null,2),a=await br(t,r);alert(`✅ 配置已保存
备份文件: `+a.backup),this.loadConfigs()}catch(r){alert("保存失败: "+(r instanceof Error?r.message:String(r)))}finally{this.saving=null}}}async _restoreBackup(t){if(confirm(`确定要还原备份 ${t} 吗？`))try{const e=await fr(t);alert(`✅ 已还原备份
原配置已备份为: ${e.pre_restore_backup}`),this.showBackups=!1,this.loadConfigs()}catch(e){alert("还原失败: "+(e instanceof Error?e.message:String(e)))}}async _deleteBackup(t){if(confirm(`确定要删除备份 ${t} 吗？`))try{await mr(t);const e=await Zt();this.backups=e.backups}catch(e){alert("删除失败: "+(e instanceof Error?e.message:String(e)))}}_renderSimpleFields(t){return n`
      <div class="field-list">
        ${Object.entries(t.data).map(([e,r])=>n`
          <div class="field-item">
            <div class="field-label">${this._getLabel(e)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input mono"
                .value=${String(r)}
                @change=${a=>this._onFieldChange(t.name,e,a.target.value)}
              >
            </div>
          </div>
        `)}
      </div>
    `}_renderSectionFields(t){return Object.entries(t.data).map(([e,r])=>typeof r!="object"||r===null?n`
          <div class="field-item">
            <div class="field-label">${this._getLabel(e)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input"
                .value=${String(r)}
                @change=${a=>this._onFieldChange(t.name,e,a.target.value)}
              >
            </div>
          </div>
        `:n`
        <div class="section">
          <div class="section-title">${this._getLabel(e)}</div>
          <div class="section-grid">
            ${this._renderSectionFieldsRecursive(t.name,e,r)}
          </div>
        </div>
      `)}_renderSectionFieldsRecursive(t,e,r){return Object.entries(r).map(([a,i])=>{const s=`${e}.${a}`;return typeof i=="object"&&i!==null&&!Array.isArray(i)?n`
          <div class="section">
            <div class="section-title">${this._getLabel(a)}</div>
            ${this._renderSectionFieldsRecursive(t,s,i)}
          </div>
        `:n`
        <div class="field-item">
          <div class="field-label">${this._getLabel(a)}</div>
          <div class="field-input">
            ${this._renderInput(t,s,i)}
          </div>
        </div>
      `})}_renderInput(t,e,r){return typeof r=="boolean"?n`
        <input 
          type="checkbox" 
          class="checkbox"
          .checked=${r}
          @change=${a=>this._onFieldChange(t,e,a.target.checked)}
        >
      `:Array.isArray(r)?n`
        <input 
          type="text" 
          class="input mono"
          .value=${JSON.stringify(r)}
          @change=${a=>{try{const i=JSON.parse(a.target.value);this._onFieldChange(t,e,i)}catch{}}}
        >
      `:n`
      <input 
        type="text" 
        class="input"
        .value=${String(r??"")}
        @change=${a=>this._onFieldChange(t,e,a.target.value)}
      >
    `}_renderConfigCard(t){const e=this._getConfigInfo(t.name),r=this.saving===t.name,a=t.name==="api_keys";return n`
      <div class="config-card">
        <div class="config-header">
          <div class="config-title-group">
            <div class="config-icon">${e.icon}</div>
            <div class="config-title-text">
              <h3>${e.title}</h3>
              <p>${e.desc}</p>
            </div>
          </div>
          <div class="config-actions">
            <button 
              class="btn btn-primary" 
              ?disabled=${r}
              @click=${()=>this._saveConfig(t.name)}
            >${r?"保存中...":"保存"}</button>
          </div>
        </div>
        
        <div class="config-body">
          ${a?this._renderSimpleFields(t):this._renderSectionFields(t)}
        </div>
        
        <div class="config-meta">
          <span>文件: ${t.filename}</span>
          <span>修改时间: ${t.modified?new Date(t.modified).toLocaleString("zh-CN"):"-"}</span>
        </div>
      </div>
    `}render(){return n`
      <h2>系统设置</h2>

      <div class="actions">
        <button class="btn btn-secondary" @click=${()=>this.loadConfigs()}>刷新配置</button>
        <button class="btn btn-secondary" @click=${()=>this.showBackups=!0}>查看备份</button>
      </div>

      ${this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.configs.map(t=>this._renderConfigCard(t))}

      ${this.showBackups?n`
        <div class="modal-overlay" @click=${()=>this.showBackups=!1}>
          <div class="modal" @click=${t=>t.stopPropagation()}>
            <div class="modal-header">
              <span class="modal-title">备份管理</span>
              <button class="modal-close" @click=${()=>this.showBackups=!1}>✕</button>
            </div>
            <div class="modal-body">
              ${this.backups.length===0?n`<div style="text-align:center;padding:24px;color:var(--muted)">暂无备份文件</div>`:this.backups.map(t=>n`
                  <div class="backup-item">
                    <div class="backup-info">
                      <div class="backup-name">${t.filename}</div>
                      <div class="backup-meta">
                        ${t.config_name} | ${new Date(t.created).toLocaleString("zh-CN")} | ${t.size} bytes
                      </div>
                    </div>
                    <div class="backup-actions">
                      <button class="action-btn restore" @click=${()=>this._restoreBackup(t.filename)}>还原</button>
                      <button class="action-btn delete" @click=${()=>this._deleteBackup(t.filename)}>删除</button>
                    </div>
                  </div>
                `)}
            </div>
          </div>
        </div>
      `:""}
    `}};Rr(U,"styles",w`
    :host { display: block; }
    
    h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-strong);
      margin-bottom: 24px;
    }
    
    .actions {
      display: flex;
      gap: 12px;
      margin-bottom: 24px;
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
    
    .btn-primary {
      background: var(--accent);
      color: var(--accent-foreground);
    }
    
    .btn-primary:hover { background: var(--accent-hover); }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
    
    .btn-secondary {
      background: var(--bg-elevated);
      color: var(--text);
      border: 1px solid var(--border);
    }
    
    .btn-secondary:hover { background: var(--bg-hover); }
    
    .config-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      margin-bottom: 20px;
      overflow: hidden;
    }
    
    .config-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      background: linear-gradient(135deg, var(--bg-accent) 0%, var(--card) 100%);
      border-bottom: 1px solid var(--border);
    }
    
    .config-title-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .config-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: var(--accent-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }
    
    .config-title-text h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .config-title-text p {
      margin: 2px 0 0;
      font-size: 12px;
      color: var(--muted);
    }
    
    .config-actions {
      display: flex;
      gap: 8px;
    }
    
    .config-body {
      padding: 20px;
    }
    
    /* 简单字段列表 */
    .field-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    
    .field-item {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    
    .field-label {
      width: 160px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
      flex-shrink: 0;
    }
    
    .field-input {
      flex: 1;
    }
    
    .input {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      transition: var(--duration-fast) ease;
    }
    
    .input:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-subtle);
    }
    
    .input.mono {
      font-family: var(--mono);
      font-size: 12px;
    }
    
    .checkbox {
      width: 20px;
      height: 20px;
      cursor: pointer;
      accent-color: var(--accent);
    }
    
    /* 分组区域 */
    .section {
      background: var(--bg-elevated);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
    }
    
    .section:last-child { margin-bottom: 0; }
    
    .section-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-strong);
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
    }
    
    .section-field {
      display: flex;
      align-items: center;
      gap: 16px;
    }
    
    .section-field-label {
      width: 160px;
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
      flex-shrink: 0;
    }
    
    .section-field-input {
      flex: 1;
    }
    
    .config-meta {
      font-size: 11px;
      color: var(--muted);
      padding: 12px 20px;
      border-top: 1px solid var(--border);
      background: var(--bg-accent);
      display: flex;
      justify-content: space-between;
    }
    
    /* Modal */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal {
      background: var(--card);
      border-radius: var(--radius-lg);
      width: 600px;
      max-height: 80vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
    }
    
    .modal-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-strong);
    }
    
    .modal-close {
      background: none;
      border: none;
      color: var(--muted);
      cursor: pointer;
      font-size: 20px;
    }
    
    .modal-body {
      padding: 16px;
      overflow-y: auto;
      flex: 1;
    }
    
    .backup-item {
      background: var(--bg-elevated);
      border-radius: var(--radius-md);
      padding: 12px;
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .backup-info { font-size: 13px; }
    
    .backup-name {
      font-weight: 500;
      color: var(--text-strong);
    }
    
    .backup-meta {
      font-size: 11px;
      color: var(--muted);
    }
    
    .backup-actions {
      display: flex;
      gap: 8px;
    }
    
    .action-btn {
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      cursor: pointer;
      border: none;
      transition: var(--duration-fast) ease;
    }
    
    .action-btn.restore {
      background: var(--ok-subtle);
      color: var(--ok);
    }
    
    .action-btn.restore:hover { background: var(--ok); color: white; }
    
    .action-btn.delete {
      background: var(--danger-subtle);
      color: var(--danger);
    }
    
    .action-btn.delete:hover { background: var(--danger); color: white; }
    
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
  `);Q([l()],U.prototype,"configs",2);Q([l()],U.prototype,"backups",2);Q([l()],U.prototype,"showBackups",2);Q([l()],U.prototype,"loading",2);Q([l()],U.prototype,"saving",2);U=Q([k("ea-settings")],U);var xe=Object.defineProperty,Vr=Object.getOwnPropertyDescriptor,qr=(o,t,e)=>t in o?xe(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,tt=(o,t,e,r)=>{for(var a=r>1?void 0:r?Vr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&xe(t,e,a),a},Gr=(o,t,e)=>qr(o,t+"",e);let L=class extends m{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"amazonData",{});d(this,"tiktokData",{});d(this,"loading",!1);d(this,"pinnedCategories",new Set)}connectedCallback(){super.connectedCallback(),this._loadPinned(),this.loadData()}_loadPinned(){const t=localStorage.getItem("pinned-categories");t&&(this.pinnedCategories=new Set(JSON.parse(t)))}_savePinned(){localStorage.setItem("pinned-categories",JSON.stringify([...this.pinnedCategories]))}_togglePin(t){this.pinnedCategories.has(t)?this.pinnedCategories.delete(t):this.pinnedCategories.add(t),this._savePinned(),this.requestUpdate()}async loadData(){this.loading=!0;try{this.platform==="amazon"&&Object.keys(this.amazonData).length===0?this.amazonData=await yr():this.platform==="tiktok"&&Object.keys(this.tiktokData).length===0&&(this.tiktokData=await $r())}catch(t){console.error("Load top error:",t)}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.loadData()}_truncate(t,e=20){return t?t.length>e?t.substring(0,e)+"...":t:"-"}_renderRankChange(t,e){return e?n`<span class="new-badge">新</span>`:t==null?null:t>0?n`<span class="rank-change up">↑${t}</span>`:t<0?n`<span class="rank-change down">↓${Math.abs(t)}</span>`:null}_sortCategories(t){const e=t.filter(a=>this.pinnedCategories.has(a)),r=t.filter(a=>!this.pinnedCategories.has(a));return[...e,...r]}render(){const t=this.platform==="amazon"?this.amazonData:this.tiktokData,e=this._sortCategories(Object.keys(t));return n`
      <div class="tabs">
        <button class="tab-btn ${this.platform==="amazon"?"active":""}" @click=${()=>this._switchPlatform("amazon")}>Amazon</button>
        <button class="tab-btn ${this.platform==="tiktok"?"active":""}" @click=${()=>this._switchPlatform("tiktok")}>TikTok</button>
      </div>

      ${this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:e.length===0?n`<div style="text-align:center;padding:48px;color:var(--muted)">暂无数据</div>`:n`
            <div class="categories-grid">
              ${e.map(r=>{const a=this.pinnedCategories.has(r);return n`
                  <div class="category-card ${a?"pinned":""}">
                    <div class="category-header">
                      <span>${r}</span>
                      <button 
                        class="pin-btn ${a?"pinned":""}" 
                        @click=${()=>this._togglePin(r)}
                        title=${a?"取消置顶":"置顶"}
                      >${a?"★":"☆"}</button>
                    </div>
                    <table>
                      <tbody>
                        ${(t[r]||[]).slice(0,15).map((i,s)=>n`
                          <tr style="cursor:pointer" @click=${()=>window.open(i.product_url||"#","_blank")}>
                            <td>
                              <div class="rank-cell">
                                <span class="rank">#${s+1}</span>
                                ${this._renderRankChange(i.rank_change,i.is_new)}
                              </div>
                            </td>
                            <td>
                              <a class="product-link" href=${i.product_url||"#"} target="_blank" title=${i.name}>
                                ${this._truncate(i.short_name||i.name)}
                              </a>
                            </td>
                            <td>${i.price?`$${i.price.toFixed(2)}`:"-"}</td>
                            <td>${i.rating?`${i.rating.toFixed(1)} ⭐`:"-"}</td>
                          </tr>
                        `)}
                      </tbody>
                    </table>
                  </div>
                `})}
            </div>
          `}
    `}};Gr(L,"styles",w`
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
  `);tt([l()],L.prototype,"platform",2);tt([l()],L.prototype,"amazonData",2);tt([l()],L.prototype,"tiktokData",2);tt([l()],L.prototype,"loading",2);tt([l()],L.prototype,"pinnedCategories",2);L=tt([k("ea-today-top")],L);var ye=Object.defineProperty,Jr=Object.getOwnPropertyDescriptor,Wr=(o,t,e)=>t in o?ye(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,R=(o,t,e,r)=>{for(var a=r>1?void 0:r?Jr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&ye(t,e,a),a},Yr=(o,t,e)=>Wr(o,t+"",e);let O=class extends m{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"products",[]);d(this,"loading",!1);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"category","")}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){var t;this.loading=!0,console.log("=== RawData: Loading, platform:",this.platform);try{const e={page:this.page,limit:20,search:this.search,category:this.category},r=this.platform==="amazon"?await _r(e):await wr(e);console.log("=== RawData: Result:",r),this.products=r.data||[],this.pages=((t=r.pagination)==null?void 0:t.pages)||0}catch(e){console.error("=== RawData: Error:",e),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_renderPagination(){const t=[];let r=Math.max(1,this.page-Math.floor(2.5)),a=Math.min(this.pages,r+5-1);a-r<4&&(r=Math.max(1,a-5+1));for(let i=r;i<=a;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return n`<div class="pagination">${t}</div>`}render(){return n`
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

      ${this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:n`
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>产品简称</th>
                  <th>搜索关键词</th>
                  <th>${this.platform==="tiktok"?"TikTokShop ID":"分类"}</th>
                  ${this.platform==="tiktok"?n`<th>分类</th>`:""}
                  <th>价格</th>
                  <th>评分</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                ${this.products.map(t=>n`
                  <tr>
                    <td style="font-size:11px;color:var(--muted)">${t.id}</td>
                    <td class="truncate" title=${t.name}>${t.short_name||t.name||"-"}</td>
                    <td class="truncate" title=${t.search_keyword}>${t.search_keyword||"-"}</td>
                    ${this.platform==="tiktok"?n`<td style="font-size:11px;font-family:monospace">${t.tiktokshop_id||"-"}</td>`:""}
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
    `}};Yr(O,"styles",w`
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
  `);R([l()],O.prototype,"platform",2);R([l()],O.prototype,"products",2);R([l()],O.prototype,"loading",2);R([l()],O.prototype,"page",2);R([l()],O.prototype,"pages",2);R([l()],O.prototype,"search",2);R([l()],O.prototype,"category",2);O=R([k("ea-raw-data")],O);var $e=Object.defineProperty,Kr=Object.getOwnPropertyDescriptor,Xr=(o,t,e)=>t in o?$e(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,_t=(o,t,e,r)=>{for(var a=r>1?void 0:r?Kr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&$e(t,e,a),a},Zr=(o,t,e)=>Xr(o,t+"",e);let Z=class extends m{constructor(){super(...arguments);d(this,"stats",{amazon_hot_tiktok_not:0,tiktok_hot_amazon_not:0,both_hot:0});d(this,"items",[]);d(this,"loading",!1)}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=await kr();this.stats=t.stats||this.stats,this.items=t.items||[]}catch(t){console.error("Load cross-platform error:",t)}finally{this.loading=!1}}render(){return n`
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

      ${this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:n`
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
                ${this.items.length===0?n`<tr><td colspan="4" style="text-align:center;color:var(--muted)">暂无数据</td></tr>`:this.items.map(t=>n`
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
    `}};Zr(Z,"styles",w`
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
  `);_t([l()],Z.prototype,"stats",2);_t([l()],Z.prototype,"items",2);_t([l()],Z.prototype,"loading",2);Z=_t([k("ea-cross-platform")],Z);var _e=Object.defineProperty,Qr=Object.getOwnPropertyDescriptor,ta=(o,t,e)=>t in o?_e(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Ut=(o,t,e,r)=>{for(var a=r>1?void 0:r?Qr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&_e(t,e,a),a},ea=(o,t,e)=>ta(o,t+"",e);let ct=class extends m{constructor(){super(...arguments);d(this,"format","csv");d(this,"dateRange","all")}_export(t){console.log("Export:",{platform:t,format:this.format,dateRange:this.dateRange}),alert(`导出功能开发中...
平台: ${t}
格式: ${this.format}
时间范围: ${this.dateRange}`)}render(){return n`
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
    `}};ea(ct,"styles",w`
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
  `);Ut([l()],ct.prototype,"format",2);Ut([l()],ct.prototype,"dateRange",2);ct=Ut([k("ea-export")],ct);/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ra={CHILD:2},aa=o=>(...t)=>({_$litDirective$:o,values:t});class oa{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,r){this._$Ct=t,this._$AM=e,this._$Ci=r}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class Ot extends oa{constructor(t){if(super(t),this.it=f,t.type!==ra.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===f||t==null)return this._t=void 0,this.it=t;if(t===G)return t;if(typeof t!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.it)return this._t;this.it=t;const e=[t];return e.raw=e,this._t={_$litType$:this.constructor.resultType,strings:e,values:[]}}}Ot.directiveName="unsafeHTML",Ot.resultType=1;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class Tt extends Ot{}Tt.directiveName="unsafeSVG",Tt.resultType=2;const Qt=aa(Tt);var we=Object.defineProperty,ia=Object.getOwnPropertyDescriptor,sa=(o,t,e)=>t in o?we(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,z=(o,t,e,r)=>{for(var a=r>1?void 0:r?ia(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&we(t,e,a),a},na=(o,t,e)=>sa(o,t+"",e);let C=class extends m{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"loading",!0);d(this,"product",{});d(this,"trend",[]);d(this,"details",[]);d(this,"pagination",{page:1,limit:20,total:0,pages:1});d(this,"timePreset","7");d(this,"customStart","");d(this,"customEnd","");d(this,"metric","sales_count");d(this,"currentPage",1);d(this,"tooltipData",{show:!1,x:0,y:0,date:"",value:null,index:0})}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=new URLSearchParams;this.timePreset==="custom"&&this.customStart&&this.customEnd?(t.set("start_date",this.customStart),t.set("end_date",this.customEnd)):t.set("days",this.timePreset),t.set("page",String(this.currentPage));const e=await fetch(`/api/product-trend/${this.ecomCode}?${t}`);if(!e.ok)throw new Error("Failed to load");const r=await e.json();this.product=r.product,this.trend=r.trend,this.details=r.details,this.pagination=r.pagination}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}_goBack(){const t=sessionStorage.getItem("trend-source-page")||"product-master";window.ecomagentNavigate(t);const e=sessionStorage.getItem("trend-source-state");e&&sessionStorage.setItem("restore-state",e)}_onTimePreset(t){this.timePreset=t,this.currentPage=1,this.loadData()}_onCustomDateChange(){this.customStart&&this.customEnd&&(this.timePreset="custom",this.currentPage=1,this.loadData())}_onMetricChange(t){this.metric=t,this.requestUpdate()}_onPageChange(t){this.currentPage=t,this.loadData()}_formatValue(t,e){if(t==null)return"-";if(e==="sales_count"){if(t>=1e4)return`${(t/1e3).toFixed(1)}K`;if(t>=1e3)return`${(t/1e3).toFixed(1)}K`}return e==="rating"?t.toFixed(1):e==="price"?`$${t.toFixed(2)}`:String(t)}_renderChart(){const t=this.trend;if(!t||t.length<1)return n`<div class="chart-empty">暂无数据</div>`;const e=t.map(v=>{const S=v[this.metric];return{...v,value:S??0,rawValue:S}}),r=800,a=320,i={top:20,right:40,bottom:50,left:70},s=r-i.left-i.right,p=a-i.top-i.bottom,c=e.map(v=>v.value),h=Math.min(...c),u=Math.max(...c)-h||1,g=v=>i.left+v/(t.length-1||1)*s,x=v=>i.top+p-(v-h)/u*p,E=e.map((v,S)=>`${g(S)},${x(v.value)}`).join(" L "),et=`M ${E}`,Pe=`M ${i.left},${i.top+p} L ${E} L ${g(t.length-1)},${i.top+p} Z`,kt=[],Ft=5;for(let v=0;v<=Ft;v++)kt.push(h+u*v/Ft);const Se=Math.ceil(t.length/7);let M="";return M+=`<defs>
      <linearGradient id="areaGradient" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ff5c5c" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#ff5c5c" stop-opacity="0.05" />
      </linearGradient>
    </defs>`,kt.forEach(v=>{M+=`<line x1="${i.left}" y1="${x(v)}" x2="${r-i.right}" y2="${x(v)}" stroke="#444" stroke-width="1" stroke-dasharray="4,4"/>`}),M+=`<path d="${Pe}" fill="url(#areaGradient)"/>`,M+=`<path d="${et}" fill="none" stroke="#ff5c5c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>`,e.forEach((v,S)=>{M+=`<circle cx="${g(S)}" cy="${x(v.value)}" r="4" fill="#ff5c5c" stroke="#1a1a1a" stroke-width="1"/>`}),kt.forEach(v=>{const S=this._formatValue(v,this.metric);M+=`<text x="${i.left-6}" y="${x(v)+2}" text-anchor="end" fill="#888" font-size="8" font-family="system-ui, -apple-system, sans-serif" font-weight="400">${S}</text>`}),e.forEach((v,S)=>{if(S%Se!==0&&S!==t.length-1)return;const Pt=v.date.slice(5);M+=`<text x="${g(S)}" y="${a-8}" text-anchor="middle" fill="#888" font-size="8" font-family="system-ui, -apple-system, sans-serif" font-weight="400">${Pt}</text>`}),n`
      <svg class="chart-svg" viewBox="0 0 ${r} ${a}" preserveAspectRatio="xMidYMid meet"
        @mousemove=${v=>{const S=v.currentTarget.getBoundingClientRect(),Pt=v.clientX-S.left,Ce=S.width/r,ze=Pt/Ce-i.left,rt=Math.round(ze/s*(t.length-1));if(rt>=0&&rt<t.length){const St=e[rt];this.tooltipData={show:!0,x:g(rt),y:x(St.value),date:St.date,value:St.rawValue,index:rt}}}} @mouseleave=${()=>{this.tooltipData={...this.tooltipData,show:!1}}}>
        ${Qt(M)}
        ${this.tooltipData.show?Qt(`<line class="tooltip-line" x1="${this.tooltipData.x}" y1="0" x2="${this.tooltipData.x}" y2="${a}" stroke="#ff5c5c" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/><circle class="tooltip-point" cx="${this.tooltipData.x}" cy="${this.tooltipData.y}" r="8" fill="#ff5c5c" stroke="#fff" stroke-width="3"/>`):null}
      </svg>
      
      <!-- Tooltip 浮框 -->
      ${this.tooltipData.show?n`
        <div class="tooltip" style="left:calc(${this.tooltipData.x/800*100}%);top:calc(${this.tooltipData.y/320*100}%)">
          <div class="tooltip-date">${this.tooltipData.date}</div>
          <div class="tooltip-value">
            <span class="tooltip-label">${this._getMetricLabel()}</span>
            ${this._formatValue(this.tooltipData.value,this.metric)}
          </div>
        </div>
      `:""}
    `}_getMetricLabel(){switch(this.metric){case"sales_count":return"销量";case"rating":return"评分";case"price":return"价格";default:return""}}_getMetricHint(){switch(this.metric){case"sales_count":return"显示商品每日销量变化趋势";case"rating":return"显示商品评分变化趋势";case"price":return"显示商品价格变化趋势";default:return""}}_renderPagination(){const t=[];let r=Math.max(1,this.pagination.page-Math.floor(2.5)),a=Math.min(this.pagination.pages,r+5-1);a-r<4&&(r=Math.max(1,a-5+1)),r>1&&(t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),r>2&&t.push(n`<span style="color:var(--muted)">...</span>`));for(let i=r;i<=a;i++)t.push(n`
        <button class="page-btn ${i===this.pagination.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return a<this.pagination.pages&&(a<this.pagination.pages-1&&t.push(n`<span style="color:var(--muted)">...</span>`),t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(this.pagination.pages)}>${this.pagination.pages}</button>`)),n`<div class="pagination">${t}</div>`}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=[{key:"sales_count",label:"销量"},{key:"rating",label:"评分"},{key:"price",label:"价格"}],e=[{key:"7",label:"近7天"},{key:"15",label:"近15天"},{key:"30",label:"近1月"},{key:"90",label:"近3月"}];return n`
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
          ${e.map(r=>n`
            <button class="time-tab ${this.timePreset===r.key?"active":""}" @click=${()=>this._onTimePreset(r.key)}>${r.label}</button>
          `)}
        </div>
        <div class="date-inputs">
          <input type="date" class="date-input" .value=${this.customStart} @input=${r=>{this.customStart=r.target.value}} @change=${this._onCustomDateChange}>
          <span style="color:var(--muted)">至</span>
          <input type="date" class="date-input" .value=${this.customEnd} @input=${r=>{this.customEnd=r.target.value}} @change=${this._onCustomDateChange}>
          <button class="apply-btn" @click=${this._onCustomDateChange}>应用</button>
        </div>
      </div>

      <!-- 图表 -->
      <div class="chart-section">
        <div class="chart-header">
          <span class="chart-title">趋势图表</span>
          <div style="display:flex;align-items:center">
            <div class="metric-tabs">
              ${t.map(r=>n`
                <button class="metric-tab ${this.metric===r.key?"active":""}" @click=${()=>this._onMetricChange(r.key)}>${r.label}</button>
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
            ${this.details.map(r=>n`
              <tr>
                <td>${r.date}</td>
                <td style="max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${r.short_name||""}>${r.short_name||"-"}</td>
                <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${r.search_keyword||""}>${r.search_keyword||"-"}</td>
                <td>${r.rating!=null?r.rating.toFixed(1):"-"}</td>
                <td>${r.price!=null?`$${r.price.toFixed(2)}`:"-"}</td>
                <td>${r.sales_count!=null?this._formatValue(r.sales_count,"sales_count"):"-"}</td>
                <td>${r.events?r.events.split(", ").map(a=>n`<span class="event-tag">${a}</span>`):"-"}</td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pagination.pages>1?this._renderPagination():""}
      </div>
    `}};na(C,"styles",w`
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
      transform: translate(-50%, -100%);
      background: rgba(26, 26, 30, 0.95);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 92, 92, 0.2);
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 12px;
      pointer-events: none;
      white-space: nowrap;
      z-index: 10;
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
  `);z([A({type:String})],C.prototype,"ecomCode",2);z([l()],C.prototype,"loading",2);z([l()],C.prototype,"product",2);z([l()],C.prototype,"trend",2);z([l()],C.prototype,"details",2);z([l()],C.prototype,"pagination",2);z([l()],C.prototype,"timePreset",2);z([l()],C.prototype,"customStart",2);z([l()],C.prototype,"customEnd",2);z([l()],C.prototype,"metric",2);z([l()],C.prototype,"currentPage",2);z([l()],C.prototype,"tooltipData",2);C=z([k("ea-product-trend-page")],C);var ke=Object.defineProperty,da=Object.getOwnPropertyDescriptor,la=(o,t,e)=>t in o?ke(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Lt=(o,t,e,r)=>{for(var a=r>1?void 0:r?da(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(a=(r?s(t,e,a):s(a))||a);return r&&a&&ke(t,e,a),a},ca=(o,t,e)=>la(o,t+"",e);const wt=new Set;let pt="dashboard";window.ecomagentNavigate=o=>{pt=o,wt.forEach(t=>t(o))};window.ecomagentGetCurrentPage=()=>pt;window.ecomagentOnPageChange=o=>{wt.add(o)};window.ecomagentOpenTrend=(o,t="product-master")=>{sessionStorage.setItem("trend-source-page",t),sessionStorage.setItem("trend-source-state",JSON.stringify({page:pt,scrollY:window.scrollY})),pt="product-trend",sessionStorage.setItem("trend-ecom-code",o),wt.forEach(e=>e("product-trend"))};let ht=class extends m{constructor(){super();d(this,"_page",pt);d(this,"_trendCode","");wt.add(t=>{this._page=t,t==="product-trend"&&(this._trendCode=sessionStorage.getItem("trend-ecom-code")||""),this.requestUpdate()})}connectedCallback(){super.connectedCallback();const t=localStorage.getItem("theme")||"dark";document.body.setAttribute("data-theme-mode",t)}_renderPage(){if(this._page==="product-trend")return n`<ea-product-trend-page ecomCode=${this._trendCode}></ea-product-trend-page>`;switch(this._page){case"dashboard":return n`<ea-dashboard></ea-dashboard>`;case"settings":return n`<ea-settings></ea-settings>`;case"product-master":return n`<ea-product-master></ea-product-master>`;case"tracking":return n`<ea-tracking></ea-tracking>`;case"cross-platform":return n`<ea-cross-platform></ea-cross-platform>`;case"today-top":return n`<ea-today-top></ea-today-top>`;case"raw-data":return n`<ea-raw-data></ea-raw-data>`;case"export":return n`<ea-export></ea-export>`;default:return n`<div style="padding:24px;color:var(--muted)">未知页面</div>`}}render(){return this._page==="product-trend"?n`
        <ea-layout currentPage=${this._page}>
          <div style="padding:24px">${this._renderPage()}</div>
        </ea-layout>
      `:n`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `}};ca(ht,"styles",w`:host { display: block; min-height: 100vh; }`);Lt([l()],ht.prototype,"_page",2);Lt([l()],ht.prototype,"_trendCode",2);ht=Lt([k("ecomagent-app")],ht);console.log("EcomAgent UI loaded");

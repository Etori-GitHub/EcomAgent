var Le=Object.defineProperty;var Ue=(o,t,e)=>t in o?Le(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e;var d=(o,t,e)=>Ue(o,typeof t!="symbol"?t+"":t,e);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))a(r);new MutationObserver(r=>{for(const i of r)if(i.type==="childList")for(const s of i.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&a(s)}).observe(document,{childList:!0,subtree:!0});function e(r){const i={};return r.integrity&&(i.integrity=r.integrity),r.referrerPolicy&&(i.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?i.credentials="include":r.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function a(r){if(r.ep)return;r.ep=!0;const i=e(r);fetch(r.href,i)}})();/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const $t=globalThis,Ut=$t.ShadowRoot&&($t.ShadyCSS===void 0||$t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,Ft=Symbol(),Jt=new WeakMap;let se=class{constructor(t,e,a){if(this._$cssResult$=!0,a!==Ft)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(Ut&&t===void 0){const a=e!==void 0&&e.length===1;a&&(t=Jt.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),a&&Jt.set(e,t))}return t}toString(){return this.cssText}};const Fe=o=>new se(typeof o=="string"?o:o+"",void 0,Ft),$=(o,...t)=>{const e=o.length===1?o[0]:t.reduce((a,r,i)=>a+(s=>{if(s._$cssResult$===!0)return s.cssText;if(typeof s=="number")return s;throw Error("Value passed to 'css' function must be a 'css' function result: "+s+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(r)+o[i+1],o[0]);return new se(e,o,Ft)},Re=(o,t)=>{if(Ut)o.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const e of t){const a=document.createElement("style"),r=$t.litNonce;r!==void 0&&a.setAttribute("nonce",r),a.textContent=e.cssText,o.appendChild(a)}},Yt=Ut?o=>o:o=>o instanceof CSSStyleSheet?(t=>{let e="";for(const a of t.cssRules)e+=a.cssText;return Fe(e)})(o):o;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const{is:He,defineProperty:qe,getOwnPropertyDescriptor:Be,getOwnPropertyNames:Ve,getOwnPropertySymbols:Ge,getPrototypeOf:Je}=Object,F=globalThis,Wt=F.trustedTypes,Ye=Wt?Wt.emptyScript:"",Ot=F.reactiveElementPolyfillSupport,ht=(o,t)=>o,_t={toAttribute(o,t){switch(t){case Boolean:o=o?Ye:null;break;case Object:case Array:o=o==null?o:JSON.stringify(o)}return o},fromAttribute(o,t){let e=o;switch(t){case Boolean:e=o!==null;break;case Number:e=o===null?null:Number(o);break;case Object:case Array:try{e=JSON.parse(o)}catch{e=null}}return e}},Rt=(o,t)=>!He(o,t),Kt={attribute:!0,type:String,converter:_t,reflect:!1,useDefault:!1,hasChanged:Rt};Symbol.metadata??(Symbol.metadata=Symbol("metadata")),F.litPropertyMetadata??(F.litPropertyMetadata=new WeakMap);let at=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??(this.l=[])).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Kt){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const a=Symbol(),r=this.getPropertyDescriptor(t,a,e);r!==void 0&&qe(this.prototype,t,r)}}static getPropertyDescriptor(t,e,a){const{get:r,set:i}=Be(this.prototype,t)??{get(){return this[e]},set(s){this[e]=s}};return{get:r,set(s){const p=r==null?void 0:r.call(this);i==null||i.call(this,s),this.requestUpdate(t,p,a)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Kt}static _$Ei(){if(this.hasOwnProperty(ht("elementProperties")))return;const t=Je(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(ht("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(ht("properties"))){const e=this.properties,a=[...Ve(e),...Ge(e)];for(const r of a)this.createProperty(r,e[r])}const t=this[Symbol.metadata];if(t!==null){const e=litPropertyMetadata.get(t);if(e!==void 0)for(const[a,r]of e)this.elementProperties.set(a,r)}this._$Eh=new Map;for(const[e,a]of this.elementProperties){const r=this._$Eu(e,a);r!==void 0&&this._$Eh.set(r,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const a=new Set(t.flat(1/0).reverse());for(const r of a)e.unshift(Yt(r))}else t!==void 0&&e.push(Yt(t));return e}static _$Eu(t,e){const a=e.attribute;return a===!1?void 0:typeof a=="string"?a:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){var t;this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),(t=this.constructor.l)==null||t.forEach(e=>e(this))}addController(t){var e;(this._$EO??(this._$EO=new Set)).add(t),this.renderRoot!==void 0&&this.isConnected&&((e=t.hostConnected)==null||e.call(t))}removeController(t){var e;(e=this._$EO)==null||e.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const a of e.keys())this.hasOwnProperty(a)&&(t.set(a,this[a]),delete this[a]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Re(t,this.constructor.elementStyles),t}connectedCallback(){var t;this.renderRoot??(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostConnected)==null?void 0:a.call(e)})}enableUpdating(t){}disconnectedCallback(){var t;(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostDisconnected)==null?void 0:a.call(e)})}attributeChangedCallback(t,e,a){this._$AK(t,a)}_$ET(t,e){var i;const a=this.constructor.elementProperties.get(t),r=this.constructor._$Eu(t,a);if(r!==void 0&&a.reflect===!0){const s=(((i=a.converter)==null?void 0:i.toAttribute)!==void 0?a.converter:_t).toAttribute(e,a.type);this._$Em=t,s==null?this.removeAttribute(r):this.setAttribute(r,s),this._$Em=null}}_$AK(t,e){var i,s;const a=this.constructor,r=a._$Eh.get(t);if(r!==void 0&&this._$Em!==r){const p=a.getPropertyOptions(r),c=typeof p.converter=="function"?{fromAttribute:p.converter}:((i=p.converter)==null?void 0:i.fromAttribute)!==void 0?p.converter:_t;this._$Em=r;const h=c.fromAttribute(e,p.type);this[r]=h??((s=this._$Ej)==null?void 0:s.get(r))??h,this._$Em=null}}requestUpdate(t,e,a,r=!1,i){var s;if(t!==void 0){const p=this.constructor;if(r===!1&&(i=this[t]),a??(a=p.getPropertyOptions(t)),!((a.hasChanged??Rt)(i,e)||a.useDefault&&a.reflect&&i===((s=this._$Ej)==null?void 0:s.get(t))&&!this.hasAttribute(p._$Eu(t,a))))return;this.C(t,e,a)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:a,reflect:r,wrapped:i},s){a&&!(this._$Ej??(this._$Ej=new Map)).has(t)&&(this._$Ej.set(t,s??e??this[t]),i!==!0||s!==void 0)||(this._$AL.has(t)||(this.hasUpdated||a||(e=void 0),this._$AL.set(t,e)),r===!0&&this._$Em!==t&&(this._$Eq??(this._$Eq=new Set)).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var a;if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??(this.renderRoot=this.createRenderRoot()),this._$Ep){for(const[i,s]of this._$Ep)this[i]=s;this._$Ep=void 0}const r=this.constructor.elementProperties;if(r.size>0)for(const[i,s]of r){const{wrapped:p}=s,c=this[i];p!==!0||this._$AL.has(i)||c===void 0||this.C(i,void 0,s,c)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),(a=this._$EO)==null||a.forEach(r=>{var i;return(i=r.hostUpdate)==null?void 0:i.call(r)}),this.update(e)):this._$EM()}catch(r){throw t=!1,this._$EM(),r}t&&this._$AE(e)}willUpdate(t){}_$AE(t){var e;(e=this._$EO)==null||e.forEach(a=>{var r;return(r=a.hostUpdated)==null?void 0:r.call(a)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&(this._$Eq=this._$Eq.forEach(e=>this._$ET(e,this[e]))),this._$EM()}updated(t){}firstUpdated(t){}};at.elementStyles=[],at.shadowRootOptions={mode:"open"},at[ht("elementProperties")]=new Map,at[ht("finalized")]=new Map,Ot==null||Ot({ReactiveElement:at}),(F.reactiveElementVersions??(F.reactiveElementVersions=[])).push("2.1.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ut=globalThis,Xt=o=>o,wt=ut.trustedTypes,Zt=wt?wt.createPolicy("lit-html",{createHTML:o=>o}):void 0,ne="$lit$",U=`lit$${Math.random().toFixed(9).slice(2)}$`,de="?"+U,We=`<${de}>`,K=document,gt=()=>K.createComment(""),vt=o=>o===null||typeof o!="object"&&typeof o!="function",Ht=Array.isArray,Ke=o=>Ht(o)||typeof(o==null?void 0:o[Symbol.iterator])=="function",Mt=`[ 	
\f\r]`,pt=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Qt=/-->/g,te=/>/g,J=RegExp(`>|${Mt}(?:([^\\s"'>=/]+)(${Mt}*=${Mt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),ee=/'/g,ae=/"/g,le=/^(?:script|style|textarea|title)$/i,Xe=o=>(t,...e)=>({_$litType$:o,strings:t,values:e}),n=Xe(1),X=Symbol.for("lit-noChange"),f=Symbol.for("lit-nothing"),re=new WeakMap,Y=K.createTreeWalker(K,129);function ce(o,t){if(!Ht(o)||!o.hasOwnProperty("raw"))throw Error("invalid template strings array");return Zt!==void 0?Zt.createHTML(t):t}const Ze=(o,t)=>{const e=o.length-1,a=[];let r,i=t===2?"<svg>":t===3?"<math>":"",s=pt;for(let p=0;p<e;p++){const c=o[p];let h,b,u=-1,g=0;for(;g<c.length&&(s.lastIndex=g,b=s.exec(c),b!==null);)g=s.lastIndex,s===pt?b[1]==="!--"?s=Qt:b[1]!==void 0?s=te:b[2]!==void 0?(le.test(b[2])&&(r=RegExp("</"+b[2],"g")),s=J):b[3]!==void 0&&(s=J):s===J?b[0]===">"?(s=r??pt,u=-1):b[1]===void 0?u=-2:(u=s.lastIndex-b[2].length,h=b[1],s=b[3]===void 0?J:b[3]==='"'?ae:ee):s===ae||s===ee?s=J:s===Qt||s===te?s=pt:(s=J,r=void 0);const x=s===J&&o[p+1].startsWith("/>")?" ":"";i+=s===pt?c+We:u>=0?(a.push(h),c.slice(0,u)+ne+c.slice(u)+U+x):c+U+(u===-2?p:x)}return[ce(o,i+(o[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),a]};class bt{constructor({strings:t,_$litType$:e},a){let r;this.parts=[];let i=0,s=0;const p=t.length-1,c=this.parts,[h,b]=Ze(t,e);if(this.el=bt.createElement(h,a),Y.currentNode=this.el.content,e===2||e===3){const u=this.el.content.firstChild;u.replaceWith(...u.childNodes)}for(;(r=Y.nextNode())!==null&&c.length<p;){if(r.nodeType===1){if(r.hasAttributes())for(const u of r.getAttributeNames())if(u.endsWith(ne)){const g=b[s++],x=r.getAttribute(u).split(U),O=/([.?@])?(.*)/.exec(g);c.push({type:1,index:i,name:O[2],strings:x,ctor:O[1]==="."?ta:O[1]==="?"?ea:O[1]==="@"?aa:St}),r.removeAttribute(u)}else u.startsWith(U)&&(c.push({type:6,index:i}),r.removeAttribute(u));if(le.test(r.tagName)){const u=r.textContent.split(U),g=u.length-1;if(g>0){r.textContent=wt?wt.emptyScript:"";for(let x=0;x<g;x++)r.append(u[x],gt()),Y.nextNode(),c.push({type:2,index:++i});r.append(u[g],gt())}}}else if(r.nodeType===8)if(r.data===de)c.push({type:2,index:i});else{let u=-1;for(;(u=r.data.indexOf(U,u+1))!==-1;)c.push({type:7,index:i}),u+=U.length-1}i++}}static createElement(t,e){const a=K.createElement("template");return a.innerHTML=t,a}}function rt(o,t,e=o,a){var s,p;if(t===X)return t;let r=a!==void 0?(s=e._$Co)==null?void 0:s[a]:e._$Cl;const i=vt(t)?void 0:t._$litDirective$;return(r==null?void 0:r.constructor)!==i&&((p=r==null?void 0:r._$AO)==null||p.call(r,!1),i===void 0?r=void 0:(r=new i(o),r._$AT(o,e,a)),a!==void 0?(e._$Co??(e._$Co=[]))[a]=r:e._$Cl=r),r!==void 0&&(t=rt(o,r._$AS(o,t.values),r,a)),t}class Qe{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:a}=this._$AD,r=((t==null?void 0:t.creationScope)??K).importNode(e,!0);Y.currentNode=r;let i=Y.nextNode(),s=0,p=0,c=a[0];for(;c!==void 0;){if(s===c.index){let h;c.type===2?h=new yt(i,i.nextSibling,this,t):c.type===1?h=new c.ctor(i,c.name,c.strings,this,t):c.type===6&&(h=new ra(i,this,t)),this._$AV.push(h),c=a[++p]}s!==(c==null?void 0:c.index)&&(i=Y.nextNode(),s++)}return Y.currentNode=K,r}p(t){let e=0;for(const a of this._$AV)a!==void 0&&(a.strings!==void 0?(a._$AI(t,a,e),e+=a.strings.length-2):a._$AI(t[e])),e++}}class yt{get _$AU(){var t;return((t=this._$AM)==null?void 0:t._$AU)??this._$Cv}constructor(t,e,a,r){this.type=2,this._$AH=f,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=a,this.options=r,this._$Cv=(r==null?void 0:r.isConnected)??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return e!==void 0&&(t==null?void 0:t.nodeType)===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=rt(this,t,e),vt(t)?t===f||t==null||t===""?(this._$AH!==f&&this._$AR(),this._$AH=f):t!==this._$AH&&t!==X&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Ke(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==f&&vt(this._$AH)?this._$AA.nextSibling.data=t:this.T(K.createTextNode(t)),this._$AH=t}$(t){var i;const{values:e,_$litType$:a}=t,r=typeof a=="number"?this._$AC(t):(a.el===void 0&&(a.el=bt.createElement(ce(a.h,a.h[0]),this.options)),a);if(((i=this._$AH)==null?void 0:i._$AD)===r)this._$AH.p(e);else{const s=new Qe(r,this),p=s.u(this.options);s.p(e),this.T(p),this._$AH=s}}_$AC(t){let e=re.get(t.strings);return e===void 0&&re.set(t.strings,e=new bt(t)),e}k(t){Ht(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let a,r=0;for(const i of t)r===e.length?e.push(a=new yt(this.O(gt()),this.O(gt()),this,this.options)):a=e[r],a._$AI(i),r++;r<e.length&&(this._$AR(a&&a._$AB.nextSibling,r),e.length=r)}_$AR(t=this._$AA.nextSibling,e){var a;for((a=this._$AP)==null?void 0:a.call(this,!1,!0,e);t!==this._$AB;){const r=Xt(t).nextSibling;Xt(t).remove(),t=r}}setConnected(t){var e;this._$AM===void 0&&(this._$Cv=t,(e=this._$AP)==null||e.call(this,t))}}class St{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,a,r,i){this.type=1,this._$AH=f,this._$AN=void 0,this.element=t,this.name=e,this._$AM=r,this.options=i,a.length>2||a[0]!==""||a[1]!==""?(this._$AH=Array(a.length-1).fill(new String),this.strings=a):this._$AH=f}_$AI(t,e=this,a,r){const i=this.strings;let s=!1;if(i===void 0)t=rt(this,t,e,0),s=!vt(t)||t!==this._$AH&&t!==X,s&&(this._$AH=t);else{const p=t;let c,h;for(t=i[0],c=0;c<i.length-1;c++)h=rt(this,p[a+c],e,c),h===X&&(h=this._$AH[c]),s||(s=!vt(h)||h!==this._$AH[c]),h===f?t=f:t!==f&&(t+=(h??"")+i[c+1]),this._$AH[c]=h}s&&!r&&this.j(t)}j(t){t===f?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class ta extends St{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===f?void 0:t}}class ea extends St{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==f)}}class aa extends St{constructor(t,e,a,r,i){super(t,e,a,r,i),this.type=5}_$AI(t,e=this){if((t=rt(this,t,e,0)??f)===X)return;const a=this._$AH,r=t===f&&a!==f||t.capture!==a.capture||t.once!==a.once||t.passive!==a.passive,i=t!==f&&(a===f||r);r&&this.element.removeEventListener(this.name,this,a),i&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e;typeof this._$AH=="function"?this._$AH.call(((e=this.options)==null?void 0:e.host)??this.element,t):this._$AH.handleEvent(t)}}class ra{constructor(t,e,a){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=a}get _$AU(){return this._$AM._$AU}_$AI(t){rt(this,t)}}const Dt=ut.litHtmlPolyfillSupport;Dt==null||Dt(bt,yt),(ut.litHtmlVersions??(ut.litHtmlVersions=[])).push("3.3.2");const oa=(o,t,e)=>{const a=(e==null?void 0:e.renderBefore)??t;let r=a._$litPart$;if(r===void 0){const i=(e==null?void 0:e.renderBefore)??null;a._$litPart$=r=new yt(t.insertBefore(gt(),i),i,void 0,e??{})}return r._$AI(o),r};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const W=globalThis;let m=class extends at{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e;const t=super.createRenderRoot();return(e=this.renderOptions).renderBefore??(e.renderBefore=t.firstChild),t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=oa(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),(t=this._$Do)==null||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),(t=this._$Do)==null||t.setConnected(!1)}render(){return X}};var ie;m._$litElement$=!0,m.finalized=!0,(ie=W.litElementHydrateSupport)==null||ie.call(W,{LitElement:m});const It=W.litElementPolyfillSupport;It==null||It({LitElement:m});(W.litElementVersions??(W.litElementVersions=[])).push("4.2.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const _=o=>(t,e)=>{e!==void 0?e.addInitializer(()=>{customElements.define(o,t)}):customElements.define(o,t)};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const ia={attribute:!0,type:String,converter:_t,reflect:!1,hasChanged:Rt},sa=(o=ia,t,e)=>{const{kind:a,metadata:r}=e;let i=globalThis.litPropertyMetadata.get(r);if(i===void 0&&globalThis.litPropertyMetadata.set(r,i=new Map),a==="setter"&&((o=Object.create(o)).wrapped=!0),i.set(e.name,o),a==="accessor"){const{name:s}=e;return{set(p){const c=t.get.call(this);t.set.call(this,p),this.requestUpdate(s,c,o,!0,p)},init(p){return p!==void 0&&this.C(s,void 0,o,p),p}}}if(a==="setter"){const{name:s}=e;return function(p){const c=this[s];t.call(this,p),this.requestUpdate(s,c,o,!0,p)}}throw Error("Unsupported decorator location: "+a)};function T(o){return(t,e)=>typeof e=="object"?sa(o,t,e):((a,r,i)=>{const s=r.hasOwnProperty(i);return r.constructor.createProperty(i,a),s?Object.getOwnPropertyDescriptor(r,i):void 0})(o,t,e)}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function l(o){return T({...o,state:!0,attribute:!1})}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const na={CHILD:2},da=o=>(...t)=>({_$litDirective$:o,values:t});class la{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,e,a){this._$Ct=t,this._$AM=e,this._$Ci=a}_$AS(t,e){return this.update(t,e)}update(t,e){return this.render(...e)}}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class jt extends la{constructor(t){if(super(t),this.it=f,t.type!==na.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===f||t==null)return this._t=void 0,this.it=t;if(t===X)return t;if(typeof t!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.it)return this._t;this.it=t;const e=[t];return e.raw=e,this._t={_$litType$:this.constructor.resultType,strings:e,values:[]}}}jt.directiveName="unsafeHTML",jt.resultType=1;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class Nt extends jt{}Nt.directiveName="unsafeSVG",Nt.resultType=2;const Lt=da(Nt),w="/api";async function k(o,t){const e=await fetch(o,t);if(!e.ok){const a=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(a.detail||`HTTP ${e.status}`)}return e.json()}async function ca(){return k(`${w}/stats`)}async function pa(o){return k(`${w}/categories`)}async function ha(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return k(`${w}/product-master?${t}`)}async function pe(o,t=7){return k(`${w}/sales-trend/${o}?days=${t}`)}async function ua(o){return k(`${w}/tracked-products?ids=${o.join(",")}`)}async function ga(){return k(`${w}/config/list`)}async function he(o){return k(`${w}/config/${o}`)}async function va(){return{app_name:(await he("settings")).data.app_name||"EcomAgent"}}async function ba(o,t){return k(`${w}/config/${o}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:t})})}async function oe(){return k(`${w}/config/backups/list`)}async function ma(o){return k(`${w}/config/backups/${o}/restore`,{method:"POST"})}async function fa(o){return k(`${w}/config/backups/${o}`,{method:"DELETE"})}async function xa(o,t=7){return k(`${w}/product-trend/${o}?days=${t}`)}async function ya(){return k(`${w}/amazon/top-by-category`)}async function $a(){return k(`${w}/tiktok/top-by-category`)}async function _a(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return k(`${w}/amazon/products?${t}`)}async function wa(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return k(`${w}/tiktok/products?${t}`)}async function ka(){return k(`${w}/cross-platform-analysis`)}var ue=Object.defineProperty,Pa=Object.getOwnPropertyDescriptor,Sa=(o,t,e)=>t in o?ue(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,qt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Pa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ue(t,e,r),r},za=(o,t,e)=>Sa(o,t+"",e);const Ca=[{group:"Main",items:[{id:"dashboard",icon:"grid",label:"数据概览"},{id:"product-master",icon:"box",label:"商品总库"},{id:"sourcing",icon:"package",label:"货源库"},{id:"tracking",icon:"target",label:"商品追踪"},{id:"cross-platform",icon:"sync",label:"跨平台分析"}]},{group:"平台数据",items:[{id:"today-top",icon:"star",label:"今日TOP榜"},{id:"raw-data",icon:"database",label:"原始数据"}]},{group:"系统",items:[{id:"export",icon:"download",label:"数据导出"},{id:"translation-logs",icon:"file-text",label:"翻译日志"},{id:"settings",icon:"settings",label:"系统设置"}]}],Ta={grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',box:'<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',package:'<line x1="16.5" y1="9.4" x2="7.5" y1="4.21"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/><line x1="12" y1="12" x2="7.5" y1="9.4"/>',target:'<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',sync:'<path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/>',star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',database:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',settings:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',"file-text":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>'};let mt=class extends m{constructor(){super();d(this,"collapsed",!1);d(this,"appName",window.ecomagentAppName||"EcomAgent");d(this,"_currentPage","dashboard");this._loadAppName(),window.ecomagentOnPageChange&&window.ecomagentOnPageChange(t=>{this._currentPage=t,this.requestUpdate()}),window.ecomagentGetCurrentPage&&(this._currentPage=window.ecomagentGetCurrentPage())}async _loadAppName(){if(window.ecomagentAppName){this.appName=window.ecomagentAppName;return}try{const t=await va();this.appName=t.app_name,window.ecomagentAppName=t.app_name}catch(t){console.error("Failed to load app name:",t)}}_onNavClick(t){if(t==="sourcing"&&window.ecomagentNavigateDirectToSourcing){window.ecomagentNavigateDirectToSourcing();return}window.ecomagentNavigate&&window.ecomagentNavigate(t)}_onToggle(){this.collapsed=!this.collapsed,this.requestUpdate("collapsed")}render(){const t=this._currentPage,e=this.appName.charAt(0);return n`
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
        ${Ca.map(a=>n`
          <div class="nav-group">
            <div class="nav-group-header"><span class="nav-group-title">${a.group}</span></div>
            <ul class="nav-items">
              ${a.items.map(r=>n`
                <li class="nav-item ${t===r.id?"active":""}" @click=${()=>this._onNavClick(r.id)}>
                  <svg class="nav-icon" viewBox="0 0 24 24">${Lt(Ta[r.icon])}</svg>
                  <span class="nav-label">${r.label}</span>
                </li>
              `)}
            </ul>
          </div>
        `)}
      </div>
    `}};za(mt,"styles",$`
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
  `);qt([T({type:Boolean,reflect:!0})],mt.prototype,"collapsed",2);qt([l()],mt.prototype,"appName",2);mt=qt([_("ea-sidebar")],mt);var ge=Object.defineProperty,Aa=Object.getOwnPropertyDescriptor,Ea=(o,t,e)=>t in o?ge(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,ve=(o,t,e,a)=>{for(var r=a>1?void 0:a?Aa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ge(t,e,r),r},Oa=(o,t,e)=>Ea(o,t+"",e);const Ma={dashboard:{title:"数据概览",subtitle:"查看数据统计和概览"},"product-master":{title:"商品总库",subtitle:"统一管理所有平台商品"},sourcing:{title:"货源库",subtitle:"1688货源采集与管理"},tracking:{title:"商品追踪",subtitle:"追踪特定商品的价格、销量变化"},"cross-platform":{title:"跨平台分析",subtitle:"对比分析不同平台数据"},"today-top":{title:"今日TOP榜",subtitle:"各平台热销产品排行"},"raw-data":{title:"原始数据",subtitle:"查看和搜索原始数据"},export:{title:"数据导出",subtitle:"导出数据为 CSV 或 Excel"},"translation-logs":{title:"翻译日志",subtitle:"翻译任务执行记录"},settings:{title:"系统设置",subtitle:"配置数据源和其他选项"},"product-trend":{title:"商品趋势",subtitle:"查看商品各维度数据随时间变化"}};let kt=class extends m{constructor(){super(...arguments);d(this,"currentPage","dashboard")}toggleTheme(){const t=document.body,a=t.getAttribute("data-theme-mode")==="dark"?"light":"dark";t.setAttribute("data-theme-mode",a),localStorage.setItem("theme",a),this.requestUpdate()}render(){const{title:t,subtitle:e}=Ma[this.currentPage],a=document.body.getAttribute("data-theme-mode")!=="light";return n`
      <div>
        <div class="title">${t}</div>
        <div class="subtitle">${e}</div>
      </div>
      
      <div class="actions">
        <button class="icon-btn" @click=${this.toggleTheme} title="切换主题">
          ${a?n`
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
    `}};Oa(kt,"styles",$`
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
  `);ve([T({type:String})],kt.prototype,"currentPage",2);kt=ve([_("ea-header")],kt);var be=Object.defineProperty,Da=Object.getOwnPropertyDescriptor,Ia=(o,t,e)=>t in o?be(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Bt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Da(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&be(t,e,r),r},ja=(o,t,e)=>Ia(o,t+"",e);let ft=class extends m{constructor(){super(...arguments);d(this,"currentPage","dashboard");d(this,"sidebarCollapsed",!1)}render(){return n`
      <ea-sidebar ?collapsed=${this.sidebarCollapsed}></ea-sidebar>
      <main class="main-content">
        <ea-header .currentPage=${this.currentPage}></ea-header>
        <div class="content-body"><slot></slot></div>
      </main>
    `}};ja(ft,"styles",$`
    :host { display: flex; min-height: 100vh; }
    .main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
    .content-body { animation: fadeIn 0.3s ease; }
    @media (max-width: 1024px) { :host { flex-direction: column; } .main-content { padding: 16px; } }
  `);Bt([T({type:String})],ft.prototype,"currentPage",2);Bt([l()],ft.prototype,"sidebarCollapsed",2);ft=Bt([_("ea-layout")],ft);var me=Object.defineProperty,Na=Object.getOwnPropertyDescriptor,La=(o,t,e)=>t in o?me(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,B=(o,t,e,a)=>{for(var r=a>1?void 0:a?Na(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&me(t,e,r),r},fe=(o,t,e)=>La(o,t+"",e);let Pt=class extends m{constructor(){super(...arguments);d(this,"padding",16)}render(){return n`
      <slot name="header"></slot>
      <div class="card-content" style="--padding: ${this.padding}px">
        <slot></slot>
      </div>
    `}};fe(Pt,"styles",$`
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
  `);B([T({type:Number})],Pt.prototype,"padding",2);Pt=B([_("ea-card")],Pt);let R=class extends m{constructor(){super(...arguments);d(this,"label","");d(this,"value","-");d(this,"icon","");d(this,"desc","");d(this,"color","")}render(){return n`
      <div class="stat-header">
        <div>
          <div class="stat-label">${this.label}</div>
          <div class="stat-value ${this.color}">${this.value}</div>
          ${this.desc?n`<div class="stat-desc">${this.desc}</div>`:""}
        </div>
        ${this.icon?n`<span class="stat-icon">${this.icon}</span>`:""}
      </div>
      <slot></slot>
    `}};fe(R,"styles",$`
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
  `);B([T({type:String})],R.prototype,"label",2);B([T({type:String})],R.prototype,"value",2);B([T({type:String})],R.prototype,"icon",2);B([T({type:String})],R.prototype,"desc",2);B([T({type:String})],R.prototype,"color",2);R=B([_("ea-stat-card")],R);var xe=Object.defineProperty,Ua=Object.getOwnPropertyDescriptor,Fa=(o,t,e)=>t in o?xe(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,V=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ua(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&xe(t,e,r),r},Ra=(o,t,e)=>Fa(o,t+"",e);let M=class extends m{constructor(){super(...arguments);d(this,"stats",null);d(this,"loading",!0);d(this,"error","");d(this,"expandedPanel",null);d(this,"categories",{amazon:[],tiktok:[]});d(this,"categoriesLoading",!1);d(this,"fetchTaskStatus",{amazon:"",tiktok:""})}connectedCallback(){super.connectedCallback(),this.loadStats()}async loadStats(){this.loading=!0,this.error="";try{this.stats=await ca()}catch(t){this.error=t instanceof Error?t.message:String(t)}finally{this.loading=!1,this.requestUpdate()}}async _togglePanel(t){if(this.expandedPanel===t){this.expandedPanel=null;return}this.expandedPanel=t,this.requestUpdate(),(!this.categories[t]||this.categories[t].length===0)&&await this._loadCategories(t)}async _loadCategories(t){this.categoriesLoading=!0,this.requestUpdate();try{const a=await(await fetch(`/api/categories/${t}`)).json();this.categories={...this.categories,[t]:a.categories||[]},this.requestUpdate()}catch(e){console.error("加载类目失败:",e)}finally{this.categoriesLoading=!1,this.requestUpdate()}}async _refreshCategories(t){this.categoriesLoading=!0;try{const a=await(await fetch(`/api/categories/${t}/refresh`,{method:"POST"})).json();a.success?await this._loadCategories(t):alert(a.message||"刷新失败")}catch(e){alert(`刷新失败: ${e}`)}finally{this.categoriesLoading=!1}}async _toggleCategory(t,e,a){try{await fetch(`/api/categories/${e}/enabled?enabled=${a}`,{method:"PUT"}),this.categories={...this.categories,[t]:this.categories[t].map(r=>r.id===e?{...r,enabled:a?1:0}:r)}}catch(r){alert(`更新失败: ${r}`)}}async _startFetch(t){this.fetchTaskStatus={...this.fetchTaskStatus,[t]:"running"};try{const a=await(await fetch(`/api/tasks/${t}/fetch`,{method:"POST"})).json();a.success?alert(`${t} 抓取任务已启动`):(alert(a.message||"启动失败"),this.fetchTaskStatus={...this.fetchTaskStatus,[t]:""})}catch(e){alert(`启动失败: ${e}`),this.fetchTaskStatus={...this.fetchTaskStatus,[t]:""}}}_renderFetchPanel(t){const e=this.expandedPanel===t,a=this.categories[t],r=this.categoriesLoading,i=this.fetchTaskStatus[t]==="running",s=a.filter(c=>c.today_status==="done").length,p=a.filter(c=>c.today_status==="pending").length;return n`
      <div class="fetch-panel ${e?"expanded":""}">
        <div class="fetch-header" @click=${()=>this._togglePanel(t)}>
          <div class="fetch-header-left">
            <svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
            <span class="fetch-header-title">数据抓取</span>
            ${a.length>0?n`
              <span class="fetch-header-badge">${a.length} 个类目 · 今日已抓 ${s} / 待抓 ${p}</span>
            `:""}
          </div>
        </div>

        <div class="fetch-content">
          ${r?n`<div class="empty-text">加载中...</div>`:""}

          ${!r&&a.length===0?n`
            <div class="empty-text">暂无类目数据,请点击「刷新类目」获取</div>
          `:""}

          ${!r&&a.length>0?n`
            <div class="category-list">
              ${a.map(c=>n`
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
            <button @click=${()=>this._refreshCategories(t)} ?disabled=${r}>
              刷新类目
            </button>
            <button
              class="primary"
              @click=${()=>this._startFetch(t)}
              ?disabled=${i||a.filter(c=>c.enabled&&c.today_status==="pending").length===0}
            >
              ${i?"抓取中...":"开始抓取"}
            </button>
          </div>
        </div>
      </div>
    `}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;if(this.error)return n`
        <div class="error-box">
          <p>加载失败: ${this.error}</p>
          <button class="retry-btn" @click=${this.loadStats}>重试</button>
        </div>
      `;if(!this.stats)return n`<div class="error-box"><p>无数据</p></div>`;const{amazon:t,tiktok:e}=this.stats;return n`
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
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${t.sales.toLocaleString()}<br>
              今日新增: ${t.today.toLocaleString()}
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
            <div style="font-size: 13px; color: var(--muted);">
              抓取记录: ${e.sales.toLocaleString()}<br>
              今日新增: ${e.today.toLocaleString()}
            </div>
          </ea-stat-card>
          ${this._renderFetchPanel("tiktok")}
        </div>
      </div>
    `}};Ra(M,"styles",$`
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
  `);V([l()],M.prototype,"stats",2);V([l()],M.prototype,"loading",2);V([l()],M.prototype,"error",2);V([l()],M.prototype,"expandedPanel",2);V([l()],M.prototype,"categories",2);V([l()],M.prototype,"categoriesLoading",2);V([l()],M.prototype,"fetchTaskStatus",2);M=V([_("ea-dashboard")],M);var ye=Object.defineProperty,Ha=Object.getOwnPropertyDescriptor,qa=(o,t,e)=>t in o?ye(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Q=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ha(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ye(t,e,r),r},Ba=(o,t,e)=>qa(o,t+"",e);let I=class extends m{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"product",null);d(this,"trendData",[]);d(this,"loading",!0);d(this,"metric","rating");d(this,"days",7)}connectedCallback(){super.connectedCallback(),this.ecomCode&&this.loadTrendData()}updated(t){t.has("ecomCode")&&this.ecomCode&&this.loadTrendData()}async loadTrendData(){if(this.ecomCode){this.loading=!0;try{const t=await xa(this.ecomCode,this.days);this.product=t.product,this.trendData=t.trend||[]}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}}_onMetricChange(t){this.metric=t.target.value,this.requestUpdate()}_onDaysChange(t){const e=t.target.value;e!=="custom"&&(this.days=parseInt(e),this.loadTrendData())}_getMetricLabel(){switch(this.metric){case"price":return"价格";case"rating":return"评分";case"rank":return"排名"}}_renderChart(){if(this.trendData.length===0)return n`<div class="chart-empty">暂无数据</div>`;const t=this.trendData.map(i=>i[this.metric]).filter(i=>i!=null);if(t.length===0)return n`<div class="chart-empty">暂无${this._getMetricLabel()}数据</div>`;const e=Math.max(...t),a=Math.min(...t),r=e-a||1;return n`
      <div class="chart">
        ${this.trendData.map(i=>{const s=i[this.metric];if(s==null)return n`<div class="chart-bar" style="height:0"></div>`;const p=(s-a)/r*250+20;return n`
            <div class="chart-bar" style="height:${p}px">
              <span class="chart-bar-value">${this.metric==="rating"?s.toFixed(1):s}</span>
              <span class="chart-bar-label">${i.date.slice(5)}</span>
            </div>
          `})}
      </div>
    `}_renderTrend(t,e){if(t===null||e===null)return"-";const a=t-e;return Math.abs(a)<.01?"-":this.metric==="rank"?a<0?n`<span class="trend-up">↑${Math.abs(a).toFixed(0)}</span>`:n`<span class="trend-down">↓${Math.abs(a).toFixed(0)}</span>`:a>0?n`<span class="trend-up">↑${a.toFixed(2)}</span>`:n`<span class="trend-down">↓${Math.abs(a).toFixed(2)}</span>`}render(){return this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.product?n`
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
            ${this.trendData.map((t,e)=>{const a=e<this.trendData.length-1?this.trendData[e+1]:null;return n`
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
    `:n`
        <div class="header">
          <a class="back-link" href="javascript:history.back()">← 返回</a>
        </div>
        <div style="text-align:center;padding:48px;color:var(--muted)">商品不存在</div>
      `}};Ba(I,"styles",$`
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
  `);Q([T({type:String})],I.prototype,"ecomCode",2);Q([l()],I.prototype,"product",2);Q([l()],I.prototype,"trendData",2);Q([l()],I.prototype,"loading",2);Q([l()],I.prototype,"metric",2);Q([l()],I.prototype,"days",2);I=Q([_("ea-product-trend")],I);var $e=Object.defineProperty,Va=Object.getOwnPropertyDescriptor,Ga=(o,t,e)=>t in o?$e(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,P=(o,t,e,a)=>{for(var r=a>1?void 0:a?Va(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&$e(t,e,r),r},Ja=(o,t,e)=>Ga(o,t+"",e);let y=class extends m{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"platform","amazon");d(this,"category","");d(this,"categories",{amazon:[],tiktok:[],all:[]});d(this,"sortBy","total_sales");d(this,"sortOrder","desc");d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map);d(this,"previewImg",{show:!1,src:"",x:0,y:0})}async connectedCallback(){super.connectedCallback(),this.loadTracked(),await this.loadCategories(),this.loadData()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t)))}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadCategories(){try{if(this.categories=await pa(),!this.category){const t=this.platform==="amazon"?this.categories.amazon:this.categories.tiktok;t.length>0&&(this.category=t[0])}}catch(t){console.error("Failed to load categories",t)}}async loadData(){this.loading=!0;try{const t=await ha({page:this.page,limit:20,search:this.search,platform:this.platform,category:this.category,sort_by:this.sortBy||void 0,sort_order:this.sortOrder});this.products=t.data,this.pages=t.pagination.pages,this.loadSparklines(t.data)}catch(t){console.error("Failed to load products",t)}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async a=>{try{const r=await pe(a.ecom_code,7);this.sparklines.set(a.ecom_code,r.trend)}catch{this.sparklines.set(a.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_onPlatformChange(t){this.platform=t;const e=t==="amazon"?this.categories.amazon:this.categories.tiktok;this.category=e.length>0?e[0]:"",this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onInputChange(t,e){this[e]=t.target.value}_onCategoryChange(t){this.category=t.target.value,this.page=1,this.loadData()}_onSort(t){this.sortBy===t?this.sortOrder=this.sortOrder==="desc"?"asc":"desc":(this.sortBy=t,this.sortOrder="desc"),this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_toggleTrack(t){this.trackedIds.has(t)?this.trackedIds.delete(t):this.trackedIds.add(t),this.saveTracked(),this.requestUpdate()}async _resetTranslation(t){try{(await(await fetch(`/api/products/${t}/reset-translation`,{method:"POST"})).json()).success&&this.loadData()}catch(e){console.error("Reset translation failed:",e)}}_showTrendPage(t){const e={platform:this.platform,category:this.category,search:this.search,sortBy:this.sortBy,sortOrder:this.sortOrder,page:this.page,scrollY:window.scrollY};sessionStorage.setItem("product-master-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"product-master")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_showSourcingModal(t){window.ecomagentNavigateToSourcing(t)}async _open1688(t,e){if(t)try{const i=`${(await(await fetch(`/api/1688-search-url?keyword=${encodeURIComponent(t)}`)).json()).url}&ecom_code=${e}`;window.open(i,"_blank")}catch{const r=`https://s.1688.com/selloffer/offer_search.htm?keywords=${encodeURIComponent(t)}&ecom_code=${e}`;window.open(r,"_blank")}}_showImgPreview(t,e){this.previewImg={show:!0,src:e,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement()}_hideImgPreview(){this.previewImg={...this.previewImg,show:!1},this._updatePreviewElement()}_moveImgPreview(t){this.previewImg.show&&(this.previewImg={...this.previewImg,x:t.clientX+16,y:t.clientY+16},this._updatePreviewElement())}_updatePreviewElement(){let t=document.getElementById("global-img-preview");t||(t=document.createElement("img"),t.id="global-img-preview",t.style.cssText="position:fixed;z-index:9999;max-width:400px;max-height:400px;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.5);pointer-events:none;border:1px solid rgba(255,255,255,0.1);",document.body.appendChild(t)),this.previewImg.show?(t.src=this.previewImg.src,t.style.left=this.previewImg.x+"px",t.style.top=this.previewImg.y+"px",t.style.display="block"):t.style.display="none"}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=e.map(g=>g.value).filter(g=>g!=null);if(a.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const r=Math.min(...a),s=Math.max(...a)-r||1,p=100,c=32,h=2,b=a.map((g,x)=>{const O=h+x/(a.length-1)*(p-h*2),lt=c-h-(g-r)/s*(c-h*2);return`${O},${lt}`}).join(" "),u=b+` ${h+(a.length-1)/(a.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return n`
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
    `}_renderSortHeader(t,e){const a=this.sortBy===e,r=a?this.sortOrder==="desc"?"▼":"▲":"⇅";return n`
      <th class="sortable ${a?"sorted":""}" @click=${()=>this._onSort(e)}>
        ${t} <span class="sort-icon">${r}</span>
      </th>
    `}_getCategoryOptions(){return this.platform==="amazon"?this.categories.amazon:this.platform==="tiktok"?this.categories.tiktok:[]}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),r=Math.min(this.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1)),a>1&&(t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),a>2&&t.push(n`<span style="color:var(--muted)">...</span>`));for(let i=a;i<=r;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return r<this.pages&&(r<this.pages-1&&t.push(n`<span style="color:var(--muted)">...</span>`),t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>`)),n`<div class="pagination">${t}</div>`}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=this._getCategoryOptions();return n`
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
              ${this._renderSortHeader("总销售额","total_sales")}
              <th style="width:100px">7日趋势</th>
              <th style="width:90px">操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map((e,a)=>n`
              <tr class="product-row">
                <td style="text-align:center;font-weight:600;color:var(--muted)">${(this.page-1)*20+a+1}</td>
                <td>
                  ${e.local_image_path||e.image_url?n`<img class="product-img" src=${e.local_image_path?`/images/${e.local_image_path}`:e.image_url||""} loading="lazy" 
                        @mouseenter=${r=>this._showImgPreview(r,e.local_image_path?`/images/${e.local_image_path}`:e.image_url||"")}
                        @mouseleave=${this._hideImgPreview}
                        @mousemove=${this._moveImgPreview} />`:n`<div class="product-img-placeholder">📦</div>`}
                </td>
                <td>
                  <div class="product-info">
                    <div class="product-name-row">
                      ${e.product_url?n`<a class="product-name product-link" href=${e.product_url} target="_blank" title=${e.name}>${e.short_name||e.name||"无名称"}</a>`:n`<span class="product-name" title=${e.name}>${e.short_name||e.name||"无名称"}</span>`}
                      ${e.translation_status==="translated"?n`<button class="retranslate-btn" @click=${()=>this._resetTranslation(e.ecom_code)} title="重新翻译">🔄</button>`:""}
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
                <td>${e.rating?n`${e.rating.toFixed(1)} ⭐`:"-"}</td>
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
      ${this.showTrend?n`
        <div class="modal-overlay" @click=${this._closeTrendModal}>
          <div class="modal-content" @click=${e=>e.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
      
      <!-- 图片预览浮框 -->
    `}};Ja(y,"styles",$`
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
  `);P([l()],y.prototype,"products",2);P([l()],y.prototype,"loading",2);P([l()],y.prototype,"page",2);P([l()],y.prototype,"pages",2);P([l()],y.prototype,"search",2);P([l()],y.prototype,"platform",2);P([l()],y.prototype,"category",2);P([l()],y.prototype,"categories",2);P([l()],y.prototype,"sortBy",2);P([l()],y.prototype,"sortOrder",2);P([l()],y.prototype,"trackedIds",2);P([l()],y.prototype,"showTrend",2);P([l()],y.prototype,"trendCode",2);P([l()],y.prototype,"sparklines",2);P([l()],y.prototype,"previewImg",2);y=P([_("ea-product-master")],y);var _e=Object.defineProperty,Ya=Object.getOwnPropertyDescriptor,Wa=(o,t,e)=>t in o?_e(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,tt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ya(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&_e(t,e,r),r},Ka=(o,t,e)=>Wa(o,t+"",e);let j=class extends m{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","");d(this,"sparklines",new Map)}connectedCallback(){super.connectedCallback(),this.loadTracked()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t))),this.loadData()}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadData(){if(this.loading=!0,this.trackedIds.size===0){this.products=[],this.loading=!1,this.requestUpdate();return}try{const t=await ua([...this.trackedIds]);this.products=t.products||[],this.loadSparklines(this.products)}catch(t){console.error("Load tracking error:",t),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}async loadSparklines(t){const e=t.map(async a=>{try{const r=await pe(a.ecom_code,7);this.sparklines.set(a.ecom_code,r.trend)}catch{this.sparklines.set(a.ecom_code,[])}});await Promise.all(e),this.requestUpdate()}_untrack(t){this.trackedIds.delete(t),this.saveTracked(),this.products=this.products.filter(e=>e.ecom_code!==t),this.requestUpdate()}_showTrendPage(t){const e={scrollY:window.scrollY};sessionStorage.setItem("tracking-state",JSON.stringify(e)),window.ecomagentOpenTrend(t,"tracking")}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_formatSales(t){return t==null?"-":t>=1e4?`${(t/1e3).toFixed(1)}K`:t>=1e3?`${(t/1e3).toFixed(1)}K`:String(t)}_renderSparkline(t){const e=this.sparklines.get(t);if(!e||e.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const a=e.map(g=>g.value).filter(g=>g!=null);if(a.length<2)return n`<div class="sparkline-container" style="display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:10px;">暂无数据</div>`;const r=Math.min(...a),s=Math.max(...a)-r||1,p=100,c=32,h=2,b=a.map((g,x)=>{const O=h+x/(a.length-1)*(p-h*2),lt=c-h-(g-r)/s*(c-h*2);return`${O},${lt}`}).join(" "),u=b+` ${h+(a.length-1)/(a.length-1)*(p-h*2)},${c-h} ${h},${c-h}`;return n`
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
    `}};Ka(j,"styles",$`
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
  `);tt([l()],j.prototype,"products",2);tt([l()],j.prototype,"loading",2);tt([l()],j.prototype,"trackedIds",2);tt([l()],j.prototype,"showTrend",2);tt([l()],j.prototype,"trendCode",2);tt([l()],j.prototype,"sparklines",2);j=tt([_("ea-tracking")],j);var we=Object.defineProperty,Xa=Object.getOwnPropertyDescriptor,Za=(o,t,e)=>t in o?we(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,st=(o,t,e,a)=>{for(var r=a>1?void 0:a?Xa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&we(t,e,r),r},Qa=(o,t,e)=>Za(o,t+"",e);const tr={app_name:"软件名称",google:"Google API Key",volcano:"火山引擎 API Key",xai:"xAI API Key",image_providers:"图片生成模型",default:"默认模型",available:"可用模型",flash_image:"Flash Image",model:"模型名称",aspect_ratios:"支持比例",resolutions:"支持分辨率",video_providers:"视频生成模型",grok:"Grok",max_duration:"最大时长(秒)",gemini:"Gemini 配置",temperature:"温度参数",max_output_tokens:"最大输出Token",triggers:"触发器列表",image:"生成图片",video:"生成视频",amazon:"亚马逊抓取",tiktok:"TikTok抓取",test:"测试模式",name:"名称",script:"脚本路径",keywords:"触发关键词",description:"描述",settings:"设置",cache_expire_minutes:"缓存过期时间(分钟)",case_sensitive:"区分大小写"},er={settings:{title:"系统设置",desc:"应用名称等基础配置",icon:"⚙️"},api_keys:{title:"API 密钥",desc:"各平台 API 访问密钥",icon:"🔑"},models:{title:"模型配置",desc:"图片、视频生成模型参数",icon:"🤖"},triggers:{title:"触发器",desc:"命令关键词触发配置",icon:"⚡"}};let H=class extends m{constructor(){super(...arguments);d(this,"configs",[]);d(this,"backups",[]);d(this,"showBackups",!1);d(this,"loading",!0);d(this,"saving",null)}connectedCallback(){super.connectedCallback(),this.loadConfigs()}async loadConfigs(){this.loading=!0;try{const t=await ga(),e=await oe(),a=[];for(const r of t.configs)if(!r.name.includes("template"))try{const i=await he(r.name);a.push({name:r.name,filename:r.filename,data:i.data,modified:i.modified})}catch(i){console.error("Load config error:",r.name,i)}this.configs=a,this.backups=e.backups}catch(t){console.error("Failed to load configs:",t)}finally{this.loading=!1,this.requestUpdate()}}_getLabel(t){return tr[t]||t}_getConfigInfo(t){return er[t]||{title:t,desc:"",icon:"📄"}}_onFieldChange(t,e,a){const r=this.configs.find(i=>i.name===t);if(r){const i=e.split(".");let s=r.data;for(let p=0;p<i.length-1;p++)s=s[i[p]];s[i[i.length-1]]=a,this.requestUpdate()}}async _saveConfig(t){const e=this.configs.find(a=>a.name===t);if(e){this.saving=t;try{const a=JSON.stringify(e.data,null,2),r=await ba(t,a);alert(`✅ 配置已保存
备份文件: `+r.backup),this.loadConfigs()}catch(a){alert("保存失败: "+(a instanceof Error?a.message:String(a)))}finally{this.saving=null}}}async _restoreBackup(t){if(confirm(`确定要还原备份 ${t} 吗？`))try{const e=await ma(t);alert(`✅ 已还原备份
原配置已备份为: ${e.pre_restore_backup}`),this.showBackups=!1,this.loadConfigs()}catch(e){alert("还原失败: "+(e instanceof Error?e.message:String(e)))}}async _deleteBackup(t){if(confirm(`确定要删除备份 ${t} 吗？`))try{await fa(t);const e=await oe();this.backups=e.backups}catch(e){alert("删除失败: "+(e instanceof Error?e.message:String(e)))}}_renderSimpleFields(t){return n`
      <div class="field-list">
        ${Object.entries(t.data).map(([e,a])=>n`
          <div class="field-item">
            <div class="field-label">${this._getLabel(e)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input mono"
                .value=${String(a)}
                @change=${r=>this._onFieldChange(t.name,e,r.target.value)}
              >
            </div>
          </div>
        `)}
      </div>
    `}_renderSectionFields(t){return Object.entries(t.data).map(([e,a])=>typeof a!="object"||a===null?n`
          <div class="field-item">
            <div class="field-label">${this._getLabel(e)}</div>
            <div class="field-input">
              <input 
                type="text" 
                class="input"
                .value=${String(a)}
                @change=${r=>this._onFieldChange(t.name,e,r.target.value)}
              >
            </div>
          </div>
        `:n`
        <div class="section">
          <div class="section-title">${this._getLabel(e)}</div>
          <div class="section-grid">
            ${this._renderSectionFieldsRecursive(t.name,e,a)}
          </div>
        </div>
      `)}_renderSectionFieldsRecursive(t,e,a){return Object.entries(a).map(([r,i])=>{const s=`${e}.${r}`;return typeof i=="object"&&i!==null&&!Array.isArray(i)?n`
          <div class="section">
            <div class="section-title">${this._getLabel(r)}</div>
            ${this._renderSectionFieldsRecursive(t,s,i)}
          </div>
        `:n`
        <div class="field-item">
          <div class="field-label">${this._getLabel(r)}</div>
          <div class="field-input">
            ${this._renderInput(t,s,i)}
          </div>
        </div>
      `})}_renderInput(t,e,a){return typeof a=="boolean"?n`
        <input 
          type="checkbox" 
          class="checkbox"
          .checked=${a}
          @change=${r=>this._onFieldChange(t,e,r.target.checked)}
        >
      `:Array.isArray(a)?n`
        <input 
          type="text" 
          class="input mono"
          .value=${JSON.stringify(a)}
          @change=${r=>{try{const i=JSON.parse(r.target.value);this._onFieldChange(t,e,i)}catch{}}}
        >
      `:n`
      <input 
        type="text" 
        class="input"
        .value=${String(a??"")}
        @change=${r=>this._onFieldChange(t,e,r.target.value)}
      >
    `}_renderConfigCard(t){const e=this._getConfigInfo(t.name),a=this.saving===t.name,r=t.name==="api_keys"||t.name==="settings";return n`
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
              ?disabled=${a}
              @click=${()=>this._saveConfig(t.name)}
            >${a?"保存中...":"保存"}</button>
          </div>
        </div>
        
        <div class="config-body">
          ${r?this._renderSimpleFields(t):this._renderSectionFields(t)}
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
    `}};Qa(H,"styles",$`
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
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 16px;
      align-items: center;
    }
    
    .field-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    
    .field-input {
      min-width: 0; /* 防止溢出 */
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
      display: grid;
      grid-template-columns: 160px 1fr;
      gap: 16px;
      align-items: center;
    }
    
    .section-field-label {
      font-size: 13px;
      font-weight: 500;
      color: var(--text);
    }
    
    .section-field-input {
      min-width: 0;
    }
    
    .section-grid {
      display: flex;
      flex-direction: column;
      gap: 16px;
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
  `);st([l()],H.prototype,"configs",2);st([l()],H.prototype,"backups",2);st([l()],H.prototype,"showBackups",2);st([l()],H.prototype,"loading",2);st([l()],H.prototype,"saving",2);H=st([_("ea-settings")],H);var ke=Object.defineProperty,ar=Object.getOwnPropertyDescriptor,rr=(o,t,e)=>t in o?ke(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,nt=(o,t,e,a)=>{for(var r=a>1?void 0:a?ar(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ke(t,e,r),r},or=(o,t,e)=>rr(o,t+"",e);let q=class extends m{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"amazonData",{});d(this,"tiktokData",{});d(this,"loading",!1);d(this,"pinnedCategories",new Set)}connectedCallback(){super.connectedCallback(),this._loadPinned(),this.loadData()}_loadPinned(){const t=localStorage.getItem("pinned-categories");t&&(this.pinnedCategories=new Set(JSON.parse(t)))}_savePinned(){localStorage.setItem("pinned-categories",JSON.stringify([...this.pinnedCategories]))}_togglePin(t){this.pinnedCategories.has(t)?this.pinnedCategories.delete(t):this.pinnedCategories.add(t),this._savePinned(),this.requestUpdate()}async loadData(){this.loading=!0;try{this.platform==="amazon"&&Object.keys(this.amazonData).length===0?this.amazonData=await ya():this.platform==="tiktok"&&Object.keys(this.tiktokData).length===0&&(this.tiktokData=await $a())}catch(t){console.error("Load top error:",t)}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.loadData()}_truncate(t,e=20){return t?t.length>e?t.substring(0,e)+"...":t:"-"}_renderRankChange(t,e){return e?n`<span class="new-badge">新</span>`:t==null?null:t>0?n`<span class="rank-change up">↑${t}</span>`:t<0?n`<span class="rank-change down">↓${Math.abs(t)}</span>`:null}_sortCategories(t){const e=t.filter(r=>this.pinnedCategories.has(r)),a=t.filter(r=>!this.pinnedCategories.has(r));return[...e,...a]}render(){const t=this.platform==="amazon"?this.amazonData:this.tiktokData,e=this._sortCategories(Object.keys(t));return n`
      <div class="tabs">
        <button class="tab-btn ${this.platform==="amazon"?"active":""}" @click=${()=>this._switchPlatform("amazon")}>Amazon</button>
        <button class="tab-btn ${this.platform==="tiktok"?"active":""}" @click=${()=>this._switchPlatform("tiktok")}>TikTok</button>
      </div>

      ${this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:e.length===0?n`<div style="text-align:center;padding:48px;color:var(--muted)">暂无数据</div>`:n`
            <div class="categories-grid">
              ${e.map(a=>{const r=this.pinnedCategories.has(a);return n`
                  <div class="category-card ${r?"pinned":""}">
                    <div class="category-header">
                      <span>${a}</span>
                      <button 
                        class="pin-btn ${r?"pinned":""}" 
                        @click=${()=>this._togglePin(a)}
                        title=${r?"取消置顶":"置顶"}
                      >${r?"★":"☆"}</button>
                    </div>
                    <table>
                      <tbody>
                        ${(t[a]||[]).slice(0,15).map((i,s)=>n`
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
    `}};or(q,"styles",$`
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
  `);nt([l()],q.prototype,"platform",2);nt([l()],q.prototype,"amazonData",2);nt([l()],q.prototype,"tiktokData",2);nt([l()],q.prototype,"loading",2);nt([l()],q.prototype,"pinnedCategories",2);q=nt([_("ea-today-top")],q);var Pe=Object.defineProperty,ir=Object.getOwnPropertyDescriptor,sr=(o,t,e)=>t in o?Pe(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,G=(o,t,e,a)=>{for(var r=a>1?void 0:a?ir(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Pe(t,e,r),r},nr=(o,t,e)=>sr(o,t+"",e);let D=class extends m{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"products",[]);d(this,"loading",!1);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"category","")}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){var t;this.loading=!0,console.log("=== RawData: Loading, platform:",this.platform);try{const e={page:this.page,limit:20,search:this.search,category:this.category},a=this.platform==="amazon"?await _a(e):await wa(e);console.log("=== RawData: Result:",a),this.products=a.data||[],this.pages=((t=a.pagination)==null?void 0:t.pages)||0}catch(e){console.error("=== RawData: Error:",e),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),r=Math.min(this.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1));for(let i=a;i<=r;i++)t.push(n`
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
    `}};nr(D,"styles",$`
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
  `);G([l()],D.prototype,"platform",2);G([l()],D.prototype,"products",2);G([l()],D.prototype,"loading",2);G([l()],D.prototype,"page",2);G([l()],D.prototype,"pages",2);G([l()],D.prototype,"search",2);G([l()],D.prototype,"category",2);D=G([_("ea-raw-data")],D);var Se=Object.defineProperty,dr=Object.getOwnPropertyDescriptor,lr=(o,t,e)=>t in o?Se(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,zt=(o,t,e,a)=>{for(var r=a>1?void 0:a?dr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Se(t,e,r),r},cr=(o,t,e)=>lr(o,t+"",e);let ot=class extends m{constructor(){super(...arguments);d(this,"stats",{amazon_hot_tiktok_not:0,tiktok_hot_amazon_not:0,both_hot:0});d(this,"items",[]);d(this,"loading",!1)}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=await ka();this.stats=t.stats||this.stats,this.items=t.items||[]}catch(t){console.error("Load cross-platform error:",t)}finally{this.loading=!1}}render(){return n`
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
    `}};cr(ot,"styles",$`
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
  `);zt([l()],ot.prototype,"stats",2);zt([l()],ot.prototype,"items",2);zt([l()],ot.prototype,"loading",2);ot=zt([_("ea-cross-platform")],ot);var ze=Object.defineProperty,pr=Object.getOwnPropertyDescriptor,hr=(o,t,e)=>t in o?ze(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Vt=(o,t,e,a)=>{for(var r=a>1?void 0:a?pr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ze(t,e,r),r},ur=(o,t,e)=>hr(o,t+"",e);let xt=class extends m{constructor(){super(...arguments);d(this,"format","csv");d(this,"dateRange","all")}_export(t){console.log("Export:",{platform:t,format:this.format,dateRange:this.dateRange}),alert(`导出功能开发中...
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
    `}};ur(xt,"styles",$`
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
  `);Vt([l()],xt.prototype,"format",2);Vt([l()],xt.prototype,"dateRange",2);xt=Vt([_("ea-export")],xt);var Ce=Object.defineProperty,gr=Object.getOwnPropertyDescriptor,vr=(o,t,e)=>t in o?Ce(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,A=(o,t,e,a)=>{for(var r=a>1?void 0:a?gr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Ce(t,e,r),r},br=(o,t,e)=>vr(o,t+"",e);let z=class extends m{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"loading",!0);d(this,"product",{});d(this,"trend",[]);d(this,"details",[]);d(this,"pagination",{page:1,limit:20,total:0,pages:1});d(this,"timePreset","7");d(this,"customStart","");d(this,"customEnd","");d(this,"metric","");d(this,"currentPage",1);d(this,"tooltipData",{show:!1,x:0,y:0,date:"",value:null,index:0})}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=new URLSearchParams;this.timePreset==="custom"&&this.customStart&&this.customEnd?(t.set("start_date",this.customStart),t.set("end_date",this.customEnd)):t.set("days",this.timePreset),t.set("page",String(this.currentPage));const e=await fetch(`/api/product-trend/${this.ecomCode}?${t}`);if(!e.ok)throw new Error("Failed to load");const a=await e.json();this.product=a.product,this.trend=a.trend,this.details=a.details,this.pagination=a.pagination,this.metric||(this.product.platform==="amazon"?this.metric="rating":this.metric="sales_count")}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}_goBack(){const t=sessionStorage.getItem("trend-source-page")||"product-master";window.ecomagentNavigate(t);const e=sessionStorage.getItem("trend-source-state");e&&sessionStorage.setItem("restore-state",e)}_onTimePreset(t){this.timePreset=t,this.currentPage=1,this.loadData()}_onCustomDateChange(){this.customStart&&this.customEnd&&(this.timePreset="custom",this.currentPage=1,this.loadData())}_onMetricChange(t){this.metric=t,this.requestUpdate()}_onPageChange(t){this.currentPage=t,this.loadData()}_formatValue(t,e){if(t==null)return"-";if(e==="sales_count"){if(t>=1e4)return`${(t/1e3).toFixed(1)}K`;if(t>=1e3)return`${(t/1e3).toFixed(1)}K`}return e==="rating"?t.toFixed(1):e==="price"?`$${t.toFixed(2)}`:String(t)}_renderChart(){const t=this.trend;if(!t||t.length<1)return n`<div class="chart-empty">暂无数据</div>`;const e=t.map(v=>{const S=v[this.metric];return{...v,value:S??0,rawValue:S}}),a=800,r=320,i={top:20,right:40,bottom:50,left:70},s=a-i.left-i.right,p=r-i.top-i.bottom,c=e.map(v=>v.value),h=Math.min(...c),u=Math.max(...c)-h||1,g=v=>i.left+v/(t.length-1||1)*s,x=v=>i.top+p-(v-h)/u*p,O=e.map((v,S)=>`${g(S)},${x(v.value)}`).join(" L "),lt=`M ${O}`,De=`M ${i.left},${i.top+p} L ${O} L ${g(t.length-1)},${i.top+p} Z`,Tt=[],Gt=5;for(let v=0;v<=Gt;v++)Tt.push(h+u*v/Gt);const Ie=Math.ceil(t.length/7);let L="";return L+=`<defs>
      <linearGradient id="areaGradient" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0%" stop-color="#ff5c5c" stop-opacity="0.3" />
        <stop offset="100%" stop-color="#ff5c5c" stop-opacity="0.05" />
      </linearGradient>
    </defs>`,Tt.forEach(v=>{L+=`<line x1="${i.left}" y1="${x(v)}" x2="${a-i.right}" y2="${x(v)}" stroke="#444" stroke-width="1" stroke-dasharray="4,4"/>`}),L+=`<path d="${De}" fill="url(#areaGradient)"/>`,L+=`<path d="${lt}" fill="none" stroke="#ff5c5c" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>`,e.forEach((v,S)=>{L+=`<circle cx="${g(S)}" cy="${x(v.value)}" r="4" fill="#ff5c5c" stroke="#1a1a1a" stroke-width="1"/>`}),Tt.forEach(v=>{const S=this._formatValue(v,this.metric);L+=`<text x="${i.left-10}" y="${x(v)+4}" text-anchor="end" fill="#aaa" font-size="11" font-family="system-ui, -apple-system, sans-serif" font-weight="500">${S}</text>`}),e.forEach((v,S)=>{if(S%Ie!==0&&S!==t.length-1)return;const At=v.date.slice(5);L+=`<text x="${g(S)}" y="${r-20}" text-anchor="middle" fill="#aaa" font-size="11" font-family="system-ui, -apple-system, sans-serif" font-weight="500">${At}</text>`}),n`
      <svg class="chart-svg" viewBox="0 0 ${a} ${r}" preserveAspectRatio="xMidYMid meet"
        @mousemove=${v=>{const S=v.currentTarget.getBoundingClientRect(),At=v.clientX-S.left,je=S.width/a,Ne=At/je-i.left,ct=Math.round(Ne/s*(t.length-1));if(ct>=0&&ct<t.length){const Et=e[ct];this.tooltipData={show:!0,x:g(ct),y:x(Et.value),date:Et.date,value:Et.rawValue,index:ct},this.requestUpdate()}}} @mouseleave=${()=>{this.tooltipData={...this.tooltipData,show:!1},this.requestUpdate()}}>
        ${Lt(L)}
        ${this.tooltipData.show?Lt(`<line class="tooltip-line" x1="${this.tooltipData.x}" y1="0" x2="${this.tooltipData.x}" y2="${r}" stroke="#ff5c5c" stroke-width="1" stroke-dasharray="4,4" opacity="0.6"/><circle class="tooltip-point" cx="${this.tooltipData.x}" cy="${this.tooltipData.y}" r="8" fill="#ff5c5c" stroke="#fff" stroke-width="3"/>`):null}
      </svg>
      
      <!-- Tooltip 浮框 -->
      ${this.tooltipData.show?n`
        <div class="tooltip" style="left:${this.tooltipData.x/800*100}%;top:${this.tooltipData.y/320*100}%;transform:translate(-50%,-130%)">
          <div class="tooltip-date">${this.tooltipData.date}</div>
          <div class="tooltip-value">
            <span class="tooltip-label">${this._getMetricLabel()}:</span>
            <span>${this._formatValue(this.tooltipData.value,this.metric)}</span>
          </div>
        </div>
      `:""}
    `}_getMetricLabel(){switch(this.metric){case"sales_count":return"销量";case"rank":return"排名";case"rating":return"评分";case"price":return"价格";default:return""}}_getMetricHint(){switch(this.metric){case"sales_count":return"显示商品每日销量变化趋势";case"rank":return"显示商品排名变化趋势";case"rating":return"显示商品评分变化趋势";case"price":return"显示商品价格变化趋势";default:return""}}_renderPagination(){const t=[];let a=Math.max(1,this.pagination.page-Math.floor(2.5)),r=Math.min(this.pagination.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1)),a>1&&(t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),a>2&&t.push(n`<span style="color:var(--muted)">...</span>`));for(let i=a;i<=r;i++)t.push(n`
        <button class="page-btn ${i===this.pagination.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return r<this.pagination.pages&&(r<this.pagination.pages-1&&t.push(n`<span style="color:var(--muted)">...</span>`),t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(this.pagination.pages)}>${this.pagination.pages}</button>`)),n`<div class="pagination">${t}</div>`}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;const t=this.product.platform==="amazon"?[{key:"rank",label:"排名"},{key:"rating",label:"评分"},{key:"price",label:"价格"}]:[{key:"sales_count",label:"销量"},{key:"rating",label:"评分"},{key:"price",label:"价格"}],e=[{key:"7",label:"近7天"},{key:"15",label:"近15天"},{key:"30",label:"近1月"},{key:"90",label:"近3月"}];return n`
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
          ${e.map(a=>n`
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
              ${t.map(a=>n`
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
            ${this.details.map(a=>n`
              <tr>
                <td>${a.date}</td>
                <td style="max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${a.short_name||""}>${a.short_name||"-"}</td>
                <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title=${a.search_keyword||""}>${a.search_keyword||"-"}</td>
                <td>${a.rating!=null?a.rating.toFixed(1):"-"}</td>
                <td>${a.price!=null?`$${a.price.toFixed(2)}`:"-"}</td>
                <td>${a.sales_count!=null?this._formatValue(a.sales_count,"sales_count"):"-"}</td>
                <td>${a.events?a.events.split(", ").map(r=>n`<span class="event-tag">${r}</span>`):"-"}</td>
              </tr>
            `)}
          </tbody>
        </table>
        ${this.pagination.pages>1?this._renderPagination():""}
      </div>
    `}};br(z,"styles",$`
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
  `);A([T({type:String})],z.prototype,"ecomCode",2);A([l()],z.prototype,"loading",2);A([l()],z.prototype,"product",2);A([l()],z.prototype,"trend",2);A([l()],z.prototype,"details",2);A([l()],z.prototype,"pagination",2);A([l()],z.prototype,"timePreset",2);A([l()],z.prototype,"customStart",2);A([l()],z.prototype,"customEnd",2);A([l()],z.prototype,"metric",2);A([l()],z.prototype,"currentPage",2);A([l()],z.prototype,"tooltipData",2);z=A([_("ea-product-trend-page")],z);var Te=Object.defineProperty,mr=Object.getOwnPropertyDescriptor,fr=(o,t,e)=>t in o?Te(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,E=(o,t,e,a)=>{for(var r=a>1?void 0:a?mr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Te(t,e,r),r},xr=(o,t,e)=>fr(o,t+"",e);let C=class extends m{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"sourcingList",[]);d(this,"loading",!0);d(this,"search","");d(this,"page",1);d(this,"pages",0);d(this,"total",0);d(this,"stats",{total:0,products_linked:0,today_count:0,last_updated:null});d(this,"showModal",!1);d(this,"modalType","");d(this,"modalItem",null)}connectedCallback(){super.connectedCallback(),this.loadStats(),this.loadSourcing()}async loadStats(){try{const t=await fetch("/api/sourcing/stats");this.stats=await t.json(),console.log("[Sourcing] stats:",this.stats)}catch(t){console.error("加载统计失败:",t)}}async loadSourcing(){var t,e;try{const a=new URLSearchParams;a.set("page",String(this.page)),a.set("limit","20"),this.search&&a.set("search",this.search),this.ecomCode&&a.set("ecom_code",this.ecomCode),console.log("[Sourcing] 请求:",`/api/sourcing/list?${a}`);const i=await(await fetch(`/api/sourcing/list?${a}`)).json();console.log("[Sourcing] 响应:",i),this.sourcingList=i.data||[],this.total=((t=i.pagination)==null?void 0:t.total)||0,this.pages=((e=i.pagination)==null?void 0:e.pages)||0,this.loading=!1,console.log("[Sourcing] loading 设为 false, 触发 requestUpdate"),this.requestUpdate()}catch(a){console.error("加载货源失败:",a),this.sourcingList=[],this.loading=!1,this.requestUpdate()}}_onSearch(t){t.key==="Enter"&&(this.page=1,this.loadSourcing())}_onPageChange(t){this.page=t,this.loadSourcing(),window.scrollTo({top:0,behavior:"smooth"})}_formatPrice(t){return t?`¥${t.toFixed(2)}`:"-"}_formatDate(t){if(!t)return"-";const e=new Date(t);return`${e.getMonth()+1}/${e.getDate()} ${e.getHours()}:${String(e.getMinutes()).padStart(2,"0")}`}async _deleteSourcing(t,e){if(confirm("确定删除此货源记录？"))try{await fetch(`/api/sourcing/${t}/${e}`,{method:"DELETE"}),await Promise.all([this.loadStats(),this.loadSourcing()])}catch(a){console.error("删除失败:",a)}}_openProduct(t){t&&window.open(t,"_blank")}_showModal(t,e){console.log("[Sourcing] _showModal called:",t,e),this.modalType=t,this.modalItem=e,this.showModal=!0,this.requestUpdate()}_closeModal(){console.log("[Sourcing] _closeModal called"),this.showModal=!1,this.modalType="",this.modalItem=null,this.requestUpdate()}_confirmModal(){console.log(`[Sourcing] 确认生成: ${this.modalType}`,this.modalItem),this._closeModal(),alert(this.modalType==="video"?"视频生成功能开发中...":"详情图生成功能开发中...")}async _uploadToTikTok(t){console.log("[Sourcing] _uploadToTikTok called, item:",t);try{console.log("[Sourcing] Checking TikTok connection...");const a=await(await fetch("/api/tiktok/status")).json();if(console.log("[Sourcing] TikTok status:",a),!a.connected){console.log("[Sourcing] Chrome not running, starting...");const r=await fetch("/api/tiktok/ensure-chrome",{method:"POST"}),i=await r.json();if(console.log("[Sourcing] Ensure Chrome result:",i),!r.ok){alert("Failed to start Chrome. Please start manually.");return}if(await new Promise(p=>setTimeout(p,2e3)),(await fetch("/api/tiktok/open-login",{method:"POST"})).ok){alert(`Chrome started!
Please login to TikTok Shop, then click TikTok button again.`);return}}}catch(e){console.error("[Sourcing] Status check failed:",e),alert("Server connection failed");return}console.log("[Sourcing] 开始上传到 TikTok:",t.ecom_code);try{const a=await(await fetch(`/api/tiktok/upload/${t.ecom_code}`,{method:"POST"})).json();console.log("[Sourcing] 上传结果:",a),a.success?alert(`上传成功!
请在 TikTok Shop 后台检查草稿商品`):alert(`上传失败: ${a.message}`)}catch(e){console.error("[Sourcing] 上传失败:",e),alert("上传失败，请检查服务器连接")}}_renderModal(){var r,i;if(!this.showModal)return null;const t=this.modalType==="video"?"🎬":"🖼️",e=this.modalType==="video"?"生成宣传视频":"生成详情图",a=this.modalType==="video"?"将使用货源商品信息自动生成宣传视频，用于社交平台推广":"将使用货源商品详情自动生成电商详情图，用于商品上架";return n`
      <div class="modal-overlay" @click=${s=>{s.target===s.currentTarget&&this._closeModal()}}>
        <div class="modal-content">
          <div class="modal-icon">${t}</div>
          <div class="modal-title">${e}</div>
          <div class="modal-desc">${a}</div>
          <div class="modal-product">
            <img 
              class="modal-product-thumb" 
              src=${((r=this.modalItem)==null?void 0:r.image_url)||'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect fill="%23ddd" width="40" height="40"/></svg>'}
              onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect fill=%22%23ddd%22 width=%2240%22 height=%2240%22/></svg>'"
            >
            <div class="modal-product-title">${((i=this.modalItem)==null?void 0:i.title)||"未知商品"}</div>
          </div>
          <div class="modal-buttons">
            <button class="modal-btn modal-btn-cancel" @click=${this._closeModal}>取消</button>
            <button class="modal-btn modal-btn-confirm" @click=${this._confirmModal}>确认生成</button>
          </div>
        </div>
      </div>
    `}_renderPagination(){if(this.pages<=1)return null;const t=[],e=5;let a=Math.max(1,this.page-Math.floor(e/2)),r=Math.min(this.pages,a+e-1);r-a<e-1&&(a=Math.max(1,r-e+1)),t.push(n`
      <button class="page-btn" ?disabled=${this.page===1} @click=${()=>this._onPageChange(this.page-1)}>
        ‹
      </button>
    `);for(let i=a;i<=r;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>
          ${i}
        </button>
      `);return t.push(n`
      <button class="page-btn" ?disabled=${this.page===this.pages} @click=${()=>this._onPageChange(this.page+1)}>
        ›
      </button>
    `),n`
      <div class="pagination">
        <span class="page-info">共 ${this.total} 条</span>
        ${t}
      </div>
    `}render(){return console.log("[Sourcing] render called, loading=",this.loading,"list=",this.sourcingList.length),this.loading?n`<div class="loading-state">加载中...</div>`:n`
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
        ${this.ecomCode?n`
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
      ${this.sourcingList.length===0?n`
        <div class="empty-state">
          <div class="empty-icon">📦</div>
          <div class="empty-title">暂无货源记录</div>
          <div class="empty-desc">点击商品库的「1688」按钮开始采集货源</div>
        </div>
      `:n`
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
              ${this.sourcingList.map(t=>n`
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
                      TikTok
                    </button>
                    <button class="action-btn action-btn-video" @click=${()=>this._showModal("video",t)}>
                      视频
                    </button>
                    <button class="action-btn action-btn-detail" @click=${()=>this._showModal("detail",t)}>
                      详情图
                    </button>
                    <button class="action-btn action-btn-view" @click=${()=>this._openProduct(t.product_url)}>
                      查看
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
    `}};xr(C,"styles",$`
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
  `);E([T({type:String})],C.prototype,"ecomCode",2);E([l()],C.prototype,"sourcingList",2);E([l()],C.prototype,"loading",2);E([l()],C.prototype,"search",2);E([l()],C.prototype,"page",2);E([l()],C.prototype,"pages",2);E([l()],C.prototype,"total",2);E([l()],C.prototype,"stats",2);E([l()],C.prototype,"showModal",2);E([l()],C.prototype,"modalType",2);E([l()],C.prototype,"modalItem",2);C=E([_("ea-sourcing")],C);var Ae=Object.defineProperty,yr=Object.getOwnPropertyDescriptor,$r=(o,t,e)=>t in o?Ae(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,et=(o,t,e,a)=>{for(var r=a>1?void 0:a?yr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Ae(t,e,r),r},_r=(o,t,e)=>$r(o,t+"",e);const Ee="/api";async function Oe(o,t){const e=await fetch(o,t);if(!e.ok){const a=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(a.detail||`HTTP ${e.status}`)}return e.json()}async function wr(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return Oe(`${Ee}/translation-logs?${t}`)}async function kr(){return Oe(`${Ee}/translation-logs/stats`)}let N=class extends m{constructor(){super(...arguments);d(this,"logs",[]);d(this,"stats",null);d(this,"loading",!0);d(this,"page",1);d(this,"pages",0);d(this,"statusFilter","")}async connectedCallback(){super.connectedCallback(),await this.loadData()}async loadData(){this.loading=!0;try{const[t,e]=await Promise.all([wr({page:this.page,limit:20,status:this.statusFilter||void 0}),kr()]);this.logs=t.data,this.pages=t.pagination.pages,this.stats=e}catch(t){console.error("Failed to load translation logs:",t)}finally{this.loading=!1,this.requestUpdate()}}_onStatusFilter(t){this.statusFilter=t.target.value,this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_formatDateTime(t){return t?new Date(t).toLocaleString("zh-CN",{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit"}):"-"}_renderStatusBadge(t){return n`
      <span class="status-badge ${t}">
        <span class="status-dot"></span>
        ${{pending:"等待中",running:"运行中",completed:"已完成",failed:"失败"}[t]||t}
      </span>
    `}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),r=Math.min(this.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1)),a>1&&t.push(n`
        <button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>
        ${a>2?n`<span style="color:var(--muted)">...</span>`:""}
      `);for(let i=a;i<=r;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return r<this.pages&&t.push(n`
        ${r<this.pages-1?n`<span style="color:var(--muted)">...</span>`:""}
        <button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>
      `),n`<div class="pagination">${t}</div>`}render(){return n`
      <h2>翻译日志</h2>
      
      ${this.stats?n`
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
      
      ${this.loading?n`
        <div class="loading">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
      `:this.logs.length===0?n`
        <div class="table-container">
          <div class="empty-state">
            <div class="empty-icon">📝</div>
            <p>暂无翻译日志</p>
          </div>
        </div>
      `:n`
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
              ${this.logs.map(t=>n`
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
    `}};_r(N,"styles",$`
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
  `);et([l()],N.prototype,"logs",2);et([l()],N.prototype,"stats",2);et([l()],N.prototype,"loading",2);et([l()],N.prototype,"page",2);et([l()],N.prototype,"pages",2);et([l()],N.prototype,"statusFilter",2);N=et([_("ea-translation-logs")],N);var Me=Object.defineProperty,Pr=Object.getOwnPropertyDescriptor,Sr=(o,t,e)=>t in o?Me(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Ct=(o,t,e,a)=>{for(var r=a>1?void 0:a?Pr(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Me(t,e,r),r},zr=(o,t,e)=>Sr(o,t+"",e);const dt=new Set;let Z="dashboard";window.ecomagentNavigate=o=>{Z=o,dt.forEach(t=>t(o))};window.ecomagentGetCurrentPage=()=>Z;window.ecomagentOnPageChange=o=>{dt.add(o)};window.ecomagentOpenTrend=(o,t="product-master")=>{sessionStorage.setItem("trend-source-page",t),sessionStorage.setItem("trend-source-state",JSON.stringify({page:Z,scrollY:window.scrollY})),Z="product-trend",sessionStorage.setItem("trend-ecom-code",o),dt.forEach(e=>e("product-trend"))};window.ecomagentNavigateToSourcing=o=>{Z="sourcing",o?sessionStorage.setItem("sourcing-ecom-code",o):sessionStorage.removeItem("sourcing-ecom-code"),dt.forEach(t=>t("sourcing"))};window.ecomagentNavigateDirectToSourcing=()=>{sessionStorage.removeItem("sourcing-ecom-code"),Z="sourcing",dt.forEach(o=>o("sourcing"))};let it=class extends m{constructor(){super();d(this,"_page",Z);d(this,"_trendCode","");d(this,"_sourcingCode","");dt.add(t=>{this._page=t,t==="product-trend"&&(this._trendCode=sessionStorage.getItem("trend-ecom-code")||""),t==="sourcing"&&(this._sourcingCode=sessionStorage.getItem("sourcing-ecom-code")||""),this.requestUpdate()})}connectedCallback(){super.connectedCallback();const t=localStorage.getItem("theme")||"dark";document.body.setAttribute("data-theme-mode",t)}_renderPage(){switch(this._page){case"dashboard":return n`<ea-dashboard></ea-dashboard>`;case"settings":return n`<ea-settings></ea-settings>`;case"product-master":return n`<ea-product-master></ea-product-master>`;case"tracking":return n`<ea-tracking></ea-tracking>`;case"cross-platform":return n`<ea-cross-platform></ea-cross-platform>`;case"today-top":return n`<ea-today-top></ea-today-top>`;case"raw-data":return n`<ea-raw-data></ea-raw-data>`;case"export":return n`<ea-export></ea-export>`;case"product-trend":return n`<ea-product-trend-page ecomCode=${this._trendCode}></ea-product-trend-page>`;case"sourcing":return n`<ea-sourcing ecomCode=${this._sourcingCode}></ea-sourcing>`;case"translation-logs":return n`<ea-translation-logs></ea-translation-logs>`;default:return n`<div style="padding:24px;color:var(--muted)">未知页面</div>`}}render(){return this._page==="product-trend"?n`
        <ea-layout currentPage=${this._page}>
          <div style="padding:24px">${this._renderPage()}</div>
        </ea-layout>
      `:n`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `}};zr(it,"styles",$`:host { display: block; min-height: 100vh; }`);Ct([l()],it.prototype,"_page",2);Ct([l()],it.prototype,"_trendCode",2);Ct([l()],it.prototype,"_sourcingCode",2);it=Ct([_("ecomagent-app")],it);console.log("EcomAgent UI loaded");

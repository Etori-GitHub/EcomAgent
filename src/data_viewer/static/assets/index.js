var le=Object.defineProperty;var ce=(o,t,e)=>t in o?le(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e;var d=(o,t,e)=>ce(o,typeof t!="symbol"?t+"":t,e);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const r of document.querySelectorAll('link[rel="modulepreload"]'))a(r);new MutationObserver(r=>{for(const i of r)if(i.type==="childList")for(const s of i.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&a(s)}).observe(document,{childList:!0,subtree:!0});function e(r){const i={};return r.integrity&&(i.integrity=r.integrity),r.referrerPolicy&&(i.referrerPolicy=r.referrerPolicy),r.crossOrigin==="use-credentials"?i.credentials="include":r.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function a(r){if(r.ep)return;r.ep=!0;const i=e(r);fetch(r.href,i)}})();/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const it=globalThis,xt=it.ShadowRoot&&(it.ShadyCSS===void 0||it.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,$t=Symbol(),At=new WeakMap;let Rt=class{constructor(t,e,a){if(this._$cssResult$=!0,a!==$t)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const e=this.t;if(xt&&t===void 0){const a=e!==void 0&&e.length===1;a&&(t=At.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),a&&At.set(e,t))}return t}toString(){return this.cssText}};const pe=o=>new Rt(typeof o=="string"?o:o+"",void 0,$t),m=(o,...t)=>{const e=o.length===1?o[0]:t.reduce((a,r,i)=>a+(s=>{if(s._$cssResult$===!0)return s.cssText;if(typeof s=="number")return s;throw Error("Value passed to 'css' function must be a 'css' function result: "+s+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(r)+o[i+1],o[0]);return new Rt(e,o,$t)},he=(o,t)=>{if(xt)o.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(const e of t){const a=document.createElement("style"),r=it.litNonce;r!==void 0&&a.setAttribute("nonce",r),a.textContent=e.cssText,o.appendChild(a)}},Ct=xt?o=>o:o=>o instanceof CSSStyleSheet?(t=>{let e="";for(const a of t.cssRules)e+=a.cssText;return pe(e)})(o):o;/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const{is:ue,defineProperty:ge,getOwnPropertyDescriptor:ve,getOwnPropertyNames:be,getOwnPropertySymbols:fe,getPrototypeOf:me}=Object,S=globalThis,St=S.trustedTypes,xe=St?St.emptyScript:"",vt=S.reactiveElementPolyfillSupport,Z=(o,t)=>o,st={toAttribute(o,t){switch(t){case Boolean:o=o?xe:null;break;case Object:case Array:o=o==null?o:JSON.stringify(o)}return o},fromAttribute(o,t){let e=o;switch(t){case Boolean:e=o!==null;break;case Number:e=o===null?null:Number(o);break;case Object:case Array:try{e=JSON.parse(o)}catch{e=null}}return e}},yt=(o,t)=>!ue(o,t),Et={attribute:!0,type:String,converter:st,reflect:!1,useDefault:!1,hasChanged:yt};Symbol.metadata??(Symbol.metadata=Symbol("metadata")),S.litPropertyMetadata??(S.litPropertyMetadata=new WeakMap);let F=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??(this.l=[])).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Et){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const a=Symbol(),r=this.getPropertyDescriptor(t,a,e);r!==void 0&&ge(this.prototype,t,r)}}static getPropertyDescriptor(t,e,a){const{get:r,set:i}=ve(this.prototype,t)??{get(){return this[e]},set(s){this[e]=s}};return{get:r,set(s){const c=r==null?void 0:r.call(this);i==null||i.call(this,s),this.requestUpdate(t,c,a)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Et}static _$Ei(){if(this.hasOwnProperty(Z("elementProperties")))return;const t=me(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(Z("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(Z("properties"))){const e=this.properties,a=[...be(e),...fe(e)];for(const r of a)this.createProperty(r,e[r])}const t=this[Symbol.metadata];if(t!==null){const e=litPropertyMetadata.get(t);if(e!==void 0)for(const[a,r]of e)this.elementProperties.set(a,r)}this._$Eh=new Map;for(const[e,a]of this.elementProperties){const r=this._$Eu(e,a);r!==void 0&&this._$Eh.set(r,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const a=new Set(t.flat(1/0).reverse());for(const r of a)e.unshift(Ct(r))}else t!==void 0&&e.push(Ct(t));return e}static _$Eu(t,e){const a=e.attribute;return a===!1?void 0:typeof a=="string"?a:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){var t;this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),(t=this.constructor.l)==null||t.forEach(e=>e(this))}addController(t){var e;(this._$EO??(this._$EO=new Set)).add(t),this.renderRoot!==void 0&&this.isConnected&&((e=t.hostConnected)==null||e.call(t))}removeController(t){var e;(e=this._$EO)==null||e.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const a of e.keys())this.hasOwnProperty(a)&&(t.set(a,this[a]),delete this[a]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return he(t,this.constructor.elementStyles),t}connectedCallback(){var t;this.renderRoot??(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostConnected)==null?void 0:a.call(e)})}enableUpdating(t){}disconnectedCallback(){var t;(t=this._$EO)==null||t.forEach(e=>{var a;return(a=e.hostDisconnected)==null?void 0:a.call(e)})}attributeChangedCallback(t,e,a){this._$AK(t,a)}_$ET(t,e){var i;const a=this.constructor.elementProperties.get(t),r=this.constructor._$Eu(t,a);if(r!==void 0&&a.reflect===!0){const s=(((i=a.converter)==null?void 0:i.toAttribute)!==void 0?a.converter:st).toAttribute(e,a.type);this._$Em=t,s==null?this.removeAttribute(r):this.setAttribute(r,s),this._$Em=null}}_$AK(t,e){var i,s;const a=this.constructor,r=a._$Eh.get(t);if(r!==void 0&&this._$Em!==r){const c=a.getPropertyOptions(r),p=typeof c.converter=="function"?{fromAttribute:c.converter}:((i=c.converter)==null?void 0:i.fromAttribute)!==void 0?c.converter:st;this._$Em=r;const u=p.fromAttribute(e,c.type);this[r]=u??((s=this._$Ej)==null?void 0:s.get(r))??u,this._$Em=null}}requestUpdate(t,e,a,r=!1,i){var s;if(t!==void 0){const c=this.constructor;if(r===!1&&(i=this[t]),a??(a=c.getPropertyOptions(t)),!((a.hasChanged??yt)(i,e)||a.useDefault&&a.reflect&&i===((s=this._$Ej)==null?void 0:s.get(t))&&!this.hasAttribute(c._$Eu(t,a))))return;this.C(t,e,a)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:a,reflect:r,wrapped:i},s){a&&!(this._$Ej??(this._$Ej=new Map)).has(t)&&(this._$Ej.set(t,s??e??this[t]),i!==!0||s!==void 0)||(this._$AL.has(t)||(this.hasUpdated||a||(e=void 0),this._$AL.set(t,e)),r===!0&&this._$Em!==t&&(this._$Eq??(this._$Eq=new Set)).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var a;if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??(this.renderRoot=this.createRenderRoot()),this._$Ep){for(const[i,s]of this._$Ep)this[i]=s;this._$Ep=void 0}const r=this.constructor.elementProperties;if(r.size>0)for(const[i,s]of r){const{wrapped:c}=s,p=this[i];c!==!0||this._$AL.has(i)||p===void 0||this.C(i,void 0,s,p)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),(a=this._$EO)==null||a.forEach(r=>{var i;return(i=r.hostUpdate)==null?void 0:i.call(r)}),this.update(e)):this._$EM()}catch(r){throw t=!1,this._$EM(),r}t&&this._$AE(e)}willUpdate(t){}_$AE(t){var e;(e=this._$EO)==null||e.forEach(a=>{var r;return(r=a.hostUpdated)==null?void 0:r.call(a)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&(this._$Eq=this._$Eq.forEach(e=>this._$ET(e,this[e]))),this._$EM()}updated(t){}firstUpdated(t){}};F.elementStyles=[],F.shadowRootOptions={mode:"open"},F[Z("elementProperties")]=new Map,F[Z("finalized")]=new Map,vt==null||vt({ReactiveElement:F}),(S.reactiveElementVersions??(S.reactiveElementVersions=[])).push("2.1.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const K=globalThis,Ot=o=>o,nt=K.trustedTypes,Tt=nt?nt.createPolicy("lit-html",{createHTML:o=>o}):void 0,Ft="$lit$",C=`lit$${Math.random().toFixed(9).slice(2)}$`,Ht="?"+C,$e=`<${Ht}>`,j=document,X=()=>j.createComment(""),Q=o=>o===null||typeof o!="object"&&typeof o!="function",_t=Array.isArray,ye=o=>_t(o)||typeof(o==null?void 0:o[Symbol.iterator])=="function",bt=`[ 	
\f\r]`,W=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Dt=/-->/g,Mt=/>/g,I=RegExp(`>|${bt}(?:([^\\s"'>=/]+)(${bt}*=${bt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),It=/'/g,Nt=/"/g,Bt=/^(?:script|style|textarea|title)$/i,_e=o=>(t,...e)=>({_$litType$:o,strings:t,values:e}),n=_e(1),H=Symbol.for("lit-noChange"),v=Symbol.for("lit-nothing"),Ut=new WeakMap,N=j.createTreeWalker(j,129);function qt(o,t){if(!_t(o)||!o.hasOwnProperty("raw"))throw Error("invalid template strings array");return Tt!==void 0?Tt.createHTML(t):t}const ke=(o,t)=>{const e=o.length-1,a=[];let r,i=t===2?"<svg>":t===3?"<math>":"",s=W;for(let c=0;c<e;c++){const p=o[c];let u,b,h=-1,P=0;for(;P<p.length&&(s.lastIndex=P,b=s.exec(p),b!==null);)P=s.lastIndex,s===W?b[1]==="!--"?s=Dt:b[1]!==void 0?s=Mt:b[2]!==void 0?(Bt.test(b[2])&&(r=RegExp("</"+b[2],"g")),s=I):b[3]!==void 0&&(s=I):s===I?b[0]===">"?(s=r??W,h=-1):b[1]===void 0?h=-2:(h=s.lastIndex-b[2].length,u=b[1],s=b[3]===void 0?I:b[3]==='"'?Nt:It):s===Nt||s===It?s=I:s===Dt||s===Mt?s=W:(s=I,r=void 0);const A=s===I&&o[c+1].startsWith("/>")?" ":"";i+=s===W?p+$e:h>=0?(a.push(u),p.slice(0,h)+Ft+p.slice(h)+C+A):p+C+(h===-2?c:A)}return[qt(o,i+(o[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),a]};class Y{constructor({strings:t,_$litType$:e},a){let r;this.parts=[];let i=0,s=0;const c=t.length-1,p=this.parts,[u,b]=ke(t,e);if(this.el=Y.createElement(u,a),N.currentNode=this.el.content,e===2||e===3){const h=this.el.content.firstChild;h.replaceWith(...h.childNodes)}for(;(r=N.nextNode())!==null&&p.length<c;){if(r.nodeType===1){if(r.hasAttributes())for(const h of r.getAttributeNames())if(h.endsWith(Ft)){const P=b[s++],A=r.getAttribute(h).split(C),ot=/([.?@])?(.*)/.exec(P);p.push({type:1,index:i,name:ot[2],strings:A,ctor:ot[1]==="."?Pe:ot[1]==="?"?ze:ot[1]==="@"?Ae:ht}),r.removeAttribute(h)}else h.startsWith(C)&&(p.push({type:6,index:i}),r.removeAttribute(h));if(Bt.test(r.tagName)){const h=r.textContent.split(C),P=h.length-1;if(P>0){r.textContent=nt?nt.emptyScript:"";for(let A=0;A<P;A++)r.append(h[A],X()),N.nextNode(),p.push({type:2,index:++i});r.append(h[P],X())}}}else if(r.nodeType===8)if(r.data===Ht)p.push({type:2,index:i});else{let h=-1;for(;(h=r.data.indexOf(C,h+1))!==-1;)p.push({type:7,index:i}),h+=C.length-1}i++}}static createElement(t,e){const a=j.createElement("template");return a.innerHTML=t,a}}function B(o,t,e=o,a){var s,c;if(t===H)return t;let r=a!==void 0?(s=e._$Co)==null?void 0:s[a]:e._$Cl;const i=Q(t)?void 0:t._$litDirective$;return(r==null?void 0:r.constructor)!==i&&((c=r==null?void 0:r._$AO)==null||c.call(r,!1),i===void 0?r=void 0:(r=new i(o),r._$AT(o,e,a)),a!==void 0?(e._$Co??(e._$Co=[]))[a]=r:e._$Cl=r),r!==void 0&&(t=B(o,r._$AS(o,t.values),r,a)),t}class we{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:a}=this._$AD,r=((t==null?void 0:t.creationScope)??j).importNode(e,!0);N.currentNode=r;let i=N.nextNode(),s=0,c=0,p=a[0];for(;p!==void 0;){if(s===p.index){let u;p.type===2?u=new at(i,i.nextSibling,this,t):p.type===1?u=new p.ctor(i,p.name,p.strings,this,t):p.type===6&&(u=new Ce(i,this,t)),this._$AV.push(u),p=a[++c]}s!==(p==null?void 0:p.index)&&(i=N.nextNode(),s++)}return N.currentNode=j,r}p(t){let e=0;for(const a of this._$AV)a!==void 0&&(a.strings!==void 0?(a._$AI(t,a,e),e+=a.strings.length-2):a._$AI(t[e])),e++}}class at{get _$AU(){var t;return((t=this._$AM)==null?void 0:t._$AU)??this._$Cv}constructor(t,e,a,r){this.type=2,this._$AH=v,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=a,this.options=r,this._$Cv=(r==null?void 0:r.isConnected)??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return e!==void 0&&(t==null?void 0:t.nodeType)===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=B(this,t,e),Q(t)?t===v||t==null||t===""?(this._$AH!==v&&this._$AR(),this._$AH=v):t!==this._$AH&&t!==H&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):ye(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==v&&Q(this._$AH)?this._$AA.nextSibling.data=t:this.T(j.createTextNode(t)),this._$AH=t}$(t){var i;const{values:e,_$litType$:a}=t,r=typeof a=="number"?this._$AC(t):(a.el===void 0&&(a.el=Y.createElement(qt(a.h,a.h[0]),this.options)),a);if(((i=this._$AH)==null?void 0:i._$AD)===r)this._$AH.p(e);else{const s=new we(r,this),c=s.u(this.options);s.p(e),this.T(c),this._$AH=s}}_$AC(t){let e=Ut.get(t.strings);return e===void 0&&Ut.set(t.strings,e=new Y(t)),e}k(t){_t(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let a,r=0;for(const i of t)r===e.length?e.push(a=new at(this.O(X()),this.O(X()),this,this.options)):a=e[r],a._$AI(i),r++;r<e.length&&(this._$AR(a&&a._$AB.nextSibling,r),e.length=r)}_$AR(t=this._$AA.nextSibling,e){var a;for((a=this._$AP)==null?void 0:a.call(this,!1,!0,e);t!==this._$AB;){const r=Ot(t).nextSibling;Ot(t).remove(),t=r}}setConnected(t){var e;this._$AM===void 0&&(this._$Cv=t,(e=this._$AP)==null||e.call(this,t))}}class ht{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,a,r,i){this.type=1,this._$AH=v,this._$AN=void 0,this.element=t,this.name=e,this._$AM=r,this.options=i,a.length>2||a[0]!==""||a[1]!==""?(this._$AH=Array(a.length-1).fill(new String),this.strings=a):this._$AH=v}_$AI(t,e=this,a,r){const i=this.strings;let s=!1;if(i===void 0)t=B(this,t,e,0),s=!Q(t)||t!==this._$AH&&t!==H,s&&(this._$AH=t);else{const c=t;let p,u;for(t=i[0],p=0;p<i.length-1;p++)u=B(this,c[a+p],e,p),u===H&&(u=this._$AH[p]),s||(s=!Q(u)||u!==this._$AH[p]),u===v?t=v:t!==v&&(t+=(u??"")+i[p+1]),this._$AH[p]=u}s&&!r&&this.j(t)}j(t){t===v?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class Pe extends ht{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===v?void 0:t}}class ze extends ht{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==v)}}class Ae extends ht{constructor(t,e,a,r,i){super(t,e,a,r,i),this.type=5}_$AI(t,e=this){if((t=B(this,t,e,0)??v)===H)return;const a=this._$AH,r=t===v&&a!==v||t.capture!==a.capture||t.once!==a.once||t.passive!==a.passive,i=t!==v&&(a===v||r);r&&this.element.removeEventListener(this.name,this,a),i&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){var e;typeof this._$AH=="function"?this._$AH.call(((e=this.options)==null?void 0:e.host)??this.element,t):this._$AH.handleEvent(t)}}class Ce{constructor(t,e,a){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=a}get _$AU(){return this._$AM._$AU}_$AI(t){B(this,t)}}const ft=K.litHtmlPolyfillSupport;ft==null||ft(Y,at),(K.litHtmlVersions??(K.litHtmlVersions=[])).push("3.3.2");const Se=(o,t,e)=>{const a=(e==null?void 0:e.renderBefore)??t;let r=a._$litPart$;if(r===void 0){const i=(e==null?void 0:e.renderBefore)??null;a._$litPart$=r=new at(t.insertBefore(X(),i),i,void 0,e??{})}return r._$AI(o),r};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const U=globalThis;class g extends F{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e;const t=super.createRenderRoot();return(e=this.renderOptions).renderBefore??(e.renderBefore=t.firstChild),t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=Se(e,this.renderRoot,this.renderOptions)}connectedCallback(){var t;super.connectedCallback(),(t=this._$Do)==null||t.setConnected(!0)}disconnectedCallback(){var t;super.disconnectedCallback(),(t=this._$Do)==null||t.setConnected(!1)}render(){return H}}var Lt;g._$litElement$=!0,g.finalized=!0,(Lt=U.litElementHydrateSupport)==null||Lt.call(U,{LitElement:g});const mt=U.litElementPolyfillSupport;mt==null||mt({LitElement:g});(U.litElementVersions??(U.litElementVersions=[])).push("4.2.2");/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const x=o=>(t,e)=>{e!==void 0?e.addInitializer(()=>{customElements.define(o,t)}):customElements.define(o,t)};/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */const Ee={attribute:!0,type:String,converter:st,reflect:!1,hasChanged:yt},Oe=(o=Ee,t,e)=>{const{kind:a,metadata:r}=e;let i=globalThis.litPropertyMetadata.get(r);if(i===void 0&&globalThis.litPropertyMetadata.set(r,i=new Map),a==="setter"&&((o=Object.create(o)).wrapped=!0),i.set(e.name,o),a==="accessor"){const{name:s}=e;return{set(c){const p=t.get.call(this);t.set.call(this,c),this.requestUpdate(s,p,o,!0,c)},init(c){return c!==void 0&&this.C(s,void 0,o,c),c}}}if(a==="setter"){const{name:s}=e;return function(c){const p=this[s];t.call(this,c),this.requestUpdate(s,p,o,!0,c)}}throw Error("Unsupported decorator location: "+a)};function k(o){return(t,e)=>typeof e=="object"?Oe(o,t,e):((a,r,i)=>{const s=r.hasOwnProperty(i);return r.constructor.createProperty(i,a),s?Object.getOwnPropertyDescriptor(r,i):void 0})(o,t,e)}/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */function l(o){return k({...o,state:!0,attribute:!1})}var Vt=Object.defineProperty,Te=Object.getOwnPropertyDescriptor,De=(o,t,e)=>t in o?Vt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Jt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Te(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Vt(t,e,r),r},Me=(o,t,e)=>De(o,t+"",e);const Ie=[{group:"Main",items:[{id:"dashboard",icon:"grid",label:"数据概览"},{id:"product-master",icon:"box",label:"商品总库"},{id:"tracking",icon:"target",label:"商品追踪"},{id:"cross-platform",icon:"sync",label:"跨平台分析"}]},{group:"平台数据",items:[{id:"today-top",icon:"star",label:"今日TOP榜"},{id:"raw-data",icon:"database",label:"原始数据"}]},{group:"配置",items:[{id:"export",icon:"download",label:"数据导出"},{id:"settings",icon:"settings",label:"系统设置"}]}],Ne={grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',box:'<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',target:'<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',sync:'<path d="M16 3h5v5M8 21H3v-5M21 3l-7 7M3 21l7-7"/>',star:'<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',database:'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',download:'<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',settings:'<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>'};let dt=class extends g{constructor(){super();d(this,"collapsed",!1);d(this,"_currentPage","dashboard");window.ecomagentOnPageChange&&window.ecomagentOnPageChange(t=>{this._currentPage=t,this.requestUpdate()}),window.ecomagentGetCurrentPage&&(this._currentPage=window.ecomagentGetCurrentPage())}_onNavClick(t){window.ecomagentNavigate&&window.ecomagentNavigate(t)}_onToggle(){this.collapsed=!this.collapsed,this.requestUpdate("collapsed")}render(){const t=this._currentPage;return n`
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
        ${Ie.map(e=>n`
          <div class="nav-group">
            <div class="nav-group-header"><span class="nav-group-title">${e.group}</span></div>
            <ul class="nav-items">
              ${e.items.map(a=>n`
                <li class="nav-item ${t===a.id?"active":""}" @click=${()=>this._onNavClick(a.id)}>
                  <svg class="nav-icon" viewBox="0 0 24 24">${Ne[a.icon]}</svg>
                  <span class="nav-label">${a.label}</span>
                </li>
              `)}
            </ul>
          </div>
        `)}
      </div>
    `}};Me(dt,"styles",m`
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
  `);Jt([k({type:Boolean,reflect:!0})],dt.prototype,"collapsed",2);dt=Jt([x("ea-sidebar")],dt);var Gt=Object.defineProperty,Ue=Object.getOwnPropertyDescriptor,je=(o,t,e)=>t in o?Gt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,Wt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ue(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Gt(t,e,r),r},Le=(o,t,e)=>je(o,t+"",e);const Re={dashboard:{title:"数据概览",subtitle:"查看数据统计和概览"},"product-master":{title:"商品总库",subtitle:"统一管理所有平台商品"},tracking:{title:"商品追踪",subtitle:"追踪特定商品的价格、销量变化"},"cross-platform":{title:"跨平台分析",subtitle:"对比分析不同平台数据"},"today-top":{title:"今日TOP榜",subtitle:"各平台热销产品排行"},"raw-data":{title:"原始数据",subtitle:"查看和搜索原始数据"},export:{title:"数据导出",subtitle:"导出数据为 CSV 或 Excel"},settings:{title:"系统设置",subtitle:"配置数据源和其他选项"}};let lt=class extends g{constructor(){super(...arguments);d(this,"currentPage","dashboard")}toggleTheme(){const t=document.body,a=t.getAttribute("data-theme-mode")==="dark"?"light":"dark";t.setAttribute("data-theme-mode",a),localStorage.setItem("theme",a),this.requestUpdate()}render(){const{title:t,subtitle:e}=Re[this.currentPage],a=document.body.getAttribute("data-theme-mode")!=="light";return n`
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
    `}};Le(lt,"styles",m`
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
  `);Wt([k({type:String})],lt.prototype,"currentPage",2);lt=Wt([x("ea-header")],lt);var Zt=Object.defineProperty,Fe=Object.getOwnPropertyDescriptor,He=(o,t,e)=>t in o?Zt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,kt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Fe(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Zt(t,e,r),r},Be=(o,t,e)=>He(o,t+"",e);let tt=class extends g{constructor(){super(...arguments);d(this,"currentPage","dashboard");d(this,"sidebarCollapsed",!1)}render(){return n`
      <ea-sidebar ?collapsed=${this.sidebarCollapsed}></ea-sidebar>
      <main class="main-content">
        <ea-header .currentPage=${this.currentPage}></ea-header>
        <div class="content-body"><slot></slot></div>
      </main>
    `}};Be(tt,"styles",m`
    :host { display: flex; min-height: 100vh; }
    .main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
    .content-body { animation: fadeIn 0.3s ease; }
    @media (max-width: 1024px) { :host { flex-direction: column; } .main-content { padding: 16px; } }
  `);kt([k({type:String})],tt.prototype,"currentPage",2);kt([l()],tt.prototype,"sidebarCollapsed",2);tt=kt([x("ea-layout")],tt);const $="/api";async function y(o,t){const e=await fetch(o,t);if(!e.ok){const a=await e.json().catch(()=>({detail:"Request failed"}));throw new Error(a.detail||`HTTP ${e.status}`)}return e.json()}async function qe(){return y(`${$}/stats`)}async function Ve(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return y(`${$}/product-master?${t}`)}async function Je(o){return y(`${$}/tracked-products?ids=${o.join(",")}`)}async function Ge(){return y(`${$}/config/list`)}async function We(o){return y(`${$}/config/${o}`)}async function Ze(o,t){return y(`${$}/config/${o}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify({content:t})})}async function jt(){return y(`${$}/config/backups/list`)}async function Ke(o){return y(`${$}/config/backups/${o}/restore`,{method:"POST"})}async function Xe(o){return y(`${$}/config/backups/${o}`,{method:"DELETE"})}async function Qe(o,t=7){return y(`${$}/product-trend/${o}?days=${t}`)}async function Ye(){return y(`${$}/amazon/top-by-category`)}async function ta(){return y(`${$}/tiktok/top-by-category`)}async function ea(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return y(`${$}/amazon/products?${t}`)}async function aa(o){const t=new URLSearchParams(Object.entries(o).filter(([,e])=>e!==void 0&&e!=="").map(([e,a])=>[e,String(a)]));return y(`${$}/tiktok/products?${t}`)}async function ra(){return y(`${$}/cross-platform-analysis`)}var Kt=Object.defineProperty,oa=Object.getOwnPropertyDescriptor,ia=(o,t,e)=>t in o?Kt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,D=(o,t,e,a)=>{for(var r=a>1?void 0:a?oa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Kt(t,e,r),r},Xt=(o,t,e)=>ia(o,t+"",e);let ct=class extends g{constructor(){super(...arguments);d(this,"padding",16)}render(){return n`
      <slot name="header"></slot>
      <div class="card-content" style="--padding: ${this.padding}px">
        <slot></slot>
      </div>
    `}};Xt(ct,"styles",m`
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
  `);D([k({type:Number})],ct.prototype,"padding",2);ct=D([x("ea-card")],ct);let E=class extends g{constructor(){super(...arguments);d(this,"label","");d(this,"value","-");d(this,"icon","");d(this,"desc","");d(this,"color","")}render(){return n`
      <div class="stat-header">
        <div>
          <div class="stat-label">${this.label}</div>
          <div class="stat-value ${this.color}">${this.value}</div>
          ${this.desc?n`<div class="stat-desc">${this.desc}</div>`:""}
        </div>
        ${this.icon?n`<span class="stat-icon">${this.icon}</span>`:""}
      </div>
      <slot></slot>
    `}};Xt(E,"styles",m`
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
  `);D([k({type:String})],E.prototype,"label",2);D([k({type:String})],E.prototype,"value",2);D([k({type:String})],E.prototype,"icon",2);D([k({type:String})],E.prototype,"desc",2);D([k({type:String})],E.prototype,"color",2);E=D([x("ea-stat-card")],E);var Qt=Object.defineProperty,sa=Object.getOwnPropertyDescriptor,na=(o,t,e)=>t in o?Qt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,rt=(o,t,e,a)=>{for(var r=a>1?void 0:a?sa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Qt(t,e,r),r},da=(o,t,e)=>na(o,t+"",e);let L=class extends g{constructor(){super(...arguments);d(this,"stats",null);d(this,"loading",!0);d(this,"error","");d(this,"updating",null)}connectedCallback(){super.connectedCallback(),this.loadStats()}async loadStats(){this.loading=!0,this.error="";try{this.stats=await qe()}catch(t){this.error=t instanceof Error?t.message:String(t)}finally{this.loading=!1,this.requestUpdate()}}async _updatePlatform(t){this.updating=t;try{console.log(`开始抓取 ${t} 数据...`),await new Promise(e=>setTimeout(e,2e3)),alert(`${t} 数据抓取完成`),await this.loadStats()}catch(e){alert(`抓取失败: ${e}`)}finally{this.updating=null}}render(){if(this.loading)return n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`;if(this.error)return n`
        <div class="error-box">
          <p>加载失败: ${this.error}</p>
          <button class="retry-btn" @click=${this.loadStats}>重试</button>
        </div>
      `;if(!this.stats)return n`<div class="error-box"><p>无数据</p></div>`;const{amazon:t,tiktok:e,product_master:a}=this.stats;return n`
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
        <ea-stat-card label="总商品数" .value=${a.total.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="Amazon" .value=${a.amazon.toLocaleString()} color="accent"></ea-stat-card>
        <ea-stat-card label="TikTok" .value=${a.tiktok.toLocaleString()} color="info"></ea-stat-card>
        <ea-stat-card label="今日新增" .value=${a.today.toLocaleString()} color="ok"></ea-stat-card>
      </div>
    `}};da(L,"styles",m`
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
  `);rt([l()],L.prototype,"stats",2);rt([l()],L.prototype,"loading",2);rt([l()],L.prototype,"error",2);rt([l()],L.prototype,"updating",2);L=rt([x("ea-dashboard")],L);var Yt=Object.defineProperty,la=Object.getOwnPropertyDescriptor,ca=(o,t,e)=>t in o?Yt(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,R=(o,t,e,a)=>{for(var r=a>1?void 0:a?la(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&Yt(t,e,r),r},pa=(o,t,e)=>ca(o,t+"",e);let z=class extends g{constructor(){super(...arguments);d(this,"ecomCode","");d(this,"product",null);d(this,"trendData",[]);d(this,"loading",!0);d(this,"metric","rating");d(this,"days",7)}connectedCallback(){super.connectedCallback(),this.ecomCode&&this.loadTrendData()}updated(t){t.has("ecomCode")&&this.ecomCode&&this.loadTrendData()}async loadTrendData(){if(this.ecomCode){this.loading=!0;try{const t=await Qe(this.ecomCode,this.days);this.product=t.product,this.trendData=t.trend||[]}catch(t){console.error("Load trend error:",t)}finally{this.loading=!1,this.requestUpdate()}}}_onMetricChange(t){this.metric=t.target.value,this.requestUpdate()}_onDaysChange(t){const e=t.target.value;e!=="custom"&&(this.days=parseInt(e),this.loadTrendData())}_getMetricLabel(){switch(this.metric){case"price":return"价格";case"rating":return"评分";case"rank":return"排名"}}_renderChart(){if(this.trendData.length===0)return n`<div class="chart-empty">暂无数据</div>`;const t=this.trendData.map(i=>i[this.metric]).filter(i=>i!=null);if(t.length===0)return n`<div class="chart-empty">暂无${this._getMetricLabel()}数据</div>`;const e=Math.max(...t),a=Math.min(...t),r=e-a||1;return n`
      <div class="chart">
        ${this.trendData.map(i=>{const s=i[this.metric];if(s==null)return n`<div class="chart-bar" style="height:0"></div>`;const c=(s-a)/r*250+20;return n`
            <div class="chart-bar" style="height:${c}px">
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
      `}};pa(z,"styles",m`
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
  `);R([k({type:String})],z.prototype,"ecomCode",2);R([l()],z.prototype,"product",2);R([l()],z.prototype,"trendData",2);R([l()],z.prototype,"loading",2);R([l()],z.prototype,"metric",2);R([l()],z.prototype,"days",2);z=R([x("ea-product-trend")],z);var te=Object.defineProperty,ha=Object.getOwnPropertyDescriptor,ua=(o,t,e)=>t in o?te(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,_=(o,t,e,a)=>{for(var r=a>1?void 0:a?ha(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&te(t,e,r),r},ga=(o,t,e)=>ua(o,t+"",e);let f=class extends g{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"page",1);d(this,"total",0);d(this,"pages",0);d(this,"stats",{});d(this,"search","");d(this,"platform","");d(this,"category","");d(this,"trackedIds",new Set);d(this,"showTrend",!1);d(this,"trendCode","")}connectedCallback(){super.connectedCallback(),this.loadTracked(),this.loadData()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t)))}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadData(){this.loading=!0,console.log("=== ProductMaster: Loading data ===");try{const t=await Ve({page:this.page,limit:20,search:this.search,platform:this.platform,category:this.category});console.log("=== ProductMaster: Data loaded ===",t),this.products=t.data,this.total=t.pagination.total,this.pages=t.pagination.pages,this.stats=t.stats}catch(t){console.error("=== ProductMaster: Error ===",t)}finally{this.loading=!1,this.requestUpdate()}}_onSearch(){this.page=1,this.loadData()}_onInputChange(t,e){this[e]=t.target.value}_onPageChange(t){this.page=t,this.loadData()}_toggleTrack(t){this.trackedIds.has(t)?this.trackedIds.delete(t):this.trackedIds.add(t),this.saveTracked(),this.requestUpdate()}_showTrendModal(t){this.trendCode=t,this.showTrend=!0}_closeTrendModal(){this.showTrend=!1,this.trendCode=""}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),r=Math.min(this.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1)),a>1&&(t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(1)}>1</button>`),a>2&&t.push(n`<span style="color:var(--muted)">...</span>`));for(let i=a;i<=r;i++)t.push(n`
        <button class="page-btn ${i===this.page?"active":""}" @click=${()=>this._onPageChange(i)}>${i}</button>
      `);return r<this.pages&&(r<this.pages-1&&t.push(n`<span style="color:var(--muted)">...</span>`),t.push(n`<button class="page-btn" @click=${()=>this._onPageChange(this.pages)}>${this.pages}</button>`)),n`<div class="pagination">${t}</div>`}render(){return this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:n`
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value text">${this.stats.total||this.total}</div>
          <div class="stat-label">总商品数</div>
        </div>
        <div class="stat-card">
          <div class="stat-value accent">${this.stats.amazon||0}</div>
          <div class="stat-label">Amazon</div>
        </div>
        <div class="stat-card">
          <div class="stat-value tiktok">${this.stats.tiktok||0}</div>
          <div class="stat-label">TikTok</div>
        </div>
        <div class="stat-card">
          <div class="stat-value ok">${this.stats.today||0}</div>
          <div class="stat-label">今日新增</div>
        </div>
      </div>

      <!-- 搜索过滤 -->
      <div class="toolbar">
        <div class="toolbar-grid">
          <div>
            <label class="field-label">搜索关键词</label>
            <input type="text" class="input" placeholder="商品名称..." 
              .value=${this.search}
              @input=${t=>this._onInputChange(t,"search")}
              @keyup=${t=>t.key==="Enter"&&this._onSearch()}>
          </div>
          <div>
            <label class="field-label">平台</label>
            <select class="select" .value=${this.platform} @change=${t=>{this._onInputChange(t,"platform"),this._onSearch()}}>
              <option value="">全部平台</option>
              <option value="amazon">Amazon</option>
              <option value="tiktok">TikTok</option>
            </select>
          </div>
          <div>
            <label class="field-label">分类</label>
            <input type="text" class="input" placeholder="分类..." 
              .value=${this.category}
              @input=${t=>this._onInputChange(t,"category")}
              @keyup=${t=>t.key==="Enter"&&this._onSearch()}>
          </div>
          <button class="search-btn" @click=${this._onSearch}>🔍 搜索</button>
        </div>
      </div>

      <!-- 商品列表 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>编码</th>
              <th>平台</th>
              <th>产品简称</th>
              <th>分类</th>
              <th>价格</th>
              <th>评分</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map(t=>n`
              <tr>
                <td style="font-size:11px;color:var(--muted)">${t.ecom_code}</td>
                <td>
                  <span class="platform-badge ${t.platform==="amazon"?"platform-amazon":"platform-tiktok"}">
                    ${t.platform}
                  </span>
                </td>
                <td>
                  <span style="display:flex;align-items:center;gap:8px">
                    ${t.product_url?n`<a class="product-link" href=${t.product_url} target="_blank" title=${t.name}>${t.short_name||t.name||"无名称"}</a>`:n`<span title=${t.name}>${t.short_name||t.name||"无名称"}</span>`}
                    <button 
                      class="action-btn track ${this.trackedIds.has(t.ecom_code)?"active":""}"
                      @click=${()=>this._toggleTrack(t.ecom_code)}
                      title=${this.trackedIds.has(t.ecom_code)?"取消追踪":"添加追踪"}
                    >${this.trackedIds.has(t.ecom_code)?"★":"☆"}</button>
                  </span>
                </td>
                <td>${t.category||"-"}</td>
                <td>${t.price?`$${t.price.toFixed(2)}`:"-"}</td>
                <td>${t.rating?n`${t.rating.toFixed(1)} ⭐`:"-"}</td>
                <td>${t.last_updated_at||"-"}</td>
                <td>
                  <button class="action-btn" @click=${()=>this._showTrendModal(t.ecom_code)} title="查看趋势">趋势</button>
                  <button class="action-btn" @click=${()=>window.open(t.product_url||"#","_blank")} title="查看详情">查看</button>
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
          <div class="modal-content" @click=${t=>t.stopPropagation()}>
            <button class="modal-close" @click=${this._closeTrendModal}>✕</button>
            <ea-product-trend ecomCode=${this.trendCode}></ea-product-trend>
          </div>
        </div>
      `:""}
    `}};ga(f,"styles",m`
    :host { display: block; }
    
    /* 模态框 */
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
    
    .modal-content {
      background: var(--bg);
      border-radius: var(--radius-lg);
      width: 90%;
      max-width: 900px;
      max-height: 90vh;
      overflow-y: auto;
      position: relative;
    }
    
    .modal-close {
      position: absolute;
      top: 12px;
      right: 12px;
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      width: 28px;
      height: 28px;
      cursor: pointer;
      font-size: 16px;
      color: var(--muted);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10;
    }
    
    .modal-close:hover {
      color: var(--text);
    }
    
    /* 统计卡片 */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      text-align: center;
    }
    
    .stat-value {
      font-size: 32px;
      font-weight: 700;
    }
    
    .stat-value.accent { color: var(--accent); }
    .stat-value.tiktok { color: #00f2ea; }
    .stat-value.ok { color: var(--ok); }
    .stat-value.text { color: var(--text-strong); }
    
    .stat-label {
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }
    
    /* 工具栏 */
    .toolbar {
      background: var(--card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 24px;
    }
    
    .toolbar-grid {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr auto;
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
    
    .input, .select {
      width: 100%;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      font-size: 13px;
      background: var(--bg-elevated);
      color: var(--text);
      transition: var(--duration-fast) ease;
    }
    
    .input:focus, .select:focus {
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
      transition: var(--duration-fast) ease;
    }
    
    .search-btn:hover {
      background: var(--accent-hover);
    }
    
    /* 表格 */
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
    
    .platform-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
    }
    
    .platform-amazon {
      background: var(--accent-subtle);
      color: var(--accent);
    }
    
    .platform-tiktok {
      background: rgba(0, 242, 234, 0.1);
      color: #00f2ea;
    }
    
    .product-link {
      color: var(--accent);
      text-decoration: none;
    }
    
    .product-link:hover { text-decoration: underline; }
    
    .truncate {
      max-width: 150px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    /* 操作按钮 */
    .action-btn {
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--muted);
      margin-right: 4px;
    }
    
    .action-btn:hover {
      background: var(--bg-hover);
      color: var(--text);
    }
    
    .action-btn.track {
      background: transparent;
      border: none;
      font-size: 14px;
    }
    
    .action-btn.track.active {
      color: #fbbf24;
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
    
    @media (max-width: 768px) {
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .toolbar-grid { grid-template-columns: 1fr; }
    }
  `);_([l()],f.prototype,"products",2);_([l()],f.prototype,"loading",2);_([l()],f.prototype,"page",2);_([l()],f.prototype,"total",2);_([l()],f.prototype,"pages",2);_([l()],f.prototype,"stats",2);_([l()],f.prototype,"search",2);_([l()],f.prototype,"platform",2);_([l()],f.prototype,"category",2);_([l()],f.prototype,"trackedIds",2);_([l()],f.prototype,"showTrend",2);_([l()],f.prototype,"trendCode",2);f=_([x("ea-product-master")],f);var ee=Object.defineProperty,va=Object.getOwnPropertyDescriptor,ba=(o,t,e)=>t in o?ee(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,ut=(o,t,e,a)=>{for(var r=a>1?void 0:a?va(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ee(t,e,r),r},fa=(o,t,e)=>ba(o,t+"",e);let q=class extends g{constructor(){super(...arguments);d(this,"products",[]);d(this,"loading",!0);d(this,"trackedIds",new Set)}connectedCallback(){super.connectedCallback(),this.loadTracked()}loadTracked(){const t=localStorage.getItem("tracked-products");t&&(this.trackedIds=new Set(JSON.parse(t))),this.loadData()}saveTracked(){localStorage.setItem("tracked-products",JSON.stringify([...this.trackedIds]))}async loadData(){if(this.loading=!0,this.trackedIds.size===0){this.products=[],this.loading=!1,this.requestUpdate();return}try{const t=await Je([...this.trackedIds]);this.products=t.products||[]}catch(t){console.error("Load tracking error:",t),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}_untrack(t){this.trackedIds.delete(t),this.saveTracked(),this.products=this.products.filter(e=>e.ecom_code!==t),this.requestUpdate()}render(){return this.loading?n`<div class="loading"><div class="spinner"></div><p>加载中...</p></div>`:this.products.length===0?n`
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
              <th>编码</th>
              <th>平台</th>
              <th>产品简称</th>
              <th>分类</th>
              <th>价格</th>
              <th>评分</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            ${this.products.map(t=>n`
              <tr>
                <td style="font-size:11px;color:var(--muted)">${t.ecom_code}</td>
                <td>
                  <span class="platform-badge ${t.platform==="amazon"?"platform-amazon":"platform-tiktok"}">
                    ${t.platform}
                  </span>
                </td>
                <td>
                  ${t.product_url?n`<a class="product-link" href=${t.product_url} target="_blank" title=${t.name}>${t.short_name||t.name||"无名称"}</a>`:n`<span title=${t.name}>${t.short_name||t.name||"无名称"}</span>`}
                </td>
                <td>${t.category||"-"}</td>
                <td>${t.price?`$${t.price.toFixed(2)}`:"-"}</td>
                <td>${t.rating?n`${t.rating.toFixed(1)} ⭐`:"-"}</td>
                <td>${t.last_updated_at||"-"}</td>
                <td>
                  <button class="action-btn" @click=${()=>console.log("趋势:",t.ecom_code)}>趋势</button>
                  <button class="action-btn" @click=${()=>window.open(t.product_url||"#","_blank")}>查看</button>
                  <button class="action-btn" style="color:var(--danger)" @click=${()=>this._untrack(t.ecom_code)} title="取消追踪">删除</button>
                </td>
              </tr>
            `)}
          </tbody>
        </table>
      </div>
    `}};fa(q,"styles",m`
    :host { display: block; }
    
    .empty-state {
      text-align: center;
      padding: 48px;
      color: var(--muted);
    }
    
    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
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
    
    .platform-badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
    }
    
    .platform-amazon {
      background: var(--accent-subtle);
      color: var(--accent);
    }
    
    .platform-tiktok {
      background: rgba(0, 242, 234, 0.1);
      color: #00f2ea;
    }
    
    .product-link {
      color: var(--accent);
      text-decoration: none;
    }
    
    .product-link:hover { text-decoration: underline; }
    
    .action-btn {
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      font-size: 11px;
      cursor: pointer;
      transition: var(--duration-fast) ease;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--muted);
      margin-right: 4px;
    }
    
    .action-btn:hover {
      background: var(--bg-hover);
      color: var(--text);
    }
    
    .action-btn.untrack {
      background: transparent;
      border: none;
      font-size: 14px;
      color: #fbbf24;
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
  `);ut([l()],q.prototype,"products",2);ut([l()],q.prototype,"loading",2);ut([l()],q.prototype,"trackedIds",2);q=ut([x("ea-tracking")],q);var ae=Object.defineProperty,ma=Object.getOwnPropertyDescriptor,xa=(o,t,e)=>t in o?ae(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,J=(o,t,e,a)=>{for(var r=a>1?void 0:a?ma(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ae(t,e,r),r},$a=(o,t,e)=>xa(o,t+"",e);const ya={google:"Google API Key",volcano:"火山引擎 API Key",xai:"xAI API Key",image_providers:"图片生成模型",default:"默认模型",available:"可用模型",flash_image:"Flash Image",model:"模型名称",aspect_ratios:"支持比例",resolutions:"支持分辨率",video_providers:"视频生成模型",grok:"Grok",max_duration:"最大时长(秒)",gemini:"Gemini 配置",temperature:"温度参数",max_output_tokens:"最大输出Token",triggers:"触发器列表",image:"生成图片",video:"生成视频",amazon:"亚马逊抓取",tiktok:"TikTok抓取",test:"测试模式",name:"名称",script:"脚本路径",keywords:"触发关键词",description:"描述",settings:"设置",cache_expire_minutes:"缓存过期时间(分钟)",case_sensitive:"区分大小写"},_a={api_keys:{title:"API 密钥",desc:"各平台 API 访问密钥",icon:"🔑"},models:{title:"模型配置",desc:"图片、视频生成模型参数",icon:"🤖"},triggers:{title:"触发器",desc:"命令关键词触发配置",icon:"⚡"}};let O=class extends g{constructor(){super(...arguments);d(this,"configs",[]);d(this,"backups",[]);d(this,"showBackups",!1);d(this,"loading",!0);d(this,"saving",null)}connectedCallback(){super.connectedCallback(),this.loadConfigs()}async loadConfigs(){this.loading=!0;try{const t=await Ge(),e=await jt(),a=[];for(const r of t.configs)if(!r.name.includes("template"))try{const i=await We(r.name);a.push({name:r.name,filename:r.filename,data:i.data,modified:i.modified})}catch(i){console.error("Load config error:",r.name,i)}this.configs=a,this.backups=e.backups}catch(t){console.error("Failed to load configs:",t)}finally{this.loading=!1,this.requestUpdate()}}_getLabel(t){return ya[t]||t}_getConfigInfo(t){return _a[t]||{title:t,desc:"",icon:"📄"}}_onFieldChange(t,e,a){const r=this.configs.find(i=>i.name===t);if(r){const i=e.split(".");let s=r.data;for(let c=0;c<i.length-1;c++)s=s[i[c]];s[i[i.length-1]]=a,this.requestUpdate()}}async _saveConfig(t){const e=this.configs.find(a=>a.name===t);if(e){this.saving=t;try{const a=JSON.stringify(e.data,null,2),r=await Ze(t,a);alert(`✅ 配置已保存
备份文件: `+r.backup),this.loadConfigs()}catch(a){alert("保存失败: "+(a instanceof Error?a.message:String(a)))}finally{this.saving=null}}}async _restoreBackup(t){if(confirm(`确定要还原备份 ${t} 吗？`))try{const e=await Ke(t);alert(`✅ 已还原备份
原配置已备份为: ${e.pre_restore_backup}`),this.showBackups=!1,this.loadConfigs()}catch(e){alert("还原失败: "+(e instanceof Error?e.message:String(e)))}}async _deleteBackup(t){if(confirm(`确定要删除备份 ${t} 吗？`))try{await Xe(t);const e=await jt();this.backups=e.backups}catch(e){alert("删除失败: "+(e instanceof Error?e.message:String(e)))}}_renderSimpleFields(t){return n`
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
    `}_renderConfigCard(t){const e=this._getConfigInfo(t.name),a=this.saving===t.name,r=t.name==="api_keys";return n`
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
    `}};$a(O,"styles",m`
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
  `);J([l()],O.prototype,"configs",2);J([l()],O.prototype,"backups",2);J([l()],O.prototype,"showBackups",2);J([l()],O.prototype,"loading",2);J([l()],O.prototype,"saving",2);O=J([x("ea-settings")],O);var re=Object.defineProperty,ka=Object.getOwnPropertyDescriptor,wa=(o,t,e)=>t in o?re(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,G=(o,t,e,a)=>{for(var r=a>1?void 0:a?ka(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&re(t,e,r),r},Pa=(o,t,e)=>wa(o,t+"",e);let T=class extends g{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"amazonData",{});d(this,"tiktokData",{});d(this,"loading",!1);d(this,"pinnedCategories",new Set)}connectedCallback(){super.connectedCallback(),this._loadPinned(),this.loadData()}_loadPinned(){const t=localStorage.getItem("pinned-categories");t&&(this.pinnedCategories=new Set(JSON.parse(t)))}_savePinned(){localStorage.setItem("pinned-categories",JSON.stringify([...this.pinnedCategories]))}_togglePin(t){this.pinnedCategories.has(t)?this.pinnedCategories.delete(t):this.pinnedCategories.add(t),this._savePinned(),this.requestUpdate()}async loadData(){this.loading=!0;try{this.platform==="amazon"&&Object.keys(this.amazonData).length===0?this.amazonData=await Ye():this.platform==="tiktok"&&Object.keys(this.tiktokData).length===0&&(this.tiktokData=await ta())}catch(t){console.error("Load top error:",t)}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.loadData()}_truncate(t,e=20){return t?t.length>e?t.substring(0,e)+"...":t:"-"}_renderRankChange(t,e){return e?n`<span class="new-badge">新</span>`:t==null?null:t>0?n`<span class="rank-change up">↑${t}</span>`:t<0?n`<span class="rank-change down">↓${Math.abs(t)}</span>`:null}_sortCategories(t){const e=t.filter(r=>this.pinnedCategories.has(r)),a=t.filter(r=>!this.pinnedCategories.has(r));return[...e,...a]}render(){const t=this.platform==="amazon"?this.amazonData:this.tiktokData,e=this._sortCategories(Object.keys(t));return n`
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
    `}};Pa(T,"styles",m`
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
  `);G([l()],T.prototype,"platform",2);G([l()],T.prototype,"amazonData",2);G([l()],T.prototype,"tiktokData",2);G([l()],T.prototype,"loading",2);G([l()],T.prototype,"pinnedCategories",2);T=G([x("ea-today-top")],T);var oe=Object.defineProperty,za=Object.getOwnPropertyDescriptor,Aa=(o,t,e)=>t in o?oe(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,M=(o,t,e,a)=>{for(var r=a>1?void 0:a?za(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&oe(t,e,r),r},Ca=(o,t,e)=>Aa(o,t+"",e);let w=class extends g{constructor(){super(...arguments);d(this,"platform","amazon");d(this,"products",[]);d(this,"loading",!1);d(this,"page",1);d(this,"pages",0);d(this,"search","");d(this,"category","")}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){var t;this.loading=!0,console.log("=== RawData: Loading, platform:",this.platform);try{const e={page:this.page,limit:20,search:this.search,category:this.category},a=this.platform==="amazon"?await ea(e):await aa(e);console.log("=== RawData: Result:",a),this.products=a.data||[],this.pages=((t=a.pagination)==null?void 0:t.pages)||0}catch(e){console.error("=== RawData: Error:",e),this.products=[]}finally{this.loading=!1,this.requestUpdate()}}_switchPlatform(t){this.platform=t,this.page=1,this.loadData()}_onSearch(){this.page=1,this.loadData()}_onPageChange(t){this.page=t,this.loadData()}_renderPagination(){const t=[];let a=Math.max(1,this.page-Math.floor(2.5)),r=Math.min(this.pages,a+5-1);r-a<4&&(a=Math.max(1,r-5+1));for(let i=a;i<=r;i++)t.push(n`
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
    `}};Ca(w,"styles",m`
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
  `);M([l()],w.prototype,"platform",2);M([l()],w.prototype,"products",2);M([l()],w.prototype,"loading",2);M([l()],w.prototype,"page",2);M([l()],w.prototype,"pages",2);M([l()],w.prototype,"search",2);M([l()],w.prototype,"category",2);w=M([x("ea-raw-data")],w);var ie=Object.defineProperty,Sa=Object.getOwnPropertyDescriptor,Ea=(o,t,e)=>t in o?ie(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,gt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Sa(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ie(t,e,r),r},Oa=(o,t,e)=>Ea(o,t+"",e);let V=class extends g{constructor(){super(...arguments);d(this,"stats",{amazon_hot_tiktok_not:0,tiktok_hot_amazon_not:0,both_hot:0});d(this,"items",[]);d(this,"loading",!1)}connectedCallback(){super.connectedCallback(),this.loadData()}async loadData(){this.loading=!0;try{const t=await ra();this.stats=t.stats||this.stats,this.items=t.items||[]}catch(t){console.error("Load cross-platform error:",t)}finally{this.loading=!1}}render(){return n`
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
    `}};Oa(V,"styles",m`
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
  `);gt([l()],V.prototype,"stats",2);gt([l()],V.prototype,"items",2);gt([l()],V.prototype,"loading",2);V=gt([x("ea-cross-platform")],V);var se=Object.defineProperty,Ta=Object.getOwnPropertyDescriptor,Da=(o,t,e)=>t in o?se(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,wt=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ta(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&se(t,e,r),r},Ma=(o,t,e)=>Da(o,t+"",e);let et=class extends g{constructor(){super(...arguments);d(this,"format","csv");d(this,"dateRange","all")}_export(t){console.log("Export:",{platform:t,format:this.format,dateRange:this.dateRange}),alert(`导出功能开发中...
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
    `}};Ma(et,"styles",m`
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
  `);wt([l()],et.prototype,"format",2);wt([l()],et.prototype,"dateRange",2);et=wt([x("ea-export")],et);var ne=Object.defineProperty,Ia=Object.getOwnPropertyDescriptor,Na=(o,t,e)=>t in o?ne(o,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):o[t]=e,de=(o,t,e,a)=>{for(var r=a>1?void 0:a?Ia(t,e):t,i=o.length-1,s;i>=0;i--)(s=o[i])&&(r=(a?s(t,e,r):s(r))||r);return a&&r&&ne(t,e,r),r},Ua=(o,t,e)=>Na(o,t+"",e);const Pt=new Set;let zt="dashboard";window.ecomagentNavigate=o=>{zt=o,Pt.forEach(t=>t(o))};window.ecomagentGetCurrentPage=()=>zt;window.ecomagentOnPageChange=o=>{Pt.add(o)};let pt=class extends g{constructor(){super();d(this,"_page",zt);Pt.add(t=>{this._page=t,this.requestUpdate()})}connectedCallback(){super.connectedCallback();const t=localStorage.getItem("theme")||"dark";document.body.setAttribute("data-theme-mode",t)}_renderPage(){switch(this._page){case"dashboard":return n`<ea-dashboard></ea-dashboard>`;case"settings":return n`<ea-settings></ea-settings>`;case"product-master":return n`<ea-product-master></ea-product-master>`;case"tracking":return n`<ea-tracking></ea-tracking>`;case"cross-platform":return n`<ea-cross-platform></ea-cross-platform>`;case"today-top":return n`<ea-today-top></ea-today-top>`;case"raw-data":return n`<ea-raw-data></ea-raw-data>`;case"export":return n`<ea-export></ea-export>`;default:return n`<div style="padding:24px;color:var(--muted)">未知页面</div>`}}render(){return n`
      <ea-layout currentPage=${this._page}>
        ${this._renderPage()}
      </ea-layout>
    `}};Ua(pt,"styles",m`:host { display: block; min-height: 100vh; }`);de([l()],pt.prototype,"_page",2);pt=de([x("ecomagent-app")],pt);console.log("EcomAgent UI loaded");

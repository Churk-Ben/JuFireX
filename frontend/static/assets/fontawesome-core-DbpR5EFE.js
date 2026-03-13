import{P as La,w as za,f as Y,Q as Ra}from"./vendor-BntURTnA.js";/*!
 * Font Awesome Free 7.2.0 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2026 Fonticons, Inc.
 */function Ie(e,t){(t==null||t>e.length)&&(t=e.length);for(var a=0,n=Array(t);a<t;a++)n[a]=e[a];return n}function Wa(e){if(Array.isArray(e))return e}function Ua(e){if(Array.isArray(e))return Ie(e)}function Ya(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function Ba(e,t){for(var a=0;a<t.length;a++){var n=t[a];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,Nt(n.key),n)}}function Ha(e,t,a){return t&&Ba(e.prototype,t),Object.defineProperty(e,"prototype",{writable:!1}),e}function ie(e,t){var a=typeof Symbol<"u"&&e[Symbol.iterator]||e["@@iterator"];if(!a){if(Array.isArray(e)||(a=Ue(e))||t){a&&(e=a);var n=0,r=function(){};return{s:r,n:function(){return n>=e.length?{done:!0}:{done:!1,value:e[n++]}},e:function(l){throw l},f:r}}throw new TypeError(`Invalid attempt to iterate non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var i,o=!0,s=!1;return{s:function(){a=a.call(e)},n:function(){var l=a.next();return o=l.done,l},e:function(l){s=!0,i=l},f:function(){try{o||a.return==null||a.return()}finally{if(s)throw i}}}}function g(e,t,a){return(t=Nt(t))in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function Ga(e){if(typeof Symbol<"u"&&e[Symbol.iterator]!=null||e["@@iterator"]!=null)return Array.from(e)}function Xa(e,t){var a=e==null?null:typeof Symbol<"u"&&e[Symbol.iterator]||e["@@iterator"];if(a!=null){var n,r,i,o,s=[],l=!0,u=!1;try{if(i=(a=a.call(e)).next,t===0){if(Object(a)!==a)return;l=!1}else for(;!(l=(n=i.call(a)).done)&&(s.push(n.value),s.length!==t);l=!0);}catch(c){u=!0,r=c}finally{try{if(!l&&a.return!=null&&(o=a.return(),Object(o)!==o))return}finally{if(u)throw r}}return s}}function Ka(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Va(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function et(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter(function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable})),a.push.apply(a,n)}return a}function f(e){for(var t=1;t<arguments.length;t++){var a=arguments[t]!=null?arguments[t]:{};t%2?et(Object(a),!0).forEach(function(n){g(e,n,a[n])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):et(Object(a)).forEach(function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))})}return e}function de(e,t){return Wa(e)||Xa(e,t)||Ue(e,t)||Ka()}function j(e){return Ua(e)||Ga(e)||Ue(e)||Va()}function Ja(e,t){if(typeof e!="object"||!e)return e;var a=e[Symbol.toPrimitive];if(a!==void 0){var n=a.call(e,t);if(typeof n!="object")return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return(t==="string"?String:Number)(e)}function Nt(e){var t=Ja(e,"string");return typeof t=="symbol"?t:t+""}function le(e){"@babel/helpers - typeof";return le=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(t){return typeof t}:function(t){return t&&typeof Symbol=="function"&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},le(e)}function Ue(e,t){if(e){if(typeof e=="string")return Ie(e,t);var a={}.toString.call(e).slice(8,-1);return a==="Object"&&e.constructor&&(a=e.constructor.name),a==="Map"||a==="Set"?Array.from(e):a==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a)?Ie(e,t):void 0}}var tt=function(){},Ye={},_t={},Tt=null,$t={mark:tt,measure:tt};try{typeof window<"u"&&(Ye=window),typeof document<"u"&&(_t=document),typeof MutationObserver<"u"&&(Tt=MutationObserver),typeof performance<"u"&&($t=performance)}catch{}var qa=Ye.navigator||{},at=qa.userAgent,nt=at===void 0?"":at,M=Ye,x=_t,rt=Tt,ne=$t;M.document;var $=!!x.documentElement&&!!x.head&&typeof x.addEventListener=="function"&&typeof x.createElement=="function",Mt=~nt.indexOf("MSIE")||~nt.indexOf("Trident/"),ye,Qa=/fa(k|kd|s|r|l|t|d|dr|dl|dt|b|slr|slpr|wsb|tl|ns|nds|es|gt|jr|jfr|jdr|usb|ufsb|udsb|cr|ss|sr|sl|st|sds|sdr|sdl|sdt)?[\-\ ]/,Za=/Font ?Awesome ?([567 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Sharp Duotone|Sharp|Kit|Notdog Duo|Notdog|Chisel|Etch|Graphite|Thumbprint|Jelly Fill|Jelly Duo|Jelly|Utility|Utility Fill|Utility Duo|Slab Press|Slab|Whiteboard)?.*/i,Dt={classic:{fa:"solid",fas:"solid","fa-solid":"solid",far:"regular","fa-regular":"regular",fal:"light","fa-light":"light",fat:"thin","fa-thin":"thin",fab:"brands","fa-brands":"brands"},duotone:{fa:"solid",fad:"solid","fa-solid":"solid","fa-duotone":"solid",fadr:"regular","fa-regular":"regular",fadl:"light","fa-light":"light",fadt:"thin","fa-thin":"thin"},sharp:{fa:"solid",fass:"solid","fa-solid":"solid",fasr:"regular","fa-regular":"regular",fasl:"light","fa-light":"light",fast:"thin","fa-thin":"thin"},"sharp-duotone":{fa:"solid",fasds:"solid","fa-solid":"solid",fasdr:"regular","fa-regular":"regular",fasdl:"light","fa-light":"light",fasdt:"thin","fa-thin":"thin"},slab:{"fa-regular":"regular",faslr:"regular"},"slab-press":{"fa-regular":"regular",faslpr:"regular"},thumbprint:{"fa-light":"light",fatl:"light"},whiteboard:{"fa-semibold":"semibold",fawsb:"semibold"},notdog:{"fa-solid":"solid",fans:"solid"},"notdog-duo":{"fa-solid":"solid",fands:"solid"},etch:{"fa-solid":"solid",faes:"solid"},graphite:{"fa-thin":"thin",fagt:"thin"},jelly:{"fa-regular":"regular",fajr:"regular"},"jelly-fill":{"fa-regular":"regular",fajfr:"regular"},"jelly-duo":{"fa-regular":"regular",fajdr:"regular"},chisel:{"fa-regular":"regular",facr:"regular"},utility:{"fa-semibold":"semibold",fausb:"semibold"},"utility-duo":{"fa-semibold":"semibold",faudsb:"semibold"},"utility-fill":{"fa-semibold":"semibold",faufsb:"semibold"}},en={GROUP:"duotone-group",PRIMARY:"primary",SECONDARY:"secondary"},Lt=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone","fa-thumbprint","fa-whiteboard","fa-notdog","fa-notdog-duo","fa-chisel","fa-etch","fa-graphite","fa-jelly","fa-jelly-fill","fa-jelly-duo","fa-slab","fa-slab-press","fa-utility","fa-utility-duo","fa-utility-fill"],k="classic",ee="duotone",zt="sharp",Rt="sharp-duotone",Wt="chisel",Ut="etch",Yt="graphite",Bt="jelly",Ht="jelly-duo",Gt="jelly-fill",Xt="notdog",Kt="notdog-duo",Vt="slab",Jt="slab-press",qt="thumbprint",Qt="utility",Zt="utility-duo",ea="utility-fill",ta="whiteboard",tn="Classic",an="Duotone",nn="Sharp",rn="Sharp Duotone",on="Chisel",sn="Etch",ln="Graphite",fn="Jelly",un="Jelly Duo",cn="Jelly Fill",dn="Notdog",mn="Notdog Duo",vn="Slab",hn="Slab Press",gn="Thumbprint",pn="Utility",yn="Utility Duo",bn="Utility Fill",xn="Whiteboard",aa=[k,ee,zt,Rt,Wt,Ut,Yt,Bt,Ht,Gt,Xt,Kt,Vt,Jt,qt,Qt,Zt,ea,ta];ye={},g(g(g(g(g(g(g(g(g(g(ye,k,tn),ee,an),zt,nn),Rt,rn),Wt,on),Ut,sn),Yt,ln),Bt,fn),Ht,un),Gt,cn),g(g(g(g(g(g(g(g(g(ye,Xt,dn),Kt,mn),Vt,vn),Jt,hn),qt,gn),Qt,pn),Zt,yn),ea,bn),ta,xn);var wn={classic:{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},duotone:{900:"fad",400:"fadr",300:"fadl",100:"fadt"},sharp:{900:"fass",400:"fasr",300:"fasl",100:"fast"},"sharp-duotone":{900:"fasds",400:"fasdr",300:"fasdl",100:"fasdt"},slab:{400:"faslr"},"slab-press":{400:"faslpr"},whiteboard:{600:"fawsb"},thumbprint:{300:"fatl"},notdog:{900:"fans"},"notdog-duo":{900:"fands"},etch:{900:"faes"},graphite:{100:"fagt"},chisel:{400:"facr"},jelly:{400:"fajr"},"jelly-fill":{400:"fajfr"},"jelly-duo":{400:"fajdr"},utility:{600:"fausb"},"utility-duo":{600:"faudsb"},"utility-fill":{600:"faufsb"}},Sn={"Font Awesome 7 Free":{900:"fas",400:"far"},"Font Awesome 7 Pro":{900:"fas",400:"far",normal:"far",300:"fal",100:"fat"},"Font Awesome 7 Brands":{400:"fab",normal:"fab"},"Font Awesome 7 Duotone":{900:"fad",400:"fadr",normal:"fadr",300:"fadl",100:"fadt"},"Font Awesome 7 Sharp":{900:"fass",400:"fasr",normal:"fasr",300:"fasl",100:"fast"},"Font Awesome 7 Sharp Duotone":{900:"fasds",400:"fasdr",normal:"fasdr",300:"fasdl",100:"fasdt"},"Font Awesome 7 Jelly":{400:"fajr",normal:"fajr"},"Font Awesome 7 Jelly Fill":{400:"fajfr",normal:"fajfr"},"Font Awesome 7 Jelly Duo":{400:"fajdr",normal:"fajdr"},"Font Awesome 7 Slab":{400:"faslr",normal:"faslr"},"Font Awesome 7 Slab Press":{400:"faslpr",normal:"faslpr"},"Font Awesome 7 Thumbprint":{300:"fatl",normal:"fatl"},"Font Awesome 7 Notdog":{900:"fans",normal:"fans"},"Font Awesome 7 Notdog Duo":{900:"fands",normal:"fands"},"Font Awesome 7 Etch":{900:"faes",normal:"faes"},"Font Awesome 7 Graphite":{100:"fagt",normal:"fagt"},"Font Awesome 7 Chisel":{400:"facr",normal:"facr"},"Font Awesome 7 Whiteboard":{600:"fawsb",normal:"fawsb"},"Font Awesome 7 Utility":{600:"fausb",normal:"fausb"},"Font Awesome 7 Utility Duo":{600:"faudsb",normal:"faudsb"},"Font Awesome 7 Utility Fill":{600:"faufsb",normal:"faufsb"}},An=new Map([["classic",{defaultShortPrefixId:"fas",defaultStyleId:"solid",styleIds:["solid","regular","light","thin","brands"],futureStyleIds:[],defaultFontWeight:900}],["duotone",{defaultShortPrefixId:"fad",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["sharp",{defaultShortPrefixId:"fass",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["sharp-duotone",{defaultShortPrefixId:"fasds",defaultStyleId:"solid",styleIds:["solid","regular","light","thin"],futureStyleIds:[],defaultFontWeight:900}],["chisel",{defaultShortPrefixId:"facr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["etch",{defaultShortPrefixId:"faes",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["graphite",{defaultShortPrefixId:"fagt",defaultStyleId:"thin",styleIds:["thin"],futureStyleIds:[],defaultFontWeight:100}],["jelly",{defaultShortPrefixId:"fajr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["jelly-duo",{defaultShortPrefixId:"fajdr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["jelly-fill",{defaultShortPrefixId:"fajfr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["notdog",{defaultShortPrefixId:"fans",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["notdog-duo",{defaultShortPrefixId:"fands",defaultStyleId:"solid",styleIds:["solid"],futureStyleIds:[],defaultFontWeight:900}],["slab",{defaultShortPrefixId:"faslr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["slab-press",{defaultShortPrefixId:"faslpr",defaultStyleId:"regular",styleIds:["regular"],futureStyleIds:[],defaultFontWeight:400}],["thumbprint",{defaultShortPrefixId:"fatl",defaultStyleId:"light",styleIds:["light"],futureStyleIds:[],defaultFontWeight:300}],["utility",{defaultShortPrefixId:"fausb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["utility-duo",{defaultShortPrefixId:"faudsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["utility-fill",{defaultShortPrefixId:"faufsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}],["whiteboard",{defaultShortPrefixId:"fawsb",defaultStyleId:"semibold",styleIds:["semibold"],futureStyleIds:[],defaultFontWeight:600}]]),kn={chisel:{regular:"facr"},classic:{brands:"fab",light:"fal",regular:"far",solid:"fas",thin:"fat"},duotone:{light:"fadl",regular:"fadr",solid:"fad",thin:"fadt"},etch:{solid:"faes"},graphite:{thin:"fagt"},jelly:{regular:"fajr"},"jelly-duo":{regular:"fajdr"},"jelly-fill":{regular:"fajfr"},notdog:{solid:"fans"},"notdog-duo":{solid:"fands"},sharp:{light:"fasl",regular:"fasr",solid:"fass",thin:"fast"},"sharp-duotone":{light:"fasdl",regular:"fasdr",solid:"fasds",thin:"fasdt"},slab:{regular:"faslr"},"slab-press":{regular:"faslpr"},thumbprint:{light:"fatl"},utility:{semibold:"fausb"},"utility-duo":{semibold:"faudsb"},"utility-fill":{semibold:"faufsb"},whiteboard:{semibold:"fawsb"}},na=["fak","fa-kit","fakd","fa-kit-duotone"],it={kit:{fak:"kit","fa-kit":"kit"},"kit-duotone":{fakd:"kit-duotone","fa-kit-duotone":"kit-duotone"}},Pn=["kit"],In="kit",On="kit-duotone",En="Kit",Fn="Kit Duotone";g(g({},In,En),On,Fn);var jn={kit:{"fa-kit":"fak"}},Cn={"Font Awesome Kit":{400:"fak",normal:"fak"},"Font Awesome Kit Duotone":{400:"fakd",normal:"fakd"}},Nn={kit:{fak:"fa-kit"}},ot={kit:{kit:"fak"},"kit-duotone":{"kit-duotone":"fakd"}},be,re={GROUP:"duotone-group",SWAP_OPACITY:"swap-opacity",PRIMARY:"primary",SECONDARY:"secondary"},_n=["fa-classic","fa-duotone","fa-sharp","fa-sharp-duotone","fa-thumbprint","fa-whiteboard","fa-notdog","fa-notdog-duo","fa-chisel","fa-etch","fa-graphite","fa-jelly","fa-jelly-fill","fa-jelly-duo","fa-slab","fa-slab-press","fa-utility","fa-utility-duo","fa-utility-fill"],Tn="classic",$n="duotone",Mn="sharp",Dn="sharp-duotone",Ln="chisel",zn="etch",Rn="graphite",Wn="jelly",Un="jelly-duo",Yn="jelly-fill",Bn="notdog",Hn="notdog-duo",Gn="slab",Xn="slab-press",Kn="thumbprint",Vn="utility",Jn="utility-duo",qn="utility-fill",Qn="whiteboard",Zn="Classic",er="Duotone",tr="Sharp",ar="Sharp Duotone",nr="Chisel",rr="Etch",ir="Graphite",or="Jelly",sr="Jelly Duo",lr="Jelly Fill",fr="Notdog",ur="Notdog Duo",cr="Slab",dr="Slab Press",mr="Thumbprint",vr="Utility",hr="Utility Duo",gr="Utility Fill",pr="Whiteboard";be={},g(g(g(g(g(g(g(g(g(g(be,Tn,Zn),$n,er),Mn,tr),Dn,ar),Ln,nr),zn,rr),Rn,ir),Wn,or),Un,sr),Yn,lr),g(g(g(g(g(g(g(g(g(be,Bn,fr),Hn,ur),Gn,cr),Xn,dr),Kn,mr),Vn,vr),Jn,hr),qn,gr),Qn,pr);var yr="kit",br="kit-duotone",xr="Kit",wr="Kit Duotone";g(g({},yr,xr),br,wr);var Sr={classic:{"fa-brands":"fab","fa-duotone":"fad","fa-light":"fal","fa-regular":"far","fa-solid":"fas","fa-thin":"fat"},duotone:{"fa-regular":"fadr","fa-light":"fadl","fa-thin":"fadt"},sharp:{"fa-solid":"fass","fa-regular":"fasr","fa-light":"fasl","fa-thin":"fast"},"sharp-duotone":{"fa-solid":"fasds","fa-regular":"fasdr","fa-light":"fasdl","fa-thin":"fasdt"},slab:{"fa-regular":"faslr"},"slab-press":{"fa-regular":"faslpr"},whiteboard:{"fa-semibold":"fawsb"},thumbprint:{"fa-light":"fatl"},notdog:{"fa-solid":"fans"},"notdog-duo":{"fa-solid":"fands"},etch:{"fa-solid":"faes"},graphite:{"fa-thin":"fagt"},jelly:{"fa-regular":"fajr"},"jelly-fill":{"fa-regular":"fajfr"},"jelly-duo":{"fa-regular":"fajdr"},chisel:{"fa-regular":"facr"},utility:{"fa-semibold":"fausb"},"utility-duo":{"fa-semibold":"faudsb"},"utility-fill":{"fa-semibold":"faufsb"}},Ar={classic:["fas","far","fal","fat","fad"],duotone:["fadr","fadl","fadt"],sharp:["fass","fasr","fasl","fast"],"sharp-duotone":["fasds","fasdr","fasdl","fasdt"],slab:["faslr"],"slab-press":["faslpr"],whiteboard:["fawsb"],thumbprint:["fatl"],notdog:["fans"],"notdog-duo":["fands"],etch:["faes"],graphite:["fagt"],jelly:["fajr"],"jelly-fill":["fajfr"],"jelly-duo":["fajdr"],chisel:["facr"],utility:["fausb"],"utility-duo":["faudsb"],"utility-fill":["faufsb"]},Oe={classic:{fab:"fa-brands",fad:"fa-duotone",fal:"fa-light",far:"fa-regular",fas:"fa-solid",fat:"fa-thin"},duotone:{fadr:"fa-regular",fadl:"fa-light",fadt:"fa-thin"},sharp:{fass:"fa-solid",fasr:"fa-regular",fasl:"fa-light",fast:"fa-thin"},"sharp-duotone":{fasds:"fa-solid",fasdr:"fa-regular",fasdl:"fa-light",fasdt:"fa-thin"},slab:{faslr:"fa-regular"},"slab-press":{faslpr:"fa-regular"},whiteboard:{fawsb:"fa-semibold"},thumbprint:{fatl:"fa-light"},notdog:{fans:"fa-solid"},"notdog-duo":{fands:"fa-solid"},etch:{faes:"fa-solid"},graphite:{fagt:"fa-thin"},jelly:{fajr:"fa-regular"},"jelly-fill":{fajfr:"fa-regular"},"jelly-duo":{fajdr:"fa-regular"},chisel:{facr:"fa-regular"},utility:{fausb:"fa-semibold"},"utility-duo":{faudsb:"fa-semibold"},"utility-fill":{faufsb:"fa-semibold"}},kr=["fa-solid","fa-regular","fa-light","fa-thin","fa-duotone","fa-brands","fa-semibold"],ra=["fa","fas","far","fal","fat","fad","fadr","fadl","fadt","fab","fass","fasr","fasl","fast","fasds","fasdr","fasdl","fasdt","faslr","faslpr","fawsb","fatl","fans","fands","faes","fagt","fajr","fajfr","fajdr","facr","fausb","faudsb","faufsb"].concat(_n,kr),Pr=["solid","regular","light","thin","duotone","brands","semibold"],ia=[1,2,3,4,5,6,7,8,9,10],Ir=ia.concat([11,12,13,14,15,16,17,18,19,20]),Or=["aw","fw","pull-left","pull-right"],Er=[].concat(j(Object.keys(Ar)),Pr,Or,["2xs","xs","sm","lg","xl","2xl","beat","border","fade","beat-fade","bounce","flip-both","flip-horizontal","flip-vertical","flip","inverse","layers","layers-bottom-left","layers-bottom-right","layers-counter","layers-text","layers-top-left","layers-top-right","li","pull-end","pull-start","pulse","rotate-180","rotate-270","rotate-90","rotate-by","shake","spin-pulse","spin-reverse","spin","stack-1x","stack-2x","stack","ul","width-auto","width-fixed",re.GROUP,re.SWAP_OPACITY,re.PRIMARY,re.SECONDARY]).concat(ia.map(function(e){return"".concat(e,"x")})).concat(Ir.map(function(e){return"w-".concat(e)})),Fr={"Font Awesome 5 Free":{900:"fas",400:"far"},"Font Awesome 5 Pro":{900:"fas",400:"far",normal:"far",300:"fal"},"Font Awesome 5 Brands":{400:"fab",normal:"fab"},"Font Awesome 5 Duotone":{900:"fad"}},_="___FONT_AWESOME___",Ee=16,oa="fa",sa="svg-inline--fa",R="data-fa-i2svg",Fe="data-fa-pseudo-element",jr="data-fa-pseudo-element-pending",Be="data-prefix",He="data-icon",st="fontawesome-i2svg",Cr="async",Nr=["HTML","HEAD","STYLE","SCRIPT"],la=["::before","::after",":before",":after"],fa=(function(){try{return!0}catch{return!1}})();function te(e){return new Proxy(e,{get:function(a,n){return n in a?a[n]:a[k]}})}var ua=f({},Dt);ua[k]=f(f(f(f({},{"fa-duotone":"duotone"}),Dt[k]),it.kit),it["kit-duotone"]);var _r=te(ua),je=f({},kn);je[k]=f(f(f(f({},{duotone:"fad"}),je[k]),ot.kit),ot["kit-duotone"]);var lt=te(je),Ce=f({},Oe);Ce[k]=f(f({},Ce[k]),Nn.kit);var Ge=te(Ce),Ne=f({},Sr);Ne[k]=f(f({},Ne[k]),jn.kit);te(Ne);var Tr=Qa,ca="fa-layers-text",$r=Za,Mr=f({},wn);te(Mr);var Dr=["class","data-prefix","data-icon","data-fa-transform","data-fa-mask"],xe=en,Lr=[].concat(j(Pn),j(Er)),q=M.FontAwesomeConfig||{};function zr(e){var t=x.querySelector("script["+e+"]");if(t)return t.getAttribute(e)}function Rr(e){return e===""?!0:e==="false"?!1:e==="true"?!0:e}if(x&&typeof x.querySelector=="function"){var Wr=[["data-family-prefix","familyPrefix"],["data-css-prefix","cssPrefix"],["data-family-default","familyDefault"],["data-style-default","styleDefault"],["data-replacement-class","replacementClass"],["data-auto-replace-svg","autoReplaceSvg"],["data-auto-add-css","autoAddCss"],["data-search-pseudo-elements","searchPseudoElements"],["data-search-pseudo-elements-warnings","searchPseudoElementsWarnings"],["data-search-pseudo-elements-full-scan","searchPseudoElementsFullScan"],["data-observe-mutations","observeMutations"],["data-mutate-approach","mutateApproach"],["data-keep-original-source","keepOriginalSource"],["data-measure-performance","measurePerformance"],["data-show-missing-icons","showMissingIcons"]];Wr.forEach(function(e){var t=de(e,2),a=t[0],n=t[1],r=Rr(zr(a));r!=null&&(q[n]=r)})}var da={styleDefault:"solid",familyDefault:k,cssPrefix:oa,replacementClass:sa,autoReplaceSvg:!0,autoAddCss:!0,searchPseudoElements:!1,searchPseudoElementsWarnings:!0,searchPseudoElementsFullScan:!1,observeMutations:!0,mutateApproach:"async",keepOriginalSource:!0,measurePerformance:!1,showMissingIcons:!0};q.familyPrefix&&(q.cssPrefix=q.familyPrefix);var X=f(f({},da),q);X.autoReplaceSvg||(X.observeMutations=!1);var v={};Object.keys(da).forEach(function(e){Object.defineProperty(v,e,{enumerable:!0,set:function(a){X[e]=a,Q.forEach(function(n){return n(v)})},get:function(){return X[e]}})});Object.defineProperty(v,"familyPrefix",{enumerable:!0,set:function(t){X.cssPrefix=t,Q.forEach(function(a){return a(v)})},get:function(){return X.cssPrefix}});M.FontAwesomeConfig=v;var Q=[];function Ur(e){return Q.push(e),function(){Q.splice(Q.indexOf(e),1)}}var B=Ee,C={size:16,x:0,y:0,rotate:0,flipX:!1,flipY:!1};function Yr(e){if(!(!e||!$)){var t=x.createElement("style");t.setAttribute("type","text/css"),t.innerHTML=e;for(var a=x.head.childNodes,n=null,r=a.length-1;r>-1;r--){var i=a[r],o=(i.tagName||"").toUpperCase();["STYLE","LINK"].indexOf(o)>-1&&(n=i)}return x.head.insertBefore(t,n),e}}var Br="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";function ft(){for(var e=12,t="";e-- >0;)t+=Br[Math.random()*62|0];return t}function K(e){for(var t=[],a=(e||[]).length>>>0;a--;)t[a]=e[a];return t}function Xe(e){return e.classList?K(e.classList):(e.getAttribute("class")||"").split(" ").filter(function(t){return t})}function ma(e){return"".concat(e).replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/'/g,"&#39;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}function Hr(e){return Object.keys(e||{}).reduce(function(t,a){return t+"".concat(a,'="').concat(ma(e[a]),'" ')},"").trim()}function me(e){return Object.keys(e||{}).reduce(function(t,a){return t+"".concat(a,": ").concat(e[a].trim(),";")},"")}function Ke(e){return e.size!==C.size||e.x!==C.x||e.y!==C.y||e.rotate!==C.rotate||e.flipX||e.flipY}function Gr(e){var t=e.transform,a=e.containerWidth,n=e.iconWidth,r={transform:"translate(".concat(a/2," 256)")},i="translate(".concat(t.x*32,", ").concat(t.y*32,") "),o="scale(".concat(t.size/16*(t.flipX?-1:1),", ").concat(t.size/16*(t.flipY?-1:1),") "),s="rotate(".concat(t.rotate," 0 0)"),l={transform:"".concat(i," ").concat(o," ").concat(s)},u={transform:"translate(".concat(n/2*-1," -256)")};return{outer:r,inner:l,path:u}}function Xr(e){var t=e.transform,a=e.width,n=a===void 0?Ee:a,r=e.height,i=r===void 0?Ee:r,o="";return Mt?o+="translate(".concat(t.x/B-n/2,"em, ").concat(t.y/B-i/2,"em) "):o+="translate(calc(-50% + ".concat(t.x/B,"em), calc(-50% + ").concat(t.y/B,"em)) "),o+="scale(".concat(t.size/B*(t.flipX?-1:1),", ").concat(t.size/B*(t.flipY?-1:1),") "),o+="rotate(".concat(t.rotate,"deg) "),o}var Kr=`:root, :host {
  --fa-font-solid: normal 900 1em/1 'Font Awesome 7 Free';
  --fa-font-regular: normal 400 1em/1 'Font Awesome 7 Free';
  --fa-font-light: normal 300 1em/1 'Font Awesome 7 Pro';
  --fa-font-thin: normal 100 1em/1 'Font Awesome 7 Pro';
  --fa-font-duotone: normal 900 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-regular: normal 400 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-light: normal 300 1em/1 'Font Awesome 7 Duotone';
  --fa-font-duotone-thin: normal 100 1em/1 'Font Awesome 7 Duotone';
  --fa-font-brands: normal 400 1em/1 'Font Awesome 7 Brands';
  --fa-font-sharp-solid: normal 900 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-regular: normal 400 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-light: normal 300 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-thin: normal 100 1em/1 'Font Awesome 7 Sharp';
  --fa-font-sharp-duotone-solid: normal 900 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-regular: normal 400 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-light: normal 300 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-sharp-duotone-thin: normal 100 1em/1 'Font Awesome 7 Sharp Duotone';
  --fa-font-slab-regular: normal 400 1em/1 'Font Awesome 7 Slab';
  --fa-font-slab-press-regular: normal 400 1em/1 'Font Awesome 7 Slab Press';
  --fa-font-whiteboard-semibold: normal 600 1em/1 'Font Awesome 7 Whiteboard';
  --fa-font-thumbprint-light: normal 300 1em/1 'Font Awesome 7 Thumbprint';
  --fa-font-notdog-solid: normal 900 1em/1 'Font Awesome 7 Notdog';
  --fa-font-notdog-duo-solid: normal 900 1em/1 'Font Awesome 7 Notdog Duo';
  --fa-font-etch-solid: normal 900 1em/1 'Font Awesome 7 Etch';
  --fa-font-graphite-thin: normal 100 1em/1 'Font Awesome 7 Graphite';
  --fa-font-jelly-regular: normal 400 1em/1 'Font Awesome 7 Jelly';
  --fa-font-jelly-fill-regular: normal 400 1em/1 'Font Awesome 7 Jelly Fill';
  --fa-font-jelly-duo-regular: normal 400 1em/1 'Font Awesome 7 Jelly Duo';
  --fa-font-chisel-regular: normal 400 1em/1 'Font Awesome 7 Chisel';
  --fa-font-utility-semibold: normal 600 1em/1 'Font Awesome 7 Utility';
  --fa-font-utility-duo-semibold: normal 600 1em/1 'Font Awesome 7 Utility Duo';
  --fa-font-utility-fill-semibold: normal 600 1em/1 'Font Awesome 7 Utility Fill';
}

.svg-inline--fa {
  box-sizing: content-box;
  display: var(--fa-display, inline-block);
  height: 1em;
  overflow: visible;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.svg-inline--fa.fa-2xs {
  vertical-align: 0.1em;
}
.svg-inline--fa.fa-xs {
  vertical-align: 0em;
}
.svg-inline--fa.fa-sm {
  vertical-align: -0.0714285714em;
}
.svg-inline--fa.fa-lg {
  vertical-align: -0.2em;
}
.svg-inline--fa.fa-xl {
  vertical-align: -0.25em;
}
.svg-inline--fa.fa-2xl {
  vertical-align: -0.3125em;
}
.svg-inline--fa.fa-pull-left,
.svg-inline--fa .fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-pull-right,
.svg-inline--fa .fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}
.svg-inline--fa.fa-li {
  width: var(--fa-li-width, 2em);
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  inset-block-start: 0.25em; /* syncing vertical alignment with Web Font rendering */
}

.fa-layers-counter, .fa-layers-text {
  display: inline-block;
  position: absolute;
  text-align: center;
}

.fa-layers {
  display: inline-block;
  height: 1em;
  position: relative;
  text-align: center;
  vertical-align: -0.125em;
  width: var(--fa-width, 1.25em);
}
.fa-layers .svg-inline--fa {
  inset: 0;
  margin: auto;
  position: absolute;
  transform-origin: center center;
}

.fa-layers-text {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  transform-origin: center center;
}

.fa-layers-counter {
  background-color: var(--fa-counter-background-color, #ff253a);
  border-radius: var(--fa-counter-border-radius, 1em);
  box-sizing: border-box;
  color: var(--fa-inverse, #fff);
  line-height: var(--fa-counter-line-height, 1);
  max-width: var(--fa-counter-max-width, 5em);
  min-width: var(--fa-counter-min-width, 1.5em);
  overflow: hidden;
  padding: var(--fa-counter-padding, 0.25em 0.5em);
  right: var(--fa-right, 0);
  text-overflow: ellipsis;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-counter-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-bottom-right {
  bottom: var(--fa-bottom, 0);
  right: var(--fa-right, 0);
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom right;
}

.fa-layers-bottom-left {
  bottom: var(--fa-bottom, 0);
  left: var(--fa-left, 0);
  right: auto;
  top: auto;
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: bottom left;
}

.fa-layers-top-right {
  top: var(--fa-top, 0);
  right: var(--fa-right, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top right;
}

.fa-layers-top-left {
  left: var(--fa-left, 0);
  right: auto;
  top: var(--fa-top, 0);
  transform: scale(var(--fa-layers-scale, 0.25));
  transform-origin: top left;
}

.fa-1x {
  font-size: 1em;
}

.fa-2x {
  font-size: 2em;
}

.fa-3x {
  font-size: 3em;
}

.fa-4x {
  font-size: 4em;
}

.fa-5x {
  font-size: 5em;
}

.fa-6x {
  font-size: 6em;
}

.fa-7x {
  font-size: 7em;
}

.fa-8x {
  font-size: 8em;
}

.fa-9x {
  font-size: 9em;
}

.fa-10x {
  font-size: 10em;
}

.fa-2xs {
  font-size: calc(10 / 16 * 1em); /* converts a 10px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 10 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 10 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xs {
  font-size: calc(12 / 16 * 1em); /* converts a 12px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 12 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 12 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-sm {
  font-size: calc(14 / 16 * 1em); /* converts a 14px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 14 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 14 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-lg {
  font-size: calc(20 / 16 * 1em); /* converts a 20px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 20 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 20 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-xl {
  font-size: calc(24 / 16 * 1em); /* converts a 24px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 24 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 24 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-2xl {
  font-size: calc(32 / 16 * 1em); /* converts a 32px size into an em-based value that's relative to the scale's 16px base */
  line-height: calc(1 / 32 * 1em); /* sets the line-height of the icon back to that of it's parent */
  vertical-align: calc((6 / 32 - 0.375) * 1em); /* vertically centers the icon taking into account the surrounding text's descender */
}

.fa-width-auto {
  --fa-width: auto;
}

.fa-fw,
.fa-width-fixed {
  --fa-width: 1.25em;
}

.fa-ul {
  list-style-type: none;
  margin-inline-start: var(--fa-li-margin, 2.5em);
  padding-inline-start: 0;
}
.fa-ul > li {
  position: relative;
}

.fa-li {
  inset-inline-start: calc(-1 * var(--fa-li-width, 2em));
  position: absolute;
  text-align: center;
  width: var(--fa-li-width, 2em);
  line-height: inherit;
}

/* Heads Up: Bordered Icons will not be supported in the future!
  - This feature will be deprecated in the next major release of Font Awesome (v8)!
  - You may continue to use it in this version *v7), but it will not be supported in Font Awesome v8.
*/
/* Notes:
* --@{v.$css-prefix}-border-width = 1/16 by default (to render as ~1px based on a 16px default font-size)
* --@{v.$css-prefix}-border-padding =
  ** 3/16 for vertical padding (to give ~2px of vertical whitespace around an icon considering it's vertical alignment)
  ** 4/16 for horizontal padding (to give ~4px of horizontal whitespace around an icon)
*/
.fa-border {
  border-color: var(--fa-border-color, #eee);
  border-radius: var(--fa-border-radius, 0.1em);
  border-style: var(--fa-border-style, solid);
  border-width: var(--fa-border-width, 0.0625em);
  box-sizing: var(--fa-border-box-sizing, content-box);
  padding: var(--fa-border-padding, 0.1875em 0.25em);
}

.fa-pull-left,
.fa-pull-start {
  float: inline-start;
  margin-inline-end: var(--fa-pull-margin, 0.3em);
}

.fa-pull-right,
.fa-pull-end {
  float: inline-end;
  margin-inline-start: var(--fa-pull-margin, 0.3em);
}

.fa-beat {
  animation-name: fa-beat;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-bounce {
  animation-name: fa-bounce;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
}

.fa-fade {
  animation-name: fa-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-beat-fade {
  animation-name: fa-beat-fade;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-flip {
  animation-name: fa-flip;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-shake {
  animation-name: fa-shake;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin {
  animation-name: fa-spin;
  animation-delay: var(--fa-animation-delay, 0s);
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 2s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin-reverse {
  --fa-animation-direction: reverse;
}

.fa-pulse,
.fa-spin-pulse {
  animation-name: fa-spin;
  animation-direction: var(--fa-animation-direction, normal);
  animation-duration: var(--fa-animation-duration, 1s);
  animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  animation-timing-function: var(--fa-animation-timing, steps(8));
}

@media (prefers-reduced-motion: reduce) {
  .fa-beat,
  .fa-bounce,
  .fa-fade,
  .fa-beat-fade,
  .fa-flip,
  .fa-pulse,
  .fa-shake,
  .fa-spin,
  .fa-spin-pulse {
    animation: none !important;
    transition: none !important;
  }
}
@keyframes fa-beat {
  0%, 90% {
    transform: scale(1);
  }
  45% {
    transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@keyframes fa-bounce {
  0% {
    transform: scale(1, 1) translateY(0);
  }
  10% {
    transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    transform: scale(1, 1) translateY(0);
  }
  100% {
    transform: scale(1, 1) translateY(0);
  }
}
@keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@keyframes fa-flip {
  50% {
    transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@keyframes fa-shake {
  0% {
    transform: rotate(-15deg);
  }
  4% {
    transform: rotate(15deg);
  }
  8%, 24% {
    transform: rotate(-18deg);
  }
  12%, 28% {
    transform: rotate(18deg);
  }
  16% {
    transform: rotate(-22deg);
  }
  20% {
    transform: rotate(22deg);
  }
  32% {
    transform: rotate(-12deg);
  }
  36% {
    transform: rotate(12deg);
  }
  40%, 100% {
    transform: rotate(0deg);
  }
}
@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.fa-rotate-90 {
  transform: rotate(90deg);
}

.fa-rotate-180 {
  transform: rotate(180deg);
}

.fa-rotate-270 {
  transform: rotate(270deg);
}

.fa-flip-horizontal {
  transform: scale(-1, 1);
}

.fa-flip-vertical {
  transform: scale(1, -1);
}

.fa-flip-both,
.fa-flip-horizontal.fa-flip-vertical {
  transform: scale(-1, -1);
}

.fa-rotate-by {
  transform: rotate(var(--fa-rotate-angle, 0));
}

.svg-inline--fa .fa-primary {
  fill: var(--fa-primary-color, currentColor);
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa .fa-secondary {
  fill: var(--fa-secondary-color, currentColor);
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-primary {
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-secondary {
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa mask .fa-primary,
.svg-inline--fa mask .fa-secondary {
  fill: black;
}

.svg-inline--fa.fa-inverse {
  fill: var(--fa-inverse, #fff);
}

.fa-stack {
  display: inline-block;
  height: 2em;
  line-height: 2em;
  position: relative;
  vertical-align: middle;
  width: 2.5em;
}

.fa-inverse {
  color: var(--fa-inverse, #fff);
}

.svg-inline--fa.fa-stack-1x {
  --fa-width: 1.25em;
  height: 1em;
  width: var(--fa-width);
}
.svg-inline--fa.fa-stack-2x {
  --fa-width: 2.5em;
  height: 2em;
  width: var(--fa-width);
}

.fa-stack-1x,
.fa-stack-2x {
  inset: 0;
  margin: auto;
  position: absolute;
  z-index: var(--fa-stack-z-index, auto);
}`;function va(){var e=oa,t=sa,a=v.cssPrefix,n=v.replacementClass,r=Kr;if(a!==e||n!==t){var i=new RegExp("\\.".concat(e,"\\-"),"g"),o=new RegExp("\\--".concat(e,"\\-"),"g"),s=new RegExp("\\.".concat(t),"g");r=r.replace(i,".".concat(a,"-")).replace(o,"--".concat(a,"-")).replace(s,".".concat(n))}return r}var ut=!1;function we(){v.autoAddCss&&!ut&&(Yr(va()),ut=!0)}var Vr={mixout:function(){return{dom:{css:va,insertCss:we}}},hooks:function(){return{beforeDOMElementCreation:function(){we()},beforeI2svg:function(){we()}}}},T=M||{};T[_]||(T[_]={});T[_].styles||(T[_].styles={});T[_].hooks||(T[_].hooks={});T[_].shims||(T[_].shims=[]);var F=T[_],ha=[],ga=function(){x.removeEventListener("DOMContentLoaded",ga),fe=1,ha.map(function(t){return t()})},fe=!1;$&&(fe=(x.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(x.readyState),fe||x.addEventListener("DOMContentLoaded",ga));function Jr(e){$&&(fe?setTimeout(e,0):ha.push(e))}function ae(e){var t=e.tag,a=e.attributes,n=a===void 0?{}:a,r=e.children,i=r===void 0?[]:r;return typeof e=="string"?ma(e):"<".concat(t," ").concat(Hr(n),">").concat(i.map(ae).join(""),"</").concat(t,">")}function ct(e,t,a){if(e&&e[t]&&e[t][a])return{prefix:t,iconName:a,icon:e[t][a]}}var Se=function(t,a,n,r){var i=Object.keys(t),o=i.length,s=a,l,u,c;for(n===void 0?(l=1,c=t[i[0]]):(l=0,c=n);l<o;l++)u=i[l],c=s(c,t[u],u,t);return c};function pa(e){return j(e).length!==1?null:e.codePointAt(0).toString(16)}function dt(e){return Object.keys(e).reduce(function(t,a){var n=e[a],r=!!n.icon;return r?t[n.iconName]=n.icon:t[a]=n,t},{})}function _e(e,t){var a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},n=a.skipHooks,r=n===void 0?!1:n,i=dt(t);typeof F.hooks.addPack=="function"&&!r?F.hooks.addPack(e,dt(t)):F.styles[e]=f(f({},F.styles[e]||{}),i),e==="fas"&&_e("fa",t)}var Z=F.styles,qr=F.shims,ya=Object.keys(Ge),Qr=ya.reduce(function(e,t){return e[t]=Object.keys(Ge[t]),e},{}),Ve=null,ba={},xa={},wa={},Sa={},Aa={};function Zr(e){return~Lr.indexOf(e)}function ei(e,t){var a=t.split("-"),n=a[0],r=a.slice(1).join("-");return n===e&&r!==""&&!Zr(r)?r:null}var ka=function(){var t=function(i){return Se(Z,function(o,s,l){return o[l]=Se(s,i,{}),o},{})};ba=t(function(r,i,o){if(i[3]&&(r[i[3]]=o),i[2]){var s=i[2].filter(function(l){return typeof l=="number"});s.forEach(function(l){r[l.toString(16)]=o})}return r}),xa=t(function(r,i,o){if(r[o]=o,i[2]){var s=i[2].filter(function(l){return typeof l=="string"});s.forEach(function(l){r[l]=o})}return r}),Aa=t(function(r,i,o){var s=i[2];return r[o]=o,s.forEach(function(l){r[l]=o}),r});var a="far"in Z||v.autoFetchSvg,n=Se(qr,function(r,i){var o=i[0],s=i[1],l=i[2];return s==="far"&&!a&&(s="fas"),typeof o=="string"&&(r.names[o]={prefix:s,iconName:l}),typeof o=="number"&&(r.unicodes[o.toString(16)]={prefix:s,iconName:l}),r},{names:{},unicodes:{}});wa=n.names,Sa=n.unicodes,Ve=ve(v.styleDefault,{family:v.familyDefault})};Ur(function(e){Ve=ve(e.styleDefault,{family:v.familyDefault})});ka();function Je(e,t){return(ba[e]||{})[t]}function ti(e,t){return(xa[e]||{})[t]}function z(e,t){return(Aa[e]||{})[t]}function Pa(e){return wa[e]||{prefix:null,iconName:null}}function ai(e){var t=Sa[e],a=Je("fas",e);return t||(a?{prefix:"fas",iconName:a}:null)||{prefix:null,iconName:null}}function D(){return Ve}var Ia=function(){return{prefix:null,iconName:null,rest:[]}};function ni(e){var t=k,a=ya.reduce(function(n,r){return n[r]="".concat(v.cssPrefix,"-").concat(r),n},{});return aa.forEach(function(n){(e.includes(a[n])||e.some(function(r){return Qr[n].includes(r)}))&&(t=n)}),t}function ve(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=t.family,n=a===void 0?k:a,r=_r[n][e];if(n===ee&&!e)return"fad";var i=lt[n][e]||lt[n][r],o=e in F.styles?e:null,s=i||o||null;return s}function ri(e){var t=[],a=null;return e.forEach(function(n){var r=ei(v.cssPrefix,n);r?a=r:n&&t.push(n)}),{iconName:a,rest:t}}function mt(e){return e.sort().filter(function(t,a,n){return n.indexOf(t)===a})}var vt=ra.concat(na);function he(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=t.skipLookups,n=a===void 0?!1:a,r=null,i=mt(e.filter(function(p){return vt.includes(p)})),o=mt(e.filter(function(p){return!vt.includes(p)})),s=i.filter(function(p){return r=p,!Lt.includes(p)}),l=de(s,1),u=l[0],c=u===void 0?null:u,m=ni(i),y=f(f({},ri(o)),{},{prefix:ve(c,{family:m})});return f(f(f({},y),li({values:e,family:m,styles:Z,config:v,canonical:y,givenPrefix:r})),ii(n,r,y))}function ii(e,t,a){var n=a.prefix,r=a.iconName;if(e||!n||!r)return{prefix:n,iconName:r};var i=t==="fa"?Pa(r):{},o=z(n,r);return r=i.iconName||o||r,n=i.prefix||n,n==="far"&&!Z.far&&Z.fas&&!v.autoFetchSvg&&(n="fas"),{prefix:n,iconName:r}}var oi=aa.filter(function(e){return e!==k||e!==ee}),si=Object.keys(Oe).filter(function(e){return e!==k}).map(function(e){return Object.keys(Oe[e])}).flat();function li(e){var t=e.values,a=e.family,n=e.canonical,r=e.givenPrefix,i=r===void 0?"":r,o=e.styles,s=o===void 0?{}:o,l=e.config,u=l===void 0?{}:l,c=a===ee,m=t.includes("fa-duotone")||t.includes("fad"),y=u.familyDefault==="duotone",p=n.prefix==="fad"||n.prefix==="fa-duotone";if(!c&&(m||y||p)&&(n.prefix="fad"),(t.includes("fa-brands")||t.includes("fab"))&&(n.prefix="fab"),!n.prefix&&oi.includes(a)){var S=Object.keys(s).find(function(A){return si.includes(A)});if(S||u.autoFetchSvg){var b=An.get(a).defaultShortPrefixId;n.prefix=b,n.iconName=z(n.prefix,n.iconName)||n.iconName}}return(n.prefix==="fa"||i==="fa")&&(n.prefix=D()||"fas"),n}var fi=(function(){function e(){Ya(this,e),this.definitions={}}return Ha(e,[{key:"add",value:function(){for(var a=this,n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];var o=r.reduce(this._pullDefinitions,{});Object.keys(o).forEach(function(s){a.definitions[s]=f(f({},a.definitions[s]||{}),o[s]),_e(s,o[s]);var l=Ge[k][s];l&&_e(l,o[s]),ka()})}},{key:"reset",value:function(){this.definitions={}}},{key:"_pullDefinitions",value:function(a,n){var r=n.prefix&&n.iconName&&n.icon?{0:n}:n;return Object.keys(r).map(function(i){var o=r[i],s=o.prefix,l=o.iconName,u=o.icon,c=u[2];a[s]||(a[s]={}),c.length>0&&c.forEach(function(m){typeof m=="string"&&(a[s][m]=u)}),a[s][l]=u}),a}}])})(),ht=[],H={},G={},ui=Object.keys(G);function ci(e,t){var a=t.mixoutsTo;return ht=e,H={},Object.keys(G).forEach(function(n){ui.indexOf(n)===-1&&delete G[n]}),ht.forEach(function(n){var r=n.mixout?n.mixout():{};if(Object.keys(r).forEach(function(o){typeof r[o]=="function"&&(a[o]=r[o]),le(r[o])==="object"&&Object.keys(r[o]).forEach(function(s){a[o]||(a[o]={}),a[o][s]=r[o][s]})}),n.hooks){var i=n.hooks();Object.keys(i).forEach(function(o){H[o]||(H[o]=[]),H[o].push(i[o])})}n.provides&&n.provides(G)}),a}function Te(e,t){for(var a=arguments.length,n=new Array(a>2?a-2:0),r=2;r<a;r++)n[r-2]=arguments[r];var i=H[e]||[];return i.forEach(function(o){t=o.apply(null,[t].concat(n))}),t}function W(e){for(var t=arguments.length,a=new Array(t>1?t-1:0),n=1;n<t;n++)a[n-1]=arguments[n];var r=H[e]||[];r.forEach(function(i){i.apply(null,a)})}function L(){var e=arguments[0],t=Array.prototype.slice.call(arguments,1);return G[e]?G[e].apply(null,t):void 0}function $e(e){e.prefix==="fa"&&(e.prefix="fas");var t=e.iconName,a=e.prefix||D();if(t)return t=z(a,t)||t,ct(Oa.definitions,a,t)||ct(F.styles,a,t)}var Oa=new fi,di=function(){v.autoReplaceSvg=!1,v.observeMutations=!1,W("noAuto")},mi={i2svg:function(){var t=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};return $?(W("beforeI2svg",t),L("pseudoElements2svg",t),L("i2svg",t)):Promise.reject(new Error("Operation requires a DOM of some kind."))},watch:function(){var t=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},a=t.autoReplaceSvgRoot;v.autoReplaceSvg===!1&&(v.autoReplaceSvg=!0),v.observeMutations=!0,Jr(function(){hi({autoReplaceSvgRoot:a}),W("watch",t)})}},vi={icon:function(t){if(t===null)return null;if(le(t)==="object"&&t.prefix&&t.iconName)return{prefix:t.prefix,iconName:z(t.prefix,t.iconName)||t.iconName};if(Array.isArray(t)&&t.length===2){var a=t[1].indexOf("fa-")===0?t[1].slice(3):t[1],n=ve(t[0]);return{prefix:n,iconName:z(n,a)||a}}if(typeof t=="string"&&(t.indexOf("".concat(v.cssPrefix,"-"))>-1||t.match(Tr))){var r=he(t.split(" "),{skipLookups:!0});return{prefix:r.prefix||D(),iconName:z(r.prefix,r.iconName)||r.iconName}}if(typeof t=="string"){var i=D();return{prefix:i,iconName:z(i,t)||t}}}},E={noAuto:di,config:v,dom:mi,parse:vi,library:Oa,findIconDefinition:$e,toHtml:ae},hi=function(){var t=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},a=t.autoReplaceSvgRoot,n=a===void 0?x:a;(Object.keys(F.styles).length>0||v.autoFetchSvg)&&$&&v.autoReplaceSvg&&E.dom.i2svg({node:n})};function ge(e,t){return Object.defineProperty(e,"abstract",{get:t}),Object.defineProperty(e,"html",{get:function(){return e.abstract.map(function(n){return ae(n)})}}),Object.defineProperty(e,"node",{get:function(){if($){var n=x.createElement("div");return n.innerHTML=e.html,n.children}}}),e}function gi(e){var t=e.children,a=e.main,n=e.mask,r=e.attributes,i=e.styles,o=e.transform;if(Ke(o)&&a.found&&!n.found){var s=a.width,l=a.height,u={x:s/l/2,y:.5};r.style=me(f(f({},i),{},{"transform-origin":"".concat(u.x+o.x/16,"em ").concat(u.y+o.y/16,"em")}))}return[{tag:"svg",attributes:r,children:t}]}function pi(e){var t=e.prefix,a=e.iconName,n=e.children,r=e.attributes,i=e.symbol,o=i===!0?"".concat(t,"-").concat(v.cssPrefix,"-").concat(a):i;return[{tag:"svg",attributes:{style:"display: none;"},children:[{tag:"symbol",attributes:f(f({},r),{},{id:o}),children:n}]}]}function yi(e){var t=["aria-label","aria-labelledby","title","role"];return t.some(function(a){return a in e})}function qe(e){var t=e.icons,a=t.main,n=t.mask,r=e.prefix,i=e.iconName,o=e.transform,s=e.symbol,l=e.maskId,u=e.extra,c=e.watchable,m=c===void 0?!1:c,y=n.found?n:a,p=y.width,S=y.height,b=[v.replacementClass,i?"".concat(v.cssPrefix,"-").concat(i):""].filter(function(O){return u.classes.indexOf(O)===-1}).filter(function(O){return O!==""||!!O}).concat(u.classes).join(" "),A={children:[],attributes:f(f({},u.attributes),{},{"data-prefix":r,"data-icon":i,class:b,role:u.attributes.role||"img",viewBox:"0 0 ".concat(p," ").concat(S)})};!yi(u.attributes)&&!u.attributes["aria-hidden"]&&(A.attributes["aria-hidden"]="true"),m&&(A.attributes[R]="");var d=f(f({},A),{},{prefix:r,iconName:i,main:a,mask:n,maskId:l,transform:o,symbol:s,styles:f({},u.styles)}),h=n.found&&a.found?L("generateAbstractMask",d)||{children:[],attributes:{}}:L("generateAbstractIcon",d)||{children:[],attributes:{}},w=h.children,P=h.attributes;return d.children=w,d.attributes=P,s?pi(d):gi(d)}function gt(e){var t=e.content,a=e.width,n=e.height,r=e.transform,i=e.extra,o=e.watchable,s=o===void 0?!1:o,l=f(f({},i.attributes),{},{class:i.classes.join(" ")});s&&(l[R]="");var u=f({},i.styles);Ke(r)&&(u.transform=Xr({transform:r,width:a,height:n}),u["-webkit-transform"]=u.transform);var c=me(u);c.length>0&&(l.style=c);var m=[];return m.push({tag:"span",attributes:l,children:[t]}),m}function bi(e){var t=e.content,a=e.extra,n=f(f({},a.attributes),{},{class:a.classes.join(" ")}),r=me(a.styles);r.length>0&&(n.style=r);var i=[];return i.push({tag:"span",attributes:n,children:[t]}),i}var Ae=F.styles;function Me(e){var t=e[0],a=e[1],n=e.slice(4),r=de(n,1),i=r[0],o=null;return Array.isArray(i)?o={tag:"g",attributes:{class:"".concat(v.cssPrefix,"-").concat(xe.GROUP)},children:[{tag:"path",attributes:{class:"".concat(v.cssPrefix,"-").concat(xe.SECONDARY),fill:"currentColor",d:i[0]}},{tag:"path",attributes:{class:"".concat(v.cssPrefix,"-").concat(xe.PRIMARY),fill:"currentColor",d:i[1]}}]}:o={tag:"path",attributes:{fill:"currentColor",d:i}},{found:!0,width:t,height:a,icon:o}}var xi={found:!1,width:512,height:512};function wi(e,t){!fa&&!v.showMissingIcons&&e&&console.error('Icon with name "'.concat(e,'" and prefix "').concat(t,'" is missing.'))}function De(e,t){var a=t;return t==="fa"&&v.styleDefault!==null&&(t=D()),new Promise(function(n,r){if(a==="fa"){var i=Pa(e)||{};e=i.iconName||e,t=i.prefix||t}if(e&&t&&Ae[t]&&Ae[t][e]){var o=Ae[t][e];return n(Me(o))}wi(e,t),n(f(f({},xi),{},{icon:v.showMissingIcons&&e?L("missingIconAbstract")||{}:{}}))})}var pt=function(){},Le=v.measurePerformance&&ne&&ne.mark&&ne.measure?ne:{mark:pt,measure:pt},J='FA "7.2.0"',Si=function(t){return Le.mark("".concat(J," ").concat(t," begins")),function(){return Ea(t)}},Ea=function(t){Le.mark("".concat(J," ").concat(t," ends")),Le.measure("".concat(J," ").concat(t),"".concat(J," ").concat(t," begins"),"".concat(J," ").concat(t," ends"))},Qe={begin:Si,end:Ea},oe=function(){};function yt(e){var t=e.getAttribute?e.getAttribute(R):null;return typeof t=="string"}function Ai(e){var t=e.getAttribute?e.getAttribute(Be):null,a=e.getAttribute?e.getAttribute(He):null;return t&&a}function ki(e){return e&&e.classList&&e.classList.contains&&e.classList.contains(v.replacementClass)}function Pi(){if(v.autoReplaceSvg===!0)return se.replace;var e=se[v.autoReplaceSvg];return e||se.replace}function Ii(e){return x.createElementNS("http://www.w3.org/2000/svg",e)}function Oi(e){return x.createElement(e)}function Fa(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=t.ceFn,n=a===void 0?e.tag==="svg"?Ii:Oi:a;if(typeof e=="string")return x.createTextNode(e);var r=n(e.tag);Object.keys(e.attributes||[]).forEach(function(o){r.setAttribute(o,e.attributes[o])});var i=e.children||[];return i.forEach(function(o){r.appendChild(Fa(o,{ceFn:n}))}),r}function Ei(e){var t=" ".concat(e.outerHTML," ");return t="".concat(t,"Font Awesome fontawesome.com "),t}var se={replace:function(t){var a=t[0];if(a.parentNode)if(t[1].forEach(function(r){a.parentNode.insertBefore(Fa(r),a)}),a.getAttribute(R)===null&&v.keepOriginalSource){var n=x.createComment(Ei(a));a.parentNode.replaceChild(n,a)}else a.remove()},nest:function(t){var a=t[0],n=t[1];if(~Xe(a).indexOf(v.replacementClass))return se.replace(t);var r=new RegExp("".concat(v.cssPrefix,"-.*"));if(delete n[0].attributes.id,n[0].attributes.class){var i=n[0].attributes.class.split(" ").reduce(function(s,l){return l===v.replacementClass||l.match(r)?s.toSvg.push(l):s.toNode.push(l),s},{toNode:[],toSvg:[]});n[0].attributes.class=i.toSvg.join(" "),i.toNode.length===0?a.removeAttribute("class"):a.setAttribute("class",i.toNode.join(" "))}var o=n.map(function(s){return ae(s)}).join(`
`);a.setAttribute(R,""),a.innerHTML=o}};function bt(e){e()}function ja(e,t){var a=typeof t=="function"?t:oe;if(e.length===0)a();else{var n=bt;v.mutateApproach===Cr&&(n=M.requestAnimationFrame||bt),n(function(){var r=Pi(),i=Qe.begin("mutate");e.map(r),i(),a()})}}var Ze=!1;function Ca(){Ze=!0}function ze(){Ze=!1}var ue=null;function xt(e){if(rt&&v.observeMutations){var t=e.treeCallback,a=t===void 0?oe:t,n=e.nodeCallback,r=n===void 0?oe:n,i=e.pseudoElementsCallback,o=i===void 0?oe:i,s=e.observeMutationsRoot,l=s===void 0?x:s;ue=new rt(function(u){if(!Ze){var c=D();K(u).forEach(function(m){if(m.type==="childList"&&m.addedNodes.length>0&&!yt(m.addedNodes[0])&&(v.searchPseudoElements&&o(m.target),a(m.target)),m.type==="attributes"&&m.target.parentNode&&v.searchPseudoElements&&o([m.target],!0),m.type==="attributes"&&yt(m.target)&&~Dr.indexOf(m.attributeName))if(m.attributeName==="class"&&Ai(m.target)){var y=he(Xe(m.target)),p=y.prefix,S=y.iconName;m.target.setAttribute(Be,p||c),S&&m.target.setAttribute(He,S)}else ki(m.target)&&r(m.target)})}}),$&&ue.observe(l,{childList:!0,attributes:!0,characterData:!0,subtree:!0})}}function Fi(){ue&&ue.disconnect()}function ji(e){var t=e.getAttribute("style"),a=[];return t&&(a=t.split(";").reduce(function(n,r){var i=r.split(":"),o=i[0],s=i.slice(1);return o&&s.length>0&&(n[o]=s.join(":").trim()),n},{})),a}function Ci(e){var t=e.getAttribute("data-prefix"),a=e.getAttribute("data-icon"),n=e.innerText!==void 0?e.innerText.trim():"",r=he(Xe(e));return r.prefix||(r.prefix=D()),t&&a&&(r.prefix=t,r.iconName=a),r.iconName&&r.prefix||(r.prefix&&n.length>0&&(r.iconName=ti(r.prefix,e.innerText)||Je(r.prefix,pa(e.innerText))),!r.iconName&&v.autoFetchSvg&&e.firstChild&&e.firstChild.nodeType===Node.TEXT_NODE&&(r.iconName=e.firstChild.data)),r}function Ni(e){var t=K(e.attributes).reduce(function(a,n){return a.name!=="class"&&a.name!=="style"&&(a[n.name]=n.value),a},{});return t}function _i(){return{iconName:null,prefix:null,transform:C,symbol:!1,mask:{iconName:null,prefix:null,rest:[]},maskId:null,extra:{classes:[],styles:{},attributes:{}}}}function wt(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{styleParser:!0},a=Ci(e),n=a.iconName,r=a.prefix,i=a.rest,o=Ni(e),s=Te("parseNodeAttributes",{},e),l=t.styleParser?ji(e):[];return f({iconName:n,prefix:r,transform:C,mask:{iconName:null,prefix:null,rest:[]},maskId:null,symbol:!1,extra:{classes:i,styles:l,attributes:o}},s)}var Ti=F.styles;function Na(e){var t=v.autoReplaceSvg==="nest"?wt(e,{styleParser:!1}):wt(e);return~t.extra.classes.indexOf(ca)?L("generateLayersText",e,t):L("generateSvgReplacementMutation",e,t)}function $i(){return[].concat(j(na),j(ra))}function St(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;if(!$)return Promise.resolve();var a=x.documentElement.classList,n=function(m){return a.add("".concat(st,"-").concat(m))},r=function(m){return a.remove("".concat(st,"-").concat(m))},i=v.autoFetchSvg?$i():Lt.concat(Object.keys(Ti));i.includes("fa")||i.push("fa");var o=[".".concat(ca,":not([").concat(R,"])")].concat(i.map(function(c){return".".concat(c,":not([").concat(R,"])")})).join(", ");if(o.length===0)return Promise.resolve();var s=[];try{s=K(e.querySelectorAll(o))}catch{}if(s.length>0)n("pending"),r("complete");else return Promise.resolve();var l=Qe.begin("onTree"),u=s.reduce(function(c,m){try{var y=Na(m);y&&c.push(y)}catch(p){fa||p.name==="MissingIcon"&&console.error(p)}return c},[]);return new Promise(function(c,m){Promise.all(u).then(function(y){ja(y,function(){n("active"),n("complete"),r("pending"),typeof t=="function"&&t(),l(),c()})}).catch(function(y){l(),m(y)})})}function Mi(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;Na(e).then(function(a){a&&ja([a],t)})}function Di(e){return function(t){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=(t||{}).icon?t:$e(t||{}),r=a.mask;return r&&(r=(r||{}).icon?r:$e(r||{})),e(n,f(f({},a),{},{mask:r}))}}var Li=function(t){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=a.transform,r=n===void 0?C:n,i=a.symbol,o=i===void 0?!1:i,s=a.mask,l=s===void 0?null:s,u=a.maskId,c=u===void 0?null:u,m=a.classes,y=m===void 0?[]:m,p=a.attributes,S=p===void 0?{}:p,b=a.styles,A=b===void 0?{}:b;if(t){var d=t.prefix,h=t.iconName,w=t.icon;return ge(f({type:"icon"},t),function(){return W("beforeDOMElementCreation",{iconDefinition:t,params:a}),qe({icons:{main:Me(w),mask:l?Me(l.icon):{found:!1,width:null,height:null,icon:{}}},prefix:d,iconName:h,transform:f(f({},C),r),symbol:o,maskId:c,extra:{attributes:S,styles:A,classes:y}})})}},zi={mixout:function(){return{icon:Di(Li)}},hooks:function(){return{mutationObserverCallbacks:function(a){return a.treeCallback=St,a.nodeCallback=Mi,a}}},provides:function(t){t.i2svg=function(a){var n=a.node,r=n===void 0?x:n,i=a.callback,o=i===void 0?function(){}:i;return St(r,o)},t.generateSvgReplacementMutation=function(a,n){var r=n.iconName,i=n.prefix,o=n.transform,s=n.symbol,l=n.mask,u=n.maskId,c=n.extra;return new Promise(function(m,y){Promise.all([De(r,i),l.iconName?De(l.iconName,l.prefix):Promise.resolve({found:!1,width:512,height:512,icon:{}})]).then(function(p){var S=de(p,2),b=S[0],A=S[1];m([a,qe({icons:{main:b,mask:A},prefix:i,iconName:r,transform:o,symbol:s,maskId:u,extra:c,watchable:!0})])}).catch(y)})},t.generateAbstractIcon=function(a){var n=a.children,r=a.attributes,i=a.main,o=a.transform,s=a.styles,l=me(s);l.length>0&&(r.style=l);var u;return Ke(o)&&(u=L("generateAbstractTransformGrouping",{main:i,transform:o,containerWidth:i.width,iconWidth:i.width})),n.push(u||i.icon),{children:n,attributes:r}}}},Ri={mixout:function(){return{layer:function(a){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=n.classes,i=r===void 0?[]:r;return ge({type:"layer"},function(){W("beforeDOMElementCreation",{assembler:a,params:n});var o=[];return a(function(s){Array.isArray(s)?s.map(function(l){o=o.concat(l.abstract)}):o=o.concat(s.abstract)}),[{tag:"span",attributes:{class:["".concat(v.cssPrefix,"-layers")].concat(j(i)).join(" ")},children:o}]})}}}},Wi={mixout:function(){return{counter:function(a){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};n.title;var r=n.classes,i=r===void 0?[]:r,o=n.attributes,s=o===void 0?{}:o,l=n.styles,u=l===void 0?{}:l;return ge({type:"counter",content:a},function(){return W("beforeDOMElementCreation",{content:a,params:n}),bi({content:a.toString(),extra:{attributes:s,styles:u,classes:["".concat(v.cssPrefix,"-layers-counter")].concat(j(i))}})})}}}},Ui={mixout:function(){return{text:function(a){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=n.transform,i=r===void 0?C:r,o=n.classes,s=o===void 0?[]:o,l=n.attributes,u=l===void 0?{}:l,c=n.styles,m=c===void 0?{}:c;return ge({type:"text",content:a},function(){return W("beforeDOMElementCreation",{content:a,params:n}),gt({content:a,transform:f(f({},C),i),extra:{attributes:u,styles:m,classes:["".concat(v.cssPrefix,"-layers-text")].concat(j(s))}})})}}},provides:function(t){t.generateLayersText=function(a,n){var r=n.transform,i=n.extra,o=null,s=null;if(Mt){var l=parseInt(getComputedStyle(a).fontSize,10),u=a.getBoundingClientRect();o=u.width/l,s=u.height/l}return Promise.resolve([a,gt({content:a.innerHTML,width:o,height:s,transform:r,extra:i,watchable:!0})])}}},_a=new RegExp('"',"ug"),At=[1105920,1112319],kt=f(f(f(f({},{FontAwesome:{normal:"fas",400:"fas"}}),Sn),Fr),Cn),Re=Object.keys(kt).reduce(function(e,t){return e[t.toLowerCase()]=kt[t],e},{}),Yi=Object.keys(Re).reduce(function(e,t){var a=Re[t];return e[t]=a[900]||j(Object.entries(a))[0][1],e},{});function Bi(e){var t=e.replace(_a,"");return pa(j(t)[0]||"")}function Hi(e){var t=e.getPropertyValue("font-feature-settings").includes("ss01"),a=e.getPropertyValue("content"),n=a.replace(_a,""),r=n.codePointAt(0),i=r>=At[0]&&r<=At[1],o=n.length===2?n[0]===n[1]:!1;return i||o||t}function Gi(e,t){var a=e.replace(/^['"]|['"]$/g,"").toLowerCase(),n=parseInt(t),r=isNaN(n)?"normal":n;return(Re[a]||{})[r]||Yi[a]}function Pt(e,t){var a="".concat(jr).concat(t.replace(":","-"));return new Promise(function(n,r){if(e.getAttribute(a)!==null)return n();var i=K(e.children),o=i.filter(function(U){return U.getAttribute(Fe)===t})[0],s=M.getComputedStyle(e,t),l=s.getPropertyValue("font-family"),u=l.match($r),c=s.getPropertyValue("font-weight"),m=s.getPropertyValue("content");if(o&&!u)return e.removeChild(o),n();if(u&&m!=="none"&&m!==""){var y=s.getPropertyValue("content"),p=Gi(l,c),S=Bi(y),b=u[0].startsWith("FontAwesome"),A=Hi(s),d=Je(p,S),h=d;if(b){var w=ai(S);w.iconName&&w.prefix&&(d=w.iconName,p=w.prefix)}if(d&&!A&&(!o||o.getAttribute(Be)!==p||o.getAttribute(He)!==h)){e.setAttribute(a,h),o&&e.removeChild(o);var P=_i(),O=P.extra;O.attributes[Fe]=t,De(d,p).then(function(U){var V=qe(f(f({},P),{},{icons:{main:U,mask:Ia()},prefix:p,iconName:h,extra:O,watchable:!0})),pe=x.createElementNS("http://www.w3.org/2000/svg","svg");t==="::before"?e.insertBefore(pe,e.firstChild):e.appendChild(pe),pe.outerHTML=V.map(function(Da){return ae(Da)}).join(`
`),e.removeAttribute(a),n()}).catch(r)}else n()}else n()})}function Xi(e){return Promise.all([Pt(e,"::before"),Pt(e,"::after")])}function Ki(e){return e.parentNode!==document.head&&!~Nr.indexOf(e.tagName.toUpperCase())&&!e.getAttribute(Fe)&&(!e.parentNode||e.parentNode.tagName!=="svg")}var Vi=function(t){return!!t&&la.some(function(a){return t.includes(a)})},Ji=function(t){if(!t)return[];var a=new Set,n=t.split(/,(?![^()]*\))/).map(function(l){return l.trim()});n=n.flatMap(function(l){return l.includes("(")?l:l.split(",").map(function(u){return u.trim()})});var r=ie(n),i;try{for(r.s();!(i=r.n()).done;){var o=i.value;if(Vi(o)){var s=la.reduce(function(l,u){return l.replace(u,"")},o);s!==""&&s!=="*"&&a.add(s)}}}catch(l){r.e(l)}finally{r.f()}return a};function It(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1;if($){var a;if(t)a=e;else if(v.searchPseudoElementsFullScan)a=e.querySelectorAll("*");else{var n=new Set,r=ie(document.styleSheets),i;try{for(r.s();!(i=r.n()).done;){var o=i.value;try{var s=ie(o.cssRules),l;try{for(s.s();!(l=s.n()).done;){var u=l.value,c=Ji(u.selectorText),m=ie(c),y;try{for(m.s();!(y=m.n()).done;){var p=y.value;n.add(p)}}catch(b){m.e(b)}finally{m.f()}}}catch(b){s.e(b)}finally{s.f()}}catch(b){v.searchPseudoElementsWarnings&&console.warn("Font Awesome: cannot parse stylesheet: ".concat(o.href," (").concat(b.message,`)
If it declares any Font Awesome CSS pseudo-elements, they will not be rendered as SVG icons. Add crossorigin="anonymous" to the <link>, enable searchPseudoElementsFullScan for slower but more thorough DOM parsing, or suppress this warning by setting searchPseudoElementsWarnings to false.`))}}}catch(b){r.e(b)}finally{r.f()}if(!n.size)return;var S=Array.from(n).join(", ");try{a=e.querySelectorAll(S)}catch{}}return new Promise(function(b,A){var d=K(a).filter(Ki).map(Xi),h=Qe.begin("searchPseudoElements");Ca(),Promise.all(d).then(function(){h(),ze(),b()}).catch(function(){h(),ze(),A()})})}}var qi={hooks:function(){return{mutationObserverCallbacks:function(a){return a.pseudoElementsCallback=It,a}}},provides:function(t){t.pseudoElements2svg=function(a){var n=a.node,r=n===void 0?x:n;v.searchPseudoElements&&It(r)}}},Ot=!1,Qi={mixout:function(){return{dom:{unwatch:function(){Ca(),Ot=!0}}}},hooks:function(){return{bootstrap:function(){xt(Te("mutationObserverCallbacks",{}))},noAuto:function(){Fi()},watch:function(a){var n=a.observeMutationsRoot;Ot?ze():xt(Te("mutationObserverCallbacks",{observeMutationsRoot:n}))}}}},Et=function(t){var a={size:16,x:0,y:0,flipX:!1,flipY:!1,rotate:0};return t.toLowerCase().split(" ").reduce(function(n,r){var i=r.toLowerCase().split("-"),o=i[0],s=i.slice(1).join("-");if(o&&s==="h")return n.flipX=!0,n;if(o&&s==="v")return n.flipY=!0,n;if(s=parseFloat(s),isNaN(s))return n;switch(o){case"grow":n.size=n.size+s;break;case"shrink":n.size=n.size-s;break;case"left":n.x=n.x-s;break;case"right":n.x=n.x+s;break;case"up":n.y=n.y-s;break;case"down":n.y=n.y+s;break;case"rotate":n.rotate=n.rotate+s;break}return n},a)},Zi={mixout:function(){return{parse:{transform:function(a){return Et(a)}}}},hooks:function(){return{parseNodeAttributes:function(a,n){var r=n.getAttribute("data-fa-transform");return r&&(a.transform=Et(r)),a}}},provides:function(t){t.generateAbstractTransformGrouping=function(a){var n=a.main,r=a.transform,i=a.containerWidth,o=a.iconWidth,s={transform:"translate(".concat(i/2," 256)")},l="translate(".concat(r.x*32,", ").concat(r.y*32,") "),u="scale(".concat(r.size/16*(r.flipX?-1:1),", ").concat(r.size/16*(r.flipY?-1:1),") "),c="rotate(".concat(r.rotate," 0 0)"),m={transform:"".concat(l," ").concat(u," ").concat(c)},y={transform:"translate(".concat(o/2*-1," -256)")},p={outer:s,inner:m,path:y};return{tag:"g",attributes:f({},p.outer),children:[{tag:"g",attributes:f({},p.inner),children:[{tag:n.icon.tag,children:n.icon.children,attributes:f(f({},n.icon.attributes),p.path)}]}]}}}},ke={x:0,y:0,width:"100%",height:"100%"};function Ft(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;return e.attributes&&(e.attributes.fill||t)&&(e.attributes.fill="black"),e}function eo(e){return e.tag==="g"?e.children:[e]}var to={hooks:function(){return{parseNodeAttributes:function(a,n){var r=n.getAttribute("data-fa-mask"),i=r?he(r.split(" ").map(function(o){return o.trim()})):Ia();return i.prefix||(i.prefix=D()),a.mask=i,a.maskId=n.getAttribute("data-fa-mask-id"),a}}},provides:function(t){t.generateAbstractMask=function(a){var n=a.children,r=a.attributes,i=a.main,o=a.mask,s=a.maskId,l=a.transform,u=i.width,c=i.icon,m=o.width,y=o.icon,p=Gr({transform:l,containerWidth:m,iconWidth:u}),S={tag:"rect",attributes:f(f({},ke),{},{fill:"white"})},b=c.children?{children:c.children.map(Ft)}:{},A={tag:"g",attributes:f({},p.inner),children:[Ft(f({tag:c.tag,attributes:f(f({},c.attributes),p.path)},b))]},d={tag:"g",attributes:f({},p.outer),children:[A]},h="mask-".concat(s||ft()),w="clip-".concat(s||ft()),P={tag:"mask",attributes:f(f({},ke),{},{id:h,maskUnits:"userSpaceOnUse",maskContentUnits:"userSpaceOnUse"}),children:[S,d]},O={tag:"defs",children:[{tag:"clipPath",attributes:{id:w},children:eo(y)},P]};return n.push(O,{tag:"rect",attributes:f({fill:"currentColor","clip-path":"url(#".concat(w,")"),mask:"url(#".concat(h,")")},ke)}),{children:n,attributes:r}}}},ao={provides:function(t){var a=!1;M.matchMedia&&(a=M.matchMedia("(prefers-reduced-motion: reduce)").matches),t.missingIconAbstract=function(){var n=[],r={fill:"currentColor"},i={attributeType:"XML",repeatCount:"indefinite",dur:"2s"};n.push({tag:"path",attributes:f(f({},r),{},{d:"M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z"})});var o=f(f({},i),{},{attributeName:"opacity"}),s={tag:"circle",attributes:f(f({},r),{},{cx:"256",cy:"364",r:"28"}),children:[]};return a||s.children.push({tag:"animate",attributes:f(f({},i),{},{attributeName:"r",values:"28;14;28;28;14;28;"})},{tag:"animate",attributes:f(f({},o),{},{values:"1;0;1;1;0;1;"})}),n.push(s),n.push({tag:"path",attributes:f(f({},r),{},{opacity:"1",d:"M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z"}),children:a?[]:[{tag:"animate",attributes:f(f({},o),{},{values:"1;0;0;0;0;1;"})}]}),a||n.push({tag:"path",attributes:f(f({},r),{},{opacity:"0",d:"M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z"}),children:[{tag:"animate",attributes:f(f({},o),{},{values:"0;0;1;1;0;0;"})}]}),{tag:"g",attributes:{class:"missing"},children:n}}}},no={hooks:function(){return{parseNodeAttributes:function(a,n){var r=n.getAttribute("data-fa-symbol"),i=r===null?!1:r===""?!0:r;return a.symbol=i,a}}}},ro=[Vr,zi,Ri,Wi,Ui,qi,Qi,Zi,to,ao,no];ci(ro,{mixoutsTo:E});E.noAuto;E.config;var bo=E.library;E.dom;var We=E.parse;E.findIconDefinition;E.toHtml;var io=E.icon;E.layer;E.text;E.counter;function I(e,t,a){return(t=fo(t))in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function jt(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter(function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable})),a.push.apply(a,n)}return a}function N(e){for(var t=1;t<arguments.length;t++){var a=arguments[t]!=null?arguments[t]:{};t%2?jt(Object(a),!0).forEach(function(n){I(e,n,a[n])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):jt(Object(a)).forEach(function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(a,n))})}return e}function oo(e,t){if(e==null)return{};var a,n,r=so(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(n=0;n<i.length;n++)a=i[n],t.indexOf(a)===-1&&{}.propertyIsEnumerable.call(e,a)&&(r[a]=e[a])}return r}function so(e,t){if(e==null)return{};var a={};for(var n in e)if({}.hasOwnProperty.call(e,n)){if(t.indexOf(n)!==-1)continue;a[n]=e[n]}return a}function lo(e,t){if(typeof e!="object"||!e)return e;var a=e[Symbol.toPrimitive];if(a!==void 0){var n=a.call(e,t);if(typeof n!="object")return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return(t==="string"?String:Number)(e)}function fo(e){var t=lo(e,"string");return typeof t=="symbol"?t:t+""}function ce(e){"@babel/helpers - typeof";return ce=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(t){return typeof t}:function(t){return t&&typeof Symbol=="function"&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},ce(e)}function Pe(e,t){return Array.isArray(t)&&t.length>0||!Array.isArray(t)&&t?I({},e,t):{}}function uo(e){var t,a=(t={"fa-spin":e.spin,"fa-pulse":e.pulse,"fa-fw":e.fixedWidth,"fa-border":e.border,"fa-li":e.listItem,"fa-inverse":e.inverse,"fa-flip":e.flip===!0,"fa-flip-horizontal":e.flip==="horizontal"||e.flip==="both","fa-flip-vertical":e.flip==="vertical"||e.flip==="both"},I(I(I(I(I(I(I(I(I(I(t,"fa-".concat(e.size),e.size!==null),"fa-rotate-".concat(e.rotation),e.rotation!==null),"fa-rotate-by",e.rotateBy),"fa-pull-".concat(e.pull),e.pull!==null),"fa-swap-opacity",e.swapOpacity),"fa-bounce",e.bounce),"fa-shake",e.shake),"fa-beat",e.beat),"fa-fade",e.fade),"fa-beat-fade",e.beatFade),I(I(I(I(t,"fa-flash",e.flash),"fa-spin-pulse",e.spinPulse),"fa-spin-reverse",e.spinReverse),"fa-width-auto",e.widthAuto));return Object.keys(a).map(function(n){return a[n]?n:null}).filter(function(n){return n})}var co=typeof globalThis<"u"?globalThis:typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},Ta={exports:{}};(function(e){(function(t){var a=function(d,h,w){if(!u(h)||m(h)||y(h)||p(h)||l(h))return h;var P,O=0,U=0;if(c(h))for(P=[],U=h.length;O<U;O++)P.push(a(d,h[O],w));else{P={};for(var V in h)Object.prototype.hasOwnProperty.call(h,V)&&(P[d(V,w)]=a(d,h[V],w))}return P},n=function(d,h){h=h||{};var w=h.separator||"_",P=h.split||/(?=[A-Z])/;return d.split(P).join(w)},r=function(d){return S(d)?d:(d=d.replace(/[\-_\s]+(.)?/g,function(h,w){return w?w.toUpperCase():""}),d.substr(0,1).toLowerCase()+d.substr(1))},i=function(d){var h=r(d);return h.substr(0,1).toUpperCase()+h.substr(1)},o=function(d,h){return n(d,h).toLowerCase()},s=Object.prototype.toString,l=function(d){return typeof d=="function"},u=function(d){return d===Object(d)},c=function(d){return s.call(d)=="[object Array]"},m=function(d){return s.call(d)=="[object Date]"},y=function(d){return s.call(d)=="[object RegExp]"},p=function(d){return s.call(d)=="[object Boolean]"},S=function(d){return d=d-0,d===d},b=function(d,h){var w=h&&"process"in h?h.process:h;return typeof w!="function"?d:function(P,O){return w(P,d,O)}},A={camelize:r,decamelize:o,pascalize:i,depascalize:o,camelizeKeys:function(d,h){return a(b(r,h),d)},decamelizeKeys:function(d,h){return a(b(o,h),d,h)},pascalizeKeys:function(d,h){return a(b(i,h),d)},depascalizeKeys:function(){return this.decamelizeKeys.apply(this,arguments)}};e.exports?e.exports=A:t.humps=A})(co)})(Ta);var mo=Ta.exports,vo=["class","style"];function ho(e){return e.split(";").map(function(t){return t.trim()}).filter(function(t){return t}).reduce(function(t,a){var n=a.indexOf(":"),r=mo.camelize(a.slice(0,n)),i=a.slice(n+1).trim();return t[r]=i,t},{})}function go(e){return e.split(/\s+/).reduce(function(t,a){return t[a]=!0,t},{})}function $a(e){var t=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};if(typeof e=="string")return e;var n=(e.children||[]).map(function(l){return $a(l)}),r=Object.keys(e.attributes||{}).reduce(function(l,u){var c=e.attributes[u];switch(u){case"class":l.class=go(c);break;case"style":l.style=ho(c);break;default:l.attrs[u]=c}return l},{attrs:{},class:{},style:{}});a.class;var i=a.style,o=i===void 0?{}:i,s=oo(a,vo);return Ra(e.tag,N(N(N({},t),{},{class:r.class,style:N(N({},r.style),o)},r.attrs),s),n)}var Ma=!1;try{Ma=!0}catch{}function po(){if(!Ma&&console&&typeof console.error=="function"){var e;(e=console).error.apply(e,arguments)}}function Ct(e){if(e&&ce(e)==="object"&&e.prefix&&e.iconName&&e.icon)return e;if(We.icon)return We.icon(e);if(e===null)return null;if(ce(e)==="object"&&e.prefix&&e.iconName)return e;if(Array.isArray(e)&&e.length===2)return{prefix:e[0],iconName:e[1]};if(typeof e=="string")return{prefix:"fas",iconName:e}}var xo=La({name:"FontAwesomeIcon",props:{border:{type:Boolean,default:!1},fixedWidth:{type:Boolean,default:!1},flip:{type:[Boolean,String],default:!1,validator:function(t){return[!0,!1,"horizontal","vertical","both"].indexOf(t)>-1}},icon:{type:[Object,Array,String],required:!0},mask:{type:[Object,Array,String],default:null},maskId:{type:String,default:null},listItem:{type:Boolean,default:!1},pull:{type:String,default:null,validator:function(t){return["right","left"].indexOf(t)>-1}},pulse:{type:Boolean,default:!1},rotation:{type:[String,Number],default:null,validator:function(t){return[90,180,270].indexOf(Number.parseInt(t,10))>-1}},rotateBy:{type:Boolean,default:!1},swapOpacity:{type:Boolean,default:!1},size:{type:String,default:null,validator:function(t){return["2xs","xs","sm","lg","xl","2xl","1x","2x","3x","4x","5x","6x","7x","8x","9x","10x"].indexOf(t)>-1}},spin:{type:Boolean,default:!1},transform:{type:[String,Object],default:null},symbol:{type:[Boolean,String],default:!1},title:{type:String,default:null},titleId:{type:String,default:null},inverse:{type:Boolean,default:!1},bounce:{type:Boolean,default:!1},shake:{type:Boolean,default:!1},beat:{type:Boolean,default:!1},fade:{type:Boolean,default:!1},beatFade:{type:Boolean,default:!1},flash:{type:Boolean,default:!1},spinPulse:{type:Boolean,default:!1},spinReverse:{type:Boolean,default:!1},widthAuto:{type:Boolean,default:!1}},setup:function(t,a){var n=a.attrs,r=Y(function(){return Ct(t.icon)}),i=Y(function(){return Pe("classes",uo(t))}),o=Y(function(){return Pe("transform",typeof t.transform=="string"?We.transform(t.transform):t.transform)}),s=Y(function(){return Pe("mask",Ct(t.mask))}),l=Y(function(){var c=N(N(N(N({},i.value),o.value),s.value),{},{symbol:t.symbol,maskId:t.maskId});return c.title=t.title,c.titleId=t.titleId,io(r.value,c)});za(l,function(c){if(!c)return po("Could not find one or more icon(s)",r.value,s.value)},{immediate:!0});var u=Y(function(){return l.value?$a(l.value.abstract[0],{},n):null});return function(){return u.value}}});export{xo as F,bo as l};

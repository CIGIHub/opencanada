// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeline', 'timelineEnd', 'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

// Place any jQuery/helper plugins in here.

// Smooth Scroll https://css-tricks.com/snippets/jquery/smooth-scrolling/
$(function() {
  $('a[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html, body').animate({
        	scrollTop: $( $(this).attr('href') ).offset().top
		}, 1000);
		return false;
      }
    }
  });
});



/*! WOW - v1.1.3 - 2016-05-06
* Copyright (c) 2016 Matthieu Aussaguel;*/(function(){var a,b,c,d,e,f=function(a,b){return function(){return a.apply(b,arguments)}},g=[].indexOf||function(a){for(var b=0,c=this.length;c>b;b++)if(b in this&&this[b]===a)return b;return-1};b=function(){function a(){}return a.prototype.extend=function(a,b){var c,d;for(c in b)d=b[c],null==a[c]&&(a[c]=d);return a},a.prototype.isMobile=function(a){return/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(a)},a.prototype.createEvent=function(a,b,c,d){var e;return null==b&&(b=!1),null==c&&(c=!1),null==d&&(d=null),null!=document.createEvent?(e=document.createEvent("CustomEvent"),e.initCustomEvent(a,b,c,d)):null!=document.createEventObject?(e=document.createEventObject(),e.eventType=a):e.eventName=a,e},a.prototype.emitEvent=function(a,b){return null!=a.dispatchEvent?a.dispatchEvent(b):b in(null!=a)?a[b]():"on"+b in(null!=a)?a["on"+b]():void 0},a.prototype.addEvent=function(a,b,c){return null!=a.addEventListener?a.addEventListener(b,c,!1):null!=a.attachEvent?a.attachEvent("on"+b,c):a[b]=c},a.prototype.removeEvent=function(a,b,c){return null!=a.removeEventListener?a.removeEventListener(b,c,!1):null!=a.detachEvent?a.detachEvent("on"+b,c):delete a[b]},a.prototype.innerHeight=function(){return"innerHeight"in window?window.innerHeight:document.documentElement.clientHeight},a}(),c=this.WeakMap||this.MozWeakMap||(c=function(){function a(){this.keys=[],this.values=[]}return a.prototype.get=function(a){var b,c,d,e,f;for(f=this.keys,b=d=0,e=f.length;e>d;b=++d)if(c=f[b],c===a)return this.values[b]},a.prototype.set=function(a,b){var c,d,e,f,g;for(g=this.keys,c=e=0,f=g.length;f>e;c=++e)if(d=g[c],d===a)return void(this.values[c]=b);return this.keys.push(a),this.values.push(b)},a}()),a=this.MutationObserver||this.WebkitMutationObserver||this.MozMutationObserver||(a=function(){function a(){"undefined"!=typeof console&&null!==console&&console.warn("MutationObserver is not supported by your browser."),"undefined"!=typeof console&&null!==console&&console.warn("WOW.js cannot detect dom mutations, please call .sync() after loading new content.")}return a.notSupported=!0,a.prototype.observe=function(){},a}()),d=this.getComputedStyle||function(a,b){return this.getPropertyValue=function(b){var c;return"float"===b&&(b="styleFloat"),e.test(b)&&b.replace(e,function(a,b){return b.toUpperCase()}),(null!=(c=a.currentStyle)?c[b]:void 0)||null},this},e=/(\-([a-z]){1})/g,this.WOW=function(){function e(a){null==a&&(a={}),this.scrollCallback=f(this.scrollCallback,this),this.scrollHandler=f(this.scrollHandler,this),this.resetAnimation=f(this.resetAnimation,this),this.start=f(this.start,this),this.scrolled=!0,this.config=this.util().extend(a,this.defaults),null!=a.scrollContainer&&(this.config.scrollContainer=document.querySelector(a.scrollContainer)),this.animationNameCache=new c,this.wowEvent=this.util().createEvent(this.config.boxClass)}return e.prototype.defaults={boxClass:"wow",animateClass:"animated",offset:0,mobile:!0,live:!0,callback:null,scrollContainer:null},e.prototype.init=function(){var a;return this.element=window.document.documentElement,"interactive"===(a=document.readyState)||"complete"===a?this.start():this.util().addEvent(document,"DOMContentLoaded",this.start),this.finished=[]},e.prototype.start=function(){var b,c,d,e;if(this.stopped=!1,this.boxes=function(){var a,c,d,e;for(d=this.element.querySelectorAll("."+this.config.boxClass),e=[],a=0,c=d.length;c>a;a++)b=d[a],e.push(b);return e}.call(this),this.all=function(){var a,c,d,e;for(d=this.boxes,e=[],a=0,c=d.length;c>a;a++)b=d[a],e.push(b);return e}.call(this),this.boxes.length)if(this.disabled())this.resetStyle();else for(e=this.boxes,c=0,d=e.length;d>c;c++)b=e[c],this.applyStyle(b,!0);return this.disabled()||(this.util().addEvent(this.config.scrollContainer||window,"scroll",this.scrollHandler),this.util().addEvent(window,"resize",this.scrollHandler),this.interval=setInterval(this.scrollCallback,50)),this.config.live?new a(function(a){return function(b){var c,d,e,f,g;for(g=[],c=0,d=b.length;d>c;c++)f=b[c],g.push(function(){var a,b,c,d;for(c=f.addedNodes||[],d=[],a=0,b=c.length;b>a;a++)e=c[a],d.push(this.doSync(e));return d}.call(a));return g}}(this)).observe(document.body,{childList:!0,subtree:!0}):void 0},e.prototype.stop=function(){return this.stopped=!0,this.util().removeEvent(this.config.scrollContainer||window,"scroll",this.scrollHandler),this.util().removeEvent(window,"resize",this.scrollHandler),null!=this.interval?clearInterval(this.interval):void 0},e.prototype.sync=function(b){return a.notSupported?this.doSync(this.element):void 0},e.prototype.doSync=function(a){var b,c,d,e,f;if(null==a&&(a=this.element),1===a.nodeType){for(a=a.parentNode||a,e=a.querySelectorAll("."+this.config.boxClass),f=[],c=0,d=e.length;d>c;c++)b=e[c],g.call(this.all,b)<0?(this.boxes.push(b),this.all.push(b),this.stopped||this.disabled()?this.resetStyle():this.applyStyle(b,!0),f.push(this.scrolled=!0)):f.push(void 0);return f}},e.prototype.show=function(a){return this.applyStyle(a),a.className=a.className+" "+this.config.animateClass,null!=this.config.callback&&this.config.callback(a),this.util().emitEvent(a,this.wowEvent),this.util().addEvent(a,"animationend",this.resetAnimation),this.util().addEvent(a,"oanimationend",this.resetAnimation),this.util().addEvent(a,"webkitAnimationEnd",this.resetAnimation),this.util().addEvent(a,"MSAnimationEnd",this.resetAnimation),a},e.prototype.applyStyle=function(a,b){var c,d,e;return d=a.getAttribute("data-wow-duration"),c=a.getAttribute("data-wow-delay"),e=a.getAttribute("data-wow-iteration"),this.animate(function(f){return function(){return f.customStyle(a,b,d,c,e)}}(this))},e.prototype.animate=function(){return"requestAnimationFrame"in window?function(a){return window.requestAnimationFrame(a)}:function(a){return a()}}(),e.prototype.resetStyle=function(){var a,b,c,d,e;for(d=this.boxes,e=[],b=0,c=d.length;c>b;b++)a=d[b],e.push(a.style.visibility="visible");return e},e.prototype.resetAnimation=function(a){var b;return a.type.toLowerCase().indexOf("animationend")>=0?(b=a.target||a.srcElement,b.className=b.className.replace(this.config.animateClass,"").trim()):void 0},e.prototype.customStyle=function(a,b,c,d,e){return b&&this.cacheAnimationName(a),a.style.visibility=b?"hidden":"visible",c&&this.vendorSet(a.style,{animationDuration:c}),d&&this.vendorSet(a.style,{animationDelay:d}),e&&this.vendorSet(a.style,{animationIterationCount:e}),this.vendorSet(a.style,{animationName:b?"none":this.cachedAnimationName(a)}),a},e.prototype.vendors=["moz","webkit"],e.prototype.vendorSet=function(a,b){var c,d,e,f;d=[];for(c in b)e=b[c],a[""+c]=e,d.push(function(){var b,d,g,h;for(g=this.vendors,h=[],b=0,d=g.length;d>b;b++)f=g[b],h.push(a[""+f+c.charAt(0).toUpperCase()+c.substr(1)]=e);return h}.call(this));return d},e.prototype.vendorCSS=function(a,b){var c,e,f,g,h,i;for(h=d(a),g=h.getPropertyCSSValue(b),f=this.vendors,c=0,e=f.length;e>c;c++)i=f[c],g=g||h.getPropertyCSSValue("-"+i+"-"+b);return g},e.prototype.animationName=function(a){var b;try{b=this.vendorCSS(a,"animation-name").cssText}catch(c){b=d(a).getPropertyValue("animation-name")}return"none"===b?"":b},e.prototype.cacheAnimationName=function(a){return this.animationNameCache.set(a,this.animationName(a))},e.prototype.cachedAnimationName=function(a){return this.animationNameCache.get(a)},e.prototype.scrollHandler=function(){return this.scrolled=!0},e.prototype.scrollCallback=function(){var a;return!this.scrolled||(this.scrolled=!1,this.boxes=function(){var b,c,d,e;for(d=this.boxes,e=[],b=0,c=d.length;c>b;b++)a=d[b],a&&(this.isVisible(a)?this.show(a):e.push(a));return e}.call(this),this.boxes.length||this.config.live)?void 0:this.stop()},e.prototype.offsetTop=function(a){for(var b;void 0===a.offsetTop;)a=a.parentNode;for(b=a.offsetTop;a=a.offsetParent;)b+=a.offsetTop;return b},e.prototype.isVisible=function(a){var b,c,d,e,f;return c=a.getAttribute("data-wow-offset")||this.config.offset,f=this.config.scrollContainer&&this.config.scrollContainer.scrollTop||window.pageYOffset,e=f+Math.min(this.element.clientHeight,this.util().innerHeight())-c,d=this.offsetTop(a),b=d+a.clientHeight,e>=d&&b>=f},e.prototype.util=function(){return null!=this._util?this._util:this._util=new b},e.prototype.disabled=function(){return!this.config.mobile&&this.util().isMobile(navigator.userAgent)},e}()}).call(this);




/*! npm.im/object-fit-images */
var objectFitImages=function(){"use strict";function t(t){for(var e,r=getComputedStyle(t).fontFamily,i={};null!==(e=n.exec(r));)i[e[1]]=e[2];return i}function e(e,i){if(!e[c].parsingSrcset){var s=t(e);if(s["object-fit"]=s["object-fit"]||"fill",!e[c].s){if("fill"===s["object-fit"])return;if(!e[c].skipTest&&l&&!s["object-position"])return}var n=e[c].ios7src||e.currentSrc||e.src;if(i)n=i;else if(e.srcset&&!a&&window.picturefill){var o=window.picturefill._.ns;e[c].parsingSrcset=!0,e[o]&&e[o].evaled||window.picturefill._.fillImg(e,{reselect:!0}),e[o].curSrc||(e[o].supported=!1,window.picturefill._.fillImg(e,{reselect:!0})),delete e[c].parsingSrcset,n=e[o].curSrc||n}if(e[c].s)e[c].s=n,i&&(e[c].srcAttr=i);else{e[c]={s:n,srcAttr:i||f.call(e,"src"),srcsetAttr:e.srcset},e.src=c;try{e.srcset&&(e.srcset="",Object.defineProperty(e,"srcset",{value:e[c].srcsetAttr})),r(e)}catch(t){e[c].ios7src=n}}e.style.backgroundImage='url("'+n+'")',e.style.backgroundPosition=s["object-position"]||"center",e.style.backgroundRepeat="no-repeat",/scale-down/.test(s["object-fit"])?(e[c].i||(e[c].i=new Image,e[c].i.src=n),function t(){return e[c].i.naturalWidth?void(e[c].i.naturalWidth>e.width||e[c].i.naturalHeight>e.height?e.style.backgroundSize="contain":e.style.backgroundSize="auto"):void setTimeout(t,100)}()):e.style.backgroundSize=s["object-fit"].replace("none","auto").replace("fill","100% 100%")}}function r(t){var r={get:function(){return t[c].s},set:function(r){return delete t[c].i,e(t,r),r}};Object.defineProperty(t,"src",r),Object.defineProperty(t,"currentSrc",{get:r.get})}function i(){u||(HTMLImageElement.prototype.getAttribute=function(t){return!this[c]||"src"!==t&&"srcset"!==t?f.call(this,t):this[c][t+"Attr"]},HTMLImageElement.prototype.setAttribute=function(t,e){!this[c]||"src"!==t&&"srcset"!==t?g.call(this,t,e):this["src"===t?"src":t+"Attr"]=String(e)})}function s(t,r){var i=!A&&!t;if(r=r||{},t=t||"img",u&&!r.skipTest)return!1;"string"==typeof t?t=document.querySelectorAll("img"):t.length||(t=[t]);for(var n=0;n<t.length;n++)t[n][c]=t[n][c]||r,e(t[n]);i&&(document.body.addEventListener("load",function(t){"IMG"===t.target.tagName&&s(t.target,{skipTest:r.skipTest})},!0),A=!0,t="img"),r.watchMQ&&window.addEventListener("resize",s.bind(null,t,{skipTest:r.skipTest}))}var c="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==",n=/(object-fit|object-position)\s*:\s*([-\w\s%]+)/g,o=new Image,l="object-fit"in o.style,u="object-position"in o.style,a="string"==typeof o.currentSrc,f=o.getAttribute,g=o.setAttribute,A=!1;return s.supportsObjectFit=l,s.supportsObjectPosition=u,i(),s}();



/*!
 * jQuery Scrollify
 * Version 1.0.5
 *
 * Requires:
 * - jQuery 1.7 or higher
 *
 * https://github.com/lukehaas/Scrollify
 *
 * Copyright 2016, Luke Haas
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

!function(a,b){"use strict";"function"==typeof define&&define.amd?define(["jquery"],function(c){return b(c,a,a.document)}):"object"==typeof module&&module.exports?module.exports=function(c,d){return void 0===d&&(d="undefined"!=typeof window?require("jquery"):require("jquery")(c)),b(d,a,a.document),d}:b(jQuery,a,a.document)}("undefined"!=typeof window?window:this,function(a,b,c,d){"use strict";function D(c,d,h){if(j===c&&(h=!1),w===!0)return!0;if(f[c]){if(q=!1,h&&C.before(c,g),k=1,C.sectionName&&(z!==!0||0!==c))if(history.pushState)try{history.replaceState(null,null,f[c])}catch(a){b.console&&console.warn("Scrollify warning: This needs to be hosted on a server to manipulate the hash value.")}else b.location.hash=f[c];if(d)a(C.target).stop().scrollTop(e[c]),h&&C.after(c,g);else{if(r=!0,a().velocity?a(C.target).stop().velocity("scroll",{duration:C.scrollSpeed,easing:C.easing,offset:e[c],mobileHA:!1}):a(C.target).stop().animate({scrollTop:e[c]},C.scrollSpeed,C.easing),b.location.hash.length&&C.sectionName&&b.console)try{a(b.location.hash).length&&console.warn("Scrollify warning: There are IDs on the page that match the hash value - this will cause the page to anchor.")}catch(a){console.warn("Scrollify warning:",b.location.hash,"is not a valid jQuery expression.")}a(C.target).promise().done(function(){j=c,r=!1,z=!1,h&&C.after(c,g)})}}}function E(a){function b(b){for(var c=0,d=a.slice(Math.max(a.length-b,1)),e=0;e<d.length;e++)c+=d[e];return Math.ceil(c/b)}var c=b(10),d=b(70);return c>=d}function F(a,b){for(var c=f.length;c>=0;c--)"string"==typeof a?f[c]===a&&(i=c,D(c,b,!0)):c===a&&(i=c,D(c,b,!0))}var m,n,t,u,v,e=[],f=[],g=[],h=[],i=0,j=0,k=1,l=!1,o=a(b),p=o.scrollTop(),q=!1,r=!1,s=!1,w=!1,x=[],y=(new Date).getTime(),z=!0,A=!1,B="onwheel"in c?"wheel":c.onmousewheel!==d?"mousewheel":"DOMMouseScroll",C={section:".section",sectionName:"section-name",interstitialSection:"",easing:"easeOutExpo",scrollSpeed:1100,offset:0,scrollbars:!0,target:"html,body",standardScrollElements:!1,setHeights:!0,overflowScroll:!0,before:function(){},after:function(){},afterResize:function(){},afterRender:function(){}};a.scrollify=function(d){function j(b){a().velocity?a(C.target).stop().velocity("scroll",{duration:C.scrollSpeed,easing:C.easing,offset:b,mobileHA:!1}):a(C.target).stop().animate({scrollTop:b},C.scrollSpeed,C.easing)}function z(){var b=C.section;h=[],C.interstitialSection.length&&(b+=","+C.interstitialSection),a(b).each(function(b){var c=a(this);C.setHeights?c.is(C.interstitialSection)?h[b]=!1:c.css("height","auto").outerHeight()<o.height()||"hidden"===c.css("overflow")?(c.css({height:o.height()}),h[b]=!1):(c.css({height:c.height()}),C.overflowScroll?h[b]=!0:h[b]=!1):c.outerHeight()<o.height()||C.overflowScroll===!1?h[b]=!1:h[b]=!0})}function F(c){var d=C.section;C.interstitialSection.length&&(d+=","+C.interstitialSection),e=[],f=[],g=[],a(d).each(function(c){var h=a(this);c>0?e[c]=parseInt(h.offset().top)+C.offset:e[c]=parseInt(h.offset().top),C.sectionName&&h.data(C.sectionName)?f[c]="#"+h.data(C.sectionName).replace(/ /g,"-"):h.is(C.interstitialSection)===!1?f[c]="#"+(c+1):(f[c]="#",c===a(d).length-1&&c>1&&(e[c]=e[c-1]+parseInt(h.height()))),g[c]=h;try{a(f[c]).length&&b.console&&console.warn("Scrollify warning: Section names can't match IDs on the page - this will cause the browser to anchor.")}catch(a){}b.location.hash===f[c]&&(i=c,l=!0)}),!0===c?D(i,!1,!1):C.afterRender()}function G(){return!h[i]||(p=o.scrollTop(),!(p>parseInt(e[i])))}function H(){return!h[i]||(p=o.scrollTop(),!(p<parseInt(e[i])+(g[i].outerHeight()-o.height())-28))}A=!0,a.easing.easeOutExpo=function(a,b,c,d,e){return b==e?c+d:d*(-Math.pow(2,-10*b/e)+1)+c},t={handleMousedown:function(){return w===!0||(q=!1,void(s=!1))},handleMouseup:function(){return w===!0||(q=!0,void(s&&t.calculateNearest(!1,!0)))},handleScroll:function(){return w===!0||(m&&clearTimeout(m),void(m=setTimeout(function(){return s=!0,q!==!1&&(q=!1,void t.calculateNearest(!1,!0))},200)))},calculateNearest:function(a,b){p=o.scrollTop();for(var h,c=1,d=e.length,f=0,g=Math.abs(e[0]-p);c<d;c++)h=Math.abs(e[c]-p),h<g&&(g=h,f=c);(H()||G())&&(i=f,D(f,a,b))},wheelHandler:function(c){if(w===!0)return!0;if(C.standardScrollElements&&(a(c.target).is(C.standardScrollElements)||a(c.target).closest(C.standardScrollElements).length))return!0;h[i]||c.preventDefault();var d=(new Date).getTime();c=c||b.event;var f=c.originalEvent.wheelDelta||-c.originalEvent.deltaY||-c.originalEvent.detail,g=Math.max(-1,Math.min(1,f));if(x.length>149&&x.shift(),x.push(Math.abs(f)),d-y>200&&(x=[]),y=d,r)return!1;if(g<0){if(i<e.length-1&&H()){if(!E(x))return!1;c.preventDefault(),i++,r=!0,D(i,!1,!0)}}else if(g>0&&i>0&&G()){if(!E(x))return!1;c.preventDefault(),i--,r=!0,D(i,!1,!0)}},keyHandler:function(a){return w===!0||r!==!0&&void(38==a.keyCode?i>0&&G()&&(a.preventDefault(),i--,D(i,!1,!0)):40==a.keyCode&&i<e.length-1&&H()&&(a.preventDefault(),i++,D(i,!1,!0)))},init:function(){C.scrollbars?(o.on("mousedown",t.handleMousedown),o.on("mouseup",t.handleMouseup),o.on("scroll",t.handleScroll)):a("body").css({overflow:"hidden"}),o.on(B,t.wheelHandler),o.on("keydown",t.keyHandler)}},u={touches:{touchstart:{y:-1,x:-1},touchmove:{y:-1,x:-1},touchend:!1,direction:"undetermined"},options:{distance:30,timeGap:800,timeStamp:(new Date).getTime()},touchHandler:function(b){if(w===!0)return!0;if(C.standardScrollElements&&(a(b.target).is(C.standardScrollElements)||a(b.target).closest(C.standardScrollElements).length))return!0;var c;if("undefined"!=typeof b&&"undefined"!=typeof b.touches)switch(c=b.touches[0],b.type){case"touchstart":u.touches.touchstart.y=c.pageY,u.touches.touchmove.y=-1,u.touches.touchstart.x=c.pageX,u.touches.touchmove.x=-1,u.options.timeStamp=(new Date).getTime(),u.touches.touchend=!1;case"touchmove":u.touches.touchmove.y=c.pageY,u.touches.touchmove.x=c.pageX,u.touches.touchstart.y!==u.touches.touchmove.y&&Math.abs(u.touches.touchstart.y-u.touches.touchmove.y)>Math.abs(u.touches.touchstart.x-u.touches.touchmove.x)&&(b.preventDefault(),u.touches.direction="y",u.options.timeStamp+u.options.timeGap<(new Date).getTime()&&0==u.touches.touchend&&(u.touches.touchend=!0,u.touches.touchstart.y>-1&&Math.abs(u.touches.touchmove.y-u.touches.touchstart.y)>u.options.distance&&(u.touches.touchstart.y<u.touches.touchmove.y?u.up():u.down())));break;case"touchend":u.touches[b.type]===!1&&(u.touches[b.type]=!0,u.touches.touchstart.y>-1&&u.touches.touchmove.y>-1&&"y"===u.touches.direction&&(Math.abs(u.touches.touchmove.y-u.touches.touchstart.y)>u.options.distance&&(u.touches.touchstart.y<u.touches.touchmove.y?u.up():u.down()),u.touches.touchstart.y=-1,u.touches.touchstart.x=-1,u.touches.direction="undetermined"))}},down:function(){i<=e.length-1&&(H()&&i<e.length-1?(i++,D(i,!1,!0)):Math.floor(g[i].height()/o.height())>k?(j(parseInt(e[i])+o.height()*k),k+=1):j(parseInt(e[i])+(g[i].height()-o.height())))},up:function(){i>=0&&(G()&&i>0?(i--,D(i,!1,!0)):k>2?(k-=1,j(parseInt(e[i])+o.height()*k)):(k=1,j(parseInt(e[i]))))},init:function(){c.addEventListener&&(c.addEventListener("touchstart",u.touchHandler,!1),c.addEventListener("touchmove",u.touchHandler,!1),c.addEventListener("touchend",u.touchHandler,!1))}},v={refresh:function(a){clearTimeout(n),n=setTimeout(function(){z(),F(!0),a&&C.afterResize()},400)},handleUpdate:function(){v.refresh(!1)},handleResize:function(){v.refresh(!0)}},C=a.extend(C,d),z(),F(!1),!0===l?D(i,!1,!0):setTimeout(function(){t.calculateNearest(!0,!1)},200),e.length&&(t.init(),u.init(),o.on("resize",v.handleResize),c.addEventListener&&b.addEventListener("orientationchange",v.handleResize,!1))},a.scrollify.move=function(b){return b!==d&&(b.originalEvent&&(b=a(this).attr("href")),void F(b,!1))},a.scrollify.instantMove=function(a){return a!==d&&void F(a,!0)},a.scrollify.next=function(){i<f.length&&(i+=1,D(i,!1,!0))},a.scrollify.previous=function(){i>0&&(i-=1,D(i,!1,!0))},a.scrollify.instantNext=function(){i<f.length&&(i+=1,D(i,!0,!0))},a.scrollify.instantPrevious=function(){i>0&&(i-=1,D(i,!0,!0))},a.scrollify.destroy=function(){return!!A&&(C.setHeights&&a(C.section).each(function(){a(this).css("height","auto")}),o.off("resize",v.handleResize),C.scrollbars&&(o.off("mousedown",t.handleMousedown),o.off("mouseup",t.handleMouseup),o.off("scroll",t.handleScroll)),o.off(B,t.wheelHandler),o.off("keydown",t.keyHandler),c.addEventListener&&(c.removeEventListener("touchstart",u.touchHandler,!1),c.removeEventListener("touchmove",u.touchHandler,!1),c.removeEventListener("touchend",u.touchHandler,!1)),e=[],f=[],g=[],void(h=[]))},a.scrollify.update=function(){return!!A&&void v.handleUpdate()},a.scrollify.current=function(){return g[i]},a.scrollify.disable=function(){w=!0},a.scrollify.enable=function(){w=!1,A&&t.calculateNearest(!1,!1)},a.scrollify.isDisabled=function(){return w},a.scrollify.setOptions=function(c){return!!A&&void("object"==typeof c?(C=a.extend(C,c),v.handleUpdate()):b.console&&console.warn("Scrollify warning: Options need to be in an object."))}});



// Custom Timer Plugin From http://stackoverflow.com/questions/2540277/jquery-counter-to-count-up-to-a-target-number

(function($) {
    $.fn.countTo = function(options) {
        // merge the default plugin settings with the custom options
        options = $.extend({}, $.fn.countTo.defaults, options || {});

        // how many times to update the value, and how much to increment the value on each update
        var loops = Math.ceil(options.speed / options.refreshInterval),
            increment = (options.to - options.from) / loops;

        return $(this).each(function() {
            var _this = this,
                loopCount = 0,
                value = options.from,
                interval = setInterval(updateTimer, options.refreshInterval);

            function updateTimer() {
                value += increment;
                loopCount++;
                $(_this).html(value.toFixed(options.decimals));

                if (typeof(options.onUpdate) == 'function') {
                    options.onUpdate.call(_this, value);
                }

                if (loopCount >= loops) {
                    clearInterval(interval);
                    value = options.to;

                    if (typeof(options.onComplete) == 'function') {
                        options.onComplete.call(_this, value);
                    }
                }
            }
        });
    };

    $.fn.countTo.defaults = {
        from: 0,  // the number the element should start at
        to: 100,  // the number the element should end at
        speed: 1000,  // how long it should take to count between the target numbers
        refreshInterval: 100,  // how often the element should be updated
        decimals: 0,  // the number of decimal places to show
        onUpdate: null,  // callback method for every time the element is updated,
        onComplete: null,  // callback method for when the element finishes updating
    };
})(jQuery);
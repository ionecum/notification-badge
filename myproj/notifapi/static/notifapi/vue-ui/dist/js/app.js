(function(){"use strict";var i={9153:function(i,t,o){o(560);var n=o(9199);const e={id:"app"},a={id:"wrapper"};function s(i,t,o,s,c,r){const l=(0,n.up)("NotificationBell");return(0,n.wg)(),(0,n.iD)("div",e,[(0,n._)("div",a,[(0,n.Wm)(l,{notificationType:o.notificationType},null,8,["notificationType"])])])}const c={class:"fancy-container"},r={href:"#",class:"position-relative"},l=(0,n._)("i",{class:"fa fa-bell _gray",style:{"font-size":"24px"}},null,-1),f={class:"my-text btnLnk"};function d(i,t,o,e,a,s){const d=(0,n.up)("notifications-list");return(0,n.wg)(),(0,n.iD)("div",c,[(0,n._)("div",{class:"notification-container",onClick:t[0]||(t[0]=(...i)=>s.toggleNotificationMenu&&s.toggleNotificationMenu(...i))},[(0,n._)("a",r,[l,(0,n._)("span",f,(0,n.zw)(s.bellText),1),(0,n._)("span",{class:(0,n.C_)(["position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger _reduced",{hidden:!a.notificationCount}])},(0,n.zw)(a.notificationCount),3)]),(0,n.wy)((0,n.Wm)(d,{notifications:a.notifications,onMarkAsRead:s.handleMarkAsRead,onMarkAllRead:s.handleMarkAllRead},null,8,["notifications","onMarkAsRead","onMarkAllRead"]),[[n.F8,a.showNotifications]])])])}const u={class:"notifications-list"},p=["onClick"],h={key:1,class:"see-more-link"};function y(i,t,o,e,a,s){return(0,n.wg)(),(0,n.iD)("div",{class:"notifications-wrapper",onClick:t[2]||(t[2]=(0,n.iM)((()=>{}),["stop"]))},[(0,n._)("div",u,[s.areAnyUnread?((0,n.wg)(),(0,n.iD)("a",{key:0,href:"#",onClick:t[0]||(t[0]=(...i)=>s.markAllRead&&s.markAllRead(...i))},"Mark All as Read")):(0,n.kq)("",!0),(0,n._)("ul",null,[((0,n.wg)(!0),(0,n.iD)(n.HY,null,(0,n.Ko)(o.notifications.slice(0,10),((i,t)=>((0,n.wg)(),(0,n.iD)("li",{key:t},[(0,n._)("div",{class:(0,n.C_)(["notification",{bold:!i.is_read}]),onClick:t=>s.markAsRead(i)},(0,n.zw)(i.message),11,p)])))),128))]),o.notifications.length>10?((0,n.wg)(),(0,n.iD)("div",h,[(0,n._)("a",{href:"#",onClick:t[1]||(t[1]=(...i)=>s.showAllNotifications&&s.showAllNotifications(...i))},"See More")])):(0,n.kq)("",!0)])])}var k={props:{notifications:{type:Array,required:!0}},data(){return{visibleNotifications:[],showMoreLink:!1}},computed:{areAnyUnread(){return this.notifications.some((i=>!i.is_read))}},methods:{showAllNotifications(){},markAllRead(){this.areAnyUnread?(console.log("There are unread notifications."),this.$emit("mark-all-read")):console.log("All the notifications are already read.")},markAsRead(i){i.is_read||(console.log("The notification type is "+i),this.$emit("mark-as-read",i.id))}}},g=o(89);const m=(0,g.Z)(k,[["render",y]]);var b=m,w={components:{NotificationsList:b},props:["notificationType"],data(){return{notificationCount:0,notifications:[],webSocket:null,showNotifications:!1}},computed:{bellText(){const i={VISIT:"Visits",TEASE:"Teases",MESSAGE:"Messages",general:"All Notifications"};return i[this.notificationType]||""}},mounted(){console.log("Notification type in NotificationBell:"+this.notificationType),document.addEventListener("click",this.handleClickOutside),this.establishWebSocketConnection()},beforeUnmount(){document.removeEventListener("click",this.handleClickOutside)},methods:{handleClickOutside(i){this.$el.contains(i.target)||(this.showNotifications=!1)},async establishWebSocketConnection(){this.webSocket=new WebSocket("ws://127.0.0.1:8000/websocket/ws/notifications/"),this.webSocket.onopen=()=>{console.log("WebSocket connection established!"),this.updateNotificationCount()},this.webSocket.onmessage=i=>{const t=JSON.parse(i.data);console.log(t),"notification.update"===t.type&&"general"===this.notificationType||t.type==="notification.update."+this.notificationType?(this.notificationCount=t.count,this.notifications=t.notifications.map((i=>({id:i.id,is_read:i.is_read,message:i.message})))):"general"===this.notificationType?this.updateNotificationCount():console.log("Different type of Notification!")},this.webSocket.onclose=()=>{console.log("WebSocket connection closed.")}},toggleNotificationMenu(){this.showNotifications=!this.showNotifications,this.showNotifications&&this.notificationCount>0&&this.webSocket.send(JSON.stringify({type:"mark.all.seen",notificationType:this.notificationType}))},handleMarkAsRead(i){this.webSocket.send(JSON.stringify({type:"mark.one.read",id:i,notificationType:this.notificationType}))},handleMarkAllRead(){this.webSocket.send(JSON.stringify({type:"mark.all.read",notificationType:this.notificationType}))},updateNotificationCount(){this.webSocket.send(JSON.stringify({type:"update.notification.count",notificationType:this.notificationType}))}}};const v=(0,g.Z)(w,[["render",d]]);var T=v,S={props:["notificationType"],mounted(){console.log("Received notificationType in App.js:",this.notificationType)},components:{NotificationBell:T}};const N=(0,g.Z)(S,[["render",s]]);var A=N;let _=[];const C=document.querySelectorAll(".bell");C.forEach((i=>{const t=i.dataset.notificationType;_.push(t),(0,n.ri)({render:()=>(0,n.h)(A,{notificationType:t})}).mount(`#${i.id}`)}))}},t={};function o(n){var e=t[n];if(void 0!==e)return e.exports;var a=t[n]={exports:{}};return i[n].call(a.exports,a,a.exports,o),a.exports}o.m=i,function(){var i=[];o.O=function(t,n,e,a){if(!n){var s=1/0;for(f=0;f<i.length;f++){n=i[f][0],e=i[f][1],a=i[f][2];for(var c=!0,r=0;r<n.length;r++)(!1&a||s>=a)&&Object.keys(o.O).every((function(i){return o.O[i](n[r])}))?n.splice(r--,1):(c=!1,a<s&&(s=a));if(c){i.splice(f--,1);var l=e();void 0!==l&&(t=l)}}return t}a=a||0;for(var f=i.length;f>0&&i[f-1][2]>a;f--)i[f]=i[f-1];i[f]=[n,e,a]}}(),function(){o.d=function(i,t){for(var n in t)o.o(t,n)&&!o.o(i,n)&&Object.defineProperty(i,n,{enumerable:!0,get:t[n]})}}(),function(){o.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(i){if("object"===typeof window)return window}}()}(),function(){o.o=function(i,t){return Object.prototype.hasOwnProperty.call(i,t)}}(),function(){o.r=function(i){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(i,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(i,"__esModule",{value:!0})}}(),function(){var i={143:0};o.O.j=function(t){return 0===i[t]};var t=function(t,n){var e,a,s=n[0],c=n[1],r=n[2],l=0;if(s.some((function(t){return 0!==i[t]}))){for(e in c)o.o(c,e)&&(o.m[e]=c[e]);if(r)var f=r(o)}for(t&&t(n);l<s.length;l++)a=s[l],o.o(i,a)&&i[a]&&i[a][0](),i[a]=0;return o.O(f)},n=self["webpackChunkvue_autocomplete_component_example"]=self["webpackChunkvue_autocomplete_component_example"]||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))}();var n=o.O(void 0,[998],(function(){return o(9153)}));n=o.O(n)})();
//# sourceMappingURL=app.js.map
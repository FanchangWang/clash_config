import{r as c,R as l,k as a}from"./index-e001f514.js";function s(){return s=Object.assign||function(r){for(var o=1;o<arguments.length;o++){var t=arguments[o];for(var e in t)Object.prototype.hasOwnProperty.call(t,e)&&(r[e]=t[e])}return r},s.apply(this,arguments)}function v(r,o){if(r==null)return{};var t=u(r,o),e,n;if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(r);for(n=0;n<i.length;n++)e=i[n],!(o.indexOf(e)>=0)&&Object.prototype.propertyIsEnumerable.call(r,e)&&(t[e]=r[e])}return t}function u(r,o){if(r==null)return{};var t={},e=Object.keys(r),n,i;for(i=0;i<e.length;i++)n=e[i],!(o.indexOf(n)>=0)&&(t[n]=r[n]);return t}var p=c.forwardRef(function(r,o){var t=r.color,e=t===void 0?"currentColor":t,n=r.size,i=n===void 0?24:n,f=v(r,["color","size"]);return l.createElement("svg",s({ref:o,xmlns:"http://www.w3.org/2000/svg",width:i,height:i,viewBox:"0 0 24 24",fill:"none",stroke:e,strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round"},f),l.createElement("polyline",{points:"6 9 12 15 18 9"}))});p.propTypes={color:a.string,size:a.oneOfType([a.string,a.number])};p.displayName="ChevronDown";const h=p;export{h as C};

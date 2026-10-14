# pages.py — MX-UI v2.0.0 front-end (no build step, no CDN scripts)
#
# Design notes
#   Subject : a self-hosted VLESS tunnel panel run by one operator; shared with end users.
#   Lineage : a telephone exchange patch bay. Every config is a "line" with a status lamp
#             and a segmented VU meter; the header carries a live oscilloscope trace.
#   Type    : Red Hat Display (UI + statement numerals) / JetBrains Mono (data) / Vazirmatn (fa names)
#   Color   : signal teal #00b7a7 leads; amber #ffcd12 = attention lamp; carmine #a40000 = cut;
#             ink-navy #16317d = upload trace. Neutrals are tinted toward the teal.
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Vazirmatn:wght@400;600;700&display=swap" rel="stylesheet">')

BASE_CSS = r"""
:root{
  --bg:#f2f7f6;--card:#fcfefd;--sunk:#e6eeec;--ink:#132221;--mut:#556a67;--line:#d2dfdc;--line2:#bfd0cc;
  --sig:#00b7a7;--acc:#067c72;--acc-ink:#fff;--acc-soft:rgba(0,183,167,.13);
  --amb:#ffcd12;--amb-ink:#7a5c00;--amb-soft:rgba(255,205,18,.22);
  --red:#a40000;--red-soft:rgba(164,0,0,.09);--navy:#16317d;--plum:#b86092;
  --seg-off:#d9e4e1;--shadow:0 1px 0 rgba(19,34,33,.04),0 8px 28px -12px rgba(19,34,33,.18);
  --r:14px;--ui:'Red Hat Display','Vazirmatn',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
  --mono:'JetBrains Mono','Vazirmatn',ui-monospace,Menlo,Consolas,monospace;color-scheme:light}
:root[data-theme=dark]{
  --bg:#0d1615;--card:#13201f;--sunk:#0a1211;--ink:#e2ecea;--mut:#90a5a2;--line:#22322f;--line2:#2e4440;
  --sig:#19c9b7;--acc:#22c7b6;--acc-ink:#04201d;--acc-soft:rgba(25,201,183,.14);
  --amb:#ffcd12;--amb-ink:#ffd84a;--amb-soft:rgba(255,205,18,.13);
  --red:#ff6f61;--red-soft:rgba(255,111,97,.13);--navy:#86a2ff;--plum:#e08fbd;
  --seg-off:#1d2d2b;--shadow:0 1px 0 rgba(0,0,0,.2),0 12px 32px -14px rgba(0,0,0,.6);color-scheme:dark}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:var(--ui);background:var(--bg);color:var(--ink);font-size:16px;line-height:1.5;min-height:100dvh;-webkit-font-smoothing:antialiased;font-feature-settings:"tnum" 1}
body.lock{overflow:hidden}
a{color:inherit}
button,input,select,textarea{font:inherit;color:inherit}
button{cursor:pointer;background:none;border:0}
:focus-visible{outline:2px solid var(--sig);outline-offset:2px;border-radius:6px}
.mono{font-family:var(--mono);font-feature-settings:"zero" 1}
.mut{color:var(--mut)}.hidden{display:none!important}
svg.i{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
/* lamp: the signature status light */
.lamp{--c:var(--seg-off);width:10px;height:10px;border-radius:50%;background:var(--c);flex:none;position:relative;box-shadow:inset 0 -1px 2px rgba(0,0,0,.25)}
.lamp.on{--c:var(--sig)}
.lamp.live{--c:var(--sig);animation:glow 2.4s ease-in-out infinite}
.lamp.warn{--c:var(--amb)}
.lamp.cut{--c:var(--red)}
.lamp.off{background:transparent;box-shadow:inset 0 0 0 2px var(--line2)}
@keyframes glow{0%,100%{box-shadow:0 0 0 0 rgba(0,183,167,.0),0 0 6px 1px rgba(0,183,167,.55)}50%{box-shadow:0 0 0 5px rgba(0,183,167,.12),0 0 14px 3px rgba(0,183,167,.35)}}
/* segmented VU meter */
.vu{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;gap:3px;height:12px}
.vu i{border-radius:2px;background:var(--seg-off);transition:background .4s}
.vu i.f{background:var(--sig)}.vu i.f.a{background:var(--amb)}.vu i.f.r{background:var(--red)}
.vu.inf i{background:repeating-linear-gradient(90deg,var(--seg-off) 0 2px,transparent 2px 4px)}
/* controls */
.field{display:grid;gap:6px;min-width:0}
.field>span{font-size:14px;font-weight:700}
.field>small{font-size:14px;color:var(--mut)}
.input{width:100%;height:46px;padding:0 14px;background:var(--card);border:1.5px solid var(--line);border-radius:11px;font-size:16px;transition:border-color .15s,box-shadow .15s}
.input::placeholder{color:var(--mut);opacity:.7}
.input:focus{outline:none;border-color:var(--sig);box-shadow:0 0 0 4px var(--acc-soft)}
select.input{appearance:none;background-image:linear-gradient(45deg,transparent 50%,var(--mut) 50%),linear-gradient(135deg,var(--mut) 50%,transparent 50%);background-position:calc(100% - 18px) 50%,calc(100% - 13px) 50%;background-size:5px 5px;background-repeat:no-repeat;padding-right:34px}
.join{display:flex}.join .input:first-child{border-radius:11px 0 0 11px;border-right:0}.join .input:last-child{border-radius:0 11px 11px 0;width:auto;min-width:96px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 18px;border-radius:11px;border:1.5px solid var(--line);background:var(--card);font-weight:700;font-size:15px;white-space:nowrap;transition:background .15s,border-color .15s,transform .08s,filter .15s}
.btn:hover{border-color:var(--line2);background:var(--sunk)}.btn:active{transform:translateY(1px)}.btn:disabled{opacity:.5;cursor:not-allowed}
.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--acc-ink)}.btn.pri:hover{filter:brightness(1.08)}
.btn.bad{background:var(--red);border-color:var(--red);color:#fff}
.btn.ghost{border-color:transparent;background:transparent}.btn.ghost:hover{background:var(--sunk)}
.btn.sm{height:36px;padding:0 13px;font-size:14px;border-radius:9px}.btn.block{width:100%}
.ib{width:40px;height:40px;display:inline-grid;place-items:center;border-radius:10px;color:var(--mut);transition:background .15s,color .15s}
.ib:hover{background:var(--sunk);color:var(--ink)}.ib.sm{width:36px;height:36px}.ib.bad:hover{color:var(--red);background:var(--red-soft)}
.chip{display:inline-flex;align-items:center;gap:7px;height:30px;padding:0 12px;border-radius:99px;font-size:14px;font-weight:700;background:var(--sunk);color:var(--mut);white-space:nowrap}
.tag{display:inline-flex;align-items:center;height:22px;padding:0 8px;border-radius:6px;font:600 12.5px/1 var(--mono);background:var(--sunk);color:var(--mut);white-space:nowrap}
.tag.acc{background:var(--acc-soft);color:var(--acc)}.tag.amb{background:var(--amb-soft);color:var(--amb-ink)}.tag.red{background:var(--red-soft);color:var(--red)}
.alert{padding:11px 14px;border-radius:11px;background:var(--red-soft);color:var(--red);font-size:14px;font-weight:700}
.note{display:flex;gap:12px;align-items:flex-start;padding:13px 15px;border-radius:12px;background:var(--sunk);font-size:14px}
.note.amb{background:var(--amb-soft)}.note.amb svg{color:var(--amb-ink)}
.note b{display:block;font-size:15px}
.toast{position:fixed;left:50%;bottom:calc(22px + env(safe-area-inset-bottom));transform:translate(-50%,18px);max-width:min(92vw,440px);background:var(--ink);color:var(--bg);padding:12px 18px;border-radius:12px;font-size:15px;font-weight:700;opacity:0;pointer-events:none;transition:opacity .2s,transform .25s cubic-bezier(.2,.9,.3,1.3);z-index:200;display:flex;gap:10px;align-items:center}
.toast.on{opacity:1;transform:translate(-50%,0)}
.toast.ok::before,.toast.err::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--sig);box-shadow:0 0 8px var(--sig)}
.toast.err::before{background:#ff6f61;box-shadow:0 0 8px #ff6f61}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important}}
"""

SPRITE_ICONS = {
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>',
    "qr": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3M21 14v.01M14 21h3M21 17v4"/>',
    "open": '<path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "edit": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "trash": '<path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6M10 11v6M14 11v6"/>',
    "reset": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "pulse": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "db": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "cog": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
    "out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
    "theme": '<circle cx="12" cy="12" r="9"/><path d="M12 3v18a9 9 0 0 0 0-18Z" fill="currentColor"/>',
    "refresh": '<path d="M21 12a9 9 0 0 0-15-6.7L3 8M3 3v5h5M3 12a9 9 0 0 0 15 6.7L21 16M21 21v-5h-5"/>',
    "dl": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    "up": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "back": '<path d="m15 18-6-6 6-6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4M12 17h.01"/>',
    "play": '<path d="m6 3 14 9-14 9Z"/>',
    "terminal": '<path d="m4 17 6-6-6-6M12 19h8"/>',
    "dots": '<circle cx="5" cy="12" r="1.2"/><circle cx="12" cy="12" r="1.2"/><circle cx="19" cy="12" r="1.2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
}
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
          + "".join('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % kv for kv in SPRITE_ICONS.items())
          + '</defs></svg>')


def ic(name):
    return '<svg class="i" aria-hidden="true"><use href="#i-%s"/></svg>' % name


HEAD = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0d1615">
<meta name="robots" content="noindex,nofollow">
<title>__TITLE__</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23132221'/%3E%3Ccircle cx='16' cy='16' r='6' fill='%2300b7a7'/%3E%3C/svg%3E">
__FONTS__
<script>try{var t=localStorage.getItem('mx-theme')}catch(e){}document.documentElement.dataset.theme=t||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')</script>
<style>__BASE__
__CSS__</style>
</head>
"""


def page(title, css, body):
    return (HEAD.replace("__TITLE__", title).replace("__FONTS__", FONTS)
            .replace("__BASE__", BASE_CSS).replace("__CSS__", css) + body)


UTIL_JS = r"""
var $=function(id){return document.getElementById(id);};
var $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
var api=function(u,m,b){var o={method:m||'GET',headers:{'Content-Type':'application/json'},credentials:'same-origin'};if(b!==undefined)o.body=JSON.stringify(b);return fetch(u,o).then(function(r){if(r.status===401&&!/^\/api\/(login|setup)/.test(u)){location.replace('/login');throw new Error('Signed out');}return r;});};
var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
var ic=function(n){return '<svg class="i" aria-hidden="true"><use href="#i-'+n+'"/></svg>';};
function toast(t,k){var e=$('toast');if(!e)return;e.textContent=t;e.className='toast on '+(k||'');clearTimeout(toast.t);toast.t=setTimeout(function(){e.classList.remove('on');},2600);}
function copyText(t,msg){
  var ok=function(){toast(msg||'Copied','ok');};
  var fb=function(){var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;opacity:0;left:-9999px';document.body.appendChild(a);a.select();try{document.execCommand('copy');ok();}catch(e){toast('Copy failed','err');}a.remove();};
  if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(ok,fb);}else{fb();}
}
function fmtBytes(b){b=Number(b)||0;var u=['B','KB','MB','GB','TB'],i=0;while(b>=1024&&i<u.length-1){b/=1024;i++;}return (i?b.toFixed(b>=100?0:b>=10?1:2):b)+' '+u[i];}
function fmtRate(bps){return fmtBytes(bps)+'/s';}
function vu(pct,n,inf){n=n||20;var h='';if(inf){for(var j=0;j<n;j++)h+='<i></i>';return '<div class="vu inf" role="img" aria-label="Unlimited">'+h+'</div>';}
  pct=Math.max(0,Math.min(100,pct||0));var f=Math.round(pct/100*n);if(pct>0&&f===0)f=1;
  for(var i=0;i<n;i++){var p=(i+1)/n*100,c=i<f?'f'+(p>90?' r':p>70?' a':''):'';h+='<i class="'+c+'"></i>';}
  return '<div class="vu" role="img" aria-label="'+pct.toFixed(0)+'% used">'+h+'</div>';}
function toggleTheme(){var d=document.documentElement;d.dataset.theme=d.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('mx-theme',d.dataset.theme);}catch(e){}}
"""

# trace used behind auth screens: a slow oscilloscope sweep
TRACE_SVG = ('<svg class="trace" viewBox="0 0 1200 400" preserveAspectRatio="none" aria-hidden="true">'
             '<path class="grid" d="M0 100H1200M0 200H1200M0 300H1200M200 0V400M400 0V400M600 0V400M800 0V400M1000 0V400"/>'
             '<path class="wave" d="M0 210 C60 210 80 150 120 150 S180 260 240 260 300 120 360 120 420 230 480 230 540 180 600 180 660 300 720 300 780 90 840 90 900 220 960 220 1020 170 1080 170 1140 210 1200 210"/>'
             '<path class="wave w2" d="M0 250 C80 250 110 230 160 230 S260 280 330 280 420 210 500 210 600 260 680 260 780 220 860 220 960 270 1040 270 1140 240 1200 240"/></svg>')

# ============================================================ AUTH (login / setup)
AUTH_CSS = r"""
body{display:grid;place-items:center;padding:24px 18px;overflow-x:hidden;position:relative}
.trace{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.trace .grid{stroke:var(--line);stroke-width:1;fill:none;opacity:.7}
.trace .wave{fill:none;stroke:var(--sig);stroke-width:2.5;stroke-dasharray:2600;stroke-dashoffset:2600;animation:draw 9s cubic-bezier(.6,0,.4,1) infinite;opacity:.55;filter:drop-shadow(0 0 6px var(--sig))}
.trace .w2{stroke:var(--navy);opacity:.25;animation-delay:-4.5s;filter:none}
@keyframes draw{0%{stroke-dashoffset:2600}55%{stroke-dashoffset:0}100%{stroke-dashoffset:-2600}}
.card{position:relative;z-index:1;width:100%;max-width:420px;background:var(--card);border:1.5px solid var(--line);border-radius:22px;padding:34px 30px 28px;box-shadow:var(--shadow);display:grid;gap:20px}
.brand{display:flex;align-items:center;gap:12px}
.brand .lamp{width:14px;height:14px}
.brand b{font-weight:900;font-size:20px;letter-spacing:-.02em}
.brand small{margin-left:auto;font:500 13px var(--mono);color:var(--mut)}
h1{font-size:38px;line-height:1.02;font-weight:900;letter-spacing:-.035em}
h1+p{color:var(--mut);margin-top:8px}
.pw{position:relative}.pw .input{padding-right:48px}.pw button{position:absolute;right:4px;top:3px}
.strength{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;height:6px}.strength i{border-radius:3px;background:var(--seg-off);transition:background .25s}
.strength[data-s="1"] i:nth-child(-n+1){background:var(--red)}.strength[data-s="2"] i:nth-child(-n+2){background:var(--amb)}
.strength[data-s="3"] i:nth-child(-n+3){background:var(--sig)}.strength[data-s="4"] i{background:var(--sig)}
.shake{animation:shake .35s}@keyframes shake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.foot{text-align:center;font-size:14px;color:var(--mut)}
.themebtn{position:fixed;top:14px;right:14px;z-index:2}
@media(max-width:480px){.card{padding:26px 20px 22px;border-radius:18px}h1{font-size:32px}}
"""


def _auth_page(title, heading, sub, form_inner, script):
    return page(title, AUTH_CSS, '<body>' + SPRITE + TRACE_SVG +
                '<button class="ib themebtn" onclick="toggleTheme()" aria-label="Toggle theme">' + ic("theme") + '</button>'
                '<main class="card"><div class="brand"><span class="lamp live"></span><b>MX-UI</b><small>v2.0</small></div>'
                '<div><h1>' + heading + '</h1><p>' + sub + '</p></div>' + form_inner +
                '<p class="foot">Created by Muvixo</p></main><div id="toast" class="toast" role="status"></div>'
                '<script>' + UTIL_JS + script + '</script></body></html>')


def _pw_field(fid, label, ac, ph):
    return ('<label class="field"><span>' + label + '</span><div class="pw"><input type="password" id="' + fid +
            '" class="input" required autocomplete="' + ac + '" placeholder="' + ph + '">'
            '<button type="button" class="ib sm" data-eye="' + fid + '" aria-label="Show password">' + ic("eye") + '</button></div></label>')


_EYE_JS = r"""
document.querySelectorAll('[data-eye]').forEach(function(b){b.onclick=function(){var i=$(b.dataset.eye);i.type=i.type==='password'?'text':'password';i.focus();};});
"""

LOGIN_HTML = _auth_page(
    "Sign in · MX-UI", "Patch in.", "Admin password opens the switchboard.",
    '<form id="f" class="field" style="gap:16px" novalidate>' + _pw_field("pw", "Password", "current-password", "Your admin password") +
    '<div id="err" class="alert hidden" role="alert"></div>'
    '<button type="submit" id="go" class="btn pri block">Sign in</button></form>',
    _EYE_JS + r"""
$('pw').focus();
$('f').onsubmit=async function(e){
  e.preventDefault();var b=$('go'),er=$('err'),pw=$('pw');
  if(!pw.value){pw.focus();return;}
  er.classList.add('hidden');b.disabled=true;b.textContent='Checking…';
  try{
    var r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pw.value})});
    if(!r.ok){var m='Wrong password';try{var d=await r.json();if(d.detail)m=d.detail;}catch(x){}throw new Error(m);}
    var p={};try{p=await (await fetch('/api/current-paths')).json();}catch(x){}
    location.replace(p.dashboard||'/dashboard');
  }catch(x){
    er.textContent=x.message;er.classList.remove('hidden');b.disabled=false;b.textContent='Sign in';
    var c=document.querySelector('.card');c.classList.remove('shake');void c.offsetWidth;c.classList.add('shake');pw.select();
  }
};
""")

SETUP_HTML = _auth_page(
    "First run · MX-UI", "Set the master key.", "First boot. Pick the password that guards this panel.",
    '<form id="f" class="field" style="gap:16px" novalidate>' + _pw_field("pw", "New password", "new-password", "At least 6 characters") +
    '<div class="strength" id="st" data-s="0" aria-hidden="true"><i></i><i></i><i></i><i></i></div>' +
    _pw_field("pw2", "Repeat it", "new-password", "Same again") +
    '<div id="err" class="alert hidden" role="alert"></div>'
    '<button type="submit" id="go" class="btn pri block">Save and open dashboard</button></form>',
    _EYE_JS + r"""
$('pw').focus();
$('pw').oninput=function(){var v=this.value,s=0;if(v.length>=6)s++;if(v.length>=10)s++;if(/[A-Z]/.test(v)&&/[a-z]/.test(v))s++;if(/[0-9]/.test(v)&&/[^A-Za-z0-9]/.test(v))s++;$('st').dataset.s=v?Math.max(1,s):0;};
$('f').onsubmit=async function(e){
  e.preventDefault();var b=$('go'),er=$('err'),a=$('pw').value,c=$('pw2').value;
  var fail=function(m){er.textContent=m;er.classList.remove('hidden');};
  er.classList.add('hidden');
  if(a.length<6)return fail('Use at least 6 characters.');
  if(a!==c)return fail("Passwords don't match.");
  b.disabled=true;b.textContent='Saving…';
  try{
    var r=await fetch('/api/setup',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:a})});
    var d=await r.json().catch(function(){return {};});
    if(!r.ok)throw new Error(d.detail||'Setup failed');
    var p={};try{p=await (await fetch('/api/current-paths')).json();}catch(x){}
    location.replace(p.dashboard||'/dashboard');
  }catch(x){fail(x.message);b.disabled=false;b.textContent='Save and open dashboard';}
};
""")


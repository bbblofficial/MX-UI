# pages_portal.py — the page a subscriber sees when they open their link in a browser.
#
# Lineage: a boarding pass. The QR sits on a perforated stub, the quota is a segmented
# fuel-gauge, and the status is a rubber stamp. Everything is server-rendered, no JS needed
# except copy buttons.
import html as _h

from pages import page, ic, SPRITE, UTIL_JS

PORTAL_CSS = r"""
body{display:grid;place-items:start center;padding:28px 16px 48px;background:
  radial-gradient(1200px 600px at 10% -10%,color-mix(in srgb,var(--sig) 16%,transparent),transparent 60%),
  radial-gradient(900px 500px at 110% 110%,color-mix(in srgb,var(--navy) 12%,transparent),transparent 60%),var(--bg)}
.theme{position:fixed;top:14px;right:14px}
.pass{width:100%;max-width:640px;background:var(--card);border:1.5px solid var(--line);border-radius:24px;box-shadow:var(--shadow);overflow:hidden;position:relative}
.head{display:flex;align-items:center;gap:12px;padding:20px 24px;border-bottom:1.5px dashed var(--line2)}
.head b{font-weight:900;font-size:17px;letter-spacing:-.01em}
.head small{display:block;font:500 12px/1 var(--mono);color:var(--mut);margin-top:4px}
.head .sp{margin-left:auto}
.body{display:grid;grid-template-columns:minmax(0,1fr) 230px;position:relative}
.main{padding:26px 26px 24px;display:grid;gap:20px;min-width:0}
.stub{padding:24px 22px;border-left:2px dashed var(--line2);display:grid;gap:12px;justify-items:center;align-content:start;background:color-mix(in srgb,var(--sunk) 60%,transparent)}
.stub .qr{width:100%;max-width:184px;aspect-ratio:1;background:#fff;border-radius:12px;padding:10px;display:grid;place-items:center}
.stub .qr img{width:100%;height:100%;image-rendering:pixelated}
.stub small{font:500 12px/1.3 var(--mono);color:var(--mut);text-align:center}
.body::before,.body::after{content:"";position:absolute;left:calc(100% - 230px);width:22px;height:22px;border-radius:50%;background:var(--bg);border:1.5px solid var(--line);transform:translateY(-50%);z-index:2}
.body::before{top:0;transform:translate(-50%,-50%)}
.body::after{bottom:0;transform:translate(-50%,50%)}
.name{font-size:clamp(30px,5vw,40px);font-weight:900;letter-spacing:-.035em;line-height:1.02;word-break:break-word}
.stamp{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border:2px solid currentColor;border-radius:8px;font:800 13px/1 var(--ui);letter-spacing:.14em;text-transform:uppercase;transform:rotate(-2deg);color:var(--acc)}
.stamp.off{color:var(--mut)}.stamp.bad{color:var(--red)}.stamp.warn{color:var(--amb-ink)}
.stamp .lamp{width:8px;height:8px}
.gauge{display:grid;gap:10px}
.gauge .top{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.gauge .top b{font-size:28px;font-weight:900;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.gauge .top b em{font-style:normal;font-size:.55em;color:var(--mut);font-weight:700}
.gauge .top span{font:500 13px var(--mono);color:var(--mut)}
.gauge .vu{height:22px;gap:4px}.gauge .vu i{border-radius:3px}
.facts{display:grid;grid-template-columns:1fr 1fr;border:1.5px solid var(--line);border-radius:14px;overflow:hidden}
.facts div{padding:13px 15px;min-width:0}
.facts div:nth-child(odd){border-right:1.5px solid var(--line)}
.facts div:nth-child(-n+2){border-bottom:1.5px solid var(--line)}
.facts small{display:block;color:var(--mut);font-size:12.5px;font-weight:700}
.facts b{display:block;font-size:17px;font-weight:800;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sec{display:flex;align-items:center;justify-content:space-between;gap:10px}
.sec b{font-size:16px;font-weight:800}
.links{border:1.5px solid var(--line);border-radius:14px;overflow:hidden}
.lrow{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:center;padding:11px 12px;border-bottom:1.5px solid var(--line)}
.lrow:last-child{border-bottom:0}
.lrow input{width:100%;min-width:0;height:38px;padding:0 10px;border:1.5px solid var(--line);border-radius:9px;background:var(--sunk);font:12.5px var(--mono);color:var(--mut);text-overflow:ellipsis}
.lrow input:focus{outline:none;border-color:var(--sig)}
.tag{display:inline-flex;align-items:center;height:24px;padding:0 9px;border-radius:6px;font:600 12px/1 var(--mono);background:var(--sunk);color:var(--mut)}
.tag.acc{background:var(--acc-soft);color:var(--acc)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 18px;border-radius:11px;border:1.5px solid var(--line);background:var(--card);font-weight:700;font-size:15px;white-space:nowrap;transition:transform .08s,filter .15s}
.btn:hover{filter:brightness(1.05)}.btn:active{transform:translateY(1px)}
.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--acc-ink)}
.btn.sm{height:36px;padding:0 12px;font-size:14px;border-radius:9px}
.btn.block{width:100%}
.lrow .btn{height:38px}
.foot{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:14px 24px;border-top:1.5px dashed var(--line2);color:var(--mut);font-size:13px;background:var(--sunk)}
.foot b{color:var(--ink)}
.none{padding:18px;text-align:center;color:var(--mut);font-size:14px}
@media(max-width:640px){
  .body{grid-template-columns:1fr}
  .stub{border-left:0;border-top:2px dashed var(--line2);grid-template-columns:auto 1fr;justify-items:start;align-items:center}
  .stub .qr{max-width:132px}
  .stub small{text-align:left}
  .body::before,.body::after{display:none}
  .main{padding:22px 20px}
  .facts{grid-template-columns:1fr}
  .facts div:nth-child(odd){border-right:0}
  .facts div:nth-child(-n+3){border-bottom:1.5px solid var(--line)}
  .lrow{grid-template-columns:minmax(0,1fr) auto}
  .lrow .tag{display:none}
}
"""

PORTAL_JS = r"""
function copyAll(){var v=$$('.lrow input').map(function(i){return i.value;}).filter(Boolean);if(!v.length)return toast('Nothing to copy','err');copyText(v.join('\n'),'All '+v.length+' links copied');}
document.addEventListener('click',function(e){var b=e.target.closest('[data-copy]');if(b){var i=document.getElementById(b.dataset.copy);copyText(i.value,'Link copied');}});
document.querySelectorAll('.lrow input').forEach(function(i){i.addEventListener('focus',function(){i.select();});});
"""


def _gb(n) -> str:
    n = float(n or 0)
    for unit, size in (("TB", 1024 ** 4), ("GB", 1024 ** 3), ("MB", 1024 ** 2), ("KB", 1024)):
        if n >= size:
            return f"{n / size:.2f} {unit}"
    return f"{int(n)} B"


def _fmt_date(iso):
    if not iso:
        return "Never"
    try:
        from datetime import datetime
        return datetime.fromisoformat(iso).strftime("%d %b %Y")
    except Exception:
        return str(iso)[:10]


def _vu(pct: float, n: int = 30, unlimited: bool = False) -> str:
    if unlimited:
        return '<div class="vu inf" role="img" aria-label="Unlimited">' + "<i></i>" * n + "</div>"
    pct = max(0.0, min(100.0, pct))
    filled = round(pct / 100 * n)
    if pct > 0 and filled == 0:
        filled = 1
    cells = []
    for i in range(n):
        p = (i + 1) / n * 100
        cls = ""
        if i < filled:
            cls = "f" + (" r" if p > 90 else " a" if p > 70 else "")
        cells.append(f'<i class="{cls}"></i>')
    return f'<div class="vu" role="img" aria-label="{pct:.0f}% used">' + "".join(cells) + "</div>"


def render_portal(d: dict) -> str:
    """d: output of main.link_public() without ip_pool/note, plus a 'qr' data-URI."""
    e = _h.escape
    label = e(str(d.get("label") or "Config"))
    state = d.get("state", "active")
    limit = int(d.get("limit_bytes") or 0)
    used = int(d.get("used_bytes") or 0)
    pct = 0.0 if limit <= 0 else min(100.0, used / limit * 100)
    unlimited = limit <= 0

    stamp_cls, stamp_text, lamp = {
        "active": ("", "Active", "live"),
        "disabled": ("off", "Paused", "off"),
        "expired": ("bad", "Expired", "cut"),
        "depleted": ("warn", "Out of data", "warn"),
    }.get(state, ("off", "Unavailable", "off"))

    days = d.get("days_left")
    if d.get("expires_at"):
        exp_text = _fmt_date(d.get("expires_at"))
        exp_sub = f"{int(days) if days is not None else 0} day(s) left" if state == "active" else ""
    else:
        exp_text, exp_sub = "Never", "No expiry"

    variants = d.get("variants") or []
    rows = []
    for i, v in enumerate(variants):
        rid = f"lk{i}"
        rows.append(
            f'<div class="lrow"><span class="tag{" acc" if i == 0 else ""}">{e(v["tag"])}</span>'
            f'<input id="{rid}" readonly value="{e(v["url"])}" aria-label="{e(v["tag"])} link">'
            f'<button class="btn sm" data-copy="{rid}">{ic("copy")}<span>Copy</span></button></div>')
    links_html = "".join(rows) if rows else '<div class="none">No links available right now.</div>'

    sub_url = e(str(d.get("sub_url") or ""))
    rid_sub = "subUrl"
    rows_sub = (f'<div class="lrow"><span class="tag">Subscription</span>'
                f'<input id="{rid_sub}" readonly value="{sub_url}" aria-label="Subscription URL">'
                f'<button class="btn sm" data-copy="{rid_sub}">{ic("copy")}<span>Copy</span></button></div>')

    return page(f"{label} · MX-UI", PORTAL_CSS, f"""<body>
{SPRITE}
<button class="ib theme" onclick="toggleTheme()" aria-label="Toggle theme" style="width:40px;height:40px;display:grid;place-items:center;border-radius:10px;color:var(--mut)">{ic("theme")}</button>
<article class="pass" aria-labelledby="pname">
  <header class="head">
    <span class="lamp {lamp}"></span>
    <div><b>MX-UI</b><small>Subscription pass</small></div>
    <span class="sp"></span>
  </header>
  <div class="body">
    <section class="main">
      <div style="display:grid;gap:12px">
        <h1 class="name" id="pname">{label}</h1>
        <span class="stamp {stamp_cls}"><span class="lamp {lamp}"></span>{stamp_text}</span>
      </div>
      <div class="gauge">
        <div class="top"><b>{_gb(used)}<em> / {_gb(limit) if not unlimited else "∞"}</em></b><span>{"unlimited" if unlimited else f"{pct:.0f}% used"}</span></div>
        {_vu(pct, 30, unlimited)}
      </div>
      <div class="facts">
        <div><small>Remaining</small><b>{"∞" if unlimited else _gb(max(0, limit - used))}</b></div>
        <div><small>Expires</small><b>{exp_text}</b><small>{exp_sub}</small></div>
        <div><small>Last seen</small><b>{_fmt_date(d.get("last_used")) if d.get("last_used") else "—"}</b></div>
        <div><small>Live devices</small><b>{int(d.get("live_connections") or 0)}</b></div>
      </div>
      <div class="sec"><b>Connection links</b><button class="btn sm" onclick="copyAll()">{ic("copy")}<span>Copy all</span></button></div>
      <div class="links">{links_html}{rows_sub}</div>
    </section>
    <aside class="stub">
      <div class="qr"><img src="{d.get("qr", "")}" alt="Subscription QR code"></div>
      <small>Scan with your client<br>to import everything</small>
    </aside>
  </div>
  <footer class="foot"><span>Created by Muvixo</span><span>MX-UI <b>v2.0.0</b></span></footer>
</article>
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script>{UTIL_JS}{PORTAL_JS}</script>
</body></html>""")

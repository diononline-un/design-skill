#!/usr/bin/env python3
"""research.py - collect outside evidence cheaply, so the model reads facts instead of raw pages.

  research.py suggest TERM [TERM...] [--lang de] [--expand]   real search phrasing (Google autocomplete)
  research.py profile URL [URL...] [--shots DIR]              rendered page facts: SEO, structure, type, palette, trust, speed
  research.py logo FILE                                       logo colours by share, OKLCH, contrast, role hints
  research.py arena TERM                                      are.na channels to open (public API)

--json on every subcommand. Exit 0 ok, 2 cannot run. Every result names its source URL:
cite it. What a script cannot see (backlinks, search volume, reviews behind logins) is unknown,
never estimated.
"""

import importlib.util
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cd = _load("cd", "check-design.py")
ra = _load("ra", "render-audit.py")
JSON = "--json" in sys.argv
TOOL_UA = "do-design-research/1.0"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def get(url, timeout=15, ua=UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua} if ua else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", errors="replace")


def opt(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) else default
    return default


def positional():
    out, skip = [], False
    for a in sys.argv[2:]:
        if skip:
            skip = False
        elif a in ("--lang", "--shots"):
            skip = True
        elif not a.startswith("--"):
            out.append(a)
    return out


# ------------------------------------------------------------------ suggest
MODIFIERS = {"de": ["kosten", "preis", "in der nähe", "notdienst", "förderung", "erfahrungen", "wie", "was",
                    "wann", "warum", "vs", "oder"],
             "en": ["cost", "price", "near me", "emergency", "reviews", "how", "what", "when", "why", "vs", "or"]}


def cmd_suggest():
    terms, lang = positional(), opt("--lang", "de")
    if not terms:
        print(__doc__)
        return 2
    out = {}
    for term in terms:
        queries = [term] + ([f"{term} {m}" for m in MODIFIERS.get(lang, MODIFIERS["en"])] +
                            [f"{term} {c}" for c in "abcdefghijklmnoprstuvwz"] if "--expand" in sys.argv else [])
        seen = []
        for q in queries:
            url = ("https://suggestqueries.google.com/complete/search?client=firefox&hl=" + lang +
                   "&q=" + urllib.parse.quote(q))
            try:
                for s in json.loads(get(url, ua=None))[1]:
                    if s not in seen:
                        seen.append(s)
            except (OSError, ValueError, IndexError):
                pass
            time.sleep(0.15)
        out[term] = seen
    if JSON:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        for term, s in out.items():
            print(f"{term}  ({len(s)} suggestions, source: Google autocomplete, hl={lang}; "
                  "order = popularity hint, not volume; results lean toward the caller's region)")
            for x in s:
                print(f"  {x}")
    return 0 if any(out.values()) else 2


# ------------------------------------------------------------------ profile
PROFILE_JS = r"""
(() => {
  const W = document.documentElement.clientWidth, H = innerHeight, t = s => (s || '').trim().replace(/\s+/g, ' ');
  const shown = e => e.checkVisibility ? e.checkVisibility() : !!e.offsetWidth;
  const q = s => [...document.querySelectorAll(s)].filter(shown);
  const cs = e => getComputedStyle(e);
  const meta = n => (document.querySelector(`meta[name="${n}"],meta[property="${n}"]`) || {}).content || '';
  const ld = []; for (const s of document.querySelectorAll('script[type="application/ld+json"]')) {
    try { const walk = o => { if (Array.isArray(o)) return o.forEach(walk); if (o && typeof o === 'object') {
      if (o['@type']) ld.push([].concat(o['@type']).join('/')); if (o['@graph']) walk(o['@graph']); } }; walk(JSON.parse(s.textContent)); } catch (e) {} }
  const cv = document.createElement('canvas').getContext('2d', {willReadFrequently: true});
  const norm = c => { cv.clearRect(0, 0, 1, 1); cv.fillStyle = '#000'; cv.fillStyle = c; cv.fillRect(0, 0, 1, 1);
    const d = cv.getImageData(0, 0, 1, 1).data; return d[3] < 200 ? null : '#' + [d[0], d[1], d[2]].map(v => v.toString(16).padStart(2, '0')).join(''); };
  const area = {}, ink = {}, fonts = {};
  for (const e of q('body, body *')) { const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const s = cs(e), a = Math.min(r.width, W) * Math.min(r.height, 4 * H);
    const bg = norm(s.backgroundColor); if (bg) area[bg] = (area[bg] || 0) + a;
    const own = [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim().length;
    if (own) { const c = norm(s.color); if (c) ink[c] = (ink[c] || 0) + own;
      const f = s.fontFamily.split(',')[0].replace(/["']/g, '').trim(); fonts[f] = (fonts[f] || 0) + own; } }
  const top = (o, n) => { const sum = Object.values(o).reduce((a, b) => a + b, 0) || 1;
    return Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n).map(([k, v]) => `${k} ${Math.round(v / sum * 100)}%`); };
  const h1 = q('h1')[0], btn = q('a,button').filter(e => { const r = e.getBoundingClientRect(); return r.top < H && norm(cs(e).backgroundColor) && t(e.innerText).length > 1 && t(e.innerText).length < 40; });
  const fold = t(document.body.innerText.slice(0, 4000)), body = t(document.body.innerText);
  const host = location.hostname, links = q('a[href]'), internal = links.filter(a => a.hostname === host).length;
  const nav = q('header a, nav a').map(a => t(a.innerText)).filter(x => x && x.length < 40);
  const phoneTop = q('a[href^="tel:"]').some(a => a.getBoundingClientRect().top < H);
  const trust = (body.match(/\b(seit \d{4}|since \d{4}|\d+\s*(jahre|years)|meister\w*|innung|zertifiz\w*|certified|award\w*|auszeichnung\w*|garantie|guarantee|bewertung\w*|reviews?|sterne|stars?|t[üu]v|f[öo]rder\w*)\b/gi) || [])
    .map(x => x.toLowerCase());
  const nav_t = performance.getEntriesByType('navigation')[0] || {};
  const bytes = performance.getEntriesByType('resource').reduce((a, r) => a + (r.transferSize || 0), nav_t.transferSize || 0);
  return {
    title: document.title, description: meta('description'), lang: document.documentElement.lang,
    canonical: (document.querySelector('link[rel=canonical]') || {}).href || '', robots: meta('robots'),
    h1: h1 ? t(h1.innerText) : '', h1_px: h1 ? parseFloat(cs(h1).fontSize) : 0,
    h2: q('h2').map(e => t(e.innerText)).filter(Boolean).slice(0, 10),
    nav: [...new Set(nav)].slice(0, 12), ctas_above_fold: [...new Set(btn.map(e => t(e.innerText)))].slice(0, 6),
    phone_above_fold: phoneTop, schema: [...new Set(ld)], words: body.split(' ').length,
    links_internal: internal, links_external: links.length - internal,
    images: q('img').length, images_no_alt: q('img:not([alt])').length,
    hero_media: !!q('img,video,picture,canvas,svg').find(e => { const r = e.getBoundingClientRect(); return r.top < H && r.width * r.height > W * H * 0.15; }),
    fonts_by_text: top(fonts, 4), fonts_loaded: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '')))].slice(0, 6),
    palette_by_area: top(area, 6), text_colors: top(ink, 4),
    trust_signals: Object.entries(trust.reduce((o, x) => (o[x] = (o[x] || 0) + 1, o), {})).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => `${k} x${v}`),
    load_ms: Math.round(nav_t.loadEventEnd || 0), transfer_kb: Math.round(bytes / 1024), viewport_meta: !!document.querySelector('meta[name=viewport]'),
  };
})()
"""


def static_profile(url):
    """Fallback without a browser: SEO fields only, from the raw HTML."""
    html = get(url)
    grab = lambda rx: [re.sub(r"<[^>]+>|\s+", " ", m).strip() for m in re.findall(rx, html, re.S | re.I)]  # noqa: E731
    meta = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, re.I)
    return {"title": (grab(r"<title[^>]*>(.*?)</title>") or [""])[0], "description": meta.group(1) if meta else "",
            "h1": (grab(r"<h1[^>]*>(.*?)</h1>") or [""])[0], "h2": grab(r"<h2[^>]*>(.*?)</h2>")[:10],
            "schema": sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', html))),
            "note": "static HTML only: no browser found, so no fonts, palette, speed or JS-rendered content"}


def cmd_profile():
    urls, shots = positional(), opt("--shots")
    if not urls:
        print(__doc__)
        return 2
    chrome, results = ra.find_chrome(None), {}
    if not chrome:
        for u in urls:
            try:
                results[u] = static_profile(u)
            except OSError as e:
                results[u] = {"error": str(e)}
    else:
        proc, profile, ws = ra.launch(chrome)
        try:
            cdp = ra.CDP(ws, timeout=60)
            cdp.call("Page.enable")
            cdp.call("Network.setUserAgentOverride", userAgent=UA)
            cdp.call("Emulation.setDeviceMetricsOverride", width=1280, height=900, deviceScaleFactor=1, mobile=False)
            for i, u in enumerate(urls):
                try:
                    cdp.events.clear()
                    cdp.call("Page.navigate", url=u)
                    cdp.wait_event("Page.loadEventFired", 30)
                    cdp.js("new Promise(r => setTimeout(r, 1200))")
                    results[u] = cdp.js(PROFILE_JS)
                    if shots:
                        Path(shots).mkdir(parents=True, exist_ok=True)
                        shot = cdp.call("Page.captureScreenshot", format="jpeg", quality=70)
                        p = Path(shots) / f"{i + 1:02d}-{urllib.parse.urlparse(u).hostname}.jpg"
                        p.write_bytes(ra.base64.b64decode(shot["data"]))
                        results[u]["shot"] = str(p)
                except (RuntimeError, OSError) as e:
                    results[u] = {"error": str(e)}
        finally:
            proc.kill()
            ra.shutil.rmtree(profile, ignore_errors=True)
    if JSON:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for u, r in results.items():
            print(f"\n{u}")
            for k, v in r.items():
                if v not in ("", [], None):
                    print(f"  {k}: {', '.join(map(str, v)) if isinstance(v, list) else v}")
    if len(urls) > 1 and not JSON and all("error" not in r for r in results.values()):
        common = Counter(x.split(" ")[0] for r in results.values() for x in r.get("schema", []))
        print(f"\nshared across {len(urls)} sites: schema {dict(common.most_common(4))}; "
              f"phone above fold {sum(bool(r.get('phone_above_fold')) for r in results.values())}/{len(urls)}")
    return 0


# ------------------------------------------------------------------ logo
LOGO_JS = r"""
(async (src) => {
  const img = new Image(); img.src = src; await img.decode();
  const w = Math.min(img.naturalWidth || 400, 400), h = Math.round(w * (img.naturalHeight || 400) / (img.naturalWidth || 400));
  const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'); x.drawImage(img, 0, 0, w, h);
  const d = x.getImageData(0, 0, w, h).data, bins = {};
  for (let i = 0; i < d.length; i += 4) { if (d[i + 3] < 128) continue;
    const k = [d[i], d[i + 1], d[i + 2]].map(v => Math.min(255, Math.round(v / 12) * 12)).join(',');
    bins[k] = (bins[k] || 0) + 1; }
  return Object.entries(bins).sort((a, b) => b[1] - a[1]).slice(0, 40);
})
"""


def cmd_logo():
    files = positional()
    if not files or not Path(files[0]).is_file():
        print("usage: research.py logo FILE   (svg, png, jpg, webp)")
        return 2
    path = Path(files[0]).resolve()
    counts = Counter()
    chrome = ra.find_chrome(None)
    if chrome:
        proc, profile, ws = ra.launch(chrome)
        try:
            cdp = ra.CDP(ws)
            cdp.call("Page.enable")
            mime = {".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
                    ".gif": "image/gif"}.get(path.suffix.lower(), "image/png")
            src = f"data:{mime};base64," + ra.base64.b64encode(path.read_bytes()).decode()  # file:// would taint the canvas
            for k, n in cdp.js(LOGO_JS + f"({json.dumps(src)})"):
                counts[tuple(int(v) for v in k.split(","))] += n
        finally:
            proc.kill()
            ra.shutil.rmtree(profile, ignore_errors=True)
    elif path.suffix.lower() == ".svg":
        for m in cd.COLOR_RE.findall(path.read_text(encoding="utf-8", errors="replace")):
            c = cd.parse_color(m)
            if c:
                counts[tuple(int(v) for v in c[:3])] += 1
    else:
        print("raster logos need Chrome/Chromium (CHROME=...); SVG works without it")
        return 2
    merged = []  # fold anti-aliasing steps into their parent colour
    for rgb, n in counts.most_common():
        for m in merged:
            if max(abs(a - b) for a, b in zip(rgb, m[0])) <= 36:
                m[1] += n
                break
        else:
            merged.append([rgb, n])
    total = sum(n for _, n in merged) or 1
    rows = []
    for rgb, n in merged[:6]:
        if n / total < 0.01:
            continue
        c = rgb + (1.0,)
        L, C, H = cd.oklch(c)
        role = ("accent candidate" if C >= 0.08 else "ink candidate" if L < 0.35 else
                "ground candidate" if L > 0.92 else "neutral step")
        rows.append({"hex": cd.to_hex(c), "share": round(n / total * 100), "oklch": f"{L:.2f} {C:.3f} {H:.0f}",
                     "on_white": round(cd.contrast(c, (255, 255, 255, 1)), 2),
                     "on_black": round(cd.contrast(c, (0, 0, 0, 1)), 2), "role": role})
    if JSON:
        print(json.dumps({"file": str(path), "colors": rows}, indent=2))
    else:
        print(f"{path.name}: colours by share (transparent pixels ignored)")
        for r in rows:
            print(f"  {r['hex']}  {r['share']:>3}%  oklch {r['oklch']:<15} {r['on_white']:>5}:1 on white  "
                  f"{r['on_black']:>5}:1 on black  {r['role']}")
        print("  The logo is evidence, not the palette: an accent must still pass 4.5:1 as text and with text on it.")
    return 0


# ------------------------------------------------------------------ are.na
def cmd_arena():
    terms = positional()
    if not terms:
        print(__doc__)
        return 2
    term = urllib.parse.quote(" ".join(terms))
    try:  # public channel search; block search and channel contents now need an are.na login
        ch = json.loads(get(f"https://api.are.na/v2/search/channels?q={term}&per=15", ua=TOOL_UA))
    except (OSError, ValueError) as e:
        print(f"are.na unreachable: {e}")
        return 2
    out = [{"title": c.get("title"), "blocks": c.get("length"),
            "url": f"https://www.are.na/{(c.get('user') or {}).get('slug', '')}/{c.get('slug')}"}
           for c in ch.get("channels", []) if c.get("length")]
    if JSON:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"are.na channels for '{' '.join(terms)}' (open the URLs in a browser to see the blocks)")
        for c in out:
            print(f"  {c['blocks']:>5} blocks  {c['title'][:50]:<50} {c['url']}")
    return 0 if out else 2


def main():
    cmds = {"suggest": cmd_suggest, "profile": cmd_profile, "logo": cmd_logo, "arena": cmd_arena}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        return 2
    return cmds[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())

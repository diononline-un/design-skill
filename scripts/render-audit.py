#!/usr/bin/env python3
"""render-audit.py - measure what the browser actually painted. Stdlib + Chrome/Chromium.

  python3 render-audit.py <url|file> [--widths 1280,768,390] [--shots DIR] [--full]
                          [--min-font 12] [--max N] [--chrome PATH] [--inject-css FILE] [--json]

--inject-css adds a stylesheet after load: measure a CSS fix against the deployed page
before deploying it.

Source scanners cannot see that a headline sits on the nav at 390px. This loads the
page at each width and reports measurements, not taste:

  page_scrolls_sideways P0  document wider than the viewport (names the widest offender)
  text_overlap        P0/P1 unrelated text boxes overlap >18% (P0 >50%)
  text_squeezed         P0  >=8 chars in a column under 3x font size, 4+ lines
  text_clipped          P1  overflow hidden cuts real text (no ellipsis, no line-clamp)
  text_offscreen        P1  text past the viewport edge
  contrast_below_aa     P1  against the painted background, translucent layers composited
                            (disabled controls are exempt, as in WCAG)
  focus_invisible       P1  Tab focus changes nothing visible (first width only)
  img_no_alt            P1  rendered <img> without alt
  text_too_small     P1/P2  computed size under --min-font
  tap_target_small      P2  control under 24x24 at <=560px (links in running prose exempt)
  row_misaligned        P2  3+ equal cards in a row whose short trailing labels sit at different heights
  heading_order         P2  not exactly one h1, or a skipped level
  no_lang               P2  <html> without lang

Measured with prefers-reduced-motion: reduce and after one scroll pass, so scroll reveals,
lazy content and count-ups are in their final state, not mid-animation.
Visually-hidden content (clip-path: inset(50%), clip: rect(0 0 0 0), 1px boxes) is skipped.
Contrast over background images is skipped, not guessed. Screenshots (--shots) come from
the same viewport emulation as the measurements; a screenshot taken another way can lie.
Exit: 0 clean, 1 P0/P1 findings above --max, 2 cannot run.
"""

import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


# ------------------------------------------------------------------ minimal CDP over WebSocket

class CDP:
    def __init__(self, ws_url, timeout=30):
        host_port, path = ws_url[len("ws://"):].split("/", 1)
        host, port = host_port.split(":")
        self.sock = socket.create_connection((host, int(port)), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f"GET /{path} HTTP/1.1\r\nHost: {host_port}\r\nUpgrade: websocket\r\n"
                           f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
                           "Sec-WebSocket-Version: 13\r\n\r\n").encode())
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self.sock.recv(1)
            if not chunk:
                raise ConnectionError("websocket handshake failed")
            head += chunk
        if b" 101 " not in head.split(b"\r\n", 1)[0]:
            raise ConnectionError(head.decode(errors="replace"))
        self.next_id, self.events = 0, []

    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("browser closed the connection")
            buf += chunk
        return buf

    def _recv(self):
        data = b""
        while True:
            b1, b2 = self._recv_exact(2)
            n = b2 & 0x7F
            if n == 126:
                n = struct.unpack(">H", self._recv_exact(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._recv_exact(8))[0]
            payload = self._recv_exact(n)
            op = b1 & 0x0F
            if op == 0x8:
                raise ConnectionError("browser closed the connection")
            if op == 0x9:
                self._send(payload, 0xA)
                continue
            data += payload
            if b1 & 0x80:
                return json.loads(data)

    def _send(self, payload, op=0x1):
        mask = os.urandom(4)
        n = len(payload)
        head = bytes([0x80 | op]) + (bytes([0x80 | n]) if n < 126 else
                                     bytes([0x80 | 126]) + struct.pack(">H", n) if n < 65536 else
                                     bytes([0x80 | 127]) + struct.pack(">Q", n))
        self.sock.sendall(head + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def call(self, method, **params):
        self.next_id += 1
        self._send(json.dumps({"id": self.next_id, "method": method, "params": params}).encode())
        while True:
            msg = self._recv()
            if msg.get("id") == self.next_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg["method"])

    def wait_event(self, name, timeout):
        end = time.time() + timeout
        while name not in self.events:
            if time.time() > end:
                return False
            self.sock.settimeout(max(0.1, end - time.time()))
            try:
                msg = self._recv()
            except socket.timeout:
                return False
            if "method" in msg:
                self.events.append(msg["method"])
        self.sock.settimeout(30)
        return True

    def js(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", "page script failed"))
        return r["result"].get("value")


def find_chrome(explicit):
    for c in [explicit, os.environ.get("CHROME")] + [shutil.which(n) for n in (
            "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
            "microsoft-edge", "brave", "brave-browser")] + [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"]:
        if c and Path(c).exists():
            return c
    return None


def launch(chrome):
    profile = tempfile.mkdtemp(prefix="render-audit-")
    args = [chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
            "--hide-scrollbars", "--mute-audio", "--disable-extensions", "--remote-debugging-port=0",
            f"--user-data-dir={profile}", "about:blank"]
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        args.insert(1, "--no-sandbox")
    proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    port_file = Path(profile) / "DevToolsActivePort"
    for _ in range(200):
        if port_file.exists() and port_file.read_text().strip():
            break
        time.sleep(0.1)
    else:
        proc.kill()
        raise RuntimeError("browser did not start")
    port = port_file.read_text().split()[0]
    for _ in range(50):
        try:
            targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=2))
            page = next(t for t in targets if t.get("type") == "page")
            return proc, profile, page["webSocketDebuggerUrl"]
        except (OSError, StopIteration, ValueError):
            time.sleep(0.1)
    proc.kill()
    raise RuntimeError("no page target")


# ------------------------------------------------------------------ in-page measurement

MEASURE_JS = r"""
(async (O) => {
  scrollTo(0, 0);
  const W = document.documentElement.clientWidth, out = [];  // layout viewport: mobile shrink-to-fit must not hide overflow
  const sel = el => { if (!el || !el.tagName) return ''; let s = el.tagName.toLowerCase();
    if (el.id) return s + '#' + el.id;
    const c = (typeof el.className === 'string' ? el.className : '').trim().split(/\s+/).filter(c => c && !c.includes(':')).slice(0, 2);
    return s + (c.length ? '.' + c.join('.') : ''); };
  const txt = el => ((el && (el.innerText || el.getAttribute && el.getAttribute('aria-label'))) || '').trim().replace(/\s+/g, ' ').slice(0, 40);
  const add = (code, sev, el, detail) => out.push({code, sev, sel: sel(el), text: txt(el), detail: detail || ''});
  const cs = el => getComputedStyle(el);
  const cv = document.createElement('canvas').getContext('2d', {willReadFrequently: true}), cache = {};
  const rgba = c => { if (cache[c]) return cache[c]; cv.clearRect(0, 0, 1, 1); cv.fillStyle = '#000'; cv.fillStyle = c;
    cv.fillRect(0, 0, 1, 1); const d = cv.getImageData(0, 0, 1, 1).data; return cache[c] = [d[0], d[1], d[2], d[3] / 255]; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const over = (top, bot) => { const a = top[3] + bot[3] * (1 - top[3]); if (!a) return [0, 0, 0, 0];
    return [0, 1, 2].map(i => (top[i] * top[3] + bot[i] * bot[3] * (1 - top[3])) / a).concat(a); };
  const hex = c => '#' + c.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const hiddenOnPurpose = el => { for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const s = cs(e); if (s.clipPath.startsWith('inset(50%') || s.clip.startsWith('rect(0')) return true;
      const r = e.getBoundingClientRect(); if (r.width <= 2 && r.height <= 2 && s.overflow !== 'visible') return true; }
    return false; };
  const shown = el => el.checkVisibility ? el.checkVisibility({opacityProperty: true, visibilityProperty: true, checkOpacity: true, checkVisibilityCSS: true})
    : !!(el.offsetWidth || el.offsetHeight);
  // Line boxes of an element's own text, in document coordinates. Each line is capped at the
  // line height: tight display leading leaves empty ascender space above the line box.
  const textLines = el => { const s = cs(el), lh = parseFloat(s.lineHeight) || parseFloat(s.fontSize) * 1.2, out = [];
    for (const n of el.childNodes) if (n.nodeType === 3 && n.nodeValue.trim()) {
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q of rg.getClientRects()) if (q.width && q.height) { let t = q.top + scrollY, b = q.bottom + scrollY;
        if (b - t > lh) { const c = (t + b) / 2; t = c - lh / 2; b = c + lh / 2; }
        out.push({l: q.left, t, r: q.right, b}); } }
    return out; };
  const union = rs => rs.length ? rs.reduce((u, q) => ({l: Math.min(u.l, q.l), t: Math.min(u.t, q.t), r: Math.max(u.r, q.r), b: Math.max(u.b, q.b)})) : null;
  const visibleBox = (el, b) => { b = {...b};  // what survives overflow clipping, for overlap
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const s = cs(a);
      if (s.overflowX === 'visible' && s.overflowY === 'visible') continue; const r = a.getBoundingClientRect();
      if (s.overflowX !== 'visible') { b.l = Math.max(b.l, r.left); b.r = Math.min(b.r, r.right); }
      if (s.overflowY !== 'visible') { b.t = Math.max(b.t, r.top + scrollY); b.b = Math.min(b.b, r.bottom + scrollY); } }
    if (/hidden|clip/.test(cs(el).overflowX + cs(el).overflowY)) { const r = el.getBoundingClientRect();
      b.l = Math.max(b.l, r.left); b.r = Math.min(b.r, r.right); b.t = Math.max(b.t, r.top + scrollY); b.b = Math.min(b.b, r.bottom + scrollY); }
    return b.r > b.l && b.b > b.t ? b : null; };
  const clipsX = e => { for (let a = e.parentElement; a && a !== document.body && a !== document.documentElement; a = a.parentElement)
      if (cs(a).overflowX !== 'visible') return true; return false; };

  const texts = [], seen = new Set();
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {acceptNode: n => n.nodeValue.trim() ? 1 : 2});
  while (tw.nextNode()) { const el = tw.currentNode.parentElement;
    if (!el || seen.has(el) || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|OPTION|TITLE)$/.test(el.tagName)) continue;
    seen.add(el); if (!shown(el) || hiddenOnPurpose(el)) continue;
    const lines = textLines(el), box = union(lines);
    if (box) { const vis = visibleBox(el, box);
      const clipTo = q => vis && {l: Math.max(q.l, vis.l), t: Math.max(q.t, vis.t), r: Math.min(q.r, vis.r), b: Math.min(q.b, vis.b)};
      texts.push({el, box, vis, lines: lines.map(clipTo).filter(q => q && q.r > q.l && q.b > q.t), s: cs(el)}); } }

  // sideways scroll
  const sw = document.documentElement.scrollWidth;
  if (sw > W + 1) { let worst = null, wr = W;
    for (const e of document.body.querySelectorAll('*')) { const r = e.getBoundingClientRect();
      if (r.right > wr + 0.5 && r.width && !clipsX(e)) { wr = r.right; worst = e; } }
    add('page_scrolls_sideways', 'P0', worst, `document ${sw}px wide in a ${W}px viewport; widest: right edge ${Math.round(wr)}px. Usually a flex/grid child without min-width: 0`); }

  for (const {el, box, s} of texts) {
    const fs = parseFloat(s.fontSize), own = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.nodeValue).join('').trim();
    if (fs < O.minFont) add('text_too_small', fs < O.minFont - 1 ? 'P1' : 'P2', el, `${fs}px`);
    if ((box.l < -1 || box.r > W + 1) && !clipsX(el)) add('text_offscreen', 'P1', el, `text spans ${Math.round(box.l)}..${Math.round(box.r)}px of ${W}`);
    const lh = parseFloat(s.lineHeight) || fs * 1.2, w = el.clientWidth || box.r - box.l, h = box.b - box.t;
    if (own.length >= 8 && w < 3 * fs && h > 4 * lh) add('text_squeezed', 'P0', el, `${Math.round(w)}px wide, ${Math.round(h / lh)} lines`);
    if (s.textOverflow !== 'ellipsis' && s.webkitLineClamp === 'none') {
      for (let a = el, d = 0; a && d < 4 && a !== document.body; a = a.parentElement, d++) {
        const as = cs(a); if (!/hidden|clip/.test(as.overflowX + as.overflowY)) continue;
        if (as.textOverflow === 'ellipsis' || as.webkitLineClamp !== 'none') break;
        const r = a.getBoundingClientRect(), top = r.top + scrollY, bot = r.bottom + scrollY;
        if (box.b > bot + 2 && /hidden|clip/.test(as.overflowY) || (box.r > r.right + 2 || box.l < r.left - 2) && /hidden|clip/.test(as.overflowX) || box.t < top - 2 && /hidden|clip/.test(as.overflowY))
          { add('text_clipped', 'P1', el, `cut by ${sel(a)} (overflow ${as.overflow}); use min-height, not height`); break; } } }
  }

  // overlap: unrelated text, line box against line box; fixed/sticky layers excluded
  const area = rs => rs.reduce((a, q) => a + (q.r - q.l) * (q.b - q.t), 0);
  const flow = texts.filter(t => t.lines.length && !/fixed|sticky/.test(t.s.position)).map(t => ({...t, box: union(t.lines)}))
    .slice(0, 3000).sort((a, b) => a.box.t - b.box.t);
  let overlaps = 0;
  for (let i = 0; i < flow.length && overlaps < 50; i++) { const A = flow[i];
    for (let j = i + 1; j < flow.length && flow[j].box.t < A.box.b; j++) { const B = flow[j];
      if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
      let inter = 0;
      for (const p of A.lines) for (const q of B.lines) { const x = Math.min(p.r, q.r) - Math.max(p.l, q.l), y = Math.min(p.b, q.b) - Math.max(p.t, q.t);
        if (x > 0 && y > 0) inter += x * y; }
      if (!inter) continue;
      const ratio = inter / Math.min(area(A.lines), area(B.lines));
      if (ratio > 0.18) { overlaps++; add('text_overlap', ratio > 0.5 ? 'P0' : 'P1', A.el, `${Math.round(ratio * 100)}% over ${sel(B.el)} "${txt(B.el).slice(0, 24)}"`); } } }

  // contrast against what is painted under the text
  let skipped = 0; const vh = innerHeight;
  for (const {el, box, s} of [...texts].sort((a, b) => a.box.t - b.box.t)) {
    if (s.webkitTextFillColor && rgba(s.webkitTextFillColor)[3] === 0) continue;
    if (el.closest(':disabled, [aria-disabled="true"]')) continue;  // WCAG 1.4.3 exempts inactive controls
    let fg = rgba(s.color), op = 1; for (let e = el; e; e = e.parentElement) op *= +cs(e).opacity;
    fg = fg.slice(0, 3).concat(fg[3] * op); if (fg[3] < 0.05) continue;
    const cy = (box.t + box.b) / 2, cx = Math.min(Math.max((box.l + box.r) / 2, 1), W - 1);
    if (cy < scrollY || cy > scrollY + vh - 1) scrollTo(0, Math.max(0, cy - vh / 2));
    const stack = document.elementsFromPoint(cx, cy - scrollY); let k = stack.indexOf(el);
    let layers = k >= 0 ? stack.slice(k) : []; if (k < 0) for (let e = el; e; e = e.parentElement) layers.push(e);
    let bg = null, unknown = false; const cols = [];
    for (const e of layers) { const es = cs(e); if (es.backgroundImage !== 'none' || e.tagName === 'IMG' || e.tagName === 'VIDEO' || e.tagName === 'CANVAS') { unknown = true; break; }
      const c = rgba(es.backgroundColor); if (c[3] > 0) { cols.push(c); if (c[3] >= 1) break; } }
    if (unknown) { skipped++; continue; }
    bg = [255, 255, 255, 1]; for (const c of cols.reverse()) bg = over(c, bg);
    const f = over(fg, bg), L1 = lum(f), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const fs = parseFloat(s.fontSize), large = fs >= 24 || fs >= 18.66 && +s.fontWeight >= 700, need = large ? 3 : 4.5;
    if (ratio < need - 0.005) add('contrast_below_aa', 'P1', el, `${ratio.toFixed(2)}:1, needs ${need} (${hex(f)} on ${hex(bg)})`); }
  scrollTo(0, 0);

  if (W <= 560) for (const e of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[tabindex]:not([tabindex="-1"])')) {
    if (!shown(e) || hiddenOnPurpose(e)) continue; const r = e.getBoundingClientRect();
    const inProse = e.tagName === 'A' && cs(e).display === 'inline' && (e.parentElement.innerText || '').trim().length > (e.innerText || '').trim().length + 20;
    if (!inProse && (r.width < 24 || r.height < 24)) add('tap_target_small', 'P2', e, `${Math.round(r.width)}x${Math.round(r.height)}px`); }

  // rows of equal cards whose trailing short labels do not line up
  for (const p of document.body.querySelectorAll('*')) { const kids = [...p.children].filter(shown); if (kids.length < 3) continue;
    const rows = {}; for (const k of kids) { const r = k.getBoundingClientRect(); if (r.width < 40) continue;
      (rows[Math.round(r.top / 3)] = rows[Math.round(r.top / 3)] || []).push({k, r}); }
    for (const row of Object.values(rows)) { if (row.length < 3) continue;
      if (row.some(x => Math.abs(x.r.width - row[0].r.width) > 2 || Math.abs(x.r.height - row[0].r.height) > 2)) continue;
      const offs = row.map(({k, r}) => { const last = texts.filter(t => k.contains(t.el) && t.el !== k && txt(t.el).length <= 40).pop();
        return last ? last.box.t - (r.top + scrollY) : null; });
      if (offs.includes(null)) continue; const d = Math.max(...offs) - Math.min(...offs);
      if (d > 4) add('row_misaligned', 'P2', p, `trailing labels differ by ${Math.round(d)}px; card = flex column, body flex: 1`); } }

  for (const i of document.querySelectorAll('img:not([alt])')) if (shown(i)) add('img_no_alt', 'P1', i, i.currentSrc.split('/').pop().slice(0, 40));
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(shown), h1 = hs.filter(h => h.tagName === 'H1').length;
  let skip = null; for (let i = 1; i < hs.length; i++) if (+hs[i].tagName[1] > +hs[i - 1].tagName[1] + 1) { skip = hs[i]; break; }
  if (hs.length && (h1 !== 1 || skip)) add('heading_order', 'P2', skip || hs[0], h1 !== 1 ? `${h1} h1 elements` : `skips a level before ${skip.tagName.toLowerCase()}`);
  if (!document.documentElement.lang) add('no_lang', 'P2', document.documentElement, 'screen readers and hyphens: auto need it');
  return {findings: out, scrollWidth: sw, width: W, height: document.documentElement.scrollHeight, texts: texts.length, contrastSkipped: skipped};
})
"""

# Scroll once through the page so IntersectionObserver reveals and lazy content fire.
SETTLE_JS = r"""
(async () => { const step = innerHeight * 0.8, wait = ms => new Promise(r => setTimeout(r, ms));
  for (let y = 0; y < document.documentElement.scrollHeight && y < 40000; y += step) { scrollTo(0, y); await wait(50); }
  scrollTo(0, 0); await wait(700); })()
"""

FOCUS_BASE_JS = r"""
(() => {
  const sig = e => { const s = getComputedStyle(e), a = getComputedStyle(e, '::after'), b = getComputedStyle(e, '::before');
    return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.backgroundColor, s.borderColor, s.color,
            s.textDecorationLine, a.outlineStyle, a.boxShadow, a.opacity, b.boxShadow, b.opacity].join('|'); };
  window.__raSig = sig; window.__raBase = new Map();
  for (const e of document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[tabindex]:not([tabindex="-1"])'))
    if (e.checkVisibility ? e.checkVisibility() : e.offsetWidth) window.__raBase.set(e, sig(e));
  document.activeElement && document.activeElement.blur();
  return window.__raBase.size;
})()
"""
FOCUS_STEP_JS = r"""
(() => { const e = document.activeElement; if (!e || !window.__raBase.has(e)) return null;
  const changed = window.__raSig(e) !== window.__raBase.get(e) || (e.parentElement && e.parentElement.matches(':focus-within')
    && getComputedStyle(e.parentElement).outlineStyle !== 'none');
  let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id;
  return {changed, sel: s, text: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 40)}; })()
"""


def audit(cdp, url, width, opts, first):
    cdp.call("Emulation.setDeviceMetricsOverride", width=width, height=900 if width >= 768 else 844,
             deviceScaleFactor=1, mobile=width < 768)
    cdp.events.clear()
    cdp.call("Page.navigate", url=url)
    if not cdp.wait_event("Page.loadEventFired", 30):
        raise RuntimeError(f"{url} did not finish loading in 30 s")
    if opts.inject_css:
        css = Path(opts.inject_css).read_text(encoding="utf-8")
        cdp.js(f"document.head.insertAdjacentHTML('beforeend', '<style>' + {json.dumps(css)} + '</style>')")
    cdp.js("document.fonts.ready.then(() => new Promise(r => setTimeout(r, 400)))")
    cdp.js(SETTLE_JS)
    res = cdp.js(MEASURE_JS + f"({json.dumps({'minFont': opts.min_font})})")
    if first:
        n = cdp.js(FOCUS_BASE_JS)
        silent, seen = [], set()
        for _ in range(min(n, 20)):
            for t in ("keyDown", "keyUp"):
                cdp.call("Input.dispatchKeyEvent", type=t, key="Tab", code="Tab", windowsVirtualKeyCode=9)
            step = cdp.js(FOCUS_STEP_JS)
            if step and step["sel"] + step["text"] not in seen:
                seen.add(step["sel"] + step["text"])
                if not step["changed"]:
                    silent.append(step)
        for s in silent:
            res["findings"].append({"code": "focus_invisible", "sev": "P1", "sel": s["sel"], "text": s["text"],
                                    "detail": "Tab focus changes nothing visible; add a :focus-visible ring >=3:1"})
    if opts.shots:
        Path(opts.shots).mkdir(parents=True, exist_ok=True)
        height = min(res["height"], 8000) if opts.full else (900 if width >= 768 else 844)
        shot = cdp.call("Page.captureScreenshot", format="png", captureBeyondViewport=opts.full,
                        clip={"x": 0, "y": 0, "width": width, "height": height, "scale": 1})
        path = Path(opts.shots) / f"{width}.png"
        path.write_bytes(base64.b64decode(shot["data"]))
        res["shot"] = str(path)
    return res


def main():
    ap = argparse.ArgumentParser(description="Measure the rendered page at several widths.")
    ap.add_argument("target", help="URL or local HTML file")
    ap.add_argument("--widths", default="1280,768,390")
    ap.add_argument("--shots", help="directory for viewport screenshots, one per width")
    ap.add_argument("--full", action="store_true", help="full-page screenshots (capped at 8000px)")
    ap.add_argument("--min-font", type=float, default=12)
    ap.add_argument("--max", type=int, default=0, help="allowed P0+P1 findings before exit 1")
    ap.add_argument("--chrome")
    ap.add_argument("--inject-css", help="stylesheet added after load, to test a fix before deploying")
    ap.add_argument("--json", action="store_true")
    opts = ap.parse_args()

    url = opts.target if "://" in opts.target else Path(opts.target).resolve().as_uri()
    chrome = find_chrome(opts.chrome)
    if not chrome:
        print("No Chrome/Chromium found. Pass --chrome PATH or set CHROME. "
              "Without it, mark render-dependent fields unverified.")
        return 2
    try:
        proc, profile, ws = launch(chrome)
    except RuntimeError as e:
        print(f"cannot start {chrome}: {e}")
        return 2
    results = {}
    try:
        cdp = CDP(ws)
        cdp.call("Page.enable")
        cdp.call("Emulation.setFocusEmulationEnabled", enabled=True)
        cdp.call("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
        for i, w in enumerate(int(x) for x in opts.widths.split(",")):
            results[w] = audit(cdp, url, w, opts, i == 0)
    except (RuntimeError, ConnectionError, OSError) as e:
        print(f"render audit failed: {e}")
        return 2
    finally:
        proc.kill()
        shutil.rmtree(profile, ignore_errors=True)

    serious = len({(f["code"], f["sel"], f["text"]) for r in results.values() for f in r["findings"]
                   if f["sev"] in ("P0", "P1")})  # unique: the same defect at three widths counts once
    if opts.json:
        print(json.dumps({"url": url, "widths": results}, indent=2, ensure_ascii=False))
    else:
        print(f"render audit: {url}")
        order = {"P0": 0, "P1": 1, "P2": 2}
        key = lambda f: (f["code"], f["sel"], f["text"])  # noqa: E731
        sets = [{key(f) for f in r["findings"]} for r in results.values()]
        common = set.intersection(*sets) if len(sets) > 1 else set()

        def show(label, findings):
            groups = {}
            for f in findings:
                groups.setdefault((f["sev"], f["code"]), []).append(f)
            print(f"\n{label}" + ("" if groups else "  clean"))
            for (sev, code), fs in sorted(groups.items(), key=lambda kv: (order[kv[0][0]], -len(kv[1]))):
                print(f"  {sev} {code} x{len(fs)}")
                for f in fs[:3]:
                    label = f'{f["sel"]} "{f["text"]}"' if f["text"] else f["sel"]
                    print(f"       {label}  {f['detail']}")
                if len(fs) > 3:
                    print(f"       + {len(fs) - 3} more")

        if common:
            first = next(iter(results.values()))["findings"]
            show("all widths", [f for f in first if key(f) in common])
        for w, r in results.items():
            notes = ([f"{r['contrastSkipped']} text boxes over images: contrast not measured"]
                     if r["contrastSkipped"] else []) + ([f"shot: {r['shot']}"] if r.get("shot") else [])
            show(f"{w}px" + "".join(f"  [{n}]" for n in notes),
                 [f for f in r["findings"] if key(f) not in common])
        print(f"\nP0+P1 (unique): {serious}")
    return 1 if serious > opts.max else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""audit.py - the mechanical half of an audit. Stdlib only, Python 3.8+.

  audit.py scan  [ROOT]            source tells, a11y and browser-surface gaps, value inventory
  audit.py copy  [ROOT|FILE...]    prose and microcopy tells, sentence rhythm
  audit.py contrast FG BG          WCAG ratio of two CSS colours
  audit.py contrast --paper FILE   ink/accent x ground and on-accent x accent, per mode (-dark keys)
  audit.py score H L S C T U D     weighted score, band, work list (0-4 each, u = unverified)

--json on every subcommand; --skip a,b ignores folders by name (archives, demos) for scan and copy.
Exit: 0 nothing found, 1 findings, 2 bad input.
A finding is evidence of a default nobody chose, never proof of authorship.
"""

import importlib.util
import json
import os
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

_spec = importlib.util.spec_from_file_location("cd", Path(__file__).with_name("check-design.py"))
cd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cd)

SEV_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
JSON = "--json" in sys.argv


def I(rx):  # noqa: E743
    return re.compile(rx, re.I)


# ------------------------------------------------------------------ scan rules
# (id, severity, regex, fix, minimum hits before it counts). IDs match references/slop-catalog.md.
LINE_RULES = [
    ("C1", "P0", re.compile(r"\bfrom-(?:indigo|violet|purple|fuchsia)-\d+\b.*\bto-(?:purple|pink|violet|blue|indigo|fuchsia)-\d+"
                            r"|\bfrom-(?:blue|indigo)-\d+\b.*\bto-(?:purple|violet|fuchsia)-\d+"),
     "tonal gradient inside one brand hue, or a flat ground", 1),
    ("C3", "P0", cd.GRADIENT_TEXT_RE, "solid ink; let scale carry emphasis", 1),
    ("C5", "P1", re.compile(r"\bblur-(?:2xl|3xl)\b|\bblur-\[\d{2,}px\]|(?<![\w-])filter\s*:\s*blur\(\s*(?:[4-9]\d|\d{3,})px"),
     "earn the space with content, not blurred blobs", 1),
    ("S2", "P1", re.compile(r"--radius\s*:\s*0?\.(?:5|625)rem"), "a radius that says something", 1),
    ("S3", "P1", re.compile(r"border-(?:left|right)\s*:\s*(?:[2-9]|\d{2,})px\s+solid|\bborder-[lr]-(?:[2-8]|\[\d+px\])\b"),
     "drop the accent stripe; rank with weight, scale, position", 1),
    ("S4", "P1", re.compile(r"backdrop-filter\s*:\s*blur|\bbackdrop-blur"),
     "blur only where content really passes under", 3),
    ("S8", "P2", re.compile(r"box-shadow\s*:\s*-?[1-9]\d*px\s+-?[1-9]\d*px\s+0(?:px)?\s|\bshadow-\[-?\d+px_-?\d+px_0"),
     "hard offset shadows only inside a deliberate neobrutalist world", 1),
    ("K1", "P0", re.compile(r"--primary\s*:\s*(?:222\.2 47\.4% 11\.2%|240 5\.9% 10%|oklch\(0\.205 0 0\))"),
     "theme base colour, radius, button and card: the stock tokens are untouched", 1),
    ("K4", "P1", re.compile(r"<(?:Spotlight|BackgroundBeams\w*|ShimmerButton|NumberTicker|Meteors|BorderBeam|SparklesCore"
                            r"|AuroraBackground|TextGenerateEffect|LampContainer|MagicCard|AnimatedGradientText"
                            r"|RetroGrid|Particles|ShineBorder|TypingAnimation)\b"),
     "one effect that belongs here, or none", 1),
    ("K5", "P1", I(r"\bmost popular\b|\bbest value\b"), "structure follows the real offer", 1),
    ("K7", "P2", re.compile(r"\bbg-red-[345]00\b.*\bbg-(?:yellow|amber)-[345]00\b.*\bbg-green-[345]00\b"),
     "a real screenshot instead of fake window chrome", 1),
    ("I1", "P1", re.compile("✨|<Sparkles\\b"), "use words: sparkles do not read as 'AI' to users", 1),
    ("I4", "P1", I(r"dicebear|pravatar|picsum\.photos|placehold\.co|via\.placeholder|placeholder\.com|randomuser\.me|unsplash\.it"),
     "real avatars and screenshots, or remove the slot", 1),
    ("M3", "P2", I(r"\b(?:animate-bounce|ease-?(?:out|in)?-?(?:back|elastic|bounce))\b|\bspring\b.*\bbounce\s*:"),
     "ease out without overshoot, 150-250 ms", 1),
    ("M4", "P2", re.compile(r"\b(?:CountUp|NumberTicker|useCountUp|react-countup|countup\.js)\b"), "show the real number", 1),
    ("M6", "P2", re.compile(r"\bhover:(?:scale-\d+|-translate-y-\d+)|:hover[^{]*\{[^}]*transform\s*:\s*(?:scale|translateY\(-)"),
     "one shared motion language; nothing moves more than a few px on hover", 3),
    ("M7", "P2", re.compile(r"\bease-linear\b|transition(?:-timing-function)?\s*:[^;]*\blinear\b"),
     "never linear for UI: ease-out arriving, ease-in leaving", 1),
    ("M8", "P2", re.compile(r"transition\s*:\s*all\b|\btransition-all\b"), "name the properties", 1),
    ("M9", "P2", re.compile(r"transition(?:-property)?\s*:[^;]*\b(?:width|height|top|left|right|bottom|margin|padding)\b"),
     "animate transform and opacity, never layout properties", 1),
    ("M10", "P2", re.compile(r"\banimate-(?:pulse|ping)\b|animation\s*:[^;]*\binfinite\b"),
     "loop only what is live", 2),
    ("T3", "P1", re.compile(r"\buppercase\b[^\"'`]*\btracking-(?:wide|wider|widest|\[)|\btracking-(?:wide|wider|widest|\[)[^\"'`]*\buppercase\b"),
     "keep a tracked all-caps label only where it carries information", 3),
    ("T8", "P2", I(r"fonts\.googleapis\.com|fonts\.gstatic\.com|use\.typekit\.net|fonts\.bunny\.net"),
     "self-host the font files", 1),
    ("L3", "P1", re.compile(r">\s*(?:\d+(?:[.,]\d+)?[kKmM]\+|\d{2,3},000\+|\d{2,4}\+|99(?:\.9+)?%|100%|24/7)\s*<"),
     "real numbers with a source, or cut the strip", 3),
    ("L4", "P1", re.compile(r">\s*0[1-9]\s*[./]?\s*<|['\"]0[1-9]['\"]"), "number only real sequences", 3),
    ("F1", "P1", I(r"lovable-tagger|gptengineer|v0\.dev|bolt\.new|<meta[^>]+name=[\"']generator"),
     "remove the builder signature before shipping", 1),
    ("A2", "P1", re.compile(r"<(?:img|Image)\b(?![^>]*\balt=)[^>]*>"), "every image gets alt text (empty alt for decoration)", 1),
    ("A4", "P1", I(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?\b"), "never disable zoom", 1),
]
FOCUS_RE = re.compile(r":focus-visible|\bfocus-visible:|:focus\b|\bfocus:(?:ring|outline|border|shadow)")
OUTLINE_KILL_RE = re.compile(r"outline\s*:\s*(?:none|0)\b|\boutline-none\b")
INTERACTIVE_RE = re.compile(r"<(?:button|a\s|input|select|textarea|Button|Link)\b")
SURFACES = [
    ("selection colour", re.compile(r"::selection|\bselection:")),
    ("caret", re.compile(r"caret-color|\bcaret-[a-z]")),
    ("scrollbar", re.compile(r"scrollbar-(?:color|width|gutter)|::-webkit-scrollbar")),
    ("underline offset", re.compile(r"text-underline-offset|\bunderline-offset-")),
    ("tabular figures", re.compile(r"tabular-nums")),
    ("balanced headings", re.compile(r"text-wrap\s*:\s*(?:balance|pretty)|\btext-(?:balance|pretty)\b")),
]
LUCIDE_WORN = {"Zap", "Rocket", "Shield", "BarChart3", "ArrowRight", "CheckCircle2", "Sparkles", "Star"}
SERIF = {"fraunces", "instrument serif", "newsreader", "playfair display", "lora", "merriweather",
         "eb garamond", "cormorant", "cormorant garamond", "libre baskerville", "dm serif display",
         "dm serif text", "source serif 4", "source serif pro", "crimson pro", "crimson text",
         "spectral", "georgia", "pt serif", "noto serif", "literata", "bodoni moda", "young serif"}
DEFAULT_FACES = {"inter", "roboto", "arial", "helvetica", "helvetica neue", "system-ui"}
TASTEFUL_FREE = {"space grotesk", "geist", "syne", "sora", "instrument serif", "fraunces",
                 "cal sans", "plus jakarta sans", "plus jakarta"}
FONT_LOAD_RE = re.compile(
    r"@font-face[^}]*font-family\s*:\s*['\"]?([^;'\"}]+)"
    r"|from\s+['\"]next/font/(?:google|local)['\"]"
    r"|@fontsource(?:-variable)?/([\w-]+)"
    r"|family=([\w+]+)")
NEXT_FONT_RE = re.compile(r"import\s*\{([^}]+)\}\s*from\s*['\"]next/font/google['\"]")
BG_RE = re.compile(r"(?:background(?:-color)?|--(?:background|bg|ground|surface)[\w-]*)\s*:\s*([^;}\n]+)")


def hue_in(h, lo, hi):
    return lo <= h <= hi if lo <= hi else (h >= lo or h <= hi)


def new_report():
    return defaultdict(lambda: {"sev": None, "fix": "", "hits": []})


def hit(rep, rid, sev, fix, where):
    r = rep[rid]
    r["sev"], r["fix"] = sev, fix
    r["hits"].append(where)


def scan(root):
    rep, minimum = new_report(), {}
    records, n_files, anim, gated = cd.extract(root)
    paper = cd.find_paper(root)
    tokens = cd.parse_tokens(paper.read_text(encoding="utf-8", errors="replace")) if paper else None
    declared = bool(tokens)
    blob_parts, loaded, used_fonts, bg_colors, sizes, durations = [], set(), Counter(), Counter(), Counter(), Counter()
    lucide = set()

    for path in cd.iter_sources(root):
        text = cd.read_clean(path)
        rel = path.relative_to(root).as_posix()
        blob_parts.append(text)
        lines = text.splitlines()
        for rid, sev, rx, fix, mn in LINE_RULES:
            minimum[rid] = mn
            for i, line in enumerate(lines, 1):
                m = rx.search(line)
                if m:
                    hit(rep, rid, sev, fix, f"{rel}:{i}  {m.group(0)[:50]}")
        for m in FONT_LOAD_RE.finditer(text):
            name = (m.group(1) or m.group(2) or m.group(3) or "").replace("+", " ").replace("-", " ")
            if name:
                loaded.add(name.strip().lower())
        for m in NEXT_FONT_RE.finditer(text):
            loaded.update(n.strip().split(" as ")[0].replace("_", " ").lower() for n in m.group(1).split(","))
        for m in re.finditer(r"import\s*\{([^}]+)\}\s*from\s*['\"]lucide-react['\"]", text):
            lucide.update(n.strip().split(" as ")[0] for n in m.group(1).split(","))
        for m in BG_RE.finditer(text):
            for c in cd.COLOR_RE.findall(m.group(1)):
                col = cd.parse_color(c)
                if col and col[3] == 1:
                    bg_colors[cd.to_hex(col)] += 1
        for m in re.finditer(r"(?<![\w-])font-size\s*:\s*([\d.]+(?:px|rem))|\btext-\[([\d.]+(?:px|rem))\]", text):
            sizes[m.group(1) or m.group(2)] += 1
        for m in re.finditer(r"(?:transition|animation)(?:-duration)?\s*:[^;}\n]*?(\d*\.?\d+m?s)\b|\bduration-(\d+)\b", text):
            durations[m.group(1) or m.group(2) + "ms"] += 1
        # C1 in CSS: a gradient whose chromatic stops all sit in the violet-blue-pink band
        for m in re.finditer(r"(?:linear|radial|conic)-gradient\(([^;]*)", text):
            stops = [cd.oklch(c) for c in map(cd.parse_color, cd.COLOR_RE.findall(m.group(1))) if c]
            chroma = [s for s in stops if s[1] >= 0.08]
            if len(chroma) >= 2 and all(hue_in(s[2], 220, 350) for s in chroma) \
                    and any(hue_in(s[2], 265, 330) for s in chroma):
                line = text.count("\n", 0, m.start()) + 1
                hit(rep, "C1", "P0", "tonal gradient inside one brand hue, or a flat ground",
                    f"{rel}:{line}  {m.group(0)[:50]}")
        if re.search(r"mousemove", text) and re.search(r"radial-gradient", text):
            hit(rep, "M5", "P2", "cut the cursor-following glow", rel)

    blob = "\n".join(blob_parts)
    for r in records:
        if r["kind"] == "font":
            used_fonts[r["raw"]] += 1
        elif r["kind"] == "emoji":
            hit(rep, "I3", "P1", "a real icon set, or nothing", f"{r['file']}:{r['line']}  {r['raw']}")
    worn = lucide & LUCIDE_WORN
    if len(worn) >= 3:
        hit(rep, "I2", "P1", "icons for meaning, not availability", "lucide-react: " + ", ".join(sorted(worn)))
    if anim and not gated:
        hit(rep, "M2", "P1", "gate it: @media (prefers-reduced-motion: reduce)", ", ".join(sorted(anim)[:3]))
    if INTERACTIVE_RE.search(blob):
        if not FOCUS_RE.search(blob):
            hit(rep, "K3", "P1", "hover, focus-visible, active, disabled on every control", "no focus style anywhere")
        elif OUTLINE_KILL_RE.search(blob) and ":focus-visible" not in blob and "focus-visible:" not in blob:
            hit(rep, "K3", "P1", "replace the removed outline with a :focus-visible ring", "outline removed, no :focus-visible")
    if re.search(r"<html\b", blob) and not re.search(r"<html\b[^>]*\blang=", blob):
        hit(rep, "A3", "P2", "set lang on <html>: screen readers and hyphens: auto depend on it", "<html> without lang")
    missing = [name for name, rx in SURFACES if not rx.search(blob)]
    if n_files and len(missing) >= 2:
        hit(rep, "B1", "P2", "design the browser surfaces; defaults belong to no system",
            "left at browser default: " + ", ".join(missing))

    # Face and palette tells only apply to undeclared choices: a paper turns them into decisions.
    faces = set(used_fonts) | {f for f in loaded if f}
    if not declared:
        if not faces or faces <= DEFAULT_FACES:
            hit(rep, "T1", "P1", "choose faces for the brief, or state in the paper why the default stays",
                "faces: " + (", ".join(sorted(faces)) or "browser default"))
        for f in sorted(faces & TASTEFUL_FREE):
            hit(rep, "T2", "P1", "keep only if earned; never the face of your last three projects", f)
        palette = [cd.parse_color(h) for h, _ in Counter(
            cd.to_hex(r["val"]) for r in records if r["kind"] == "color").most_common(12)]
        accents = [cd.oklch(c) for c in palette if cd.oklch(c)[1] >= 0.1]
        grounds = [cd.oklch(cd.parse_color(h)) for h, _ in bg_colors.most_common(1)]
        serif = bool(faces & SERIF) or bool(re.search(r"font-family\s*:[^;]*(?<!sans-)\bserif\b", blob))
        acc, gr = (accents[0] if accents else None), (grounds[0] if grounds else None)
        if acc:
            if hue_in(acc[2], 270, 320):
                hit(rep, "C2", "P1", "tie the primary to the brand, not the default violet", "accent hue %.0f" % acc[2])
            if hue_in(acc[2], 160, 200):
                hit(rep, "SD3", "P2", "teal/emerald is still the purple-avoiding default", "accent hue %.0f" % acc[2])
            if hue_in(acc[2], 40, 70) and serif:
                hit(rep, "SD6", "P2", "orange + serif is the 'I avoided purple' signature", "accent hue %.0f + serif" % acc[2])
        if acc and gr:
            if gr[0] >= 0.93 and 0.008 <= gr[1] <= 0.045 and hue_in(gr[2], 50, 105) \
                    and hue_in(acc[2], 25, 60) and serif:
                hit(rep, "SD1", "P1", "cream + terracotta + serif is the tasteful default; derive from the subject",
                    "ground L%.2f, accent hue %.0f, serif" % (gr[0], acc[2]))
            if gr[0] <= 0.2 and acc[1] >= 0.15 and (hue_in(acc[2], 110, 150) or hue_in(acc[2], 20, 40)):
                hit(rep, "SD2", "P1", "near-black + acid accent is the serious-tech default",
                    "ground L%.2f, accent hue %.0f" % (gr[0], acc[2]))

    for rid in list(rep):
        if len(rep[rid]["hits"]) < minimum.get(rid, 1):
            del rep[rid]

    inv = {
        "files": n_files,
        "colors": Counter(cd.to_hex(r["val"]) for r in records if r["kind"] == "color").most_common(10),
        "distinct_colors": len({cd.to_hex(r["val"]) for r in records if r["kind"] == "color"}),
        "radius_px": sorted({r["val"] for r in records if r["kind"] == "radius"}),
        "spacing_px": sorted({r["val"] for r in records if r["kind"] == "spacing"}),
        "off_4px_grid": sorted({r["val"] for r in records if r["kind"] == "spacing" and r["val"] % 4 and r["val"] > 2}),
        "fonts": used_fonts.most_common(6),
        "fonts_loaded": sorted(loaded),
        "font_sizes": [s for s, _ in sizes.most_common(12)],
        "durations": [d for d, _ in durations.most_common(8)],
        "paper_tokens": declared,
    }
    unloaded = sorted(f for f in used_fonts if f not in GENERIC_SAFE and not any(f in l or l in f for l in loaded))
    if unloaded and n_files:
        hit(rep, "T6", "P1", "ship the font files, or drop the declaration (check loaders this scan cannot see)",
            "declared, no loader found: " + ", ".join(unloaded[:4]))
    return rep, inv


GENERIC_SAFE = cd.GENERIC_FONTS | {"inter var"}


# ------------------------------------------------------------------ copy rules
HYPE = I(r"\b(?:supercharg\w*|seamless(?:ly)?|unlock\w*|magic(?:al)?|revolutioni[sz]\w*|game[- ]?chang\w*|ai[- ]powered"
         r"|cutting[- ]edge|next[- ]gen(?:eration)?|world[- ]class|best[- ]in[- ]class|empower\w*|elevate\w*"
         r"|effortless(?:ly)?|unleash\w*|synerg\w*|holistic|streamlin\w*|transformative"
         r"|nahtlos\w*|revolution\w*|bahnbrechend\w*|ganzheitlich\w*|ma(?:ß|ss)geschneidert\w*"
         r"|zukunftssicher\w*|spielend leicht|m[üu]helos\w*|leistungsstark\w*|erstklassig\w*)\b")
AI_VOCAB = I(r"\b(?:additionally|align(?:s|ed)? with|boasts?|bolster\w*|crucial|deep dive|delve\w*|emphasi[sz]ing|enduring"
             r"|enhanc\w*|foster\w*|garner\w*|highlighting|interplay|intricate|landscape|meticulous\w*|pivotal|robust"
             r"|showcas\w*|tapestry|testament|underscor\w*|vibrant|multifaceted|nestled|realm|myriad|leverag\w*"
             r"|navigat\w* the|ever-evolving|in today's)\b")
COPY_RULES = [
    # (id, sev, regex, fix, scope) scope: any | heading | ui (ui + headings) | short (ui, headings, text <= 12 words)
    ("W16", "P0", I(r"\b(?:I hope this helps|Certainly!|as an AI(?: language model)?|here'?s (?:a|the) (?:revised|updated) version"
                   r"|I'?d be happy to|great question|ich hoffe,? das hilft)"), "unshipped work: delete it", "any"),
    ("W17", "P0", I(r"\[(?:your|insert|company|name|todo|placeholder|number needed|source needed)[^\]]*\]|\bINSERT_[A-Z_]+\b"
                   r"|\b20\d\d-XX-XX\b|\blorem ipsum\b"), "fill the gap with a real, sourced fact or cut the sentence", "any"),
    ("W4", "P1", I(r"\b(?:it'?s|this is|we'?re) not (?:just|only|merely) [^.;!?]{1,50}[,;:—-]\s*(?:it'?s|but|we'?re)\b"
                   r"|\bnot (?:just|only) (?:a|an) \w+(?: \w+)?[,;—-]+\s*(?:but )?(?:a|an) \w+"), "say the one true thing once", "any"),
    ("W10", "P2", I(r"\b(?:serves as|stands as|acts as a|represents a|boasts an?|functions as)\b"), "plain 'is' / 'has'", "any"),
    ("W11", "P1", I(r"\b(?:pivotal (?:moment|role)|(?:is )?a testament to|cornerstone of|plays? a (?:crucial|vital|key|pivotal) role"
                   r"|reflects broader|in today'?s (?:fast-paced|digital|ever-changing|modern))"), "evidence instead of importance", "any"),
    ("W12", "P1", I(r"\b(?:experts (?:say|argue|agree|believe)|studies (?:show|suggest)|research (?:shows|suggests)"
                   r"|industry reports|many believe)\b"), "name the source or cut the claim", "any"),
    ("W13", "P1", I(r"\bdespite (?:these|its|the|their) challenges\b"), "drop the formula; state the actual difficulty", "any"),
    ("W14", "P1", I(r"\b(?:in a world where|whether you'?re an? |in this (?:article|post|guide),? we(?:'ll| will)"
                   r"|in today'?s (?:world|landscape))"), "start with the point", "any"),
    ("W15", "P1", I(r"^(?:in conclusion|in summary|conclusion|fazit|zusammenfassung)\b"), "end on the last real point", "heading"),
    ("W1", "P1", I(r"^(?:elevate|supercharge|unlock|transform|empower|revolutioni[sz]e|reimagine|unleash) your\b"
                   r"|\bthe all-in-one (?:platform|solution)\b"), "what it does, for whom, what changes", "heading"),
    ("W5", "P2", I(r"^(?:learn more|get started|click here|read more|submit|discover more|mehr erfahren|jetzt starten"
                   r"|hier klicken|absenden|weiterlesen)$"), "verb + object, consistent across the page", "button"),
    ("W6", "P2", re.compile(r"!(?![=\w])"), "no exclamation marks in interface text", "short"),
    ("W8", "P2", I(r"^(?:welcome back|hey there|hi there|hello there|willkommen zur[üu]ck)\b"),
     "the title names the context or period, not a greeting", "heading"),
    ("W9", "P2", re.compile(r"^[^.]{1,60}[^.]\.$"), "no trailing period on headings, labels, buttons", "ui"),
    ("W7", "P2", I(r"\b(?:john doe|jane doe|max mustermann|erika mustermann|example@example\.\w+|foo@bar|acme (?:inc|corp)"
                   r"|123[,.]456)\b"), "mock data that looks real", "any"),
    ("I3", "P1", cd.EMOJI_RE, "no emoji in headings", "heading"),
]
TEXT_NODE_RE = re.compile(r"<([A-Za-z][\w.]*)\b(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>([^<>{}]*[A-Za-zÄÖÜäöüß][^<>{}]*)(?=<)")
ATTR_TEXT_RE = re.compile(r"\b(?:placeholder|aria-label|title|alt|label)=[\"']([^\"'{}]{2,})[\"']")
STRING_RE = re.compile(r"([\"'`])((?:(?!\1)[^\n{}<>\\]){6,})\1")
UI_TAGS = {"button", "a", "label", "Button", "Link", "option", "th", "summary", "legend"}
TEXT_EXT = {".md", ".mdx", ".txt"}


def looks_like_code(s):
    toks = s.split()
    if len(toks) < 2 or re.search(r"[=;{}\\]|https?://|\w/\w|\.\w+\(|^use (?:client|server|strict)$", s):
        return True
    return s == s.lower() and sum(bool(re.search(r"[-:\[\]/]", t)) for t in toks) >= max(2, len(toks) / 2)


def units(path, root):
    """(where, text, kind) for every piece of copy in a file. kind: heading | ui | text."""
    rel = path.relative_to(root).as_posix() if root in path.parents or path == root else str(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in TEXT_EXT:
        raw = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
        for i, line in enumerate(raw.splitlines(), 1):
            line = re.sub(r"`[^`]*`|\]\([^)]*\)", "", line).strip()
            if not line or line.startswith(("|", "<!--", "---")):
                continue
            h = re.match(r"#{1,6}\s+(.*)", line)
            yield (f"{rel}:{i}", h.group(1) if h else re.sub(r"^[-*>\d.]+\s+", "", line), "heading" if h else "text")
        return
    text = cd.read_clean(path)
    line_of = lambda pos: text.count("\n", 0, pos) + 1  # noqa: E731
    seen = set()
    for m in TEXT_NODE_RE.finditer(text):
        t = " ".join(m.group(2).split())
        if not t or looks_like_code(t) and len(t.split()) > 2 and not re.search(r"[.!?]$", t):
            continue
        tag = m.group(1)
        kind = "heading" if re.fullmatch(r"h[1-6]", tag) else "ui" if tag in UI_TAGS or len(t.split()) <= 4 else "text"
        seen.add(t)
        yield (f"{rel}:{line_of(m.start(2))}", t, kind)
    for rx, kind in ((ATTR_TEXT_RE, "ui"), (STRING_RE, "text")):
        for m in rx.finditer(text):
            t = " ".join(m.group(m.lastindex).split())
            code = re.search(r"https?://|[{}=;]", t) if kind == "ui" else looks_like_code(t)
            if t not in seen and not code and re.search(r"[a-zäöü]{2,}", t, re.I):
                seen.add(t)
                yield (f"{rel}:{line_of(m.start(m.lastindex))}", t, kind)


def is_title_case(t):
    words = re.findall(r"[A-Za-z][\w'-]*", t)
    long_words = [w for w in words if len(w) > 3]
    return len(words) >= 3 and len(long_words) >= 2 and all(w[0].isupper() for w in long_words)


def copy(targets, root):
    rep = new_report()
    prose, md_lines, headings = [], [], []
    files = []
    for t in targets:
        p = Path(t).resolve()
        files += [p] if p.is_file() else list(cd.iter_sources(p, cd.SOURCE_EXT | TEXT_EXT))
    for path in files:
        if path.suffix.lower() not in cd.SOURCE_EXT | TEXT_EXT:
            continue
        for where, t, kind in units(path, root):
            scopes = {"any", kind, "short"} if kind != "text" or len(t.split()) <= 12 else {"any"}
            scopes |= {"ui"} if kind in ("ui", "heading") else set()
            for rid, sev, rx, fix, scope in COPY_RULES:
                if (scope in scopes or scope == "button" and kind == "ui") and rx.search(t):
                    hit(rep, rid, sev, fix, f"{where}  {t[:60]}")
            for m in HYPE.finditer(t):
                hit(rep, "W2", "P2", "a number, a verb, or a disputable claim", f"{where}  {m.group(0)}")
            if kind == "heading":
                headings.append((where, t))
            if kind == "text" and len(t.split()) >= 6:
                prose.append(t)
        if path.suffix.lower() in TEXT_EXT:
            md_lines += path.read_text(encoding="utf-8", errors="replace").splitlines()

    tc = [(w, t) for w, t in headings if is_title_case(t)]
    if len(tc) >= 3 and not looks_german(" ".join(prose)):
        for w, t in tc:
            hit(rep, "T7", "P2", "sentence case", f"{w}  {t[:50]}")
    qs = [(w, t) for w, t in headings if t.rstrip().endswith("?")]
    if len(qs) >= 2:
        for w, t in qs:
            hit(rep, "W19", "P2", "headings state, they do not ask", f"{w}  {t[:50]}")
    inline_hdr = [l for l in md_lines if re.match(r"\s*[-*]\s+\*\*[^*]+:\*\*", l)]
    if len(inline_hdr) >= 4:
        hit(rep, "W18", "P1", "write the list as sentences or a table", f"{len(inline_hdr)} '**Label:** text' bullets")

    body = " ".join(prose)
    words = re.findall(r"[A-Za-zÀ-ÿ']+", body)
    vocab = AI_VOCAB.findall(body)
    if len(vocab) >= 3 and len(vocab) * 1000 / max(len(words), 1) >= 4:
        hit(rep, "W3", "P1", "plain words; restore the specific thing that was flattened",
            f"{len(vocab)} hits / {len(words)} words: " + ", ".join(sorted(set(v.lower() for v in vocab))[:8]))
    sents = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", body) if len(s.split()) >= 2]
    if len(sents) >= 8:
        mean = statistics.mean(sents)
        var = statistics.pstdev(sents) / mean if mean else 0
        if var < 0.42 and min(sents) >= 8:
            hit(rep, "W20", "P1", "uneven rhythm: a four-word sentence beside a thirty-word one",
                f"{len(sents)} sentences, variation {var:.0%}, shortest {min(sents)} words")
    if len(words) >= 300:
        marks = re.findall(r"[,.;:?!()—–]", body)
        other = [c for c in marks if c not in ",."]
        if marks and len(other) / len(marks) < 0.06:
            hit(rep, "W21", "P2", "vary the punctuation: a colon, a question, a parenthesis",
                f"{len(other) / len(marks):.0%} of marks are not comma or period")
        dashes = body.count(" — ")
        if dashes * 1000 / len(words) >= 5:
            hit(rep, "W22", "P2", "fewer spaced em dashes", f"{dashes} in {len(words)} words")
    return rep, {"files": len(files), "words": len(words), "sentences": len(sents)}


def looks_german(s):
    w = re.findall(r"\b(?:und|der|die|das|nicht|mit|f[üu]r|ist|wir|sie)\b", s, re.I)
    return len(w) >= 5


# ------------------------------------------------------------------ output
def emit(rep, meta, title):
    items = sorted(rep.items(), key=lambda kv: (SEV_ORDER[kv[1]["sev"]], -len(kv[1]["hits"])))
    cluster = [k for k, v in items if v["sev"] in ("P0", "P1")]
    verdict = ("cluster: act on it" if len(cluster) >= 3 else
               "traces: below the density threshold, report P0s only" if items else "clean")
    if JSON:
        print(json.dumps({"verdict": verdict, "meta": meta,
                          "findings": [{"id": k, "severity": v["sev"], "count": len(v["hits"]),
                                        "fix": v["fix"], "hits": v["hits"][:20]} for k, v in items]},
                         indent=2, ensure_ascii=False))
        return 1 if items else 0
    print(f"{title}: {verdict} ({len(cluster)} distinct P0/P1 tells)")
    for k, v in items:
        print(f"  {v['sev']} {k} x{len(v['hits'])}  -> {v['fix']}")
        for h in v["hits"][:3]:
            print(f"       {h}")
        if len(v["hits"]) > 3:
            print(f"       + {len(v['hits']) - 3} more")
    for k, val in meta.items():
        print(f"  {k}: {val}")
    return 1 if items else 0


def cmd_contrast(args):
    if args[:1] == ["--paper"]:
        tokens = cd.parse_tokens(Path(args[1]).read_text(encoding="utf-8")) or {}
        pairs, seen = [], set()
        for mode in ("", "-dark"):  # pair colours within one mode only
            grounds = tokens.get("ground" + mode, [])
            fgs = [("ink" + mode, c) for c in tokens.get("ink" + mode, [])] + \
                  [("accent" + mode, c) for c in tokens.get("accent" + mode, [])]
            if not mode and not grounds:  # no roles declared: every pair, informational
                grounds = tokens.get("color", [])
                fgs = [("color", c) for c in tokens.get("color", []) + tokens.get("accent", [])]
            fgs += [("on-accent" + mode, f) for f in tokens.get("on-accent" + mode, [])]
            for role, f in fgs:
                for g in (tokens.get("accent" + mode, []) if role.startswith("on-accent") else grounds):
                    if f != g and frozenset((f, g)) not in seen:  # ratio is symmetric
                        seen.add(frozenset((f, g)))
                        pairs.append((role, f, g))
        if not pairs:
            print("no pairs in the token block (keys: ground, ink, accent, on-accent; -dark variants)")
            return 2
    elif len(args) >= 2:
        pairs = [("", args[0], args[1])]
    else:
        print(__doc__)
        return 2
    rows, bad = [], 0
    for role, f, g in pairs:
        fc, gc = cd.parse_color(f), cd.parse_color(g)
        if not fc or not gc:
            print(f"cannot parse {f} or {g}")
            return 2
        r = cd.contrast(fc, gc)
        verdict = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA large/UI only" if r >= 3 else "FAIL"
        bad += r < 4.5 and role != "color"
        rows.append({"role": role, "fg": f, "bg": g, "ratio": round(r, 2), "verdict": verdict})
    if JSON:
        print(json.dumps(rows, indent=2))
    else:
        for x in sorted(rows, key=lambda x: x["ratio"]):
            print(f"  {x['ratio']:>5.2f}:1  {x['verdict']:<16} {x['role']:<9} {x['fg']} on {x['bg']}")
        print("  body text needs 4.5:1; large text (>=24px, >=18.7px bold) and UI boundaries 3:1. "
              "Accent as text and text on accent are separate checks.")
    return 1 if bad else 0


FIELDS = [("Hierarchy", 3), ("Legibility", 3), ("System", 2), ("Craft", 2),
          ("Content truth", 3), ("Usability", 3), ("Distinction", 2)]
BANDS = [(85, "Strong", "ship; fix P0 only"), (70, "Sound", "ship after the named P1s"),
         (50, "Weak", "a real pass before shipping"), (0, "Failing", "the direction is wrong: rebuild, don't polish")]


def cmd_score(args):
    if len(args) != 7 or any(a not in "01234u" or len(a) != 1 for a in args):
        print("usage: audit.py score H L S C T U D   (each 0-4, or u for unverified)")
        return 2
    vals = [0 if a == "u" else int(a) for a in args]
    total = round(sum(v * w for v, (_, w) in zip(vals, FIELDS)) / 72 * 100)
    band = next(b for b in BANDS if total >= b[0])
    worst = sorted(range(7), key=lambda i: (vals[i], -FIELDS[i][1]))[:3]
    out = {"score": total, "band": band[1], "action": band[2],
           "fields": {FIELDS[i][0]: ("unverified" if args[i] == "u" else vals[i]) for i in range(7)},
           "work_list": [FIELDS[i][0] for i in worst]}
    if JSON:
        print(json.dumps(out, indent=2))
    else:
        print(f"{total}/100  {band[1]}: {band[2]}")
        print("  " + "  ".join(f"{FIELDS[i][0]} {args[i]}" for i in range(7)))
        print("  work list: " + ", ".join(f"{FIELDS[i][0]} ({args[i]})" for i in worst))
    return 0


def main():
    args, skip = [], False
    for a in sys.argv[1:]:
        if skip:
            cd.EXTRA_SKIP.update(filter(None, a.split(",")))
            skip = False
        elif a == "--skip":
            skip = True
        elif a != "--json":
            args.append(a)
    if not args or args[0] not in ("scan", "copy", "contrast", "score"):
        print(__doc__)
        return 2
    cmd, rest = args[0], args[1:]
    if cmd == "contrast":
        return cmd_contrast(rest)
    if cmd == "score":
        return cmd_score(rest)
    root = Path(rest[0] if rest else ".").resolve()
    if not root.exists():
        print(f"no such path: {root}")
        return 2
    paths = [Path(p).resolve() for p in rest or ["."]]
    base = root if cmd == "scan" else Path(os.path.commonpath([p if p.is_dir() else p.parent for p in paths]))
    paper = cd.find_paper(base) or cd.find_paper(base.parent)
    tokens = (cd.parse_tokens(paper.read_text(encoding="utf-8")) or {}) if paper else {}
    cd.EXTRA_SKIP.update(tokens.get("skip", []))
    rep, meta = scan(root) if cmd == "scan" else copy([str(p) for p in paths], base)
    for rid in tokens.get("allow", []):
        rep.pop(rid, None)  # the paper decided this on purpose
    return emit(rep, meta, cmd)


if __name__ == "__main__":
    sys.exit(main())

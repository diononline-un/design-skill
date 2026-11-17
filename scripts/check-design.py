#!/usr/bin/env python3
"""
check-design.py — report drift between the source tree and DESIGN.md.

Reads the machine-checkable token block from DESIGN.md, then greps the source
tree for design values that are not in it.

Deliberately narrow. It checks what is mechanically checkable and stays silent
about taste. A checker that cries wolf gets disabled in a week.

Dependency-free (stdlib only). Python 3.8+.

Usage:
    python3 scripts/check-design.py [--root DIR] [--json] [--quiet]
    python3 scripts/check-design.py --init    # print the DESIGN.md token block

Exit codes: 0 clean, 1 findings, 2 cannot check (no paper / no token block),
           3 bad usage.

Token block format in DESIGN.md — a fenced yaml-ish block marked:

    <!-- TOKENS
    color: #14161A #F7F7F5 #8C5A3C #EDEDED
    radius: 0 4 8 12 14 9999
    spacing: 0 2 4 8 12 16 24 32 48 64 96 128
    fonts: Inter "Instrument Serif" "Space Grotesk"
    accent: #8C5A3C
    -->

Values are whitespace-separated. Quotes allowed for font names with spaces.
Comments with # begin a token on their own line only — colours inside the line
are kept as-is (a hex starts with #, so per-line comments use //).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

SOURCE_EXT = {".css", ".scss", ".sass", ".less", ".html", ".htm",
              ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
SKIP_DIRS = {"node_modules", ".git", ".next", "dist", "build", ".svelte-kit",
             ".nuxt", "vendor", "coverage", ".turbo", "out", ".cache",
             "public/assets", "public/build"}

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RADIUS_RE = re.compile(r"border-radius\s*:\s*([^;}\n]+)")
SPACING_RE = re.compile(
    r"(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|right|bottom|left|inline|block))?"
    r"\s*:\s*([^;}\n]+)")
FONT_RE = re.compile(r"font-family\s*:\s*([^;}\n]+)")
GRADIENT_TEXT_RE = re.compile(r"background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text")
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
ANIM_RE = re.compile(r"@keyframes|animation\s*:")
RM_RE = re.compile(r"prefers-reduced-motion")

# values that are never drift
IGNORE_VALUES = {"0", "auto", "inherit", "initial", "unset", "none", "revert",
                 "revert-layer", "100%", "50%", "9999px", "999px", "transparent",
                 "currentColor", "currentcolor", "1em", "0.5em"}

# Generic font families and system stacks are correct by definition: a fallback
# is not a brand decision, it's what keeps text on screen when the webfont fails.
GENERIC_FONTS = {
    "serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
    "-apple-system", "blinkmacsystemfont", "segoe ui", "roboto", "helvetica",
    "helvetica neue", "arial", "georgia", "times new roman", "times",
    "courier new", "ui-sans-serif", "ui-serif", "ui-monospace", "ui-rounded",
    "menlo", "monaco", "consolas", "sf mono", "dejavu sans", "liberation sans",
    "noto sans", "emoji", "apple color emoji", "segoe ui emoji",
}
NAMED_COLORS_OK = True  # we only flag hex literals, not named colours


def find_paper(root: Path):
    for candidate in (root / "DESIGN.md", root / "docs" / "DESIGN.md",
                      root / "design.md", root / "DESIGN.MD"):
        if candidate.is_file():
            return candidate
    return None


def parse_tokens(paper: Path):
    text = paper.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<!--\s*TOKENS(.*?)-->", text, re.S)
    if not m:
        return None
    block = m.group(1)
    tokens = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        key, _, rest = line.partition(":")
        if not rest:
            continue
        key = key.strip().lower()
        rest = re.sub(r"//.*$", "", rest).strip()
        parts = re.findall(r'"[^"]*"|\'[^\']*\'|\S+', rest)
        tokens[key] = [p.strip("\"'") for p in parts]
    return tokens or None


def norm_hex(h: str) -> str:
    h = h.lower()
    if len(h) in (4, 5):  # #abc -> #aabbcc
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


def numbers_in(value: str):
    """Yield (raw, numeric_or_None) for each length token in a CSS value."""
    for part in re.split(r"\s+", value.strip()):
        part = part.strip("()")
        if not part:
            continue
        m = re.fullmatch(r"(-?\d*\.?\d+)(px|rem|em|%|)", part)
        if m:
            yield part, float(m.group(1)), m.group(2)
        else:
            yield part, None, None


def iter_sources(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root).as_posix()
        dirnames[:] = [d for d in dirnames
                       if d not in SKIP_DIRS and not d.startswith(".")
                       and f"{rel}/{d}".lstrip("./") not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in SOURCE_EXT:
                yield p


def check(root: Path, tokens: dict):
    findings = []
    palette = {norm_hex(v) for v in tokens.get("color", []) + tokens.get("accent", [])
               if v.startswith("#")}
    radii = set()
    for v in tokens.get("radius", []):
        for raw, num, _ in numbers_in(v):
            if num is not None:
                radii.add(num)
    spacings = set()
    for v in tokens.get("spacing", []):
        for raw, num, _ in numbers_in(v):
            if num is not None:
                spacings.add(num)
    fonts = {f.lower().strip("\"'") for f in tokens.get("fonts", [])}

    files = list(iter_sources(root))
    anim_files, rm_files = set(), set()

    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        lines = text.splitlines()

        if ANIM_RE.search(text):
            anim_files.add(rel)
        if RM_RE.search(text):
            rm_files.add(rel)

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                continue

            # 1. hex outside palette
            if palette:
                for h in HEX_RE.findall(line):
                    if norm_hex(h) not in palette:
                        findings.append({
                            "rule": "hex-outside-palette", "severity": "P1",
                            "file": rel, "line": i, "value": h,
                            "fix": "use a colour from DESIGN.md §2, or amend the palette"})

            # 2. radius outside scale
            if radii:
                for m in RADIUS_RE.finditer(line):
                    for raw, num, unit in numbers_in(m.group(1)):
                        if num is None or unit in ("%",):
                            continue
                        base = num * 16 if unit == "rem" else num
                        if num in radii or base in radii:
                            continue
                        findings.append({
                            "rule": "radius-outside-scale", "severity": "P2",
                            "file": rel, "line": i, "value": raw,
                            "fix": f"use a radius from DESIGN.md §6 {sorted(radii)}"})

            # 3. spacing outside scale
            if spacings:
                for m in SPACING_RE.finditer(line):
                    for raw, num, unit in numbers_in(m.group(1)):
                        if num is None or unit == "%":
                            continue
                        base = num * 16 if unit == "rem" else num
                        if num in spacings or base in spacings:
                            continue
                        findings.append({
                            "rule": "spacing-outside-scale", "severity": "P2",
                            "file": rel, "line": i, "value": raw,
                            "fix": "use a step from DESIGN.md §4, or amend the scale"})

            # 4. font outside paper
            if fonts:
                for m in FONT_RE.finditer(line):
                    # split a font stack on commas, keep quoted names whole
                    stack = re.findall(r'"[^"]*"|\'[^\']*\'|[^,\s]+', m.group(1))
                    for raw in stack:
                        name = raw.lower().strip("\"'")
                        if not name or name in IGNORE_VALUES:
                            continue
                        if name in GENERIC_FONTS:
                            continue
                        if raw.strip() and re.fullmatch(r"[\d.]+(px|rem|em|%)?", name):
                            continue
                        if any(f in name or name in f for f in fonts):
                            continue
                        findings.append({
                            "rule": "font-outside-paper", "severity": "P1",
                            "file": rel, "line": i, "value": name,
                            "fix": f"use a face from DESIGN.md §3 {sorted(fonts)}"})

            # 5. gradient-clipped text (ban)
            if GRADIENT_TEXT_RE.search(line):
                findings.append({
                    "rule": "gradient-text", "severity": "P0",
                    "file": rel, "line": i, "value": "background-clip: text",
                    "fix": "solid ink; emphasis via size or weight"})

            # 6. emoji in markup
            if path.suffix.lower() in {".jsx", ".tsx", ".vue", ".svelte", ".html", ".htm", ".astro"}:
                for e in EMOJI_RE.findall(line):
                    findings.append({
                        "rule": "emoji-ui", "severity": "P1",
                        "file": rel, "line": i, "value": e,
                        "fix": "a drawn icon from one set, or no icon"})

    # 7. motion without reduced-motion guard (project-wide, not per file)
    #    A global @media in one stylesheet covers every file; if it exists
    #    anywhere in the tree, the animation is considered gated.
    if anim_files and not rm_files:
        findings.append({
            "rule": "motion-ungated", "severity": "P1",
            "file": ", ".join(sorted(anim_files)[:3]),
            "line": 0, "value": "no prefers-reduced-motion anywhere in the project",
            "fix": "add @media (prefers-reduced-motion: reduce) — strip transform, keep opacity"})

    return findings, len(files)


def main():
    ap = argparse.ArgumentParser(description="Check source against DESIGN.md tokens.")
    ap.add_argument("--root", default=".", help="project root (default: cwd)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="only print on findings")
    ap.add_argument("--init", action="store_true", help="print a TOKENS block to paste into DESIGN.md")
    args = ap.parse_args()

    if args.init:
        print("""<!-- TOKENS
color: #14161A #F7F7F5 #5B6068 #EDEDED
accent: #8C5A3C
radius: 0 4 8 12 14 9999
spacing: 0 2 4 8 12 16 24 32 48 64 96 128
fonts: Inter "Instrument Serif"
-->
Paste this into DESIGN.md §2–§6 and edit the values to match the paper.""")
        return 0

    root = Path(args.root).resolve()
    paper = find_paper(root)
    if not paper:
        msg = ("No DESIGN.md found. The guardrail has no contract to enforce.\n"
               "Create one with do-design-new, or draft it from the code "
               "(retrofit mode). Until then this check cannot run.")
        if args.json:
            print(json.dumps({"status": "no-paper", "message": msg}, indent=2))
        elif not args.quiet:
            print(msg)
        return 2

    tokens = parse_tokens(paper)
    if not tokens:
        msg = (f"{paper.relative_to(root)} exists but has no <!-- TOKENS ... --> block.\n"
               "Run: python3 scripts/check-design.py --init")
        if args.json:
            print(json.dumps({"status": "no-tokens", "message": msg}, indent=2))
        elif not args.quiet:
            print(msg)
        return 2

    findings, n_files = check(root, tokens)

    if args.json:
        print(json.dumps({
            "status": "findings" if findings else "clean",
            "paper": str(paper.relative_to(root)),
            "files_scanned": n_files,
            "count": len(findings),
            "findings": findings}, indent=2))
    else:
        if not findings:
            if not args.quiet:
                print(f"clean — {n_files} files, no drift from "
                      f"{paper.relative_to(root)}")
        else:
            by_sev = {}
            for f in findings:
                by_sev.setdefault(f["severity"], []).append(f)
            print(f"design drift — {n_files} files scanned against "
                  f"{paper.relative_to(root)}")
            for sev in ("P0", "P1", "P2"):
                group = by_sev.get(sev, [])
                if not group:
                    continue
                print(f"\n{sev} ({len(group)})")
                for f in group[:25]:
                    loc = f"{f['file']}:{f['line']}" if f["line"] else f["file"]
                    print(f"  {loc}  {f['rule']}  {f['value']}")
                    print(f"      → {f['fix']}")
                if len(group) > 25:
                    print(f"  … and {len(group) - 25} more")
            print("\nFix drift, or explain it and amend DESIGN.md §12.")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

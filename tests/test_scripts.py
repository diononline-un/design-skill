#!/usr/bin/env python3
"""Smoke tests for scripts/: python3 tests/test_scripts.py  (browser tests skip without Chrome)."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FX = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "scripts"))


def run(*args):
    p = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=ROOT)
    return p.returncode, p.stdout


def ids(out):
    return {f.get("id") or f.get("rule") for f in json.loads(out)["findings"]}


def test_check_design():
    code, out = run("scripts/check-design.py", "--root", FX / "drift", "--json")
    rules = ids(out)
    assert code == 1
    assert {"gradient-text", "hex-outside-palette", "tailwind-palette", "font-outside-paper", "emoji-ui",
            "motion-ungated", "radius-outside-scale", "spacing-outside-scale"} <= rules, rules
    values = {f["value"] for f in json.loads(out)["findings"]}
    # comments, alpha variants, var() fonts, anchors and HTML entities are not drift
    assert not values & {"#123456", "#8c5a3c80", "var(--font-display)", "#add", "#8212", "#ff00ff"}, values
    assert "comic neue" in values  # font stacks in custom properties count
    code, out = run("scripts/check-design.py", "--root", FX / "clean", "--json")
    # @font-face is a declaration, not use; legacy values are counted, not failed
    assert code == 0 and json.loads(out)["legacy"] == {"hex-outside-palette": 1}, out
    assert run("scripts/check-design.py", "--root", FX / "copy")[0] == 2  # no paper


def test_colour_maths():
    import importlib.util
    spec = importlib.util.spec_from_file_location("cd", ROOT / "scripts" / "check-design.py")
    cd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cd)
    assert cd.to_hex(cd.parse_color("oklch(0.6279 0.2577 29.23)")) in ("#ff0000", "#fe0000")
    assert cd.to_hex(cd.parse_color("hsl(120 100% 25%)")) == "#008000"
    assert cd.to_hex(cd.parse_color("rgb(20 22 26 / .1)")) == "#14161a"
    assert round(cd.contrast(cd.parse_color("#777"), cd.parse_color("#fff")), 2) == 4.48


def test_audit():
    code, out = run("scripts/audit.py", "scan", FX / "drift", "--json")
    assert code == 1 and {"C3", "I3", "M2", "K3", "B1"} <= ids(out), ids(out)
    code, out = run("scripts/audit.py", "copy", FX / "copy", "--json")
    assert {"W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W11", "W12", "W15", "W17", "W18", "T7"} <= ids(out), ids(out)
    assert run("scripts/audit.py", "copy", FX / "clean")[0] == 0
    code, out = run("scripts/audit.py", "score", "3", "4", "2", "3", "2", "4", "1", "--json")
    s = json.loads(out)
    assert s["score"] == 71 and s["band"] == "Sound" and s["work_list"][0] == "Distinction", s
    assert run("scripts/audit.py", "score", "5", "4", "2", "3", "2", "4", "1")[0] == 2
    code, out = run("scripts/audit.py", "contrast", "--paper", FX / "drift" / "DESIGN.md", "--json")
    assert code == 0 and len(json.loads(out)) == 6


def test_render():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ra", ROOT / "scripts" / "render-audit.py")
    ra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ra)
    if not ra.find_chrome(None):
        print("  skip: no Chrome")
        return
    code, out = run("scripts/render-audit.py", FX / "render" / "bad.html", "--widths", "1280,390", "--json")
    w = json.loads(out)["widths"]
    found = {f["code"] for r in w.values() for f in r["findings"]}
    assert code == 1 and {"page_scrolls_sideways", "text_overlap", "text_squeezed", "text_clipped",
                          "contrast_below_aa", "text_too_small", "tap_target_small", "row_misaligned",
                          "img_no_alt", "heading_order", "no_lang", "focus_invisible"} <= found, found
    code, out = run("scripts/render-audit.py", FX / "render" / "good.html", "--json")
    assert code == 0 and not any(r["findings"] for r in json.loads(out)["widths"].values()), out
    code, out = run("scripts/research.py", "logo", FX / "logo.svg", "--json")
    hexes = [c["hex"] for c in json.loads(out)["colors"]]
    assert code == 0 and "#0c5490" in hexes, hexes


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")

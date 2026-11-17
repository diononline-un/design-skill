#!/usr/bin/env bash
# install-guardrails.sh — put the design guardrail where agents will read it.
#
# Usage: ./install-guardrails.sh [project-root]
#
# Idempotent: safe to run twice. Never overwrites an existing DESIGN.md, never
# duplicates the AGENTS.md block.

set -euo pipefail

ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(dirname "$HERE")"

MARKER="<!-- /do-design guardrail -->"

echo "→ project: $ROOT"

# ---------------------------------------------------------------- 1. DESIGN.md
if [ -f "$ROOT/DESIGN.md" ]; then
  if grep -q "TOKENS" "$ROOT/DESIGN.md"; then
    echo "✓ DESIGN.md exists with a TOKENS block"
  else
    echo "⚠ DESIGN.md exists but has no TOKENS block"
    echo "  The checker cannot run without one. Add it with:"
    echo "    python3 $HERE/check-design.py --init"
  fi
else
  if [ -f "$SKILL/templates/DESIGN.md" ]; then
    cp "$SKILL/templates/DESIGN.md" "$ROOT/DESIGN.md"
    echo "✓ DESIGN.md created from template — fill in §2–§9"
    echo "  then add the token block: python3 $HERE/check-design.py --init"
  else
    echo "✗ template not found at $SKILL/templates/DESIGN.md"
    echo "  copy the template from the skill manually"
  fi
fi

# ---------------------------------------------------------- 2. the checker
mkdir -p "$ROOT/scripts"
if [ -f "$ROOT/scripts/check-design.py" ]; then
  if cmp -s "$HERE/check-design.py" "$ROOT/scripts/check-design.py"; then
    echo "✓ scripts/check-design.py up to date"
  else
    cp "$HERE/check-design.py" "$ROOT/scripts/check-design.py"
    echo "✓ scripts/check-design.py updated"
  fi
else
  cp "$HERE/check-design.py" "$ROOT/scripts/check-design.py"
  echo "✓ scripts/check-design.py installed"
fi
chmod +x "$ROOT/scripts/check-design.py" 2>/dev/null || true

# --------------------------------------------------------- 3. AGENTS.md block
BLOCK=$(cat <<'EOF'
<!-- do-design guardrail -->
## Design guardrail (read before any UI change)

`DESIGN.md` in the repo root is binding; §2–§6 hold the tokens.

Before you change any colour, size, radius, font, shadow or spacing value:
1. Find the token in `DESIGN.md` §2–§6.
2. Use the token. Do not introduce a value that is not in the paper.
3. If the task genuinely needs a value the paper lacks, **stop and ask**:
   "The paper has no token for X. Amend it (§12), or use <nearest>?"

After changing UI files, run:

```bash
python3 scripts/check-design.py          # drift report
python3 scripts/check-design.py --json   # for tooling
```

Fix drift or explain it. Do not silence it by editing the tokens to match
accidental values.

**Hard rules — no exception without an amendment:**
- No colour outside the palette in §2, including in gradients and shadows.
- No font outside §3. No new weights.
- No radius, spacing or shadow value outside §4 and §6.
- Accent colour: ≤5 % of any screen, never body text.
- No emoji as UI icons. No gradient-clipped text.
- Every animation gated by `prefers-reduced-motion`.
- Nested radii are concentric: inner = outer − padding.

If there is no `DESIGN.md`, say so and ask — do not invent one to make the
check pass.
<!-- /do-design guardrail -->
EOF
)

for f in AGENTS.md CLAUDE.md .cursorrules; do
  target="$ROOT/$f"
  if [ -f "$target" ]; then
    if grep -qF "$MARKER" "$target"; then
      echo "✓ $f already has the guardrail block"
    else
      printf '\n\n%s\n' "$BLOCK" >> "$target"
      echo "✓ $f — guardrail block appended"
    fi
  else
    case "$f" in
      AGENTS.md)
        printf '%s\n' "$BLOCK" > "$target"
        echo "✓ AGENTS.md created (agents read this at session start)"
        ;;
      *)
        # only create a file if a sibling of that kind already exists
        ;;
    esac
  fi
done

# ----------------------------------------------------------------- 4. verify
echo
echo "── verifying ──"
if command -v python3 >/dev/null 2>&1; then
  ( cd "$ROOT" && python3 scripts/check-design.py --quiet ) || true
  echo "(exit $? — 0 clean, 1 drift, 2 no paper/tokens)"
else
  echo "⚠ python3 not found — the checker needs it"
fi

cat <<EOF

Done. What now:
  · Fill in DESIGN.md §2–§9 (or run do-design-renew to derive it)
  · Add the token block: python3 scripts/check-design.py --init
  · Wire the check into CI/pre-commit (optional):
      python3 scripts/check-design.py || exit 1

The guardrail works without anyone invoking the skill: any agent that reads
AGENTS.md/CLAUDE.md at session start now knows the paper is binding.
EOF

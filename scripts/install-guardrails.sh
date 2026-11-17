#!/usr/bin/env bash
# install-guardrails.sh - put the design guardrail where coding agents already look.
# Usage: install-guardrails.sh [project-root]
# Idempotent: never overwrites DESIGN.md, never duplicates the agent block.
set -euo pipefail

ROOT="$(cd "${1:-.}" && pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(dirname "$HERE")"
MARKER="<!-- /do-design guardrail -->"
echo "project: $ROOT"

# 1. the paper
if [ -f "$ROOT/DESIGN.md" ]; then
  grep -q "TOKENS" "$ROOT/DESIGN.md" && echo "ok  DESIGN.md has a TOKENS block" \
    || echo "!!  DESIGN.md has no TOKENS block; draft one: python3 scripts/check-design.py --init"
else
  cp "$SKILL/templates/DESIGN.md" "$ROOT/DESIGN.md"
  echo "ok  DESIGN.md created from the template: fill §1-§9 and the TOKENS block"
fi

# 2. the checker (copied, so it runs without the skill installed)
mkdir -p "$ROOT/scripts"
if ! cmp -s "$HERE/check-design.py" "$ROOT/scripts/check-design.py" 2>/dev/null; then
  cp "$HERE/check-design.py" "$ROOT/scripts/check-design.py"
  chmod +x "$ROOT/scripts/check-design.py"
  echo "ok  scripts/check-design.py installed"
fi

# 3. the block agents read at session start (kept short: it is loaded in every session)
BLOCK=$(cat <<'EOF'
<!-- do-design guardrail -->
## Design guardrail

`DESIGN.md` is binding. Before changing any colour, font, size, radius, shadow or spacing:
use a token from its §2-§7. If the task needs a value the paper lacks, stop and ask:
"No token for X. Amend the paper (§12) or use <nearest>?" Never invent one.

After UI changes run `python3 scripts/check-design.py`. Fix the drift or explain it;
never edit the tokens to match accidental values. Also not checkable by script:
accent on at most 5% of a screen and never body text; no new font weights; nested
radii concentric (inner = outer - padding). No DESIGN.md: say so and ask.
<!-- /do-design guardrail -->
EOF
)
append() { grep -qF "$MARKER" "$1" 2>/dev/null && echo "ok  $(basename "$1") already has the block" \
  || { printf '\n%s\n' "$BLOCK" >> "$1"; echo "ok  $(basename "$1"): block added"; }; }

append "$ROOT/AGENTS.md"
# Claude Code reads CLAUDE.md; import AGENTS.md instead of loading the block twice.
if [ ! -f "$ROOT/CLAUDE.md" ]; then
  printf '@AGENTS.md\n' > "$ROOT/CLAUDE.md"; echo "ok  CLAUDE.md created (imports AGENTS.md)"
elif ! grep -q "^@AGENTS.md" "$ROOT/CLAUDE.md"; then
  append "$ROOT/CLAUDE.md"
fi
[ -f "$ROOT/.cursorrules" ] && append "$ROOT/.cursorrules"

# 4. verify
rc=0
( cd "$ROOT" && python3 scripts/check-design.py --quiet ) || rc=$?
case $rc in
  0) echo "ok  no drift" ;;
  1) echo "!!  drift found: run python3 scripts/check-design.py" ;;
  2) echo "..  checker waits for a filled TOKENS block (python3 scripts/check-design.py --init drafts one)" ;;
  *) echo "!!  checker failed to run (exit $rc); it needs python3" ;;
esac
echo "Optional CI / pre-commit: python3 scripts/check-design.py || exit 1"

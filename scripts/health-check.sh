#!/bin/bash
# scripts/health-check.sh — System health summary for Cyber AI OS
# Usage: bash scripts/health-check.sh

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "============================================"
echo "  Cyber AI OS — Health Check"
echo "============================================"

# System integrity
echo ""
echo "[1] Path Integrity..."
if python3 tests/validate.py 2>/dev/null; then
  : # validator prints its own ✓
else
  echo "    [!] Validation failed — run: python3 tests/validate.py -v"
fi

# Session status
echo ""
echo "[2] Active Session..."
SESSION="workspace/active/session.md"
if [ -f "$SESSION" ]; then
  TARGET=$(grep "^target:" "$SESSION" 2>/dev/null | head -1 | cut -d: -f2- | xargs)
  TYPE=$(grep "^type:" "$SESSION" 2>/dev/null | head -1 | cut -d: -f2- | xargs)
  PHASE=$(grep "^phase:" "$SESSION" 2>/dev/null | head -1 | cut -d: -f2- | xargs)
  echo "    Target : ${TARGET:-unknown}"
  echo "    Type   : ${TYPE:-unknown}"
  echo "    Phase  : ${PHASE:-unknown}"
else
  echo "    No active session (clean slate)"
fi

# Counts
echo ""
echo "[3] System Stats..."
AGENTS=$(ls .claude/agents/*.md 2>/dev/null | wc -l)
COMMANDS=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
ROLES=$(find department -name "*.md" -path "*/roles/*" 2>/dev/null | wc -l)
SKILLS=$(find skills -name "SKILL.md" 2>/dev/null | wc -l)
KB=$(find knowledge -name "*.md" ! -name "README.md" 2>/dev/null | wc -l)
ARCHIVES=$(ls workspace/archive/ 2>/dev/null | wc -l)

echo "    Departments : $AGENTS"
echo "    Commands    : $COMMANDS"
echo "    Roles       : $ROLES"
echo "    Skills      : $SKILLS"
echo "    KB entries  : $KB"
echo "    Archived sessions: $ARCHIVES"

# Config check
echo ""
echo "[4] Config..."
LHOST=$(python3 -c "import yaml; c=yaml.safe_load(open('config/tools.yaml')); print(c.get('lhost','NOT SET'))" 2>/dev/null || echo "NOT SET (pyyaml missing?)")
LPORT=$(python3 -c "import yaml; c=yaml.safe_load(open('config/tools.yaml')); print(c.get('lport','NOT SET'))" 2>/dev/null || echo "NOT SET")
echo "    LHOST : $LHOST"
echo "    LPORT : $LPORT"

echo ""
echo "============================================"
echo "  Done."
echo "============================================"

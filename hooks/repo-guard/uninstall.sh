#!/usr/bin/env bash
# Removes only the repo-guard hook and skill link (macOS, Linux). Windows: uninstall.ps1.
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)"; S="$HOME/.claude/settings.json"
rm -f "$HOME/.claude/skills/repo-guard-sandbox"
[ -f "$S" ] && python3 "$H/settings_merge.py" remove "$S"
echo "repo-guard hook and skill removed (backup: $S.bak-repo-guard)."

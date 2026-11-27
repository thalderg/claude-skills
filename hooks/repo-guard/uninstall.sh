#!/usr/bin/env bash
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)"; S="$HOME/.claude/settings.json"; HOOK="$H/claude-code/pretooluse.py"
rm -f "$HOME/.claude/skills/repo-guard-sandbox"
cp "$S" "$S.bak-repo-guard-uninstall"
jq --arg c "$HOOK" '.hooks.PreToolUse |= map(.hooks |= map(select(.command != $c)))' "$S.bak-repo-guard-uninstall" > "$S"
echo "repo-guard hook and skill removed (backup: $S.bak-repo-guard-uninstall)."

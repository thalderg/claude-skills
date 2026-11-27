#!/usr/bin/env bash
# Installs the repo-guard hook and skill for Claude Code (user level) on macOS or Linux. Windows: install.ps1.
# Needs repo-guard first (its install.sh).
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)"
S="$HOME/.claude/settings.json"
command -v repo-guard >/dev/null || [ -x "$HOME/code/repo-guard/bin/repo-guard" ] || { echo "Install repo-guard first (install.sh in the repo-guard folder)."; exit 1; }
mkdir -p "$HOME/.claude/skills"
ln -sfn "$H/skill/repo-guard-sandbox" "$HOME/.claude/skills/repo-guard-sandbox"
chmod +x "$H/claude-code/pretooluse.py"
python3 "$H/settings_merge.py" add "$S" "$H/claude-code/pretooluse.py"
echo "Hook added to $S (backup: $S.bak-repo-guard). Skill linked: ~/.claude/skills/repo-guard-sandbox. Start a new Claude Code session."

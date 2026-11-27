#!/usr/bin/env bash
# Installs the repo-guard hook and skill for Claude Code (user level). Needs repo-guard: ~/code/repo-guard/install.sh
set -euo pipefail
H="$(cd "$(dirname "$0")" && pwd)"
S="$HOME/.claude/settings.json"
command -v repo-guard >/dev/null || [ -x "$HOME/code/repo-guard/bin/repo-guard" ] || { echo "Install repo-guard first: ~/code/repo-guard/install.sh"; exit 1; }
mkdir -p "$HOME/.claude/skills"
ln -sfn "$H/skill/repo-guard-sandbox" "$HOME/.claude/skills/repo-guard-sandbox"
[ -f "$S" ] || echo '{}' > "$S"
cp "$S" "$S.bak-repo-guard"
HOOK="$H/claude-code/pretooluse.py"
jq --arg c "$HOOK" '
  .hooks //= {} | .hooks.PreToolUse //= [] |
  if ([.hooks.PreToolUse[].hooks[]?.command] | index($c)) then . else
    (if any(.hooks.PreToolUse[]; .matcher == "Bash") then
       .hooks.PreToolUse |= map(if .matcher == "Bash" then .hooks += [{"type":"command","command":$c,"timeout":300,"statusMessage":"repo-guard: checking download/install"}] else . end)
     else .hooks.PreToolUse += [{"matcher":"Bash","hooks":[{"type":"command","command":$c,"timeout":300,"statusMessage":"repo-guard: checking download/install"}]}] end) end' \
  "$S.bak-repo-guard" > "$S"
echo "Hook added to $S (backup: $S.bak-repo-guard). Skill linked: ~/.claude/skills/repo-guard-sandbox. Start a new Claude Code session."

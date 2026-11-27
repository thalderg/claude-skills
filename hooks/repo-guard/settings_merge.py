#!/usr/bin/env python3
"""Adds or removes the repo-guard hook in a Claude Code settings.json, keeping every other setting and hook.

  settings_merge.py add    <settings.json> <hook command>
  settings_merge.py remove <settings.json>

Used by install.sh / uninstall.sh (macOS, Linux) and install.ps1 / uninstall.ps1 (Windows).
A backup is written next to the file first (settings.json.bak-repo-guard).
"""
import json, os, shutil, sys

MARK = "hooks/repo-guard/claude-code/pretooluse.py"


def ours(hook):
    return MARK in str(hook.get("command", "")).replace("\\", "/")


def main():
    action, path = sys.argv[1], sys.argv[2]
    data = {}
    if os.path.exists(path) and os.path.getsize(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        shutil.copy(path, path + ".bak-repo-guard")
    pre = data.setdefault("hooks", {}).setdefault("PreToolUse", [])
    # remove our old entry (also one with an older path) before adding the current one;
    # a block that held only our entry is removed with it
    pre[:] = [b for b in pre if not (b.get("hooks") and all(ours(h) for h in b["hooks"]))]
    for block in pre:
        block["hooks"] = [h for h in block.get("hooks", []) if not ours(h)]
    if action == "add":
        entry = {"type": "command", "command": sys.argv[3], "timeout": 300, "statusMessage": "repo-guard: checking download/install"}
        bash = next((b for b in pre if b.get("matcher") == "Bash"), None)
        if bash:
            bash["hooks"].append(entry)
        else:
            pre.append({"matcher": "Bash", "hooks": [entry]})
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()

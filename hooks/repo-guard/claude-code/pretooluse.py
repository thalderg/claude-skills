#!/usr/bin/env python3
"""Claude Code PreToolUse hook (matcher: Bash) for repo-guard.

Every Bash command Claude wants to run comes in on stdin. If it clones a repository or installs a
package (git clone, gh repo clone, npm/pnpm/yarn/bun install, npx, pip install, uvx, curl | bash…),
repo-guard checks it FIRST, in code, and the hook answers:
  repo-guard exit 0 (clean)      → nothing printed: the command runs
  repo-guard exit 1 (odd)        → "ask": YOU see the findings and approve or refuse
  repo-guard exit 2 (known bad)  → "deny": the command is blocked
  repo-guard exit 3 / missing    → "deny": no check, no download (fail closed)
Commands that clone or install nothing are not touched.
"""
import json, os, re, shutil, subprocess, sys

TRIGGER = re.compile(r"\b(git\s+(-C\s+\S+\s+)?(clone|submodule\s+add)|gh\s+repo\s+clone|npm\s+(i|install|add)\b|pnpm\s+(i|install|add)\b|"
                     r"yarn\s+(add|install)\b|bun\s+(add|install|i)\b|npx\s|bunx\s|pip3?\s+install|uv\s+(add|pip)|uvx\s|pipx\s+(install|run))|"
                     r"(curl|wget)[^|]*\|\s*(sudo\s+)?(ba|z)?sh")


def out(decision, reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    if data.get("tool_name") != "Bash":
        sys.exit(0)
    cmd = (data.get("tool_input") or {}).get("command", "")
    if not TRIGGER.search(cmd) or os.environ.get("REPO_GUARD_HOOK_OFF"):
        sys.exit(0)
    rg = shutil.which("repo-guard") or os.path.expanduser("~/code/repo-guard/bin/repo-guard")
    if not os.path.exists(rg):
        out("deny", "repo-guard is not installed, so this download or install cannot be checked. Install it (~/code/repo-guard/install.sh) or ask the user.")
    try:
        r = subprocess.run([rg, "check-command", "--json", cmd], capture_output=True, text=True, timeout=280)
        res = json.loads(r.stdout)
    except Exception as e:
        out("deny", f"repo-guard could not check this command ({e}). Do not download or install it; tell the user.")
    level = res.get("level", 3)
    if level == 0:
        sys.exit(0)
    lines = []
    for c in res.get("checked", []):
        if c["level"] == 0:
            continue
        lines.append(f"{c['verdict']}: {c['meta'].get('target')}")
        for f in c["findings"]:
            if f["level"]:
                lines.append(f"  - {f['where']}: {f['why']}")
                if f.get("fix"):
                    lines.append(f"    what the user can do: {f['fix']}")
    report = "\n".join(lines)[:3000]
    if level == 1:
        out("ask", "repo-guard found ODD things (not proof of malware):\n" + report +
            "\nApprove only if you expect this. Safer: refuse, and let Claude offer the repo-guard sandbox test (skill: repo-guard-sandbox).")
    if level == 2:
        out("deny", "repo-guard BLOCKED this: KNOWN BAD.\n" + report +
            "\nDo not retry or work around this (no RG_SKIP, no other download tool). Tell the user exactly what was found.")
    out("deny", "repo-guard could NOT CHECK this, so it is not allowed yet:\n" + report +
        "\nDo not download or install it another way. Tell the user the reason and what they can do (above), and let them decide.")


if __name__ == "__main__":
    main()

# repo-guard hook (Claude Code, and any AI tool with command hooks)

Stops an AI coding agent from downloading or installing code that is known-bad or unchecked.

Before the agent runs a shell command, the hook looks for anything that brings code onto the machine:

| Command | What is checked |
|---|---|
| `git clone …`, `git submodule add …`, `gh repo clone …` | the repository (lookup, then a full read inside a throwaway container) |
| `npm/pnpm/yarn/bun install|add <pkg>`, `npx`, `bunx` | the packages (the PolinRider advisory list + OSV malicious-package database); GitHub specs as repositories |
| `pip install`, `uv add`, `uvx`, `pipx` | the packages (OSV, PyPI); `git+https://github.com/…` as repositories |
| `curl … \| bash`, `wget … \| sh`, `iex (…)` | flagged as odd: a downloaded script run without any check |

Every other command passes untouched (the hook exits at once).

## What happens

The check is [repo-guard](https://github.com/thalderg/repo-guard) (`~/code/repo-guard`). It is plain code: no AI model decides. Its exit code becomes the hook's decision:

| repo-guard | Meaning | Hook decision in Claude Code |
|---|---|---|
| 0 | clean | nothing: the command runs |
| 1 | odd (not proof of malware) | **ask**: you see the findings in the permission prompt and approve or refuse |
| 2 | known bad | **deny**: blocked; Claude is told not to work around it |
| 3 | could not check | **deny**: blocked, with the reason and what you can do (e.g. "Docker is not running: start Docker Desktop") |
| repo-guard missing | — | **deny** (fail closed) |

The `repo-guard-sandbox` skill (in `skill/`) tells Claude what to do next: explain the findings in plain words, ask "run it in the sandbox first?", and only on your "yes" run `repo-guard sandbox <target>`, then report what the code did (secrets it tried to read, servers it contacted, files it wrote, processes it left running).

## Install (Claude Code)

1. Install repo-guard first ([its README](https://github.com/thalderg/repo-guard): `install.sh` on macOS/Linux, `install.ps1` on Windows).
2. Then, in this folder:
   - macOS / Linux: `./install.sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File .\install.ps1`

   Both:
   - add a `PreToolUse` hook on `Bash` to `~/.claude/settings.json` (all projects), next to any hooks you already have, with a backup in `~/.claude/settings.json.bak-repo-guard` (the merge is done by `settings_merge.py`; running it again replaces its own entry, never adds a second one);
   - link the skill to `~/.claude/skills/repo-guard-sandbox` (Windows: a directory junction, no administrator rights needed).
3. Start a new Claude Code session.

Remove: `./uninstall.sh` (Windows: `uninstall.ps1`). It removes only this hook and the skill link.

The entry it adds (macOS / Linux):

```json
{ "hooks": { "PreToolUse": [ { "matcher": "Bash", "hooks": [
  { "type": "command", "command": "/Users/<you>/claude-skills/hooks/repo-guard/claude-code/pretooluse.py",
    "timeout": 300, "statusMessage": "repo-guard: checking download/install" } ] } ] } }
```

On Windows the command is `"C:/…/python.exe" "C:/Users/<you>/claude-skills/hooks/repo-guard/claude-code/pretooluse.py"`: forward slashes, so it works whether Claude Code runs it through cmd or Git Bash.

Tested: macOS (live). Linux: `~/code/repo-guard/tests/linux-test.sh` tests this hook too, in a throwaway Ubuntu container. Windows: not yet run on a Windows machine.

Claude Code hook reference: https://code.claude.com/docs/en/hooks

## Other AI coding tools (any provider that supports hooks)

The decision is not tied to Claude. Any tool whose hooks can run a program **before a shell command** and read its exit code or output can use the same check:

```bash
repo-guard check-command --json "<the shell command the agent wants to run>"
# exit 0 = allow, 1 = ask the user, 2 = block, 3 = block (could not check)
# stdout (JSON): level, verdict, and for every repository/package checked: findings with "why" and, for 3, "fix"
```

A small adapter turns that into the tool's own format, as `claude-code/pretooluse.py` does for Claude Code (input: `tool_input.command` on stdin; output: `permissionDecision` allow / ask / deny). For another tool:

1. Find its "before shell command" hook in its documentation (for example Cursor: https://cursor.com/docs/agent/hooks).
2. Read the command it sends to the hook.
3. Call `repo-guard check-command --json "<command>"`.
4. Map 0 → allow, 1 → ask, 2 and 3 → deny, and pass the findings text as the message the user and the agent see.

Check the tool's own documentation for the exact field names; they differ between tools and versions.

## Limits

- The hook sees only shell commands. Code fetched another way (a browser download, an MCP tool, a file the user drags in) is not checked: run `repo-guard scan <folder>` on it.
- A determined user (or a prompt-injected agent ignoring the skill) can disable hooks in settings. The hook protects against mistakes and against an agent that follows its rules, not against someone with full control of the machine.
- See the full manual: [MANUAL.md](https://github.com/thalderg/repo-guard/blob/main/MANUAL.md).

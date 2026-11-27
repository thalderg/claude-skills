---
name: repo-guard-sandbox
description: Use when the repo-guard hook stopped or flagged a git clone, a package install or a curl|bash (ODD or KNOWN BAD), when the user asks to install, clone or run a repository or package from GitHub or anywhere else, or when the user asks whether a repo is safe. Explains the findings in plain words, recommends a sandbox test and, only after the user says yes, runs `repo-guard sandbox` (a throwaway container with fake secrets) and reports what the code did.
---

# repo-guard: check first, sandbox on request

repo-guard is the single, code-based first check for every download and install (`~/code/repo-guard`). The hook runs it automatically before any Bash command that clones or installs something. This skill is what happens around it.

## Rules (never break these)

1. Never run, build, install or open untrusted code on the user's machine to "see what it does". Only `repo-guard sandbox` runs it.
2. Never work around a block: no `RG_SKIP=1`, no `REPO_GUARD_HOOK_OFF`, no other tool (curl, wget, a browser, a different package manager) to fetch the same thing, no editing the hook or settings.
3. KNOWN BAD (exit 2) is final. Tell the user what was found and stop. Run the sandbox on it only if the user explicitly asks to study it, and then only with `--force`, never on the host.
4. ODD (exit 1) is the user's decision. Explain each finding, then ask one question: "Run it in the sandbox first?"

## When the user asks to install or clone something

1. Run the check yourself before anything else: `repo-guard scan <url or owner/repo>` (for a package: `repo-guard check-command "npm install <pkg>"`).
2. CLEAN (0): go ahead with the user's command. If the owner is not trusted and the user wants to *run* the code, mention the sandbox in one line.
3. ODD (1) or KNOWN BAD (2): follow the rules above.

## Explaining findings

For every finding give: the file or package, what it does in plain words, and why it matters. Odd is not proof of malware (install scripts are common); known bad means it matches a known campaign or a flagged package.

## Running the sandbox (only after the user says yes)

1. Run in the background (it takes 1 to 5 minutes): `repo-guard sandbox <target> --json` (add `--offline` if the user wants no internet).
2. Report, from the JSON:
   - the verdict: CLEAN / ODD / KNOWN BAD;
   - secrets it tried to read (the fake keys, wallets, browser passwords): the strongest sign of a stealer;
   - servers it contacted (`meta.sandbox.dns_names`), and any blockchain service;
   - files it wrote outside the project, processes left running, odd programs started;
   - the report file path.
3. Always add the limit: some malware stays quiet in containers, so a quiet sandbox lowers the risk but is not proof.
4. Then ask what the user wants: stop, or go ahead with the original command (for ODD, the user approves it in the permission prompt).

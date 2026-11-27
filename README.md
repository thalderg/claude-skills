# Claude Skills Collection

A collection of custom skills for Claude AI - compatible with Claude Projects, Claude Code, and the Claude API.

## 📂 What's Inside

Each folder in this repository is a self-contained skill with its own `SKILL.md` file and supporting resources. Browse the repository to see available skills - each skill folder contains documentation explaining what it does and how to use it.

The [`hooks/`](hooks/) folder holds **hooks**: small programs that Claude Code (or another AI coding tool) runs automatically at fixed moments, for example before every shell command. Unlike a skill, a hook does not depend on the model remembering to use it. See [Hooks](#-hooks) below.

---

## 🚀 Installation

### For Claude Projects (Web/Desktop)

**Option 1: Add Entire Repository**
1. Open your Claude Project
2. Go to Project Settings → Knowledge → Add GitHub repository
3. Enter URL: `https://github.com/YOUR-USERNAME/claude-skills`
4. Select all or specific skills you want

**Option 2: Upload Individual Skills**
1. Download a specific skill folder from this repo
2. Zip the folder (must contain the folder itself, not just contents)
3. Settings → Capabilities → Upload skill
4. Upload the ZIP file

**Usage in Projects:**
```
Use [skill-name] to [task description]
```

### For Claude Code

**Option 1: Install as Plugin (Recommended)**
```bash
# Add this repository as a plugin marketplace
/plugin marketplace add YOUR-USERNAME/claude-skills

# List available skills
/plugin list

# Install specific skills
/plugin install skill-name@YOUR-USERNAME-claude-skills
```

**Option 2: Clone to Your Skills Directory**

For project-specific use:
```bash
cd your-project/.claude/skills/
git clone https://github.com/YOUR-USERNAME/claude-skills.git
```

For global use across all projects:
```bash
cd ~/.claude/skills/
git clone https://github.com/YOUR-USERNAME/claude-skills.git
```

**Option 3: Git Submodule (For Team Sharing)**
```bash
# Add as submodule to share with your team
git submodule add https://github.com/YOUR-USERNAME/claude-skills.git .claude/skills/shared-skills
git submodule update --init --recursive

# Team members clone with:
git clone --recurse-submodules [your-repo-url]
```

**Usage in Claude Code:**
```bash
# If installed as plugin
/skill-name [arguments]

# Or reference naturally
"Use the skill-name skill to accomplish [task]"
```

### For Claude API

See [Skills API Documentation](https://docs.anthropic.com/en/docs/build-with-claude/skills) for integrating these skills programmatically.

---

## 🔍 Discovering Skills

**In this repository:**
- Each top-level folder is a skill
- Read the `SKILL.md` file in each folder for documentation
- Look for `examples/` folders for usage examples

**In Claude Code:**
```bash
# List all installed skills
/skills

# Search for specific skills
/plugin search [keyword]
```

---

## 📁 Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md           # Required: Main skill definition
├── scripts/           # Optional: Executable scripts
├── examples/          # Optional: Usage examples
├── templates/         # Optional: Templates to fill
└── resources/         # Optional: Reference materials
```

---

## 🛠️ Contributing Your Own Skills

### Creating a New Skill

1. **Create the skill folder:**
```bash
mkdir my-new-skill
cd my-new-skill
```

2. **Create SKILL.md with frontmatter:**
```markdown
---
name: my-new-skill
description: Clear, concise description for skill discovery
---

# My New Skill

[Your detailed instructions here]

## Usage
[Examples of how to use this skill]

## Parameters
[Any arguments or options]
```

3. **Add supporting files (optional):**
```bash
mkdir scripts examples templates
```

4. **Test locally first:**
- For Projects: Create a ZIP and upload to test
- For Claude Code: Place in `.claude/skills/` and test

5. **Commit and push:**
```bash
git add my-new-skill/
git commit -m "feat: add my-new-skill"
git push
```

That's it! No need to update this README - the skill will automatically be discoverable.

---

## 🪝 Hooks

Hooks live in `hooks/<name>/`, each with its own README, an install script and an uninstall script.

| Hook | What it does | Install |
|---|---|---|
| [repo-guard](hooks/repo-guard/) | Before Claude runs any command that downloads code (`git clone`, `gh repo clone`, `npm/pnpm/yarn/bun install`, `npx`, `pip install`, `uvx`, `curl … \| bash`), it checks the repository or package with [repo-guard](https://github.com/thalderg/repo-guard): known malware campaigns (PolinRider), flagged packages (OSV), and odd patterns. Clean → it runs. Odd → you decide. Known bad → blocked. Could not check → blocked, with the reason and what you can do. Comes with the `repo-guard-sandbox` skill, which offers to run a flagged repo in a throwaway container and reports what it does. | macOS/Linux: `hooks/repo-guard/install.sh`; Windows: `hooks/repo-guard/install.ps1` (needs repo-guard installed first) |

**How a hook is wired in Claude Code:** an entry under `hooks` in `~/.claude/settings.json` (all projects) or `.claude/settings.json` (one project). The install scripts add the entry and keep a backup; the uninstall scripts remove only their own entry. Docs: [Claude Code hooks](https://code.claude.com/docs/en/hooks).

**Other AI coding tools:** the check itself is a plain command with exit codes (`repo-guard check-command "<shell command>"` → 0 clean, 1 odd, 2 known bad, 3 could not check), so any tool whose hooks can run a command before a shell command can use it. See [hooks/repo-guard/README.md](hooks/repo-guard/README.md).

---

## 🔒 Security Best Practices

- ⚠️ **Never commit credentials** - Use `.env` files (gitignored) or environment variables
- 🛡️ **Check code before it reaches your machine** - The [repo-guard hook](hooks/repo-guard/) checks every clone and install Claude runs
- ✅ **Review scripts** - Audit any executable code before use
- ✅ **Test in isolation** - Verify skills work before sharing
- ✅ **Document dependencies** - Note any required packages in SKILL.md

---

## 📖 Learn More

- [Claude Skills Documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Agent Skills Standard](https://agentskills.io)
- [Claude Code Skills Guide](https://code.claude.com/docs/en/skills)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12597488-how-to-create-custom-skills)

---

## 🤝 Support

- **Issues**: [Report bugs or request features](https://github.com/YOUR-USERNAME/claude-skills/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/YOUR-USERNAME/claude-skills/discussions)

---

## 📄 License

MIT License

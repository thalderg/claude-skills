# My Custom Claude Skills

A collection of custom skills for Claude Projects.

## Available Skills

### 🎯 two-phase-resource-curator
Intelligently filter and rank large collections (20-3000+) of technical resources using statistical metadata filtering and optional deep quality analysis.

**Location:** `/two-phase-resource-curator/`
**Documentation:** [SKILL.md](./two-phase-resource-curator/SKILL.md)

**Usage:**
```
"Use two-phase-resource-curator on https://github.com/thalderg/claude-skills/tree/main/two-phase-resource-curator"
```

---

## Installation for Claude Projects

Add this repository to your Claude Project:
1. Project Settings → Knowledge → Add GitHub repository
2. URL: `https://github.com/thalderg/claude-skills`

All skills will be available at:
- `/mnt/skills/user/two-phase-resource-curator/`
- (future skills will appear here automatically)

## Adding New Skills

To add a new skill to this collection:
1. Create a new folder: `my-new-skill/`
2. Add `SKILL.md` and any supporting files
3. Update this README with the new skill
4. Commit and push
5. Claude will automatically sync the new skill

## Skills Roadmap

- [x] two-phase-resource-curator
- [ ] custom-prompt-analyzer (planned)
- [ ] workflow-optimizer (planned)
```

### Step 3: Create .gitignore

Create `claude-skills/.gitignore`:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# Environment variables
.env
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.log
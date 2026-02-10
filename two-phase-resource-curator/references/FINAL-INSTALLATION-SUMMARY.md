# FINAL PACKAGE - Installation for Claude Desktop

## ✅ Required Files (6 Total - Complete Architecture)

**Download these 6 files above:**

1. **SKILL.md** (498 lines) - Main skill logic
2. **references/github.md** - GitHub methodology (loaded only when filtering GitHub)
3. **references/reddit.md** - Reddit methodology (loaded only when filtering Reddit)
4. **references/statistical-methodology.md** - Percentile explanation (loaded when needed)
5. **scripts/filter_github.py** - GitHub filter (uses GITHUB_PUB_TOKEN10F26)
6. **scripts/filter_reddit.py** - Reddit filter (no token needed)

**Why ALL 6 are needed:**
- SKILL.md alone = broken skill
- references/ = loaded ON DEMAND to save tokens
- scripts/ = actual filtering code
- This architecture was specifically designed to save tokens!

---

## 📁 Installation for Claude Desktop (Your Setup)

```bash
# 1. Create folder structure
mkdir -p ~/.config/claude/skills/two-phase-curator/references
mkdir -p ~/.config/claude/skills/two-phase-curator/scripts

# 2. Copy files
cp SKILL.md ~/.config/claude/skills/two-phase-curator/
cp github.md ~/.config/claude/skills/two-phase-curator/references/
cp reddit.md ~/.config/claude/skills/two-phase-curator/references/
cp statistical-methodology.md ~/.config/claude/skills/two-phase-curator/references/
cp filter_github.py ~/.config/claude/skills/two-phase-curator/scripts/
cp filter_reddit.py ~/.config/claude/skills/two-phase-curator/scripts/

# 3. Set GitHub token (for large repos)
export GITHUB_PUB_TOKEN10F26=ghp_your_token_here

# Make permanent:
echo 'export GITHUB_PUB_TOKEN10F26=ghp_your_token_here' >> ~/.bashrc
source ~/.bashrc

# 4. Verify
ls ~/.config/claude/skills/two-phase-curator/
# Should show: SKILL.md, references/, scripts/

echo $GITHUB_PUB_TOKEN10F26
# Should show: ghp_your_token...
```

---

## 🎯 Why This Structure?

### Token-Saving Design:

**Example 1: GitHub filtering**
```
User: "Use two-phase-curator on GitHub repo"

Claude loads:
1. SKILL.md (498 lines) ← Always
2. references/github.md (~150 lines) ← Only this one
3. Executes: scripts/filter_github.py

Total: ~650 lines
```

**Example 2: Reddit filtering**
```
User: "Use two-phase-curator on Reddit thread"

Claude loads:
1. SKILL.md (498 lines) ← Always
2. references/reddit.md (~130 lines) ← Different reference
3. Executes: scripts/filter_reddit.py

Total: ~630 lines
```

**If we removed references/ (your concern):**
- All methodology would be in SKILL.md
- Would be 800+ lines
- ALL loaded ALWAYS (even irrelevant parts)
- Token waste

**With references/:**
- SKILL.md: 498 lines (core only)
- References: Loaded only when needed
- More information available, less tokens used
- ✅ This is the point of the architecture!

---

## 📊 How It Works - Complete Flow

### Small Collection (≤30 items):
```
User: "Analyze these 5 workflows: [URL]"

Step 0: Count → 5 files detected
Decision: ≤30 → Phase 2 directly

Claude loads:
- SKILL.md (498 lines)
- No references needed (direct analysis)
- No scripts needed (no filtering)

Result: Quality analysis of all 5
Time: 2 minutes
```

### Large Collection (>30 items):
```
User: "Filter https://github.com/Zie619/n8n-workflows"

Step 0: Count → 4,343 files detected
Decision: >30 → Phase 1

Claude loads:
- SKILL.md (498 lines)
- references/github.md (~150 lines) ← Only GitHub details
- Executes: scripts/filter_github.py

Result: 4,343 → 650 filtered
Time: 10 minutes
Token usage: ~650 lines of context
```

---

## 🔑 Token Management

### GITHUB_PUB_TOKEN10F26

**Why this name?**
- GITHUB = Platform
- PUB = Public repos
- TOKEN = It's a token
- 10F26 = Created Feb 10, 2026

**Expiration:**
- Created: Feb 10, 2026
- Expires: May 11, 2026 (90 days)

**When needed:**
- Small repos (<100 files): Optional
- Large repos (1000+ files): Required
- Zie619/n8n-workflows (4,343 files): Absolutely required

**Priority order:**
1. `--token` command line argument
2. `GITHUB_PUB_TOKEN10F26` environment variable ← Your token
3. `GITHUB_TOKEN` environment variable (fallback)
4. No token (60 calls/hour limit)

---

## ✅ Verification

```bash
# Check skill installed
ls ~/.config/claude/skills/two-phase-curator/SKILL.md
ls ~/.config/claude/skills/two-phase-curator/references/
ls ~/.config/claude/skills/two-phase-curator/scripts/

# Check token set
echo $GITHUB_PUB_TOKEN10F26

# Test (in Claude Desktop)
"Use two-phase-curator on https://github.com/small-repo"
```

---

## 🎓 Summary

**What you need:** 6 files (SKILL.md + references + scripts)

**Why 6 files:** Token-efficient modular architecture
- Not just SKILL.md (that breaks it)
- Not just documentation (that's separate)
- The complete working architecture

**Where to put them:** `~/.config/claude/skills/two-phase-curator/`
- NOT `/mnt/skills/user/` (that's web/server)
- Your path is correct!

**Token for large repos:** `GITHUB_PUB_TOKEN10F26`
- Expires: May 11, 2026
- Set in environment variable

**Ready to use!**

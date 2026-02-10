---
name: two-phase-curator
description: Efficiently filter large collections (100-3000+ resources) using statistical metadata filtering. Phase 1 auto-filters by percentile ranking (no hard thresholds). Phase 2 optional deep analysis. Works for GitHub, Reddit, YouTube, and any technical content regardless of niche size.
---

# Two-Phase Resource Curator

## Purpose

Filter large collections using a **two-phase statistical approach** that adapts to any niche:
1. **Phase 1 (Automatic):** Fast percentile-based metadata filtering
2. **Phase 2 (Optional):** Deep quality analysis with alternative detection

**Key Innovation:** No hard thresholds. Uses statistical percentile ranking that works for N8n (small community) AND React (huge community).

## When to Use

**ALWAYS use for:**
- ✅ Any GitHub repo or Reddit thread (skill auto-detects size)
- ✅ Collections where you're unsure of resource count
- ✅ Want intelligent filtering based on collection size

**Skill automatically chooses:**
- **>30 resources:** Phase 1 (metadata filter) → Optional Phase 2
- **≤30 resources:** Skip Phase 1 → Phase 2 directly (deep analysis)

**DON'T use for:**
- ❌ Already know collection is tiny (<5 items) and high quality
- ❌ Resources already hand-curated
- ❌ Need specific custom filtering logic

## Core Philosophy

### Intelligent Phase Selection

**The skill always checks resource count first:**

```
1. Detect platform (GitHub/Reddit/etc.)
   ↓
2. Quick count: How many resources in collection?
   ↓
3. IF count > 30:
     → Run Phase 1 (statistical metadata filtering)
     → STOP (offer Phase 2 optionally)
   ELSE (count ≤ 30):
     → Skip Phase 1
     → Run Phase 2 directly (deep quality analysis)
```

**Why 30 as threshold?**
- ≤30 items: Can deep-analyze directly in reasonable time
- >30 items: Need metadata pre-filter to avoid waste

**Examples:**
- 5 GitHub files → Phase 2 directly (quality analysis)
- 50 GitHub files → Phase 1 (filter to ~15) → Optional Phase 2
- 3000 GitHub files → Phase 1 (filter to ~450) → Optional Phase 2

### Statistical Filtering (Not Hard Thresholds)

**Problem with hard thresholds:**
```python
if stars < 50:  # Fails for N8n (niche, <50 stars normal)
    reject()
```

**Solution - Percentile ranking:**
```python
stars_percentile = percentile_rank(stars, all_stars_in_collection)
# 15 stars in N8n → 85th percentile → KEEP
# 15 stars in React → 5th percentile → REJECT
```

**Why this works:**
- Adapts to ANY niche automatically
- Based on actual distribution, not arbitrary numbers
- Works for small communities AND large communities

See `references/statistical-methodology.md` for detailed explanation.

## Execution Flow

### Step 0: Resource Count Detection (ALWAYS FIRST)

Before running any phase, detect collection size:

```
1. User provides URL/collection
   ↓
2. Detect platform (GitHub/Reddit/YouTube)
   ↓
3. Quick count check:
   - GitHub: API call to count files
   - Reddit: Check post count in subreddit
   - List: Count items provided
   ↓
4. Decision:
   IF count > 30:
     → Run Phase 1 (metadata filtering)
   ELSE:
     → Skip to Phase 2 (deep analysis)
```

**Count methods by platform:**

| Platform | Count Method | Speed |
|----------|--------------|-------|
| **GitHub** | `GET /repos/{owner}/{repo}` + tree API | <5 sec |
| **Reddit** | Subreddit info endpoint | <2 sec |
| **List** | Simple length check | <1 sec |

---

## Phase 1: Metadata Filtering (IF >30 RESOURCES)

## Phase 1: Metadata Filtering (IF >30 RESOURCES)

**Only executed if Step 0 detects >30 resources.**

### Platform Detection

Identify platform to select appropriate filtering strategy:

| Platform | Script | Metrics Used |
|----------|--------|--------------|
| **GitHub** | `scripts/filter_github.py` | Stars, forks, recency, file size |
| **Reddit** | `scripts/filter_reddit.py` | Score, comments, upvote ratio, recency |
| **YouTube** | `scripts/filter_youtube.py` | Views, engagement, recency |
| **Generic** | `scripts/filter_generic.py` | File size, naming patterns |

### Execution Flow (For >30 Resources)

```
1. Platform detected (from Step 0)
   ↓
2. Execute: python scripts/filter_{platform}.py [url]
   ↓
3. Script calculates percentiles for ALL resources
   ↓
4. Ranks each by composite score (weighted percentiles)
   ↓
5. Filters by adaptive cutoff (based on collection size)
   ↓
6. Outputs: filtered_resources.json
   ↓
7. Present results to user
   ↓
8. STOP (unless user requests Phase 2)
```

### Platform-Specific Weighting

Each platform has different quality indicators:

| Platform | Top Metrics | See Reference |
|----------|------------|---------------|
| **GitHub** | Recency (40%), Stars (35%), Forks (15%) | `references/github.md` |
| **Reddit** | Score (40%), Recency (30%), Comments (20%) | `references/reddit.md` |
| **YouTube** | Recency (40%), Views (30%), Engagement (30%) | `references/youtube.md` |

Weights chosen based on what ACTUALLY predicts quality per platform.

### Adaptive Cutoffs

Cutoff percentile adjusts to collection size:

| Original Size | Target Keep % | Cutoff Percentile |
|--------------|---------------|-------------------|
| 100-200 | ~50% | 50th |
| 200-500 | ~40% | 60th |
| 500-1000 | ~30% | 70th |
| 1000-3000 | ~20% | 80th |
| 3000+ | ~10-15% | 85th |

**Rationale:** Larger collections need stricter filtering to reach manageable size.

### Phase 1 Output Format

```json
{
  "original_count": 3000,
  "filtered_count": 247,
  "reduction": "91.8%",
  "platform": "github",
  "cutoff_percentile_used": 85,
  "statistics": {
    "stars_median": 12,
    "stars_p75": 28
  },
  "resources": [...top 247 with scores...]
}
```

See `references/github.md` for complete output specification.

## Phase 2: Deep Quality Analysis

**Runs in two scenarios:**
1. **Automatically:** If Step 0 detects ≤30 resources (skips Phase 1)
2. **On request:** If user says "do deep analysis" after Phase 1

### When Phase 2 Runs Automatically

**Collection ≤30 resources:**
- No Phase 1 needed (can analyze all directly)
- Immediately performs deep quality analysis
- Outputs detailed ranking

**User says after seeing count:**
```
"I found this repo with 5 N8n workflows"
→ Skill detects: 5 resources (≤30)
→ Automatically runs Phase 2
→ No need to ask permission
```

### When Phase 2 is Optional

**Collection >30 resources:**
- Phase 1 already ran and filtered
- User must explicitly request Phase 2
- Say: "do deep analysis", "run Phase 2", "check for alternatives"

### Phase 2 Process

Performs comprehensive quality analysis:

1. **Quality Scoring:**
   - Read actual content (code, workflow structure, post content)
   - Technical quality assessment (1-10)
   - Production-readiness check
   - Code patterns, error handling, documentation

2. **Recency Weighting:**
   - Age penalties for AI/LLM resources (double penalty)
   - Standard aging for general tech content
   - Modern best practices check

3. **Alternative Detection:**
   - Search for modern alternatives (resources >12mo or score <8)
   - Identify obsolete patterns
   - Calculate effort saved with modern approach
   - Provide links to alternatives

4. **Final Ranking:**
   - Tier 1 (9-10): Must-use
   - Tier 2 (7-8): Recommended
   - Tier 3 (5-6): Use with caution
   - Tier 4 (<5): Deprecated

### Phase 2 Output

```markdown
# Deep Analysis

**Tier 1 (9-10):** X must-use resources
**Tier 2 (7-8):** Y recommended
**Tier 3 (5-6):** Z use with caution
**Tier 4 (<5):** W deprecated

[Detailed breakdowns with alternatives...]

Recommendation: Feed tier 1+2 to NotebookLM
```

See original `resource-curator-with-alternatives` skill for full Phase 2 specification.

## Usage Instructions

### Scenario 1: Small Collection (≤30 resources)

```
User: "Analyze these 5 N8n workflows: [URL]"

Claude:
→ Detects: 5 workflows
→ Runs Phase 2 directly (no Phase 1)

Output:
"📊 5 workflows detected - running deep analysis...

✅ Analysis Complete
Tier 1: 2 workflows (must-use)
Tier 2: 3 workflows (recommended)

All high quality. Feed all to NotebookLM."
```

### Scenario 2: Large Collection (>30 resources)

```
User: "Filter this repo with 3000 workflows: [URL]"

Claude:
→ Detects: 3000 workflows
→ Runs Phase 1 (metadata filter)
→ 3000 → 247 workflows
→ STOPS

Output:
"📊 3000 workflows filtered to 247 (91.8% reduction)
Top resources ranked by N8n community standards.

Say 'do deep analysis' for Phase 2 or review the list."

User: "Do deep analysis"

→ Runs Phase 2 on 247
→ 247 → 148 recommended (≥7/10)
```

### Scenario 3: Single File

```
User: "Check quality of this workflow: [URL]"

Claude:
→ Detects: 1 file
→ Runs Phase 2 directly

Output:
"📊 Single file analysis
Rank: 7/10 (Recommended, but 14mo old)
Alternative: Modern Claude API pattern (40% simpler)"
```

## Script Specifications

### Step 0: Count Detection (Run First)

```python
count = quick_count(url, platform)
if count <= 30:
    run_phase_2_directly()
else:
    run_phase_1_then_offer_phase_2()
```

### GitHub Filter

```bash
python scripts/filter_github.py --url URL --token TOKEN
```

**Output:** `filtered_github.json`

### Reddit Filter

```bash
python scripts/filter_reddit.py --subreddit NAME --limit 1000
```

**Output:** `filtered_reddit.json`

**See `references/github.md` and `references/reddit.md` for complete specifications.**

## Integration with NotebookLM Workflow

**Standard flow:**

```
1. Large collection (3000 items)
   ↓
2. Phase 1: Filter to 200-300 (statistical metadata)
   ↓
3. User reviews filtered list
   ↓
4. Optional: Phase 2 on filtered 200-300
   ↓
5. Final set (100-150 quality resources)
   ↓
6. Feed to NotebookLM
   ↓
7. NotebookLM creates manual
   ↓
8. Add to Claude Project
```

## Performance Benchmarks

| Collection Size | Phase 1 Time | Phase 1 Cost | Phase 2 Time | Phase 2 Cost |
|----------------|--------------|--------------|--------------|--------------|
| 100 | 30 sec | $0.10 | 5 min | $2-3 |
| 500 | 2 min | $0.50 | 20 min | $8-10 |
| 1000 | 5 min | $1 | 40 min | $15-20 |
| 3000 | 10 min | $2-3 | 2 hours | $40-60 |

**Phase 1 is 20x faster and 10x cheaper.**

## Error Handling

**If GitHub API fails:**
- Try without token (lower rate limit)
- Reduce depth: `--max-depth 2`
- Process in smaller batches

**If collection too large:**
- Phase 1 can handle up to ~5000 items
- Beyond that, sample first 5000 or process in batches

**If platform unknown:**
- Falls back to `filter_generic.py`
- Uses file size and naming patterns only
- Less accurate but functional

## Critical Rules

1. **ALWAYS check resource count FIRST** (before any phase)
2. **IF ≤30 resources: Run Phase 2 automatically** (skip Phase 1, no asking)
3. **IF >30 resources: Run Phase 1 automatically** (metadata filter)
4. **Phase 2 after Phase 1: Only if user requests** ("do deep analysis")
5. **Use statistical percentiles, never hard thresholds**
6. **Adjust cutoffs based on collection size**
7. **Present results with statistics and breakdown**
8. **Save outputs** for user download
9. **Select appropriate script** per platform

**Count Check Examples:**
- 1 file → Phase 2 direct ✅
- 5 files → Phase 2 direct ✅
- 30 files → Phase 2 direct ✅
- 31 files → Phase 1 first ✅
- 3000 files → Phase 1 first ✅

## Decision Tree

```
Collection/URL provided
    ↓
Detect platform (GitHub/Reddit/YouTube/etc.)
    ↓
Quick count: How many resources?
    ↓
    ├─── ≤30 resources ────────┐
    │                          ↓
    │                    Skip Phase 1
    │                          ↓
    │                    Run Phase 2 (automatic)
    │                          ↓
    │                    Present quality analysis
    │                          ↓
    │                         END
    │
    └─── >30 resources ────────┐
                               ↓
                         Select script (github/reddit/youtube)
                               ↓
                         Execute Phase 1 (statistical filtering)
                               ↓
                         Present filtered results
                               ↓
                              STOP
                               ↓
                         User says "deep analysis"? ─NO→ END
                               ↓ YES
                         Execute Phase 2 (quality + alternatives)
                               ↓
                         Present detailed ranking
                               ↓
                              END
```

**Key Points:**
- **Always check count first** (Step 0)
- **≤30:** Phase 2 automatic (no asking)
- **>30:** Phase 1 automatic, Phase 2 optional

## Success Criteria

✅ **Phase 1 reduces collection appropriately** (not too much, not too little)
✅ **High-quality resources retained** (spot-check top 10)
✅ **Low-effort execution** (<10 min for 1000+ items)
✅ **Statistics make sense** (check percentiles are reasonable)
✅ **User reviews filtered list** before proceeding
✅ **Phase 2 only executed on request**

## References

For detailed platform-specific methodologies:
- `references/github.md` - GitHub filtering details
- `references/reddit.md` - Reddit filtering details
- `references/statistical-methodology.md` - How percentile ranking works
- `references/platform-weights.md` - Why weights are chosen

For implementation:
- `scripts/filter_github.py` - GitHub statistical filter
- `scripts/filter_reddit.py` - Reddit statistical filter

## Updates & Maintenance

**Update quarterly:**
- Review platform engagement trends
- Adjust weights if needed
- Update for new platforms

**Current version:** February 2026
**Next review:** May 2026

# GitHub Filtering Methodology

## Overview

GitHub repositories have specific engagement patterns that differ from other platforms. This reference explains the statistical filtering approach for GitHub content.

## Key Metrics

### 1. Stars (35% weight)
**What it measures:** Popularity, community validation
**Why it matters:** High stars indicate quality and usefulness
**Niche consideration:** 20 stars in N8n ≠ 20 stars in React

**Statistical approach:**
```python
stars_percentile = percentile_rank(repo_stars, all_stars_in_collection)
# Returns 0-100 indicating position in THIS collection
```

### 2. Recency (40% weight - HIGHEST)
**What it measures:** How recently updated
**Why it matters most:** Tech code ages FAST
- 18-month-old workflow often uses deprecated APIs
- Old patterns replaced by better approaches
- Dependencies become obsolete

**Scoring:**
```python
days_old = (now - last_updated).days

if days_old <= 30:    return 100
elif days_old <= 90:  return 90
elif days_old <= 180: return 75
elif days_old <= 365: return 50
elif days_old <= 730: return 25
else:                 return max(0, 25 - (days_old-730)/365*10)
```

### 3. Forks (15% weight)
**What it measures:** Actual usage, people building on it
**Why it matters:** Shows it's useful enough to fork

**Percentile ranking within collection**

### 4. File Size (10% weight)
**What it measures:** Substance vs trivial example
**Why it matters:** Filters out 50-line "hello world" examples

**Thresholds:**
- <500 bytes: Likely trivial, skip
- 500-2000 bytes: Basic, low weight
- 2000-10000 bytes: Substantial
- >10000 bytes: Complex, high weight

## Why These Weights?

**Recency = 40%:**
- Most important for technical content
- Outdated code is worse than no code
- Fast-moving field (AI/automation/LLMs)

**Stars = 35%:**
- Strong signal of quality
- Crowd validation
- But can be gamed, so not 50%+

**Forks = 15%:**
- Shows real usage
- People actually implementing it
- Lower weight because fewer people fork than star

**File Size = 10%:**
- Basic quality check
- Prevents trivial examples
- Lowest weight (doesn't predict quality alone)

## Example: N8n Repository

**Scenario:** 300 workflows in niche N8n community

**Statistics calculated:**
```
Stars: median=8, p75=22, p90=58
Forks: median=2, p75=6, p90=15
File sizes: median=3500 bytes, p75=8200, p90=15000
```

**Workflow A:**
- Stars: 15 (58th percentile in N8n collection)
- Updated: 2 months ago (recency score: 100)
- Forks: 4 (55th percentile)
- File size: 6500 bytes (62nd percentile)

**Composite score:**
```
= (100 * 0.40) + (58 * 0.35) + (55 * 0.15) + (62 * 0.10)
= 40.0 + 20.3 + 8.25 + 6.2
= 74.75 / 100
```

**Workflow B:**
- Stars: 42 (82nd percentile - strong!)
- Updated: 8 months ago (recency score: 65)
- Forks: 12 (78th percentile)
- File size: 12000 bytes (85th percentile)

**Composite score:**
```
= (65 * 0.40) + (82 * 0.35) + (78 * 0.15) + (85 * 0.10)
= 26.0 + 28.7 + 11.7 + 8.5
= 74.9 / 100
```

**Result:** Both score ~75, both kept (above 70th percentile cutoff for 300-item collection)

## Special Filtering Rules

### Skip These Files
```python
Skip if filename contains:
- 'test', 'example', 'demo', 'sample'
- '.md', 'readme', 'license'
- '.min.', 'backup'
- '.gitignore', '.yml' (config files)

Skip if size < 500 bytes (trivial)
```

### Repository-Level Checks

If entire repo is abandoned (>2 years no updates), flag for user review.

If repo has <3 stars AND <2 forks, likely personal/experimental - flag.

## Adaptive Cutoff by Collection Size

| Size | Cutoff | Why |
|------|--------|-----|
| 100-200 files | 50th percentile | Small set, be generous |
| 200-500 files | 60th percentile | Moderate filtering |
| 500-1000 files | 70th percentile | Significant reduction needed |
| 1000-3000 files | 80th percentile | Heavy filtering |
| 3000+ files | 85th percentile | Very strict |

**Rationale:** Can't manually review 1500 files, need aggressive filtering.

## Output Format

```json
{
  "name": "advanced-workflow.json",
  "url": "https://github.com/owner/repo/blob/main/workflow.json",
  "composite_score": 74.7,
  "score_breakdown": {
    "recency": 100,
    "stars": 58,
    "forks": 55,
    "file_size": 62
  },
  "metadata": {
    "stars": 15,
    "forks": 4,
    "size_bytes": 6500,
    "last_updated": "2025-12-15"
  }
}
```

## Limitations

**What this CAN'T detect:**
- Code quality (need Phase 2 for that)
- Security issues
- Whether it actually works
- Documentation quality

**What it CAN detect:**
- Popularity (stars)
- Usage (forks)
- Maintenance (recency)
- Substance (file size)

**Phase 1 filters by engagement. Phase 2 filters by quality.**

## GitHub API Considerations

**Rate Limits:**
- Without token: 60 requests/hour
- With token: 5,000 requests/hour

**Solution:** Always use token for collections >50 files

**Depth Limit:**
- Default: 3 levels deep
- Prevents hitting rate limits on huge repos
- Can adjust with `--max-depth` flag

## Real-World Examples

### Example 1: N8n Workflows (Niche)
- 300 workflows
- Median: 8 stars
- 70th percentile cutoff
- Result: Keep 90 workflows (top 30%)

### Example 2: React Components (Mainstream)
- 500 components
- Median: 450 stars
- 70th percentile cutoff
- Result: Keep 150 components (top 30%)

**Same percentile logic, different absolute numbers.**

## When GitHub Filtering Works Best

✅ **Good for:**
- Code repositories
- Workflow collections
- Technical examples
- Active communities

⚠️ **Less reliable for:**
- Brand new repos (<1 month old, no stars yet)
- Personal projects (owner doesn't promote)
- Private repos (can't access metadata)

## Integration with Phase 2

**Phase 1 output → Phase 2 input:**
1. Phase 1 filters 3000 → 300 by metadata
2. Phase 2 reads actual code of those 300
3. Phase 2 filters 300 → 150 by quality
4. Final: 150 high-quality, well-maintained resources

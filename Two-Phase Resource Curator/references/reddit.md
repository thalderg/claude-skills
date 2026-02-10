# Reddit Filtering Methodology

## Overview

Reddit posts have different engagement patterns than code repositories. Community size, subreddit activity, and discussion quality vary widely.

## Key Metrics

### 1. Score/Upvotes (40% weight - HIGHEST)
**What it measures:** Direct community approval
**Why it matters:** Upvotes = useful/valuable content
**Reliable signal:** Hard to game compared to other platforms

**Statistical approach:**
```python
score_percentile = percentile_rank(post_score, all_scores_in_collection)
```

### 2. Recency (30% weight)
**What it measures:** How recent the post is
**Why it matters:** Tech discussions age, APIs change, best practices evolve

**Scoring:**
```python
days_old = (now - created_date).days

if days_old <= 30:    return 100
elif days_old <= 90:  return 85
elif days_old <= 180: return 70
elif days_old <= 365: return 50
elif days_old <= 730: return 25
else:                 return max(0, 25 - (days_old-730)/365*10)
```

### 3. Comments (20% weight)
**What it measures:** Discussion, engagement, usefulness
**Why it matters:** More comments = generated discussion = valuable

**Percentile ranking within collection**

### 4. Upvote Ratio (10% weight - LOWEST)
**What it measures:** Controversy (likes / (likes + dislikes))
**Why it matters less:** Controversial ≠ bad, just polarizing

**Absolute scoring:**
```python
ratio_score = upvote_ratio * 100  # 0.85 → 85/100
```

## Why These Weights?

**Score = 40%:**
- Most reliable quality signal
- Direct community validation
- Harder to manipulate than stars

**Recency = 30%:**
- Tech content ages
- Old solutions may be obsolete
- But less critical than GitHub (code ages faster than discussions)

**Comments = 20%:**
- Discussion indicates value
- People engaged enough to respond
- But can include arguments, so lower weight

**Upvote Ratio = 10%:**
- Controversial ≠ bad necessarily
- Lowest weight
- Used as tie-breaker mainly

## Example: r/n8n Subreddit

**Scenario:** 500 posts about N8n automation

**Statistics calculated:**
```
Score: median=25, p75=58, p90=142
Comments: median=8, p75=18, p90=35
Upvote ratio: median=0.89
```

**Post A:**
- Score: 42 upvotes (65th percentile)
- Age: 2 months (recency: 85)
- Comments: 12 (58th percentile)
- Upvote ratio: 0.92 (92/100)

**Composite score:**
```
= (65 * 0.40) + (85 * 0.30) + (58 * 0.20) + (92 * 0.10)
= 26.0 + 25.5 + 11.6 + 9.2
= 72.3 / 100
```

**Post B:**
- Score: 85 upvotes (82nd percentile - strong!)
- Age: 11 months (recency: 52)
- Comments: 22 (78th percentile)
- Upvote ratio: 0.88 (88/100)

**Composite score:**
```
= (82 * 0.40) + (52 * 0.30) + (78 * 0.20) + (88 * 0.10)
= 32.8 + 15.6 + 15.6 + 8.8
= 72.8 / 100
```

**Result:** Both ~72-73, both kept if cutoff is 70th percentile

## Special Filtering Rules

### Skip These Posts
```python
Skip if:
- Deleted (author == '[deleted]')
- Removed by moderator
- Score < 1 AND comments < 1 (no engagement at all)
- Obvious spam (regex patterns)
```

### Basic Sanity Checks

**Must have SOME engagement:**
- Score >= 1 OR
- Comments >= 1

(Filters out complete duds)

## Adaptive Cutoff by Collection Size

| Size | Cutoff | Why |
|------|--------|-----|
| 50-100 posts | 50th percentile | Small sub, be generous |
| 100-500 posts | 60th percentile | Moderate |
| 500-1000 posts | 70th percentile | Larger sub, filter more |
| 1000+ posts | 75th percentile | Big sub, be selective |

**Note:** Less aggressive than GitHub because:
- Reddit posts harder to produce than starring a repo
- Lower volume overall
- Higher signal-to-noise already

## Output Format

```json
{
  "title": "How I automated my entire workflow with N8n",
  "url": "https://reddit.com/r/n8n/comments/abc123/...",
  "composite_score": 72.3,
  "score_breakdown": {
    "score": 65,
    "recency": 85,
    "comments": 58,
    "ratio": 92
  },
  "metadata": {
    "score": 42,
    "num_comments": 12,
    "upvote_ratio": 0.92,
    "created_date": "2025-10-15",
    "days_old": 62,
    "author": "automation_expert",
    "subreddit": "n8n"
  }
}
```

## Reddit API Access

### No Auth Needed (JSON Endpoint)
```bash
# Just add .json to any Reddit URL
curl "https://www.reddit.com/r/n8n/top.json?limit=100"
```

**Advantages:**
- No API keys needed
- No rate limits (reasonable usage)
- Simple HTTP requests

**Limitations:**
- Max 100 posts per request
- Need to paginate with `after` parameter
- Some private subs inaccessible

### With PRAW (Optional)
```python
import praw

reddit = praw.Reddit(
    client_id='YOUR_ID',
    client_secret='YOUR_SECRET',
    user_agent='ResourceCurator/2.0'
)
```

**When to use:** Large-scale scraping, need metadata not in JSON

## Subreddit-Specific Considerations

### Active vs Inactive Subs

**r/n8n (moderately active):**
- ~20-50 posts/week
- Median score: 15-30
- Use 60th percentile cutoff

**r/programming (very active):**
- 100+ posts/day
- Median score: 100+
- Use 75th percentile cutoff

**Percentile approach handles both automatically**

### Niche Technical Subs

For r/n8n, r/pipedream, r/zapier:
- Lower absolute numbers
- But percentiles still work
- 20 upvotes might be top 10%

### Mainstream Subs

For r/programming, r/MachineLearning:
- Higher absolute numbers
- Same percentiles
- 20 upvotes might be bottom 5%

## Real-World Examples

### Example 1: Small Niche Sub
- r/n8n: 500 posts
- Median: 18 score
- 70th percentile cutoff = score of 35+
- Result: Keep 150 posts

### Example 2: Large Active Sub
- r/programming: 5000 posts
- Median: 250 score
- 75th percentile cutoff = score of 850+
- Result: Keep 1250 posts

## Limitations

**What Reddit filtering CAN'T detect:**
- Content accuracy (might be popular but wrong)
- Depth of technical detail
- Whether solutions actually work

**What it CAN detect:**
- Community approval (score)
- Generated discussion (comments)
- Recency
- Not controversial (ratio)

**Phase 2 would verify technical accuracy**

## Integration with Phase 2

**Typical flow:**
1. Phase 1: Filter 1000 posts → 300 (metadata)
2. Phase 2: Read actual content of 300
3. Phase 2: Check if solutions are current/correct
4. Phase 2: Search for modern alternatives
5. Final: 150 high-quality, current discussions

## Best Practices

**For specific topics:**
```bash
# Good: Search specific subreddit
python filter_reddit.py --subreddit n8n

# Also good: Filter from URL
python filter_reddit.py --url "https://reddit.com/r/n8n/top?t=year"
```

**For broad research:**
- Hit multiple related subs
- Combine results
- Deduplicate

**Time filters:**
- `t=week` - Very recent
- `t=month` - Recent
- `t=year` - Last year (good default)
- `t=all` - All time (includes outdated)

## When Reddit Filtering Works Best

✅ **Good for:**
- Finding discussions
- Community recommendations
- Problem-solving threads
- "How I did X" posts

⚠️ **Less reliable for:**
- Memes/jokes (high score, low value)
- Rants (engaging but not useful)
- Very old content (>2 years)

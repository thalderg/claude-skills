# Statistical Methodology: Percentile-Based Filtering

## The Problem with Hard Thresholds

### What Doesn't Work

```python
# Rigid thresholds fail across niches
if stars < 50:
    reject()  # ❌ Excludes 95% of N8n repos
              # ❌ Excludes 95% of niche communities
              # ✅ Only works for mainstream (React, Python)
```

**Why hard thresholds fail:**
1. **Niche blind:** 20 stars in N8n community = excellent
2. **Mainstream biased:** 20 stars in React = poor
3. **Arbitrary:** Why 50? Why not 48 or 52?
4. **No statistical basis:** Not based on actual distributions

### Real-World Example

**N8n Repository (niche):**
- Total workflows: 300
- Stars distribution: 2, 5, 8, 12, 15, 22, 28, 42, 58...
- **Median: 12 stars**
- **75th percentile: 28 stars**
- **90th percentile: 65 stars**

**Hard threshold of "50 stars" would reject 90%+ of workflows!**

---

## The Solution: Percentile Ranking

### Core Concept

**Instead of:** "Is it above threshold X?"
**Ask:** "Where does it rank WITHIN this collection?"

```python
# Statistical approach
def percentile_rank(value, all_values):
    """Returns what percentile this value is (0-100)"""
    count_below = sum(1 for x in all_values if x < value)
    count_equal = sum(1 for x in all_values if x == value)
    return ((count_below + 0.5 * count_equal) / len(all_values)) * 100
```

### Example Calculation

**Collection:** [5, 8, 12, 15, 22, 28, 42, 58]

**Value: 22 stars**
```python
count_below = 4  # (5, 8, 12, 15 are below 22)
count_equal = 1  # (one instance of 22)
total = 8

percentile = ((4 + 0.5 * 1) / 8) * 100
          = (4.5 / 8) * 100
          = 56.25th percentile
```

**Interpretation:** This resource is better than 56% of the collection.

---

## Why Percentiles Work

### Adapts to Any Niche

**N8n (small community):**
- 15 stars → 58th percentile → KEEP ✅
- Above median → Quality indicator

**React (huge community):**
- 15 stars → 3rd percentile → REJECT ❌
- Way below median → Poor quality indicator

**Same absolute value, different context, different meaning.**

### Scale Independent

Works for:
- 50 resources
- 500 resources
- 5,000 resources

**Cutoff adjusts to collection size:**
- 50 items → Keep top 50% (25 items)
- 5000 items → Keep top 15% (750 items)

### Statistically Sound

Based on:
- Actual data distribution
- Median and quartiles
- Standard statistical measures

Not based on:
- Gut feeling
- Arbitrary numbers
- One-size-fits-all assumptions

---

## Composite Scoring

### Multiple Metrics Problem

Can't just use stars. Also need:
- Recency (is it current?)
- Forks (is it used?)
- File size (is it substantial?)

**Solution:** Weight different percentiles

```python
def composite_score(resource, all_data, weights):
    # Get percentile for each metric
    stars_pct = percentile_rank(resource.stars, all_data.all_stars)
    forks_pct = percentile_rank(resource.forks, all_data.all_forks)
    size_pct = percentile_rank(resource.size, all_data.all_sizes)
    
    # Recency is absolute (not relative)
    recency = calculate_recency_score(resource.updated_at)
    
    # Weighted average
    composite = (
        recency * weights['recency'] +      # 40%
        stars_pct * weights['stars'] +      # 35%
        forks_pct * weights['forks'] +      # 15%
        size_pct * weights['file_size']     # 10%
    )
    
    return composite  # 0-100 score
```

### Weight Justification

**Why recency gets 40%:**
- Tech code ages FAST
- 18-month-old workflow often obsolete
- More important than popularity

**Why stars gets 35%:**
- Strong signal of quality
- Crowd validation
- But can be gamed (hence not 50%+)

**Why forks gets 15%:**
- Actual usage indicator
- People building on it
- Fewer people fork than star (lower weight)

**Why file size gets 10%:**
- Basic quality check only
- Filters trivial examples
- Not predictive of quality alone

See `references/platform-weights.md` for detailed rationale.

---

## Adaptive Cutoffs

### Why Adjust by Collection Size?

**Small collection (100 items):**
- Can manually review 50 items
- Be generous: keep top 50%
- Cutoff: 50th percentile

**Large collection (3000 items):**
- Can't manually review 1500 items
- Be strict: keep top 15%
- Cutoff: 85th percentile

### Cutoff Formula

```python
def determine_cutoff(collection_size):
    if collection_size <= 100:
        return 50  # Keep half
    elif collection_size <= 500:
        return 60  # Keep 40%
    elif collection_size <= 1000:
        return 70  # Keep 30%
    elif collection_size <= 3000:
        return 80  # Keep 20%
    else:
        return 85  # Keep 15%
```

**Goal:** Reduce to manageable size while preserving quality.

---

## Complete Example

### Scenario: 300 N8n Workflows

**Step 1: Fetch all 300**

**Step 2: Calculate statistics**
```python
all_stars = [2, 3, 5, 8, 8, 12, 15, 15, 22, 28, ...]  # 300 values
all_forks = [0, 1, 1, 2, 2, 3, 4, 6, 8, 12, ...]      # 300 values
all_sizes = [800, 1200, 2500, 3200, 4500, ...]         # 300 values

stats = {
    'stars_median': 12,
    'stars_p75': 28,
    'stars_p90': 65,
    'forks_median': 3,
    'size_median': 4200
}
```

**Step 3: Score workflow X**
```python
workflow_X = {
    'stars': 22,
    'forks': 6,
    'size': 6500,
    'updated_at': '2025-10-15'
}

# Calculate percentiles
stars_pct = percentile_rank(22, all_stars)  # → 72nd percentile
forks_pct = percentile_rank(6, all_forks)   # → 65th percentile
size_pct = percentile_rank(6500, all_sizes) # → 68th percentile
recency = 85  # Updated 4 months ago

# Composite score
composite = (85 * 0.40) + (72 * 0.35) + (65 * 0.15) + (68 * 0.10)
         = 34.0 + 25.2 + 9.75 + 6.8
         = 75.75 / 100
```

**Step 4: Apply cutoff**
```python
cutoff = determine_cutoff(300)  # → 70th percentile

if composite >= cutoff:
    KEEP  # 75.75 >= 70 ✅
else:
    REJECT
```

**Result:** Workflow X is kept (top 30%)

---

## Advantages Summary

### ✅ Niche-Aware
- N8n with 20 stars = top tier
- React with 20 stars = poor
- System knows the difference

### ✅ Platform-Appropriate
- Weights what matters per platform
- GitHub ≠ Reddit ≠ YouTube

### ✅ Scale-Independent
- Works for 50 or 5000 items
- Adaptive cutoffs

### ✅ No Arbitrary Thresholds
- Based on actual distribution
- Statistical foundation

### ✅ Transparent
- Shows percentile breakdown
- Explains scoring
- User understands why each scored that way

---

## Comparison: Hard vs Statistical

| Aspect | Hard Thresholds | Statistical Percentiles |
|--------|----------------|------------------------|
| **Niche handling** | ❌ Fails for small communities | ✅ Adapts automatically |
| **Mainstream handling** | ✅ Works | ✅ Works |
| **Statistical basis** | ❌ None | ✅ Median, quartiles |
| **Transparency** | ⚠️ "Why 50?" | ✅ "72nd percentile" |
| **Maintenance** | ❌ Constant tweaking | ✅ Self-adjusting |
| **Cross-platform** | ❌ Different per platform | ✅ Same logic, different weights |

---

## Limitations

### What Percentiles DON'T Solve

**Still can't detect:**
- Code quality (need to read code)
- Accuracy (might be popular but wrong)
- Security issues
- Whether it actually works

**But CAN detect:**
- Relative popularity
- Relative engagement
- Relative recency
- Relative substance

**Percentiles filter by ENGAGEMENT. Phase 2 filters by QUALITY.**

---

## Implementation Notes

### Percentile Calculation

```python
def percentile(data, p):
    """Calculate pth percentile of dataset"""
    if not data:
        return 0
    sorted_data = sorted(data)
    index = (len(sorted_data) - 1) * p / 100
    floor = int(index)
    ceil = floor + 1
    if ceil >= len(sorted_data):
        return sorted_data[-1]
    
    # Linear interpolation
    return sorted_data[floor] + (sorted_data[ceil] - sorted_data[floor]) * (index - floor)
```

### Efficiency

**Time complexity:** O(n log n) for sorting
**Space complexity:** O(n) for storing values

**For 3000 items:**
- Calculation: <1 second
- Total filtering: ~10 minutes (API calls dominate)

---

## When to Use vs Not Use

### ✅ Use Statistical Filtering When:
- Large collection (100+)
- Niche community
- Cross-platform comparison needed
- Want objective ranking

### ❌ Don't Use When:
- Very small (<50 items)
- Need deep quality assessment
- Already have hard requirements (e.g., "must be from 2025")
- Manual curation already done

---

## Further Reading

- `references/github.md` - GitHub-specific implementation
- `references/reddit.md` - Reddit-specific implementation
- `references/platform-weights.md` - Why weights are chosen

# LLM Council — README

Technical reference for the llm-council skill. Covers how the parallelism works, token costs, environment requirements, script usage, and HTML template placeholders.

Claude reads `SKILL.md` during a session. This file is for developers and operators who want to understand the machinery or run scripts manually.

---

## How It Works — The Full Picture

The council runs in four rounds:

```
Round 1 — 5 Advisors (parallel)
  Each advisor has a distinct thinking lens.
  All 5 run simultaneously. Isolated contexts. No cross-contamination.
         ↓
Round 2 — Anonymization
  Script shuffles advisor → letter mapping (A-E).
  Reveal key saved to disk separately. Reviewer prompts never see the mapping.
         ↓
Round 3 — 5 Reviewers (parallel)
  Each reviewer has a distinct critical lens.
  All 5 run simultaneously on the anonymized responses.
  Evidence Auditor / Constraints Checker / Second-Order Thinker /
  Stakeholder Scout / Assumption Excavator
         ↓
Round 4 — Chairman (single)
  Receives everything de-anonymized.
  Produces the final verdict.
```

---

## How Parallelism Works

The original Karpathy methodology dispatches queries to multiple models simultaneously. This skill implements the same pattern inside Claude Code using Python's `asyncio` + the `claude -p` subprocess interface.

### The mechanism

```python
# scripts/run_council.py (simplified)

async def call_claude(prompt: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        "claude", "-p", prompt,
        stdout=asyncio.subprocess.PIPE,
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()

async def main():
    # asyncio.gather = launch all 5 simultaneously, await all results
    results = await asyncio.gather(
        call_claude(contrarian_prompt),
        call_claude(firstp_prompt),
        call_claude(expansionist_prompt),
        call_claude(outsider_prompt),
        call_claude(executor_prompt),
    )
```

`asyncio.gather` launches all subprocess calls at the same time. Total wall time ≈ time of the slowest single call, not the sum of all calls. The same pattern runs for the 5 reviewers.

### Why not use Claude Code's Task tool?

The Task tool can spawn parallel sub-agents but Claude decides whether to parallelize based on context — it's not guaranteed. `asyncio.gather` + subprocess is deterministic: always parallel, always isolated, output captured programmatically for anonymization.

### Why this matters for quality

Without parallelism, each advisor's response sits in Claude's context when the next advisor runs. Advisor 2 has read Advisor 1's output. The independence guarantee collapses. The peer review step — the core of Karpathy's insight — only works if responses are genuinely independent. `asyncio.gather` + `claude -p` subprocesses gives each agent a clean, isolated context.

---

## Token Cost

Roughly **~30,000 tokens per council session**.

| Round | Calls | Input each | Output each | Subtotal |
|---|---|---|---|---|
| 5 advisors | 5 | ~500 | ~250 | ~3,750 |
| 5 reviewers | 5 | ~3,500 | ~200 | ~18,500 |
| 1 chairman | 1 | ~7,000 | ~600 | ~7,600 |

The reviewer round is the expensive part — each reviewer receives all 5 advisor responses as input. Unavoidable if you want genuine blind review.

At Anthropic API pricing for Sonnet (~$3/$15 per million input/output tokens): **~$0.10–0.15 per session**.

On Pro/Max subscriptions: each `claude -p` call counts as a separate message. One council session = ~11 messages (5 advisors + 5 reviewers + 1 chairman).

**Compared to the original skill:** same token cost, better quality. The original had the same architecture but wasted the reviewer round with 5 identical prompts producing noise variation instead of signal. The improved version uses the same budget with distinct reviewer lenses.

---

## Environment Requirements

**Claude Code (primary, recommended)**
- `claude` CLI is already present — it's the environment you're in
- Python 3.10+ (stdlib only, no pip installs)
- Works on Pro, Max, and API key setups
- True parallelism, full script pipeline, HTML reports

**Claude.ai (fallback)**
- No `claude -p`, no scripts
- Sequential execution with contamination prevention protocol
- Manual anonymization
- Markdown report only (no HTML)
- Lower output quality — advisor independence not guaranteed

---

## Running the Council

### Normal usage (Claude handles it)

Just trigger the skill naturally in Claude Code:
> "Council this: should I launch X or Y?"

Claude frames the question and runs:
```bash
python scripts/run_council.py --question "framed question"
```

No flags needed for normal use.

### Manual / power-user usage

```bash
# Basic
python scripts/run_council.py --question "Your framed question here"

# From a file (for long questions)
python scripts/run_council.py --question-file my-question.txt

# Reproducible anonymization (same shuffle every run)
python scripts/run_council.py --question "..." --seed 42

# Custom output directory
python scripts/run_council.py --question "..." --output-dir ./my-council
```

### Output files

Written to `council-output-[timestamp]/`:
```
council-output-20250415-143022/
├── advisor-responses.json      ← raw advisor outputs
├── council-anon-[ts].json      ← anonymization mapping + reveal key
├── reviewer-outputs.json       ← raw reviewer outputs
├── chairman-input.md           ← assembled chairman prompt (for inspection)
├── council-report.md           ← final markdown report (the artifact)
└── council-report.html         ← visual HTML report
```

### Anonymizer standalone

```bash
# From JSON file
python scripts/anonymize.py --responses advisor-responses.json

# Reproducible
python scripts/anonymize.py --responses advisor-responses.json --seed 42

# From stdin
cat advisor-responses.json | python scripts/anonymize.py
```

Input format:
```json
{
  "contrarian": "response text...",
  "first_principles": "response text...",
  "expansionist": "response text...",
  "outsider": "response text...",
  "executor": "response text..."
}
```

Output: anonymized block ready to paste into reviewer prompts + reveal key. Saves `council-anon-[timestamp].json`.

---

## Why the Reviewer Round Has 5 Distinct Prompts

The original skill used one reviewer prompt repeated 5 times. Five identical calls produce noise variation — slightly different answers to the same questions driven by LLM randomness, not genuine independent signal.

The improved reviewers each have one focused job:

| Reviewer | Lens | What they catch |
|---|---|---|
| Evidence Auditor | Which claims are supported vs. asserted? | Unsupported confident assertions |
| Constraints Checker | Which advice ignores real-world limits? | Frictionless-world recommendations |
| Second-Order Thinker | What happens after the action succeeds? | Downstream effects, new problems created |
| Stakeholder Scout | Who is missing from the analysis? | Affected parties nobody mentioned |
| Assumption Excavator | What has to be true for this to hold? | Load-bearing hidden assumptions |

Every reviewer also answers: *what did ALL five advisors miss?* — the universal blind-spot question, kept as one short item, not a full third question.

Same token cost. Genuinely different signal.

---

## Why Anonymization Uses a Script

Manual anonymization (asking Claude to shuffle names to letters) is unreliable. Claude tends to "remember" which advisor said what even after anonymization, defeating the blind review. The script uses an isolated `random.Random(seed)` instance — never touches global state — and saves the reveal key to a separate file. Reviewer prompts never contain the mapping.

---

## HTML Template Placeholder Reference

`assets/report-template.html` uses `{{PLACEHOLDER}}` substitution. Full reference:

| Placeholder | Contents |
|---|---|
| `{{COUNCIL_TITLE}}` | First 80 chars of question (for `<title>` tag) |
| `{{TIMESTAMP}}` | Human-readable datetime |
| `{{QUESTION}}` | Full framed question (HTML-escaped) |
| `{{CHAIRMAN_OUTPUT}}` | Full chairman synthesis (HTML paragraphs) |
| `{{CONTRARIAN_RESPONSE}}` | Contrarian response (HTML paragraphs) |
| `{{FIRSTP_RESPONSE}}` | First Principles Thinker response |
| `{{EXPANSIONIST_RESPONSE}}` | Expansionist response |
| `{{OUTSIDER_RESPONSE}}` | Outsider response |
| `{{EXECUTOR_RESPONSE}}` | Executor response |
| `{{PEER_REVIEWS_HTML}}` | Full HTML block for all 5 reviewer cards |
| `{{MARKDOWN_CONTENT}}` | Full raw markdown report (HTML-escaped, in `<pre>`) |

### Peer review card pattern (for `{{PEER_REVIEWS_HTML}}`)

```html
<div class="review-card">
  <div class="review-head" onclick="this.parentElement.classList.toggle('open')">
    <span>Reviewer N — Lens Name</span>
    <button class="toggle-btn">expand</button>
  </div>
  <div class="review-body"><p>Review text...</p></div>
</div>
```

### Text → HTML conversion

- HTML-escape `&`, `<`, `>`
- `**bold**` → `<strong>bold</strong>`
- `*italic*` → `<em>italic</em>`
- Double newlines → `<p>` blocks

---

## Known Limitations

**Chairman section parsing:** `run_council.py` passes the full chairman output as one block. The HTML renders it together rather than in per-section slots. A future improvement would parse the chairman's structured markdown headers into separate verdict sections for cleaner HTML display.

**Rate limits:** 10 parallel `claude -p` calls may hit limits on some plans. If calls fail, re-run — the output directory preserves completed steps. A future `--sequential` flag would help here.

**Claude.ai quality gap:** Sequential execution means advisors are not truly independent. The contamination prevention protocol (write-once, don't re-read) mitigates but doesn't eliminate this. For high-stakes decisions, run in Claude Code.

---
name: llm-council
description: "Run decisions through 5 independent AI advisors with blind peer review and chairman synthesis. Trigger: 'council this', 'pressure-test this', 'stress-test this', 'debate this', or when user presents a complex decision with real trade-offs."
---

# LLM Council

## When to Use This Skill

**MANDATORY TRIGGERS:** 'council this', 'run the council', 'war room this', 'pressure-test this', 'stress-test this', 'debate this'

**STRONG TRIGGERS:** 'should I X or Y', 'which option', 'what would you do', 'is this the right move', 'validate this', 'get multiple perspectives', 'I can't decide', 'I'm torn between'

**DO NOT trigger on:** simple yes/no questions, factual lookups, casual 'should I' without meaningful trade-offs

**DO trigger when:** user presents a genuine decision with stakes, multiple options, and context suggesting they want it pressure-tested from multiple angles

Good: "Should I launch a $97 workshop or a $497 course?" / "Which positioning angle is strongest?" / "I'm thinking of pivoting from X to Y. Am I crazy?"

Bad: "What's the capital of France?" / "Write me a tweet" / "Summarize this article"

---

Five independent advisors. Blind peer review. One chairman synthesizes the verdict.

Adapted from Andrej Karpathy's LLM Council: dispatch queries to multiple independent agents, have them peer-review each other anonymously, then a chairman produces the final answer. This skill implements that with five distinct thinking lenses instead of different models.

**The council is for questions where being wrong is expensive.**

---

## Environment

**Claude Code (primary):** True parallel dispatch via `asyncio.gather` + `claude -p` subprocesses. All 5 advisors run simultaneously; all 5 reviewers run simultaneously. This is the intended environment. See `README.md` for mechanics.

**Claude.ai (fallback):** No true parallelism. Run advisors sequentially with strict contamination prevention (see Step 2 protocol below).

---

## Step 1 — Frame the Question

### 1A. Scan for context

Before framing, do a genuine scan of the project directory — not a fixed checklist, a real read of what's there.

**Step 1: List the directory tree.** Run `ls -la` on the project root and obvious subdirectories (`memory/`, `docs/`, `data/`, `research/`). Get a full picture before deciding what to read.

**Step 2: Read what's relevant to this specific question.** Use the question type to guide priority:

- Always read if present: `CLAUDE.md` / `claude.md` — business context that improves every council
- Always read: any files the user explicitly referenced or attached
- Always check: previous council transcripts — avoid re-counciling the same ground
- Pricing/launch decisions → revenue data, past launch results, audience research, conversion numbers
- Positioning/strategy decisions → competitor docs, brand guidelines, past messaging experiments
- Hiring/build/buy decisions → budget docs, org charts, existing tool lists, role descriptions
- Product decisions → user research, analytics, roadmap docs, customer feedback

**Step 3: Apply a hard cap.** Read at most 5 files beyond `CLAUDE.md`. If more look relevant, prioritize by recency and specificity — a recent postmortem beats a 2-year-old strategy deck. Skim first (first 50 lines), read fully only if clearly useful.

**The goal:** advisors should give advice grounded in your actual numbers, constraints, and history — not generic advice that applies to anyone. A council without context is expensive noise. If the directory is empty or nothing relevant exists, go straight to 1B.

### 1B. Clarify if needed

If context is thin and the question is ambiguous, ask targeted clarifying questions based on what the question is *about*. Examples:

**For a pricing/launch decision:**
- What's your current audience size and how warm are they?
- Have you sold anything in this price range before? What converted?
- What's your timeline — is there a launch window or is this open-ended?

**For a positioning/messaging decision:**
- Who is this actually for? Be specific (not "entrepreneurs" — which ones, at what stage)?
- What have you tried that didn't land?
- Who's winning in this space right now and why?

**For a build/hire/invest decision:**
- What resources do you actually have (time, money, people)?
- What does success look like in 90 days?
- What's the cost of doing nothing for 3 months?

Ask max 3 questions. Don't ask questions you can infer from context.

### 1C. Write the framed question

Take the user's raw question + context and produce a clear, neutral prompt all advisors receive. Include:
1. The core decision or question
2. Key context from the user's message
3. Relevant context from workspace files (numbers, constraints, past results)
4. What's at stake — why this decision matters

Do not add your opinion. Do not steer it. Make it specific enough that advisors can give grounded answers, not generic advice.

---

## Step 2 — Convene the Council (Advisors)

Read `references/advisor-prompts.md` now. It contains the expert-voiced prompt templates for all five advisors:
- **The Contrarian** — finds the fatal flaw
- **The First Principles Thinker** — strips assumptions, reframes the question
- **The Expansionist** — finds upside and adjacent opportunities being missed
- **The Outsider** — responds with fresh eyes, no prior context
- **The Executor** — only cares about what actually happens Monday morning

### Claude Code

```bash
python scripts/run_council.py --question "YOUR FRAMED QUESTION"
```

Dispatches all 5 advisors in parallel via `asyncio.gather` + `claude -p` subprocesses. Handles anonymization, parallel peer review, and report generation automatically.

### Claude.ai Protocol

Run advisors sequentially with this strict contamination prevention protocol:

1. Write the Contrarian response. **Stop. Do not re-read it.**
2. Write the First Principles response. **Stop. Do not re-read either.**
3. Continue for all five advisors.
4. Only after all five are written: read them together for the review step.

The contamination risk is real: once advisor 1's output is in your context, you will subtly pull toward it. Treat each response as write-once.

---

## Step 3 — Peer Review (Blind)

Read `references/reviewer-chairman-prompts.md` for the reviewer prompt templates.

### Anonymization

**Claude Code:** `run_council.py` handles this automatically via `scripts/anonymize.py`. Shuffles advisor → letter mapping with isolated RNG, saves reveal key to `council-anon-[timestamp].json`.

**Claude.ai:** Manually assign letters to advisors. Write the mapping down (e.g. A=Expansionist, B=Contrarian, C=Executor, D=Outsider, E=FirstP). Keep the reveal key for Step 4.

### Run the reviewers

Each of the 5 reviewers gets all 5 anonymized responses. Each has a distinct critical lens:
- **Reviewer 1** — Evidence Auditor: which claims are supported vs. asserted?
- **Reviewer 2** — Constraints Checker: which advice ignores real-world limits?
- **Reviewer 3** — Second-Order Thinker: what happens after the action succeeds?
- **Reviewer 4** — Stakeholder Scout: whose perspective is missing entirely?
- **Reviewer 5** — Assumption Excavator: what has to be true for any of this to hold?

Every reviewer also answers: what did ALL five advisors miss? This universal question, run through five independent isolated contexts, is where the most valuable blind spots surface.

**Claude Code:** `run_council.py` dispatches all 5 reviewers in parallel (same `asyncio.gather` mechanism).

**Claude.ai:** Run sequentially. Same contamination protocol as Step 2.

---

## Step 4 — Chairman Synthesis

Read `references/reviewer-chairman-prompts.md` for the chairman prompt template.

De-anonymize using the reveal key. The chairman receives all 5 advisor responses (named) and all 5 peer reviews, and produces the final verdict:

1. **Where the Council Agrees** — high-confidence convergences
2. **Where the Council Clashes** — genuine disagreements, both sides named
3. **What the Peer Review Caught** — the "nobody said this" findings
4. **The Recommendation** — a real answer, not "it depends"
5. **The One Thing to Do First** — one concrete next step

The chairman can disagree with the majority if the minority argument is stronger. No hedging.

---

## Step 5 — Generate Reports

Two outputs always produced:

**`council-report.md`** — Full markdown: question, verdict, all advisor responses, all peer reviews. Always generated. This is the permanent record.

**`council-report.html`** — Visual report from `assets/report-template.html`. Collapsible advisor cards, peer review section, embedded raw markdown.

**Claude Code:** `run_council.py` generates both automatically.

**Claude.ai:** Generate markdown inline. Populate HTML template manually using placeholder reference in `README.md`.

---

## Important Notes

- **The chairman can dissent.** 4 of 5 say go, but the 1 dissenter has the stronger argument — chairman backs the dissenter.
- **Don't council trivial questions.** One right answer → just answer it.
- **The peer review round is the differentiator.** Five independent lenses on the same blind spot question — this is where the real signal comes from.
- **The markdown report always ships.** Even if HTML fails, the `.md` is the artifact.

---

## File Reference

```
llm-council/
├── SKILL.md                              ← you are here
├── README.md                             ← parallelism mechanics, token costs, placeholder reference
├── references/
│   ├── advisor-prompts.md                ← load in Step 2
│   └── reviewer-chairman-prompts.md      ← load in Steps 3 & 4
├── assets/
│   └── report-template.html              ← HTML report template
└── scripts/
    ├── run_council.py                     ← full parallel pipeline (Claude Code)
    └── anonymize.py                       ← standalone anonymizer
```

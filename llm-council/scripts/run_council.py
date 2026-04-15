#!/usr/bin/env python3
"""
run_council.py — LLM Council parallel dispatcher

Runs all 5 advisors simultaneously via `claude -p`, then all 5 peer reviewers
simultaneously, then produces outputs for the chairman step.

Usage:
    python run_council.py --question "Your framed question here"
    python run_council.py --question-file framed-question.txt
    python run_council.py --question "..." --seed 42  # reproducible anonymization

Requirements:
    - claude CLI installed and authenticated (`claude --version` should work)
    - Python 3.10+

Output files (written to ./council-output-[timestamp]/):
    - advisor-responses.json       raw advisor outputs
    - council-anon-[ts].json       anonymization mapping
    - reviewer-outputs.json        raw reviewer outputs  
    - chairman-input.md            assembled prompt for chairman (Claude reads this)
    - council-report.md            final markdown report (chairman fills this in)
    - council-report.html          visual HTML report (generated from template)
"""

import asyncio
import json
import os
import random
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
AGENTS_DIR = SKILL_DIR / "agents"
ASSETS_DIR = SKILL_DIR / "assets"

ADVISOR_PROMPTS_FILE = AGENTS_DIR / "advisor-prompts.md"
REVIEWER_CHAIRMAN_FILE = AGENTS_DIR / "reviewer-chairman-prompts.md"
HTML_TEMPLATE_FILE = ASSETS_DIR / "report-template.html"

# ── Advisor definitions ───────────────────────────────────────────────────────

ADVISORS = ["contrarian", "first_principles", "expansionist", "outsider", "executor"]
LETTERS = ["A", "B", "C", "D", "E"]

DISPLAY_NAMES = {
    "contrarian":      "The Contrarian",
    "first_principles": "The First Principles Thinker",
    "expansionist":    "The Expansionist",
    "outsider":        "The Outsider",
    "executor":        "The Executor",
}

# ── Prompt extraction ─────────────────────────────────────────────────────────

def extract_advisor_prompts(question: str) -> dict[str, str]:
    """
    Reads advisor-prompts.md and extracts each advisor's prompt block,
    substituting the framed question.
    """
    raw = ADVISOR_PROMPTS_FILE.read_text()
    prompts = {}

    sections = {
        "contrarian":      "## THE CONTRARIAN",
        "first_principles": "## THE FIRST PRINCIPLES THINKER",
        "expansionist":    "## THE EXPANSIONIST",
        "outsider":        "## THE OUTSIDER",
        "executor":        "## THE EXECUTOR",
    }

    lines = raw.split("\n")
    current = None
    in_block = False
    block_lines = []

    for line in lines:
        # Check for section header
        for key, header in sections.items():
            if line.strip() == header:
                # Save previous block
                if current and block_lines:
                    prompts[current] = "\n".join(block_lines).strip()
                current = key
                in_block = False
                block_lines = []
                break

        if current:
            if line.strip() == "```" and not in_block:
                in_block = True
            elif line.strip() == "```" and in_block:
                in_block = False
            elif in_block:
                block_lines.append(line)

    # Save last block
    if current and block_lines:
        prompts[current] = "\n".join(block_lines).strip()

    # Substitute question
    for key in prompts:
        prompts[key] = prompts[key].replace("[FRAMED QUESTION]", question)

    missing = [a for a in ADVISORS if a not in prompts]
    if missing:
        raise ValueError(f"Could not extract prompts for: {missing}")

    return prompts


REVIEWER_HEADERS = [
    "## REVIEWER 1 — The Evidence Auditor",
    "## REVIEWER 2 — The Constraints Checker",
    "## REVIEWER 3 — The Second-Order Thinker",
    "## REVIEWER 4 — The Stakeholder Scout",
    "## REVIEWER 5 — The Assumption Excavator",
]

REVIEWER_LABELS = [
    "Reviewer 1 — Evidence Auditor",
    "Reviewer 2 — Constraints Checker",
    "Reviewer 3 — Second-Order Thinker",
    "Reviewer 4 — Stakeholder Scout",
    "Reviewer 5 — Assumption Excavator",
]

def build_reviewer_prompts(question: str, anonymized: dict[str, str]) -> list[str]:
    """
    Extracts all 5 distinct reviewer prompts and injects anonymized responses.
    Each reviewer has a different critical lens — not the same prompt repeated.
    All 5 run in parallel via asyncio.gather with isolated subprocess contexts.
    """
    raw = REVIEWER_CHAIRMAN_FILE.read_text()

    # Build the anonymized responses block (same content, injected into each)
    responses_block = "\n\n".join(
        f"**Response {letter}:**\n{anonymized[letter]}" for letter in LETTERS
    )

    # Canonical placeholder used in all 5 templates
    placeholder_block = "\n\n".join(
        f"**Response {letter}:**\n[response]" for letter in LETTERS
    )

    prompts = []
    for i, header in enumerate(REVIEWER_HEADERS):
        start = raw.find(header)
        if i + 1 < len(REVIEWER_HEADERS):
            end = raw.find(REVIEWER_HEADERS[i + 1])
        else:
            end = raw.find("## CHAIRMAN SYNTHESIS PROMPT")

        section = raw[start:end]
        block_start = section.find("```\n") + 4
        block_end = section.rfind("\n```")
        template = section[block_start:block_end]

        template = template.replace("[FRAMED QUESTION]", question)
        template = template.replace(placeholder_block, responses_block)
        prompts.append(template)

    if len(prompts) != 5:
        raise ValueError(f"Expected 5 reviewer prompts, extracted {len(prompts)}")

    return prompts


def build_chairman_prompt(question: str, advisor_responses: dict, peer_reviews: list[str], reveal_key: dict) -> str:
    """Assembles the chairman prompt with de-anonymized advisor responses and all peer reviews."""
    raw = REVIEWER_CHAIRMAN_FILE.read_text()

    start = raw.find("## CHAIRMAN SYNTHESIS PROMPT")
    block_start = raw.find("```\n", start) + 4
    block_end = raw.rfind("\n```")
    template = raw[block_start:block_end]

    template = template.replace("[FRAMED QUESTION]", question)

    for advisor in ADVISORS:
        display = DISPLAY_NAMES[advisor]
        template = template.replace(f"**{display}:**\n[response]", f"**{display}:**\n{advisor_responses[advisor]}")

    # Replace each named reviewer slot directly
    for i, label in enumerate(REVIEWER_LABELS):
        template = template.replace(
            f"**{label}:**\n[response]",
            f"**{label}:**\n{peer_reviews[i]}"
        )

    return template

# ── Anonymization ─────────────────────────────────────────────────────────────

def anonymize(responses: dict, seed: int | None = None) -> tuple[dict, dict]:
    """
    Returns:
        anonymized: {letter: response_text}
        reveal_key: {letter: advisor_key}
    """
    rng = random.Random(seed)
    shuffled = ADVISORS[:]
    rng.shuffle(shuffled)

    anonymized = {letter: responses[advisor] for letter, advisor in zip(LETTERS, shuffled)}
    reveal_key = {letter: advisor for letter, advisor in zip(LETTERS, shuffled)}
    return anonymized, reveal_key

# ── Claude subprocess caller ──────────────────────────────────────────────────

async def call_claude(prompt: str, label: str) -> str:
    """
    Calls `claude -p <prompt>` as an async subprocess.
    This is what enables true parallelism — asyncio.gather launches all
    subprocess calls simultaneously and awaits all results together.
    """
    print(f"  → dispatching: {label}")
    proc = await asyncio.create_subprocess_exec(
        "claude", "-p", prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        err = stderr.decode().strip()
        print(f"  ✗ {label} failed: {err}", file=sys.stderr)
        return f"[ERROR: {label} subprocess failed — {err}]"

    result = stdout.decode().strip()
    print(f"  ✓ done: {label}")
    return result

# ── Report generation ─────────────────────────────────────────────────────────

def generate_markdown_report(question: str, advisor_responses: dict,
                              peer_reviews: list, chairman_output: str,
                              timestamp: str) -> str:
    lines = [
        f"# Council Report",
        f"",
        f"**Generated:** {timestamp}",
        f"",
        f"---",
        f"",
        f"## The Question",
        f"",
        question,
        f"",
        f"---",
        f"",
        f"## Chairman's Verdict",
        f"",
        chairman_output,
        f"",
        f"---",
        f"",
        f"## Advisor Responses",
        f"",
    ]
    for advisor in ADVISORS:
        lines += [
            f"### {DISPLAY_NAMES[advisor]}",
            f"",
            advisor_responses[advisor],
            f"",
        ]

    lines += [
        f"---",
        f"",
        f"## Peer Reviews",
        f"",
    ]
    for i, review in enumerate(peer_reviews, 1):
        lines += [f"### Reviewer {i}", f"", review, f""]

    return "\n".join(lines)


def generate_html_report(question: str, md_content: str, chairman_output: str,
                         advisor_responses: dict, timestamp: str) -> str:
    """Reads the HTML template and substitutes all placeholders."""
    if not HTML_TEMPLATE_FILE.exists():
        print("  ⚠ HTML template not found, skipping HTML report")
        return ""

    html = HTML_TEMPLATE_FILE.read_text()

    # Escape for HTML
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def md_to_paragraphs(text):
        """Minimal markdown → HTML: paragraphs and bold."""
        import re
        text = esc(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        paras = [f"<p>{p.strip()}</p>" for p in text.split("\n\n") if p.strip()]
        return "\n".join(paras)

    html = html.replace("{{COUNCIL_TITLE}}", esc(question[:80]))
    html = html.replace("{{TIMESTAMP}}", timestamp)
    html = html.replace("{{QUESTION}}", esc(question))
    html = html.replace("{{CHAIRMAN_OUTPUT}}", md_to_paragraphs(chairman_output))

    for advisor in ADVISORS:
        key = advisor.upper()
        html = html.replace(f"{{{{{key}_RESPONSE}}}}", md_to_paragraphs(advisor_responses[advisor]))

    # Embed full markdown in the raw-md section
    html = html.replace("{{MARKDOWN_CONTENT}}", esc(md_content))

    return html

# ── Main pipeline ─────────────────────────────────────────────────────────────

async def run_council(question: str, seed: int | None = None, output_dir: Path | None = None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ts_slug = datetime.now().strftime("%Y%m%d-%H%M%S")

    if output_dir is None:
        output_dir = Path(f"council-output-{ts_slug}")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n╔══════════════════════════════════════════╗")
    print(f"  LLM Council — {ts_slug}")
    print(f"╚══════════════════════════════════════════╝\n")

    # ── Step 1: Extract advisor prompts ──────────────────────────────────────
    print("▸ Extracting advisor prompts...")
    advisor_prompts = extract_advisor_prompts(question)

    # ── Step 2: Dispatch all 5 advisors IN PARALLEL ──────────────────────────
    print("\n▸ Convening council — dispatching 5 advisors in parallel...")
    advisor_tasks = [
        call_claude(advisor_prompts[advisor], DISPLAY_NAMES[advisor])
        for advisor in ADVISORS
    ]
    # asyncio.gather = the actual parallelism mechanism
    # All 5 claude -p calls are launched simultaneously here
    advisor_results = await asyncio.gather(*advisor_tasks)
    advisor_responses = dict(zip(ADVISORS, advisor_results))

    # Save
    (output_dir / "advisor-responses.json").write_text(
        json.dumps(advisor_responses, indent=2)
    )
    print(f"  Saved: advisor-responses.json")

    # ── Step 3: Anonymize ────────────────────────────────────────────────────
    print("\n▸ Anonymizing for blind peer review...")
    anonymized, reveal_key = anonymize(advisor_responses, seed=seed)
    anon_data = {
        "timestamp": ts_slug,
        "anonymized": anonymized,
        "reveal_key": reveal_key,
        "display_names": {k: DISPLAY_NAMES[v] for k, v in reveal_key.items()},
    }
    anon_file = output_dir / f"council-anon-{ts_slug}.json"
    anon_file.write_text(json.dumps(anon_data, indent=2))
    print(f"  Reveal key: {', '.join(f'{l}={DISPLAY_NAMES[v]}' for l, v in reveal_key.items())}")
    print(f"  Saved: council-anon-{ts_slug}.json")

    # ── Step 4: Dispatch all 5 reviewers IN PARALLEL ─────────────────────────
    # Each reviewer has a DISTINCT prompt/lens — not the same prompt 5 times.
    # All 5 run simultaneously via asyncio.gather with isolated subprocess contexts.
    print("\n▸ Running peer review — dispatching 5 reviewers in parallel...")
    print("  (Each reviewer has a distinct lens: Evidence, Constraints, Second-Order, Stakeholder, Assumptions)")
    reviewer_prompts = build_reviewer_prompts(question, anonymized)
    reviewer_tasks = [
        call_claude(prompt, REVIEWER_LABELS[i])
        for i, prompt in enumerate(reviewer_prompts)
    ]
    peer_reviews = await asyncio.gather(*reviewer_tasks)

    (output_dir / "reviewer-outputs.json").write_text(
        json.dumps(list(peer_reviews), indent=2)
    )
    print(f"  Saved: reviewer-outputs.json")

    # ── Step 5: Build chairman input ─────────────────────────────────────────
    print("\n▸ Assembling chairman brief...")
    chairman_prompt = build_chairman_prompt(question, advisor_responses, list(peer_reviews), reveal_key)
    chairman_input_file = output_dir / "chairman-input.md"
    chairman_input_file.write_text(
        f"# Chairman Brief\n\n{chairman_prompt}"
    )
    print(f"  Saved: chairman-input.md")
    print(f"\n  ┌─────────────────────────────────────────────────────┐")
    print(f"  │  The chairman step requires YOUR judgment.          │")
    print(f"  │  Read chairman-input.md and write the verdict.      │")
    print(f"  │  Or: pass it back to Claude with the chairman       │")
    print(f"  │  prompt from references/reviewer-chairman-prompts.md    │")
    print(f"  └─────────────────────────────────────────────────────┘")

    # ── Step 6: Run chairman ─────────────────────────────────────────────────
    print("\n▸ Running chairman synthesis...")
    chairman_output = await call_claude(chairman_prompt, "Chairman")

    # ── Step 7: Generate reports ─────────────────────────────────────────────
    print("\n▸ Generating reports...")

    md_report = generate_markdown_report(
        question, advisor_responses, list(peer_reviews), chairman_output, timestamp
    )
    md_file = output_dir / "council-report.md"
    md_file.write_text(md_report)
    print(f"  Saved: council-report.md")

    html_report = generate_html_report(
        question, md_report, chairman_output, advisor_responses, timestamp
    )
    if html_report:
        html_file = output_dir / "council-report.html"
        html_file.write_text(html_report)
        print(f"  Saved: council-report.html")

    print(f"\n✓ Council complete → {output_dir}/")
    print(f"  Open council-report.html to read the verdict.\n")

    return output_dir


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Run the LLM Council")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--question", help="The framed question to council")
    group.add_argument("--question-file", help="Path to a .txt file containing the framed question")
    parser.add_argument("--seed", type=int, help="Random seed for anonymization (optional, for reproducibility)")
    parser.add_argument("--output-dir", help="Directory for output files (default: council-output-[timestamp])")
    args = parser.parse_args()

    if args.question_file:
        question = Path(args.question_file).read_text().strip()
    else:
        question = args.question

    output_dir = Path(args.output_dir) if args.output_dir else None

    asyncio.run(run_council(question, seed=args.seed, output_dir=output_dir))


if __name__ == "__main__":
    main()

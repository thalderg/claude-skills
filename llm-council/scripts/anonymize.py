#!/usr/bin/env python3
"""
llm-council anonymizer
Shuffles advisor names → letters for blind peer review, outputs anonymized block + reveal key.

Usage:
    python anonymize.py --responses responses.json
    python anonymize.py                              (reads JSON from stdin)
    python anonymize.py --responses responses.json --seed 42  (reproducible)

Input JSON format:
{
  "contrarian": "response text...",
  "first_principles": "response text...",
  "expansionist": "response text...",
  "outsider": "response text...",
  "executor": "response text..."
}

Output:
  - Prints anonymized block (A-E) ready to paste into reviewer prompts
  - Prints reveal key for chairman de-anonymization step
  - Saves both to council-anon-[timestamp].json in current directory
"""

import json
import random
import sys
import argparse
from datetime import datetime

ADVISORS = ["contrarian", "first_principles", "expansionist", "outsider", "executor"]
LETTERS = ["A", "B", "C", "D", "E"]

DISPLAY_NAMES = {
    "contrarian":       "The Contrarian",
    "first_principles": "The First Principles Thinker",
    "expansionist":     "The Expansionist",
    "outsider":         "The Outsider",
    "executor":         "The Executor",
}


def anonymize(responses: dict, seed: int | None = None) -> tuple[dict, dict]:
    """
    Shuffle advisors → letters using an isolated RNG (never touches global state).

    Returns:
        anonymized: {letter: response_text}
        reveal_key: {letter: advisor_key}
    """
    rng = random.Random(seed)   # isolated — does not affect global random state
    shuffled = ADVISORS[:]
    rng.shuffle(shuffled)

    anonymized = {letter: responses[advisor] for letter, advisor in zip(LETTERS, shuffled)}
    reveal_key = {letter: advisor          for letter, advisor in zip(LETTERS, shuffled)}
    return anonymized, reveal_key


def format_anonymized_block(anonymized: dict) -> str:
    """Format the anonymized responses for pasting into reviewer prompts."""
    lines = []
    for letter in LETTERS:  # always in A-E order
        lines.append(f"**Response {letter}:**")
        lines.append(anonymized[letter].strip())
        lines.append("")
    return "\n".join(lines)


def format_reveal_key(reveal_key: dict) -> str:
    """Format the reveal key for the chairman de-anonymization step."""
    lines = ["## Anonymization Reveal Key", ""]
    lines.append("Use this to de-anonymize responses in the chairman prompt:\n")
    for letter in LETTERS:  # always in A-E order
        advisor = reveal_key[letter]
        lines.append(f"  Response {letter}  →  {DISPLAY_NAMES[advisor]}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Anonymize LLM Council advisor responses for blind peer review"
    )
    parser.add_argument(
        "--responses",
        metavar="FILE",
        help="Path to advisor-responses.json (reads from stdin if omitted)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Integer seed for reproducible shuffling (optional)"
    )
    args = parser.parse_args()

    # Load responses
    if args.responses:
        with open(args.responses) as f:
            responses = json.load(f)
    else:
        print("Reading responses from stdin (JSON)...", file=sys.stderr)
        responses = json.load(sys.stdin)

    # Validate all 5 advisors present
    missing = [k for k in ADVISORS if k not in responses]
    if missing:
        print(f"ERROR: Missing advisor responses for: {missing}", file=sys.stderr)
        sys.exit(1)

    # args.seed is None when not provided — works correctly with seed=0
    anonymized, reveal_key = anonymize(responses, seed=args.seed)

    anon_block = format_anonymized_block(anonymized)
    key_block  = format_reveal_key(reveal_key)

    print("=" * 60)
    print("ANONYMIZED BLOCK (paste into all 5 reviewer prompts)")
    print("=" * 60)
    print(anon_block)
    print()
    print("=" * 60)
    print(key_block)
    print("=" * 60)

    # Save mapping to disk
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    outfile = f"council-anon-{timestamp}.json"
    with open(outfile, "w") as f:
        json.dump(
            {
                "timestamp":    timestamp,
                "seed":         args.seed,
                "anonymized":   anonymized,
                "reveal_key":   reveal_key,
                "display_names": {k: DISPLAY_NAMES[v] for k, v in reveal_key.items()},
            },
            f,
            indent=2,
        )

    print(f"\nSaved to: {outfile}")
    print("Pass this file (or the reveal_key field) to the chairman step.")


if __name__ == "__main__":
    main()

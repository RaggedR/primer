#!/usr/bin/env python3
"""Red Team the Guards — test all 63 AI guard prompts with a local LLM.

For each source, a small LLM reads the source description, writes a persuasive
argument, then faces the guard.  We count how many gates open.

Usage:
    python3 red_team.py [--model MODEL] [--workers N] [--source N] [--url URL]
"""

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

PRIMER_DIR = Path(__file__).resolve().parent
GUARDS_DIR = PRIMER_DIR / "guards"
SOURCES_FILE = PRIMER_DIR / "SOURCES.md"

GUARD_FILES = [
    "01-power.md", "02-resistance.md", "03-science.md", "04-war.md",
    "05-daily-life.md", "06-ideas.md", "07-view-from-here.md",
]

# ── Data types ──────────────────────────────────────────────────────────────

@dataclass
class Guard:
    source_num: int
    title: str
    character: str
    difficulty: str
    system_prompt: str

@dataclass
class Source:
    num: int
    title: str
    description: str   # full text from SOURCES.md
    difficulty: str

@dataclass
class Result:
    source_num: int
    title: str
    difficulty: str
    student_argument: str = ""
    guard_response: str = ""
    raw_json: dict = field(default_factory=dict)
    score: float = 0.0
    opened: bool = False
    reasoning: str = ""
    error: str = ""

# ── Parsing ─────────────────────────────────────────────────────────────────

def parse_guards() -> dict[int, Guard]:
    """Parse all guard files. Returns {source_num: Guard}."""
    guards = {}
    for fname in GUARD_FILES:
        path = GUARDS_DIR / fname
        text = path.read_text()

        # Split on ## Source N: headers
        chunks = re.split(r"(?=^## Source \d+:)", text, flags=re.MULTILINE)
        for chunk in chunks:
            m = re.match(r"^## Source (\d+):\s*(.+)", chunk)
            if not m:
                continue
            num = int(m.group(1))
            title = m.group(2).strip()

            # Extract character
            cm = re.search(r"\*\*Character\*\*:\s*(.+)", chunk)
            character = cm.group(1).strip() if cm else title

            # Extract difficulty
            dm = re.search(r"\*\*Difficulty\*\*:\s*(\w)", chunk)
            difficulty = dm.group(1).strip() if dm else "?"

            # Extract system prompt from triple-backtick block after ### System Prompt
            sp_match = re.search(
                r"### System Prompt\s*\n```\n(.*?)```",
                chunk, re.DOTALL
            )
            if not sp_match:
                print(f"  [warn] No system prompt found for source {num}", file=sys.stderr)
                continue
            system_prompt = sp_match.group(1).strip()

            guards[num] = Guard(
                source_num=num, title=title, character=character,
                difficulty=difficulty, system_prompt=system_prompt,
            )

    return guards


def parse_sources() -> dict[int, Source]:
    """Parse SOURCES.md. Returns {source_num: Source}."""
    text = SOURCES_FILE.read_text()
    sources = {}

    # Match entries: N. **Title** ... until next numbered entry or section break
    entries = re.split(r"(?=^\d+\.\s+\*\*)", text, flags=re.MULTILINE)
    for entry in entries:
        m = re.match(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)", entry, re.DOTALL)
        if not m:
            continue
        num = int(m.group(1))
        title = m.group(2).strip()
        rest = m.group(3).strip()

        # Extract difficulty from the rest
        dm = re.search(r"Difficulty:\s*(\w)", rest)
        difficulty = dm.group(1) if dm else "?"

        # Full description is everything (title + rest) up to section breaks
        description = f"{title} — {rest}".strip()
        # Trim trailing section markers
        description = re.split(r"\n---\n", description)[0].strip()

        sources[num] = Source(num=num, title=title, description=description,
                              difficulty=difficulty)

    return sources


# ── JSON response normalization ─────────────────────────────────────────────

def parse_llm_json(text: str) -> dict | None:
    """Extract first JSON object from LLM response. Tolerant of markdown fences."""
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)

    # Find first { ... } block (non-greedy, handles nested braces poorly but
    # LLM JSON is flat)
    match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def normalize_score(parsed: dict) -> tuple[float, bool, str]:
    """Normalize any of the 5 guard JSON formats to (score 0-100, opened, reasoning).

    Formats encountered:
      1. {"position_shift": 0-10}                                    (sources 1-20)
      2. {"persuasion_score": 0-100, "door_open": bool, ...}         (sources 21-28)
      3. {"persuasion_level": 0-10, "door_status": "locked|unlocked"}(sources 29-38)
      4. {"position_shift": 0.0-1.0, "reason": "..."}               (sources 39-47)
      5. {"position_shift": 0-10, "reasoning": "..."}                (sources 48-63)
    """
    reasoning = parsed.get("reasoning", parsed.get("reason", ""))
    if isinstance(reasoning, dict):
        reasoning = str(reasoning)

    # Format 2: persuasion_score (0-100) with door_open
    if "persuasion_score" in parsed:
        score = float(parsed["persuasion_score"])
        opened = bool(parsed.get("door_open", score >= 75))
        return score, opened, reasoning

    # Format 3: persuasion_level (0-10) with door_status
    if "persuasion_level" in parsed:
        level = float(parsed["persuasion_level"])
        score = level * 10
        opened = parsed.get("door_status", "locked") == "unlocked"
        if not opened:
            opened = level >= 8  # threshold stated in war guards
        return score, opened, reasoning

    # Formats 1, 4, 5: position_shift (various scales)
    if "position_shift" in parsed:
        val = parsed["position_shift"]
        # It might be a string description (war format reuses the key)
        if isinstance(val, str):
            return 0.0, False, val

        val = float(val)
        if val <= 1.0 and val != 0.0 and val != 1.0:
            # Float 0.0-1.0 scale (daily-life)
            score = val * 100
        elif val <= 10:
            # Integer 0-10 scale
            score = val * 10
        else:
            score = val  # already 0-100?

        opened = score >= 70
        return score, opened, reasoning

    # Fallback: try any numeric-looking key
    for key in parsed:
        try:
            val = float(parsed[key])
            if 0 <= val <= 100:
                return val if val > 10 else val * 10, val >= 7 if val <= 10 else val >= 70, reasoning
        except (ValueError, TypeError):
            continue

    return 0.0, False, reasoning


# ── Ollama API ──────────────────────────────────────────────────────────────

def call_ollama(url: str, model: str, messages: list[dict],
                temp: float = 0.7, max_tokens: int = 1024) -> str:
    """Send a chat completion to Ollama. Returns response text."""
    import requests

    resp = requests.post(
        f"{url}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "options": {"temperature": temp, "num_predict": max_tokens},
            "stream": False,
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def _msgs(user: str, system: str = "") -> list[dict]:
    """Build a simple system+user message list."""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    return msgs


# ── Core logic ──────────────────────────────────────────────────────────────

STUDENT_SYSTEM = (
    "You are a student who has read this primary source. Write a persuasive "
    "argument (3-5 sentences) to convince the historical character guarding "
    "the gate to let you through. You must demonstrate genuine engagement "
    "with the source material — quote it, reference specific details, engage "
    "with its internal logic. Generic rhetoric will fail."
)

# Nudge prompt for when the guard forgets to append JSON
SCORE_NUDGE = (
    "Now rate that student's argument. Respond with ONLY a JSON object, "
    "nothing else: {\"position_shift\": <0-10>} where 0 is unmoved and "
    "10 is fully persuaded."
)


def run_one(source: Source, guard: Guard, url: str, model: str) -> Result:
    """Run student + guard for one source. Returns Result."""
    result = Result(
        source_num=source.num, title=source.title,
        difficulty=guard.difficulty,
    )

    try:
        # Student turn: generate argument from source description
        student_arg = call_ollama(
            url, model,
            messages=_msgs(source.description, STUDENT_SYSTEM),
            temp=0.7,
        )
        result.student_argument = student_arg

        # Guard turn: evaluate the argument
        guard_msgs = _msgs(student_arg, guard.system_prompt)
        guard_response = call_ollama(
            url, model, messages=guard_msgs, temp=0.3,
        )
        result.guard_response = guard_response

        # Parse JSON from guard response
        parsed = parse_llm_json(guard_response)

        # Nudge: if no JSON in the response, ask for the score explicitly
        if not parsed:
            nudge_msgs = guard_msgs + [
                {"role": "assistant", "content": guard_response},
                {"role": "user", "content": SCORE_NUDGE},
            ]
            nudge_response = call_ollama(
                url, model, messages=nudge_msgs, temp=0.1, max_tokens=64,
            )
            result.guard_response += "\n\n[nudge] " + nudge_response
            parsed = parse_llm_json(nudge_response)

        if parsed:
            result.raw_json = parsed
            result.score, result.opened, result.reasoning = normalize_score(parsed)
        else:
            result.error = "no JSON in guard response"

    except Exception as e:
        result.error = str(e)

    return result


# ── Output ──────────────────────────────────────────────────────────────────

def print_results(results: list[Result]) -> None:
    """Print summary table to stdout."""
    results.sort(key=lambda r: r.source_num)

    print()
    print(f"{'Src':>3}  {'Guard':<40} {'Diff':>4}  {'Score':>5}  {'Opened':<6}")
    print(f"{'───':>3}  {'─' * 40} {'────':>4}  {'─────':>5}  {'──────':<6}")

    for r in results:
        label = f"{r.title[:40]}"
        status = "Yes" if r.opened else "No"
        if r.error:
            status = f"ERR: {r.error[:20]}"
        print(f"{r.source_num:>3}  {label:<40} {r.difficulty:>4}  {r.score:>5.0f}  {status:<6}")

    # Totals
    valid = [r for r in results if not r.error]
    opened = [r for r in valid if r.opened]
    total = len(valid)
    n_opened = len(opened)

    print(f"{'───':>3}  {'─' * 40} {'────':>4}  {'─────':>5}  {'──────':<6}")
    print(f"Total: {n_opened}/{total} gates opened ({n_opened/total*100:.0f}%)" if total else "No results")

    # By difficulty
    for d in ("A", "M", "C"):
        d_all = [r for r in valid if r.difficulty == d]
        d_open = [r for r in d_all if r.opened]
        if d_all:
            print(f"  {d}: {len(d_open)}/{len(d_all)} ({len(d_open)/len(d_all)*100:.0f}%)", end="")
    print()


def save_results(results: list[Result], path: Path) -> None:
    """Write full results to JSON."""
    data = []
    for r in sorted(results, key=lambda r: r.source_num):
        data.append({
            "source_num": r.source_num,
            "title": r.title,
            "difficulty": r.difficulty,
            "student_argument": r.student_argument,
            "guard_response": r.guard_response,
            "raw_json": r.raw_json,
            "score": r.score,
            "opened": r.opened,
            "reasoning": r.reasoning,
            "error": r.error,
        })
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nFull results saved to {path}")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Red team the Primer guard prompts")
    parser.add_argument("--model", default="llama3.2:3b", help="Ollama model (default: llama3.2:3b)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4)")
    parser.add_argument("--source", type=int, default=None, help="Run only source N (for debugging)")
    parser.add_argument("--url", default="http://localhost:11434", help="Ollama URL")
    args = parser.parse_args()

    # Parse everything
    print("Parsing guards...", end=" ", flush=True)
    guards = parse_guards()
    print(f"{len(guards)} guards")

    print("Parsing sources...", end=" ", flush=True)
    sources = parse_sources()
    print(f"{len(sources)} sources")

    # Determine which sources to run
    if args.source:
        if args.source not in guards:
            print(f"Error: no guard for source {args.source}", file=sys.stderr)
            sys.exit(1)
        if args.source not in sources:
            print(f"Error: no source description for {args.source}", file=sys.stderr)
            sys.exit(1)
        run_nums = [args.source]
    else:
        run_nums = sorted(set(guards.keys()) & set(sources.keys()))

    print(f"\nRunning {len(run_nums)} sources with {args.model} ({args.workers} workers)\n")
    t0 = time.time()

    # Execute
    results: list[Result] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_one, sources[n], guards[n], args.url, args.model): n
            for n in run_nums
        }
        for future in as_completed(futures):
            n = futures[future]
            try:
                r = future.result()
                results.append(r)
                status = f"score={r.score:.0f}" if not r.error else f"error={r.error[:30]}"
                opened = " OPENED" if r.opened else ""
                print(f"  [{r.source_num:>2}] {r.title[:35]:<35} {status}{opened}")
            except Exception as e:
                print(f"  [{n:>2}] FAILED: {e}", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"\nCompleted in {elapsed:.1f}s")

    # Output
    print_results(results)
    save_results(results, PRIMER_DIR / "results.json")


if __name__ == "__main__":
    main()

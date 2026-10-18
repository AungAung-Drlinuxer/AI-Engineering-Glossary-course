#!/usr/bin/env python3
"""`terms/` မှ self-quiz ဖန်တီးသည့် script (offline၊ deterministic)။

    python3 quiz.py                              # term ၁၀ ခု၊ မေးခွန်းတိုင်း interactive
    python3 quiz.py --area 06 --count 15
    python3 quiz.py --seed 42 --answers          # အဖြေစာရင်း ပြရန် (interactive မဟုတ်)
    python3 quiz.py --self-test                  # စစ်ဆေးချက် (offline၊ ချက်ချင်း)

မေးခွန်း ပုံစံ — term တစ်ခု ပေးပြီး၊ source ၏ အင်္ဂလိပ် အဓိပ္ပာယ် ၄ ခုအနက် မှန်သည့် တစ်ခုကို ရွေးသည်။
ရွေးချယ်စရာ ၃ ခုသည် တူညီသော နယ်ပယ်မှ အခြား term များ၏ အဓိပ္ပာယ် ဖြစ်သည်။
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import terms_corpus as tc

REPO = Path(__file__).resolve().parent


def load() -> list[dict]:
    """`terms/NN_<slug>.md` မှ term အားလုံးကို နယ်ပယ် အချက်အလက်နှင့်အတူ ဖတ်သည်။"""
    entries: list[dict] = []
    for path in tc.area_paths():
        num = path.name[:2]
        name = tc.area_name(num)
        for entry in tc.parse_area(path):
            if not entry.get("english", "").strip():
                continue
            entries.append(dict(term=entry["term"], area=num, category=name,
                                means=entry["english"].strip(),
                                related=entry.get("related", "")))
    return entries


def build(seed: int, area: str | None, count: int) -> list[dict]:
    entries = load()
    pool = [e for e in entries if area is None or e["area"] == area]
    if len(pool) < 4:
        raise SystemExit(f"area {area} has too few terms for a quiz")
    rng = random.Random(seed)
    picked = rng.sample(pool, min(count, len(pool)))
    questions = []
    for entry in picked:
        distractors = [e for e in pool if e["term"] != entry["term"]]
        options = rng.sample(distractors, 3) + [entry]
        rng.shuffle(options)
        questions.append(dict(
            term=entry["term"],
            category=entry["category"],
            options=[o["means"] for o in options],
            answer=[o["term"] for o in options].index(entry["term"]),
            related=entry.get("related", ""),
        ))
    return questions


def ask(questions: list[dict], answers_only: bool) -> int:
    score = 0
    for i, q in enumerate(questions, 1):
        if not answers_only:
            print(f"\nQ{i}. {q['term']}  ({q['category']})")
            for n, opt in enumerate(q["options"], 1):
                print(f"   {n}) {opt[:180]}{'...' if len(opt) > 180 else ''}")
        if answers_only:
            print(f"Q{i}. {q['term']} -> {q['answer'] + 1}) {q['options'][q['answer']][:110]}...")
            continue
        try:
            reply = input("   answer (1-4, Enter to skip, q to quit): ").strip().lower()
        except EOFError:
            break
        if reply == "q":
            break
        if not reply:
            print(f"   skipped — correct: {q['answer'] + 1}")
            continue
        if reply.isdigit() and int(reply) == q["answer"] + 1:
            print("   correct")
            score += 1
        else:
            print(f"   wrong — correct: {q['answer'] + 1}) {q['options'][q['answer']][:140]}")
            print(f"   related: {q['related']}")
    return score


def self_test() -> int:
    """offline၊ deterministic စစ်ဆေးချက် — interactive input မလိုပါ။"""
    for seed in (0, 7, 42):
        questions = build(seed, None, 10)
        assert len(questions) == 10
        assert len({q["term"] for q in questions}) == 10
        for q in questions:
            assert len(q["options"]) == 4
            assert 0 <= q["answer"] < 4
            assert len(set(q["options"])) == 4
        assert [q["term"] for q in questions] == [q["term"] for q in build(seed, None, 10)]
    area_questions = build(1, "06", 15)
    assert all(q["category"] == "Agents & tools" for q in area_questions)
    print("self-test: 3 seeds x 10 questions + one area run — all assertions passed")
    print("[PASS] quiz.py works offline and deterministically.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Self-quiz over the terms files.")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--area", default=None, help="area number, e.g. 06")
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--answers", action="store_true", help="print the answer key instead of asking")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    questions = build(args.seed, args.area, args.count)
    score = ask(questions, args.answers)
    if not args.answers:
        print(f"\nscore: {score}/{len(questions)}")
        if score * 2 < len(questions):
            print("အကြံပြုချက် — မှားသည့် term များကို ပြန်ဖတ်ပြီး နောက်တစ်ကြိမ် ပြန်လုပ်ပါ။")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

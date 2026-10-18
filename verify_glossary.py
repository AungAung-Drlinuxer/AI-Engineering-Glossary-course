#!/usr/bin/env python3
"""Glossary ဖိုင်များကို စစ်ဆေးသည့် script။

    python3 verify_glossary.py                 # နယ်ပယ် အားလုံး
    python3 verify_glossary.py --area 01        # နယ်ပယ် တစ်ခုသာ
    python3 verify_glossary.py --verbose

စစ်ဆေးချက် — term အရေအတွက်နှင့် အစဉ်၊ source ၏ အင်္ဂလိပ် စာသား တူညီမှု၊ မြန်မာ field ပြည့်စုံမှု၊
register သန့်ရှင်းမှု (ပြောစကား ပါတ်တစ်လ်လ်၊ အခြားဘာသာ အက္ခရာ၊ emoji)။
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent
AREAS = REPO / "glossary" / "by_area"
TERMS = REPO / "terms"
BANNED = ["ပါတယ်", "ပါဘူး", "ရမယ်", "ဖြစ်တယ်", "တဲ့", "နဲ့", "ဖို့", "ရဲ့", "နော်", "ပေါ့", "လို့", "ဆိုတာ", "ဒီ"]
REQUIRED = ["**မြန်မာ:**", "**ဆိုလိုသည့် အဓိပ္ပာယ်:**", "**အရေးပါသည့် အကြောင်းရင်း:**",
            "**ဆက်စပ် term များ:**", "**English (source):**"]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def foreign(text: str) -> list[str]:
    bad = set()
    for ch in text:
        code = ord(ch)
        if 0x3000 <= code <= 0x9FFF or 0xAC00 <= code <= 0xD7AF or 0x0900 <= code <= 0x097F:
            bad.add(ch)
        if 0x1F300 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF:
            bad.add(ch)
    return sorted(bad)


def check_area(num: str, verbose: bool) -> tuple[int, int, list[str]]:
    slices = sorted(AREAS.glob(f"{num}_*.json"))
    if not slices:
        return 0, 0, [f"{num}: no data slice found"]
    data = json.loads(slices[0].read_text(encoding="utf-8"))
    slug = slices[0].stem.split("_", 1)[1]
    path = TERMS / f"{num}_{slug}.md"
    problems: list[str] = []
    if not path.exists():
        return 0, 0, [f"{path.name}: file is missing"]
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    found = [b.split("\n", 1)[0].strip() for b in blocks]
    expected = [e["term"] for e in data]
    if found != expected:
        missing = [t for t in expected if t not in found]
        extra = [t for t in found if t not in expected]
        if missing:
            problems.append(f"{len(missing)} term missing, first: {missing[:3]}")
        if extra:
            problems.append(f"{len(extra)} unexpected term, first: {extra[:3]}")
        if not missing and not extra:
            problems.append("term order differs from the source slice")
    by_term = {b.split("\n", 1)[0].strip(): b for b in blocks}
    for entry in data:
        block = by_term.get(entry["term"])
        if block is None:
            continue
        for label in REQUIRED:
            if label not in block:
                problems.append(f"{entry['term']}: {label} is missing")
        flat = norm(block)
        if norm(entry["means"]) not in flat:
            problems.append(f"{entry['term']}: the source English definition is not present verbatim")
        if entry["why"] and norm(entry["why"]) not in flat:
            problems.append(f"{entry['term']}: the source English 'why it matters' is missing")
        if entry["related"] and norm(entry["related"]) not in flat:
            problems.append(f"{entry['term']}: related terms are missing")
    for marker in BANNED:
        if marker in text:
            lines = [i + 1 for i, l in enumerate(text.splitlines()) if marker in l]
            problems.append(f"colloquial marker {marker} on line(s) {lines[:4]}")
    bad = foreign(text)
    if bad:
        problems.append(f"foreign glyphs: {bad}")
    if verbose:
        print(f"  {path.name}: {len(found)}/{len(expected)} terms, {len(text.splitlines())} lines")
    return len(found), len(expected), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify the bilingual glossary files.")
    ap.add_argument("--area", default=None, help="area number, e.g. 01")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    numbers = sorted(p.name.split("_")[0] for p in AREAS.glob("*.json"))
    if args.area:
        numbers = [n for n in numbers if n == args.area]
        if not numbers:
            print(f"unknown area {args.area}")
            return 1

    total_found = total_expected = 0
    problems: list[str] = []
    print("=" * 74)
    for num in numbers:
        found, expected, probs = check_area(num, args.verbose)
        total_found += found
        total_expected += expected
        status = "PASS" if not probs else "FAIL"
        print(f"{num}  terms {found:>3}/{expected:<3} {status}")
        problems.extend(f"{num}: {p}" for p in probs)
    print("=" * 74)
    print(f"TOTAL: {total_found}/{total_expected} terms across {len(numbers)} area file(s)")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems[:40]:
            print("  -", p)
        return 1
    print("[PASS] Every term is present, ordered, bilingual and free of colloquial markers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

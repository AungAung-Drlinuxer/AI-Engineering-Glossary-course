#!/usr/bin/env python3
"""`terms/` ဖိုင်များကို စစ်ဆေးသည့် script — data အရင်းအမြစ်မှာ `terms/` ကိုယ်တိုင် ဖြစ်သည်။

    python3 verify_glossary.py                 # နယ်ပယ် အားလုံး
    python3 verify_glossary.py --area 01        # နယ်ပယ် တစ်ခုသာ
    python3 verify_glossary.py --verbose

စစ်ဆေးချက် —
1. term heading အရေအတွက်သည် `terms/00_index.md` ၏ အကျဉ်းချုပ် ဇယားနှင့် တူညီမှု
2. index ရှိ term တိုင်း ဖိုင်ထဲ ပါဝင်မှု၊ အပို term မရှိမှု၊ ထပ်နေသည့် heading မရှိမှု
3. label ငါးခု (မြန်မာ၊ ဆိုလိုသည့် အဓိပ္ပာယ်၊ အရေးပါသည့် အကြောင်းရင်း၊ ဆက်စပ် term များ၊
   English (source)) ပြည့်စုံ၍ တန်ဖိုး မလွတ်မှု
4. index လင့် တိုင်း၏ anchor သည် ဖိုင်ထဲ ရှိသည့် heading နှင့် ကိုက်ညီမှု (လင့် အားလုံး အလုပ်လုပ်မှု)
5. register သန့်ရှင်းမှု (စကားပြော particle၊ အခြားဘာသာ အက္ခရာ၊ emoji)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import terms_corpus as tc

REPO = Path(__file__).resolve().parent
BANNED = ["ပါတယ်", "ပါဘူး", "ရမယ်", "ဖြစ်တယ်", "တဲ့", "နဲ့", "ဖို့", "ရဲ့", "နော်", "ပေါ့", "လို့", "ဆိုတာ", "ဒီ"]
FIELDS = (("burmese", "မြန်မာ"), ("means", "ဆိုလိုသည့် အဓိပ္ပာယ်"),
          ("why", "အရေးပါသည့် အကြောင်းရင်း"), ("related", "ဆက်စပ် term များ"),
          ("english", "English (source)"))


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
    path = tc.area_path(num)
    if path is None:
        return 0, 0, [f"{num}: no terms file found"]
    expected_count = tc.area_counts().get(num)
    text = path.read_text(encoding="utf-8")
    entries = tc.parse_area(path)
    found = [e["term"] for e in entries]
    blocks = tc.raw_blocks(path)
    rows = tc.index_rows(num)
    problems: list[str] = []

    dupes = sorted({t for t in found if found.count(t) > 1})
    if dupes:
        problems.append(f"duplicate heading(s): {dupes[:3]}")

    indexed = [r["term"] for r in rows]
    if not rows:
        problems.append("the index has no rows for this area")
    missing = [t for t in indexed if t not in found]
    extra = [t for t in found if t not in indexed]
    if missing:
        problems.append(f"{len(missing)} indexed term(s) absent from the file, first: {missing[:3]}")
    if extra:
        problems.append(f"{len(extra)} term(s) absent from the index, first: {extra[:3]}")
    if expected_count is not None and len(found) != expected_count:
        problems.append(f"heading count {len(found)} != index summary {expected_count}")

    for entry in entries:
        block = blocks.get(entry["term"], "")
        for label in tc.REQUIRED_LABELS:
            if label not in block:
                problems.append(f"{entry['term']}: {label} is missing")
        for field, label in FIELDS:
            if not str(entry.get(field, "")).strip():
                problems.append(f"{entry['term']}: {label} is empty")

    slugs = {tc.slugify(t) for t in found}
    for row in rows:
        want = tc.slugify(row["term"])
        if row["anchor"] != want:
            problems.append(f"index anchor {row['anchor']!r} does not match the heading slug {want!r}")
        elif row["anchor"] not in slugs:
            problems.append(f"index anchor {row['anchor']!r} has no matching heading in {path.name}")

    for marker in BANNED:
        if marker in text:
            lines = [i + 1 for i, l in enumerate(text.splitlines()) if marker in l]
            problems.append(f"colloquial marker {marker} on line(s) {lines[:4]}")
    bad = foreign(text)
    if bad:
        problems.append(f"foreign glyphs: {bad}")

    if verbose:
        print(f"  {path.name}: {len(found)}/{expected_count} terms, {len(text.splitlines())} lines")
    return len(found), expected_count if expected_count is not None else len(found), problems


def check_corpus() -> list[str]:
    """Index နှင့် ဖိုင်များ စုစုပေါင်း ကိုက်ညီမှု။"""
    problems: list[str] = []
    headings = sum(len(tc.parse_area(p)) for p in tc.area_paths())
    rows = tc.parse_index()
    counts = tc.area_counts()
    if len(rows) != headings:
        problems.append(f"index rows {len(rows)} != total headings {headings}")
    if len(rows) != len({r["term"] for r in rows}):
        problems.append("the index lists a term twice")
    if len(counts) != len(tc.area_paths()):
        problems.append(f"index summary covers {len(counts)} areas, files {len(tc.area_paths())}")
    if sum(counts.values()) != headings:
        problems.append(f"index summary total {sum(counts.values())} != total headings {headings}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify the bilingual terms files.")
    ap.add_argument("--area", default=None, help="area number, e.g. 01")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    numbers = [p.name[:2] for p in tc.area_paths()]
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
    if not args.area:
        problems.extend(f"index: {p}" for p in check_corpus())
    print("=" * 74)
    print(f"TOTAL: {total_found}/{total_expected} terms across {len(numbers)} area file(s)")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems[:40]:
            print("  -", p)
        return 1
    print("[PASS] Every term is present, indexed, bilingual, complete and free of colloquial markers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

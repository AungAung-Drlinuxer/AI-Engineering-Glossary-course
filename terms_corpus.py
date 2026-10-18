#!/usr/bin/env python3
"""`terms/` ကို ဖတ်သည့် shared parser — tool အားလုံး (verify_glossary၊ verify_guide၊ quiz) ဤဖိုင်ကို အသုံးပြုသည်။

`terms/NN_<slug>.md` သည် term တိုင်းကို `### <Term>` heading နှင့် label များ
(`**မြန်မာ:**`၊ `- **ဆိုလိုသည့် အဓိပ္ပာယ်:**`၊ `- **English (source):**` …) ဖြင့် ရေးထားသည်။
`terms/00_index.md` သည် term တိုင်း၏ မြန်မာ အမည်၊ နယ်ပယ်နှင့် ဆက်စပ် term များကို စာရင်း လုပ်ထားသည်။
ဤ parser သည် ထို ဖိုင်များကို data အရင်းအမြစ်အဖြစ် တိုက်ရိုက် ဖတ်သည် (အပိုဆောင်း data ဖိုင် မလိုပါ)။
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent
TERMS = REPO / "terms"
INDEX = TERMS / "00_index.md"

LABELS = {
    "မြန်မာ": "burmese",
    "ဆိုလိုသည့် အဓိပ္ပာယ်": "means",
    "အရေးပါသည့် အကြောင်းရင်း": "why",
    "မကြာခဏ ရောထွေးမှု": "confusion",
    "လက်တွေ့": "practice",
    "Infrastructure အကျိုးသက်ရောက်မှု": "infrastructure",
    "ဆက်စပ် term များ": "related",
    "English (source)": "english",
    "Learn it": "learn",
}
REQUIRED_LABELS = ["**မြန်မာ:**", "**ဆိုလိုသည့် အဓိပ္ပာယ်:**", "**အရေးပါသည့် အကြောင်းရင်း:**",
                   "**ဆက်စပ် term များ:**", "**English (source):**"]
LABEL_RE = re.compile(r"^(?:-\s*)?\*\*(?P<label>[^*]+?)\s*:\*\*\s*(?P<value>.*)$")


def area_paths() -> list[Path]:
    """term ဖိုင်များ (00_index.md မပါ)။"""
    return sorted(p for p in TERMS.glob("*.md") if not p.name.startswith("00_"))


def area_path(number: str) -> Path | None:
    for path in area_paths():
        if path.name.startswith(f"{number}_"):
            return path
    return None


def area_name(number: str) -> str:
    """index မှ နယ်ပယ်၏ အင်္ဂလိပ် အမည် (ရှာမတွေ့ပါက slug မှ ပြန်ထုတ်သည်)။"""
    titles = area_titles()
    if number in titles:
        return titles[number]
    path = area_path(number)
    if path is None:
        return ""
    return path.stem.split("_", 1)[1].replace("_", " ").capitalize()


def parse_area(path: Path) -> list[dict]:
    """ဖိုင် တစ်ခုကို `### ` ဖြင့် ခွဲ၍ term တိုင်း၏ label များကို dict အဖြစ် ပြန်ပေးသည်။"""
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    for chunk in re.split(r"^### ", text, flags=re.M)[1:]:
        lines = chunk.splitlines()
        if not lines:
            continue
        entry: dict = {"term": lines[0].strip()}
        field: str | None = None
        for line in lines[1:]:
            if line.startswith("#"):
                break
            match = LABEL_RE.match(line.strip())
            if match:
                field = LABELS.get(match.group("label").strip())
                if field:
                    entry[field] = match.group("value").strip()
                else:
                    field = None
                continue
            if field and line.strip():
                entry[field] = (entry.get(field, "") + " " + line.strip()).strip()
        entry.setdefault("means", "")
        entry.setdefault("english", "")
        entry.setdefault("burmese", "")
        entry.setdefault("related", "")
        entries.append(entry)
    return entries


def terms_of(number: str) -> list[str]:
    """နယ်ပယ် တစ်ခု၏ term အမည်များ (ဖိုင်ထဲ ပါသည့် အစဉ်အတိုင်း)။"""
    path = area_path(number)
    return [] if path is None else [e["term"] for e in parse_area(path)]


def parse_index() -> list[dict]:
    """`terms/00_index.md` ၏ ဇယား အတန်းများ — term၊ မြန်မာ အမည်၊ နယ်ပယ်၊ ဖိုင်၊ ဆက်စပ် term များ။"""
    rows: list[dict] = []
    link = re.compile(r"^\|\s*\[(?P<term>[^\]]+)\]\((?P<target>[^)]+)\)\s*\|(?P<rest>.*)$")
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        match = link.match(line.strip())
        if not match:
            continue
        cells = [c.strip() for c in match.group("rest").split("|")]
        target = match.group("target")
        rows.append(dict(
            term=match.group("term"),
            burmese=cells[0] if cells else "",
            area_name=cells[1] if len(cells) > 1 else "",
            file=cells[2].strip("`") if len(cells) > 2 else "",
            related=cells[3] if len(cells) > 3 else "",
            target=target,
            anchor=target.split("#", 1)[1] if "#" in target else "",
        ))
    return rows


def area_titles() -> dict[str, str]:
    """နယ်ပယ် နံပါတ် → အင်္ဂလိပ် အမည် (index မှ)။"""
    titles: dict[str, str] = {}
    for row in parse_index():
        name = Path(row["file"]).name
        if name[:2].isdigit():
            titles.setdefault(name[:2], row["area_name"])
    return titles


def raw_blocks(path: Path) -> dict[str, str]:
    """term → မူရင်း block စာသား (label စစ်ဆေးရန်)။"""
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for chunk in re.split(r"^### ", text, flags=re.M)[1:]:
        head = chunk.split("\n", 1)
        out[head[0].strip()] = chunk
    return out


def slugify(term: str) -> str:
    """Index လင့်၏ anchor ပုံစံ (`Adam (Optimizer)` → `adam-optimizer`)။"""
    text = term.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def index_rows(number: str | None = None) -> list[dict]:
    """Index အတန်းများ (နယ်ပယ် နံပါတ် ပေးပါက ထို နယ်ပယ်သာ)။"""
    rows = parse_index()
    if number is None:
        return rows
    return [r for r in rows if Path(r["file"]).name.startswith(f"{number}_")]


def area_counts() -> dict[str, int]:
    """Index ၏ `## Learning area အလိုက်` ဇယားမှ နယ်ပယ် တိုင်း၏ term အရေအတွက်။"""
    counts: dict[str, int] = {}
    row = re.compile(r"^\|\s*(\d{2})\s*\|[^|]*\|\s*(\d+)\s*\|")
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        match = row.match(line.strip())
        if match:
            counts[match.group(1)] = int(match.group(2))
    return counts


def parse_all() -> dict[str, list[dict]]:
    """နယ်ပယ် နံပါတ် → entries။"""
    return {p.name[:2]: parse_area(p) for p in area_paths()}


if __name__ == "__main__":
    total = 0
    for path in area_paths():
        entries = parse_area(path)
        total += len(entries)
        print(f"{path.name:34s} {len(entries):>3} terms")
    print(f"{'TOTAL':34s} {total:>3} terms | index rows {len(parse_index())}")
    print("areas:", area_titles())

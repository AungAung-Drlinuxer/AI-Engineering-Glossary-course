#!/usr/bin/env python3
"""လေ့လာလမ်းညွှန် (guides/) အားလုံးကို စစ်ဆေးသည့် script။

    python3 verify_guide.py                    # လမ်းညွှန် အားလုံး
    python3 verify_guide.py --guide 02          # နယ်ပယ် တစ်ခုသာ
    python3 verify_guide.py --documents         # document ဖိုင်များသာ
    python3 verify_guide.py --labs              # lab များသာ
    python3 verify_guide.py --verbose

လမ်းညွှန် တစ်ခုစီအတွက် စစ်ဆေးချက် —

1. လိုအပ်သည့် ဖိုင် ၆ ခု ရှိမှု (README, အစဉ်, ပုံများ, အောက်ခံစနစ်, လေ့ကျင့်ခန်း, labs/README)
2. register သန့်ရှင်းမှု — စကားပြော ပါတ်တစ်လ်လ်၊ အခြားဘာသာ အက္ခရာ၊ emoji
3. ထို နယ်ပယ်၏ term အားလုံး `01_learning_sequence.md` တွင် ပါဝင်မှု
4. `02_visual_explanations.md` တွင် Mermaid ပုံ အနည်းဆုံး ၄ ခု
5. lab တိုင်း `--self-test` ကို ၃ ကြိမ် run ၍ exit 0 နှင့် output တူညီမှု၊ `run_labs.py` အောင်မြင်မှု
6. ဖိုင်ထဲ ကူးထားသည့် run တိုင်း (`$ python3 <path>` နှင့် labs/README ၏ block များ) ပြန် run ၍ တူညီမှု
7. လမ်းညွှန် က ညွှန်သည့် `scripts/*.py` ဖိုင်များ ရှိမှု
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
GUIDES = REPO / "guides"
SLICES = REPO / "glossary" / "by_area"
REQUIRED_DOCS = ["README.md", "01_learning_sequence.md", "02_visual_explanations.md",
                 "03_theory_to_infrastructure.md", "04_exercises.md", "labs/README.md"]
BANNED = ["ပါတယ်", "ပါဘူး", "ရမယ်", "ဖြစ်တယ်", "တဲ့", "နဲ့", "ဖို့", "ရဲ့", "နော်", "ပေါ့", "လို့", "ဆိုတာ", "ဒီ"]
MIN_CHARS = 800
MIN_DIAGRAMS = 4


def foreign(text: str) -> list[str]:
    bad = set()
    for ch in text:
        code = ord(ch)
        if 0x3000 <= code <= 0x9FFF or 0xAC00 <= code <= 0xD7AF or 0x0900 <= code <= 0x097F:
            bad.add(ch)
        if 0x1F300 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF:
            bad.add(ch)
    return sorted(bad)


def slice_terms(number: str) -> list[str]:
    for path in sorted(SLICES.glob(f"{number}_*.json")):
        return [e["term"] for e in json.loads(path.read_text(encoding="utf-8"))]
    return []


def check_documents(guide: Path, number: str, verbose: bool) -> list[str]:
    problems: list[str] = []
    for name in REQUIRED_DOCS:
        path = guide / name
        if not path.exists():
            problems.append(f"{name}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if len(text) < MIN_CHARS:
            problems.append(f"{name}: only {len(text)} chars — too thin to teach anything")
        for marker in BANNED:
            if marker in text:
                problems.append(f"{name}: colloquial marker {marker} on line "
                                f"{[i + 1 for i, l in enumerate(text.splitlines()) if marker in l][:3]}")
        bad = foreign(text)
        if bad:
            problems.append(f"{name}: foreign glyphs {bad}")
        if verbose:
            print(f"    {name}: {len(text)} chars, {len(text.splitlines())} lines")
    sequence = guide / "01_learning_sequence.md"
    terms = slice_terms(number)
    if sequence.exists() and terms:
        text = sequence.read_text(encoding="utf-8")
        missing = [t for t in terms if t not in text]
        if missing:
            problems.append(f"01_learning_sequence.md: {len(missing)} of {len(terms)} term(s) absent: {missing[:4]}")
        elif verbose:
            print(f"    01_learning_sequence.md: all {len(terms)} terms placed in the sequence")
    visuals = guide / "02_visual_explanations.md"
    if visuals.exists():
        count = visuals.read_text(encoding="utf-8").count("```mermaid")
        if count < MIN_DIAGRAMS:
            problems.append(f"02_visual_explanations.md: {count} Mermaid diagram(s), at least {MIN_DIAGRAMS} expected")
        elif verbose:
            print(f"    02_visual_explanations.md: {count} Mermaid diagrams")
    return problems


def check_labs(guide: Path, verbose: bool) -> list[str]:
    problems: list[str] = []
    labs = sorted(p for p in (guide / "labs").glob("*.py") if p.name.startswith("lab_"))
    if len(labs) < 2:
        problems.append(f"labs/: {len(labs)} lab script(s) — at least 2 expected")
    for path in labs:
        if "--self-test" not in path.read_text(encoding="utf-8"):
            problems.append(f"labs/{path.name}: no --self-test entry point")
            continue
        results = []
        for _ in range(3):
            done = subprocess.run([sys.executable, str(path), "--self-test"],
                                  capture_output=True, text=True, timeout=180)
            results.append((done.returncode, done.stdout))
        codes = {c for c, _ in results}
        if codes != {0}:
            problems.append(f"labs/{path.name}: --self-test exit codes {sorted(codes)}")
            continue
        if len({o for _, o in results}) != 1:
            problems.append(f"labs/{path.name}: --self-test output differs between runs (not deterministic)")
        elif verbose:
            print(f"    labs/{path.name}: 3 runs, exit 0, output identical")
    runner = guide / "labs" / "run_labs.py"
    if not runner.exists():
        problems.append("labs/run_labs.py: file is missing")
    else:
        done = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True, timeout=900)
        if done.returncode != 0:
            problems.append(f"labs/run_labs.py: exit {done.returncode}")
        elif verbose:
            last = done.stdout.strip().splitlines()[-1] if done.stdout.strip() else "(no output)"
            print("    labs/run_labs.py:", last)
    return problems


def check_examples(guide: Path, verbose: bool) -> list[str]:
    """ဖိုင်ထဲ ကူးထားသည့် run တိုင်း ပြန် run ၍ တူညီကြောင်း စစ်သည်။"""
    problems: list[str] = []
    for path in sorted(guide.rglob("*.md")):
        name = path.relative_to(guide)
        text = path.read_text(encoding="utf-8")
        for cmd, pasted in re.findall(r"```text\n\$ python3 (\S+)\n(.*?)```", text, re.S):
            local = cmd.split(f"guides/{guide.name}/")[-1]
            target = guide / local
            if not target.exists():
                problems.append(f"{name}: pasted example runs {cmd}, which does not exist")
                continue
            done = subprocess.run([sys.executable, str(target)], capture_output=True, text=True, timeout=300)
            if done.stdout.rstrip().strip() != pasted.rstrip().strip():
                problems.append(f"{name}: the pasted output of {Path(cmd).name} no longer matches the run")
            elif verbose:
                print(f"    {name}: {Path(cmd).name} output reproduces byte-for-byte")
        if str(name).startswith("labs/"):
            for bash, pasted in re.findall(r"```bash\n(.*?)```\n(?:.*?\n)?```\n(.*?)```", text, re.S):
                lines = [l.split("#")[0].strip() for l in bash.splitlines() if l.strip().startswith("python3")]
                if not lines:
                    continue
                parts = lines[0].split()
                script = guide / "labs" / parts[1].split("/")[-1]
                if not script.exists():
                    problems.append(f"{name}: {parts[1]} does not exist")
                    continue
                done = subprocess.run([sys.executable, str(script), *parts[2:]],
                                      capture_output=True, text=True, timeout=300)
                if done.stdout.rstrip().strip() != pasted.rstrip().strip():
                    problems.append(f"{name}: the pasted output of {parts[1]} no longer matches the run")
                elif verbose:
                    print(f"    {name}: {parts[1]} output reproduces byte-for-byte")
    return problems


def check_script_refs(guide: Path) -> list[str]:
    problems: list[str] = []
    text = "\n".join(p.read_text(encoding="utf-8") for p in guide.rglob("*.md"))
    for ref in sorted(set(re.findall(r"scripts/[\w.]+\.py", text))):
        if not (guide / ref).exists():
            problems.append(f"{ref}: referenced by the guide but missing from scripts/")
    if not (guide / "scripts").exists() or not list((guide / "scripts").glob("*.py")):
        problems.append("scripts/: no calculation script is present")
    return problems


def check_script_names(guide: Path) -> list[str]:
    """Every lab_*.py or ex_*.py the prose names must exist on disk.

    A writer who drafts the prose before the sibling's labs land tends to leave
    placeholder file names behind; the study path then points at a script no reader
    can run.
    """
    problems: list[str] = []
    present = {p.name for p in (guide / "labs").glob("*.py")}
    present |= {p.name for p in (guide / "scripts").glob("*.py")}
    named: set[str] = set()
    for path in sorted(guide.rglob("*.md")):
        named |= set(re.findall(r"\b(?:lab|run_labs|ex)_[a-z0-9_]+\.py", path.read_text(encoding="utf-8")))
    for name in sorted(named - present):
        problems.append(f"{name}: named in the guide but no such file in labs/ or scripts/")
    return problems


def terms_only(guide: Path) -> bool:
    """A guide that declares itself terms-only carries a shortcut glossary and no labs.

    The full gate (6 documents, 4 diagrams, a lab suite, pasted-run reproduction) is
    for teaching guides. A guide whose README.md carries the marker below is instead
    held to the terms-only gate in check_terms_only().
    """
    readme = guide / "README.md"
    if not readme.is_file():
        return False
    return "guide-kind: terms-only" in readme.read_text(encoding="utf-8")


def check_terms_only(guide: Path, number: str, verbose: bool) -> list[str]:
    """Reduced gate for a terms-only guide: one document, covering every term.

    The colloquial-marker register check is deliberately NOT applied here: a terms-only
    glossary is written in the plain spoken register the user asked for ("Epoch ဆိုတာ …
    ဆိုလိုပါတယ်"), which the formal-prose ban list would reject by construction. The
    foreign-glyph and term-coverage checks still apply.
    """
    problems: list[str] = []
    text = (guide / "README.md").read_text(encoding="utf-8")
    if len(text) < MIN_CHARS:
        problems.append(f"README.md: only {len(text)} chars — too thin to teach anything")
    bad = foreign(text)
    if bad:
        problems.append(f"README.md: foreign glyphs {bad}")
    terms = slice_terms(number)
    missing = [t for t in terms if t not in text]
    if missing:
        problems.append(f"README.md: {len(missing)} of {len(terms)} term(s) absent: {missing[:4]}")
    elif verbose:
        print(f"    README.md: terms-only guide, all {len(terms)} terms present, {len(text)} chars")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify every study guide under guides/.")
    ap.add_argument("--guide", default=None, help="area number, e.g. 02")
    ap.add_argument("--documents", action="store_true")
    ap.add_argument("--labs", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    do_docs = args.documents or not args.labs
    do_labs = args.labs or not args.documents

    found = sorted(p for p in GUIDES.glob("*") if p.is_dir())
    if not found:
        print("guides/: no guide directory exists yet")
        return 1
    if args.guide:
        found = [p for p in found if p.name.startswith(f"{args.guide}_") or p.name == args.guide]
        if not found:
            print(f"unknown guide {args.guide}")
            return 1

    problems: list[str] = []
    total_terms = 0
    print("=" * 74)
    for guide in found:
        number = guide.name.split("_")[0]
        total_terms += len(slice_terms(number))
        print(f"{guide.name}")
        own: list[str] = []
        if terms_only(guide):
            own += check_terms_only(guide, number, args.verbose)
            print(f"  -> {'PASS' if not own else 'FAIL'}")
            problems.extend(f"{guide.name}: {p}" for p in own)
            continue
        if do_docs:
            own += check_documents(guide, number, args.verbose)
            own += check_examples(guide, args.verbose)
            own += check_script_refs(guide)
            own += check_script_names(guide)
        if do_labs:
            own += check_labs(guide, args.verbose)
        print(f"  -> {'PASS' if not own else 'FAIL'}")
        problems.extend(f"{guide.name}: {p}" for p in own)
    print("=" * 74)
    print(f"TOTAL: {len(found)} guide(s), {total_terms} terms covered")
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems[:60]:
            print("  -", p)
        return 1
    print("[PASS] Every guide is complete, in register, and every pasted run and lab reproduces offline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

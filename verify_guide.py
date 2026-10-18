#!/usr/bin/env python3
"""Model guide ကို စစ်ဆေးသည့် script (area 02 — Models & inference)။

    python3 verify_guide.py                 # ဖိုင် + lab အားလုံး
    python3 verify_guide.py --documents      # document ဖိုင်များသာ
    python3 verify_guide.py --labs           # lab များသာ
    python3 verify_guide.py --verbose

စစ်ဆေးချက် — လိုအပ်သည့် ဖိုင်များ ရှိမှု၊ register သန့်ရှင်းမှု၊ term ၂၉ ခုလုံး learning sequence တွင်
ပါဝင်မှု၊ lab တိုင်း `--self-test` အောင်မြင်မှု (offline၊ deterministic)။
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
GUIDE = REPO / "guides" / "02_models_and_inference"
SLICE = REPO / "glossary" / "by_area" / "02_models_and_inference.json"
REQUIRED_DOCS = ["README.md", "01_learning_sequence.md", "02_visual_explanations.md",
                 "03_theory_to_infrastructure.md", "04_exercises.md", "labs/README.md"]
LABS = ["lab_sampling.py", "lab_kv_cache.py", "lab_quantization.py", "lab_attention_cost.py",
        "lab_batching.py", "lab_context_budget.py"]
BANNED = ["ပါတယ်", "ပါဘူး", "ရမယ်", "ဖြစ်တယ်", "တဲ့", "နဲ့", "ဖို့", "ရဲ့", "နော်", "ပေါ့", "လို့", "ဆိုတာ", "ဒီ"]


def foreign(text: str) -> list[str]:
    bad = set()
    for ch in text:
        code = ord(ch)
        if 0x3000 <= code <= 0x9FFF or 0xAC00 <= code <= 0xD7AF or 0x0900 <= code <= 0x097F:
            bad.add(ch)
        if 0x1F300 <= code <= 0x1FAFF or 0x2600 <= code <= 0x27BF:
            bad.add(ch)
    return sorted(bad)


def check_documents(verbose: bool) -> list[str]:
    problems: list[str] = []
    for name in REQUIRED_DOCS:
        path = GUIDE / name
        if not path.exists():
            problems.append(f"{name}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if len(text) < 800:
            problems.append(f"{name}: only {len(text)} chars — too thin to teach anything")
        for marker in BANNED:
            if marker in text:
                problems.append(f"{name}: colloquial marker {marker} on line "
                                f"{[i + 1 for i, l in enumerate(text.splitlines()) if marker in l][:3]}")
        bad = foreign(text)
        if bad:
            problems.append(f"{name}: foreign glyphs {bad}")
        if verbose:
            print(f"  {name}: {len(text)} chars, {len(text.splitlines())} lines")
    seq = GUIDE / "01_learning_sequence.md"
    if seq.exists():
        text = seq.read_text(encoding="utf-8")
        terms = [e["term"] for e in json.loads(SLICE.read_text(encoding="utf-8"))]
        missing = [t for t in terms if t not in text]
        if missing:
            problems.append(f"01_learning_sequence.md: {len(missing)} term(s) absent from the sequence: {missing[:4]}")
        elif verbose:
            print(f"  01_learning_sequence.md: all {len(terms)} terms placed in the sequence")
    return problems


def check_labs(verbose: bool) -> list[str]:
    problems: list[str] = []
    for name in LABS:
        path = GUIDE / "labs" / name
        if not path.exists():
            problems.append(f"labs/{name}: file is missing")
            continue
        source = path.read_text(encoding="utf-8")
        if "--self-test" not in source:
            problems.append(f"labs/{name}: no --self-test entry point")
            continue
        results = []
        for _ in range(3):
            run = subprocess.run([sys.executable, str(path), "--self-test"], capture_output=True, text=True, timeout=120)
            results.append((run.returncode, run.stdout))
        codes = {c for c, _ in results}
        if codes != {0}:
            problems.append(f"labs/{name}: --self-test exit codes {sorted(codes)}")
            continue
        if len({o for _, o in results}) != 1:
            problems.append(f"labs/{name}: --self-test output differs between runs (not deterministic)")
        if verbose:
            print(f"  labs/{name}: 3 runs, exit 0, output identical")
    runner = GUIDE / "labs" / "run_labs.py"
    if not runner.exists():
        problems.append("labs/run_labs.py: file is missing")
    else:
        run = subprocess.run([sys.executable, str(runner)], capture_output=True, text=True, timeout=600)
        if run.returncode != 0:
            problems.append(f"labs/run_labs.py: exit {run.returncode}")
        elif verbose:
            print("  labs/run_labs.py:", run.stdout.strip().splitlines()[-1])
    return problems


def check_examples(verbose: bool) -> list[str]:
    """Every pasted run in the guide must still reproduce from the script it names."""
    problems: list[str] = []
    for name in REQUIRED_DOCS + ["labs/README.md"]:
        path = (GUIDE / name)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for cmd, pasted in re.findall(r"```text\n\$ python3 (\S+)\n(.*?)```", text, re.S):
            target = cmd.replace("guides/02_models_and_inference/", f"{GUIDE}/")
            if not Path(target).exists():
                problems.append(f"{name}: pasted example runs {cmd}, which does not exist")
                continue
            run = subprocess.run([sys.executable, target], capture_output=True, text=True, timeout=180)
            if run.stdout.rstrip().strip() != pasted.rstrip().strip():
                problems.append(f"{name}: the pasted output of {os.path.basename(cmd)} no longer matches the run")
            elif verbose:
                print(f"  {name}: {os.path.basename(cmd)} output reproduces byte-for-byte")
        if name.startswith("labs/README"):
            for bash, pasted in re.findall(r"```bash\n(.*?)```\n(?:.*?\n)?```\n(.*?)```", text, re.S):
                lines = [l.split("#")[0].strip() for l in bash.splitlines() if l.strip().startswith("python3")]
                if not lines:
                    continue
                parts = lines[0].split()
                script = GUIDE / "labs" / parts[1].split("/")[-1]
                if not script.exists():
                    problems.append(f"{name}: {parts[1]} does not exist")
                    continue
                run = subprocess.run([sys.executable, str(script)] + parts[2:], capture_output=True, text=True, timeout=180)
                if run.stdout.rstrip().strip() != pasted.rstrip().strip():
                    problems.append(f"{name}: the pasted output of {parts[1]} no longer matches the run")
                elif verbose:
                    print(f"  {name}: {parts[1]} output reproduces byte-for-byte")
    return problems


def check_script_refs() -> list[str]:
    """The calculation scripts the guide names must exist in scripts/."""
    problems: list[str] = []
    text = "\n".join(p.read_text(encoding="utf-8") for p in GUIDE.glob("*.md"))
    for ref in sorted(set(re.findall(r"scripts/[\w.]+\.py", text))):
        if not (GUIDE / ref).exists():
            problems.append(f"{ref}: referenced by the guide but missing from scripts/")
    scripts = sorted(p.name for p in (GUIDE / "scripts").glob("*.py")) if (GUIDE / "scripts").exists() else []
    if not scripts:
        problems.append("scripts/: no calculation script is present")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify the area 02 model guide.")
    ap.add_argument("--documents", action="store_true")
    ap.add_argument("--labs", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    do_docs = args.documents or not args.labs
    do_labs = args.labs or not args.documents

    problems: list[str] = []
    print("=" * 74)
    if do_docs:
        problems += check_documents(args.verbose)
    if do_labs:
        problems += check_labs(args.verbose)
    if do_docs:
        problems += check_examples(args.verbose)
        problems += check_script_refs()
    print("=" * 74)
    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems[:40]:
            print("  -", p)
        return 1
    print("[PASS] The area 02 guide is complete, in register, and every lab passes offline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

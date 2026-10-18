#!/usr/bin/env python3
"""run_labs - area 03 (Data & representations) ၏ lab သုံးခုလုံးကို `--self-test` ဖြင့် run သည်။

    python3 run_labs.py

Lab တိုင်းအတွက် တစ်လိုင်း ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်၊ တစ်ခုခု ကျရှုံးပါက
`[FAIL]` ဖြင့် ပြီး exit 1 ဖြစ်သည်။ Offline ဖြစ်သည်၊ network သို့မဟုတ် GPU မလိုအပ်ပါ။
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

LABS_DIR = Path(__file__).resolve().parent
LABS = [
    "lab_tokenizer.py",
    "lab_split_leak.py",
    "lab_pipeline_budget.py",
]
RULE = "=" * 74


def main() -> int:
    print(RULE)
    print("run_labs - area 03 Data & representations (offline, deterministic)")
    print(RULE)
    passed = 0
    for name in LABS:
        path = LABS_DIR / name
        if not path.exists():
            print(f"[FAIL] {name}: file is missing")
            continue
        run = subprocess.run([sys.executable, str(path), "--self-test"],
                             capture_output=True, text=True, cwd=str(LABS_DIR), timeout=300)
        last = run.stdout.strip().splitlines()[-1] if run.stdout.strip() else "(no output)"
        if run.returncode == 0 and last.startswith("[PASS]"):
            passed += 1
            print(f"[PASS] {name}: {last}")
        else:
            print(f"[FAIL] {name}: exit {run.returncode} - {last}")
    print(RULE)
    if passed == len(LABS):
        print(f"[PASS] All {passed}/{len(LABS)} labs passed successfully.")
        return 0
    print(f"[FAIL] Only {passed}/{len(LABS)} labs passed successfully.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

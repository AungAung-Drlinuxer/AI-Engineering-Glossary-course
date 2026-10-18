#!/usr/bin/env python3
"""lab_context_strategy - context strategy သုံးမျိုးကို token နှင့် cost အနေဖြင့် နှိုင်းယှဉ်သည်။

whole-repo context၊ directory-scoped context နှင့် retrieval-scoped context သုံးမျိုးအတွက်
token အရေအတွက်၊ ကုန်ကျစရိတ်၊ window ထဲ ဆံ့မှု နှင့် whole-repo နှင့် နှိုင်းယှဉ်သည့် ချွေတာမှုကို
ပြသည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ —
    context_tokens = files * avg_file_tokens
    cost_usd       = context_tokens / 1e6 * price_per_mtok
    saving         = 1 - scoped_tokens / whole_tokens
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74
MTOK = 1_000_000.0

DEFAULT_REPO_FILES = 900
DEFAULT_AVG_FILE_TOKENS = 420
DEFAULT_SCOPE_FILES = 60
DEFAULT_WINDOW = 128000
DEFAULT_PRICE_PER_MTOK = 3.00

# ယူဆချက် (assumption) — retrieval scope သည် ရွေးထုတ်သည့် ဖိုင် အရေအတွက် ဖြစ်သည်။
RETRIEVAL_FILES = 12
SWEEP_SCOPE_FILES = (8, 16, 32, 64, 128, 256, 512, 900)


def context_tokens(files: int, avg_file_tokens: int) -> int:
    return files * avg_file_tokens


def cost_usd(tokens: int, price_per_mtok: float) -> float:
    return tokens / MTOK * price_per_mtok


def strategy_rows(repo_files: int, avg_file_tokens: int, scope_files: int,
                  window: int, price_per_mtok: float) -> list[dict]:
    rows = [("whole-repo", repo_files),
            ("directory-scoped", scope_files),
            ("retrieval-scoped", RETRIEVAL_FILES)]
    whole_tokens = context_tokens(repo_files, avg_file_tokens)
    out = []
    for name, files in rows:
        tokens = context_tokens(files, avg_file_tokens)
        out.append({
            "name": name,
            "files": files,
            "tokens": tokens,
            "cost": cost_usd(tokens, price_per_mtok),
            "fits": tokens <= window,
            "saving": 0.0 if whole_tokens == 0 else 1.0 - tokens / whole_tokens,
        })
    return out


def report(repo_files: int, avg_file_tokens: int, scope_files: int,
           window: int, price_per_mtok: float) -> None:
    rows = strategy_rows(repo_files, avg_file_tokens, scope_files, window, price_per_mtok)
    print(RULE)
    print("lab_context_strategy - whole-repo vs scoped context (offline, deterministic)")
    print(f"repo-files={repo_files:,}  avg-file-tokens={avg_file_tokens:,}  "
          f"scope-files={scope_files:,}  window={window:,}  price=USD {price_per_mtok:.2f}/Mtok")
    print(f"assumption - retrieval scope = {RETRIEVAL_FILES} files; "
          f"price is an assumed input-token price.")
    print(THIN)
    print(f"{'strategy':<18}{'files':>7}{'context tokens':>16}{'USD/task':>11}"
          f"  {'fits window':<12}{'saving vs whole':>16}")
    for r in rows:
        saving = "-" if r["name"] == "whole-repo" else f"{r['saving'] * 100:.2f}%"
        print(f"{r['name']:<18}{r['files']:>7,}{r['tokens']:>16,}{r['cost']:>11.4f}"
              f"  {'YES' if r['fits'] else 'NO':<12}{saving:>16}")
    print(THIN)
    dir_row = rows[1]
    ret_row = rows[2]
    print(f"retrieval-scoped saves USD {rows[0]['cost'] - ret_row['cost']:.4f} per task "
          f"against whole-repo context")
    print(f"directory-scoped stays {dir_row['tokens'] / window * 100:.2f}% of the window; "
          f"whole-repo needs {rows[0]['tokens'] / window:.2f}x the window")
    print("မှတ်ချက် - context ကို ကျဉ်းစွာ ရွေးလျှင် token နှင့် ကုန်ကျစရိတ် ကျဆင်းသည်၊ "
          "သို့သော် လိုအပ်သည့် အထောက်အထား မကျန်ခဲ့ရန် သတိထားရမည်။")
    print(RULE)


def sweep(repo_files: int, avg_file_tokens: int, window: int, price_per_mtok: float) -> None:
    print(RULE)
    print("lab_context_strategy --sweep : scope-files အလိုက် context ကုန်ကျစရိတ်")
    print(f"repo-files={repo_files:,}  avg-file-tokens={avg_file_tokens:,}  "
          f"window={window:,}  price=USD {price_per_mtok:.2f}/Mtok")
    print(f"assumption - retrieval scope = {RETRIEVAL_FILES} files")
    print(THIN)
    print(f"{'scope-files':>11}{'context tokens':>16}{'USD/task':>11}  "
          f"{'fits window':<12}{'saving vs whole':>16}")
    whole = context_tokens(repo_files, avg_file_tokens)
    for files in SWEEP_SCOPE_FILES:
        tokens = context_tokens(files, avg_file_tokens)
        print(f"{files:>11,}{tokens:>16,}{cost_usd(tokens, price_per_mtok):>11.4f}"
              f"  {'YES' if tokens <= window else 'NO':<12}"
              f"{100.0 * (1.0 - tokens / whole):>15.2f}%")
    print("မှတ်ချက် - scope-files တိုးလျှင် token နှင့် ကုန်ကျစရိတ် တိုးသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    whole = context_tokens(DEFAULT_REPO_FILES, DEFAULT_AVG_FILE_TOKENS)
    ret = context_tokens(RETRIEVAL_FILES, DEFAULT_AVG_FILE_TOKENS)
    t1 = whole == DEFAULT_REPO_FILES * DEFAULT_AVG_FILE_TOKENS
    print(f"[OK] context tokens = files * avg-file-tokens ({whole:,}): {t1}")
    ok = ok and t1

    t2 = abs(cost_usd(whole, 3.0) - 3.0 * cost_usd(whole, 1.0)) < 1e-9
    print(f"[OK] cost is linear in tokens and price "
          f"({cost_usd(whole, 3.0):.4f} USD): {t2}")
    ok = ok and t2

    t3 = whole > DEFAULT_WINDOW and ret < DEFAULT_WINDOW
    print(f"[OK] whole-repo context does not fit the window while retrieval does "
          f"({whole:,} > {DEFAULT_WINDOW:,} > {ret:,}): {t3}")
    ok = ok and t3

    rows = strategy_rows(DEFAULT_REPO_FILES, DEFAULT_AVG_FILE_TOKENS,
                         DEFAULT_SCOPE_FILES, DEFAULT_WINDOW, 3.0)
    t4 = (rows[1]["tokens"] > rows[2]["tokens"]
          and abs(rows[2]["saving"] - (1.0 - ret / whole)) < 1e-12
          and rows[2]["saving"] > rows[1]["saving"])
    print(f"[OK] retrieval-scoped saves more than directory-scoped "
          f"({rows[2]['saving'] * 100:.2f}% > {rows[1]['saving'] * 100:.2f}%): {t4}")
    ok = ok and t4

    same = strategy_rows(DEFAULT_REPO_FILES, DEFAULT_AVG_FILE_TOKENS,
                         DEFAULT_REPO_FILES, DEFAULT_WINDOW, 3.0)
    t5 = same[0]["tokens"] == same[1]["tokens"] and same[1]["saving"] == 0.0
    print(f"[OK] a scope equal to the whole repo saves nothing "
          f"(saving {same[1]['saving'] * 100:.2f}%): {t5}")
    ok = ok and t5

    print("[PASS] lab_context_strategy self-test passed." if ok
          else "[FAIL] lab_context_strategy self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Whole-repo vs scoped context: tokens and cost (offline, deterministic).")
    ap.add_argument("--repo-files", type=int, default=DEFAULT_REPO_FILES)
    ap.add_argument("--avg-file-tokens", type=int, default=DEFAULT_AVG_FILE_TOKENS)
    ap.add_argument("--scope-files", type=int, default=DEFAULT_SCOPE_FILES)
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW)
    ap.add_argument("--price-per-mtok", type=float, default=DEFAULT_PRICE_PER_MTOK)
    ap.add_argument("--sweep", action="store_true", help="vary scope-files across a range")
    ap.add_argument("--self-test", action="store_true",
                    help="assert the context-strategy properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        sweep(args.repo_files, args.avg_file_tokens, args.window, args.price_per_mtok)
        return 0
    report(args.repo_files, args.avg_file_tokens, args.scope_files,
           args.window, args.price_per_mtok)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

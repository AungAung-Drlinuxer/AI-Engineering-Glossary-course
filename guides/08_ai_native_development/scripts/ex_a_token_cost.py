#!/usr/bin/env python3
"""ex_a_token_cost - သတ်မှတ်ထားသည့် repository အရွယ်အစား တစ်ခုအတွက် လုပ်ငန်းတစ်ခုလျှင် token
ကုန်ကျစရိတ်ကို context strategy နှစ်မျိုးဖြင့် နှိုင်းယှဉ် တွက်ချက်သည် — whole-repo context
နှင့် retrieval-scoped context ဖြစ်သည်။

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ standard library သာ အသုံးပြုသည်။

ဖော်မြူလာ —
    context_tokens(strategy) = files(strategy) * avg_file_tokens
    input_tokens            = rounds * context_tokens(strategy)
    output_tokens           = rounds * output_tokens_per_round
    cost_per_task           = input_tokens/Mtok * input_price + output_tokens/Mtok * output_price

ဤဖိုင်ရှိ ကိန်းဂဏန်း အားလုံးသည် အောက်ပါ ယူဆချက် (assumption) များမှ တွက်ချက်ထားသည်။
"""

from __future__ import annotations

import argparse

RULE = "=" * 74
THIN = "-" * 74
MTOK = 1_000_000.0

# ယူဆချက် အားလုံး (assumptions) — ဤတန်ဖိုးများသည် အခြေအနေအလိုက် ကွာခြားသည်။
REPO_FILES = 900
AVG_FILE_TOKENS = 420
RETRIEVAL_FILES = 12
ROUNDS = 6
OUTPUT_TOKENS_PER_ROUND = 700
WINDOW = 128000
INPUT_PRICE = 3.00
OUTPUT_PRICE = 15.00


def context_tokens(files: int, avg_file_tokens: int = AVG_FILE_TOKENS) -> int:
    return files * avg_file_tokens


def input_tokens(files: int, rounds: int = ROUNDS,
                 avg_file_tokens: int = AVG_FILE_TOKENS) -> int:
    return rounds * context_tokens(files, avg_file_tokens)


def output_tokens(rounds: int = ROUNDS,
                  per_round: int = OUTPUT_TOKENS_PER_ROUND) -> int:
    return rounds * per_round


def cost_per_task(files: int, rounds: int = ROUNDS,
                  avg_file_tokens: int = AVG_FILE_TOKENS,
                  input_price: float = INPUT_PRICE,
                  output_price: float = OUTPUT_PRICE) -> float:
    inp = input_tokens(files, rounds, avg_file_tokens)
    out = output_tokens(rounds)
    return inp / MTOK * input_price + out / MTOK * output_price


def rows() -> list[tuple[str, int, int, int, float, bool]]:
    table = []
    for name, files in (("whole-repo", REPO_FILES),
                        ("directory-scoped", 60),
                        ("retrieval-scoped", RETRIEVAL_FILES)):
        ctx = context_tokens(files)
        tok = input_tokens(files)
        cost = cost_per_task(files)
        table.append((name, files, ctx, tok, cost, ctx <= WINDOW))
    return table


def report() -> None:
    base = cost_per_task(REPO_FILES)
    table = rows()
    print(RULE)
    print("ex_a_token_cost - token cost per task for a stated repository size")
    print(RULE)
    print(f"assumed repository: {REPO_FILES} files x {AVG_FILE_TOKENS} tokens/file "
          f"= {context_tokens(REPO_FILES):,} context tokens")
    print(f"assumed task       : {ROUNDS} agent rounds, "
          f"{OUTPUT_TOKENS_PER_ROUND} output tokens/round")
    print(f"assumed price      : USD {INPUT_PRICE:.2f} per 1M input tokens, "
          f"USD {OUTPUT_PRICE:.2f} per 1M output tokens")
    print(f"assumed window     : {WINDOW:,} tokens")
    print(THIN)
    print(f"{'strategy':<18}{'files':>7}{'ctx tok/round':>16}{'input tok':>13}"
          f"{'output tok':>12}{'USD/task':>11}  fits")
    for name, files, ctx, tok, cost, fits in table:
        print(f"{name:<18}{files:>7,}{ctx:>16,}{tok:>13,}"
              f"{output_tokens():>12,}{cost:>11.4f}  {'YES' if fits else 'NO'}")
    print(THIN)
    scoped = cost_per_task(RETRIEVAL_FILES)
    saved = base - scoped
    print(f"saving with retrieval-scoped context = USD {saved:.4f} per task "
          f"({saved / base * 100:.2f}%)")
    print(f"context the whole-repo strategy needs per round is "
          f"{context_tokens(REPO_FILES) // WINDOW}x the window")
    print("မှတ်ချက် - whole-repo context သည် window ထဲ မဆံ့သောကြောင့် မဖြစ်နိုင်ပါ၊ "
          "scoped retrieval သည် token နှင့် ကုန်ကျစရိတ် နှစ်ခုလုံးကို လျှော့ချသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    whole = context_tokens(REPO_FILES)
    retr = context_tokens(RETRIEVAL_FILES)
    t1 = whole == REPO_FILES * AVG_FILE_TOKENS
    print(f"[OK] whole-repo context tokens = files * avg_file_tokens ({whole:,}): {t1}")
    ok = ok and t1

    t2 = retr * 10 == context_tokens(RETRIEVAL_FILES * 10)
    print(f"[OK] context tokens scale linearly with the file count "
          f"({retr:,} -> {context_tokens(RETRIEVAL_FILES * 10):,}): {t2}")
    ok = ok and t2

    inp = input_tokens(REPO_FILES)
    t3 = abs((cost_per_task(REPO_FILES, input_price=6.0) -
              cost_per_task(REPO_FILES, input_price=3.0)) - inp / MTOK * 3.0) < 1e-6
    print(f"[OK] the input-price term scales linearly with the price: {t3}")
    ok = ok and t3

    t4 = whole > WINDOW and retr < WINDOW
    print(f"[OK] whole-repo exceeds the window while retrieval-scoped fits "
          f"({whole:,} > {WINDOW:,} > {retr:,}): {t4}")
    ok = ok and t4

    saved = cost_per_task(REPO_FILES) - cost_per_task(RETRIEVAL_FILES)
    t5 = saved > 0 and abs(cost_per_task(REPO_FILES) / cost_per_task(RETRIEVAL_FILES)
                           - (REPO_FILES / RETRIEVAL_FILES * AVG_FILE_TOKENS /
                              (RETRIEVAL_FILES * AVG_FILE_TOKENS))) > 0
    print(f"[OK] retrieval-scoped context costs less than whole-repo "
          f"(USD {saved:.4f} saved): {t5}")
    ok = ok and t5

    print("[PASS] ex_a_token_cost self-test passed." if ok
          else "[FAIL] ex_a_token_cost self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Token cost per task for a stated repository size (offline, deterministic).")
    ap.add_argument("--self-test", action="store_true", help="assert the cost properties")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""lab_prompt_budget - retrieved tokens, history room, overflow and cost per query.

Offline, deterministic, standard library only.

Model (assumptions):
  prompt        = system + question + retrieved, with retrieved = chunk * k
  reservations  : system = 400 tokens, question = 60 tokens, output reserve from --reserve
  history room  : window - system - question - retrieved - reserve
                  positive -> headroom, negative -> overflow
  input price   : 2.00 USD per million tokens
  answer        : 300 output tokens at 8.00 USD per million output tokens
  cost per query = (system + question + retrieved) / 1e6 * input price

Flags:
  --chunk, --k, --window, --reserve, --sweep, --self-test
"""

from __future__ import annotations

import argparse

SYSTEM_TOKENS = 400
QUESTION_TOKENS = 60
ANSWER_TOKENS = 300
IN_PRICE = 2.00
OUT_PRICE = 8.00
KS = (1, 2, 5, 10, 20)
SWEEP_KS = (1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 40)
RULE = "=" * 74
THIN = "-" * 74


def retrieved_tokens(chunk: int, k: int) -> int:
    return chunk * k


def prompt_tokens(chunk: int, k: int) -> int:
    return SYSTEM_TOKENS + QUESTION_TOKENS + retrieved_tokens(chunk, k)


def history_room(window: int, chunk: int, k: int, reserve: int) -> int:
    return window - prompt_tokens(chunk, k) - reserve


def cost_per_1000(chunk: int, k: int) -> float:
    return prompt_tokens(chunk, k) / 1e6 * IN_PRICE * 1000.0


def status(window: int, chunk: int, k: int, reserve: int) -> str:
    room = history_room(window, chunk, k, reserve)
    return f"FITS headroom {room:,} tokens" if room >= 0 else f"OVERFLOW {-room:,} tokens"


def print_report(chunk: int, k: int, window: int, reserve: int) -> None:
    room = history_room(window, chunk, k, reserve)
    print(RULE)
    print("lab_prompt_budget - retrieved tokens, history room, cost (offline, deterministic)")
    print(f"chunk={chunk}  k={k}  window={window:,}  reserve={reserve:,}  "
          f"system={SYSTEM_TOKENS}  question={QUESTION_TOKENS} (assumptions)")
    print(THIN)
    print(f"  retrieved tokens              : {retrieved_tokens(chunk, k):>12,}")
    print(f"  prompt tokens                 : {prompt_tokens(chunk, k):>12,}")
    print(f"  reserved for the answer       : {reserve:>12,}")
    print(f"  room left for history         : {room:>12,}")
    print(f"  status                        : {status(window, chunk, k, reserve)}")
    print(f"  input cost per query (USD)    : {prompt_tokens(chunk, k) / 1e6 * IN_PRICE:>12.6f}")
    print(f"  input cost per 1000 queries   : {cost_per_1000(chunk, k):>12.4f}")
    print(f"  total per 1000 queries        : "
          f"{cost_per_1000(chunk, k) + ANSWER_TOKENS / 1e6 * OUT_PRICE * 1000:>12.4f}")
    print(THIN)
    print(f"effect of k at chunk={chunk} (window={window:,}, reserve={reserve:,}):")
    print("    k   retrieved   prompt tok   room for history   USD/1k input")
    for kk in KS:
        r = history_room(window, chunk, kk, reserve)
        print(f"  {kk:>3} {retrieved_tokens(chunk, kk):>11,} {prompt_tokens(chunk, kk):>12,} "
              f"{r:>18,} {cost_per_1000(chunk, kk):>14.4f}")
    print(THIN)
    print("မှတ်ချက် - k တိုးလျှင် ရရှိသည့် အထောက်အထား တိုးသော်လည်း prompt token၊ ကုန်ကျစရိတ် "
          "နှင့် history အတွက် ကျန်နေရာ လျော့သည်။")
    print(RULE)


def print_sweep(chunk: int, window: int, reserve: int) -> None:
    print(RULE)
    print(f"lab_prompt_budget - k sweep 1..40 (chunk={chunk}, window={window:,}, "
          f"reserve={reserve:,})")
    print(THIN)
    print("    k   retrieved   room for history   status              USD/1k input")
    for kk in SWEEP_KS:
        r = history_room(window, chunk, kk, reserve)
        tag = "FITS" if r >= 0 else "OVERFLOW"
        print(f"  {kk:>3} {retrieved_tokens(chunk, kk):>11,} {r:>18,}   {tag:<8}"
              f"{cost_per_1000(chunk, kk):>18.4f}")
    print(THIN)
    print("မှတ်ချက် - room for history သည် k တိုးလျှင် chunk token အရေအတွက်အတိုင်း "
          "တိုက်ရိုက် လျော့သည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    r = retrieved_tokens(400, 5) == 2000
    print(f"[OK] retrieved tokens are chunk * k (400 * 5 = {retrieved_tokens(400, 5)}): {r}")
    ok = ok and r

    step = (retrieved_tokens(400, 6) - retrieved_tokens(400, 5)) == 400
    print(f"[OK] raising k by one adds exactly one chunk of tokens: {step}")
    ok = ok and step

    window, reserve = 32000, 4096
    room5 = history_room(window, 400, 5, reserve)
    room10 = history_room(window, 400, 10, reserve)
    drop = (room5 - room10) == 400 * 5
    print(f"[OK] doubling k from 5 to 10 removes {room5 - room10:,} tokens of history room: {drop}")
    ok = ok and drop

    shrunk = history_room(window, 400, 5, reserve + 1000) == room5 - 1000
    print(f"[OK] a larger output reserve reduces history room one for one: {shrunk}")
    ok = ok and shrunk

    overflow = history_room(5000, 400, 5, reserve) < 0
    fits = history_room(32000, 400, 5, reserve) > 0
    print(f"[OK] a small window overflows and a large one fits: {overflow and fits}")
    ok = ok and overflow and fits

    c1 = cost_per_1000(400, 5)
    c2 = cost_per_1000(400, 10)
    linear = abs((c2 - c1) - 400 * 5 / 1e6 * IN_PRICE * 1000.0) < 1e-9
    print(f"[OK] cost grows linearly with the retrieved tokens "
          f"({c1:.4f} -> {c2:.4f} USD per 1000 queries): {linear}")
    ok = ok and linear

    answer = abs(ANSWER_TOKENS / 1e6 * OUT_PRICE * 1000.0 - 2.40) < 1e-9
    print(f"[OK] the answer cost is independent of k "
          f"({ANSWER_TOKENS / 1e6 * OUT_PRICE * 1000.0:.4f} USD per 1000 queries): {answer}")
    ok = ok and answer

    print("[PASS] lab_prompt_budget self-test passed." if ok
          else "[FAIL] lab_prompt_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Prompt budget, history room and cost per query (offline, deterministic).")
    ap.add_argument("--chunk", type=int, default=400, help="tokens per retrieved chunk")
    ap.add_argument("--k", type=int, default=5, help="chunks retrieved per query")
    ap.add_argument("--window", type=int, default=32000, help="context window in tokens")
    ap.add_argument("--reserve", type=int, default=4096, help="tokens reserved for the answer")
    ap.add_argument("--sweep", action="store_true", help="k sweep 1..40")
    ap.add_argument("--self-test", action="store_true", help="assert the taught properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.chunk, args.window, args.reserve)
        return 0
    print_report(args.chunk, args.k, args.window, args.reserve)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

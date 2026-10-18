#!/usr/bin/env python3
"""lab_token_budget - allocate token capacity across the parts of a prompt.

Offline, deterministic, standard library only.

Model (shown, the only source of the numbers below)

    examples_tokens = example_count * EXAMPLE_TOKENS
    input_tokens    = system + instructions + examples_tokens + retrieved + history
    used            = input_tokens + reserve_output
    fits            = used <= window          headroom = window - used
    overflow        = used - window           (only when used > window)
    cost_per_call   = input_tokens * input_price / 1e6
                    + reserve_output * output_price / 1e6

Stated assumptions

    each few-shot example = 120 tokens
    input  price = USD 3.00  per 1e6 tokens
    output price = USD 15.00 per 1e6 tokens
    reserve_output is part of the budget, so it is never subtracted away
"""

from __future__ import annotations

import argparse

EXAMPLE_TOKENS = 120
IN_PRICE = 3.00
OUT_PRICE = 15.00
KEEP_RETRIEVED = 8000
HISTORY_KEEP_FRACTION = 0.25
RULE = "=" * 74
THIN = "-" * 74


def input_tokens(system: int, instructions: int, examples: int, retrieved: int, history: int) -> int:
    return system + instructions + examples * EXAMPLE_TOKENS + retrieved + history


def budget(window: int, system: int, instructions: int, examples: int,
           retrieved: int, history: int, reserve: int) -> dict[str, float]:
    inp = input_tokens(system, instructions, examples, retrieved, history)
    used = inp + reserve
    return {
        "input": float(inp),
        "used": float(used),
        "headroom": float(window - used),
        "overflow": float(max(0, used - window)),
        "fits": 1.0 if used <= window else 0.0,
    }


def remedies(system: int, examples: int, retrieved: int, history: int) -> list[tuple[str, int]]:
    return [
        ("shrink retrieved context to %d tokens" % KEEP_RETRIEVED,
         max(0, retrieved - KEEP_RETRIEVED)),
        ("summarise history to %d%% of its size" % int(HISTORY_KEEP_FRACTION * 100),
         max(0, history - int(history * HISTORY_KEEP_FRACTION))),
        ("drop few-shot examples beyond the first", max(0, (examples - 1) * EXAMPLE_TOKENS)),
        ("trim the system prompt by half", max(0, system // 2)),
    ]


def cost(inp: int, reserve: int) -> float:
    return inp * IN_PRICE / 1e6 + reserve * OUT_PRICE / 1e6


def print_report(window: int, system: int, instructions: int, examples: int,
                 retrieved: int, history: int, reserve: int) -> None:
    b = budget(window, system, instructions, examples, retrieved, history, reserve)
    rem = remedies(system, examples, retrieved, history)
    total_freed = sum(v for _, v in rem)
    used_after = b["used"] - total_freed
    inp_after = b["input"] - total_freed
    print(RULE)
    print("lab_token_budget - token budget breakdown (offline, deterministic)")
    print("window=%s  system=%s  instructions=%s  examples=%d x %d  retrieved=%s  "
          "history=%s  reserve-output=%s"
          % (f"{window:,}", f"{system:,}", f"{instructions:,}", examples, EXAMPLE_TOKENS,
             f"{retrieved:,}", f"{history:,}", f"{reserve:,}"))
    print(THIN)
    print("  system prompt             : %10s" % f"{system:,}")
    print("  task instructions         : %10s" % f"{instructions:,}")
    print("  few-shot examples         : %10s   (%d x %d tokens)"
          % (f"{examples * EXAMPLE_TOKENS:,}", examples, EXAMPLE_TOKENS))
    print("  retrieved context         : %10s" % f"{retrieved:,}")
    print("  conversation history      : %10s" % f"{history:,}")
    print("  reserved for output       : %10s" % f"{reserve:,}")
    print("  prompt tokens (input)     : %10s" % f"{b['input']:,.0f}")
    print("  used (input + reserve)    : %10s  (%.2f%% of window)"
          % (f"{b['used']:,.0f}", b["used"] / window * 100.0))
    if b["fits"]:
        print("  status                    : %10s  headroom %s tokens"
              % ("FITS", f"{b['headroom']:,.0f}"))
    else:
        print("  status                    : %10s  shortfall %s tokens"
              % ("OVERFLOW", f"{b['overflow']:,.0f}"))
    print(THIN)
    print("Remedies (each frees tokens):")
    for label, freed in rem:
        print("  %-46s frees %8s" % (label, f"{freed:,}"))
    print("  total freed %s tokens -> used after remedies %s, headroom %s"
          % (f"{total_freed:,}", f"{used_after:,.0f}", f"{window - used_after:,.0f}"))
    print(THIN)
    print("Cost per call at USD %.2f/1e6 input + USD %.2f/1e6 output (assumption):" % (IN_PRICE, OUT_PRICE))
    print("  input %s tok = USD %.6f ; output %s tok = USD %.6f ; total USD %.6f"
          % (f"{b['input']:,.0f}", b["input"] * IN_PRICE / 1e6, f"{reserve:,}",
             reserve * OUT_PRICE / 1e6, cost(int(b["input"]), reserve)))
    print("  after remedies: input %s tok = USD %.6f ; total USD %.6f"
          % (f"{inp_after:,.0f}", inp_after * IN_PRICE / 1e6, cost(int(inp_after), reserve)))
    print("မှတ်ချက် - budget သည် reserved output ပါဝင်မှသာ လုံခြုံသည်၊ ထို့ကြောင့် reserve-output ကို "
          "နုတ်မထားရ။")
    print(RULE)


def print_sweep(window: int, system: int, instructions: int, examples: int,
                retrieved: int, reserve: int) -> None:
    print(RULE)
    print("lab_token_budget - sweep: conversation history 0 -> %s" % f"{window:,}")
    print("window=%s  system=%s  instructions=%s  examples=%d  retrieved=%s  reserve-output=%s"
          % (f"{window:,}", f"{system:,}", f"{instructions:,}", examples, f"{retrieved:,}",
             f"{reserve:,}"))
    print(THIN)
    print("%12s %12s %10s  %-10s %14s" % ("history", "input tok", "used %", "status", "USD/call"))
    step = max(1, window // 8)
    history = 0
    while history <= window:
        b = budget(window, system, instructions, examples, retrieved, history, reserve)
        status = "FITS" if b["fits"] else "OVERFLOW"
        print("%12s %12s %9.2f%%  %-10s %14.6f"
              % (f"{history:,}", f"{b['input']:,.0f}", b["used"] / window * 100.0, status,
                 cost(int(b["input"]), reserve)))
        history += step
    print(THIN)
    print("trend: every added history token raises used by one token and raises cost by USD %.8f"
          % (IN_PRICE / 1e6))
    print(RULE)


def self_test() -> int:
    ok = True

    fits = budget(128000, 500, 400, 3, 24000, 30000, 4096)
    fits_ok = (fits["fits"] == 1.0 and fits["headroom"] > 0
               and fits["used"] + fits["headroom"] == 128000.0)
    print("[OK] a budget inside the window reports headroom (%s tokens): %s"
          % (f"{fits['headroom']:,.0f}", fits_ok))
    ok = ok and fits_ok

    over = budget(128000, 500, 400, 3, 24000, 100000, 4096)
    over_ok = (over["fits"] == 0.0 and over["overflow"] > 0
               and abs(over["overflow"] - (over["used"] - 128000.0)) < 1e-9
               and over["headroom"] < 0)
    print("[OK] an oversized history reports the shortfall (%s tokens): %s"
          % (f"{over['overflow']:,.0f}", over_ok))
    ok = ok and over_ok

    rem = remedies(500, 3, 24000, 100000)
    freed = sum(v for _, v in rem)
    rem_ok = all(v > 0 for _, v in rem) and (over["used"] - freed <= 128000.0)
    print("[OK] the four remedies free %s tokens and resolve the overflow: %s"
          % (f"{freed:,}", rem_ok))
    ok = ok and rem_ok

    one = budget(128000, 500, 400, 1, 24000, 30000, 4096)
    three = budget(128000, 500, 400, 3, 24000, 30000, 4096)
    ex_ok = abs((three["input"] - one["input"]) - 2 * EXAMPLE_TOKENS) < 1e-9
    print("[OK] each extra example adds %d tokens (2 examples add %s): %s"
          % (EXAMPLE_TOKENS, f"{int(three['input'] - one['input']):,}", ex_ok))
    ok = ok and ex_ok

    base = budget(128000, 500, 400, 3, 24000, 30000, 4096)
    bigger = budget(128000, 500, 400, 3, 24000, 30000, 8192)
    res_ok = (abs((bigger["used"] - base["used"]) - 4096.0) < 1e-9
              and abs((base["headroom"] - bigger["headroom"]) - 4096.0) < 1e-9)
    print("[OK] the output reserve counts against the window and is not subtracted: %s" % res_ok)
    ok = ok and res_ok

    print("[PASS] lab_token_budget self-test passed." if ok
          else "[FAIL] lab_token_budget self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Token budget lab (offline, deterministic).")
    ap.add_argument("--system", type=int, default=500, help="system prompt tokens")
    ap.add_argument("--instructions", type=int, default=400, help="task instruction tokens")
    ap.add_argument("--examples", type=int, default=3, help="number of few-shot examples")
    ap.add_argument("--retrieved", type=int, default=24000, help="retrieved context tokens")
    ap.add_argument("--history", type=int, default=30000, help="conversation history tokens")
    ap.add_argument("--window", type=int, default=128000, help="context window tokens")
    ap.add_argument("--reserve", type=int, default=4096, help="tokens reserved for output")
    ap.add_argument("--sweep", action="store_true", help="sweep the conversation history")
    ap.add_argument("--self-test", action="store_true", help="assert the budget properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.window, args.system, args.instructions, args.examples,
                    args.retrieved, args.reserve)
        return 0
    print_report(args.window, args.system, args.instructions, args.examples,
                 args.retrieved, args.history, args.reserve)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

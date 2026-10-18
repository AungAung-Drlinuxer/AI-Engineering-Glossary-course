#!/usr/bin/env python3
"""lab_prefix_cache - what a shared prompt prefix saves when many calls reuse it.

Offline, deterministic, standard library only.

Model (shown, the only source of the numbers below)

    prefill_without = calls * (prefix_tokens + suffix_tokens)
    prefill_with    = prefix_tokens + calls * suffix_tokens
    saved           = prefill_without - prefill_with
    saved_percent   = saved / prefill_without * 100
    ttft_ms         = overhead_ms + prefill_tokens / prefill_rate * 1000
    kv_mib(prefix)  = 2 * layers * prefix_tokens * heads * head_dim * bytes / MiB

Stated assumptions

    prefill rate   = 8000 tokens/s
    overhead       = 40 ms of queueing and network, cache-independent
    input price    = USD 3.00 per 1e6 prefill tokens
    reference model: layers 32, heads 32, head_dim 128, fp16 -> 0.500 MiB per token
    cache eligibility, lifetime and minimum block are provider-specific, so a
    miss is a normal outcome and not an error
"""

from __future__ import annotations

import argparse

PREFILL_RATE = 8000.0
OVERHEAD_MS = 40.0
IN_PRICE = 3.00
MIB = 1024.0 * 1024.0
LAYERS = 32
HEADS = 32
HEAD_DIM = 128
BYTES_PER_ELEMENT = 2.0
KV_PER_TOKEN = 2 * LAYERS * HEADS * HEAD_DIM * BYTES_PER_ELEMENT
RULE = "=" * 74
THIN = "-" * 74


def prefill(prefix: int, calls: int, suffix: int) -> tuple[int, int]:
    without = calls * (prefix + suffix)
    with_cache = prefix + calls * suffix
    return without, with_cache


def ttft_ms(tokens: int) -> float:
    return OVERHEAD_MS + tokens / PREFILL_RATE * 1000.0


def print_report(prefix: int, calls: int, rate: float, suffix: int) -> None:
    without, with_cache = prefill(prefix, calls, suffix)
    saved = without - with_cache
    percent = saved / without * 100.0 if without else 0.0
    print(RULE)
    print("lab_prefix_cache - prefix caching: prefill tokens, TTFT and cost (offline, deterministic)")
    print("prefix=%s tokens  calls=%d  suffix=%d tokens/call  prefill-rate=%s tok/s  overhead=%.0f ms"
          % (f"{prefix:,}", calls, suffix, f"{rate:,.0f}", OVERHEAD_MS))
    print(THIN)
    print("prefill tokens without cache    : %14s" % f"{without:,}")
    print("prefill tokens with prefix cache: %14s" % f"{with_cache:,}")
    print("prefill tokens saved            : %14s  (%.2f%%)" % (f"{saved:,}", percent))
    print("saving per added call (calls>1)  : %14s" % f"{(calls - 1) * prefix // max(1, calls):,}")
    print(THIN)
    t_without = ttft_ms(without)
    t_with = ttft_ms(with_cache)
    print("TTFT at %s tokens/s prefill:" % f"{rate:,.0f}")
    print("  without cache   : %12.1f ms" % t_without)
    print("  with cache      : %12.1f ms" % t_with)
    print("  saved           : %12.1f ms" % (t_without - t_with))
    print(THIN)
    print("cost at USD %.2f per 1e6 prefill tokens (assumption):" % IN_PRICE)
    print("  without cache   : USD %12.6f" % (without * IN_PRICE / 1e6))
    print("  with cache      : USD %12.6f" % (with_cache * IN_PRICE / 1e6))
    print("  saved           : USD %12.6f" % (saved * IN_PRICE / 1e6))
    print(THIN)
    kv = prefix * KV_PER_TOKEN / MIB
    print("shared prefix KV stored once    : %14s MiB  (%.4f GiB, reference model %.3f MiB/token)"
          % (f"{kv:,.2f}", kv / 1024.0, KV_PER_TOKEN / MIB))
    print("without sharing, %d copies would take %.2f GiB" % (calls, kv * calls / 1024.0))
    print("မှတ်ချက် - prefix cache သည် တည်ငြိမ်သည့် prefix အတွက်သာ သက်ရောက်သည်၊ "
          "cache မမိသည့် အခြေအနေကို ပုံမှန် အဖြစ် သဘောထားရမည်။")
    print(RULE)


def print_sweep(prefix: int, rate: float, suffix: int) -> None:
    print(RULE)
    print("lab_prefix_cache - sweep: calls 1 -> 128")
    print("prefix=%s tokens  suffix=%d tokens/call  prefill-rate=%s tok/s"
          % (f"{prefix:,}", suffix, f"{rate:,.0f}"))
    print(THIN)
    print("%8s %16s %16s %12s" % ("calls", "prefill without", "prefill with", "saved %"))
    calls = 1
    while calls <= 128:
        without, with_cache = prefill(prefix, calls, suffix)
        saved = without - with_cache
        print("%8d %16s %16s %11.2f%%"
              % (calls, f"{without:,}", f"{with_cache:,}", saved / without * 100.0))
        calls *= 2
    print(THIN)
    print("trend: the saved fraction rises with the number of calls that share the prefix")
    print(RULE)


def self_test() -> int:
    ok = True

    without, with_cache = prefill(3000, 100, 200)
    saved = without - with_cache
    formula_ok = (without == 100 * (3000 + 200) and with_cache == 3000 + 100 * 200
                  and saved == (100 - 1) * 3000 and with_cache + saved == without)
    print("[OK] the cache saves (calls-1)*prefix tokens (%s) and reconciles: %s"
          % (f"{saved:,}", formula_ok))
    ok = ok and formula_ok

    one_without, one_with = prefill(3000, 1, 200)
    one_ok = one_without == one_with
    print("[OK] with a single call the cache saves nothing (%s == %s): %s"
          % (f"{one_without:,}", f"{one_with:,}", one_ok))
    ok = ok and one_ok

    saved_pct = saved / without * 100.0
    pct_ok = 0.0 < saved_pct < 100.0
    print("[OK] the saved fraction is strictly between 0 and 100 percent (%.2f%%): %s"
          % (saved_pct, pct_ok))
    ok = ok and pct_ok

    small = prefill(3000, 10, 200)
    big = prefill(3000, 20, 200)
    mono_ok = ((big[0] - big[1]) > (small[0] - small[1]))
    print("[OK] doubling the calls increases the tokens saved (%s -> %s): %s"
          % (f"{small[0] - small[1]:,}", f"{big[0] - big[1]:,}", mono_ok))
    ok = ok and mono_ok

    ttft_ok = ttft_ms(without) > ttft_ms(with_cache) > 0
    print("[OK] cached prefill gives the lower TTFT (%.1f ms vs %.1f ms): %s"
          % (ttft_ms(with_cache), ttft_ms(without), ttft_ok))
    ok = ok and ttft_ok

    print("[PASS] lab_prefix_cache self-test passed." if ok
          else "[FAIL] lab_prefix_cache self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Prefix caching lab (offline, deterministic).")
    ap.add_argument("--prefix-tokens", type=int, default=3000, help="shared prefix tokens")
    ap.add_argument("--calls", type=int, default=100, help="number of calls sharing the prefix")
    ap.add_argument("--prefill-rate", type=float, default=PREFILL_RATE, help="prefill tokens/s")
    ap.add_argument("--suffix-tokens", type=int, default=200, help="request-specific tokens per call")
    ap.add_argument("--sweep", action="store_true", help="sweep the number of calls")
    ap.add_argument("--self-test", action="store_true", help="assert the caching properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.prefix_tokens, args.prefill_rate, args.suffix_tokens)
        return 0
    print_report(args.prefix_tokens, args.calls, args.prefill_rate, args.suffix_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

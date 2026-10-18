#!/usr/bin/env python3
"""Worked example (c): how prompt length moves TTFT at a stated prefill rate,
with and without cache hits.

Model (shown, and the only source of the numbers below):

    ttft_ms(prompt_tokens, cached_tokens)
        = overhead_ms + (prompt_tokens - cached_tokens) / prefill_rate * 1000

TTFT is the time from submitting a generation call to the first output token
reaching the client. It is a start-up latency, not a throughput.

Assumptions (stated; queueing, batching, network and vendor behaviour all move
these numbers in practice):

    prefill rate    = 8000 tokens/s (the rate at which prompt tokens are read)
    overhead        = 40 ms of queueing, scheduling and network, cache-independent
    cache hits      = 0, 3000 and 8000 tokens of an eligible shared prefix
    output is not modelled here; TTFT does not include generation time

Standard library only; deterministic.
"""

from __future__ import annotations

PREFILL_RATE = 8000.0     # tokens/s (assumption)
OVERHEAD_MS = 40.0        # ms, cache-independent (assumption)
CACHE_CASES = (0, 3000, 8000)


def ttft_ms(prompt_tokens: int, cached_tokens: int) -> float:
    uncached = max(0, prompt_tokens - cached_tokens)
    return OVERHEAD_MS + uncached / PREFILL_RATE * 1000.0


def main() -> int:
    print("model: ttft_ms = %.0f + (prompt_tokens - cached_tokens) / %.0f * 1000"
          % (OVERHEAD_MS, PREFILL_RATE))
    print("assumption: prefill rate %.0f tokens/s, overhead %.0f ms" % (PREFILL_RATE, OVERHEAD_MS))
    print()
    head = "%-10s" % "prompt"
    for c in CACHE_CASES:
        head += " %16s" % ("ttft cache=%d" % c)
    head += " %16s" % "saving 3000 vs 0"
    print(head)
    for prompt in (500, 1000, 2000, 4000, 8000, 16000, 32000):
        row = "%-10d" % prompt
        for c in CACHE_CASES:
            row += " %13.1f ms" % ttft_ms(prompt, c)
        no_cache = ttft_ms(prompt, 0)
        hit = ttft_ms(prompt, 3000)
        row += " %13.1f %%" % ((no_cache - hit) / no_cache * 100.0)
        print(row)
    print()
    print("a 3000-token cache hit removes %.1f ms of prefill at every prompt length"
          % (3000 / PREFILL_RATE * 1000.0))
    print("a full 8000-token cache hit removes %.1f ms of prefill at every prompt length"
          % (8000 / PREFILL_RATE * 1000.0))
    print("doubling the prompt doubles the uncached prefill term and leaves the %.0f ms "
          "overhead untouched" % OVERHEAD_MS)
    print("prefill latency = (prompt_tokens - cached_tokens) / prefill_rate, linear in "
          "prompt length and linear in cache hits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

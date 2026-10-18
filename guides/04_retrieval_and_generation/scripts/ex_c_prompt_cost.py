#!/usr/bin/env python3
"""Worked example (c): prompt tokens and cost added per retrieved chunk.

Assumptions (repeated in the guide):
  chunk size      = 400 tokens per retrieved chunk
  system prompt   = 400 tokens, question = 60 tokens
  retrieved tokens = chunk * k
  input price     = 2.00 USD per million input tokens
  answer          = 300 output tokens at 8.00 USD per million output tokens
  cost per query  = prompt_tokens / 1e6 * input_price
Standard library only, pure arithmetic.
"""

CHUNK = 400
SYSTEM = 400
QUESTION = 60
OUTPUT_TOKENS = 300
IN_PRICE = 2.00
OUT_PRICE = 8.00
KS = (2, 5, 10)
CHUNK_SIZES = (200, 400, 800)

out_cost_1k = OUTPUT_TOKENS / 1e6 * OUT_PRICE * 1000.0

print("assumptions: chunk=%d tokens, system=%d, question=%d, answer=%d tokens"
      % (CHUNK, SYSTEM, QUESTION, OUTPUT_TOKENS))
print("prices: input %.2f USD per 1M tokens, output %.2f USD per 1M tokens (assumption)"
      % (IN_PRICE, OUT_PRICE))
print()
print("%3s %11s %11s %13s %14s %16s"
      % ("k", "retrieved", "prompt tok", "USD/1k input", "USD/1k total", "added USD/1k"))
for k in KS:
    retrieved = CHUNK * k
    prompt = SYSTEM + retrieved + QUESTION
    in_1k = prompt / 1e6 * IN_PRICE * 1000.0
    print("%3d %11d %11d %13.4f %14.4f %16.4f"
          % (k, retrieved, prompt, in_1k, in_1k + out_cost_1k,
             (prompt - (SYSTEM + QUESTION)) / 1e6 * IN_PRICE * 1000.0))
print()
base = SYSTEM + CHUNK * KS[0] + QUESTION
print("cost of one retrieved chunk of %d tokens = %.8f USD per query = %.4f USD per 1000 queries"
      % (CHUNK, CHUNK / 1e6 * IN_PRICE, CHUNK / 1e6 * IN_PRICE * 1000.0))
print("retrieved context as a share of the prompt at k=%d: %.1f%%"
      % (KS[1], CHUNK * KS[1] / (SYSTEM + CHUNK * KS[1] + QUESTION) * 100.0))
print("prompt growth k=%d -> k=%d: %d -> %d tokens (%.2fx)"
      % (KS[0], KS[-1], base, SYSTEM + CHUNK * KS[-1] + QUESTION,
         (SYSTEM + CHUNK * KS[-1] + QUESTION) / base))
print()
print("chunk size effect at k=%d:" % KS[1])
print("%7s %11s %11s %15s" % ("chunk", "retrieved", "prompt tok", "USD/1k input"))
for size in CHUNK_SIZES:
    prompt = SYSTEM + size * KS[1] + QUESTION
    print("%7d %11d %11d %15.4f"
          % (size, size * KS[1], prompt, prompt / 1e6 * IN_PRICE * 1000.0))

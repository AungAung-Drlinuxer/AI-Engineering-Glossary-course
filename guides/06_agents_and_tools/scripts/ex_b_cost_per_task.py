#!/usr/bin/env python3
"""Worked example (b): cost per task with and without prefix caching.

Assumptions (repeated in the guide, all labelled as assumptions):
  task length: 10 model steps
  prefix sent at every step and identical every time:
      4000 tokens of system prompt plus tool schemas
  each step appends 300 tokens to the conversation (assistant reply + tool result)
  each step produces 120 output tokens
  input price 3.00 USD per million tokens, output price 15.00 USD per million tokens
      (output = 5x input)
  with prefix caching the shared prefix is billed 1.25x on the first write and
      0.25x on every later read; the rest of the prompt is billed at full price
No library, no model call, no network: pure arithmetic.
"""
STEPS = 10
PREFIX = 4000
STEP_ADD = 300
OUTPUT = 120
IN_PRICE = 3.00
OUT_PRICE = 15.00
CACHE_WRITE = 1.25
CACHE_READ = 0.25

print("task: %d steps, shared prefix %d tokens, +%d tokens per step, %d output tokens per step"
      % (STEPS, PREFIX, STEP_ADD, OUTPUT))
print("assumed price: input %.2f USD/Mtok, output %.2f USD/Mtok, "
      "cache write %.2fx, cache read %.2fx" % (IN_PRICE, OUT_PRICE, CACHE_WRITE, CACHE_READ))
print()
head = "%-5s %10s %14s %14s %12s %12s" % ("step", "prompt", "plain step USD",
                                          "cached step USD", "plain cum", "cached cum")
print(head)
print("-" * len(head))
plain_cum = 0.0
cached_cum = 0.0
for step in range(1, STEPS + 1):
    prompt = PREFIX + STEP_ADD * (step - 1)
    rest = prompt - PREFIX
    plain = (prompt * IN_PRICE + OUTPUT * OUT_PRICE) / 1e6
    write = CACHE_WRITE if step == 1 else CACHE_READ
    cached = (PREFIX * write * IN_PRICE + rest * IN_PRICE + OUTPUT * OUT_PRICE) / 1e6
    plain_cum += plain
    cached_cum += cached
    print("%-5d %10d %14.6f %14.6f %12.6f %12.6f"
          % (step, prompt, plain, cached, plain_cum, cached_cum))
print()
last_prompt = PREFIX + STEP_ADD * (STEPS - 1)
print("final step prompt %d tokens (%d prefix + %d accumulated)" % (last_prompt, PREFIX, last_prompt - PREFIX))
prompt_billed_plain = STEPS * PREFIX + STEP_ADD * (STEPS * (STEPS - 1) // 2)
prompt_billed_cached = (PREFIX * (CACHE_WRITE + CACHE_READ * (STEPS - 1))
                        + STEP_ADD * (STEPS * (STEPS - 1) // 2))
print("prompt tokens billed over the task: plain %d, cached-equivalent %.1f (-%.2f%%)"
      % (prompt_billed_plain, prompt_billed_cached,
         100.0 * (prompt_billed_plain - prompt_billed_cached) / prompt_billed_plain))
print("cost per task: plain USD %.6f, cached USD %.6f, saved USD %.6f (%.2f%%)"
      % (plain_cum, cached_cum, plain_cum - cached_cum,
         100.0 * (plain_cum - cached_cum) / plain_cum))
print("if the prefix grows to %d tokens the saving per task becomes USD %.6f"
      % (PREFIX * 2,
         PREFIX * 2 * ((1.0 - CACHE_WRITE) + (1.0 - CACHE_READ) * (STEPS - 1)) * IN_PRICE / 1e6))

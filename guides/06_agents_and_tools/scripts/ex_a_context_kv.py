#!/usr/bin/env python3
"""Worked example (a): agent context and KV-cache growth across turns.

Assumptions (repeated in the guide):
  reference model: layers 32, heads 32, head_dim 128, fp16 (2 bytes per element)
  KV bytes per token = 2 * layers * heads * head_dim * bytes = 524288 B = 0.500 MiB
  every turn sends the whole conversation, so prompt tokens = context tokens
  turn budget: 12 turns
  fixed prompt: system 800 tokens + task 200 tokens = 1000 tokens
  each turn appends an assistant message of 120 reasoning + 40 tool-call tokens
  a tool call also appends a tool result of 900 tokens
  summarisation replaces every earlier tool result with a 180-token digest,
  the result of the current turn stays raw
No library, no model call, no network: pure arithmetic.
"""
MIB = 1024.0 ** 2
GIB = 1024.0 ** 3
L, H, DH, BYTES = 32, 32, 128, 2
TURNS = 12
BASE = 1000
ASSISTANT = 120
TOOL_CALL = 40
RESULT = 900
DIGEST = 180

per_token = 2 * L * H * DH * BYTES
print("reference model: layers=%d heads=%d head_dim=%d fp16=2 B -> %d B/token = %.3f MiB/token"
      % (L, H, DH, per_token, per_token / MIB))
print("turns=%d  base prompt=%d  assistant=%d  tool call=%d  tool result=%d  digest=%d"
      % (TURNS, BASE, ASSISTANT, TOOL_CALL, RESULT, DIGEST))
print()
head = "%-6s %12s %12s %12s %12s %8s" % ("turn", "raw tokens", "summ tokens",
                                          "raw KV MiB", "summ KV MiB", "ratio")
print(head)
print("-" * len(head))
for t in range(1, TURNS + 1):
    raw = BASE + t * (ASSISTANT + TOOL_CALL + RESULT)
    summ = BASE + t * (ASSISTANT + TOOL_CALL) + RESULT + (t - 1) * DIGEST
    print("%-6d %12d %12d %12.1f %12.1f %8.3f"
          % (t, raw, summ, raw * per_token / MIB, summ * per_token / MIB, raw / summ))
print()
raw_last = BASE + TURNS * (ASSISTANT + TOOL_CALL + RESULT)
summ_last = BASE + TURNS * (ASSISTANT + TOOL_CALL) + RESULT + (TURNS - 1) * DIGEST
print("final turn %d: raw %d tokens = %.3f GiB KV | summarised %d tokens = %.3f GiB KV"
      % (TURNS, raw_last, raw_last * per_token / GIB, summ_last, summ_last * per_token / GIB))
print("KV saved at turn %d: %.1f MiB (%.3f GiB), ratio raw/summarised = %.3f"
      % (TURNS, (raw_last - summ_last) * per_token / MIB,
         (raw_last - summ_last) * per_token / GIB, raw_last / summ_last))
print("growth per turn: raw +%d tokens (+%.1f MiB), summarised +%d tokens (+%.1f MiB)"
      % (ASSISTANT + TOOL_CALL + RESULT, (ASSISTANT + TOOL_CALL + RESULT) * per_token / MIB,
         ASSISTANT + TOOL_CALL + DIGEST, (ASSISTANT + TOOL_CALL + DIGEST) * per_token / MIB))
print("summarisation work assumed: %d calls x (%d read + %d write) = %d extra tokens"
      % (TURNS - 1, RESULT, DIGEST, (TURNS - 1) * (RESULT + DIGEST)))

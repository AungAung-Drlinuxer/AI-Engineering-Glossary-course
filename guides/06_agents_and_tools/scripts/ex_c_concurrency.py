#!/usr/bin/env python3
"""Worked example (c): concurrency and GPU memory for parallel agent sessions.

Assumptions (repeated in the guide):
  one accelerator with 80 GB of memory, 16 GiB reserved for runtime and fragmentation
  serving weights 14.0 GiB (a 7B model in fp16)
  KV cache 0.5 MiB per token (layers 32, heads 32, head_dim 128, fp16)
  per-session runtime overhead 0.25 GiB (activations, sampler buffers, transport state)
  one agent step takes 1.2 s of wall clock
  a task is 10 agent steps
A session holds its whole context for the duration of the task, so concurrency is
limited by KV cache, not by compute. No library, no GPU, no network: pure arithmetic.
"""
MIB_IN_GIB = 1024.0
GPU_GB = 80
RESERVED_GIB = 16.0
WEIGHT_GIB = 14.0
KV_MIB_PER_TOKEN = 0.5
SESSION_OVERHEAD_GIB = 0.25
CONTEXTS = (4096, 8192, 32768)
SESSIONS = (1, 8, 32, 64)
STEP_S = 1.2
TASK_STEPS = 10

usable = GPU_GB - RESERVED_GIB - WEIGHT_GIB
print("gpu %d GB, reserved %.1f GiB, weights %.1f GiB -> usable %.1f GiB"
      % (GPU_GB, RESERVED_GIB, WEIGHT_GIB, usable))
print("KV %.2f MiB/token, per-session overhead %.2f GiB, step %.1f s, task %d steps"
      % (KV_MIB_PER_TOKEN, SESSION_OVERHEAD_GIB, STEP_S, TASK_STEPS))


def per_session_gib(context: int) -> float:
    return SESSION_OVERHEAD_GIB + context * KV_MIB_PER_TOKEN / MIB_IN_GIB


print()
head = "%-8s %8s %12s %14s %8s %8s" % ("context", "sessions", "per-session",
                                       "requested GiB", "fit", "queue")
print(head)
print("-" * len(head))
for ctx in CONTEXTS:
    per = per_session_gib(ctx)
    fits = int(usable // per)
    for n in SESSIONS:
        total = per * n
        print("%-8d %8d %12.3f %14.2f %8d %8d"
              % (ctx, n, per, total, min(n, fits), max(0, n - fits)))
print()
head2 = "%-8s %10s %8s %8s %11s %11s" % ("context", "requested", "served", "queue",
                                         "steps/min", "tasks/min")
print(head2)
print("-" * len(head2))
for ctx in CONTEXTS:
    per = per_session_gib(ctx)
    fits = int(usable // per)
    for n in (8, 32, 64):
        served = min(n, fits)
        steps_per_min = served * 60.0 / STEP_S
        print("%-8d %10d %8d %8d %11.2f %11.2f"
              % (ctx, n, served, n - served, steps_per_min, steps_per_min / TASK_STEPS))
print()
ctx = 32768
per = per_session_gib(ctx)
fits = int(usable // per)
print("case %d-token sessions: per-session %.3f GiB -> %d sessions fit, %d of 64 wait"
      % (ctx, per, fits, 64 - fits))
print("throughput at %.1f s/step: %.2f steps/min = %.2f tasks/min (a %d-step task)"
      % (STEP_S, fits * 60.0 / STEP_S, fits * 60.0 / STEP_S / TASK_STEPS, TASK_STEPS))
print("halving the context to %d tokens: per-session %.3f GiB -> %d sessions fit (%.2fx)"
      % (ctx // 2, per_session_gib(ctx // 2), int(usable // per_session_gib(ctx // 2)),
         (usable // per_session_gib(ctx // 2)) / fits))
print("memory per session at %d tokens is %.0f%% KV cache and %.0f%% overhead"
      % (ctx, 100.0 * (per - SESSION_OVERHEAD_GIB) / per, 100.0 * SESSION_OVERHEAD_GIB / per))

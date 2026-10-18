#!/usr/bin/env python3
"""Worked example (b): retrieval latency and queries per second against the generation step.

Assumptions (repeated in the guide):
  index      = 250000 vectors, dim 768
  distance   = 2 * dim FLOPs; scalar distance throughput 12.0 GFLOP/s per worker
  embedding  = 5.0 ms for one query (one encoder forward)
  ANN search = (96 + 8*k) candidates visited, 0.60 ms traversal overhead
  exact scan = 250000 candidates visited, no traversal overhead
  metadata filter and dedup = 0.20 ms
  server     = 4 concurrent workers, 0.90 USD per server hour
  generation = 420 ms to first token, 220 output tokens at 11 ms each
Every rate is an assumption, not a measurement.
"""

N = 250_000
DIM = 768
DIST_GFLOPS = 12.0
EMBED_MS = 5.0
GRAPH_MS = 0.60
META_MS = 0.20
WORKERS = 4
PRICE_PER_HOUR = 0.90
TTFT_MS = 420.0
OUT_TOKENS = 220
ITL_MS = 11.0
KS = (2, 5, 10)


def distance_ms(visited):
    return visited * 2 * DIM / (DIST_GFLOPS * 1e9) * 1000.0


def exact_ms():
    return EMBED_MS + META_MS + distance_ms(N)


def ann_ms(k):
    return EMBED_MS + META_MS + GRAPH_MS + distance_ms(96 + 8 * k)


def qps(lat):
    return WORKERS * 1000.0 / lat


def usd_per_1000(lat):
    return (lat / WORKERS) / 3600.0 * PRICE_PER_HOUR


gen_ms = TTFT_MS + OUT_TOKENS * ITL_MS
ex = exact_ms()

print("index: %d vectors, dim=%d ; candidates visited by ANN = 96 + 8*k (assumption)"
      % (N, DIM))
print("generation step it feeds: %.0f ms to first token + %d output tokens x %.0f ms = %.0f ms"
      % (TTFT_MS, OUT_TOKENS, ITL_MS, gen_ms))
print()
print("%3s %10s %9s %10s %13s %19s"
      % ("k", "ANN ms", "ANN QPS", "share %", "ANN USD/1k q", "ANN USD/1M q"))
for k in KS:
    lat = ann_ms(k)
    print("%3d %10.4f %9.1f %10.2f %13.6f %19.2f"
          % (k, lat, qps(lat), lat / (lat + gen_ms) * 100.0,
             usd_per_1000(lat), usd_per_1000(lat) * 1000))
print()
print("exact scan for reference: %.4f ms, %.1f QPS, %.2f%% of end to end, %.6f USD/1k queries"
      % (ex, qps(ex), ex / (ex + gen_ms) * 100.0, usd_per_1000(ex)))
print()
print("embedding share of the ANN query: %.1f ms of %.4f ms = %.1f%%"
      % (EMBED_MS, ann_ms(10), EMBED_MS / ann_ms(10) * 100.0))
print("candidates visited: k=10 -> %d of %d = %.3f%% of the collection"
      % (96 + 8 * 10, N, (96 + 8 * 10) / N * 100.0))
print("workers needed for 50 ANN queries/s at k=10: %.1f"
      % (50.0 / (1000.0 / ann_ms(10))))

#!/usr/bin/env python3
"""lab_vector_index - index memory, recall@k and the work of a coarse-to-fine layered search.

Offline, deterministic, standard library only. Every number is computed from the model
below, so the output reproduces byte for byte.

Model (assumptions):
  toy embedding set : the generator plants `groups` group centres (seeded uniform(-1, 1))
                      and places every vector at its centre plus seeded uniform noise.
                      Real embedding spaces show the same clustered shape.
  index memory      : chunks * dim * bytes_per_element (fp32 4, fp16 2, int8 1)
  exact search      : squared Euclidean distance against every stored vector,
                      top k by (distance, index)
  layered search    : a coarse-to-fine approximation of the idea behind HNSW, made
                      measurable offline
                        coarse layer : one centroid per group, from the mean of its members
                        fine layer   : every member of the `probe` centroids nearest the
                                       query, top k among them
                      Because the candidate set grows with the probe, recall@k is
                      monotone in `probe`, and probing every centroid reproduces the
                      exact ranking.
  latency model     : distance computations are the deterministic proxy,
                      latency_ms = distances * 2 * dim / distance_gflops / 1e9 * 1000
                      with distance_gflops = 12.0 per worker (assumption)
  recall@k          : |layered top k intersect exact top k| / k

Flags:
  --chunks  stored vectors      --k        neighbours requested
  --dim     dimensions          --queries  evaluation queries
  --dtype   memory precision    --seed     deterministic seed
  --probe   centroids visited   --sweep    chunks sweep
  --self-test
"""

from __future__ import annotations

import argparse
import random

DTYPE_BYTES = {"fp32": 4.0, "fp16": 2.0, "int8": 1.0}
DTYPE_ORDER = ["fp32", "fp16", "int8"]
GROUP_SIZE = 16
NOISE = 1.1
DISTANCE_GFLOPS = 12.0
MIB = 1024.0 * 1024.0
RULE = "=" * 74
THIN = "-" * 74
SWEEP_CHUNKS = [1024, 2048, 4096, 8192]
SWEEP_QUERIES = 8


def memory_bytes(chunks: int, dim: int, dtype: str) -> float:
    return chunks * dim * DTYPE_BYTES[dtype]


def latency_ms(distances: int, dim: int) -> float:
    return distances * 2 * dim / (DISTANCE_GFLOPS * 1e9) * 1000.0


def sq_dist(a: list[float], b: list[float]) -> float:
    total = 0.0
    for x, y in zip(a, b):
        d = x - y
        total += d * d
    return total


def build(n: int, dim: int, seed: int, group_size: int, noise: float):
    """Toy vectors with planted group structure, the groups, and their centroids."""
    rng = random.Random(seed)
    groups = max(1, (n + group_size - 1) // group_size)
    centres = [[rng.uniform(-1.0, 1.0) for _ in range(dim)] for _ in range(groups)]
    vecs = []
    members = [[] for _ in range(groups)]
    for i in range(n):
        g = i % groups
        c = centres[g]
        vecs.append([c[j] + rng.uniform(-noise, noise) for j in range(dim)])
        members[g].append(i)
    centroids = []
    for mem in members:
        cent = [0.0] * dim
        for i in mem:
            vi = vecs[i]
            for j in range(dim):
                cent[j] += vi[j]
        centroids.append([x / len(mem) for x in cent])
    return vecs, centres, members, centroids


def make_query(rng: random.Random, centres, dim: int, noise: float) -> list[float]:
    c = centres[rng.randrange(len(centres))]
    return [c[j] + rng.uniform(-noise, noise) for j in range(dim)]


def exact_topk(query: list[float], vecs: list[list[float]], k: int):
    scored = sorted((sq_dist(query, v), i) for i, v in enumerate(vecs))
    return scored[:k], len(vecs)


def layered_topk(query: list[float], vecs, members, centroids, k: int, probe: int):
    coarse = sorted((sq_dist(query, c), ci) for ci, c in enumerate(centroids))
    visited = len(centroids)
    cands = []
    for _, ci in coarse[:probe]:
        for i in members[ci]:
            cands.append((sq_dist(query, vecs[i]), i))
            visited += 1
    cands.sort()
    return cands[:k], visited


def evaluate(n: int, dim: int, k: int, queries: int, seed: int, probe: int):
    vecs, centres, members, centroids = build(n, dim, seed, GROUP_SIZE, NOISE)
    rng = random.Random(seed + 91)
    recalls, exact_work, layered_work = [], 0, 0
    for _ in range(queries):
        q = make_query(rng, centres, dim, NOISE)
        ex, work_ex = exact_topk(q, vecs, k)
        ap, work_ap = layered_topk(q, vecs, members, centroids, k, probe)
        recalls.append(len({i for _, i in ex} & {i for _, i in ap}) / k)
        exact_work += work_ex
        layered_work += work_ap
    return {
        "mean": sum(recalls) / len(recalls),
        "worst": min(recalls),
        "best": max(recalls),
        "exact_work": exact_work // queries,
        "layered_work": layered_work // queries,
        "groups": len(centroids),
    }


def print_report(n: int, dim: int, dtype: str, k: int, queries: int, seed: int, probe: int) -> None:
    print(RULE)
    print("lab_vector_index - index memory, recall@k, layered-search work (offline, deterministic)")
    print(f"chunks={n}  dim={dim}  dtype={dtype}  k={k}  queries={queries}  seed={seed}  "
          f"group={GROUP_SIZE}  noise={NOISE}  probe={probe}")
    print(THIN)
    print(f"index memory (chunks={n:,}, dim={dim}):")
    print("  dtype    bytes/vector      bytes         MiB")
    for name in DTYPE_ORDER:
        b = memory_bytes(n, dim, name)
        print(f"  {name:<7}{b / n:>15,.0f}{b:>11,.0f}{b / MIB:>12.4f}")
    print(THIN)
    res = evaluate(n, dim, k, queries, seed, probe)
    print(f"exact scan vs layered search (per query, k={k}, probe={probe} of {res['groups']} groups):")
    print(f"  distance computations exact    : {res['exact_work']:>12,}")
    print(f"  distance computations layered  : {res['layered_work']:>12,}"
          f"   ({res['layered_work'] / res['exact_work'] * 100.0:.2f}% of the collection)")
    print(f"  work ratio exact / layered     : {res['exact_work'] / res['layered_work']:>12,.2f}x")
    print(f"  modelled latency exact         : {latency_ms(res['exact_work'], dim):>12.4f} ms")
    print(f"  modelled latency layered       : {latency_ms(res['layered_work'], dim):>12.4f} ms")
    print(f"  latency ratio                  : "
          f"{latency_ms(res['exact_work'], dim) / latency_ms(res['layered_work'], dim):>12,.2f}x")
    print(f"  mean recall@{k}                 : {res['mean']:>12.4f}")
    print(f"  worst / best query recall@{k}   : {res['worst']:>12.4f} / {res['best']:.4f}")
    print(THIN)
    print("မှတ်ချက် - index memory သည် chunk အရေအတွက်၊ dimension နှင့် byte အကျယ်အပေါ် "
          "တိုက်ရိုက် အချိုးကျသည်။")
    print("layered search သည် distance တွက်ချက်မှုကို လျှော့ချ၍ latency ကျဆင်းစေသော်လည်း "
          "recall@k သည် 1 အောက်တွင် ရှိနေသည်။")
    print(RULE)


def print_sweep(dim: int, dtype: str, k: int, seed: int, probe: int) -> None:
    print(RULE)
    print(f"lab_vector_index - chunks sweep 1024..8192 (dim={dim}, dtype={dtype}, k={k}, "
          f"probe={probe}, queries={SWEEP_QUERIES})")
    print(THIN)
    print("    chunks      index MiB   exact dist   layered dist    ratio   mean recall@k")
    for n in SWEEP_CHUNKS:
        res = evaluate(n, dim, k, SWEEP_QUERIES, seed, probe)
        print(f" {n:>9,} {memory_bytes(n, dim, dtype) / MIB:>14,.4f} "
              f"{res['exact_work']:>12,} {res['layered_work']:>14,} "
              f"{res['exact_work'] / res['layered_work']:>8,.2f}x {res['mean']:>15.4f}")
    print(THIN)
    print("မှတ်ချက် - chunks တိုးလျှင် index memory linear တိုးသည်၊ probe တူညီစွာ ထားလျှင် "
          "work ချွေတာမှု တိုးသော်လည်း recall@k ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    a = memory_bytes(1000, 64, "fp32")
    b = memory_bytes(1000, 64, "fp16")
    c = memory_bytes(1000, 64, "int8")
    dtype_ok = a == 2.0 * b and a == 4.0 * c
    print(f"[OK] fp32 is twice fp16 and four times int8 ({a:,.0f} / {b:,.0f} / {c:,.0f} B): "
          f"{dtype_ok}")
    ok = ok and dtype_ok

    lin = (memory_bytes(2000, 64, "fp16") == 2.0 * memory_bytes(1000, 64, "fp16")
           and memory_bytes(1000, 128, "fp16") == 2.0 * memory_bytes(1000, 64, "fp16"))
    print(f"[OK] index memory is linear in chunks and in dimension: {lin}")
    ok = ok and lin

    n, dim, k = 512, 16, 5
    vecs, centres, members, centroids = build(n, dim, 3, GROUP_SIZE, NOISE)
    rng = random.Random(42)
    q = make_query(rng, centres, dim, NOISE)
    ex, ex_work = exact_topk(q, vecs, k)
    ordered = len(ex) == k and all(ex[i][0] <= ex[i + 1][0] for i in range(k - 1))
    print(f"[OK] the exact ranking is ordered by distance and holds k={k} items: {ordered}")
    ok = ok and ordered

    ap, ap_work = layered_topk(q, vecs, members, centroids, k, 1)
    cheap = ap_work < ex_work
    print(f"[OK] the layered search reads fewer vectors ({ap_work:,} < {ex_work:,}): {cheap}")
    ok = ok and cheap

    overlap = len({i for _, i in ex} & {i for _, i in ap})
    bounded = 0.0 <= overlap / k <= 1.0
    print(f"[OK] recall@{k} is a fraction in [0, 1] ({overlap}/{k}): {bounded}")
    ok = ok and bounded

    full, full_work = layered_topk(q, vecs, members, centroids, k, len(centroids))
    hit_full = len({i for _, i in ex} & {i for _, i in full})
    same = [i for _, i in full] == [i for _, i in ex] and hit_full == k
    print(f"[OK] probing every group reproduces the exact top k ({hit_full}/{k}): {same}")
    ok = ok and same

    r1 = len({i for _, i in ex} & {i for _, i in layered_topk(q, vecs, members, centroids, k, 1)[0]})
    r8 = len({i for _, i in ex} & {i for _, i in layered_topk(q, vecs, members, centroids, k, 8)[0]})
    mono = r1 <= r8
    print(f"[OK] recall@k does not fall when the probe grows ({r1}/{k} <= {r8}/{k}): {mono}")
    ok = ok and mono

    print("[PASS] lab_vector_index self-test passed." if ok
          else "[FAIL] lab_vector_index self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Vector index memory, recall@k and layered-search work (offline, deterministic).")
    ap.add_argument("--chunks", type=int, default=4096, help="number of stored vectors")
    ap.add_argument("--dim", type=int, default=64, help="embedding dimensions")
    ap.add_argument("--dtype", choices=DTYPE_ORDER, default="fp16", help="memory precision")
    ap.add_argument("--k", type=int, default=10, help="neighbours requested")
    ap.add_argument("--queries", type=int, default=32, help="evaluation queries")
    ap.add_argument("--seed", type=int, default=7, help="deterministic seed")
    ap.add_argument("--probe", type=int, default=2, help="groups the layered search visits")
    ap.add_argument("--sweep", action="store_true", help="chunks sweep 1024..8192")
    ap.add_argument("--self-test", action="store_true", help="assert the taught properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.chunks < args.k:
        print("chunks must be at least k")
        return 1
    groups = max(1, (args.chunks + GROUP_SIZE - 1) // GROUP_SIZE)
    if args.probe > groups:
        args.probe = groups
    if args.sweep:
        print_sweep(args.dim, args.dtype, args.k, args.seed, args.probe)
        return 0
    print_report(args.chunks, args.dim, args.dtype, args.k, args.queries, args.seed, args.probe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

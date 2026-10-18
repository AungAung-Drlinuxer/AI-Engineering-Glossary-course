#!/usr/bin/env python3
"""lab_chunking - chunk count, boundary tokens, cut sentences and index cost.

Offline, deterministic, standard library only.

Model (assumptions):
  source       : a stream of `--tokens` tokens laid out in sentences of 12 tokens
  chunking     : fixed-size chunks of `--chunk` tokens with `--overlap` shared tokens
  stride       : chunk - overlap
  chunk count  : 1 if tokens <= chunk, else 1 + ceil((tokens - chunk) / stride)
  boundaries   : stride, 2*stride, ... while the position is below tokens
  cut sentence : a boundary whose position is not a multiple of 12 (the sentence length)
  index cost   : chunks * dim(768) * 2 bytes (fp16) = 1536 bytes per vector

Flags:
  --tokens, --chunk, --overlap, --sweep, --self-test
"""

from __future__ import annotations

import argparse

SENTENCE_TOKENS = 12
DIM = 768
BYTES_PER_VECTOR = 2
MIB = 1024.0 * 1024.0
RULE = "=" * 74
THIN = "-" * 74
SWEEP_CHUNKS = [64, 128, 256, 512, 1024, 2048]


def chunk_count(tokens: int, chunk: int, overlap: int) -> int:
    if tokens <= chunk:
        return 1
    stride = chunk - overlap
    return 1 + -(-(tokens - chunk) // stride)


def boundaries(tokens: int, chunk: int, overlap: int) -> list[int]:
    stride = chunk - overlap
    count = chunk_count(tokens, chunk, overlap)
    return [stride * i for i in range(1, count) if stride * i < tokens]


def cut_sentences(tokens: int, chunk: int, overlap: int) -> int:
    return sum(1 for b in boundaries(tokens, chunk, overlap) if b % SENTENCE_TOKENS != 0)


def index_mib(count: int) -> float:
    return count * DIM * BYTES_PER_VECTOR / MIB


def duplicated(count: int, tokens: int, chunk: int) -> int:
    """Tokens stored more than once because of overlap (full-length chunks assumed)."""
    return max(0, count * chunk - tokens)


def print_report(tokens: int, chunk: int, overlap: int) -> None:
    stride = chunk - overlap
    count = chunk_count(tokens, chunk, overlap)
    bounds = boundaries(tokens, chunk, overlap)
    cut = cut_sentences(tokens, chunk, overlap)
    print(RULE)
    print("lab_chunking - chunk count, boundaries, index cost (offline, deterministic)")
    print(f"tokens={tokens:,}  chunk={chunk}  overlap={overlap}  stride={stride}  "
          f"sentence={SENTENCE_TOKENS} tokens (assumption)")
    print(THIN)
    print(f"  chunk count                   : {count:>12,}")
    print(f"  chunk boundaries              : {len(bounds):>12,}")
    print(f"  boundaries cutting a sentence : {cut:>12,}"
          f"  ({cut / len(bounds) * 100.0 if bounds else 0.0:.1f}%)")
    print(f"  duplicated (overlap) tokens   : {duplicated(count, tokens, chunk):>12,}")
    print(f"  index cost (fp16, dim {DIM})    : {index_mib(count):>12.4f} MiB")
    print(f"  index MiB per 1000 source tok  : {index_mib(count) / tokens * 1000:>12.4f}")
    print(THIN)
    print(f"chunk size settings at overlap={overlap} (fp16, dim {DIM} = {DIM * BYTES_PER_VECTOR} B/vector):")
    print("   chunk   stride    chunks   duplicated   cut sent     index MiB   MiB/1k tok")
    for size in SWEEP_CHUNKS:
        if size <= overlap:
            continue
        c = chunk_count(tokens, size, overlap)
        b = boundaries(tokens, size, overlap)
        k = sum(1 for x in b if x % SENTENCE_TOKENS != 0)
        print(f"  {size:>6} {size - overlap:>8} {c:>9,} {duplicated(c, tokens, size):>12,} "
              f"{k:>10,} {index_mib(c):>13.4f} {index_mib(c) / tokens * 1000:>11.4f}")
    print(THIN)
    print("မှတ်ချက် - chunk ကြီးလျှင် အရေအတွက် နည်း၍ index ချွေတာသည်၊ သို့သော် ရှာဖွေမှု "
          "တိကျမှု ကျဆင်းနိုင်သည်။")
    print("overlap တိုးလျှင် နယ်နိမိတ်တွင် ဖြတ်ခံရသည့် စာကြောင်း လျော့သော်လည်း chunk "
          "အရေအတွက်နှင့် index ကုန်ကျစရိတ် တိုးသည်။")
    print(RULE)


def print_sweep(tokens: int, chunk: int, overlap: int) -> None:
    print(RULE)
    print(f"lab_chunking - chunk size sweep and overlap sweep (tokens={tokens:,}, "
          f"sentence={SENTENCE_TOKENS})")
    print(THIN)
    print(f"overlap={overlap} fixed:")
    print("   chunk   stride    chunks   cut sent     index MiB")
    for size in SWEEP_CHUNKS:
        if size <= overlap:
            continue
        c = chunk_count(tokens, size, overlap)
        b = boundaries(tokens, size, overlap)
        k = sum(1 for x in b if x % SENTENCE_TOKENS != 0)
        print(f"  {size:>6} {size - overlap:>8} {c:>9,} {k:>10,} {index_mib(c):>13.4f}")
    print(THIN)
    print(f"chunk={chunk} fixed:")
    print(" overlap   stride    chunks   duplicated   cut sent     index MiB")
    for ov in (0, chunk // 8, chunk // 4, chunk // 2):
        if ov >= chunk:
            continue
        c = chunk_count(tokens, chunk, ov)
        b = boundaries(tokens, chunk, ov)
        k = sum(1 for x in b if x % SENTENCE_TOKENS != 0)
        print(f"  {ov:>7} {chunk - ov:>8} {c:>9,} {duplicated(c, tokens, chunk):>12,} "
              f"{k:>10,} {index_mib(c):>13.4f}")
    print(THIN)
    print("မှတ်ချက် - chunk size သည် index memory နှင့် boundary အရေအတွက်ကို ဆုံးဖြတ်သည်၊ "
          "overlap သည် continuity ကို ဝယ်ယူရန် memory ဖြင့် ပေးချေခြင်း ဖြစ်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    base = chunk_count(6000, 256, 0)
    expect = -(-6000 // 256)
    plain = base == expect
    print(f"[OK] without overlap the chunk count is ceil(tokens/chunk) ({base} == {expect}): {plain}")
    ok = ok and plain

    c0 = chunk_count(6000, 256, 0)
    c1 = chunk_count(6000, 256, 64)
    c2 = chunk_count(6000, 256, 128)
    grows = c0 <= c1 <= c2
    print(f"[OK] more overlap never reduces the chunk count ({c0} <= {c1} <= {c2}): {grows}")
    ok = ok and grows

    half = chunk_count(6000, 512, 0) <= chunk_count(6000, 256, 0)
    double = chunk_count(6000, 128, 0) >= chunk_count(6000, 256, 0)
    print(f"[OK] a larger chunk produces fewer chunks: {half and double}")
    ok = ok and half and double

    b = boundaries(6000, 256, 0)
    count_ok = len(b) == chunk_count(6000, 256, 0) - 1 and all(x < 6000 for x in b)
    print(f"[OK] there is one boundary between consecutive chunks ({len(b)} boundaries): {count_ok}")
    ok = ok and count_ok

    cut = cut_sentences(6000, 256, 0)
    bounds = len(boundaries(6000, 256, 0))
    inside = 0 <= cut <= bounds
    print(f"[OK] cut sentences cannot exceed boundaries ({cut} <= {bounds}): {inside}")
    ok = ok and inside

    overlap_fix = cut_sentences(6000, 240, 0)
    aligned = overlap_fix == 0
    print(f"[OK] a chunk size that is a multiple of the sentence length cuts nothing "
          f"({overlap_fix} cuts at chunk=240): {aligned}")
    ok = ok and aligned

    prop = abs(index_mib(2 * 100) - 2.0 * index_mib(100)) < 1e-9
    print(f"[OK] index cost is proportional to the chunk count: {prop}")
    ok = ok and prop

    print("[PASS] lab_chunking self-test passed." if ok else "[FAIL] lab_chunking self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Chunk count, boundaries and index cost (offline, deterministic).")
    ap.add_argument("--tokens", type=int, default=6000, help="source length in tokens")
    ap.add_argument("--chunk", type=int, default=256, help="chunk size in tokens")
    ap.add_argument("--overlap", type=int, default=32, help="shared tokens between chunks")
    ap.add_argument("--sweep", action="store_true", help="chunk size and overlap sweeps")
    ap.add_argument("--self-test", action="store_true", help="assert the taught properties")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.overlap >= args.chunk:
        print("overlap must be smaller than chunk")
        return 1
    if args.sweep:
        print_sweep(args.tokens, args.chunk, args.overlap)
        return 0
    print_report(args.tokens, args.chunk, args.overlap)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

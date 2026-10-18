#!/usr/bin/env python3
"""Worked example (a): vector index memory for a stated corpus.

Assumptions (repeated in the guide):
  chunks   = 250000 retrievable units
  dim      = 768 embedding dimensions
  metadata = 96 bytes per chunk (8-byte id + 88 bytes of source offsets and labels)
  fp32 = 4 bytes per element, fp16 = 2 bytes per element, int8 = 1 byte per element
  vector_bytes = chunks * dim * bytes_per_element
  index_bytes  = vector_bytes + chunks * metadata_bytes
  MiB = 1024**2, GiB = 1024**3
Standard library only, no GPU, pure arithmetic.
"""

CHUNKS = 250_000
DIM = 768
META_BYTES = 96
PRECISIONS = (("fp32", 4), ("fp16", 2), ("int8", 1))
DIMENSIONS = (256, 384, 768, 1536)
SOURCE_TOKENS = 12_000_000
CHUNK_SIZES = (128, 256, 512, 1024)
MIB = 1024.0 ** 2
GIB = 1024.0 ** 3

print("reference corpus: chunks=%d  dim=%d  metadata=%d B/chunk (assumption)"
      % (CHUNKS, DIM, META_BYTES))
print()
meta_gib = CHUNKS * META_BYTES / GIB
print("%-9s %8s %13s %13s %13s" % ("precision", "B/elem", "vector MiB", "vector GiB", "index GiB"))
for name, width in PRECISIONS:
    vec = CHUNKS * DIM * width
    print("%-9s %8d %13.2f %13.4f %13.4f"
          % (name, width, vec / MIB, vec / GIB, vec / GIB + meta_gib))
print()
print("dimension sweep at fp16 (chunks=%d):" % CHUNKS)
print("%10s %13s %13s %13s" % ("dim", "vector MiB", "vector GiB", "index GiB"))
for dim in DIMENSIONS:
    vec = CHUNKS * dim * 2
    print("%10d %13.2f %13.4f %13.4f" % (dim, vec / MIB, vec / GIB, vec / GIB + meta_gib))
print()
print("chunk size effect (source=%d tokens, overlap=12.5%% of chunk, fp16, dim=%d):"
      % (SOURCE_TOKENS, DIM))
print("%7s %8s %8s %10s %11s %13s"
      % ("chunk", "overlap", "stride", "chunks", "index MiB", "vectors/1k tok"))
for chunk in CHUNK_SIZES:
    overlap = chunk // 8
    stride = chunk - overlap
    count = -(-SOURCE_TOKENS // stride)
    idx = count * DIM * 2 / MIB
    print("%7d %8d %8d %10d %11.2f %13.2f"
          % (chunk, overlap, stride, count, idx, count / SOURCE_TOKENS * 1000))
print()
print("note: metadata is %d B/chunk and does not change with precision; it is %.2f GiB."
      % (META_BYTES, meta_gib))

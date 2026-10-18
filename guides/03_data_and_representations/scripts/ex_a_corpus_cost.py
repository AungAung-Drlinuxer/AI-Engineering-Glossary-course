#!/usr/bin/env python3
"""Worked example (a): raw corpus -> token count -> storage -> training cost.

Assumptions (all stated in the guide):
  corpus      : 96 GiB of raw UTF-8 text, three modalities
  bytes/token : english 4.0, burmese 1.2, code 3.5
                (character-to-token ratios vary by language, content, tokenizer)
  storage     : one uint32 token id = 4 bytes, one uint16 token id = 2 bytes
  training    : 6 * parameters FLOPs per token (forward + backward),
                7.0B parameters, 256 accelerators, 990 TFLOP/s peak each,
                MFU 0.35, USD 2.50 per accelerator-hour
No library, no GPU: pure arithmetic.  Deterministic.
"""

GIB = 1024 ** 3

CORPUS_GIB = 96.0
CORPUS_BYTES = CORPUS_GIB * GIB
MODALITIES = (
    ("english", 0.60, 4.0),
    ("burmese", 0.25, 1.2),
    ("code", 0.15, 3.5),
)
PARAMS = 7.0e9
FLOPS_PER_TOKEN = 6.0 * PARAMS
ACCELERATORS = 256
PEAK_TFLOPS = 990.0
MFU = 0.35
EPOCHS = 4
PRICE_PER_HOUR = 2.50

rows = []
total_tokens = 0.0
for name, share, bytes_per_token in MODALITIES:
    chunk_bytes = CORPUS_BYTES * share
    chunk_tokens = chunk_bytes / bytes_per_token
    total_tokens += chunk_tokens
    rows.append((name, share, chunk_bytes, bytes_per_token, chunk_tokens))

print("reference corpus: %.1f GiB of raw UTF-8 text (one pass)" % CORPUS_GIB)
print()
print("%-9s %8s %14s %12s %18s" % ("modality", "share", "bytes (GiB)", "bytes/token", "tokens"))
for name, share, chunk_bytes, bytes_per_token, chunk_tokens in rows:
    print("%-9s %7.1f%% %14.3f %12.1f %18d"
          % (name, share * 100.0, chunk_bytes / GIB, bytes_per_token, int(chunk_tokens)))
print("%-9s %7.1f%% %14.3f %12.2f %18d"
      % ("total", 100.0, CORPUS_BYTES / GIB, CORPUS_BYTES / total_tokens, int(total_tokens)))
print()
print("storage for the same one pass:")
print("  raw UTF-8 text              : %10.3f GiB" % (CORPUS_BYTES / GIB))
print("  token ids as uint32 (4 B)   : %10.3f GiB" % (total_tokens * 4.0 / GIB))
print("  token ids as uint16 (2 B)   : %10.3f GiB   (only if vocabulary < 65536)"
      % (total_tokens * 2.0 / GIB))
print()
flops = FLOPS_PER_TOKEN * total_tokens * EPOCHS
per_accelerator = PEAK_TFLOPS * 1e12 * MFU
wall_seconds = flops / (per_accelerator * ACCELERATORS)
wall_hours = wall_seconds / 3600.0
accelerator_hours = wall_hours * ACCELERATORS
cost_usd = accelerator_hours * PRICE_PER_HOUR
print("training model: %.1fB parameters, %s FLOPs per token (forward + backward)"
      % (PARAMS / 1e9, "{:,}".format(int(FLOPS_PER_TOKEN))))
print("cluster: %d accelerators x %.0f TFLOP/s peak, MFU %.2f -> %.2f PFLOP/s"
      % (ACCELERATORS, PEAK_TFLOPS, MFU, per_accelerator * ACCELERATORS / 1e15))
print("epochs=%d   price=USD %.2f per accelerator-hour" % (EPOCHS, PRICE_PER_HOUR))
print()
print("tokens seen over %d epoch(s)  : %18d" % (EPOCHS, int(total_tokens * EPOCHS)))
print("training FLOPs                : %18.4e" % flops)
print("wall clock                    : %18.2f h" % wall_hours)
print("accelerator-hours             : %18.2f" % accelerator_hours)
print("cost                          : %18.2f USD" % cost_usd)

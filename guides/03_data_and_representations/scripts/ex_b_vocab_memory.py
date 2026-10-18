#!/usr/bin/env python3
"""Worked example (b): vocabulary size against embedding and output-layer memory.

Assumptions (all stated in the guide):
  embedding matrix : vocabulary x d_model parameters
  output layer     : vocabulary x d_model parameters
                     tied with the embedding matrix -> counted once,
                     untied -> counted twice
  precision        : fp16 = 2 bytes per parameter
  reference model  : 7.0B parameters
  logits tensor    : batch x sequence x vocabulary x 4 bytes (fp32 scores)
                     vocabulary d types are the same for both matrices
No library, no GPU: pure arithmetic.  Deterministic.
"""

MIB = 1024 ** 2
GIB = 1024 ** 3

VOCABS = (32000, 64000, 128000, 256000)
D_MODEL_DEFAULT = 4096
D_MODELS = (1024, 2048, 4096, 8192)
VOCAB_FOR_D_SWEEP = 128000
TOTAL_PARAMS = 7.0e9
BATCH = 32
FP16_BYTES = 2

print("assumptions: 7.0B reference model, fp16 (2 B/parameter)")
print("             embedding and output matrices are vocabulary x d_model")
print()
print("d_model = %d, vocabulary sweep:" % D_MODEL_DEFAULT)
print("%-9s %16s %12s %12s %12s" % ("vocab", "matrix params", "tied MiB", "untied MiB", "share of model"))
for vocab in VOCABS:
    matrix_params = vocab * D_MODEL_DEFAULT
    print("%-9d %16d %12.2f %12.2f %11.2f%%"
          % (vocab, matrix_params,
             matrix_params * FP16_BYTES / MIB,
             2 * matrix_params * FP16_BYTES / MIB,
             (2 * matrix_params) / TOTAL_PARAMS * 100.0))
print()
print("vocabulary = %d, d_model sweep (untied embedding + output layer):" % VOCAB_FOR_D_SWEEP)
print("%-9s %16s %12s %12s" % ("d_model", "matrix params", "untied MiB", "share of model"))
for d_model in D_MODELS:
    matrix_params = VOCAB_FOR_D_SWEEP * d_model
    print("%-9d %16d %12.2f %11.2f%%"
          % (d_model, matrix_params,
             2 * matrix_params * FP16_BYTES / MIB,
             (2 * matrix_params) / TOTAL_PARAMS * 100.0))
print()
print("logits tensor at vocabulary %d, batch %d, fp32 (4 B per score):" % (VOCAB_FOR_D_SWEEP, BATCH))
for sequence in (1, 8192):
    logits_bytes = BATCH * sequence * VOCAB_FOR_D_SWEEP * 4
    print("  sequence %-6d %16d B = %9.3f MiB = %8.3f GiB"
          % (sequence, logits_bytes, logits_bytes / MIB, logits_bytes / GIB))
print()
print("bytes of the two matrices at vocabulary 128000, d_model 4096:")
tied = 128000 * 4096 * FP16_BYTES
print("  tied   : %10.2f MiB" % (tied / MIB))
print("  untied : %10.2f MiB  (+%.2f MiB for the second copy)"
      % (2 * tied / MIB, tied / MIB))

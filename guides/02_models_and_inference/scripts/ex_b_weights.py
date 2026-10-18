#!/usr/bin/env python3
"""Worked example (b): served-model weight memory at fp16 and at 4-bit.

Assumption: weight memory = parameter_count * bytes_per_parameter, plus a flat
runtime overhead that is ignored here (sharding, quantization metadata,
activations, framework overhead are NOT included). fp16 = 2 bytes/parameter;
4-bit = 0.5 byte/parameter. Accelerator = 80 GB, 16 GiB reserved for KV cache
and activations -> 64 GiB usable for weights.
"""
GB = 1000 ** 3
GIB = 1024 ** 3
PARAMS = (("7B", 7e9), ("70B", 70e9), ("405B", 405e9))
PREC = (("fp16", 2.0), ("4-bit", 0.5))
USABLE_GIB = 64.0

print("usable weight budget = 64 GiB (80 GB accelerator - 16 GiB reserved)")
print()
print("%-6s %-6s %12s %12s %12s" % ("params", "prec", "GiB", "GB", "copies @64GiB"))
for label, n in PARAMS:
    for prec, width in PREC:
        gib = n * width / GIB
        copies = int(USABLE_GIB // gib)
        print("%-6s %-6s %12.3f %12.3f %12d" % (label, prec, gib, n * width / GB, copies))
print()
print("ratio fp16/4-bit per model family = %.2f GiB saved for 70B" % (70e9 * 2 / GIB - 70e9 * 0.5 / GIB))

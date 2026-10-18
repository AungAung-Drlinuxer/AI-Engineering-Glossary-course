#!/usr/bin/env python3
"""Worked example (c): the effect of deduplication and leakage on effective epochs.

Assumptions (all stated in the guide):
  raw corpus        : 40,000,000 documents, 512 tokens each
  deduplication     : removes 11.0% exact copies and 7.0% near-duplicate copies
  token budget      : one pass over the raw corpus (what a naive plan buys)
  evaluation split  : 1.0% of the deduplicated documents
  leakage           : 3.5% of the evaluation documents also appear in training
  scoring model     : clean document loss 1.9320 nats (assumed),
                      leaked document loss 0.0500 nats (assumed)
One doc = 512 tokens throughout.  Deterministic, no library, no GPU
(the two loss values are assumptions, not measurements).
"""

import math

DOCS_RAW = 40000000
TOKENS_PER_DOC = 512
EXACT_DROP = 0.11
NEAR_DROP = 0.07
EVAL_SHARE = 0.010
LEAK_RATE = 0.035
CLEAN_LOSS = 1.9320
LEAKED_LOSS = 0.0500

raw_tokens = DOCS_RAW * TOKENS_PER_DOC
kept_share = 1.0 - EXACT_DROP - NEAR_DROP
kept_docs = DOCS_RAW * kept_share
kept_tokens = raw_tokens * kept_share

budget = raw_tokens
effective_epochs = budget / kept_tokens
duplicate_exposures = budget - kept_tokens

eval_docs = kept_docs * EVAL_SHARE
eval_tokens = eval_docs * TOKENS_PER_DOC
leaked_docs = eval_docs * LEAK_RATE
leaked_train_tokens = leaked_docs * TOKENS_PER_DOC

reported_loss = (1.0 - LEAK_RATE) * CLEAN_LOSS + LEAK_RATE * LEAKED_LOSS
clean_ppl = math.exp(CLEAN_LOSS)
reported_ppl = math.exp(reported_loss)
ppl_gain = (clean_ppl - reported_ppl) / clean_ppl * 100.0

print("raw corpus            : %d documents, %d tokens" % (DOCS_RAW, raw_tokens))
print("deduplication drops   : %.1f%% exact + %.1f%% near-duplicate = %.1f%% of documents"
      % (EXACT_DROP * 100.0, NEAR_DROP * 100.0, (1.0 - kept_share) * 100.0))
print("unique corpus left    : %d documents, %d tokens" % (int(kept_docs), int(kept_tokens)))
print()
print("token budget (one pass over the raw corpus) : %d tokens" % budget)
print("passes over unique data                     : %.4f epochs" % effective_epochs)
print("tokens re-read from duplicated material     : %d" % int(duplicate_exposures))
print()
print("evaluation split      : %d documents, %d tokens" % (int(eval_docs), int(eval_tokens)))
print("leaked documents      : %d  (%.2f%% of the split)"
      % (int(leaked_docs), LEAK_RATE * 100.0))
print("leaked training tokens: %d  (%.4f%% of the budget)"
      % (int(leaked_train_tokens), leaked_train_tokens / budget * 100.0))
print()
print("assumed clean loss %.4f nats ; assumed leaked-document loss %.4f nats"
      % (CLEAN_LOSS, LEAKED_LOSS))
print("reported loss over the whole split          : %.5f nats" % reported_loss)
print("understatement of loss                      : %.5f nats" % (CLEAN_LOSS - reported_loss))
print("perplexity, clean material                  : %.4f" % clean_ppl)
print("perplexity, split as reported               : %.4f" % reported_ppl)
print("apparent perplexity gain                    : %.4f%%" % ppl_gain)

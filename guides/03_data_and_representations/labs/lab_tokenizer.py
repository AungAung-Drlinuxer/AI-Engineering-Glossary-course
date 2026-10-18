#!/usr/bin/env python3
"""lab_tokenizer - BPE-style merge trainer over a fixed Burmese / English / code corpus.

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

နည်းလမ်း (character-level BPE နမူနာ):
  1. corpus အတွင်းရှိ character အားလုံးကို base symbol အစုအဝေး အဖြစ် သတ်မှတ်သည်။
  2. step တိုင်းတွင် အနီးကပ် ဆက်တွဲ ဖြစ်နေသည့် symbol အတွဲများကို ရေတွက်ပြီး
     အများဆုံး ဖြစ်ပေါ်သည့် အတွဲကို merge လုပ်သည် (count တူညီပါက pair အစဉ်ဖြင့် ဆုံးဖြတ်သည်)။
  3. merge အတွဲတိုင်းသည် vocabulary ထဲသို့ ယူနစ် တစ်ခု ထည့်သည်။
  4. စာသားတစ်ခုကို ခွဲခြမ်းရာတွင် rank အနည်းဆုံး (အစောဆုံး) merge ကို အကြိမ်ကြိမ် အသုံးပြုသည်။
     ၎င်းသည် BPE encode ၏ စံနည်းလမ်း ဖြစ်သည်။

ဤ lab သည် byte-level BPE အစစ် မဟုတ်ပါ၊ ဖွဲ့စည်းပုံ တူညီသည့် character-level နမူနာ ဖြစ်သည်။
Training corpus အပြည့်အစုံကို merge သင်ယူရာတွင် အသုံးပြုသည်၊ `--texts` သည် ခွဲခြမ်းပြသည့်
စာသားများကိုသာ ရွေးချယ်သည်။
"""

from __future__ import annotations

import argparse

BURMESE = ("အချက်အလက် ကို token များအဖြစ် ခွဲခြမ်းသည်။ model သည် token အရေအတွက် အပေါ် မှီခိုသည်။"
           " မြန်မာ စာသား အတွက် byte တစ်လုံးလျှင် token များသည်။")
ENGLISH = "the tokenizer splits text into subword units. rare words become several smaller units."
CODE = "def add(a, b):\n    return a + b"

CORPUS = (
    ("burmese", BURMESE),
    ("english", ENGLISH),
    ("code", CODE),
)
ALL_TEXTS = tuple(name for name, _ in CORPUS)
MERGE_STEPS = (0, 2, 4, 6, 8, 10, 12, 16, 20)
SHOWN_TOKENS = 18
RULE = "=" * 74
THIN = "-" * 74


def base_symbols(texts: list[str]) -> list[str]:
    """corpus အတွင်းရှိ character အားလုံးကို အစဉ်လိုက် ပြန်ပေးသည် (set အစဉ်ကို မသုံးရ)။"""
    seen = set()
    for text in texts:
        seen.update(text)
    return sorted(seen)


def count_pairs(words: list[list[str]]) -> dict[tuple[str, str], int]:
    """အနီးကပ် symbol အတွဲ တိုင်း၏ အကြိမ်အရေအတွက်။"""
    counts: dict[tuple[str, str], int] = {}
    for symbols in words:
        for i in range(len(symbols) - 1):
            pair = (symbols[i], symbols[i + 1])
            counts[pair] = counts.get(pair, 0) + 1
    return counts


def best_pair(counts: dict[tuple[str, str], int]) -> tuple[tuple[str, str], int]:
    """အများဆုံး ဖြစ်ပေါ်သည့် အတွဲ။ count တူညီပါက pair အစဉ်ဖြင့် ဆုံးဖြတ်သည်။"""
    best: tuple[str, str] = ("", "")
    best_count = -1
    for pair in sorted(counts):
        if counts[pair] > best_count:
            best = pair
            best_count = counts[pair]
    return best, best_count


def apply_merge(words: list[list[str]], pair: tuple[str, str]) -> list[list[str]]:
    """အတွဲ တစ်ခုကို corpus တစ်လျှောက်လုံးတွင် ပေါင်းစပ်သည်။"""
    merged_symbol = pair[0] + pair[1]
    out = []
    for symbols in words:
        new_symbols = []
        i = 0
        while i < len(symbols):
            if i < len(symbols) - 1 and symbols[i] == pair[0] and symbols[i + 1] == pair[1]:
                new_symbols.append(merged_symbol)
                i += 2
            else:
                new_symbols.append(symbols[i])
                i += 1
        out.append(new_symbols)
    return out


def train(texts: list[str], merges: int, vocab_target: int):
    """merge အစဉ်ကို သင်ယူသည်။ (base size, merge list, vocab size) ပြန်ပေးသည်။"""
    words = [list(text) for text in texts]
    base = len(base_symbols(texts))
    table: list[tuple[tuple[str, str], int]] = []
    vocab_size = base
    for _ in range(merges):
        if vocab_target and vocab_size >= vocab_target:
            break
        counts = count_pairs(words)
        if not counts:
            break
        pair, count = best_pair(counts)
        words = apply_merge(words, pair)
        table.append((pair, count))
        vocab_size += 1
    return base, table, vocab_size


def encode(text: str, ranks: dict[tuple[str, str], int]) -> list[str]:
    """rank အနည်းဆုံး merge ကို အကြိမ်ကြိမ် အသုံးပြု၍ ခွဲခြမ်းသည်။"""
    symbols = list(text)
    while len(symbols) > 1:
        best_index = -1
        best_rank = None
        for i in range(len(symbols) - 1):
            rank = ranks.get((symbols[i], symbols[i + 1]))
            if rank is not None and (best_rank is None or rank < best_rank):
                best_rank = rank
                best_index = i
        if best_index < 0:
            break
        symbols = symbols[:best_index] + [symbols[best_index] + symbols[best_index + 1]] \
            + symbols[best_index + 2:]
    return symbols


def ranks_of(table: list[tuple[tuple[str, str], int]]) -> dict[tuple[str, str], int]:
    return {pair: index for index, (pair, _) in enumerate(table)}


def merge_depth(text: str, table: list[tuple[tuple[str, str], int]]) -> int:
    """ခွဲခြမ်းမှုတွင် အသုံးပြုခဲ့သည့် merge အရေအတွက် (မတူညီသည့် အမျိုးအစား)။"""
    ranks = ranks_of(table)
    used = set()
    symbols = list(text)
    while len(symbols) > 1:
        best_index = -1
        best_rank = None
        for i in range(len(symbols) - 1):
            rank = ranks.get((symbols[i], symbols[i + 1]))
            if rank is not None and (best_rank is None or rank < best_rank):
                best_rank = rank
                best_index = i
        if best_index < 0:
            break
        used.add(best_rank)
        symbols = symbols[:best_index] + [symbols[best_index] + symbols[best_index + 1]] \
            + symbols[best_index + 2:]
    return len(used)


def show(token: str) -> str:
    """ထိန်းချုပ်သည့် အက္ခရာ (newline၊ tab) ကို ဖတ်နိုင်သည့် ပုံစံဖြင့် ပြသည်။"""
    return token.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def parse_texts(raw: str) -> list[str]:
    names = [part.strip() for part in raw.split(",") if part.strip()]
    unknown = [name for name in names if name not in ALL_TEXTS]
    if unknown:
        raise SystemExit("unknown text name(s): %s (choose from %s)"
                         % (", ".join(unknown), ",".join(ALL_TEXTS)))
    if not names:
        raise SystemExit("--texts must name at least one text")
    return names


def print_report(merges: int, vocab_target: int, selected: list[str]) -> None:
    texts = [text for _, text in CORPUS]
    base, table, vocab_size = train(texts, merges, vocab_target)
    corpus_chars = sum(len(text) for text in texts)

    print(RULE)
    print("lab_tokenizer - BPE-style merge trainer (offline, deterministic)")
    print("corpus: " + " / ".join("%s %d chars" % (name, len(text)) for name, text in CORPUS)
          + " / total %d" % corpus_chars)
    print("merges=%d  vocab-target=%d  base symbols=%d  final vocab=%d"
          % (merges, vocab_target, base, vocab_size))
    print(THIN)
    print("  idx  merged pair                 count   vocab")
    for index, (pair, count) in enumerate(table, start=1):
        print("  %3d  %-24s %6d   %5d"
              % (index, "%s + %s" % (show(pair[0]), show(pair[1])), count, base + index))
    if not table:
        print("  (no merge was applied)")
    print(THIN)
    print(" text      chars  tokens  bytes/token  merge depth")
    for name in selected:
        text = dict(CORPUS)[name]
        tokens = encode(text, ranks_of(table))
        print(" %-9s %5d %7d %12.2f %12d"
              % (name, len(text), len(tokens), len(text.encode("utf-8")) / len(tokens),
                 merge_depth(text, table)))
    print(THIN)
    print("segmentation (%d merges):" % len(table))
    for name in selected:
        text = dict(CORPUS)[name]
        tokens = encode(text, ranks_of(table))
        shown = " ".join(show(token) for token in tokens[:SHOWN_TOKENS])
        if len(tokens) > SHOWN_TOKENS:
            shown += " ... (+%d more)" % (len(tokens) - SHOWN_TOKENS)
        print(" %-9s %s" % (name, shown))
    print(RULE)


def print_sweep(vocab_target: int, selected: list[str]) -> None:
    texts = [text for _, text in CORPUS]
    print(RULE)
    print("lab_tokenizer - merge-count sweep (token အရေအတွက် နှင့် chars/token)")
    print(THIN)
    print(" merges  vocab  " + "  ".join("%-12s" % name for name in selected))
    for merges in MERGE_STEPS:
        base, table, vocab_size = train(texts, merges, vocab_target)
        if vocab_size != base + len(table):
            raise SystemExit("internal error: vocab accounting")
        cells = []
        for name in selected:
            tokens = encode(dict(CORPUS)[name], ranks_of(table))
            cells.append("%-12s" % ("%d tok" % len(tokens)))
        print(" %6d  %5d  %s" % (merges, vocab_size, "  ".join(cells)))
    print(THIN)
    print("မှတ်ချက် - merge တိုးလျှင် vocabulary ကြီးပြီး token အရေအတွက် ကျဆင်းသည်။")
    print(RULE)


def self_test() -> int:
    ok = True
    texts = [text for _, text in CORPUS]

    base, table, vocab_size = train(texts, 10, 0)
    growth = vocab_size == base + 10 and len(table) == 10
    print("[OK] every merge adds exactly one vocabulary entry (%d -> %d): %s"
          % (base, vocab_size, growth))
    ok = ok and growth

    _, empty, _ = train(texts, 0, 0)
    zero_ok = all(len(encode(text, ranks_of(empty))) == len(text) for text in texts)
    print("[OK] with zero merges every text is segmented into its characters: %s" % zero_ok)
    ok = ok and zero_ok

    _, long_table, _ = train(texts, 20, 0)
    drops = all(len(encode(text, ranks_of(long_table))) <= len(encode(text, ranks_of(empty)))
                for text in texts)
    print("[OK] more merges never increase the token count: %s" % drops)
    ok = ok and drops

    round_trip = all("".join(encode(text, ranks_of(table))) == text for text in texts)
    print("[OK] segmentation round-trips back to the original text: %s" % round_trip)
    ok = ok and round_trip

    words = [list(text) for text in texts]
    counts = count_pairs(words)
    pair, count = best_pair(counts)
    manual = max(counts.values())
    _, one_step, vocab_after_one = train(texts, 1, 0)
    greedy_ok = count == manual and vocab_after_one == base + 1 and len(one_step) == 1
    print("[OK] step 1 merges the most frequent pair %s + %s (%d times, max is %d): %s"
          % (show(pair[0]), show(pair[1]), count, manual, greedy_ok))
    ok = ok and greedy_ok

    again = train(texts, 10, 0)
    det_ok = again == (base, table, vocab_size)
    print("[OK] training is deterministic for identical input: %s" % det_ok)
    ok = ok and det_ok

    print("[PASS] lab_tokenizer self-test passed." if ok else "[FAIL] lab_tokenizer self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="BPE-style merge trainer lab (offline, deterministic).")
    ap.add_argument("--texts", default="burmese,english,code",
                    help="comma list of texts to segment (burmese, english, code)")
    ap.add_argument("--merges", type=int, default=10, help="number of merge operations to learn")
    ap.add_argument("--vocab-target", type=int, default=0,
                    help="stop merging once the vocabulary reaches this size (0 = no limit)")
    ap.add_argument("--sweep", action="store_true", help="token counts over a merge-count sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.merges < 0:
        raise SystemExit("--merges must not be negative")
    if args.self_test:
        return self_test()
    selected = parse_texts(args.texts)
    if args.sweep:
        print_sweep(args.vocab_target, selected)
        return 0
    print_report(args.merges, args.vocab_target, selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

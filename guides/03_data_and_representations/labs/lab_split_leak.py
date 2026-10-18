#!/usr/bin/env python3
"""lab_split_leak - random row split against entity-group split, with near-duplicate
leakage detection (offline, deterministic).

Offline ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ third-party import တစ်ခုမျှ မလိုအပ်ပါ။

ဖွဲ့စည်းပုံ:
  - record တိုင်းကို entity group တစ်ခုထဲသို့ ထည့်သည် (group-size ခုစီ)။
  - `--leak-rate` ဖြင့် record တစ်ခုသည် ၎င်း၏ ရှေ့ record ၏ အနီးစပ်ဆုံး တူညီသည့်
    မိတ္တူ (near-duplicate twin) ဖြစ်လာသည်။ twin နှင့် ၎င်း၏ source သည် group တူညီသည်။
  - **row split** သည် record များကို ကျပန်း ခွဲသည်၊ ထို့ကြောင့် twin အတွဲများသည်
    split နယ်နိမိတ်ကို ဖြတ်ကျော်နိုင်သည်။ **group split** သည် entity အလိုက် ခွဲသည်။
  - leakage ကို 5-gram shingle နှင့် Jaccard ဆင်တူမှုဖြင့် ရှာဖွေသည် (ခန့်မှန်း တန်ဖိုး အပေါ်
    မမှီခိုဘဲ တကယ် တိုင်းတာသည်)။
  - ယိုစိမ့်သည့် val record သည် training တွင် မြင်ဖူးပြီး ဖြစ်သည့်အတွက် မြင့်မားသည့် score
    ရရှိသည် (0.9900)၊ သန့်ရှင်းသည့် record သည် ၎င်း၏ ခက်ခဲမှု အလိုက် score ရရှိသည်။
"""

from __future__ import annotations

import argparse
import random

GROUP_SIZE = 6
BODY_TOKENS = 16
VOCAB = 256
SHINGLE = 5
JACCARD_MIN = 0.80
LEAKED_SCORE = 0.9900
SWEEP_RATES = (0.00, 0.05, 0.10, 0.20, 0.30)
RULE = "=" * 74
THIN = "-" * 74


def build_corpus(n: int, seed: int, leak_rate: float):
    """bodies၊ groups နှင့် difficulties ကို ပြန်ပေးသည်။

    Body token များကို leak_rate နှင့် မသက်ဆိုင်ဘဲ အမြဲ ဆွဲထုတ်သည်၊ ထို့ကြောင့်
    rate တစ်ခုမှ တစ်ခုသို့ ရွေ့လျှင် corpus ကိုယ်တိုင် မပြောင်းလဲပါ။
    """
    rng = random.Random(seed)
    bodies: list[list[str]] = []
    difficulties: list[float] = []
    planted: list[int] = []
    for index in range(n):
        drawn = ["w%03d" % rng.randrange(VOCAB) for _ in range(BODY_TOKENS)]
        plant = index > 0 and index % GROUP_SIZE != 0 and rng.random() < leak_rate
        if plant:
            bodies.append(list(bodies[index - 1]))
            planted.append(index)
        else:
            bodies.append(drawn)
        difficulties.append(0.5000 + 0.5000 * rng.random())
    return bodies, difficulties, planted


def shingles(tokens: list[str]) -> frozenset[tuple[str, ...]]:
    return frozenset(tuple(tokens[i:i + SHINGLE]) for i in range(len(tokens) - SHINGLE + 1))


def tokenize(bodies: list[list[str]]) -> list[list[str]]:
    return [body + ["tag%04d" % index] for index, body in enumerate(bodies)]


def row_split(n: int, val_fraction: float, seed: int) -> tuple[list[int], list[int]]:
    """record အလိုက် ကျပန်း ခွဲခြားမှု။"""
    val_size = int(round(n * val_fraction))
    val = sorted(random.Random(seed + 1).sample(range(n), val_size))
    val_set = set(val)
    train = [index for index in range(n) if index not in val_set]
    return train, val


def group_split(n: int, val_fraction: float, seed: int) -> tuple[list[int], list[int]]:
    """entity group အလိုက် ခွဲခြားမှု — group တစ်ခုလုံး split တစ်ခုတည်းထဲသို့ ရောက်သည်။"""
    group_count = (n + GROUP_SIZE - 1) // GROUP_SIZE
    order = list(range(group_count))
    random.Random(seed + 2).shuffle(order)
    target = int(round(n * val_fraction))
    val_groups = set()
    taken = 0
    for group in order:
        if taken >= target:
            break
        val_groups.add(group)
        first = group * GROUP_SIZE
        last = min(first + GROUP_SIZE, n)
        taken += last - first
    train = [index for index in range(n) if index // GROUP_SIZE not in val_groups]
    val = [index for index in range(n) if index // GROUP_SIZE in val_groups]
    return train, val


def detect(train: list[int], val: list[int], tokens: list[list[str]]) -> set[int]:
    """ယိုစိမ့်မှု ရှိသည့် val record ၏ global index အစုအဝေး — 5-gram shingle နှင့်
    Jaccard ဆင်တူမှုဖြင့် တိုင်းတာသည်။"""

    train_shingles = {index: shingles(tokens[index]) for index in train}
    index_map: dict[tuple[str, ...], list[int]] = {}
    for index in train:
        for shingle in train_shingles[index]:
            index_map.setdefault(shingle, []).append(index)
    hits: set[int] = set()
    for index in val:
        mine = shingles(tokens[index])
        shared: dict[int, int] = {}
        for shingle in mine:
            for other in index_map.get(shingle, ()):
                shared[other] = shared.get(other, 0) + 1
        for other, common in shared.items():
            union = len(mine) + len(train_shingles[other]) - common
            if union > 0 and common / union >= JACCARD_MIN:
                hits.add(index)
                break
    return hits


def evaluate(n: int, val_fraction: float, seed: int, leak_rate: float) -> dict:
    bodies, difficulties, planted = build_corpus(n, seed, leak_rate)
    tokens = tokenize(bodies)
    row_train, row_val = row_split(n, val_fraction, seed)
    grp_train, grp_val = group_split(n, val_fraction, seed)
    row_hits = detect(row_train, row_val, tokens)
    grp_hits = detect(grp_train, grp_val, tokens)

    def accuracy(value_indices: list[int], hits: set[int]) -> tuple[float, float]:
        clean = sum(difficulties[i] for i in value_indices) / len(value_indices)
        reported = sum(LEAKED_SCORE if i in hits else difficulties[i]
                       for i in value_indices) / len(value_indices)
        return clean, reported

    row_clean, row_reported = accuracy(row_val, row_hits)
    grp_clean, grp_reported = accuracy(grp_val, grp_hits)
    return {
        "planted": len(planted),
        "row": {
            "train": len(row_train), "val": len(row_val),
            "hits": len(row_hits),
            "rate": len(row_hits) / len(row_val),
            "clean": row_clean, "reported": row_reported,
        },
        "grp": {
            "train": len(grp_train), "val": len(grp_val),
            "hits": len(grp_hits),
            "rate": len(grp_hits) / len(grp_val),
            "clean": grp_clean, "reported": grp_reported,
        },
    }


def print_report(n: int, val_fraction: float, seed: int, leak_rate: float) -> None:
    result = evaluate(n, val_fraction, seed, leak_rate)
    row = result["row"]
    grp = result["grp"]
    print(RULE)
    print("lab_split_leak - random row split vs entity-group split (offline, deterministic)")
    print("records=%d  val-fraction=%s  seed=%d  leak-rate=%.2f  group-size=%d"
          % (n, val_fraction, seed, leak_rate, GROUP_SIZE))
    print("detection: %d-gram shingles, Jaccard >= %.2f" % (SHINGLE, JACCARD_MIN))
    print(THIN)
    print(" %-28s %10s %13s" % ("", "row split", "group split"))
    print(" %-28s %10d %13d" % ("train records", row["train"], grp["train"]))
    print(" %-28s %10d %13d" % ("val records", row["val"], grp["val"]))
    print(" %-28s %10d %13d" % ("planted near-duplicates", result["planted"], result["planted"]))
    print(" %-28s %10d %13d" % ("val records with a train twin", row["hits"], grp["hits"]))
    print(" %-28s %9.2f%% %12.2f%%" % ("contamination rate", row["rate"] * 100.0, grp["rate"] * 100.0))
    print(" %-28s %10.4f %13.4f" % ("clean val accuracy", row["clean"], grp["clean"]))
    print(" %-28s %10.4f %13.4f" % ("reported val accuracy", row["reported"], grp["reported"]))
    print(" %-28s %+10.4f %+13.4f"
          % ("score inflation", row["reported"] - row["clean"], grp["reported"] - grp["clean"]))
    print(THIN)
    print("မှတ်ချက် - ကျပန်း ခွဲခြားမှုသည် အနီးစပ်ဆုံး တူညီသည့် နမူနာများကို split နယ်နိမိတ် "
          "ဖြတ်ကျော်စေသည်၊ entity အလိုက် ခွဲခြားလျှင် ထို ဖြတ်ကျော်မှု မရှိပါ။")
    print(RULE)


def print_sweep(n: int, val_fraction: float, seed: int) -> None:
    print(RULE)
    print("lab_split_leak - leak-rate sweep (row split)")
    print(THIN)
    print(" leak-rate  planted  val twins  contamination  reported acc  inflation")
    for rate in SWEEP_RATES:
        result = evaluate(n, val_fraction, seed, rate)
        row = result["row"]
        print(" %9.2f %8d %10d %13.2f%% %13.4f %+10.4f"
              % (rate, result["planted"], row["hits"], row["rate"] * 100.0,
                 row["reported"], row["reported"] - row["clean"]))
    print(THIN)
    print("မှတ်ချက် - leak-rate တက်လျှင် contamination rate တက်ပြီး ပြသသည့် accuracy လည်း တက်သည်။")
    print(RULE)


def self_test() -> int:
    ok = True

    first = build_corpus(600, 5, 0.10)
    second = build_corpus(600, 5, 0.10)
    print("[OK] corpus construction is deterministic for a fixed seed: %s" % (first == second))
    ok = ok and first == second

    n = 600
    bodies, _, _ = first
    tokens = tokenize(bodies)
    row_train, row_val = row_split(n, 0.2, 5)
    grp_train, grp_val = group_split(n, 0.2, 5)
    partition = (sorted(row_train + row_val) == list(range(n))
                 and sorted(grp_train + grp_val) == list(range(n))
                 and not (set(row_train) & set(row_val))
                 and not (set(grp_train) & set(grp_val)))
    print("[OK] both splits partition every record with no overlap: %s" % partition)
    ok = ok and partition

    zero = evaluate(600, 0.2, 5, 0.0)
    zero_ok = zero["row"]["hits"] == 0 and zero["row"]["rate"] == 0.0
    print("[OK] with no planted duplicates the row split contaminates nothing: %s" % zero_ok)
    ok = ok and zero_ok

    base = evaluate(600, 0.2, 5, 0.10)
    grp_ok = base["grp"]["hits"] == 0 and base["planted"] > 0
    print("[OK] the group split keeps every twin inside one split (contamination 0): %s" % grp_ok)
    ok = ok and grp_ok

    rising = evaluate(600, 0.2, 5, 0.05)["row"]["rate"] < evaluate(600, 0.2, 5, 0.30)["row"]["rate"]
    print("[OK] a higher leak-rate raises the measured contamination rate: %s" % rising)
    ok = ok and rising

    inflation_ok = base["row"]["reported"] >= base["row"]["clean"] and base["row"]["hits"] > 0
    print("[OK] leaked validation records inflate the reported accuracy: %s" % inflation_ok)
    ok = ok and inflation_ok

    print("[PASS] lab_split_leak self-test passed." if ok else "[FAIL] lab_split_leak self-test failed.")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Near-duplicate leakage across a dataset split "
                                             "(offline, deterministic).")
    ap.add_argument("--n", type=int, default=2000, help="number of records in the corpus")
    ap.add_argument("--val-fraction", type=float, default=0.2, help="share of records held out")
    ap.add_argument("--seed", type=int, default=0, help="corpus and split seed")
    ap.add_argument("--leak-rate", type=float, default=0.10,
                    help="probability that a record is a near-duplicate of the previous one")
    ap.add_argument("--sweep", action="store_true", help="leak-rate 0.00 .. 0.30 sweep")
    ap.add_argument("--self-test", action="store_true", help="assert the properties this lab teaches")
    args = ap.parse_args()

    if args.n < 20:
        raise SystemExit("--n must be at least 20")
    if not 0.0 < args.val_fraction < 1.0:
        raise SystemExit("--val-fraction must lie strictly between 0 and 1")
    if not 0.0 <= args.leak_rate <= 1.0:
        raise SystemExit("--leak-rate must lie between 0 and 1")
    if args.self_test:
        return self_test()
    if args.sweep:
        print_sweep(args.n, args.val_fraction, args.seed)
        return 0
    print_report(args.n, args.val_fraction, args.seed, args.leak_rate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

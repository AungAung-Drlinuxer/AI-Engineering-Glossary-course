# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Data & Representations)

ဤဖိုင်သည် နယ်ပယ် ၀၃ ၏ term ၁၃ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့်
ဆုံးဖြတ်ချက် ချခြင်း လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့်
ဥပမာ လေးခု၊ အပိုင်း ၂ တွင် တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ
ရှာဖွေခြင်း သုံးခု၊ အပိုင်း ၄ တွင် ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင်
အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ
ပေးထားသည်။

အပိုင်း ၁ နှင့် အပိုင်း ၅ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ)
ဖြင့် အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် command
အတိုင်း run လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည်
သတ်မှတ်ထားသည့် ယူဆချက် (assumption) အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ
၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။ ဤဖိုင်၏ တွက်ချက်မှုများသည် lab များအပေါ် မှီခိုမှု မရှိပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — စာသားမှ token သို့: BPE merge အစဉ်နှင့် token အရေအတွက်

**ယူဆချက် —** corpus တွင် စကားလုံး ငါးမျိုး ရှိသည် — `low` x5၊ `lowest` x1၊ `newer` x2၊ `newest` x3၊
`wider` x1။ အစ အခြေအနေတွင် စကားလုံး တိုင်းကို စာလုံး တစ်လုံးချင်း အဖြစ် ခွဲ၍ စကားလုံး အဆုံး
သတ်မှတ်သည့် marker ကို ထည့်သည်။ merge အကြိမ် ၆ ကြိမ် လုပ်သည်။ frequency တူညီပါက
စာလုံး အစဉ်အလိုက် ရွေးသည် — ထို့ကြောင့် ရလဒ်သည် deterministic ဖြစ်သည်။

**ဖော်မြူလာ —**
- အစ token အရေအတွက် = Σ (စာလုံး အရေအတွက် + 1) × frequency
- merge တိုင်းတွင် အနီးကပ် ယူနစ် အတွဲ ၏ frequency = Σ ထို အတွဲ ပါဝင်သည့် စကားလုံး၏ frequency
- token အရေအတွက် (merge တစ်ကြိမ် ပြီးတိုင်း) = Σ ထို စကားလုံး၏ ယူနစ် အရေအတွက် × frequency

**တွက်ချက်မှု —**
1. အစ token = (3+1)×5 + (6+1)×1 + (5+1)×2 + (6+1)×3 + (5+1)×1 = 20 + 7 + 12 + 21 + 6 = 66 ဖြစ်သည်။
2. merge ၁: `w` + `e` (frequency 6)၊ token 60 သို့ ကျဆင်းသည်။
3. merge ၂: `l` + `o` (frequency 6)၊ token 54 သို့ ကျဆင်းသည်။
4. merge ၃: `w` + end marker (frequency 5)၊ token 49 ဖြစ်သည်။
5. merge ၄: `n` + `e` (frequency 5)၊ token 44 ဖြစ်သည်။
6. merge ၅: `ne` + `we` (frequency 5)၊ token 39 ဖြစ်သည်။
7. merge ၆: `lo` + `low` + end marker (frequency 5)၊ token 34 ဖြစ်သည်။
8. ဖြစ်ပေါ်သည့် vocabulary symbol = 12 ခု၊ compress ratio = 66 / 34 = 1.94 ဖြစ်သည်။

**ကောက်ချက် —** merge ခြောက်ကြိမ်ဖြင့် token အရေအတွက်သည် 66 မှ 34 သို့ ကျဆင်းသည်၊
ဆိုလိုသည်မှာ 48.5 % လျော့သည်။ ထို့ကြောင့် token အရေအတွက်နှင့် ကုန်ကျစရိတ်ကို
tokenizer ၏ merge rule က တိုက်ရိုက် ဆုံးဖြတ်သည်။ `lowest` ကဲ့သို့ ရှားပါးသည့် စကားလုံးသည်
`lo`၊ `we`၊ `s`၊ `t`၊ end marker အဖြစ် ဆက်လက် ကိုယ်စားပြုခံရသည် — ဤအချက်သည်
`Byte Pair Encoding (BPE)` ၏ မမြင်ဖူးသေးသည့် စကားလုံး ကိုင်တွယ်နိုင်စွမ်း ဖြစ်သည်။

```bash
python3 - <<'PY'
import collections

CORPUS = {"low": 5, "lowest": 1, "newer": 2, "newest": 3, "wider": 1}


def train(corpus, num_merges):
    words = {w: list(w) + ["end"] for w in corpus}
    history = [(0, sum(len(words[w]) * corpus[w] for w in corpus))]
    merges = []
    for step in range(1, num_merges + 1):
        pairs = collections.Counter()
        for w, syms in words.items():
            for i in range(len(syms) - 1):
                pairs[(syms[i], syms[i + 1])] += corpus[w]
        if not pairs:
            break
        (a, b), freq = max(pairs.items(), key=lambda kv: (kv[1], kv[0]))
        merges.append((a, b, freq))
        for w, syms in words.items():
            out, i = [], 0
            while i < len(syms):
                if i + 1 < len(syms) and syms[i] == a and syms[i + 1] == b:
                    out.append(a + b)
                    i += 2
                else:
                    out.append(syms[i])
                    i += 1
            words[w] = out
        history.append((step, sum(len(words[w]) * corpus[w] for w in corpus)))
    return words, merges, history


words, merges, history = train(CORPUS, 6)
print("corpus:", ", ".join(f"{w} x{c}" for w, c in CORPUS.items()))
print("initial token count:", history[0][1])
for a, b, freq in merges:
    print(f"merge {a} + {b} (frequency {freq})")
for step, count in history:
    print(f"tokens after {step} merges: {count}")
symbols = set()
for w in words:
    symbols |= set(words[w])
print("distinct symbols in vocabulary:", len(symbols))
for w in words:
    print(f"segmentation {w}: {' '.join(words[w])}")
PY
```

```text
corpus: low x5, lowest x1, newer x2, newest x3, wider x1
initial token count: 66
merge w + e (frequency 6)
merge l + o (frequency 6)
merge w + end (frequency 5)
merge n + e (frequency 5)
merge ne + we (frequency 5)
merge lo + wend (frequency 5)
tokens after 0 merges: 66
tokens after 1 merges: 60
tokens after 2 merges: 54
tokens after 3 merges: 49
tokens after 4 merges: 44
tokens after 5 merges: 39
tokens after 6 merges: 34
distinct symbols in vocabulary: 12
segmentation low: lowend
segmentation lowest: lo we s t end
segmentation newer: newe r end
segmentation newest: newe s t end
segmentation wider: w i d e r end
```

### ဥပမာ ၂ — Vocabulary အရွယ်အစားနှင့် embedding memory

**ယူဆချက် —** embedding နှင့် output projection ကို weight tying လုပ်ထားသည်ဟု ယူဆသည်၊
ထို့ကြောင့် matrix တစ်ခုကို နှစ်ကြိမ် ရေတွက်သည်။ fp16 ဖြစ်၍ element တစ်ခုလျှင် 2 byte။
d_model နှစ်မျိုး — 768 (မော်ဒယ် ငယ်) နှင့် 4096 (မော်ဒယ် ကြီး)။

**ဖော်မြူလာ —**
- embedding matrix bytes = vocabulary အရေအတွက် × d_model × element byte
- weight tying ရှိပါက စုစုပေါင်း = 2 × embedding matrix bytes

**တွက်ချက်မှု —**
1. vocabulary 32,000၊ d_model 768၊ fp16: 32,000 × 768 × 2 = 49,152,000 byte = 46.88 MiB ဖြစ်သည်။
2. တူညီသည့် အတိုင်းအတာတွင် weight tying ပါ ထည့်ပါက 93.75 MiB ဖြစ်သည်။
3. vocabulary 50,257၊ d_model 4096: 392.63 MiB (untied)၊ 785.27 MiB (tied) ဖြစ်သည်။
4. vocabulary 128,256၊ d_model 4096: 1002.00 MiB (untied)၊ 2004.00 MiB (tied) ဖြစ်သည်။
5. 128,256 နှင့် 32,000 ၏ memory အချိုး = 128,256 / 32,000 = 4.008 ဖြစ်သည်။
6. 128,256၊ d_model 4096 ကို int8 ဖြင့် သိမ်းပါက untied matrix သည် 501.0 MiB ဖြစ်သည်။

**ကောက်ချက် —** vocabulary အရွယ်အစားသည် embedding memory အပေါ် **တိုက်ရိုက် အချိုးကျ**
သက်ရောက်သည်၊ ဆိုလိုသည်မှာ vocabulary လေးဆ ဖြစ်ပါက memory လေးဆ ဖြစ်သည်။
weight tying ရှိပါက ထို ကုန်ကျစရိတ် နှစ်ဆ ဖြစ်သည်။ ထို့ကြောင့် multilingual
vocabulary ကြီးသည့် မော်ဒယ်တွင် embedding layer သည် အနည်းဆုံး မဟုတ်ဘဲ
အဓိက memory အစိတ်အပိုင်း ဖြစ်လာနိုင်သည်။

```bash
python3 - <<'PY'
def matrix_mib(vocab, d_model, bits, tied):
    base = vocab * d_model * bits / 8 / 2 ** 20
    return base * (2 if tied else 1)


print("vocab    d_model   fp16 MiB   tied MiB")
for vocab in (32000, 50257, 128256):
    for d in (768, 4096):
        print(f"{vocab:>7}  {d:>7}  {matrix_mib(vocab, d, 16, False):9.2f}  "
              f"{matrix_mib(vocab, d, 16, True):9.2f}")
print("rows only (d_model 4096, fp16, untied):")
for vocab in (32000, 50257, 128256):
    print(f"vocab {vocab:>7}: {matrix_mib(vocab, 4096, 16, False):9.2f} MiB untied, "
          f"{matrix_mib(vocab, 4096, 16, True):9.2f} MiB tied")
big, small = 128256, 32000
print("memory ratio 128256 / 32000 =", round(big / small, 3))
print("int8 rows at 128256, d 4096:",
      round(matrix_mib(128256, 4096, 8, False), 2), "MiB")
PY
```

```text
vocab    d_model   fp16 MiB   tied MiB
  32000      768      46.88      93.75
  32000     4096     250.00     500.00
  50257      768      73.62     147.24
  50257     4096     392.63     785.27
 128256      768     187.88     375.75
 128256     4096    1002.00    2004.00
rows only (d_model 4096, fp16, untied):
vocab   32000:    250.00 MiB untied,    500.00 MiB tied
vocab   50257:    392.63 MiB untied,    785.27 MiB tied
vocab  128256:   1002.00 MiB untied,   2004.00 MiB tied
memory ratio 128256 / 32000 = 4.008
int8 rows at 128256, d 4096: 501.0 MiB
```

### ဥပမာ ၃ — Training batch တစ်ခုတွင် ပါဝင်သည့် token အရေအတွက်

**ယူဆချက် —** batch အရွယ်အစား 8၊ sequence အရှည်များ = [512, 384, 256, 768, 640, 128, 900, 448]။
padding ကို အရှည်ဆုံး sequence အထိ ဖြည့်သည်ဟု ယူဆသည် (row တစ်ခုစီအတွက် မဟုတ်ဘဲ
batch တစ်ခုလုံးအတွက် အရှည်တူ padding)။

**ဖော်မြူလာ —**
- padded token = batch အရွယ်အစား × အရှည်ဆုံး sequence
- padding အလွင့် = padded token − အမှန်တကယ် token ပေါင်းလဒ်
- utilisation = အမှန်တကယ် token / padded token

**တွက်ချက်မှု —**
1. အရှည်ဆုံး sequence = 900 ဖြစ်သည်။
2. padded token = 8 × 900 = 7,200 ဖြစ်သည်။
3. အမှန်တကယ် token = 512+384+256+768+640+128+900+448 = 4,036 ဖြစ်သည်။
4. padding အလွင့် = 7,200 − 4,036 = 3,164 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 43.9 % ဖြစ်သည်။
5. utilisation = 4,036 / 7,200 = 56.1 % ဖြစ်သည်။
6. packing ဖြင့် အရှည် 1,024 ရှိသည့် sequence 7.031 ခု လိုအပ်သည်။

**ကောက်ချက် —** padding သည် attention score matrix ၏ အရွယ်အစားကို
အရှည်ဆုံး sequence အပေါ် မူတည်စေသည်၊ ထို့ကြောင့် အလွင့်သည် compute နှင့် memory
နှစ်ခုလုံးတွင် ဖြစ်ပေါ်သည်။ packing သည် ဤ အလွင့်ကို ဖယ်ရှားပေးသော်လည်း နမူနာ
နယ်နိမိတ် ရောထွေးမှုကို ထည့်သွင်း စဉ်းစားရမည်။

```bash
python3 - <<'PY'
LENGTHS = [512, 384, 256, 768, 640, 128, 900, 448]
padded = max(LENGTHS) * len(LENGTHS)
real = sum(LENGTHS)
waste = padded - real
print("sequence lengths      ", LENGTHS)
print("batch size            ", len(LENGTHS))
print("longest sequence      ", max(LENGTHS))
print("padded tokens (batch) ", padded)
print("real tokens           ", real)
print("padding tokens        ", waste)
print("padding share pct     ", round(100 * waste / padded, 1))
print("utilisation pct       ", round(100 * real / padded, 1))
print("packed sequences needed", round(padded / 1024, 3), "of length 1024")
print("tokens per example avg", round(real / len(LENGTHS), 1))
PY
```

```text
sequence lengths       [512, 384, 256, 768, 640, 128, 900, 448]
batch size             8
longest sequence       900
padded tokens (batch)  7200
real tokens            4036
padding tokens         3164
padding share pct      43.9
utilisation pct        56.1
packed sequences needed 7.031 of length 1024
tokens per example avg 504.5
```

### ဥပမာ ၄ — Split အရွယ်အစားနှင့် leakage

**ယူဆချက် —** dataset တွင် နမူနာ 500,000 ရှိသည်၊ user 2,500 ဦး တစ်ဦးလျှင် record 200 ခု။
split အချိုး 80/10/10။ row ကို ကျပန်း ခွဲခြားသည့် နည်းလမ်းနှင့် user အလိုက် ခွဲခြားသည့်
နည်းလမ်းကို နှိုင်းယှဉ်သည်။ ထို့အပြင် test နမူနာ၏ 3 % တွင် train ထဲ အနီးစပ်ဆုံး တူညီသည့်
နမူနာ ရှိသည်ဟု ယူဆသည်။

**ဖော်မြူလာ —**
- split အရေအတွက် = နမူနာ စုစုပေါင်း × အချိုး
- row ကျပန်း ခွဲခြားသည့် အခါ P(user တွင် train row မရှိ) = (1 − train အချိုး)^(record အရေအတွက်)
- ယိုစိမ့်သည့် test row = test row × (1 − P(user တွင် train row မရှိ))

**တွက်ချက်မှု —**
1. row ကျပန်း split = train 400,000၊ validation 50,000၊ test 50,000 ဖြစ်သည်။
2. P(user တွင် train row မရှိ) = 0.2^200 = 1.61 × 10⁻¹⁴⁰ ဖြစ်သည်၊ ဆိုလိုသည်မှာ လက်တွေ့တွင်
   သုည ဖြစ်သည်။
3. ထို့ကြောင့် ယိုစိမ့်သည့် test row = 50,000 × (1 − 1.61 × 10⁻¹⁴⁰) = 50,000 ဖြစ်သည်၊
   ဆိုလိုသည်မှာ test set ထဲ ရှိသည့် row တိုင်း၏ user သည် train set ထဲ ရှိပြီး ဖြစ်သည်။
   လုံးဝ လွတ်လပ်သည့် test row = 0 ခု ဖြစ်သည်။
4. user အလိုက် ခွဲခြားပါက train user 2,000 (နမူနာ 400,000)၊ validation user 250 (နမူနာ 50,000)၊
   test user 250 (နမူနာ 50,000) ဖြစ်သည်၊ ယိုစိမ့်သည့် row = 0 ခု ဖြစ်သည်။
5. အနီးစပ်ဆုံး တူညီသည့် နမူနာ ဖြတ်ကျော်မှု = 50,000 × 3 % = 1,500 row ဖြစ်သည်။
   ဆိုလိုသည်မှာ test set ၏ 3.0 % ဖြစ်သည်။

**ကောက်ချက် —** အရေအတွက် လုံးဝ တူညီသော်လည်း row ကျပန်း split သည် **လွတ်လပ်မှု လုံးဝ
မရှိ** ပါ။ split ကို ခွဲသည့် ယူနစ် (user၊ repository၊ organization၊ အချိန်) က
evaluation ၏ အဓိပ္ပာယ်ကို ဆုံးဖြတ်သည်။ `Data Deduplication` က ထပ်မံ၍ အနီးစပ်ဆုံး
တူညီသည့် နမူနာများကို ရှာဖွေဖယ်ရှားခြင်းဖြင့် ကျန်သည့် ယိုစိမ့်မှုကို ပိတ်သည်။

```bash
python3 - <<'PY'
examples = 500_000
users = 2_500
per_user = examples // users
train_frac = 0.8
test_rows = int(examples * 0.1)
p_no_train = (1 - train_frac) ** per_user
leaky_rows = test_rows * (1 - p_no_train)
print("examples              ", examples)
print("users                 ", users)
print("records per user      ", per_user)
print("P(user has no train row)", p_no_train)
print("test rows             ", test_rows)
print("leaky test rows (random split)", round(leaky_rows))
print("clean test rows (random split)", round(test_rows - leaky_rows))
print("leaky share pct       ", round(100 * leaky_rows / test_rows, 2))
print("group split train     ", int(examples * train_frac))
print("group split val       ", int(examples * 0.1))
print("group split test      ", int(examples * 0.1))
print("leaky rows (group split)", 0)
near_dup_share = 0.03
print("near-duplicate crossing at 3 pct:", int(test_rows * near_dup_share), "rows")
print("contaminated test pct           ",
      round(100 * test_rows * near_dup_share / test_rows, 2))
PY
```

```text
examples               500000
users                  2500
records per user       200
P(user has no train row) 1.606938044258919e-140
test rows              50000
leaky test rows (random split) 50000
clean test rows (random split) 0
leaky share pct        100.0
group split train      400000
group split val        50000
group split test       50000
leaky rows (group split) 0
near-duplicate crossing at 3 pct: 1500 rows
contaminated test pct            3.0
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ
ရှင်းလင်းချက်ကို အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — Corpus တစ်ခုအတွက် token အရေအတွက်နှင့် ကုန်ကျစရိတ်**

စာတမ်း 4,000 ခု၊ တစ်ခုလျှင် စကားလုံး 750 လုံး၊ character-to-token ratio ကို
အင်္ဂလိပ် အတွက် 1.30 token/word၊ မြန်မာ အတွက် 3.00 token/word ဟု ယူဆသည်။ input token
သန်း တစ်သန်းလျှင် USD 2.50။ တွက်ရမည့် အချက်များ — (က) ဘာသာစကား တစ်မျိုးစီအတွက်
စာတမ်း တစ်ခုလျှင် token၊ (ခ) စုစုပေါင်း token၊ (ဂ) ကုန်ကျစရိတ်၊ (ဃ) token အချိုး၊
(င) မြန်မာ ratio အပေါ် ထပ်တိုးလာသည့် token အရေအတွက်။

**လေ့ကျင့်ခန်း ၂ — Vocabulary အရွယ်အစားနှင့် embedding memory**

vocabulary 50,257၊ d_model 4096၊ fp16။ (က) untied embedding matrix MiB၊ (ခ) weight tying ပါ
ထည့်ပါက MiB၊ (ဂ) vocabulary 32,000 သို့ လျှော့ပါက untied MiB နှင့် memory အချိုး၊
(ဃ) int8 ဖြင့် သိမ်းပါက MiB၊ (င) d_model ကို 8192 သို့ တိုးပါက untied fp16 MiB။

**လေ့ကျင့်ခန်း ၃ — Batch တစ်ခုတွင် ပါဝင်သည့် token အရေအတွက်**

batch အရွယ်အစား 16၊ sequence တိုင်းတွင် prompt 1,200 token နှင့် output 400 token။
(က) sequence တစ်ခုလျှင် token၊ (ခ) batch တစ်ခုလျှင် token၊ (ဂ) prompt ၏ ရာခိုင်နှုန်း၊
(ဃ) output ကို 1,200 အထိ တိုးပါက batch token၊ (င) attention score entry အရေအတွက်
(head တစ်ခုလျှင်) နှင့် head 32 ခုအတွက်။

**လေ့ကျင့်ခန်း ၄ — Split အရွယ်အစားနှင့် leakage ပြောင်းလဲမှု**

နမူနာ 1,000,000၊ split အချိုး 90/5/5၊ users 200,000 (တစ်ဦးလျှင် record 5 ခု)။
(က) split တစ်ခုစီ၏ အရေအတွက်၊ (ခ) test နမူနာ၏ 3 % တွင် train ထဲ အနီးစပ်ဆုံး တူညီသည့်
နမူနာ ရှိပါက ယိုစိမ့်သည့် row နှင့် သန့်ရှင်းသည့် row၊ (ဂ) row ကျပန်း ခွဲခြားပါက test row
မည်မျှသည် train ထဲ user တူညီသည့် row ရှိသည်၊ (ဃ) user အလိုက် ခွဲခြားပါက user အရေအတွက်၊
(င) split ကို 80/10/10 သို့ ပြောင်းပါက held-out နမူနာ အရေအတွက်။

**လေ့ကျင့်ခန်း ၅ — Deduplication နှုန်းနှင့် epoch အပေါ် သက်ရောက်မှု**

စာတမ်း 8,000,000၊ exact duplicate 10 %၊ near-duplicate 5 %၊ မူလ အစီအစဉ်တွင်
epoch 3 အတွက် budget သတ်မှတ်ထားသည်။ (က) ဖယ်ရှားသည့် စာတမ်းနှင့် ကျန်သည့် စာတမ်း၊
(ခ) epoch 3 တွင် doc pass အရေအတွက်၊ (ဂ) တူညီသည့် doc pass ရရှိရန် deduped set အပေါ်
epoch အရေအတွက်၊ (ဃ) epoch တိုးသည့် အချိုး နှင့် ရာခိုင်နှုန်း၊ (င) epoch တစ်ခုလျှင်
ထိရောက်သည့် နမူနာ အချိုး။

**လေ့ကျင့်ခန်း ၆ — Dataset တစ်ခု၏ storage**

token 20,000,000,000၊ vocabulary 50,257။ (က) token id ကို int32 ဖြင့် သိမ်းပါက GiB၊
(ခ) int16 ဖြင့် သိမ်းပါက GiB နှင့် ချွေတာသည့် GiB၊ (ဂ) int8 ဖြင့် GiB၊
(ဃ) vocabulary 128,256 ဖြစ်ပါက int16 သုံးနိုင်သလား၊ (င) token 600 လုံးပါသည့် စာတမ်း
အရေအတွက်။

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။

### ပြဿနာ ၁ — Validation loss သည် production တွင် ရရှိသည့် ရလဒ်ထက် အလွန် ကောင်းသည်

- **Symptom —** validation loss သည် နိမ့်ပြီး validation accuracy သည် မြင့်သည်၊ သို့သော်
  production တွင် တူညီသည့် task အပေါ် တိကျမှု သိသိသာသာ ကျဆင်းသည်။ Metric နှစ်ခုကြား
  ကွာဟမှုသည် ပြောင်းလဲမှု တစ်ခုခု လုပ်ပြီးနောက် ရုတ်တရက် ပေါ်လာသည်။
- **တိုင်းတာရမည့် အချက် —** split ကို မည်သည့် ယူနစ်အလိုက် ခွဲခဲ့သည်၊ validation set နှင့်
  train set အကြား အနီးစပ်ဆုံး တူညီသည့် နမူနာ အချိုး၊ preprocessing (normalization၊
  tokenizer) ကို split မတိုင်မီ fit လုပ်ခဲ့သလား၊ feature များတွင် timestamp သို့မဟုတ်
  target မှ ဆင်းသက်သည့် တန်ဖိုး ပါသလား၊ prompt များကို test label ဖြင့် ပြင်ခဲ့သလား။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) row ကို ကျပန်း ခွဲခြားသဖြင့် entity
  တစ်ခုတည်းမှ record များ နယ်နိမိတ်ကို ဖြတ်ကျော်ခြင်း၊ (၂) အနီးစပ်ဆုံး တူညီသည့် နမူနာများ
  နှစ်ဖက်စလုံးတွင် ပါဝင်ခြင်း၊ (၃) normalization statistic ကို dataset တစ်ခုလုံးအပေါ်
  တွက်၍ validation ထဲ ယိုစိမ့်ခြင်း၊ (၄) အနာဂတ် အချက်အလက် ပါသည့် feature များ သုံးခြင်း။
- **ဖြေရှင်းနည်း —** split ကို deployment ယူနစ် (user၊ repository၊ organization၊ အချိန်)
  အလိုက် ပြန်ခွဲရမည်၊ preprocessor များကို split ပြီးမှ fit လုပ်ရမည်၊ near-duplicate ကို
  split နှစ်ခုအကြား ရှာဖွေ ဖယ်ရှားရမည်၊ historical feature များမှ အနာဂတ် အချက်အလက်
  ဖယ်ရှားရမည်။
- **ရှင်းလင်းသည့် term —** Data Leakage, Dataset Split, Data Deduplication, Feature

### ပြဿနာ ၂ — မော်ဒယ်သည် benchmark တစ်ခုကို အလွတ်ကျက်မှတ်ထားသည်

- **Symptom —** benchmark အပေါ် ရမှတ် မြင့်မားသည်၊ သို့သော် အလားတူ မေးခွန်းကို စကားလုံး
  အနည်းငယ် ပြောင်း၍ မေးပါက တိကျမှု ရုတ်တရက် ကျဆင်းသည်။ မော်ဒယ်သည် ဖြေချက်
  စာကြောင်းကို ပြန်လည် ထုတ်ပေးသည့် ပုံစံ ရှိသည်။
- **တိုင်းတာရမည့် အချက် —** training corpus နှင့် benchmark ကြား n-gram overlap အချိုး၊
  benchmark မေးခွန်း နှင့် ဆင်တူသည့် နမူနာ ရှိမရှိ (exact နှင့် near-duplicate)၊
  benchmark ကို tuning loop တွင် ထပ်ခါတလဲလဲ သုံးခဲ့သလား၊ မော်ဒယ်သည် ဖြေချက်ကို
  စာလုံးအလိုက် ပြန်ထုတ်သည့် အချိုး။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) benchmark မေးခွန်းများ training corpus
  ထဲ ပါဝင်ခြင်း (benchmark contamination)၊ (၂) benchmark ၏ paraphrase များ training
  corpus ထဲ ရှိခြင်း၊ (၃) benchmark ဖြေချက်များကို prompt သို့မဟုတ် tuning data
  အဖြစ် အသုံးပြုခြင်း၊ (၄) training corpus ထဲ ထပ်တလဲလဲ ဖြစ်နေခြင်းကြောင့်
  memorization တိုးခြင်း။
- **ဖြေရှင်းနည်း —** benchmark နှင့် ဆင်တူသည့် နမူနာများကို training corpus မှ
  ဖယ်ရှားရမည်၊ exact hash နှင့် similarity နည်းလမ်းများဖြင့် deduplication လုပ်ပြီး
  မည်သည့် rule က မည်သည့် နမူနာကို ဖယ်ရှားခဲ့သည်ကို မှတ်တမ်းတင်ရမည်၊
  benchmark ကို သီးခြား ခွဲထားရမည်၊ မမြင်ဖူးသေးသည့် test set တစ်ခု ဖန်တီးရမည်။
- **ရှင်းလင်းသည့် term —** Data Deduplication, Data Leakage, Data Provenance, Dataset Split

### ပြဿနာ ၃ — Tokenizer သည် မြန်မာ၊ ထိုင်း သို့မဟုတ် code ကို ဆိုးရွားစွာ ခွဲခြမ်းသည်

- **Symptom —** မြန်မာ သို့မဟုတ် ထိုင်း စာသားတွင် token အရေအတွက်သည် များလွန်းသည်၊
  sequence အရှည်ကန့်သတ်ချက်ကို လျင်မြန်စွာ ရောက်သည်၊ ကုန်ကျစရိတ် မြင့်သည်။
  code ဖြင့် စမ်းသပ်ပါက identifier တစ်ခုသည် အစိတ်အပိုင်း များစွာ အဖြစ် ကွဲထွက်သည်။
- **တိုင်းတာရမည့် အချက် —** ဘာသာစကား တစ်မျိုးစီအတွက် character-to-token ratio၊
  token တစ်ခုလျှင် character အရေအတွက် ပျမ်းမျှ၊ encode-decode round trip သည်
  မူရင်း စာသားနှင့် တူညီမှု၊ whitespace နှင့် special token များ ခွဲခြမ်းသည့် ပုံစံ၊
  မမြင်ဖူးသည့် စကားလုံး တစ်ခုအတွက် byte fallback ဖြစ်ပေါ်မှု။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) tokenizer ကို အဓိက အင်္ဂလိပ်
  corpus အပေါ်တွင်သာ train လုပ်ခဲ့သဖြင့် မြန်မာ၊ ထိုင်း အတွက် merge rule မလုံလောက်ခြင်း၊
  (၂) vocabulary သေးလွန်း၍ ထို ဘာသာစကား၏ ယူနစ်များ မပါဝင်ခြင်း၊
  (၃) code အတွက် identifier နှင့် punctuation ခွဲခြမ်း စည်းမျဉ်း မသင့်လျော်ခြင်း၊
  (၄) အခြား tokenizer တစ်ခု၏ weight နှင့် တွဲသုံးခြင်း (token name ဆင်တူရုံမျှဖြင့်)။
- **ဖြေရှင်းနည်း —** ဘာသာစကား တိုင်း ပါဝင်သည့် corpus အပေါ် tokenizer ကို အသစ် train
  လုပ်ရမည်၊ vocabulary အရွယ်အစားကို ပြန်ရွေးရမည်၊ multilingual text၊ code၊ whitespace နှင့်
  special token များကို စမ်းသပ်ရမည်၊ tokenizer ကို model weight နှင့်တကွ version မှတ်ရမည်။
- **ရှင်းလင်းသည့် term —** Tokenization, Token, Vocabulary, Byte Pair Encoding (BPE), Data Provenance

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — Vocabulary အရွယ်အစား ရွေးချယ်ခြင်း

**အခြေအနေ —** မော်ဒယ် တစ်ခုကို အင်္ဂလိပ်၊ မြန်မာ နှင့် code တို့ ပါဝင်သည့် training corpus
အပေါ် train လုပ်မည်။ ရွေးချယ်စရာ နှစ်ခု ရှိသည် — ရွေးချယ်မှု A သည် vocabulary 32,000
(အင်္ဂလိပ် အဓိက)၊ ရွေးချယ်မှု B သည် vocabulary 128,256 (multilingual)။ d_model 4096၊
fp16၊ weight tying ရှိသည်။

**trade-off —** A သည် embedding memory 500.00 MiB လိုအပ်သည်၊ B သည် 2004.00 MiB —
ဆိုလိုသည်မှာ 4.008 ဆ ဖြစ်သည်။ သို့သော် B သည် မြန်မာ နှင့် ထိုင်း စာသားအတွက်
sequence အရှည်ကို လျှော့ချနိုင်သည်၊ ထို့ကြောင့် attention compute နှင့် ကုန်ကျစရိတ်
လျော့သည်။ A တွင် မြန်မာ စာသားသည် byte fallback အဖြစ် ကွဲထွက်ပြီး token အရေအတွက်
အလွန်များလာသည်။

**ဆုံးဖြတ်ချက် —** B (128,256) ကို ရွေးရမည်၊ အကြောင်းမှာ multilingual corpus တွင်
sequence အရှည် လျော့ချမှုသည် training အချိန်နှင့် attention memory ကို လျှော့ပေးပြီး
ထို အကျိုးအမြတ်သည် embedding memory 1504 MiB ထပ်တိုးမှုကို ကျော်လွန်သည်။
သို့သော် ဘာသာစကား တစ်မျိုးတည်း (အင်္ဂလိပ်) ဖြစ်ပါက A ကို ရွေးရမည်။ ဤ ဆုံးဖြတ်ချက်
သည် ဘာသာစကား တိုင်းအတွက် character-to-token ratio ကို တိုင်းတာသည့် အပေါ်တွင်သာ
ခိုင်လုံသည်။

**တိုင်းတာမည့် metric —** ဘာသာစကား တစ်မျိုးစီအတွက် token တစ်ခုလျှင် character
အရေအတွက်၊ sequence အရှည် p95၊ embedding memory MiB၊ ကုန်ကျစရိတ်နှင့်
task အပေါ် တိကျမှု။

### ဆုံးဖြတ်ချက် ၂ — Deduplication ကို မည်မျှ တင်းကြပ်စွာ လုပ်မည်နည်း

**အခြေအနေ —** စာတမ်း 8,000,000 ရှိသည့် corpus တွင် exact duplicate 10 %၊
near-duplicate 5 % တိုင်းတာရရှိသည်။ လိုအပ်သည့် လေ့ကျင့်မှု doc pass သည် 24,000,000
(မူလ အစီအစဉ်တွင် epoch 3)။ ရွေးချယ်စရာ နှစ်ခု — ရွေးချယ်မှု A သည် exact duplicate သာ
ဖယ်ရှားသည်၊ ရွေးချယ်မှု B သည် exact နှင့် near-duplicate နှစ်မျိုးလုံး ဖယ်ရှားသည်။

**trade-off —** A တွင် ကျန်သည့် စာတမ်း 7,200,000 ဖြစ်သည်၊ B တွင် 6,800,000 ဖြစ်သည်။
B သည် data 5.6 % ပိုဖယ်ရှားသည်၊ သို့သော် near-duplicate သည် training distribution ကို
ပျက်စီးစေခြင်း၊ memorization တိုးစေခြင်းနှင့် test material ယိုစိမ့်စေခြင်း တို့ကို
ဖြစ်စေသည်။ B တွင် တူညီသည့် doc pass ရရှိရန် epoch သည် 3.5294 သို့ တိုးသည်
(17.65 % တိုးသည်)။

**ဆုံးဖြတ်ချက် —** B ကို ရွေးရမည်၊ သို့သော် borderline cluster များကို လူက
ပြန်လည် စစ်ဆေးရမည်။ အကြောင်းမှာ near-duplicate ဖယ်ရှားခြင်းသည် evaluation ၏
ယုံကြည်စိတ်ချရမှုကို ဝယ်ယူပြီး၊ ထို ယုံကြည်စိတ်ချရမှု မရှိပါက မည်သည့် ရလဒ်ကိုမျှ
ဆုံးဖြတ်ချက် အတွက် အသုံးမပြုနိုင်ပါ။ မတူညီသည့် record နှစ်ခုသည် စာသား တူညီစွာ
ရှိနိုင်သဖြင့် ဖယ်ရှားမှု တိုင်းကို rule id ဖြင့် မှတ်တမ်းတင်ရမည်။

**တိုင်းတာမည့် metric —** ဖယ်ရှားသည့် နမူနာ အရေအတွက်နှင့် နှုန်း၊ ကျန်သည့် corpus
အရေအတွက်၊ benchmark နှင့် ဆင်တူသည့် နမူနာ ရှိမရှိ၊ doc pass တစ်ခုလျှင်
validation loss၊ epoch အရေအတွက်နှင့် ကုန်ကျစရိတ်။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — Corpus တစ်ခုအတွက် token အရေအတွက်နှင့် ကုန်ကျစရိတ်

**ဖော်မြူလာ —** token စုစုပေါင်း = စာတမ်း အရေအတွက် × စကားလုံး/စာတမ်း × token/word၊
ကုန်ကျစရိတ် = token စုစုပေါင်း / 10⁶ × USD per million။ ယူဆချက် — ratio သည် corpus တစ်ခုလုံး
အတွက် တူညီသည်၊ input token သာ ရေတွက်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. အင်္ဂလိပ်: စာတမ်း တစ်ခုလျှင် token = 750 × 1.30 = 975 ဖြစ်သည်။
2. အင်္ဂလိပ် စုစုပေါင်း = 4,000 × 975 = 3,900,000 token ဖြစ်သည်။
3. အင်္ဂလိပ် ကုန်ကျစရိတ် = 3,900,000 / 10⁶ × 2.50 = USD 9.7500 ဖြစ်သည်။
4. မြန်မာ: စာတမ်း တစ်ခုလျှင် token = 750 × 3.00 = 2,250 ဖြစ်သည်။
5. မြန်မာ စုစုပေါင်း = 4,000 × 2,250 = 9,000,000 token ဖြစ်သည်။
6. မြန်မာ ကုန်ကျစရိတ် = 9,000,000 / 10⁶ × 2.50 = USD 22.5000 ဖြစ်သည်။
7. token အချိုး = 3.00 / 1.30 = 2.31 ဖြစ်သည်၊ ထပ်တိုးလာသည့် token = 5,100,000 ဖြစ်သည်။

**အဓိပ္ပာယ် —** တူညီသည့် စကားလုံး အရေအတွက် အတွက် မြန်မာ သည် အင်္ဂလိပ်ထက်
token 2.31 ဆ လိုအပ်သည်၊ ထို့ကြောင့် ကုန်ကျစရိတ် လည်း ထိုအချိုးအတိုင်း တိုးသည်။
ဤအချက်သည် character-to-token ratio သည် ဘာသာစကား၊ content နှင့် tokenizer အလိုက်
ကွာခြားသည့် အချက်၏ ကိန်းဂဏန်း အသွင်အပြင် ဖြစ်သည်။

```bash
python3 - <<'PY'
docs = 4000
words_per_doc = 750
price_per_million = 2.50
for label, ratio in (("English", 1.30), ("Burmese", 3.00)):
    tokens_per_doc = words_per_doc * ratio
    total = docs * tokens_per_doc
    print(f"{label}: tokens per document {tokens_per_doc:.0f}, total {total:.0f}, "
          f"USD {total / 1e6 * price_per_million:.4f}")
print("token ratio English to Burmese =", round(3.00 / 1.30, 2))
print("extra tokens at Burmese ratio  =",
      docs * words_per_doc * 3.00 - docs * words_per_doc * 1.30)
PY
```

```text
English: tokens per document 975, total 3900000, USD 9.7500
Burmese: tokens per document 2250, total 9000000, USD 22.5000
token ratio English to Burmese = 2.31
extra tokens at Burmese ratio  = 5100000.0
```

#### အဖြေ ၂ — Vocabulary အရွယ်အစားနှင့် embedding memory

**ဖော်မြူလာ —** bytes = vocabulary × d_model × element byte၊ weight tying ရှိပါက × 2။
ယူဆချက် — fp16 ဖြစ်၍ element တစ်ခုလျှင် 2 byte၊ int8 ဖြစ်ပါက 1 byte၊ metadata အပိုအလွှာ
မပါပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. vocabulary 50,257၊ d_model 4096၊ fp16၊ untied = 392.63 MiB ဖြစ်သည်။
2. tied = 392.63 × 2 = 785.27 MiB ဖြစ်သည်။
3. vocabulary 32,000၊ untied = 250.00 MiB ဖြစ်သည်၊ ထို့ကြောင့် memory အချိုး =
   392.63 / 250.00 = 1.571 ဖြစ်သည်။
4. int8 ဖြင့် 50,257၊ 4096 = 196.31 MiB (untied) ဖြစ်သည်၊ ဆိုလိုသည်မှာ fp16 ၏ ထက်ဝက် ဖြစ်သည်။
5. d_model 8192 ဖြစ်ပါက untied fp16 = 392.63 × 2 = 785.27 MiB ဖြစ်သည်။

**အဓိပ္ပာယ် —** embedding memory သည် vocabulary နှင့် d_model နှစ်ခုလုံးအပေါ်
တိုက်ရိုက် အချိုးကျသည်။ ထို့ကြောင့် d_model နှစ်ဆ ဖြစ်ခြင်းနှင့် vocabulary နှစ်ဆ ဖြစ်ခြင်းသည်
memory အပေါ် တူညီသည့် သက်ရောက်မှု ရှိသည်။

```bash
python3 - <<'PY'
def matrix_mib(vocab, d_model, bits, tied):
    base = vocab * d_model * bits / 8 / 2 ** 20
    return base * (2 if tied else 1)


print("vocab 50257 d 4096 fp16 untied", round(matrix_mib(50257, 4096, 16, False), 2), "MiB")
print("vocab 50257 d 4096 fp16 tied  ", round(matrix_mib(50257, 4096, 16, True), 2), "MiB")
print("vocab 32000 d 4096 fp16 untied", round(matrix_mib(32000, 4096, 16, False), 2), "MiB")
print("ratio 50257 / 32000          ", round(50257 / 32000, 3))
print("vocab 50257 d 4096 int8 untied", round(matrix_mib(50257, 4096, 8, False), 2), "MiB")
print("vocab 50257 d 8192 fp16 untied", round(matrix_mib(50257, 8192, 16, False), 2), "MiB")
PY
```

```text
vocab 50257 d 4096 fp16 untied 392.63 MiB
vocab 50257 d 4096 fp16 tied   785.27 MiB
vocab 32000 d 4096 fp16 untied 250.0 MiB
ratio 50257 / 32000           1.571
vocab 50257 d 4096 int8 untied 196.31 MiB
vocab 50257 d 8192 fp16 untied 785.27 MiB
```

#### အဖြေ ၃ — Batch တစ်ခုတွင် ပါဝင်သည့် token အရေအတွက်

**ဖော်မြူလာ —** sequence တစ်ခုလျှင် token = prompt + output၊ batch token = batch အရွယ်အစား ×
sequence တစ်ခုလျှင် token၊ attention score entry = batch × sequence အရှည်² × head အရေအတွက်။
ယူဆချက် — padding မရှိ၊ sequence အားလုံး အရှည်တူ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. sequence တစ်ခုလျှင် token = 1,200 + 400 = 1,600 ဖြစ်သည်။
2. batch token = 16 × 1,600 = 25,600 ဖြစ်သည်။
3. prompt ၏ ရာခိုင်နှုန်း = 1,200 / 1,600 = 75.0 % ဖြစ်သည်။
4. output ကို 1,200 သို့ တိုးပါက batch token = 16 × 2,400 = 38,400 ဖြစ်သည်။
5. attention score row (head တစ်ခုလျှင်) = 16 × 1,600² = 40,960,000 ဖြစ်သည်။
6. head 32 ခုအတွက် score entry = 40,960,000 × 32 = 1,310,720,000 ဖြစ်သည်။

**အဓိပ္ပာယ် —** batch token အရေအတွက်သည် tokenization ၏ ရလဒ် ဖြစ်သည်၊ ထို့ကြောင့်
tokenizer ပြောင်းပါက ဤ ကိန်းဂဏန်း ပြောင်းသည်။ attention score entry သည် sequence
အရှည် အပေါ် နှစ်ထပ်ကိန်း အချိုးကျ ကြီးထွားသည် — ထို့ကြောင့် မြန်မာ စာသားတွင်
token အရေအတွက် တိုးခြင်းသည် compute အပေါ် ဆိုးရွားစွာ သက်ရောက်သည်။

```bash
python3 - <<'PY'
batch, prompt, output = 16, 1200, 400
per = prompt + output
total = batch * per
print("tokens per sequence", per)
print("tokens per batch   ", total)
print("prompt share pct   ", round(100 * prompt / per, 1))
print("if output were 1200", batch * (prompt + 1200))
print("attention score rows per head",
      batch * per * per)
print("score entries if 32 heads", batch * per * per * 32)
PY
```

```text
tokens per sequence 1600
tokens per batch    25600
prompt share pct    75.0
if output were 1200 38400
attention score rows per head 40960000
score entries if 32 heads 1310720000
```

#### အဖြေ ၄ — Split အရွယ်အစားနှင့် leakage ပြောင်းလဲမှု

**ဖော်မြူလာ —** split အရေအတွက် = နမူနာ စုစုပေါင်း × အချိုး၊ ယိုစိမ့်သည့် row =
test row × near-duplicate အချိုး။ ယူဆချက် — users 200,000 တစ်ဦးလျှင် record 5 ခု
(ထို့ကြောင့် ကျပန်း ခွဲခြားပါက user တိုင်းတွင် train row ရှိသည်)။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. train = 1,000,000 × 0.90 = 900,000 ဖြစ်သည်။
2. validation = test = 1,000,000 × 0.05 = 50,000 ဖြစ်သည်။
3. near-duplicate ဖြတ်ကျော်မှု = 50,000 × 3 % = 1,500 row ဖြစ်သည်၊ ဆိုလိုသည်မှာ
   ယိုစိမ့်သည့် row 1,500 နှင့် သန့်ရှင်းသည့် row 48,500 ဖြစ်သည်။
4. row ကျပန်း ခွဲခြားပါက test row 50,000 တိုင်း၏ user သည် train ထဲ ရှိသည် (record 5 ခုအနက်
   အနည်းဆုံး တစ်ခု train ထဲ ပါဝင်သည့် ဖြစ်နိုင်ခြေ ~1)၊ ထို့ကြောင့် ယိုစိမ့်မှု 100 % ဖြစ်သည်။
5. user အလိုက် ခွဲခြားပါက train user 180,000၊ validation user 10,000၊ test user 10,000 ဖြစ်သည်။
6. split ကို 80/10/10 သို့ ပြောင်းပါက held-out နမူနာ = 200,000 ဖြစ်သည်၊ ဆိုလိုသည်မှာ
   90/5/5 ၏ 100,000 ထက် 2 ဆ ဖြစ်သည်။

**အဓိပ္ပာယ် —** hold-out အရေအတွက် တိုးခြင်းသည် နယ်နိမိတ် ဖြတ်ကျော်မှုကို မဖြေပါ။
ဖြေသည့် တစ်ခုတည်းသော နည်းလမ်းမှာ ခွဲခြားသည့် ယူနစ်ကို ပြောင်းခြင်း ဖြစ်သည်။

```bash
python3 - <<'PY'
examples = 1_000_000
splits = {"train": 0.90, "validation": 0.05, "test": 0.05}
for name, share in splits.items():
    print(f"{name:>10}: {int(examples * share):>9}")
test = int(examples * splits["test"])
near = 0.03
crossing = int(test * near)
print("test rows               ", test)
print("near-duplicate crossing rows", crossing)
print("clean test rows         ", test - crossing)
print("contaminated share pct  ", round(100 * crossing / test, 2))
print("if split were 80/10/10  ", int(examples * 0.2), "held-out of",
      int(examples))
print("entity split: 200,000 users x 5 records")
users = 200_000
print("train users", int(users * 0.9), "val users", int(users * 0.05),
      "test users", int(users * 0.05))
print("leaky test rows under random split (same user in train):",
      test)
PY
```

```text
     train:    900000
validation:     50000
      test:     50000
test rows                50000
near-duplicate crossing rows 1500
clean test rows          48500
contaminated share pct   3.0
if split were 80/10/10   200000 held-out of 1000000
entity split: 200,000 users x 5 records
train users 180000 val users 10000 test users 10000
leaky test rows under random split (same user in train): 50000
```

#### အဖြေ ၅ — Deduplication နှုန်းနှင့် epoch အပေါ် သက်ရောက်မှု

**ဖော်မြူလာ —** ကျန်သည့် စာတမ်း = စာတမ်း × (1 − ဖယ်ရှားသည့် အချိုး)၊ doc pass = စာတမ်း × epoch၊
deduped set အပေါ် epoch = doc pass / ကျန်သည့် စာတမ်း။ ယူဆချက် — စာတမ်း တိုင်း ပျမ်းမျှ token
တူညီသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. ဖယ်ရှားသည့် အချိုး = 0.10 + 0.05 = 0.15 ဖြစ်သည်၊ ဖယ်ရှားသည့် စာတမ်း = 1,200,000 ဖြစ်သည်။
2. ကျန်သည့် စာတမ်း = 8,000,000 − 1,200,000 = 6,800,000 ဖြစ်သည်။
3. epoch 3 အတွက် doc pass = 8,000,000 × 3 = 24,000,000 ဖြစ်သည်။
4. deduped set အပေါ် epoch = 24,000,000 / 6,800,000 = 3.5294 ဖြစ်သည်။
5. တိုးသည့် အချိုး = 3.5294 / 3 = 1.1765 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 17.65 % ဖြစ်သည်။
6. epoch တစ်ခုလျှင် ထိရောက်သည့် နမူနာ အချိုး = 6,800,000 / 8,000,000 = 0.85 ဖြစ်သည်။

**အဓိပ္ပာယ် —** deduplication လုပ်ပါက တူညီသည့် doc pass ရရှိရန် epoch ပိုလိုအပ်သည်၊
ထို့ကြောင့် ကုန်ကျစရိတ် တိုးသည်။ အကျိုးအမြတ်မှာ training distribution သန့်ရှင်းခြင်း၊
memorization လျော့ခြင်းနှင့် evaluation ယုံကြည်စိတ်ချရမှု ဖြစ်သည် — ဤ လဲလှယ်မှုကို
ကိန်းဂဏန်းဖြင့် တွက်ပြီးမှ ဆုံးဖြတ်ရမည်။

```bash
python3 - <<'PY'
docs = 8_000_000
exact, near = 0.10, 0.05
removed = int(docs * (exact + near))
kept = docs - removed
budget = 3
passes = docs * budget
print("documents        ", docs)
print("removed documents", removed)
print("kept documents   ", kept)
print("doc passes at 3 epochs", passes)
print("epochs over deduped set", round(passes / kept, 4))
print("increase factor  ", round((passes / kept) / budget, 4))
print("increase pct     ", round(100 * ((passes / kept) / budget - 1), 2))
print("effective unique tokens per epoch relative to before",
      round(kept / docs, 4))
PY
```

```text
documents         8000000
removed documents 1200000
kept documents    6800000
doc passes at 3 epochs 24000000
epochs over deduped set 3.5294
increase factor   1.1765
increase pct      17.65
effective unique tokens per epoch relative to before 0.85
```

#### အဖြေ ၆ — Dataset တစ်ခု၏ storage

**ဖော်မြူလာ —** bytes = token အရေအတွက် × integer width / 8၊ GiB = bytes / 2³⁰။
ယူဆချက် — token id ကို fixed-width integer ဖြင့် သိမ်းသည်၊ metadata အပိုအလွှာ မပါပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. int32: 20,000,000,000 × 32 / 8 = 80,000,000,000 byte = 74.51 GiB ဖြစ်သည်။
2. int16: 40,000,000,000 byte = 37.25 GiB ဖြစ်သည်၊ ချွေတာသည့် ပမာဏ = 37.25 GiB ဖြစ်သည်။
3. int8: 20,000,000,000 byte = 18.63 GiB ဖြစ်သည်။
4. vocabulary 50,257 သည် 65,536 အောက် ဖြစ်သဖြင့် int16 သုံးနိုင်သည်၊ vocabulary 128,256
   ဖြစ်ပါက int16 မလုံလောက်ဘဲ int32 လိုအပ်သည်။
5. token 600 လုံးပါသည့် စာတမ်း အရေအတွက် = 20,000,000,000 / 600 = 33,333,333 ဖြစ်သည်။

**အဓိပ္ပာယ် —** storage သည် **token အရေအတွက် နှင့် integer width** နှစ်ခုလုံးအပေါ်
တိုက်ရိုက် အချိုးကျသည်။ vocabulary ကို 65,536 အောက် ထိန်းထားနိုင်ပါက storage ကို
ထက်ဝက် လျှော့နိုင်သည် — ဤအချက်သည် tokenizer ၏ vocabulary ရွေးချယ်မှုနှင့်
dataset storage ကို ဆက်ပေးသည့် နေရာ ဖြစ်သည်။

```bash
python3 - <<'PY'
tokens = 20_000_000_000
for name, bits in (("int32", 32), ("int16", 16), ("int8", 8)):
    b = tokens * bits / 8
    print(f"{name}: {b:>16.0f} bytes = {b / 2 ** 30:7.2f} GiB")
print("int32 vs int16 saving GiB",
      round(20_000_000_000 * (32 - 16) / 8 / 2 ** 30, 2))
print("vocab 50257 fits int16:", 50257 < 65536)
print("vocab 128256 fits int16:", 128256 < 65536)
PY
```

```text
int32:      80000000000 bytes =   74.51 GiB
int16:      40000000000 bytes =   37.25 GiB
int8:      20000000000 bytes =   18.63 GiB
int32 vs int16 saving GiB 37.25
vocab 50257 fits int16: True
vocab 128256 fits int16: False
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — Validation ကောင်းသော်လည်း production တွင် ကျဆင်းခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** validation metric သည် **မည်သည့် အထောက်အထား** အပေါ်
တွက်ခဲ့သည် ဆိုသည့် အချက်က ၎င်း၏ အဓိပ္ပာယ်ကို ဆုံးဖြတ်သည်။ နမူနာ 500,000 တွင်
user တစ်ဦးလျှင် record 200 ခု ရှိပြီး row ကို ကျပန်း ခွဲခြားပါက test row တိုင်း၏ user သည်
train set ထဲ ရှိပြီး ဖြစ်သည် (အပိုင်း ၅.၁ အဖြေ ၄ တွင် တွက်ပြထားသည်)။ ထို့ကြောင့်
validation loss သည် "မြင်ဖူးပြီးသား entity အပေါ် ခန့်မှန်းမှု" ကို တိုင်းနေခြင်း ဖြစ်သည်။
Production တွင် entity အသစ် ရောက်လာသည့်အခါ ထို metric ပြိုလဲသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ဦးစွာ split ကို entity အလိုက် ပြန်ခွဲပြီး တူညီသည့် မော်ဒယ်ကို
ပြန်တိုင်းပါ။ Metric ကျဆင်းပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ မကျဆင်းပါက အနီးစပ်ဆုံး
တူညီသည့် နမူနာ အရေအတွက်ကို တိုင်းပါ — ရာခိုင်နှုန်း မြင့်ပါက အကြောင်းရင်း (၂) ဖြစ်သည်။
Normalization statistic ကို train subset အပေါ်တွင်သာ fit လုပ်ပြီး ပြန်တိုင်းပါ —
ပြောင်းလဲပါက အကြောင်းရင်း (၃) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** split ကို deployment ယူနစ်အလိုက် ပြောင်းပြီးနောက်
validation နှင့် production ၏ ကွာဟမှု ကျဉ်းလာပါက ဆုံးဖြတ်ချက် မှန်ကန်သည်။
ဆိုလိုသည်မှာ ဤပြဿနာသည် မော်ဒယ်၏ ပြဿနာ မဟုတ်ဘဲ **အထောက်အထား တည်ဆောက်သည့်
လုပ်ငန်းစဉ်၏ ပြဿနာ** ဖြစ်သည်။

#### အဖြေ ၂ — Benchmark ကို အလွတ်ကျက်မှတ်ထားခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** training corpus သည် web မှ စုဆောင်းထားသည့် data ဖြစ်ပါက
benchmark ၏ မေးခွန်း နှင့် ဖြေချက် များလည်း ထို corpus ထဲ ပါဝင်နိုင်သည်။
ထပ်တလဲလဲ ဖြစ်နေခြင်းသည် memorization ကို တိုးစေသည် — အပိုင်း ၅.၁ အဖြေ ၅ တွင်
near-duplicate 5 % ဖယ်ရှားခြင်းဖြင့် epoch 17.65 % တိုးသည်ကို တွက်ပြထားသည်၊ ဆိုလိုသည်မှာ
ထပ်တလဲလဲ ဖြစ်နေခြင်းသည် **တကယ် ကုန်ကျစရိတ် ရှိသည့်** အရာ ဖြစ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** benchmark မေးခွန်းများနှင့် training corpus ကြား exact hash
တိုက်စစ်ပါ။ exact match ရှိပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ မရှိဘဲ similarity အချိုး
မြင့်ပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ Tuning data ထဲ benchmark ဖြေချက် ပါသလား စစ်ပါ —
ပါပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ Corpus ထဲ ထပ်တလဲလဲ ဖြစ်နေသည့် အချိုးကို တိုင်းပါ —
မြင့်ပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** contaminated နမူနာများကို ဖယ်ရှားပြီးနောက် benchmark ရမှတ်
ကျဆင်းသော်လည်း မမြင်ဖူးသေးသည့် test set အပေါ် ရမှတ်သည် တည်ငြိမ်စွာ ရှိပါက
ဆုံးဖြတ်ချက် မှန်ကန်သည်။ မည်သည့် rule က မည်သည့် နမူနာကို ဖယ်ရှားခဲ့သည်ကို
မှတ်တမ်းတင်ထားခြင်းဖြင့် နောက်တစ်ကြိမ် တူညီသည့် စစ်ဆေးမှုကို ပြန်လုပ်နိုင်သည်။

#### အဖြေ ၃ — Tokenizer သည် မြန်မာ၊ ထိုင်း သို့မဟုတ် code ကို ဆိုးရွားစွာ ခွဲခြမ်းခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** `Byte Pair Encoding (BPE)` သည် merge rule ကို training corpus ၏
frequency အပေါ် တည်ဆောက်သည်။ Corpus တွင် အဓိက အင်္ဂလိပ် စာသား ပါဝင်ပါက မြန်မာ သို့မဟုတ်
ထိုင်း အတွက် merge rule ဖြစ်ပေါ်မည် မဟုတ်သလို၊ ထို ဘာသာစကား၏ ယူနစ်များသည်
vocabulary ထဲ မဝင်နိုင်ပါ။ ရလဒ်မှာ character-to-token ratio မြင့်မားခြင်း ဖြစ်သည် —
အပိုင်း ၅.၁ အဖြေ ၁ တွင် မြန်မာ သည် အင်္ဂလိပ်ထက် token 2.31 ဆ လိုအပ်သည်ကို
တွက်ပြထားသည်။ Token အရေအတွက် တိုးပါက sequence အရှည် တိုးသည်၊ attention compute
နှစ်ထပ်ကိန်း တိုးသည်၊ ကုန်ကျစရိတ် တိုးသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** ဘာသာစကား တစ်မျိုးစီအတွက် token တစ်ခုလျှင် character
အရေအတွက် ကို တိုင်းပါ။ မြန်မာ အတွက် အလွန်နည်းပါက (၁) (၂) ဖြစ်သည်။
Code identifier တစ်ခုသည် အစိတ်အပိုင်း များစွာ ကွဲထွက်ပါက (၃) ဖြစ်သည်။
Encode-decode round trip မတူညီပါက သို့မဟုတ် token name ဆင်တူသည့် အခြား tokenizer
တစ်ခုကို အသုံးပြုခဲ့ပါက (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** tokenizer အသစ်တွင် မြန်မာ၊ ထိုင်း နှင့် code အတွက်
character-to-token ratio ကျဆင်းပြီး encode-decode round trip မှန်ကန်ပါက ဆုံးဖြတ်ချက်
မှန်ကန်သည်။ Tokenizer ၏ merge rule နှင့် special-token သတ်မှတ်ချက်ကို model weight
နှင့်တကွ version မှတ်ရမည် — မှတ်မထားပါက နောက်တစ်ကြိမ် တူညီသည့် ရလဒ်ကို
ပြန်လည် ဖန်တီးနိုင်မည် မဟုတ်ပါ။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — Vocabulary အရွယ်အစား

**ရှင်းလင်းချက် —** vocabulary 32,000 မှ 128,256 သို့ တိုးပါက embedding matrix သည်
4.008 ဆ ဖြစ်သည် (အပိုင်း ၅.၁ အဖြေ ၂ နှင့် ဥပမာ ၂ တွင် တွက်ပြထားသည်)။
d_model 4096၊ fp16၊ tied ဖြစ်ပါက 500.00 MiB မှ 2004.00 MiB သို့ တက်သည်၊ ဆိုလိုသည်မှာ
1504 MiB ထပ်တိုးသည်။ ထို ပမာဏသည် မော်ဒယ် ကြီးတစ်ခုတွင် memory ၏ အစိတ်အပိုင်း
အနည်းငယ်သာ ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** multilingual corpus အတွက် 128,256 ကို ရွေးရမည်၊ အကြောင်းမှာ
မြန်မာ နှင့် ထိုင်း စာသားအတွက် sequence အရှည် လျော့ချမှုသည် training အချိန်နှင့်
attention memory ကို လျှော့ပေးသည်။ ဘာသာစကား တစ်မျိုးတည်း ဖြစ်ပါက 32,000 ကို
ရွေးရမည်။

**တိုင်းတာမည့် metric —** ဘာသာစကား တစ်မျိုးစီအတွက် character-to-token ratio၊
sequence အရှည် p95၊ embedding memory MiB၊ task အပေါ် တိကျမှု။ ဤဆုံးဖြတ်ချက်တွင်
အဓိက အတည်ပြုချက်မှာ ratio တိုင်းတာမှု ဖြစ်သည်၊ embedding memory သည်
ဒုတိယ အဆင့် ဖြစ်သည်။

```bash
python3 - <<'PY'
def tied_mib(vocab, d_model):
    return 2 * vocab * d_model * 2 / 2 ** 20


for vocab in (32000, 128256):
    print(f"vocab {vocab:>7}: tied fp16 {tied_mib(vocab, 4096):8.2f} MiB")
print("ratio", round(tied_mib(128256, 4096) / tied_mib(32000, 4096), 3))
print("extra MiB", round(tied_mib(128256, 4096) - tied_mib(32000, 4096), 2))
PY
```

```text
vocab   32000: tied fp16   500.00 MiB
vocab  128256: tied fp16  2004.00 MiB
ratio 4.008
extra MiB 1504.0
```

#### အဖြေ ၂ — Deduplication ၏ တင်းကြပ်မှု

**ရှင်းလင်းချက် —** exact duplicate 10 % ဖယ်ရှားပါက ကျန်သည့် စာတမ်း 7,200,000 ဖြစ်သည်။
near-duplicate 5 % ပါ ဖယ်ရှားပါက 6,800,000 ဖြစ်သည်။ doc pass 24,000,000 အတွက်
epoch သည် 3.3333 မှ 3.5294 သို့ တက်သည် (အပိုင်း ၅.၁ အဖြေ ၅ တွင် တွက်ပြထားသည်)။
ထို တိုးလာသည့် ကုန်ကျစရိတ်သည် 5.88 % သာ ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** near-duplicate ပါ ဖယ်ရှားရမည်၊ သို့သော် borderline cluster များကို
လူက ပြန်လည် စစ်ဆေးရမည်။ အကြောင်းမှာ မတူညီသည့် record နှစ်ခုသည် စာသား တူညီစွာ
ရှိနိုင်ပြီး paraphrase နှစ်ခုသည် တူညီသည့် ယိုစိမ့်သည့် အချက်အလက်ကို ဆက်လက်
သယ်ဆောင်ထားနိုင်သောကြောင့် ဖြစ်သည်။ ဖယ်ရှားမှု တိုင်းကို rule id ဖြင့် မှတ်တမ်းတင်ရမည်။

**တိုင်းတာမည့် metric —** ဖယ်ရှားသည့် နမူနာ အရေအတွက်နှင့် နှုန်း၊ doc pass တစ်ခုလျှင်
validation loss၊ benchmark နှင့် ဆင်တူသည့် နမူနာ ရှိမရှိ၊ epoch နှင့် ကုန်ကျစရိတ်။
ဤဆုံးဖြတ်ချက်တွင် ကုန်ကျစရိတ်သည် ပြတ်သားစွာ တိုးသည်၊ အန္တရာယ်မှာ evaluation
ယုံကြည်စိတ်ချရမှု ဖြစ်သည့်အတွက် ထို အချက်သည် အဓိက အတည်ပြုချက် ဖြစ်သည်။

```bash
python3 - <<'PY'
docs, budget = 8_000_000, 3
passes = docs * budget
for label, removed_share in (("exact only", 0.10), ("exact + near", 0.15)):
    kept = docs - int(docs * removed_share)
    epochs = passes / kept
    print(f"{label:>13}: kept {kept}, epochs {round(epochs, 4)}, "
          f"increase pct {round(100 * (epochs / budget - 1), 2)}")
PY
```

```text
   exact only: kept 7200000, epochs 3.3333, increase pct 11.11
exact + near: kept 6800000, epochs 3.5294, increase pct 17.65
```

## Self-check

၁။ ဥပမာ ၁ တွင် စကားလုံး တစ်လုံးချင်း အဆင့်မှ token 34 သို့ ကျဆင်းရာတွင် merge rule သည်
မည်သည့် အချက်အပေါ် မူတည်၍ ရွေးချယ်သည်။

၂။ ဥပမာ ၂ တွင် vocabulary 128,256 ၏ embedding memory သည် vocabulary 32,000 ၏
မည်မျှ ဆ ဖြစ်သည်၊ အဘယ်ကြောင့် ထို အချိုးအတိုင်း ဖြစ်သည်။

၃။ ဥပမာ ၄ တွင် row ကျပန်း split ပြီးနောက် လုံးဝ လွတ်လပ်သည့် test row မည်မျှ ကျန်သနည်း၊
အဘယ်ကြောင့် ထို ရလဒ် ရသနည်း။

၄။ အပိုင်း ၅.၁ အဖြေ ၅ တွင် deduplication သည် epoch ကို မည်သည့် အချိုးအတိုင်း
တိုးစေသနည်း၊ ထို အချိုးသည် ဖယ်ရှားသည့် အချိုး အပေါ် မည်သို့ မူတည်သနည်း။

၅။ အပိုင်း ၅.၂ အဖြေ ၁ တွင် validation metric ကောင်းခြင်း၏ အဓိက ယန္တရားကို
ရှင်းလင်းပါ။

<details>
<summary>အဖြေများ</summary>

၁။ merge rule သည် အနီးကပ် ယူနစ် အတွဲ တစ်ခု၏ frequency ကို အခြေခံ၍ ရွေးသည်၊
frequency တူညီပါက စာလုံး အစဉ်အလိုက် ရွေးသည်။ ထို့ကြောင့် merge တိုင်း ပြီးတိုင်း
frequency ဇယားကို အသစ် ပြန်ရေတွက်ရပြီး ရလဒ်သည် deterministic ဖြစ်သည်။

၂။ 4.008 ဆ ဖြစ်သည်။ embedding matrix bytes = vocabulary × d_model × element byte
ဖြစ်သည့်အတွက် memory သည် vocabulary အရေအတွက် အပေါ် တိုက်ရိုက် အချိုးကျသည်။
d_model နှင့် dtype မပြောင်းလဲသဖြင့် အချိုးသည် vocabulary အချိုး 128,256 / 32,000
နှင့် တူညီသည်။

၃။ လုံးဝ လွတ်လပ်သည့် test row = 0 ခု ဖြစ်သည်။ user တစ်ဦးလျှင် record 200 ခု ရှိပြီး
row ကို ကျပန်း ခွဲခြားသဖြင့် user တိုင်းတွင် train row ရှိသည့် ဖြစ်နိုင်ခြေ = 1 − 0.2²⁰⁰
ဖြစ်သည်၊ ဆိုလိုသည်မှာ လက်တွေ့တွင် 1 ဖြစ်သည်။

၄။ epoch အချိုးသည် 1 / (1 − ဖယ်ရှားသည့် အချိုး) ဖြစ်သည်။ 15 % ဖယ်ရှားပါက
1 / 0.85 = 1.1765 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 17.65 % တိုးသည်။ အကြောင်းမှာ doc pass
စုစုပေါင်း ကို ကျန်သည့် စာတမ်း အရေအတွက်ဖြင့် စားရသောကြောင့် ဖြစ်သည်။

၅။ user တစ်ဦးလျှင် record အများအပြား ရှိသည့် dataset တွင် row ကို ကျပန်း ခွဲခြားပါက
test row တိုင်း၏ entity သည် train set ထဲ ရှိပြီး ဖြစ်သည်။ ထို့ကြောင့် validation metric
သည် မြင်ဖူးပြီးသား entity အပေါ် ခန့်မှန်းမှုကို တိုင်းနေခြင်း ဖြစ်ပြီး entity အသစ်
ရောက်လာသည့်အခါ ပြိုလဲသည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/03_data_and_representations.md` နှင့် `glossary/by_area/03_data_and_representations.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)
- [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499)
- [scikit-learn: Data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage)
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/)
- [Datasheets for Datasets](https://cacm.acm.org/research/datasheets-for-datasets/)

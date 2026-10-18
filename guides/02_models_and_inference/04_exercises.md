# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Models & Inference)

ဤဖိုင်သည် နယ်ပယ် ၀၂ ၏ term ၂၉ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြသနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် မိသားစု ခြောက်ခုအတွက် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ ခြောက်ခု၊ အပိုင်း ၂ တွင် တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ရှစ်ခု၊ အပိုင်း ၃ တွင် ပြသနာ ရှာဖွေခြင်း ငါးခု၊ အပိုင်း ၄ တွင် ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း သုံးခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု အဆင့်ဆင့်နှင့် အကြောင်းရင်း ရှင်းလင်းချက်နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁ နှင့် အပိုင်း ၅ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့် အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် command အတိုင်း run လုပ်ပါက တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် geometry နှင့် numerical format အပေါ် မှီခိုသည်၊ ထို့ကြောင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ၎င်း၏ ယူဆချက် (assumption) ကို ဖော်ပြထားသည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် `labs/lab_kv_cache.py`၊ `labs/lab_quantization.py`၊ `labs/lab_batching.py`၊ `labs/lab_sampling.py`၊ `labs/lab_context_budget.py` နှင့် `labs/lab_attention_cost.py` တို့ကို အသုံးပြုနိုင်သည်။ ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab များအပေါ် မှီခိုမှု မရှိပါ။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — Attention နှင့် Transformer: score matrix အရွယ်အစားနှင့် FLOPs

**ယူဆချက် —** sequence အရှည် T = 2048၊ d_model = 4096၊ head 32 ခု၊ head_dim = 128၊ batch = 1၊ fp16 (element တစ်ခုလျှင် 2 byte)။ Multiply-add တစ်ကြိမ်ကို FLOPs ၂ ခု အဖြစ် ရေတွက်သည်။ Mask ကြောင့် လျော့နည်းသွားသည့် တွက်ချက်မှုကို ထည့်သွင်းမထားပါ။

**ဖော်မြူလာ —**
- score entry အရေအတွက် = T × T × head အရေအတွက် × batch
- attention FLOPs (layer တစ်ခုလျှင်) = 4 × T² × d_model × batch
- projection FLOPs (layer တစ်ခုလျှင်) = 8 × T × d_model² × batch
- causal mask ဖြင့် လိုအပ်သည့် score entry = T (T + 1) / 2

**တွက်ချက်မှု —**
1. score entry = 2048 × 2048 × 32 = 134,217,728 (2²⁷)။
2. score buffer = 134,217,728 × 2 byte = 268,435,456 byte = 256 MiB = 0.25 GiB။
3. attention = 4 × 2048² × 4096 = 68,719,476,736 FLOPs ≈ 68.7 GFLOP။
4. projection = 8 × 2048 × 4096² = 274,877,906,944 FLOPs ≈ 274.9 GFLOP။
5. attention share = 4T²d / (4T²d + 8Td²) = T / (T + 2d) = 2048 / 10240 = 0.20 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 20 % ဖြစ်သည်။
6. causal score share = (T + 1) / 2T = 2049 / 4096 = 0.5002 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 50.02 % ဖြစ်သည်။

**ကောက်ချက် —** ဤ geometry တွင် attention သည် matmul စုစုပေါင်း၏ 20 % သာ ဖြစ်သည်၊ အကြောင်းမှာ T = 2d ဖြစ်သည့်အခါ ၎င်း၏ share သည် T / (T + 2d) = 0.5 ဖြစ်သောကြောင့် ဖြစ်သည်။ context ရှည်လာသည့်အခါ T သည် d_model ကို ကျော်လွန်သည်နှင့် attention ရှယ် (share) သည် လျင်မြန်စွာ ကြီးထွားလာမည်။ ထို့ကြောင့် context အရှည်နှင့် score buffer သည် ဆက်စပ်၍ တိုင်းတာရမည့် အတိုင်းအတာ ဖြစ်သည်။

```bash
python3 - <<'PY'
T, d, heads, bpe = 2048, 4096, 32, 2
entries = T * T * heads
print("score entries          ", entries)
print("score buffer MiB fp16  ", round(entries * bpe / 2**20, 1))
print("attention FLOPs/layer  ", 4 * T * T * d)
print("projection FLOPs/layer ", 8 * T * d * d)
print("attention share pct    ", round(100 * 4 * T * T * d / (4 * T * T * d + 8 * T * d * d), 2))
print("causal score share pct ", round(100 * (T * (T + 1) // 2) / (T * T), 2))
PY
```

```text
score entries           134217728
score buffer MiB fp16   256.0
attention FLOPs/layer   68719476736
projection FLOPs/layer  274877906944
attention share pct     20.0
causal score share pct  50.02
```

### ဥပမာ ၂ — Autoregressive decoding: forward pass အရေအတွက်နှင့် latency

**ယူဆချက် —** prompt token 512 ခု၊ output token 256 ခု၊ prefill သည် prompt တစ်ခုလုံးကို တစ်ပြိုင်နက် လုပ်ဆောင်၍ 45 ms ကြာသည်၊ decode အဆင့် တစ်ခုလျှင် 18 ms ကြာသည်။ token တစ်ခုလျှင် forward pass တစ်ခု လိုအပ်သည်။

**ဖော်မြူလာ —**
- forward pass အရေအတွက် = 1 + output token အရေအတွက်
- စုစုပေါင်း အချိန် = t_prefill + output token × t_step

**တွက်ချက်မှု —**
1. pass အရေအတွက် = 1 + 256 = 257 ဖြစ်သည်။ ပထမဆုံး pass သည် prompt ကို တစ်ပြိုင်နက် လုပ်ဆောင်ပြီး ပထမဆုံး token ကို ပေးသည်။
2. decode အချိန် = 256 × 18 ms = 4,608 ms ဖြစ်သည်။
3. စုစုပေါင်း = 45 + 4,608 = 4,653 ms = 4.653 s ဖြစ်သည်။
4. decode share = 4,608 / 4,653 = 99.0 % ဖြစ်သည်။
5. decode အဆင့်ကို ထက်ဝက် လျှော့ချပါက စုစုပေါင်း = 45 + 2,304 = 2,349 ms ဖြစ်သည်၊ ဆိုလိုသည်မှာ 49.5 % လျော့သည်။

**ကောက်ချက် —** prefill သည် တစ်ပြိုင်နက် လုပ်ဆောင်နိုင်သော်လည်း generation သည် အစဉ်လိုက် ဖြစ်သည့်အတွက် ခဏတာ (latency) ၏ 99 % သည် decode အဆင့်တွင် ဖြစ်ပေါ်သည်။ KV cache နှင့် speculative decoding သည် ဤအဆင့်ကို ပစ်မှတ်ထားသည့် နည်းလမ်းများ ဖြစ်သည်။

```bash
python3 - <<'PY'
prompt, out = 512, 256
prefill_ms, step_ms = 45.0, 18.0
total_ms = prefill_ms + out * step_ms
print("forward passes        ", 1 + out)
print("prefill ms            ", prefill_ms)
print("decode ms             ", out * step_ms)
print("total s               ", round(total_ms / 1000, 3))
half = prefill_ms + out * (step_ms / 2)
print("total s half step     ", round(half / 1000, 3))
print("latency cut pct       ", round(100 * (total_ms - half) / total_ms, 1))
print("share of time decoding", round(100 * out * step_ms / total_ms, 1))
PY
```

```text
forward passes         257
prefill ms             45.0
decode ms              4608.0
total s                4.653
total s half step      2.349
latency cut pct        49.5
share of time decoding 99.0
```

### ဥပမာ ၃ — KV cache: sequence တစ်ခုအတွက် memory

**ယူဆချက် —** layer 32 ခု၊ kv head 8 ခု (grouped-query attention)၊ head_dim = 128၊ batch = 1၊ sequence အရှည် 4096၊ fp16။ Paging သို့မဟုတ် allocator အပိုအလွှာ မထည့်သွင်းပါ။

**ဖော်မြူလာ —**
- bytes = 2 (key နှင့် value) × layer × batch × sequence အရှည် × kv head × head_dim × element byte

**တွက်ချက်မှု —**
1. 2 × 32 × 1 × 4096 × 8 × 128 × 2 = 536,870,912 byte ဖြစ်သည်။
2. 536,870,912 / 1,048,576 = 512 MiB = 0.5 GiB ဖြစ်သည်။
3. token တစ်ခုလျှင် 536,870,912 / 4096 = 131,072 byte = 128 KiB ဖြစ်သည်။
4. sequence အရှည် 8192 ဖြစ်ပါက 1 GiB ဖြစ်သည်၊ batch 32 ဖြစ်ပါက 16 GiB ဖြစ်သည်။
5. kv head 8 အစား 32 ဖြစ်ပါက 4 ဆ တိုးသည်၊ ဆိုလိုသည်မှာ 2 GiB ဖြစ်သည်။

**ကောက်ချက် —** KV cache သည် sequence အရှည်၊ layer၊ batch နှင့် kv head အရေအတွက် အပေါ် တိုက်ရိုက် အချိုးကျ ကြီးထွားသည်။ ထို့ကြောင့် concurrency မြှင့်သည့်အခါ KV cache memory သည် ပထမဆုံး ပြည့်လာသည့် အရင်းအမြစ် ဖြစ်လေ့ ရှိသည်။

```bash
python3 - <<'PY'
layers, kv_heads, head_dim, batch, seq, bpe = 32, 8, 128, 1, 4096, 2
kv = 2 * layers * batch * seq * kv_heads * head_dim * bpe
print("bytes          ", kv)
print("MiB            ", round(kv / 2**20, 1))
print("GiB            ", round(kv / 2**30, 3))
print("KiB per token  ", round(kv / seq / 1024, 1))
print("at seq 8192 GiB", 2 * layers * batch * 8192 * kv_heads * head_dim * bpe / 2**30)
print("at batch 32 GiB", kv * 32 / 2**30)
print("MHA would be x ", 32 / kv_heads)
PY
```

```text
bytes           536870912
MiB             512.0
GiB             0.5
KiB per token   128.0
at seq 8192 GiB 1.0
at batch 32 GiB 16.0
MHA would be x  4.0
```

### ဥပမာ ၄ — Quantization: weight memory နှင့် error အတိုင်းအတာ

**ယူဆချက် —** parameter 7 ဘီလီယံ၊ weight အပိုင်းအခြားသည် [-1, 1] အတွင်း ရှိသည်၊ symmetric uniform quantization ကို အသုံးပြုသည်၊ rounding လုပ်ပြီးနောက် ကျန်သည့် error သည် [-scale/2, scale/2] အတွင်း တူညီစွာ ပြန့်နှံ့သည်ဟု ယူဆသည်။

**ဖော်မြူလာ —**
- weight memory = parameter အရေအတွက် × bits / 8
- scale = max|w| / (2^(bits−1) − 1)
- အကြီးဆုံး error = scale / 2
- RMSE = scale / √12 (error သည် တူညီစွာ ပြန့်နှံ့သည့် ယူဆချက်အောက်တွင်)

**တွက်ချက်မှု —**
1. fp16 = 7e9 × 16 / 8 = 14.0 GB၊ int8 = 7.0 GB၊ int4 = 3.5 GB ဖြစ်သည်။
2. int8: level = 127၊ scale = 1 / 127 = 0.007874၊ အကြီးဆုံး error = 0.003937၊ RMSE = 0.002273 ဖြစ်သည်။
3. int4: level = 7၊ scale = 1 / 7 = 0.142857၊ အကြီးဆုံး error = 0.071429၊ RMSE = 0.041239 ဖြစ်သည်။
4. error အချိုး = 0.071429 / 0.003937 = 18.14 ဖြစ်သည်။
5. memory အချိုး = 3.5 / 7 = 0.5 ဖြစ်သည်။

**ကောက်ချက် —** 4-bit သည် memory ကို ထက်ဝက် လျှော့ပေးသော်လည်း step အရွယ်အစားသည် 18.14 ဆ ကြီးလာသည်။ ထို့ကြောင့် အရည်အသွေး ဆုံးရှုံးမှု အတိုင်းအတာကို eval ဖြင့် တိုင်းတာရမည်၊ သိမ်းဆည်းသည့် bit အရေအတွက် အပေါ် သာ မှီခို၍ ဆုံးဖြတ်ချက် မချရ။

```bash
python3 - <<'PY'
import math
params = 7_000_000_000
peak = 1.0
for name, bits in (("fp16", 16), ("int8", 8), ("int4", 4)):
    print(name, bits, "bits ->", round(params * bits / 8 / 1e9, 2), "GB")
for name, bits in (("int8", 8), ("int4", 4)):
    levels = 2 ** (bits - 1) - 1
    scale = peak / levels
    print(name, "scale", round(scale, 6), "max err", round(scale / 2, 6),
          "rmse", round(scale / math.sqrt(12), 6))
s8 = peak / 127 / 2
s4 = peak / 7 / 2
print("max err ratio 4-bit / 8-bit", round(s4 / s8, 2))
print("memory ratio 4-bit / 8-bit ", round(3.5 / 7, 3))
PY
```

```text
fp16 16 bits -> 14.0 GB
int8 8 bits -> 7.0 GB
int4 4 bits -> 3.5 GB
int8 scale 0.007874 max err 0.003937 rmse 0.002273
int4 scale 0.142857 max err 0.071429 rmse 0.041239
max err ratio 4-bit / 8-bit 18.14
memory ratio 4-bit / 8-bit  0.5
```

### ဥပမာ ၅ — Batching: throughput နှင့် cost per million tokens

**ယူဆချက် —** batch 16၊ decode step တစ်ခုလျှင် 60 ms၊ GPU-hour ခ $2.20၊ throughput တိုင်းတာချက်သည် decode အဆင့်တွင် ရရှိသည့် aggregate output token ဖြစ်သည်။

**ဖော်မြူလာ —**
- tokens per second = batch / t_step
- tokens per hour = tokens per second × 3600
- cost per 1M tokens = GPU-hour ခ / (tokens per second × 3600) × 10⁶

**တွက်ချက်မှု —**
1. tokens per second = 16 / 0.06 = 266.67 ဖြစ်သည်။
2. tokens per hour = 266.67 × 3600 = 960,000 ဖြစ်သည်။
3. cost per 1M = 2.20 / 960,000 × 10⁶ = $2.2917 ဖြစ်သည်။
4. batch 32 တွင် step သည် 1.7 ဆ ကြာသည်ဟု ယူဆပါက tokens per second = 32 / 0.102 = 313.73 ဖြစ်သည်၊ ဆိုလိုသည်မှာ 17.6 % တိုးသည်။
5. per-request rate သည် 16.67 တွင် ရှိရာမှ 9.80 tokens/s သို့ ကျဆင်းသည်။

**ကောက်ချက် —** batch မြှင့်ခြင်းသည် aggregate throughput ကို တိုးစေသော်လည်း request တစ်ခုချင်း၏ inter-token latency ကို ဆိုးရွားစွာ သက်ရောက်သည်။ ထို့ကြောင့် throughput နှင့် per-request latency ကို ခွဲခြား၍ တိုင်းတာရမည်။

```bash
python3 - <<'PY'
batch, step_ms, price = 16, 60.0, 2.20
tps = batch / (step_ms / 1000)
print("tokens per second   ", round(tps, 2))
print("tokens per hour     ", round(tps * 3600))
print("USD per 1M tokens   ", round(price / (tps * 3600) * 1e6, 4))
tps2 = 32 / ((60.0 * 1.7) / 1000)
print("batch 32 tps        ", round(tps2, 2), "gain pct", round(100 * (tps2 - tps) / tps, 1))
print("per request tps b16 ", round(1000 / 60.0, 2))
print("per request tps b32 ", round(1000 / 102.0, 2))
PY
```

```text
tokens per second    266.67
tokens per hour      960000
USD per 1M tokens    2.2917
batch 32 tps         313.73 gain pct 17.6
per request tps b16  16.67
per request tps b32  9.8
```

### ဥပမာ ၆ — Context budget: request တစ်ခုအတွက် လုံလောက်မှု

**ယူဆချက် —** context window 8192 token၊ system prompt 400 token၊ tool schema 1100 token၊ retrieved doc 6 ခု (တစ်ခုလျှင် 620 token)၊ conversation history 2400 token၊ user turn 250 token၊ output အတွက် သီးသန့် ချန်ထားသည့် 1024 token။

**ဖော်မြူလာ —**
- used = system + tools + retrieved + history + user + reserved_output
- shortfall = used − window

**တွက်ချက်မှု —**
1. retrieved = 6 × 620 = 3720 token ဖြစ်သည်။
2. used = 400 + 1100 + 3720 + 2400 + 250 + 1024 = 8894 token ဖြစ်သည်။
3. shortfall = 8894 − 8192 = 702 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ output အတွက် နေရာ 702 token လိုအပ်နေသည်။
4. output အတွက် ချန်ထားသည့် 1024 token ကို ထည့်မတွက်ပါက 7870 token ဖြစ်သည်၊ ထို့ကြောင့် ပြဿနာသည် output ချန်ရန် နေရာ မကျန်ခြင်း ဖြစ်သည်။
5. doc အတွက် ကျန်သည့် နေရာ = 8192 − (8894 − 3720) = 3018 token ဖြစ်သည်၊ ဆိုလိုသည်မှာ doc 4 ခု (2480 token) သာ ထည့်နိုင်သည်၊ ထို့ကြောင့် 2 ခု ဖြုတ်ရမည်။
6. window 16384 ဖြစ်ပါက output ချန်ပြီးနောက် 7490 token ကျန်သည်။

**ကောက်ချက် —** context budget ကို တွက်သည့်အခါ reserved output ကို မဖြစ်မနေ ထည့်ရမည်။ မထည့်ပါက window အတွင်း ဝင်သည်ဟု ထင်ရသော်လည်း အဖြေသည် အလယ်တွင် ပြတ်တောက်မည်။

```bash
python3 - <<'PY'
window = 8192
system, tools, docs_one, history, user, out = 400, 1100, 620, 2400, 250, 1024
docs = 6 * docs_one
used = system + tools + docs + history + user + out
print("retrieved tokens   ", docs)
print("used total         ", used)
print("window             ", window)
print("shortfall          ", used - window)
print("free after reserve ", window - used)
room = window - (used - docs)
print("room for docs      ", room, "docs that fit", room // docs_one)
print("drop               ", 6 - room // docs_one)
print("free at 16384      ", 16384 - used)
PY
```

```text
retrieved tokens    3720
used total          8894
window              8192
shortfall           702
free after reserve  -702
room for docs       3018 docs that fit 4
drop                2
free at 16384       7490
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို အပိုင်း ၅.၁ တွင် ပေးထားသည်။ ဖော်ပြထားသည့် lab ဖြင့် လက်တွေ့ စစ်ဆေးနိုင်သည်။

**လေ့ကျင့်ခန်း ၁ — KV cache memory**

layer 40 ခု၊ kv head 8 ခု၊ head_dim = 128၊ batch 8၊ sequence အရှည် 2048၊ fp16 (element တစ်ခုလျှင် 2 byte)။ တွက်ရမည့် အချက်များ — (က) စုစုပေါင်း byte၊ (ခ) MiB နှင့် GiB၊ (ဂ) request တစ်ခုလျှင် MiB၊ (ဃ) request တစ်ခုအတွက် token တစ်ခုလျှင် KiB၊ (င) element တစ်ခုလျှင် 1 byte ဖြစ်ပါက MiB။ → `labs/lab_kv_cache.py`

**လေ့ကျင့်ခန်း ၂ — weight memory နှင့် 80 GB accelerator**

80 GB accelerator တစ်ခုတွင် 8 GB ကို runtime၊ activation၊ KV cache နှင့် allocator အတွက် ချန်ထားသည်။ (က) 70B၊ 13B နှင့် 8B မော်ဒယ်များကို fp16၊ int8 နှင့် int4 ဖြင့် သိမ်းပါက GB မည်မျှ၊ (ခ) ကျန်သည့် နေရာတွင် မော်ဒယ် မည်မျှ ထည့်နိုင်သည်၊ (ဂ) 70B int4 တွင် metadata အပိုအလွှာ 10 % ရှိပါက GB နှင့် အရေအတွက် မည်မျှ။ → `labs/lab_quantization.py`

**လေ့ကျင့်ခန်း ၃ — attention FLOPs နှင့် score matrix memory**

T = 8192၊ d_model = 4096၊ head 32 ခု၊ head_dim = 128၊ batch = 1၊ layer 32 ခု၊ fp16။ (က) score entry အရေအတွက်၊ (ခ) fp16 buffer GiB နှင့် fp32 buffer GiB၊ (ဂ) layer တစ်ခုလျှင် attention TFLOP နှင့် layer အားလုံးအတွက် PFLOP၊ (ဃ) projection TFLOP နှင့် attention ရှယ် (share) %၊ (င) causal mask ဖြင့် အချိုး၊ (စ) T = 32768 ဖြစ်ပါက buffer GiB။ → `labs/lab_attention_cost.py`

**လေ့ကျင့်ခန်း ၄ — Temperature ချိန်ညှိပြီးနောက် probability**

logits = [2.0, 1.0, 0.0, -1.0]။ (က) temperature မထည့်မီ exp တန်ဖိုးများနှင့် ၎င်းတို့၏ ပေါင်းလဒ်၊ (ခ) T = 1.0၊ T = 0.5 နှင့် T = 2.0 အတွက် softmax ကို လက်ဖြင့် တွက်ရမည်၊ (ဂ) argmax သည် တန်ဖိုး ပြောင်းလဲသည့်အခါ ပြောင်းသွားပါသလော၊ (ဃ) အမြင့်ဆုံး probability သည် T နှင့်အတူ မည်သို့ ပြောင်းလဲသည်။ → `labs/lab_sampling.py`

**လေ့ကျင့်ခန်း ၅ — Top-k နှင့် top-p အဆင့်သတ်မှတ်ချက်**

next-token distribution ကို [0.42, 0.23, 0.14, 0.09, 0.06, 0.04, 0.02] အဖြစ် ပေးထားသည်။ (က) k = 3 အတွက် ကျန်သည့် candidate အစုနှင့် renormalize လုပ်ပြီးနောက် တန်ဖိုးများ၊ (ခ) p = 0.9 အတွက် ထိန်းထားသည့် candidate အရေအတွက်နှင့် cumulative probability၊ (ဂ) renormalize လုပ်ပြီးနောက် တန်ဖိုးများ၊ (ဃ) ဖြတ်လိုက်သည့် probability mass နှင့် ဖြတ်လိုက်သည့် ပထမဆုံး candidate တန်ဖိုး။ → `labs/lab_sampling.py`

**လေ့ကျင့်ခန်း ၆ — Tokens per second နှင့် cost per million tokens**

GPU-hour ခ $2.40၊ တိုင်းတာရရှိသည့် aggregate output throughput သည် 2,000 tokens/s။ (က) တစ်နာရီ tokens၊ (ခ) 1M output token အတွက် USD၊ (ဂ) 1K token အတွက် USD နှင့် $1 လျှင် token အရေအတွက်၊ (ဃ) 1M token ထုတ်လုပ်ရန် လိုအပ်သည့် စက္ကန့်၊ (င) throughput 60 % သို့ ကျဆင်းပါက 1M token ၏ USD၊ (စ) GPU နှစ်ခုကို တူညီသည့် rate ဖြင့် သုံးပါက USD။ → `labs/lab_batching.py`

**လေ့ကျင့်ခန်း ၇ — context budget shortfall**

window 32768 token၊ system 800၊ tool schema 2400၊ retrieved doc 12 ခု (တစ်ခုလျှင် 900)၊ history 18,000၊ user turn 600၊ reserved output 4000။ (က) doc အားလုံး၏ token၊ (ခ) used စုစုပေါင်းနှင့် shortfall၊ (ဂ) window ၏ မည်မျှ ရာခိုင်နှုန်းကို doc များ ယူထားသည်၊ (ဃ) doc အတွက် ကျန်သည့် နေရာ၊ ထည့်နိုင်သည့် doc အရေအတွက်နှင့် ဖြုတ်ရမည့် အရေအတွက်၊ (င) ဖြုတ်ပြီးနောက် ကျန်သည့် နေရာ၊ (စ) history ကို turn 30 ခုအတွင်း တည်ဆောက်ပါက turn တစ်ခုလျှင် ပျမ်းမျှ token။ → `labs/lab_context_budget.py`

**လေ့ကျင့်ခန်း ၈ — 8-bit နှင့် 4-bit နှိုင်းယှဉ်ချက်**

parameter 13 ဘီလီယံ၊ weight အပိုင်းအခြား [-1, 1]၊ symmetric uniform quantization။ (က) fp16၊ int8 နှင့် int4 weight GB၊ (ခ) int4 တွင် metadata 0.5 bit/parameter ထပ်တိုးပါက GB၊ (ဂ) int8 နှင့် int4 ၏ level အရေအတွက်၊ scale၊ အကြီးဆုံး error နှင့် RMSE၊ (ဃ) အကြီးဆုံး error အချိုး၊ (င) representable level အရေအတွက် 256 မှ မည်မျှသို့ ကျဆင်းသည်။ → `labs/lab_quantization.py`

## ၃။ ပြသနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြသနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊ ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည် တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင် ပေးထားသည်။

### ပြသနာ ၁ — TTFT ကောင်းသည်၊ သို့သော် streaming နှေးသည်ဟု ခံစားရသည်

- **Symptom —** ပထမဆုံး token သည် လျင်မြန်စွာ ရောက်လာသည်၊ သို့သော် အဖြေ တစ်ခုလုံး ပြီးဆုံးရန် ကြာသည်၊ စာသား ပေါ်လာသည့် အရှိန်သည် နှေးသည်ဟု အသုံးပြုသူ ခံစားရသည်။
- **တိုင်းတာရမည့် အချက် —** output token အရေအတွက်၊ inter-token latency (output token တစ်ခုနှင့် တစ်ခုအကြား အချိန်)၊ decode step အချိန်၊ တစ်ပြိုင်နက် လုပ်ဆောင်နေသည့် batch အရေအတွက်၊ chunk ရောက်လာသည့် အချိန် တစ်ခုနှင့် တစ်ခုအကြား ကြားကာလ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) concurrency မြှင့်သည့်အတွက် decode step အချိန် ကြီးလာခြင်း၊ (၂) output token အရေအတွက် များလာခြင်း၊ (၃) chunk များ စုပြီးမှ ရောက်လာခြင်း (buffering)၊ (၄) speculative decoding သို့မဟုတ် အခြား decode အရှိန်မြှင့်သည့် နည်းလမ်း မရှိတော့ခြင်း။
- **ဖြေရှင်းနည်း —** TTFT နှင့် inter-token latency ကို သီးသန့် တိုင်းတာပြီး batch ကို SLO အတွင်း ထိန်းရမည်၊ chunk boundary ကို flush လုပ်ရမည်၊ output အရှည်ကို ကန့်သတ်ရမည်။
- **ရှင်းလင်းသည့် term —** Streaming၊ Time to First Token (TTFT)၊ Tokens per Second (TPS)၊ Autoregressive။

### ပြသနာ ၂ — concurrency မြင့်သည့်အခါ throughput သည် ပြိုလဲသည်

- **Symptom —** request အရေအတွက် တိုးသည့်အခါ aggregate tokens per second သည် တိုးမလာဘဲ ကျဆင်းသည်၊ per-request လည်း ပို၍ နှေးလာသည်။
- **တိုင်းတာရမည့် အချက် —** queue depth၊ GPU utilization နှင့် memory အသုံးပြုမှု၊ KV cache memory အသုံးပြုမှုနှင့် ဖြုတ်ချခံရသည့် request အရေအတွက် (preemption)၊ တကယ် လုပ်ဆောင်နေသည့် batch အရေအတွက်၊ prefill ကြောင့် decode ရပ်တန့်သည့် အကြိမ်အရေအတွက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) KV cache memory ပြည့်၍ request များ ဖြုတ်ချခံရပြီး ပြန်လည် တွက်ချက်ခြင်း၊ (၂) prompt ရှည်သည့် request များ၏ prefill သည် decode ကို ရပ်တန့်စေခြင်း၊ (၃) batch ကြီးလာ၍ step အချိန် အချိုးမကျ တိုးလာခြင်း၊ (၄) padding နှင့် မညီသည့် အရှည်များကြောင့် တွက်ချက်မှု ဖြုန်းတီးခြင်း။
- **ဖြေရှင်းနည်း —** admission control ဖြင့် တစ်ပြိုင်နက် request အရေအတွက် ကို ကန့်သတ်ရမည်၊ paged KV cache နှင့် chunked prefill ကို ဖွင့်ရမည်၊ batch token အများဆုံး ပမာဏကို သတ်မှတ်ရမည်။
- **ရှင်းလင်းသည့် term —** KV Cache၊ Batching (Batch Size)၊ Time to First Token (TTFT)၊ Inference။

### ပြသနာ ၃ — quantization ပြောင်းပြီးနောက်မှသာ အရည်အသွေး ကျဆင်းသည်

- **Symptom —** prompt နှင့် decoding setting မပြောင်းလဲဘဲ weight format ပြောင်းပြီးနောက် အဖြေများ ပို၍ မှားလာသည်၊ သို့မဟုတ် အသုံးမဝင်လာသည်။
- **တိုင်းတာရမည့် အချက် —** တူညီသည့် eval set အပေါ် မပြောင်းလဲမီနှင့် ပြောင်းပြီးနောက် တိကျမှု၊ decoding configuration တူညီမှု၊ layer အလိုက် error အတိုင်းအတာ၊ calibration data နှင့် granularity၊ activation သို့မဟုတ် KV cache ကို ပါ quantize လုပ်ခဲ့မှု ရှိမရှိ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) 4-bit weight error သည် သတ်မှတ်ထားသည့် တိကျမှု အဆင့်ကို ကျော်လွန်ခြင်း၊ (၂) weight အပြင် activation သို့မဟုတ် cache ကို ပါ quantize လုပ်ခဲ့ခြင်း၊ (၃) calibration set သည် အသုံးပြုသည့် domain နှင့် မကိုက်ညီ၍ outlier weight များ ဖြတ်ခံရခြင်း၊ (၄) quantization နှင့် တစ်ချိန်တည်းတွင် temperature သို့မဟုတ် stop setting ပြောင်းလဲခဲ့ခြင်း။
- **ဖြေရှင်းနည်း —** eval ဖြင့် တိုင်းတာပြီး တိကျမှု အဆင့် မမီပါက int8 သို့မဟုတ် fp16 သို့ ပြန်ရမည်၊ weight ကိုသာ quantize လုပ်ရမည်၊ calibration data ကို ကိုက်ညီအောင် ပြန်ရွေးရမည်၊ မအောင်မြင်သည့် task class အတွက် route တစ်ခု ခွဲထားရမည်။
- **ရှင်းလင်းသည့် term —** Quantization၊ Perplexity၊ Evaluation (Eval)၊ Mixed Precision။

### ပြသနာ ၄ — ရှည်သည့် session တွင် အဖြေများ ပြတ်တောက်လာသည်

- **Symptom —** session အစတွင် ပုံမှန် ဖြစ်သည်၊ turn ၂၀ ကျော်လာသည့်အခါ အဖြေများ တိုလာသည်၊ အလယ်တွင် ပြတ်သည်၊ သို့မဟုတ် လုံးဝ မထွက်တော့သည်။
- **တိုင်းတာရမည့် အချက် —** turn တစ်ခုလျှင် input token ပမာဏ၊ input token ၏ turn အလိုက် ကြီးထွားမှု၊ window နှင့် နှိုင်းယှဉ်ချက်၊ rejected request ရှိမရှိ၊ reserved output token နှင့် max output token setting၊ output တွင် stop sequence ပါမပါ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) history စုပုံလာ၍ input token သည် window ကို ကျော်လွန်ခြင်း၊ ထို့ကြောင့် output အတွက် နေရာ မကျန်ခြင်း၊ (၂) stop sequence ကို စောစီးစွာ ကြုံတွေ့ခြင်း၊ (၃) max output token အဆင့်သတ်မှတ်ချက် ပြည့်ခြင်း၊ (၄) provider က context ကျော်လွန်မှုကို အသံမထွက်ဘဲ ဖြတ်တောက်ခြင်း။
- **ဖြေရှင်းနည်း —** turn တိုင်း input token ကို မှတ်တမ်းတင်ပြီး budget တွက်ရမည်၊ history ကို အနှစ်ချုပ်၍ ကျုံ့ရမည်၊ retrieved doc ကို လျှော့ရမည်၊ output အတွက် နေရာ အမြဲ ချန်ထားရမည်။
- **ရှင်းလင်းသည့် term —** Stop Sequence၊ Prompt Cache၊ Streaming၊ Token Budget။

### ပြသနာ ၅ — request အရောအနှော မပြောင်းလဲဘဲ per-request cost မြင့်လာသည်

- **Symptom —** request အမျိုးအစားနှင့် အရေအတွက် မပြောင်းလဲသော်လည်း တစ်နာရီ ကုန်ကျစရိတ် သို့မဟုတ် တစ်ခုလျှင် ကုန်ကျစရိတ် တက်လာသည်။
- **တိုင်းတာရမည့် အချက် —** request တစ်ခုလျှင် prompt token (prefill) ပမာဏ၊ prefix သို့မဟုတ် prompt cache ၏ hit rate၊ aggregate tokens per second၊ output token ပျမ်းမျှ အရေအတွက်၊ retry နှင့် မအောင်မြင်သည့် generation အရေအတွက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) prefix cache hit rate ကျဆင်း၍ prefill ကို ပြန်လည် တွက်ချက်ခြင်း၊ (၂) output token အရေအတွက် တိုးလာခြင်း (stop sequence မထိခြင်း၊ max token အဆင့် တိုးခြင်း)၊ (၃) throughput ကျဆင်း၍ request တစ်ခုလျှင် GPU-second တိုးလာခြင်း၊ (၄) retry များ၍ တူညီသည့် request ကို နှစ်ကြိမ် ကျခံရခြင်း။
- **ဖြေရှင်းနည်း —** prefix ကို တူညီသည့် အစဉ်အတိုင်း ထားရမည်၊ stop sequence နှင့် max output ကို ပြန်သတ်မှတ်ရမည်၊ batch policy ကို ပြန်ချိန်ရမည်၊ retry ကို limit လုပ်ရမည်။
- **ရှင်းလင်းသည့် term —** Prompt Cache၊ Prefix Caching၊ Tokens per Second (TPS)၊ Stop Sequence။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — context window ကို ကြီးအောင် ထားခြင်းနှင့် ကုန်ကျစရိတ်

**အခြေအနေ —** RAG အခြေခံ ဖောက်သည်ဝန်ဆောင်မှု assistant တစ်ခု ရှိသည်။ တောင်းဆိုမှု တစ်ခုလျှင် retrieved doc များနှင့် history ပေါင်းလျှင် prompt 25,000 token ရောက်သည်။ ရွေးချယ်စရာ နှစ်ခု ရှိသည် — ရွေးချယ်မှု A သည် 128k window endpoint ကို ဆက်သုံး၍ retrieval အားလုံး ထည့်သည်၊ ရွေးချယ်မှု B သည် 32k window တွင် retrieval budget 9,000 token ဖြစ် သတ်မှတ်၍ history ကို ကျုံ့သည်။

**trade-off —** A သည် context ပိုများ တွေ့မြင်နိုင်သည်၊ သို့သော် prefill token အရေအတွက် နှင့် TTFT တိုးသည်၊ B သည် ကုန်ကျစရိတ်နှင့် TTFT လျော့သည်၊ သို့သော် retrieval recall ကျဆင်းနိုင်သည်။

**ဆုံးဖြတ်ချက် —** B ကို ရွေးရမည်၊ အကြောင်းမှာ prompt token 2.78 ဆ လျော့သည်၊ TTFT 192 ms လျော့သည်၊ 1,000 request လျှင် $5.556 မှ $2.00 သို့ ကျဆင်းသည်။ သို့သော် ဤဆုံးဖြတ်ချက်သည် retrieval recall ကို တိုင်းတာသည့် eval တွင် တိကျမှု မကျဆင်းမှသာ ခိုင်လုံသည်။

**တိုင်းတာမည့် metric —** eval set အပေါ် အဖြေ တိကျမှု (ကျဆင်းမှု 1 % အတွင်း)၊ TTFT p50 နှင့် p95၊ 1,000 request လျှင် USD။

### ဆုံးဖြတ်ချက် ၂ — တိကျမှု အဆင့်ကို ရောက်ရန် precision ရွေးချယ်ခြင်း

**အခြေအနေ —** 13B မော်ဒယ်တစ်ခုကို task တစ်ခုအတွက် deploy လုပ်မည်။ လိုအပ်သည့် တိကျမှု အဆင့်သည် eval item 200 ခုအပေါ် 95.0 % ဖြစ်သည်။ တိုင်းတာရရှိသည်မှာ fp16 96.5 %၊ int8 95.5 %၊ int4 92.0 % ဖြစ်သည်။ accelerator ၏ usable memory သည် 72 GB ဖြစ်သည်။

**trade-off —** int8 သည် memory ကို 13.0 GB လျော့ပေးသည်၊ သို့သော် တိကျမှု အဆင့်အပေါ် ကျန်သည့် အနားသတ်သည် item တစ်ခုစာ (0.5 ရာခိုင်နှုန်းအမှတ်) သာ ဖြစ်သည်။ int4 သည် အဆင့်ကို မမီပါ (3.0 ရာခိုင်နှုန်းအမှတ် လျော့သည်၊ item 6 ခု)။

**ဆုံးဖြတ်ချက် —** fp16 ကို ဆက်ထားရမည်၊ အကြောင်းမှာ fp16 နှင့် int8 နှစ်ခုလုံး card တစ်ခုတွင် အလွယ်တကူ ဝင်သည့်အတွက် memory သည် ကန့်သတ်သည့် အရင်းအမြစ် မဟုတ်ပါ။ ကန့်သတ်သည့် အရင်းအမြစ်မှာ တိကျမှု ဖြစ်သည့်အတွက် ၎င်းကို လဲလှယ်၍ အကျိုးမရှိပါ။ int8 ကို ရွေးမည်ဆိုပါက item အရေအတွက် ပိုများသည့် eval (အနည်းဆုံး 1,000 ခု) ဖြင့် ပြန်လည် တိုင်းတာပြီး အနားသတ် 2 ရာခိုင်နှုန်းအမှတ် အထက် ရရှိမှသာ ရွေးသင့်သည်။

**တိုင်းတာမည့် metric —** သတ်မှတ်ထားသည့် sample size အပေါ် eval accuracy နှင့် bar နှင့် ကြားရှိ အနားသတ်။

### ဆုံးဖြတ်ချက် ၃ — batching policy နှင့် latency SLO

**အခြေအနေ —** per-request inter-token latency ၏ p95 သည် 100 ms အောက် ရှိရမည် ဟု SLO သတ်မှတ်ထားသည်။ decode step အချိန်ကို t(b) = 18 + 2.625b ms အဖြစ် တိုင်းတာရရှိသည်။ batch 16 တွင် 60.00 ms (266.7 tokens/s)၊ batch 24 တွင် 81.00 ms (296.3 tokens/s)၊ batch 32 တွင် 102.00 ms (313.7 tokens/s) ဖြစ်သည်။

**trade-off —** batch 32 သည် throughput အမြင့်ဆုံး ဖြစ်သော်လည်း 102 ms ဖြင့် SLO ကို ကျော်လွန်သည်။

**ဆုံးဖြတ်ချက် —** batch ကို 24 တွင် ကန့်သတ်ရမည်။ အကြောင်းမှာ 81.00 ms သည် 100 ms ၏ 81 % ဖြစ်၍ 20 % အနားသတ် ကျန်သည်၊ ဆုံးရှုံးသည့် throughput သည် 5.6 % သာ ဖြစ်သည်၊ cost သည် 1M output token လျှင် $1.9479 မှ $2.0625 သို့ တက်သည်။ တိုးလာသည့် latency သည် 21.00 ms ဖြစ်သည်။

**တိုင်းတာမည့် metric —** inter-token latency p95 နှင့် SLO လိုက်နာမှု ရာခိုင်နှုန်း၊ 1M output token လျှင် USD။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — KV cache memory

**ဖော်မြူလာ —** bytes = 2 × layer × batch × sequence × kv head × head_dim × element byte။ ယူဆချက် — fp16 ဖြစ်၍ element တစ်ခုလျှင် 2 byte၊ key နှင့် value နှစ်ခုလုံးကို သိမ်းသည်၊ paging အပိုအလွှာ မရှိပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. 2 × 40 × 8 × 2048 × 8 × 128 × 2 = 2,684,354,560 byte ဖြစ်သည်။
2. ထို တန်ဖိုးကို 1,048,576 ဖြင့် စားပါက 2,560.0 MiB ဖြစ်သည်၊ 2.5 GiB နှင့် ညီသည်။
3. request တစ်ခုလျှင် 2,560 / 8 = 320.0 MiB ဖြစ်သည်။
4. token တစ်ခုလျှင် 320 MiB / 2048 = 0.15625 MiB = 160.0 KiB ဖြစ်သည်။
5. element တစ်ခုလျှင် 1 byte ဖြစ်ပါက 1,280.0 MiB သို့ ကျဆင်းသည်။

**အဓိပ္ပာယ် —** batch 8 တွင် sequence တစ်ခုလျှင် KV cache 320 MiB ယူသည်၊ ထို့ကြောင့် concurrency 100 ရှိပါက 31.25 GiB ဖြစ်သည်။ ဤအတိုင်းအတာသည် batch size ကို ကန့်သတ်သည့် အဓိက အကြောင်းရင်း ဖြစ်လေ့ ရှိသည်။

```bash
python3 - <<'PY'
layers, kv_heads, head_dim, batch, seq, bpe = 40, 8, 128, 8, 2048, 2
kv = 2 * layers * batch * seq * kv_heads * head_dim * bpe
print("bytes          ", kv)
print("MiB            ", round(kv / 2**20, 1))
print("GiB            ", round(kv / 2**30, 3))
print("MiB per request", round(kv / batch / 2**20, 1))
print("KiB per request token", round(kv / batch / seq / 1024, 1))
print("MiB at 1 byte per element", round(kv / 2 / 2**20, 1))
PY
```

```text
bytes           2684354560
MiB             2560.0
GiB             2.5
MiB per request 320.0
KiB per request token 160.0
MiB at 1 byte per element 1280.0
```

#### အဖြေ ၂ — weight memory နှင့် 80 GB accelerator

**ဖော်မြူလာ —** weight GB = parameter × bits / 8 / 10⁹၊ ထည့်နိုင်သည့် အရေအတွက် = floor(usable GB / weight GB)။ ယူဆချက် — usable = 80 − 8 = 72 GB၊ sharding မလုပ်ပါ၊ metadata မပါပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. 70B: fp16 = 140.0 GB (0 ခု)၊ int8 = 70.0 GB (1 ခု)၊ int4 = 35.0 GB (2 ခု) ဖြစ်သည်။
2. 13B: fp16 = 26.0 GB (2 ခု)၊ int8 = 13.0 GB (5 ခု)၊ int4 = 6.5 GB (11 ခု) ဖြစ်သည်။
3. 8B: fp16 = 16.0 GB (4 ခု)၊ int8 = 8.0 GB (9 ခု)၊ int4 = 4.0 GB (18 ခု) ဖြစ်သည်။
4. 70B int4 တွင် 10 % metadata ထည့်ပါက 35.0 × 1.10 = 38.5 GB ဖြစ်သည်၊ ထို့ကြောင့် 2 ခု အစား 1 ခု သာ ထည့်နိုင်သည်။

**အဓိပ္ပာယ် —** parameter အရေအတွက်သည် memory ကို တိုက်ရိုက် မဆုံးဖြတ်ပါ၊ numerical format နှင့် metadata က ဆုံးဖြတ်သည်။ 70B ကို card တစ်ခုတွင် ထည့်ရန် int4 လိုအပ်သည်၊ သို့သော် metadata အနည်းငယ်ကပင် အရေအတွက်ကို ထက်ဝက် လျှော့ချနိုင်သည်။

```bash
python3 - <<'PY'
import math
card, reserved = 80, 8
usable = card - reserved
print("usable GB", usable)
for name, params in (("70B", 70e9), ("13B", 13e9), ("8B", 8e9)):
    for label, bits in (("fp16", 16), ("int8", 8), ("int4", 4)):
        gb = params * bits / 8 / 1e9
        print(f"{name} {label}: {gb:6.1f} GB -> fits {math.floor(usable / gb)}")
print("70B int4 with 10 pct metadata GB", round(70 * 4 / 8 * 1.10, 1))
print("count with metadata           ", math.floor(usable / (70 * 4 / 8 * 1.10)))
PY
```

```text
usable GB 72
70B fp16:  140.0 GB -> fits 0
70B int8:   70.0 GB -> fits 1
70B int4:   35.0 GB -> fits 2
13B fp16:   26.0 GB -> fits 2
13B int8:   13.0 GB -> fits 5
13B int4:    6.5 GB -> fits 11
8B fp16:   16.0 GB -> fits 4
8B int8:    8.0 GB -> fits 9
8B int4:    4.0 GB -> fits 18
70B int4 with 10 pct metadata GB 38.5
count with metadata            1
```

#### အဖြေ ၃ — attention FLOPs နှင့် score matrix memory

**ဖော်မြူလာ —** score entry = T × T × head × batch၊ attention FLOPs (layer တစ်ခုလျှင်) = 4 × T² × d_model × batch၊ projection FLOPs (layer တစ်ခုလျှင်) = 8 × T × d_model² × batch။ ယူဆချက် — multiply-add = 2 FLOPs၊ masking အလျော့အကျ မထည့်ပါ၊ score buffer ကို ရေတွက်ရာတွင် head အားလုံးကို ပေါင်းရသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. score entry = 8192 × 8192 × 32 × 1 = 2,147,483,648 (2³¹) ဖြစ်သည်။
2. fp16 buffer = 2,147,483,648 × 2 byte = 4.0 GiB ဖြစ်သည်၊ fp32 ဖြစ်ပါက 8.0 GiB ဖြစ်သည်။
3. attention = 4 × 8192² × 4096 = 1.0995 × 10¹² FLOPs = 1.1 TFLOP (layer တစ်ခုလျှင်) ဖြစ်သည်။
4. layer 32 ခုအတွက် = 1.0995 × 10¹² × 32 = 3.5184 × 10¹³ FLOPs = 0.0352 PFLOP ဖြစ်သည်။
5. projection = 8 × 8192 × 4096² = 1.0995 × 10¹² FLOPs = 1.1 TFLOP ဖြစ်သည်။ ဤ geometry တွင် T = 2 × d_model ဖြစ်သည့်အတွက် attention share = 4T²d / (4T²d + 8Td²) = 50.0 % ဖြစ်သည်။
6. causal mask ဖြင့် (T + 1) / 2T = 0.5001 ဖြစ်သည်၊ ဆိုလိုသည်မှာ အလုပ်ပမာဏ ထက်ဝက် လျော့သည်။
7. T = 32768 ဖြစ်ပါက buffer = 32768² × 32 × 2 byte = 64.0 GiB ဖြစ်သည်၊ ဆိုလိုသည်မှာ T လေးဆ တိုးသည့်အခါ buffer သည် ဆယ့်ခြောက်ဆ တိုးသည်။

**အဓိပ္ပာယ် —** context အရှည်သည် score buffer အပေါ် နှစ်ထပ်ကိန်း အချိုးကျ သက်ရောက်သည်။ ထို့ကြောင့် long-context serving တွင် memory ပြဿနာသည် weight မှ မဟုတ်ဘဲ attention buffer မှ လာလေ့ ရှိသည်။

```bash
python3 - <<'PY'
T, d, heads, head_dim, batch, layers, bpe = 8192, 4096, 32, 128, 1, 32, 2
entries = T * T * heads * batch
per_layer = 4 * T * T * d * batch
proj = 8 * T * d * d * batch
print("score entries          ", entries)
print("score buffer GiB fp16  ", entries * bpe / 2**30)
print("score buffer GiB fp32  ", entries * 4 / 2**30)
print("attention TFLOP/layer  ", round(per_layer / 1e12, 3))
print("attention PFLOP all    ", round(per_layer * layers / 1e15, 4))
print("projection TFLOP/layer ", round(proj / 1e12, 3))
print("attention share pct    ", round(100 * per_layer / (per_layer + proj), 1))
print("causal ratio           ", round((T * (T + 1) // 2) / (T * T), 4))
print("score buffer GiB at 32k", 32768 * 32768 * heads * batch * bpe / 2**30)
PY
```

```text
score entries           2147483648
score buffer GiB fp16   4.0
score buffer GiB fp32   8.0
attention TFLOP/layer   1.1
attention PFLOP all     0.0352
projection TFLOP/layer  1.1
attention share pct     50.0
causal ratio            0.5001
score buffer GiB at 32k 64.0
```

#### အဖြေ ၄ — Temperature ချိန်ညှိပြီးနောက် probability

**ဖော်မြူလာ —** p_i = exp(z_i / T) / Σ_j exp(z_j / T)။ ယူဆချက် — logits vector သည် [2.0, 1.0, 0.0, -1.0]၊ T သည် အပေါင်း တန်ဖိုး ဖြစ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. exp တန်ဖိုးများ = [7.389056, 2.718282, 1.000000, 0.367879] ဖြစ်သည်၊ ပေါင်းလဒ် = 11.475217 ဖြစ်သည်။
2. T = 1.0 တွင် p = [0.643914, 0.236883, 0.087144, 0.032059] ဖြစ်သည်။ 0.643914 = 7.389056 / 11.475217 ဖြစ်သည်။
3. T = 0.5 တွင် logits ကို 2 နှင့် မြှောက်သည်၊ ထို့ကြောင့် exp တန်ဖိုးများ = [54.598150, 7.389056, 1.000000, 0.135335] ဖြစ်သည်၊ ပေါင်းလဒ် = 63.122541 ဖြစ်သည်၊ p = [0.864955, 0.117059, 0.015842, 0.002144] ဖြစ်သည်။
4. T = 2.0 တွင် logits ကို 2 နှင့် စားသည်၊ exp တန်ဖိုးများ = [2.718282, 1.648721, 1.000000, 0.606531] ဖြစ်သည်၊ ပေါင်းလဒ် = 5.973534 ဖြစ်သည်၊ p = [0.455054, 0.276004, 0.167405, 0.101536] ဖြစ်သည်။
5. T သုံးမျိုးလုံးတွင် argmax သည် ပထမ position တွင် ရှိသည်၊ ဆိုလိုသည်မှာ 0.643914 မှ 0.864955 သို့ တက်သော်လည်း အစဉ်သည် မပြောင်းလဲပါ။
6. အမြင့်ဆုံး probability သည် T = 0.5 တွင် 0.864955၊ T = 1.0 တွင် 0.643914၊ T = 2.0 တွင် 0.455054 ဖြစ်သည်၊ ဆိုလိုသည်မှာ T တိုးသည့်အခါ distribution ပြန့်ပြူးလာသည်။

**အဓိပ္ပာယ် —** T သည် logits အချိုးအစားကို မပြောင်းလဲပါ၊ ထို့ကြောင့် အစဉ် (ranking) သည် မပြောင်းပါ။ ပြောင်းလဲသည်မှာ probability တန်ဖိုးများ၏ ပြန့်ပြူးမှု ဖြစ်သည်။ ထို့ကြောင့် temperature သည် model ၏ အသိပညာကို မပြောင်းလဲပါ။

```bash
python3 - <<'PY'
import math

logits = [2.0, 1.0, 0.0, -1.0]

def softmax(xs):
    ex = [math.exp(x) for x in xs]
    s = sum(ex)
    return [e / s for e in ex]

print("exp values", [round(math.exp(l), 6) for l in logits],
      "sum", round(sum(math.exp(l) for l in logits), 6))
for T in (1.0, 0.5, 2.0):
    p = softmax([l / T for l in logits])
    print("T =", T, [round(v, 6) for v in p])
PY
```

```text
exp values [7.389056, 2.718282, 1.0, 0.367879] sum 11.475217
T = 1.0 [0.643914, 0.236883, 0.087144, 0.032059]
T = 0.5 [0.864955, 0.117059, 0.015842, 0.002144]
T = 2.0 [0.455054, 0.276004, 0.167405, 0.101536]
```

#### အဖြေ ၅ — Top-k နှင့် top-p အဆင့်သတ်မှတ်ချက်

**ဖော်မြူလာ —** top-k တွင် အမြင့်ဆုံး k လုံးကို ရွေးပြီး ၎င်းတို့၏ ပေါင်းလဒ်ဖြင့် ပြန်စားသည်။ top-p တွင် cumulative probability သည် သတ်မှတ်ချက် ပြည့်သည့် အသေးဆုံး အစုကို ရွေးသည်။ ယူဆချက် — distribution သည် [0.42, 0.23, 0.14, 0.09, 0.06, 0.04, 0.02]၊ ဆိုလိုသည်မှာ ပေါင်းလဒ် 1.0 ဖြစ်ပြီး အစဉ်လိုက် စီပြီးသား ဖြစ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. k = 3 အတွက် ကျန်သည့် အစု = [0.42, 0.23, 0.14] ဖြစ်သည်၊ ပေါင်းလဒ် = 0.79 ဖြစ်သည်။
2. renormalize လုပ်ပြီးနောက် = [0.531646, 0.291139, 0.177215] ဖြစ်သည်။ ဥပမာ 0.42 / 0.79 = 0.531646 ဖြစ်သည်။
3. p = 0.9 အတွက် cumulative သည် 0.42၊ 0.65၊ 0.79၊ 0.88၊ 0.94 ဖြစ်သည်၊ ထို့ကြောင့် ပထမ 5 လုံးတွင် ရောက်ရှိသည်။
4. renormalize လုပ်ပြီးနောက် = [0.446809, 0.244681, 0.148936, 0.095745, 0.063830] ဖြစ်သည်။
5. ဖြတ်လိုက်သည့် mass = 1 − 0.94 = 0.06 ဖြစ်သည်၊ ဖြတ်လိုက်သည့် ပထမဆုံး candidate = 0.04 ဖြစ်သည်။

**အဓိပ္ပာယ် —** top-k သည် candidate အရေအတွက်ကို အမြဲ 3 တွင် ထိန်းထားသည်၊ top-p သည် distribution အပေါ် မှီခို၍ 5 လုံး ထိန်းထားသည်။ probability စုစည်းနေသည့် distribution တွင် top-p ၏ အစုသည် ပို၍ သေးငယ်လာမည်၊ မသေချာမှု ကျယ်ပြန့်သည့်အခါ ပို၍ ကြီးလာမည်။

```bash
python3 - <<'PY'
pd = [0.42, 0.23, 0.14, 0.09, 0.06, 0.04, 0.02]
print("sum", round(sum(pd), 6))
t3 = sum(pd[:3])
print("top-k 3 raw sum", round(t3, 6), "renorm", [round(v / t3, 6) for v in pd[:3]])
acc, kept = 0.0, []
for v in pd:
    acc += v
    kept.append(v)
    if acc >= 0.9:
        break
print("top-p 0.9 keeps", len(kept), "tokens cumulative", round(acc, 6))
print("renorm", [round(v / acc, 6) for v in kept])
print("tail dropped", round(1 - acc, 6), "in one candidate", pd[len(kept)])
PY
```

```text
sum 1.0
top-k 3 raw sum 0.79 renorm [0.531646, 0.291139, 0.177215]
top-p 0.9 keeps 5 tokens cumulative 0.94
renorm [0.446809, 0.244681, 0.148936, 0.095745, 0.06383]
tail dropped 0.06 in one candidate 0.04
```

#### အဖြေ ၆ — Tokens per second နှင့် cost per million tokens

**ဖော်မြူလာ —** tokens per hour = tokens per second × 3600၊ cost per 1M = GPU-hour ခ / tokens per hour × 10⁶။ ယူဆချက် — throughput 2,000 tokens/s သည် တိုင်းတာကာလ တစ်လျှောက်လုံး တည်ငြိမ်သည်၊ GPU တစ်ခုကို အပြည့် အသုံးပြုသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. တစ်နာရီ tokens = 2,000 × 3600 = 7,200,000 ဖြစ်သည်။
2. cost per 1M = 2.40 / 7,200,000 × 10⁶ = $0.3333 ဖြစ်သည်။
3. cost per 1K = 2.40 / 7,200,000 × 10³ = $0.000333 ဖြစ်သည်။
4. $1 လျှင် 7,200,000 / 2.40 = 3,000,000 token ရသည်။
5. 1M token ထုတ်လုပ်ရန် 10⁶ / 2,000 = 500.0 စက္ကန့် လိုအပ်သည်။
6. throughput 60 % သို့ ကျဆင်းပါက ကုန်ကျစရိတ်သည် 1 / 0.6 = 1.667 ဆ တိုးသည်၊ ဆိုလိုသည်မှာ $0.5556 ဖြစ်သည်။
7. GPU နှစ်ခုကို တူညီသည့် per-GPU rate ဖြင့် သုံးပါက cost per 1M သည် မပြောင်းလဲပါ ($0.3333)၊ အကြောင်းမှာ throughput နှင့် cost နှစ်ခုလုံး ထပ်တူ နှစ်ဆ ဖြစ်သောကြောင့် ဖြစ်သည်။

**အဓိပ္ပာယ် —** cost per million သည် throughput နှင့် တစ်ပြန်တစ်လှည့် အချိုးကျသည်။ ထို့ကြောင့် throughput တိုင်းတာချက် မှားယွင်းပါက cost ခန့်မှန်းချက်လည်း ထိုအချိုးအတိုင်း မှားယွင်းမည်။

```bash
python3 - <<'PY'
price_per_hour, tps = 2.40, 2000.0
per_hour = tps * 3600
print("tokens per hour     ", round(per_hour))
print("USD per 1M tokens   ", round(price_per_hour / per_hour * 1e6, 4))
print("USD per 1K tokens   ", round(price_per_hour / per_hour * 1e3, 6))
print("tokens per USD      ", round(per_hour / price_per_hour))
print("seconds for 1M out  ", round(1e6 / tps, 1))
print("cost if tps drops 40 pct", round(price_per_hour / (tps * 0.6 * 3600) * 1e6, 4))
print("two GPUs, same rate ", round(2 * price_per_hour / (2 * tps * 3600) * 1e6, 4))
PY
```

```text
tokens per hour      7200000
USD per 1M tokens    0.3333
USD per 1K tokens    0.000333
tokens per USD       3000000
seconds for 1M out   500.0
cost if tps drops 40 pct 0.5556
two GPUs, same rate  0.3333
```

#### အဖြေ ၇ — context budget shortfall

**ဖော်မြူလာ —** used = ပုံသေ အပိုင်းများ + doc token၊ shortfall = used − window။ ယူဆချက် — doc တစ်ခုလျှင် 900 token၊ ပုံသေ အပိုင်း = system 800 + tools 2400 + history 18,000 + user 600 + reserved output 4000 = 25,800 token။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. doc token = 12 × 900 = 10,800 ဖြစ်သည်။
2. used = 25,800 + 10,800 = 36,600 ဖြစ်သည်။
3. shortfall = 36,600 − 32,768 = 3,832 token ဖြစ်သည်။
4. doc share = 10,800 / 32,768 = 33.0 % ဖြစ်သည်။
5. doc အတွက် ကျန်သည့် နေရာ = 32,768 − 25,800 = 6,968 token ဖြစ်သည်၊ ထို့ကြောင့် 6,968 / 900 = 7.74 ဖြစ်သည်၊ ဆိုလိုသည်မှာ doc 7 ခု ထည့်နိုင်သည်၊ 5 ခု ဖြုတ်ရမည်။
6. ဖြုတ်ပြီးနောက် ကျန်သည့် နေရာ = 32,768 − (25,800 + 6,300) = 668 token ဖြစ်သည်။
7. history သည် turn 30 ခုအတွင်း 18,000 token ဖြစ်လာပါက turn တစ်ခုလျှင် 600 token ဖြစ်သည်။

**အဓိပ္ပာယ် —** ဤဥပမာတွင် ပြဿနာ၏ အကြီးဆုံး အစိတ်အပိုင်းသည် history (18,000 token) ဖြစ်သည်၊ retrieved doc (10,800) မဟုတ်ပါ။ ထို့ကြောင့် doc ဖြုတ်ခြင်းထက် history ကို ကျုံ့ခြင်းသည် ပို၍ ထိရောက်သည်။ နေရာ 3,832 token လိုအပ်နေသည့်အတွက် turn ရှစ်ခုစာ history ကို အနှစ်ချုပ်လိုက်ပါက ပြဿနာ ပြီးဆုံးသည်။

```bash
python3 - <<'PY'
window = 32768
per_doc = 900
fixed = 800 + 2400 + 18000 + 600 + 4000  # system, tools, history, user, reserved output
print("fixed parts      ", fixed)
print("per doc          ", per_doc)
n_docs = 12
docs = per_doc * n_docs
print("docs tokens      ", docs)
print("used total       ", fixed + docs, "window", window)
print("shortfall        ", fixed + docs - window)
print("docs share pct   ", round(100 * docs / window, 1))
room = window - fixed
print("room for docs    ", room, "docs that fit", room // per_doc)
print("drop             ", n_docs - room // per_doc)
kept = room // per_doc
print("free after trim  ", window - (fixed + kept * per_doc))
print("history per turn ", round(18000 / 30, 1), "over 30 turns")
PY
```

```text
fixed parts       25800
per doc           900
docs tokens       10800
used total        36600 window 32768
shortfall         3832
docs share pct    33.0
room for docs     6968 docs that fit 7
drop              5
free after trim   668
history per turn  600.0 over 30 turns
```

#### အဖြေ ၈ — 8-bit နှင့် 4-bit နှိုင်းယှဉ်ချက်

**ဖော်မြူလာ —** weight GB = parameter × bits / 8 / 10⁹၊ scale = max|w| / (2^(bits−1) − 1)၊ အကြီးဆုံး error = scale / 2၊ RMSE = scale / √12။ ယူဆချက် — weight အပိုင်းအခြား [-1, 1]၊ symmetric uniform quantization၊ rounding error သည် တူညီစွာ ပြန့်နှံ့သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. weight memory = 13e9 × 16 / 8 / 10⁹ = 26.0 GB (fp16)၊ 13.0 GB (int8)၊ 6.5 GB (int4) ဖြစ်သည်။
2. int4 တွင် metadata 0.5 bit/parameter ထည့်ပါက (13e9 × 4 + 13e9 × 0.5) / 8 / 10⁹ = 7.31 GB ဖြစ်သည်၊ ဆိုလိုသည်မှာ 12.5 % တိုးသည်။
3. int8: level = 127၊ scale = 1 / 127 = 0.007874၊ အကြီးဆုံး error = 0.003937၊ RMSE = 0.007874 / 3.4641 = 0.002273 ဖြစ်သည်။
4. int4: level = 7၊ scale = 1 / 7 = 0.142857၊ အကြီးဆုံး error = 0.071429၊ RMSE = 0.142857 / 3.4641 = 0.041239 ဖြစ်သည်။
5. error အချိုး = 0.071429 / 0.003937 = 18.14 ဖြစ်သည်။
6. representable level အရေအတွက်သည် 256 မှ 16 သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ level 16 ခုသာ ကျန်သည်။

**အဓိပ္ပာယ် —** memory အချိုးသည် 0.5 (ထက်ဝက်) ဖြစ်သော်လည်း error အချိုးသည် 18.14 ဆ ဖြစ်သည်၊ ဆိုလိုသည်မှာ ဆုံးရှုံးမှု နှစ်ခုသည် တူညီစွာ မလိုက်ပါ။ ထို့ကြောင့် bit အရေအတွက် လျှော့ချမှုနှင့် memory အလျော့အကျ အချိုးကို တူညီသည်ဟု မယူဆရ။

```bash
python3 - <<'PY'
import math
params, peak = 13e9, 1.0
for label, bits in (("fp16", 16), ("int8", 8), ("int4", 4)):
    print(label, round(params * bits / 8 / 1e9, 2), "GB")
print("int4 with 0.5 bit/param metadata",
      round((params * 4 + params * 0.5) / 8 / 1e9, 2), "GB")
for label, bits in (("int8", 8), ("int4", 4)):
    levels = 2 ** (bits - 1) - 1
    scale = peak / levels
    print(label, "levels", levels, "scale", round(scale, 6),
          "max err", round(scale / 2, 6), "rmse", round(scale / math.sqrt(12), 6))
print("max error ratio 4 / 8 ", round((peak / 7 / 2) / (peak / 127 / 2), 2))
print("levels lost           ", 2 ** 8, "->", 2 ** 4)
PY
```

```text
fp16 26.0 GB
int8 13.0 GB
int4 6.5 GB
int4 with 0.5 bit/param metadata 7.31 GB
int8 levels 127 scale 0.007874 max err 0.003937 rmse 0.002273
int4 levels 7 scale 0.142857 max err 0.071429 rmse 0.041239
max error ratio 4 / 8  18.14
levels lost            256 -> 16
```

### ၅.၂ ပြသနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — TTFT ကောင်းသော်လည်း streaming နှေး

**အကြောင်းရင်း ရှင်းလင်းချက် —** TTFT နှင့် inter-token latency သည် မတူညီသည့် အဆင့်နှစ်ခုကို တိုင်းတာသည်။ TTFT သည် prefill နှင့် queueing ကို ထင်ဟပ်သည်၊ inter-token latency သည် decode အဆင့် တစ်ခုလျှင် ကြာသည့် အချိန်ကို ထင်ဟပ်သည်။ batch size မြှင့်လိုက်သည့်အခါ step တစ်ခုလျှင် ကြာချိန် တိုးလာသည်၊ သို့သော် ပထမဆုံး token ရသည့် အချိန် အပေါ် သက်ရောက်မှု နည်းသည်၊ အကြောင်းမှာ prefill သည် တစ်ပြိုင်နက် လုပ်ဆောင်သည့် အဆင့် ဖြစ်သောကြောင့် ဖြစ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** inter-token latency ကို batch size နှင့် ဆွဲပြီး တိုင်းပါ။ step အချိန် သည် batch နှင့်အတူ တိုးနေပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ step အချိန် မပြောင်းလဲဘဲ chunk များ စုပြီးမှ ရောက်လာပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ output token အရေအတွက် တိုးနေပါက အကြောင်းရင်း (၂) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** batch ကို လျှော့ပြီးနောက် inter-token latency ကျဆင်းပြီး throughput လည်း လက်ခံနိုင်သည့် အတိုင်းအတာအတွင်း ရှိပါက ဆုံးဖြတ်ချက် မှန်ကန်သည်။ ဆိုလိုသည်မှာ ဤပြဿနာသည် throughput နှင့် latency ကို ခွဲခြား မတိုင်းတာခြင်းကြောင့် ဖြစ်ပေါ်သည့် ပြဿနာ ဖြစ်သည်။

#### အဖြေ ၂ — concurrency မြင့်သည့်အခါ throughput ပြိုလဲခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** KV cache memory သည် sequence အရှည်၊ layer နှင့် batch အပေါ် အချိုးကျ ကြီးထွားသည်။ concurrency တိုးသည့်အခါ KV cache သည် weight memory နှင့် ဆက်စပ်၍ VRAM ကို အပြည့် ယူသည်။ နေရာ မလုံလောက်သည့်အခါ serving system သည် request တစ်ခုကို ဖြုတ်ချပြီး ၎င်း၏ KV state ကို ဖျက်သည်၊ ထို request ပြန်လာသည့်အခါ prompt ကို အစမှ ပြန်၍ တွက်ချက်ရသည်။ ထို့ကြောင့် အလုပ်ပမာဏ ထပ်တလဲလဲ တိုးလာပြီး throughput ကျဆင်းသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** preemption အရေအတွက်နှင့် KV cache memory အသုံးပြုမှုကို တိုင်းပါ။ KV memory အသုံးပြုမှု 90 % ကျော်ပြီး preemption ရှိပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ prefill ကြာချိန် အလွန်ရှည်သည့် request များ ရောက်လာစဉ်တွင် decode ရပ်တန့်ပါက အကြောင်းရင်း (၂) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** admission control ကို ထည့်ပြီးနောက် throughput သည် linear နီးပါး တိုးပါက ပြဿနာသည် memory အပေါ် အခြေခံသည့် ဖြစ်သည်။ paged KV cache က memory အပိုင်းအစများကို အသုံးချနိုင်စေသည့်အတွက် တူညီသည့် VRAM တွင် request ပိုများ ထည့်နိုင်သည်။

#### အဖြေ ၃ — quantization ပြောင်းပြီးနောက် အရည်အသွေး ကျဆင်းခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** quantization သည် weight များကို အကန့်အသတ်ရှိသည့် level များသို့ အဝိုင်းချုပ်သည်၊ ထို့ကြောင့် error အသစ် တစ်ခု ပေါ်လာသည်။ ယူဆချက် အပိုင်းအခြား [-1, 1] အောက်တွင် int4 ၏ အကြီးဆုံး error သည် int8 ၏ 18.14 ဆ ဖြစ်သည် (အပိုင်း ၅.၁ အဖြေ ၈)။ ထို error သည် နောက်ဆုံး output အပေါ် အမြဲ တိုက်ရိုက် မထင်ရဘဲ task အလိုက် ကွာခြားသည်၊ ထို့ကြောင့် eval ဖြင့် တိုင်းတာရမည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** decoding configuration ကို ဦးစွာ တူညီအောင် ပြန်ထားပြီး eval ကို ပြန်လုပ်ပါ။ တိကျမှု ပြန်တက်ပါက အကြောင်းရင်း (၄) ဖြစ်သည်၊ quantization မဟုတ်ပါ။ မတက်ပါက int8 သို့ ပြန်ပြီး တိုင်းပါ။ int8 တွင် ပြန်ကောင်းလာပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ int8 တွင်လည်း မကောင်းပါက activation သို့မဟုတ် cache ကို ပါ quantize လုပ်ခဲ့မှုကို စစ်ပါ (အကြောင်းရင်း ၂)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** int8 သို့ ပြန်ပြီးနောက် တိကျမှုသည် သတ်မှတ်ထားသည့် bar အပေါ် အနားသတ် 2 ရာခိုင်နှုန်းအမှတ် အထက် ရှိမှသာ ထို precision ကို လက်ခံရမည်။ ဤစည်းမျဉ်းသည် sample အရေအတွက် နည်းသည့် eval တွင် ရရှိသည့် ကွာခြားမှု အနည်းငယ်ကို အလွန်အကျွံ အဓိပ္ပာယ် ကောက်ခြင်းကို တားဆီးသည်။

#### အဖြေ ၄ — ရှည်သည့် session တွင် အဖြေ ပြတ်တောက်ခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** autoregressive generation တွင် input token အရေအတွက်နှင့် output token အရေအတွက်သည် တူညီသည့် context window ကို မျှဝေ သုံးစွဲသည်။ history သည် turn တစ်ခုလျှင် 600 token ခန့် တိုးသည်ဟု ယူဆပါက turn 30 ခုတွင် 18,000 token ဖြစ်လာသည် (အပိုင်း ၅.၁ အဖြေ ၇)။ ထို ပမာဏသည် retrieved doc အားလုံးထက် ကြီးသည်။ window ပြည့်သည့်အခါ output အတွက် ချန်ထားသည့် နေရာ မကျန်တော့ဘဲ အဖြေသည် စောစီးစွာ ရပ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** turn တစ်ခုလျှင် input token ကို မှတ်တမ်းတင်ပါ။ ၎င်းသည် window နှင့် နီးကပ်လာပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ output တွင် stop sequence ပါလာပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ max output token အရေအတွက် ပြည့်သည့် အရေအတွက် များပါက အကြောင်းရင်း (၃) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** history ကို အနှစ်ချုပ်ပြီးနောက် input token သည် window ၏ 60 % အောက် ရောက်မှသာ လုံခြုံသည်ဟု ယူဆနိုင်သည်၊ အကြောင်းမှာ output အတွက် နေရာ လုံလောက်စွာ ကျန်ရမည် ဖြစ်သောကြောင့် ဖြစ်သည်။

#### အဖြေ ၅ — per-request cost မြင့်လာခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** cost per request သည် GPU-second အပေါ် အချိုးကျသည်။ GPU-second သည် throughput နှင့် တစ်ပြန်တစ်လှည့် အချိုးကျသည်ဟု အပိုင်း ၅.၁ အဖြေ ၆ တွင် တွက်ချက်ထားသည် (throughput 60 % ကျဆင်းပါက cost 1.667 ဆ တိုးသည်)။ prefix cache hit rate ကျဆင်းသည့်အခါ prefill token များ ပြန်လည် တွက်ချက်ရသည်၊ တူညီသည့် output အရေအတွက်အတွက် GPU-second ပိုလိုအပ်သည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** prefix cache hit rate ကို တိုင်းပါ၊ သုညသို့ နီးကပ်ပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ prompt token ပြောင်းမလဲဘဲ output token တိုးပါက အကြောင်းရင်း (၂) ဖြစ်သည်။ prompt နှင့် output နှစ်ခုလုံး မပြောင်းလဲဘဲ GPU utilization ကျဆင်းပါက အကြောင်းရင်း (၃) ဖြစ်သည်။ ကျခံရသည့် token အရေအတွက်သည် ထုတ်လုပ်သည့် အရေအတွက်ထက် များပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** prefix ကို တူညီသည့် အစဉ်အတိုင်း ထားခြင်းသည် prefix cache ၏ ရည်ရွယ်ချက် ဖြစ်သည့် KV state ပြန်လည် အသုံးပြုမှုကို ပြန်ရရှိစေသည်။ ပြင်ပြီးနောက် cost per 1M token ကို ပြန်တိုင်း၍ မူလ တန်ဖိုးသို့ ပြန်ရောက်မှ အတည်ပြုရမည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — context window နှင့် cost

**ရှင်းလင်းချက် —** prompt token အရေအတွက်သည် prefill အလုပ်ပမာဏနှင့် TTFT ကို တိုက်ရိုက် သတ်မှတ်သည်။ 25,000 မှ 9,000 သို့ လျှော့ချသည့်အခါ prefill token သည် 2.78 ဆ လျော့သည်၊ သတ်မှတ်ထားသည့် တိုင်းတာမှု ပုံစံအောက်တွင် TTFT သည် 192 ms လျော့သည်၊ 1,000 request လျှင် ကုန်ကျစရိတ်သည် $5.556 မှ $2.00 သို့ ကျဆင်းသည်။

**ဆုံးဖြတ်ချက် —** 32k window နှင့် retrieval budget 9,000 token ကို ရွေးရမည်၊ သို့သော် 25,000 token လိုအပ်သည့် ရှည်သည့် စာတမ်း သုံးသပ်ခြင်း အလုပ်များအတွက် 128k endpoint ကို route တစ်ခု အဖြစ် သီးသန့် ထားရမည်။

**တိုင်းတာမည့် metric —** eval အပေါ် အဖြေ တိကျမှု (မကျဆင်းရမည်)၊ TTFT p50 နှင့် 1,000 request လျှင် USD။ ဤဆုံးဖြတ်ချက်တွင် ကုန်ကျစရိတ်သည် ပြတ်သားစွာ ကျဆင်းသည်၊ အန္တရာယ်မှာ retrieval recall ဖြစ်သည့်အတွက် eval သည် အဓိက အတည်ပြုချက် ဖြစ်သည်။

```bash
python3 - <<'PY'
full, trim = 25000, 9000
print("prompt token ratio      ", round(full / trim, 2))
print("tokens saved per request", full - trim)
ms_per_1k = 12.0
print("prefill ms full         ", round(full / 1000 * ms_per_1k, 1))
print("prefill ms trimmed      ", round(trim / 1000 * ms_per_1k, 1))
print("TTFT saving ms          ", round((full - trim) / 1000 * ms_per_1k, 1))
price, tps_prefill = 2.40, 3000.0
print("USD per 1000 requests full   ", round(full / tps_prefill * 1000 / 3600 * price, 3))
print("USD per 1000 requests trimmed", round(trim / tps_prefill * 1000 / 3600 * price, 3))
print("trimmed prompt share of 32k  ", round(100 * trim / 32768, 1), "pct")
print("full prompt share of 32768   ", round(100 * full / 32768, 1), "pct")
PY
```

```text
prompt token ratio       2.78
tokens saved per request 16000
prefill ms full          300.0
prefill ms trimmed       108.0
TTFT saving ms           192.0
USD per 1000 requests full    5.556
USD per 1000 requests trimmed 2.0
trimmed prompt share of 32k   27.5 pct
full prompt share of 32768    76.3 pct
```

#### အဖြေ ၂ — precision နှင့် တိကျမှု အဆင့်

**ရှင်းလင်းချက် —** fp16 သည် bar အပေါ် 1.5 ရာခိုင်နှုန်းအမှတ်၊ int8 သည် 0.5 ရာခိုင်နှုန်းအမှတ် (item တစ်ခုစာ)၊ int4 သည် အောက် 3.0 ရာခိုင်နှုန်းအမှတ် (item ခြောက်ခုစာ) ရှိသည်။ memory အရ fp16 26.0 GB နှင့် int8 13.0 GB သည် 72 GB usable အတွင်း နှစ်ခုလုံး ဝင်သည်၊ ထို့ကြောင့် memory သည် ကန့်သတ်သည့် အရင်းအမြစ် မဟုတ်ပါ။

**ဆုံးဖြတ်ချက် —** fp16 ကို ဆက်ထားရမည်၊ အကြောင်းမှာ လဲလှယ်ရန် အကျိုးအမြတ် မရှိဘဲ bar နှင့် ကြားရှိ အနားသတ်ကို လျှော့ချရုံသာ ဖြစ်သည်။ memory သည် အမှန် အရင်းအမြစ် ကန့်သတ်ချက် ဖြစ်လာသည့် အခြေအနေတွင် int8 ကို ရွေးပြီး eval item 1,000 ခုဖြင့် အနားသတ် 2 ရာခိုင်နှုန်းအမှတ် အထက် ရရှိမှသာ လက်ခံရမည်။

**တိုင်းတာမည့် metric —** သတ်မှတ်ထားသည့် sample size အပေါ် eval accuracy နှင့် bar နှင့် ကြားရှိ အနားသတ်။ ဤဆုံးဖြတ်ချက်တွင် အရည်အသွေး ချိန်ခွင်နှင့် memory လိုအပ်ချက် နှစ်ခုလုံးကို ထည့်သွင်း စဉ်းစားထားသည်။

```bash
python3 - <<'PY'
bar, items = 95.0, 200
for name, correct in (("fp16", 193), ("int8", 191), ("int4", 184)):
    acc = 100 * correct / items
    print(f"{name}: {correct}/{items} = {acc:.1f} pct, margin {acc - bar:+.1f} pt")
print("int8 items of slack       ", round(100 * 191 / 200 - bar, 2), "pt ->", 1, "item")
params = 13e9
for label, bits in (("fp16", 16), ("int8", 8)):
    print(label, "weights GB", round(params * bits / 8 / 1e9, 2))
print("cards needed fp16 at 72 GB usable", round(params * 16 / 8 / 1e9 / 72, 3))
print("cards needed int8 at 72 GB usable", round(params * 8 / 8 / 1e9 / 72, 3))
print("headroom left fp16 GB", round(72 - params * 16 / 8 / 1e9, 1))
print("headroom left int8 GB", round(72 - params * 8 / 8 / 1e9, 1))
PY
```

```text
fp16: 193/200 = 96.5 pct, margin +1.5 pt
int8: 191/200 = 95.5 pct, margin +0.5 pt
int4: 184/200 = 92.0 pct, margin -3.0 pt
int8 items of slack        0.5 pt -> 1 item
fp16 weights GB 26.0
int8 weights GB 13.0
cards needed fp16 at 72 GB usable 0.361
cards needed int8 at 72 GB usable 0.181
headroom left fp16 GB 46.0
headroom left int8 GB 59.0
```

#### အဖြေ ၃ — batching policy နှင့် latency SLO

**ရှင်းလင်းချက် —** step အချိန် t(b) = 18 + 2.625b ms ဖြစ်သည့်အတွက် 100 ms SLO အတွင်း ဝင်သည့် အကြီးဆုံး batch သည် 31 ဖြစ်သည် (99.38 ms)၊ 20 % အနားသတ် ထားပါက 23 ဖြစ်သည်။ batch 32 သည် 102.00 ms ဖြစ်၍ SLO ကို ကျော်လွန်သည်၊ ဆိုလိုသည်မှာ p95 အတွက် လုံးဝ မသင့်လျော်ပါ။

**ဆုံးဖြတ်ချက် —** batch ကို 24 တွင် ကန့်သတ်ရမည် (81.00 ms၊ 296.3 tokens/s)။ ဆုံးရှုံးသည့် throughput သည် 5.6 % ဖြစ်ပြီး cost သည် 1M output token လျှင် $1.9479 မှ $2.0625 သို့ တက်သည်။ ထို 5.6 % သည် SLO လိုက်နာမှုကို ဝယ်ယူသည်၊ SLO ဖောက်ဖျက်မှုဖြစ်သည့် အခါ အသုံးပြုသူ သဘောတူညီချက် ဆုံးရှုံးမှုသည် ထို ကုန်ကျစရိတ်ထက် ကြီးသည်။

**တိုင်းတာမည့် metric —** inter-token latency p95 နှင့် 1M output token လျှင် USD။ ဤရလဒ်သည် batching policy ကို metric နှစ်ခုဖြင့် တိုင်းတာရမည် ဆိုသည့် အချက်ကို ပြသသည်၊ အကြောင်းမှာ throughput ကို ပိုင်းဖြတ်၍ ကြည့်ပါက batch 32 သည် အကောင်းဆုံး ဖြစ်သည်။

```bash
python3 - <<'PY'
ms = lambda b: 18.0 + 2.625 * b
tps = lambda b: b / (ms(b) / 1000)
for b in (1, 8, 16, 24, 30, 31, 32, 64):
    print(f"batch {b:3} step {ms(b):7.2f} ms tps {tps(b):6.1f} per-request tps {1000/ms(b):5.2f}")
slo = 100.0
print("largest batch in 100 ms SLO       ", max(b for b in range(1, 65) if ms(b) <= slo))
print("largest batch with 20 pct margin  ", max(b for b in range(1, 65) if ms(b) <= slo * 0.8))
print("throughput cost 24 vs 32 pct      ", round(100 * (tps(32) - tps(24)) / tps(32), 1))
print("latency saved 24 vs 32 ms         ", round(ms(32) - ms(24), 2))
print("USD per 1M at batch 24            ", round(2.20 / (tps(24) * 3600) * 1e6, 4))
print("USD per 1M at batch 32            ", round(2.20 / (tps(32) * 3600) * 1e6, 4))
PY
```

```text
batch   1 step   20.62 ms tps   48.5 per-request tps 48.48
batch   8 step   39.00 ms tps  205.1 per-request tps 25.64
batch  16 step   60.00 ms tps  266.7 per-request tps 16.67
batch  24 step   81.00 ms tps  296.3 per-request tps 12.35
batch  30 step   96.75 ms tps  310.1 per-request tps 10.34
batch  31 step   99.38 ms tps  311.9 per-request tps 10.06
batch  32 step  102.00 ms tps  313.7 per-request tps  9.80
batch  64 step  186.00 ms tps  344.1 per-request tps  5.38
largest batch in 100 ms SLO        31
largest batch with 20 pct margin   23
throughput cost 24 vs 32 pct       5.6
latency saved 24 vs 32 ms          21.0
USD per 1M at batch 24             2.0625
USD per 1M at batch 32             1.9479
```

## Self-check

၁။ အပိုင်း ၅.၁ အဖြေ ၁ တွင် KV cache ၏ token တစ်ခုလျှင် အရွယ်အစားကို မည်သို့ တွက်ချက်သည်၊ မည်သည့် အပိုင်းများအပေါ် မှီခိုသည်။

၂။ အပိုင်း ၅.၁ အဖြေ ၄ တွင် temperature တိုးသည့်အခါ argmax သည် ဘာသောကြောင့် မပြောင်းလဲသနည်း။

၃။ အပိုင်း ၅.၁ အဖြေ ၇ တွင် ပြဿနာ၏ အကြီးဆုံး အစိတ်အပိုင်းသည် doc ဖြစ်သလော၊ history ဖြစ်သလော။

၄။ အပိုင်း ၅.၂ အဖြေ ၂ တွင် throughput ပြိုလဲခြင်း၏ အဓိက ယန္တရားကို ရှင်းလင်းပါ။

၅။ အပိုင်း ၅.၃ အဖြေ ၃ တွင် batch 32 ကို မရွေးရသည့် အကြောင်းရင်းနှင့် ဆုံးရှုံးသည့် throughput ရာခိုင်နှုန်းကို ဖော်ပြပါ။

<details>
<summary>အဖြေများ</summary>

၁။ KV cache bytes = 2 × layer × batch × sequence × kv head × head_dim × element byte ဖြစ်သည်။ token တစ်ခုလျှင် အရွယ်အစားကို ရရှိရန် စုစုပေါင်း byte ကို sequence အရှည်ဖြင့် စားသည်၊ ထို့ကြောင့် အဖြေသည် layer၊ kv head၊ head_dim နှင့် element byte အပေါ် မှီခိုပြီး batch နှင့် sequence အပေါ် မမှီခိုပါ။

၂။ temperature သည် logits တန်ဖိုးများကို တူညီသည့် အပြုကိန်းဖြင့် စားခြင်း ဖြစ်သည်၊ ထို့ကြောင့် တန်ဖိုးများ၏ အစဉ်သည် မပြောင်းလဲပါ။ argmax သည် အစဉ်အပေါ် မှီခိုသည့်အတွက် မပြောင်းလဲပါ။

၃။ history ဖြစ်သည်၊ အကြောင်းမှာ history သည် 18,000 token ဖြစ်၍ doc အားလုံး၏ 10,800 token ထက် ကြီးသောကြောင့် ဖြစ်သည်။

၄။ KV cache memory ပြည့်သည့်အခါ request များ ဖြုတ်ချခံရပြီး ၎င်းတို့၏ KV state ဖျက်ခံရသည်၊ ပြန်လာသည့်အခါ prompt ကို အစမှ ပြန်တွက်ရသောကြောင့် အလုပ်ပမာဏ ထပ်တလဲလဲ တိုးလာသည်။

၅။ batch 32 ၏ step အချိန်သည် 102.00 ms ဖြစ်၍ 100 ms SLO ကို ကျော်လွန်သောကြောင့် မရွေးရပါ။ batch 24 ကို ရွေးသည့်အခါ ဆုံးရှုံးသည့် throughput သည် 5.6 % ဖြစ်သည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — `terms/02_models_and_inference.md` နှင့် `glossary/by_area/02_models_and_inference.json`။
- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed, from `rohitg00/ai-engineering-from-scratch`။
- လက်တွေ့ lab များ — `labs/lab_kv_cache.py`၊ `labs/lab_quantization.py`၊ `labs/lab_batching.py`၊ `labs/lab_sampling.py`၊ `labs/lab_context_budget.py`၊ `labs/lab_attention_cost.py`။
- Papers and documentation: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)၊ [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)၊ [Fast Inference from Transformers via Speculative Decoding](https://proceedings.mlr.press/v202/leviathan23a.html)။

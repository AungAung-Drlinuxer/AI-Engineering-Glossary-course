# ၀၄ — လေ့ကျင့်ခန်းများနှင့် အဖြေများ (Infrastructure & serving)

ဤဖိုင်သည် နယ်ပယ် ၀၉ ၏ term ၁၈ ခုကို အသုံးပြု၍ တွက်ချက်ခြင်း၊ ပြဿနာ ရှာဖွေခြင်းနှင့် ဆုံးဖြတ်ချက် ချခြင်း
လေ့ကျင့်ခန်းများကို စုစည်းထားသည်။ အပိုင်း ၁ တွင် အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာ လေးခု၊ အပိုင်း ၂ တွင်
တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ခြောက်ခု၊ အပိုင်း ၃ တွင် ပြဿနာ ရှာဖွေခြင်း သုံးခု၊ အပိုင်း ၄ တွင်
ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်း နှစ်ခု ပါဝင်သည်။ အပိုင်း ၅ တွင် အဖြေတိုင်းကို ဖော်မြူလာ၊ တွက်ချက်မှု
အဆင့်ဆင့်နှင့် ယူဆချက် (assumption) နှင့်အတူ ပေးထားသည်။

အပိုင်း ၁၊ ၅.၁ နှင့် ၅.၃ တွင် ပါဝင်သည့် ကိန်းဂဏန်း တိုင်းသည် Python (standard library သာ) ဖြင့်
အမှန်တကယ် လုပ်ဆောင်ခဲ့သည့် တွက်ချက်မှု၏ output ဖြစ်သည်။ ဖော်ပြထားသည့် block အတိုင်း run လုပ်ပါက
တူညီသည့် output ကို ပြန်လည် ရရှိမည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် geometry နှင့်
numerical format အပေါ် မှီခိုသည်၊ ထို့ကြောင့် တန်ဖိုးတိုင်းနှင့်အတူ ၎င်း၏ ယူဆချက်ကို ဖော်ပြထားသည်။
Benchmark တိုင်းတာမှု မဟုတ်သော ကိန်းဂဏန်းများကို "ခန့်မှန်းချက်" ဟု ရှင်းလင်းစွာ မှတ်သားထားသည်။

လေ့ကျင့်ခန်းများကို လက်တွေ့ စမ်းသပ်ရန် `labs/lab_serving_memory.py`၊ `labs/lab_roofline.py`
နှင့် `labs/lab_autoscale.py` တို့ကို အသုံးပြုနိုင်သည် (flag အားလုံး — [`labs/README.md`](labs/README.md))။
ဤဖိုင်၏ တွက်ချက်မှုများသည် ထို lab များအပေါ် မှီခိုမှု မရှိပါ၊ သို့သော် ကိန်းဂဏန်းများကို
နှစ်လမ်းဖြင့် တိုက်စစ်နိုင်သည်။

## ၁။ အလုပ်လုပ်ပြီး ဖြေသည့် ဥပမာများ (Worked Examples)

### ဥပမာ ၁ — Request တစ်ခု၏ ကုန်ကျစရိတ်ကို အစိတ်အပိုင်း အလိုက် ခွဲခြင်း

**ယူဆချက် —** prompt token 2,000၊ output token 400၊ queue ကြာချိန် 40 ms၊ prefill သည် 3,000 token/s
နှုန်းဖြင့် လည်ပတ်သည်၊ decode step တစ်ခုလျှင် 22 ms၊ batch 16။

**ဖော်မြူလာ —**
- prefill ကြာချိန် = prompt token ÷ prefill နှုန်း
- TTFT = queue ကြာချိန် + prefill ကြာချိန်
- စုစုပေါင်း = TTFT + output token × step ကြာချိန်
- aggregate tokens per second = batch ÷ step ကြာချိန်

**တွက်ချက်မှု —**
1. prefill = 2,000 ÷ 3,000 s = 666.7 ms ဖြစ်သည်။
2. TTFT = 40 + 666.7 = 706.7 ms ဖြစ်သည်၊ 800 ms ပန်းတိုင်၏ 88.3 % ဖြစ်သည်။
3. decode = 400 × 22 ms = 8,800 ms ဖြစ်သည်။
4. စုစုပေါင်း = 9.507 s ဖြစ်သည်၊ decode အပိုင်းသည် 92.6 % ကို ယူသည်။
5. per-request နှုန်း = 1,000 ÷ 22 = 45.45 tokens/s ဖြစ်သည်၊ batch 16 တွင် aggregate 727.3 tokens/s ဖြစ်သည်။
6. prompt ကို 800 token သို့ လျှော့ပါက TTFT သည် 306.7 ms သို့ ကျဆင်းသည် — ဆိုလိုသည်မှာ TTFT ကို
   prompt အရှည်က ဆုံးဖြတ်သည်။

**ကောက်ချက် —** ဤ workload တွင် ခဏတာ (latency) ၏ အများစုသည် decode အဆင့်တွင် ကုန်သည်။
ထို့ကြောင့် TTFT ကို ကောင်းစေသည့် ပြောင်းလဲမှု တိုင်းသည် စုစုပေါင်း ခံစားမှုကို သိသိသာသာ
မပြောင်းလဲနိုင်ပါ။ ခံစားမှုကို တိုးတက်စေရန် `Decode Phase` ကို ပစ်မှတ်ထားရမည်။

```bash
python3 - <<'PY'
prompt, output = 2000, 400
queue_ms, prefill_tps, step_ms = 40.0, 3000.0, 22.0
prefill_ms = prompt / prefill_tps * 1000
ttft_ms = queue_ms + prefill_ms
total_ms = ttft_ms + output * step_ms
print("prefill ms           ", round(prefill_ms, 1))
print("TTFT ms              ", round(ttft_ms, 1))
print("decode ms            ", output * step_ms)
print("total s              ", round(total_ms / 1000, 3))
print("decode share pct     ", round(100 * output * step_ms / total_ms, 1))
print("per request tps      ", round(1000 / step_ms, 2))
print("aggregate tps batch16", round(16 * 1000 / step_ms, 1))
print("requests per hour 1 replica at batch 16", round(16 * 3600 / (output * step_ms / 1000), 1))
print("TTFT budget 800 ms used pct", round(100 * ttft_ms / 800, 1))
print("cut prompt to 800 tokens: TTFT ms", round(queue_ms + 800 / prefill_tps * 1000, 1))
PY
```

```text
prefill ms            666.7
TTFT ms               706.7
decode ms             8800.0
total s               9.507
decode share pct      92.6
per request tps       45.45
aggregate tps batch16 727.3
requests per hour 1 replica at batch 16 6545.5
TTFT budget 800 ms used pct 88.3
cut prompt to 800 tokens: TTFT ms 306.7
```

### ဥပမာ ၂ — Static batching နှင့် Continuous Batching ၏ slot အသုံးချမှု

**ယူဆချက် —** request လေးခု၏ output အရှည်များသည် 200၊ 40၊ 150 နှင့် 60 ဖြစ်သည်။ slot ၄ ခု၊
decode step ကြာချိန် 20 ms။ Static batching တွင် batch တစ်ခုလုံးသည် အရှည်ဆုံး request အထိ
လည်ပတ်သည်။ Continuous Batching တွင် slot အလွတ် ဖြစ်သည်နှင့် အလုပ်အသစ် ချက်ချင်း ဝင်သည်။

**ဖော်မြူလာ —**
- static slot-steps = slot အရေအတွက် × အရှည်ဆုံး output
- အသုံးဝင်သည့် slot-steps = output အရှည်များ၏ ပေါင်းလဒ်
- လွင့်သည့် အချိုး = (static slot-steps − useful) ÷ static slot-steps
- continuous wall time = ပေါင်းလဒ် ÷ slot အရေအတွက် × step ကြာချိန်

**တွက်ချက်မှု —**
1. static slot-steps = 4 × 200 = 800 ဖြစ်သည်။
2. အသုံးဝင်သည့် slot-steps = 450 ဖြစ်သည်၊ လွင့်သည့် အရေအတွက် = 350 ဖြစ်သည်။
3. လွင့်သည့် အချိုး = 43.8 % ဖြစ်သည်။
4. static တွင် wall time = 4,000 ms၊ ပြီးစီးသည့် နှုန်း = 1.00 request/s ဖြစ်သည်။
5. continuous တွင် wall time = 2,250 ms၊ နှုန်း = 1.78 request/s ဖြစ်သည် — 1.78 ဆ လျင်သည်။
6. tokens/s သည် 112.5 မှ 200.0 သို့ တိုးသည်။

**ကောက်ချက် —** ကွာခြားမှုသည် memory သို့မဟုတ် compute အသစ် မှ မဟုတ်ပါ။ အလွတ် slot ကို
ပြန်ဖြည့်ခြင်းမှ လာသည်။ ထို့ကြောင့် `Continuous Batching` သည် အရင်းအမြစ် တိုးခြင်း မဟုတ်ဘဲ
အရင်းအမြစ် အသုံးချမှု ပြောင်းလဲခြင်း ဖြစ်သည်။

```bash
python3 - <<'PY'
lens = [200, 40, 150, 60]
step_ms, slots = 20.0, 4
longest = max(lens)
slot_steps = slots * longest
useful = sum(lens)
print("requests             ", len(lens))
print("output lengths       ", lens)
print("longest output       ", longest)
print("static slot-steps    ", slot_steps)
print("useful slot-steps    ", useful)
print("idle slot-steps      ", slot_steps - useful)
print("static waste pct     ", round(100 * (slot_steps - useful) / slot_steps, 1))
print("static wall ms       ", longest * step_ms)
print("static goodput req/s ", round(slots / (longest * step_ms / 1000), 2))
refill = sum(lens)
print("continuous wall ms   ", round(refill * step_ms / slots, 1))
print("continuous req/s     ", round(slots / (refill * step_ms / slots / 1000), 2))
print("speedup              ", round((longest * step_ms) / (refill * step_ms / slots), 2))
print("static tokens/s      ", round(useful / (longest * step_ms / 1000), 1))
print("continuous tokens/s  ", round(useful / (refill * step_ms / slots / 1000), 1))
PY
```

```text
requests              4
output lengths        [200, 40, 150, 60]
longest output        200
static slot-steps     800
useful slot-steps     450
idle slot-steps       350
static waste pct      43.8
static wall ms        4000.0
static goodput req/s  1.0
continuous wall ms    2250.0
continuous req/s      1.78
speedup               1.78
static tokens/s       112.5
continuous tokens/s   200.0
```

### ဥပမာ ၃ — Paged KV Cache block နှင့် Prefix Caching ၏ အကျိုးအမြတ်

**ယူဆချက် —** layer 32၊ kv head 8၊ head_dim 128၊ fp16 (element တစ်ခုလျှင် 2 byte)။ block အရွယ်အစား
16 token။ sequence အရှည် 1,000 token၊ မျှဝေသည့် system prefix 1,500 token၊ prefill နှုန်း 3,000 token/s။
Paging အတွက် metadata အပိုအလွှာ မထည့်သွင်းပါ။

**ဖော်မြူလာ —**
- token တစ်ခုလျှင် KV byte = 2 × layer × kv head × head_dim × element byte
- block byte = token တစ်ခုလျှင် byte × block အရွယ်အစား
- လိုအပ်သည့် block = ceil(sequence အရှည် ÷ block အရွယ်အစား)
- အတွင်း လွင့်မှု = block အားလုံး၏ token − sequence အရှည်

**တွက်ချက်မှု —**
1. token တစ်ခုလျှင် = 2 × 32 × 8 × 128 × 2 = 131,072 byte = 128 KiB ဖြစ်သည်။
2. block တစ်ခုလျှင် = 128 KiB × 16 = 2 MiB ဖြစ်သည်။
3. sequence 1,000 token အတွက် block 63 လိုသည်၊ ခွဲပေးသည့် token သည် 1,008 ဖြစ်သဖြင့်
   အတွင်း လွင့်မှုသည် 8 token (0.8 %) သာ ဖြစ်သည်။
4. ထို sequence အတွက် KV သည် 126.0 MiB ဖြစ်သည်။ sequence 64 ခု တစ်ချိန်တည်း ရှိပါက 8,064 MiB ဖြစ်သည်။
5. prefix 1,500 token အတွက် block 94 လိုသည်၊ ၎င်းသည် 188.0 MiB ဖြစ်သည်၊ request တိုင်း
   ထို block များကို ပြန်သုံးပါက 500.0 ms စာ prefill အလုပ် ကျော်နိုင်သည်။
6. 8,192 token ကို ဆက်တိုက် ကြိုတင် သတ်မှတ်ထားပါက 1,024.0 MiB လိုသည် — အသုံးပြုသည့်
   အရှည်နှင့် မသက်ဆိုင်ဘဲ နေရာ ယူထားခြင်း ဖြစ်သည်။

**ကောက်ချက် —** block အခြေခံ allocation သည် အတွင်း လွင့်မှုကို သေးငယ်စေပြီး
`Prefix Caching` ကို ဖြစ်နိုင်စေသည်။ သို့သော် block အရွယ်အစား ကြီးလွန်းပါက လွင့်မှု ပြန်တိုးသည်၊
ငယ်လွန်းပါက block table ၏ overhead တိုးသည် — ထို့ကြောင့် block အရွယ်အစားသည် တိုင်းတာမှုမှ
ရွေးရမည့် parameter ဖြစ်သည်။

```bash
python3 - <<'PY'
import math
layers, kv_heads, head_dim, bpe = 32, 8, 128, 2
per_token = 2 * layers * kv_heads * head_dim * bpe
block_tokens = 16
block_bytes = per_token * block_tokens
print("bytes per token      ", per_token)
print("KiB per token        ", round(per_token / 1024, 1))
print("block bytes          ", block_bytes)
print("block MiB            ", round(block_bytes / 2**20, 2))
seq = 1000
blocks = math.ceil(seq / block_tokens)
print("blocks for 1000 tok  ", blocks)
print("allocated tokens     ", blocks * block_tokens)
print("internal frag tokens ", blocks * block_tokens - seq)
print("frag overhead pct    ", round(100 * (blocks * block_tokens - seq) / seq, 2))
print("MiB for 1000 tokens  ", round(blocks * block_bytes / 2**20, 2))
shared = 1500
shared_blocks = math.ceil(shared / block_tokens)
print("shared prefix blocks ", shared_blocks)
print("prefix MiB reused    ", round(shared_blocks * block_bytes / 2**20, 1))
print("prefill tokens saved ", shared)
print("prefill ms saved at 3000 tok/s", round(shared / 3000 * 1000, 1))
print("KV for 64 seq at 1000 token MiB", round(64 * blocks * block_bytes / 2**20, 1))
print("contiguous 8192-token reservation MiB", round(math.ceil(8192 / block_tokens) * block_bytes / 2**20, 1))
PY
```

```text
bytes per token       131072
KiB per token         128.0
block bytes           2097152
block MiB             2.0
blocks for 1000 tok   63
allocated tokens      1008
internal frag tokens  8
frag overhead pct     0.8
MiB for 1000 tokens   126.0
shared prefix blocks  94
prefix MiB reused     188.0
prefill tokens saved  1500
prefill ms saved at 3000 tok/s 500.0
KV for 64 seq at 1000 token MiB 8064.0
contiguous 8192-token reservation MiB 1024.0
```

### ဥပမာ ၄ — Parallelism layout: device တစ်ခုလျှင် memory၊ communication နှင့် idle bubble

**ယူဆချက် —** parameter 70 ဘီလီယံ၊ fp16 (element တစ်ခုလျှင် 2 byte)၊ hidden 8,192၊ layer 80။
Tensor parallelism ကို device ၈ ခုတွင်၊ pipeline parallelism ကို stage ၈ ခုတွင် microbatch ၈ ခုနှင့်
လည်ပတ်သည်။ link လျင်မြန်မှု 600 GB/s၊ HBM bandwidth 3.35 TB/s။ batch 8၊ context 8,192၊
token တစ်ခုလျှင် KV 128 KiB။

**ဖော်မြူလာ —**
- weights = parameter × bits ÷ 8
- device တစ်ခုလျှင် weights = weights ÷ tensor parallel အရေအတွက်
- idle bubble အချိုး = (stage − 1) ÷ (microbatch + stage − 1)
- roofline tokens/s = bandwidth ÷ (device တစ်ခုလျှင် ဖတ်ရသည့် weights byte)
- collective communication byte (token တစ်ခုလျှင်) = layer × 2 × hidden × element byte

**တွက်ချက်မှု —**
1. weights = 70e9 × 16 ÷ 8 = 140.0 GB ဖြစ်သည်။ 80 GB card တစ်ခုတွင် မဝင်ပါ။
2. tensor parallelism ၈ ဖြင့် device တစ်ခုလျှင် 17.5 GB ဖြစ်သည်။ batch 8၊ 8k context တွင် KV သည်
   8.59 GB ဖြစ်သဖြင့် device တိုင်း 18.57 GB ဖြစ်သည် — 12 GB ချန်ထားသည့် 80 GB card တွင် ဝင်သည်။
3. roofline အရ device ၈ ခု ပေါင်းသည် 191.4 tokens/s (60 % efficiency တွင် 114.9 tokens/s) ဖြစ်သည်။
4. collective communication သည် token တစ်ခုလျှင် 2.62 MB ဖြစ်သည်၊ 600 GB/s link တွင် 4.4 µs ဖြစ်သည်၊
   decode step 4.18 ms ၏ 0.105 % သာ ဖြစ်သည် — ဆိုလိုသည်မှာ ဤ layout တွင် communication သည်
   ကန့်သတ်ချက် မဟုတ်ပါ။
5. pipeline တွင် stage တိုင်း 17.5 GB ဖြစ်သည်၊ သို့သော် stage ၈ ခု၊ microbatch ၈ ခုဖြင့်
   idle bubble သည် 46.7 % ဖြစ်သည် (အသုံးဝင်သည့် အချိုး 53.3 %)။ microbatch 32 ခုသို့ တိုးပါက
   bubble သည် 17.9 % သို့ ကျဆင်းသည်။

**ကောက်ချက် —** tensor parallelism သည် memory ကို ခွဲပြီး communication ကို တိုးသည်၊
pipeline parallelism သည် memory ကို ခွဲပြီး idle time ကို တိုးသည်။ မည်သည့်အရာက ပိုဆိုးသည်ကို
interconnect နှင့် microbatch schedule အပေါ် မူတည်၍ တိုင်းတာရမည်၊ "device အများဆုံး ရွေးခြင်း"
သည် အဖြေ မဖြစ်ပါ။

```bash
python3 - <<'PY'
params, bits = 70e9, 16
weights_gb = params * bits / 8 / 1e9
print("weights GB fp16      ", weights_gb)
for tp in (4, 8, 16):
    print("tensor parallel", tp, "GB per device", round(weights_gb / tp, 2))
hidden, layers, act_bpe = 8192, 80, 2
per_token_bytes = layers * 2 * hidden * act_bpe
print("activation all-reduce bytes per token", per_token_bytes)
print("activation all-reduce MB per token  ", round(per_token_bytes / 1e6, 2))
nvlink = 600e9
print("link time us per token at 600 GB/s  ", round(per_token_bytes / nvlink * 1e6, 1))
P, m = 8, 8
bubble = (P - 1) / (m + P - 1)
print("pipeline stages      ", P)
print("microbatches         ", m)
print("per stage GB fp16    ", round(weights_gb / P, 2))
print("idle bubble pct      ", round(100 * bubble, 1))
print("useful pct           ", round(100 * (1 - bubble), 1))
print("bubble with m=32 pct ", round(100 * (P - 1) / (32 + P - 1), 1))
print("bubble with P=4 m=8  ", round(100 * (4 - 1) / (8 + 4 - 1), 1))
bw = 3.35e12
print("roofline tokens/s single stream", round(bw / (weights_gb * 1e9), 1))
print("roofline tokens/s at 8 devices  ", round(8 * bw / (weights_gb * 1e9), 1))
print("roofline tokens/s at 16 devices ", round(16 * bw / (weights_gb * 1e9), 1))
PY
```

```text
weights GB fp16       140.0
tensor parallel 4 GB per device 35.0
tensor parallel 8 GB per device 17.5
tensor parallel 16 GB per device 8.75
activation all-reduce bytes per token 2621440
activation all-reduce MB per token   2.62
link time us per token at 600 GB/s   4.4
pipeline stages       8
microbatches          8
per stage GB fp16     17.5
idle bubble pct       46.7
useful pct            53.3
bubble with m=32 pct  17.9
bubble with P=4 m=8   27.3
roofline tokens/s single stream 23.9
roofline tokens/s at 8 devices   191.4
roofline tokens/s at 16 devices  382.9
```

## ၂။ တွက်ချက်ရသည့် လေ့ကျင့်ခန်းများ (Calculation Exercises)

လေ့ကျင့်ခန်း တစ်ခုစီတွင် ကိန်းဂဏန်း အဖြေ အတိအကျ ရှိသည်။ အဖြေနှင့် ဖော်မြူလာ ရှင်းလင်းချက်ကို
အပိုင်း ၅.၁ တွင် ပေးထားသည်။

**လေ့ကျင့်ခန်း ၁ — KV cache အရွယ်အစား**

layer 40 ခု၊ kv head 8 ခု၊ head_dim = 128၊ batch 32၊ sequence အရှည် 8,192၊ fp16 (element တစ်ခုလျှင်
2 byte)။ တွက်ရမည့် အချက်များ — (က) စုစုပေါင်း byte၊ (ခ) GiB၊ (ဂ) request တစ်ခုလျှင် MiB၊
(ဃ) request တစ်ခုအတွက် token တစ်ခုလျှင် KiB၊ (င) int8 ဖြစ်ပါက GiB၊ (စ) batch 8 သို့မဟုတ်
sequence 2,048 ဖြစ်ပါက GiB။

**လေ့ကျင့်ခန်း ၂ — 96 GB accelerator တွင် မော်ဒယ် မည်မျှ ထည့်နိုင်သည်**

96 GB accelerator တစ်ခုတွင် 10 GB ကို runtime၊ activation၊ KV cache နှင့် allocator အတွက် ချန်ထားသည်။
(က) 32B မော်ဒယ်ကို fp16၊ int8 နှင့် int4 ဖြင့် သိမ်းပါက မော်ဒယ် မည်မျှ ထည့်နိုင်သည်၊ (ခ) 8B မော်ဒယ်ကို
int8 ဖြင့် မည်မျှ၊ (ဂ) int4 32B တွင် metadata အပိုအလွှာ 12 % ရှိပါက GB နှင့် အရေအတွက် မည်မျှ၊
(ဃ) KV cache အတွက် 20 GiB သီးသန့် ချန်ထားပါက int4 32B မော်ဒယ် မည်မျှ။

**လေ့ကျင့်ခန်း ၃ — Roofline မှ tokens per second**

decode အဆင့်သည် memory-bandwidth-bound ဖြစ်သည်။ HBM bandwidth 3.35 TB/s၊ တစ်လှမ်းလျှင် ဖတ်ရသည့်
active weights 14 GB။ (က) weights ကိုသာ ရေတွက်ပါက tokens/s ၏ အပေါ်ဘောင်၊ (ခ) 60 % efficiency တွင်
tokens/s၊ (ဂ) weight တစ်ခုလုံး ဖတ်ရန် ကြာချိန် ms၊ (င) context 32,768 နှင့် batch 32 တွင်
token တစ်ခုလျှင် KV 128 KiB ဖြစ်ပါက တစ်လှမ်းလျှင် KV ဖတ်ရမည့် GB၊ (င) ထို တန်ဖိုးအပါအဝင်
step ကြာချိန် နှင့် tokens/s၊ (စ) KV က traffic ၏ မည်မျှ ရာခိုင်နှုန်းကို ယူသည်။

**လေ့ကျင့်ခန်း ၄ — GPU-hours နှင့် cost per million tokens**

aggregate output throughput 1,800 tokens/s၊ GPU-hour ခ $2.75။ (က) တစ်နာရီ tokens၊ (ခ) 1M output token
အတွက် GPU-hours၊ (ဂ) 1M output token အတွက် USD၊ (ဃ) 1K token အတွက် USD၊ (င) $1 လျှင် token အရေအတွက်၊
(စ) 5M output token အတွက် GPU-hours နှင့် USD၊ (ဆ) throughput ထက်ဝက် ကျဆင်းပါက 1M token ၏ USD။

**လေ့ကျင့်ခန်း ၅ — Batch size နှင့် inter-token latency SLO**

decode step ကြာချိန်ကို t(b) = 14 + 1.9b ms အဖြစ် တိုင်းတာရရှိသည်။ per-request inter-token latency ၏
p95 သည် 60 ms အောက် ရှိရမည် ဟု SLO သတ်မှတ်ထားသည်။ (က) batch 1၊ 8၊ 16 နှင့် 24 တွင် step ကြာချိန်
နှင့် aggregate tokens/s၊ (ခ) 60 ms အတွင်း ဝင်သည့် အကြီးဆုံး batch၊ (ဂ) 20 % အနားသတ် ထားပါက
အကြီးဆုံး batch၊ (ဃ) အနားသတ် batch တွင် ဆုံးရှုံးသည့် throughput ရာခိုင်နှုန်း၊ (င) batch 24 နှင့် 32 ၏
step ကြာချိန် ကွာခြားမှု။

**လေ့ကျင့်ခန်း ၆ — လိုအပ်သည့် replica အရေအတွက်**

replica တစ်ခုသည် SLO အတွင်း request 12 req/s ကို ဆောင်ရွက်နိုင်သည်။ arrival rate သည် peak တွင်
95 req/s၊ off-peak တွင် 30 req/s။ (က) peak အတွက် လိုအပ်သည့် replica အနည်းဆုံး အရေအတွက်၊
(ခ) off-peak အတွက်၊ (ဂ) spare တစ်ခု ထည့်ပါက peak ၏ အရေအတွက်၊ (ဃ) replica ၈ ခုတွင် ကျန်သည့်
headroom ရာခိုင်နှုန်း၊ (င) per-replica စွမ်းရည်သည် 9 req/s သို့ ကျဆင်းပါက လိုအပ်သည့် အရေအတွက်၊
(စ) replica တစ်ခုလျှင် $3.10 ဖြစ်ပါက replica ၈ ခု၏ တစ်နာရီ ကုန်ကျစရိတ်။

## ၃။ ပြဿနာ ရှာဖွေခြင်း (Troubleshooting Scenarios)

ပြဿနာ တစ်ခုစီကို symptom၊ တိုင်းတာရမည့် အချက်၊ ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်)၊
ဖြေရှင်းနည်းနှင့် ရှင်းလင်းသည့် term ဟူသည့် အစဉ်အတိုင်း ဖော်ပြထားသည်။ အကြောင်းရင်း အစဉ်သည်
တိုင်းတာမှုဖြင့် ရှာဖွေနိုင်သည့် အစဉ်အတိုင်း ဖြစ်သည်။ အသေးစိတ် ရှင်းလင်းချက်ကို အပိုင်း ၅.၂ တွင်
ပေးထားသည်။

### ပြဿနာ ၁ — Concurrency မြင့်လာသည့်အခါ throughput ပြိုလဲသည်

- **Symptom —** request အရေအတွက် တိုးသည့်အခါ aggregate tokens per second သည် တိုးမလာဘဲ
  ကျဆင်းသည်၊ per-request latency လည်း ပို၍ နှေးလာသည်။ ပြီးစီးသည့် request အရေအတွက်သည်
  ဝင်လာသည့် အရေအတွက်ထက် နည်းလာသည်။
- **တိုင်းတာရမည့် အချက် —** queue depth နှင့် queue wait time၊ KV cache အသုံးပြုမှု ရာခိုင်နှုန်း၊
  preemption (ဖြုတ်ချခံရမှု) အရေအတွက်၊ တကယ် လည်ပတ်နေသည့် batch အရေအတွက်၊ decode step
  ကြာချိန်၏ concurrency အလိုက် ပြောင်းလဲမှု၊ prefill ကြောင့် decode ရပ်တန့်သည့် အကြိမ်အရေအတွက်။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) KV cache memory ပြည့်၍ request များ
  ဖြုတ်ချခံရပြီး prompt ကို ပြန်လည် တွက်ချက်ရခြင်း၊ (၂) prompt ရှည်သည့် request များ၏ prefill သည်
  decode ကို ရပ်တန့်စေခြင်း၊ (၃) admission control မရှိဘဲ batch အပြည့် ဖြစ်နေသဖြင့် step ကြာချိန်
  အချိုးမကျ တိုးလာခြင်း၊ (၄) မညီညာသည့် request shape များကြောင့် တွက်ချက်မှု လွင့်ခြင်း။
- **ဖြေရှင်းနည်း —** admission control ဖြင့် တစ်ချိန်တည်း request အရေအတွက်ကို ကန့်သတ်ရမည်၊
  `Paged KV Cache` နှင့် `Chunked Prefill` ကို ဖွင့်ရမည်၊ live batch သို့မဟုတ် KV budget ပြည့်သည့်အခါ
  backpressure ထည့်ရမည်။
- **ရှင်းလင်းသည့် term —** Continuous Batching, Paged KV Cache, Chunked Prefill, Goodput။

### ပြဿနာ ၂ — TTFT မြင့်လာသည်၊ သို့သော် Tokens per Second မပြောင်းလဲ

- **Symptom —** ပထမ token အထိ စောင့်ချိန် (TTFT) သည် သိသိသာသာ တိုးလာသည်၊ သို့သော် output စပြီးနောက်
  generation နှုန်းနှင့် aggregate tokens per second သည် မပြောင်းလဲပါ။
- **တိုင်းတာရမည့် အချက် —** queue ကြာချိန် နှင့် လည်ပတ်ချိန်ကို ခွဲထားခြင်း၊ prefill token အရေအတွက်
  နှင့် prefill latency၊ prefix cache ၏ hit rate၊ decode step ကြာချိန်၊ တစ်ချိန်တည်း ရှိသည့် decode အရေအတွက်၊
  prompt အရှည်၏ ဖြန့်ကျက်မှု ပုံစံ။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) prompt token များ ရှည်လာခြင်း (retrieval သို့မဟုတ်
  history ကြီးလာခြင်း)၊ (၂) prefix cache hit rate ကျဆင်း၍ မျှဝေသည့် prefix ကို ပြန်တွက်ရခြင်း၊
  (၃) queue ကြာချိန် တိုးလာခြင်း — ဆိုလိုသည်မှာ capacity မလုံလောက်ခြင်း၊ (၄) prefill နှင့် decode
  ကို တစ်ခုတည်းသော pool တွင် ရောထားသဖြင့် ရှည်သည့် prompt က decode ကို နှောင့်နှေးစေခြင်း။
- **ဖြေရှင်းနည်း —** prompt token ကို မှတ်တမ်းတင်ပြီး cache identity တွင် model နှင့် tokenizer
  version ထည့်ရမည်၊ တည်ငြိမ်သည့် token များကို request သီးသန့် အကြောင်းအရာ မတိုင်မီ ထားရမည်၊
  `Chunked Prefill` ဖြင့် ရောနှောရမည်၊ လိုအပ်ပါက `Disaggregated Serving` ဖြင့် pool ခွဲရမည်။
- **ရှင်းလင်းသည့် term —** Prefill, Prefix Caching, Chunked Prefill, Disaggregated Serving, Tokens per Second (TPS)။

### ပြဿနာ ၃ — Replica တစ်ခုသည် အမွှာ တစ်ခုထက် သိသိသာသာ လျော့ ဆောင်ရွက်သည်

- **Symptom —** တူညီသည့် မော်ဒယ်၊ တူညီသည့် hardware၊ တူညီသည့် configuration ရှိသည့် replica နှစ်ခုတွင်
  တစ်ခုက goodput ပိုနည်းသည်၊ အချို့အခါ ထက်ဝက်နီးပါး နည်းသည်။ traffic မျှဝေမှုလည်း မညီပါ။
- **တိုင်းတာရမည့် အချက် —** replica တိုင်း၏ per-replica goodput၊ ရရှိသည့် request အရေအတွက်၊
  readiness check အောင်ချိန် နှင့် traffic စတင်ရရှိချိန်၊ model version နှင့် tokenizer version၊
  parallelism configuration (tensor နှင့် pipeline layout)၊ load balancer ၏ session affinity နှင့်
  health check interval။
- **ဖြစ်နိုင်သည့် အကြောင်းရင်း (အစဉ်လိုက်) —** (၁) layout မတူညီခြင်း — pipeline stage အရေအတွက်
  သို့မဟုတ် tensor partition မတူသဖြင့် idle bubble အချိုး ကွာခြင်းခြင်း၊ (၂) version မတူညီခြင်း
  (အဟောင်း revision က traffic ရနေခြင်း)၊ (၃) readiness check ကောင်းစွာ မစစ်ဘဲ traffic ရရှိခြင်း
  သို့မဟုတ် warm-up မပြီးမီ ရရှိခြင်း၊ (၄) တစ်ခုသည် session အရှည်ကြီး သို့မဟုတ် prompt ရှည်သည့်
  request များ ပို၍ ရရှိခြင်း (load balancing မညီခြင်း)။
- **ဖြေရှင်းနည်း —** sharding layout ကို checkpoint နှင့် serving configuration နှင့်အတူ မှတ်တမ်းတင်ပြီး
  replica အားလုံး တူညီစေရမည်၊ readiness နှင့် latency signal များကို replica အလိုက် ဖော်ထုတ်ရမည်၊
  rollout ကို ပြီးဆုံးစေပြီး အဟောင်း replica များကို ဖယ်ရှားရမည်၊ prefix အလိုက် routing ဖြင့်
  `Prefix Caching` ၏ hit rate ကို ထိန်းရမည်။
- **ရှင်းလင်းသည့် term —** Tensor Parallelism, Pipeline Parallelism, Autoscaling, Prefix Caching, Model Serving။

## ၄။ ဆုံးဖြတ်ချက် လေ့ကျင့်ခန်းများ (Design Decisions)

### ဆုံးဖြတ်ချက် ၁ — 70B မော်ဒယ်၏ serving topology

**အခြေအနေ —** 70B မော်ဒယ် (fp16) တစ်ခုကို ဖွင့်တင်မည်။ 80 GB accelerator ၈ ခုရှိသည့် node တစ်ခု
ရနိုင်သည်၊ သို့မဟုတ် 80 GB accelerator ၄ ခုရှိသည့် node နှစ်ခု ရနိုင်သည်။ မော်ဒယ်ကို fp16 ဖြင့်
သိမ်းမည် (quantization မလုပ်ပါ)။ batch 8၊ context 8,192၊ token တစ်ခုလျှင် KV 128 KiB။
GPU-hour ခ $2.75၊ HBM bandwidth 3.35 TB/s၊ link 600 GB/s။

**လဲလှယ်မှု —** node တစ်ခုတွင် tensor parallelism ၈ ဖြင့် device တိုင်း 17.5 GB ဖြစ်ပြီး
communication သည် decode step ၏ 0.105 % သာ ယူသည် — ဆိုလိုသည်မှာ interconnect သည်
ကန့်သတ်ချက် မဟုတ်ပါ။ node နှစ်ခုတွင် pipeline သုံးပါက microbatches များစွာ လိုသည်၊
microbatch ၈ ခုဖြင့် idle bubble သည် 46.7 % ဖြစ်သည် (node တစ်ခုတွင် stage ၄ ခုဖြစ်ပါက 27.3 %)။
node အကြား link သည် node အတွင်း link ထက် နှေးသဖြင့် pipeline သည် ပို၍ ဆိုးသည်။
သို့သော် node တစ်ခုတည်း သုံးပါက failure domain တစ်ခုတည်း ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** node တစ်ခုတည်းတွင် tensor parallelism ၈ ဖြင့် ဖွင့်တင်ရမည်။ အကြောင်းမှာ
device တိုင်း 18.57 GB (weights + KV) သာ လိုသဖြင့် 12 GB ချန်ထားသည့် card တွင် ဝင်သည်၊
roofline အရ 191.4 tokens/s ရနိုင်သည်၊ communication ကုန်ကျစရိတ် 0.105 % သည်
pipeline bubble ၏ ဆယ်ပုံတစ်ပုံအောက် ရှိသည်။ node နှစ်ခု လိုအပ်သည့် အခြေအနေမှာ
host memory မလုံလောက်ခြင်း၊ accelerator ၈ ခု မရရှိနိုင်ခြင်း သို့မဟုတ် failure domain ကို
ခွဲလိုခြင်း ဖြစ်သည်။

**တိုင်းတာမည့် metric —** per-replica `Goodput`၊ decode step ကြာချိန်၊
`Time per Output Token (TPOT)` ၏ p95၊ 1M output token လျှင် USD။

### ဆုံးဖြတ်ချက် ၂ — Autoscaling မူဝါဒနှင့် minimum warm capacity

**အခြေအနေ —** replica တစ်ခုသည် SLO အတွင်း 9.4 req/s ကို ဆောင်ရွက်နိုင်သည်။ arrival rate သည်
off-peak 6.5 req/s၊ နေ့ခင်း 18 req/s၊ ညနေ 31 req/s၊ peak 47 req/s။ replica တစ်ခုလျှင်
တစ်နာရီ $3.10။ မော်ဒယ် ဖွင့်တင်ရန် ကြာချိန်သည် မိနစ် အတော်အသင့် ကြာသည်။
queue အရွယ်အစားကို request 60 ခုတွင် ကန့်သတ်ထားသည်။

**လဲလှယ်မှု —** replica ၅ ခုဖြင့် peak တွင် utilisation သည် 100.0 % ဖြစ်သည် — ဆိုလိုသည်မှာ
အနားသတ် လုံးဝ မကျန်၊ queue သည် ငြိမ်မနေနိုင်ပါ။ replica ၆ ခုဖြင့် 83.3 % ဖြစ်သည်၊
တစ်လလျှင် $13,392 ဖြစ်သည်။ replica ၄ ခုဖြင့် peak ကို ဆောင်ရွက်ပါက ကျန်သည့်
9.4 req/s သည် queue ထဲ စုပုံပြီး request 60 ခုရှိသည့် queue သည် 6.4 s အတွင်း ပြည့်သည် —
ဆိုလိုသည်မှာ request များ စတင် ပယ်ခံရသည်။ off-peak တွင် replica ၂ ခုဖြင့် utilisation သည်
34.6 % သာ ဖြစ်သည်၊ တစ်လလျှင် $4,464 ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** minimum warm capacity ကို replica ၂ ခုတွင် သတ်မှတ်ရမည် (off-peak ကို
ဖုံးလွှမ်းသည်၊ model load ကြာချိန်ကို ကျော်လွှားရန် ၂ ခု လိုသည်)၊ scale-up ကို replica ၆ ခုအထိ
ခွင့်ပြုရမည် (peak ၏ 83.3 %၊ အနားသတ် ကျန်သည်)၊ scale-down ကို တစ်ကြိမ်လျှင် replica တစ်ခုသာ
၍ cooldown ကာလ သတ်မှတ်ရမည် (churn ကန့်သတ်ရန်)။ signal အဖြစ် queue wait time နှင့်
per-replica `Goodput` ကို အသုံးပြုရမည်၊ CPU အသုံးပြုမှုကို မသုံးရ၊ အကြောင်းမှာ decode အဆင့်သည်
memory-bandwidth-bound ဖြစ်သဖြင့် CPU metric သည် အသုံးဝင်သည့် အလုပ်နှင့် မချိတ်ဆက်ပါ။

**တိုင်းတာမည့် metric —** `Goodput` (သဘောတူညီချက် ပြည့်မီသည့် request နှုန်း)၊ queue wait time ၏ p95၊
replica တိုင်း၏ readiness အောင်ချိန်၊ တစ်လလျှင် USD။

## ၅။ အဖြေများ (Answers with Explanations)

### ၅.၁ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း အဖြေများ

#### အဖြေ ၁ — KV cache အရွယ်အစား

**ဖော်မြူလာ —** bytes = 2 × layer × batch × sequence × kv head × head_dim × element byte။
ယူဆချက် — fp16 ဖြစ်၍ element တစ်ခုလျှင် 2 byte၊ key နှင့် value နှစ်ခုလုံးကို သိမ်းသည်၊
paging အတွက် အပိုအလွှာ မရှိပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. 2 × 40 × 8 × 128 × 2 × 32 × 8,192 = 42,949,672,960 byte ဖြစ်သည်။
2. 1,073,741,824 ဖြင့် စားပါက 40.0 GiB ဖြစ်သည်။
3. request တစ်ခုလျှင် 40.0 GiB ÷ 32 = 1,280.0 MiB ဖြစ်သည်။
4. request တစ်ခုအတွက် token တစ်ခုလျှင် 1,280.0 MiB ÷ 8,192 = 160.0 KiB ဖြစ်သည်။
5. int8 ဖြစ်ပါက element တစ်ခုလျှင် 1 byte ဖြစ်သဖြင့် 20.0 GiB သို့ ကျဆင်းသည်။
6. batch 8 ဖြစ်ပါက 10.0 GiB၊ sequence 2,048 ဖြစ်ပါက 10.0 GiB ဖြစ်သည် — နှစ်ခုလုံးသည်
   တူညီသည့် ပမာဏ အလျော့အကျကို ပေးသည်၊ အကြောင်းမှာ batch နှင့် sequence နှစ်ခုလုံးကို
   တိုက်ရိုက် မြှောက်သောကြောင့် ဖြစ်သည်။

**အဓိပ္ပာယ် —** 40.0 GiB သည် 80 GB card တစ်ခု၏ ထက်ဝက်နီးပါး ဖြစ်သည်။ ထို့ကြောင့် concurrency
မြင့်သည့် serving တွင် ပြည့်လာသည့် ပထမဆုံး အရင်းအမြစ်သည် weights မဟုတ်ဘဲ KV cache ဖြစ်လေ့ ရှိသည်။
int8 cache သို့မဟုတ် `Paged KV Cache` သည် ထို ကန့်သတ်ချက်ကို တိုက်ရိုက် သက်ရောက်သည်။

```bash
python3 - <<'PY'
import math
layers, kv_heads, head_dim, batch, seq, bpe = 40, 8, 128, 32, 8192, 2
kv = 2 * layers * kv_heads * head_dim * bpe * batch * seq
print("bytes          ", kv)
print("GiB            ", round(kv / 2**30, 2))
print("MiB per request", round(kv / batch / 2**20, 1))
print("KiB per token per request", round(kv / batch / seq / 1024, 2))
print("at int8 GiB    ", round(kv / 2 / 2**30, 2))
print("at batch 8 GiB ", round(kv / 4 / 2**30, 2))
print("at seq 2048 GiB", round(kv / 4 / 2**30, 2))
PY
```

```text
bytes           42949672960
GiB             40.0
MiB per request 1280.0
KiB per token per request 160.0
at int8 GiB     20.0
at batch 8 GiB  10.0
at seq 2048 GiB 10.0
```

#### အဖြေ ၂ — 96 GB accelerator တွင် မော်ဒယ် မည်မျှ ထည့်နိုင်သည်

**ဖော်မြူလာ —** weight GB = parameter × bits ÷ 8 ÷ 10⁹၊ ထည့်နိုင်သည့် အရေအတွက် =
floor(usable GB ÷ weight GB)။ ယူဆချက် — usable = 96 − 10 = 86 GB၊ sharding မလုပ်ပါ၊
metadata မပါပါ။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. 32B: fp16 = 64.0 GB (1 ခု)၊ int8 = 32.0 GB (2 ခု)၊ int4 = 16.0 GB (5 ခု) ဖြစ်သည်။
2. 8B int8 = 8.0 GB (10 ခု) ဖြစ်သည်။
3. int4 တွင် metadata 12 % ထည့်ပါက 16.0 × 1.12 = 17.92 GB ဖြစ်သည်၊ ထို့ကြောင့် 5 ခု အစား
   4 ခု သာ ထည့်နိုင်သည်။
4. KV cache အတွက် 20 GiB ချန်ထားပါက ကျန်သည့် 66 GB တွင် int4 32B မော်ဒယ် 4 ခု ထည့်နိုင်သည်။

**အဓိပ္ပာယ် —** parameter အရေအတွက်သည် memory ကို တိုက်ရိုက် မဆုံးဖြတ်ပါ၊ numerical format နှင့်
metadata က ဆုံးဖြတ်သည်။ metadata 12 % ကပင် အရေအတွက်ကို 5 မှ 4 သို့ လျှော့ချနိုင်သည်၊
ထို့ကြောင့် allocator အပိုအလွှာကို တွက်ချက်မှုတွင် ထည့်ရမည်။

```bash
python3 - <<'PY'
import math
card, reserved = 96, 10
usable = card - reserved
print("usable GB", usable)
for name, gb in (("32B fp16", 64.0), ("32B int8", 32.0), ("32B int4", 16.0), ("8B int8", 8.0)):
    print(f"{name}: {gb} GB -> copies {math.floor(usable / gb)}")
print("32B int4 with 12 pct metadata GB", round(16.0 * 1.12, 2))
print("copies with metadata            ", math.floor(usable / (16.0 * 1.12)))
print("KV 20 GiB subtracted from 32B int4 copies", math.floor((usable - 20) / 16.0))
PY
```

```text
usable GB 86
32B fp16: 64.0 GB -> copies 1
32B int8: 32.0 GB -> copies 2
32B int4: 16.0 GB -> copies 5
8B int8: 8.0 GB -> copies 10
32B int4 with 12 pct metadata GB 17.92
copies with metadata             4
KV 20 GiB subtracted from 32B int4 copies 4
```

#### အဖြေ ၃ — Roofline မှ tokens per second

**ဖော်မြူလာ —** tokens/s အပေါ်ဘောင် = bandwidth ÷ (တစ်လှမ်းလျှင် ဖတ်ရသည့် byte)။
ယူဆချက် — decode အဆင့်သည် memory-bandwidth-bound ဖြစ်သည်၊ compute သည် ကန့်သတ်ချက် မဟုတ်ပါ၊
batch တွင် sequence တိုင်းက weights ကို မျှဝေ ဖတ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. weights ကိုသာ ရေတွက်ပါက 3.35e12 ÷ 14e9 = 239.3 tokens/s ဖြစ်သည်။
2. 60 % efficiency တွင် 143.6 tokens/s ဖြစ်သည်။
3. weight တစ်ခုလုံး ဖတ်ရန် 14e9 ÷ 3.35e12 = 4.18 ms ဖြစ်သည်။
4. context 32,768၊ batch 32 တွင် တစ်လှမ်းလျှင် KV ဖတ်ရမည့် ပမာဏ = 32 × 32,768 × 128 KiB
   = 137.44 GB ဖြစ်သည်။
5. weights အပါအဝင် 151.44 GB ဖြစ်သဖြင့် step ကြာချိန် 45.2 ms၊ tokens/s 707.9 ဖြစ်သည်။
6. KV သည် traffic ၏ 90.8 % ကို ယူသည် — ဆိုလိုသည်မှာ context ရှည်သည့် workload တွင်
   bandwidth ကို KV cache က လွှမ်းမိုးသည်။
7. weights ကိုသာ ရေတွက်သည့် စံနှုန်းဖြင့် batch 32 သည် 7,657.1 tokens/s ဟု ရနိုင်သော်လည်း
   ထို တန်ဖိုးသည် KV traffic မပါသော အပေါ်ဘောင် ဖြစ်သည်၊ တကယ့် စနစ်တွင် မရနိုင်ပါ။

**အဓိပ္ပာယ် —** roofline သည် tokens/s ၏ အပေါ်ဘောင် ကို ပေးသည်၊ သို့သော် ထို အပေါ်ဘောင်သည်
batch ကြီးလာသည့်အခါ KV cache ၏ traffic ကြောင့် တိုက်ရိုက် ကျဆင်းသည်။ ထို့ကြောင့်
`Paged KV Cache` နှင့် `Prefix Caching` သည် bandwidth ကို ချွေတာသည့် တိုင်းတာချက် ဖြစ်လာသည်။

```bash
python3 - <<'PY'
bw = 3.35e12
active_gb = 14.0
kv_kib_per_token = 128.0
print("bandwidth TB/s            ", bw / 1e12)
print("active weights GB         ", active_gb)
print("weights only tokens/s     ", round(bw / (active_gb * 1e9), 1))
print("at 60 pct efficiency      ", round(0.6 * bw / (active_gb * 1e9), 1))
print("time for one weight read ms", round(active_gb * 1e9 / bw * 1000, 2))
ctx, batch = 32768, 32
kv_step_gb = batch * ctx * kv_kib_per_token * 1024 / 1e9
print("KV read per step GB       ", round(kv_step_gb, 2))
print("weights plus KV per step GB", round(active_gb + kv_step_gb, 2))
print("step time ms bound        ", round((active_gb + kv_step_gb) * 1e9 / bw * 1000, 1))
print("tokens/s at that bound    ", round(batch / ((active_gb + kv_step_gb) * 1e9 / bw), 1))
print("weights only tps at batch 32", round(32 * bw / (active_gb * 1e9), 1))
print("share of traffic from KV pct", round(100 * kv_step_gb / (active_gb + kv_step_gb), 1))
print("at context 4096 KV step GB", round(batch * 4096 * kv_kib_per_token * 1024 / 1e9, 2))
PY
```

```text
bandwidth TB/s             3.35
active weights GB          14.0
weights only tokens/s      239.3
at 60 pct efficiency       143.6
time for one weight read ms 4.18
KV read per step GB        137.44
weights plus KV per step GB 151.44
step time ms bound         45.2
tokens/s at that bound     707.9
weights only tps at batch 32 7657.1
share of traffic from KV pct 90.8
at context 4096 KV step GB 17.18
```

#### အဖြေ ၄ — GPU-hours နှင့် cost per million tokens

**ဖော်မြူလာ —** tokens per hour = tokens/s × 3,600၊ GPU-hours per 1M = 10⁶ ÷ tokens per hour၊
USD per 1M = GPU-hour ခ × 10⁶ ÷ tokens per hour။ ယူဆချက် — throughput သည် တိုင်းတာကာလ
တစ်လျှောက်လုံး တည်ငြိမ်သည်၊ GPU တစ်ခုကို အပြည့် အသုံးပြုသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. တစ်နာရီ tokens = 1,800 × 3,600 = 6,480,000 ဖြစ်သည်။
2. GPU-hours per 1M = 10⁶ ÷ 6,480,000 = 0.1543 ဖြစ်သည်။
3. USD per 1M = 2.75 × 0.1543 = $0.4244 ဖြစ်သည်။
4. USD per 1K = $0.000424 ဖြစ်သည်၊ $1 လျှင် 2,356,364 token ရသည်။
5. 5M output token အတွက် 0.7716 GPU-hour၊ $2.12 ဖြစ်သည်။
6. throughput ထက်ဝက် ကျဆင်းပါက cost သည် 2 ဆ တိုးပြီး $0.8488 ဖြစ်သည်။

**အဓိပ္ပာယ် —** cost per million သည် throughput နှင့် တစ်ပြန်တစ်လှည့် အချိုးကျသည်။
ထို့ကြောင့် `Tokens per Second (TPS)` ကို batch၊ concurrency၊ sequence အရှည်နှင့် hardware
ပါ ဖော်ပြရမည် — မဖော်ပြဘဲ နှိုင်းယှဉ်ခြင်းသည် cost ခန့်မှန်းချက်ကို အဓိပ္ပာယ် မဲ့စေသည်။

```bash
python3 - <<'PY'
tps, price = 1800.0, 2.75
per_hour = tps * 3600
print("tokens per hour      ", round(per_hour))
print("GPU-hours per 1M out ", round(1e6 / per_hour, 4))
print("USD per 1M tokens    ", round(price * 1e6 / per_hour, 4))
print("USD per 1K tokens    ", round(price * 1e3 / per_hour, 6))
print("tokens per USD       ", round(per_hour / price))
print("GPU-hours for 5M out ", round(5e6 / per_hour, 4))
print("USD for 5M out       ", round(5e6 / per_hour * price, 2))
print("if tps halves, USD per 1M", round(price * 1e6 / (per_hour / 2), 4))
print("20 replicas same rate, USD per 1M",
      round(20 * price * 1e6 / (20 * per_hour), 4))
print("USD per hour one replica", round(price * 1e6 / per_hour * per_hour / 1e6, 2))
PY
```

```text
tokens per hour       6480000
GPU-hours per 1M out  0.1543
USD per 1M tokens     0.4244
USD per 1K tokens     0.000424
tokens per USD        2356364
GPU-hours for 5M out  0.7716
USD for 5M out        2.12
if tps halves, USD per 1M 0.8488
20 replicas same rate, USD per 1M 0.4244
USD per hour one replica 2.75
```

#### အဖြေ ၅ — Batch size နှင့် inter-token latency SLO

**ဖော်မြူလာ —** t(b) = 14 + 1.9b ms၊ aggregate tokens/s = b ÷ (t(b) ÷ 1,000)။
ယူဆချက် — step ကြာချိန်သည် batch အပေါ် linear တိုးသည်၊ inter-token latency သည်
တစ်လှမ်းလျှင် ကြာချိန် ဖြစ်သည် (batch ထဲရှိ request တိုင်း တူညီသည်)၊ SLO သည် p95 အပေါ်
သတ်မှတ်သည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. batch 1: 15.90 ms၊ 62.9 tokens/s ဖြစ်သည်။
2. batch 8: 29.20 ms၊ 274.0 tokens/s ဖြစ်သည်။
3. batch 16: 44.40 ms၊ 360.4 tokens/s ဖြစ်သည်။
4. batch 24: 59.60 ms၊ 402.7 tokens/s ဖြစ်သည်။
5. 60 ms အတွင်း ဝင်သည့် အကြီးဆုံး batch = 24 ဖြစ်သည်၊ batch 25 သည် 61.50 ms ဖြစ်၍ ကျော်လွန်သည်။
6. 20 % အနားသတ် (48 ms) ထားပါက အကြီးဆုံး batch = 17 ဖြစ်သည်၊ ဆုံးရှုံးသည့် throughput သည် 8.8 % ဖြစ်သည်။
7. batch 32 သည် 74.80 ms ဖြစ်သဖြင့် SLO ကို 24.8 % ကျော်လွန်သည် — p95 အတွက် မသင့်လျော်ပါ။

**အဓိပ္ပာယ် —** aggregate tokens/s သည် batch ကြီးလာသည့်အခါ အမြဲ တိုးသော်လည်း
per-request inter-token latency သည် batch နှင့်အတူ တိုက်ရိုက် တိုးသည်။ ထို့ကြောင့်
batching policy ကို metric နှစ်ခုဖြင့် တိုင်းရမည်၊ throughput တစ်ခုတည်းဖြင့် မဆုံးဖြတ်ရ။

```bash
python3 - <<'PY'
ms = lambda b: 14.0 + 1.9 * b
slo = 60.0
print("batch  1 step ms", round(ms(1), 2), "tps", round(1000 / ms(1), 1))
for b in (8, 16, 24, 25, 32, 48):
    print(f"batch {b:3} step {ms(b):6.2f} ms  aggregate tps {b / (ms(b)/1000):6.1f}  per request tps {1000/ms(b):5.2f}")
print("largest batch within 60 ms SLO  ", max(b for b in range(1, 129) if ms(b) <= slo))
print("largest batch with 20 pct margin", max(b for b in range(1, 129) if ms(b) <= slo * 0.8))
print("throughput lost pct at margin batch",
      round(100 * (24 / (ms(24)/1000) - 17 / (ms(17)/1000)) / (24 / (ms(24)/1000)), 1))
PY
```

```text
batch  1 step ms 15.9 tps 62.9
batch   8 step  29.20 ms  aggregate tps  274.0  per request tps 34.25
batch  16 step  44.40 ms  aggregate tps  360.4  per request tps 22.52
batch  24 step  59.60 ms  aggregate tps  402.7  per request tps 16.78
batch  25 step  61.50 ms  aggregate tps  406.5  per request tps 16.26
batch  32 step  74.80 ms  aggregate tps  427.8  per request tps 13.37
batch  48 step 105.20 ms  aggregate tps  456.3  per request tps  9.51
largest batch within 60 ms SLO   24
largest batch with 20 pct margin 17
throughput lost pct at margin batch 8.8
```

#### အဖြေ ၆ — လိုအပ်သည့် replica အရေအတွက်

**ဖော်မြူလာ —** replica အနည်းဆုံး အရေအတွက် = ceil(arrival rate ÷ per-replica စွမ်းရည်)။
ယူဆချက် — per-replica စွမ်းရည် 12 req/s သည် SLO အတွင်း တည်ငြိမ်သည်၊
request များ replica များအကြား ညီညာစွာ ခွဲဝေခံရသည်။

**အဆင့်ဆင့် တွက်ချက်မှု —**
1. peak: ceil(95 ÷ 12) = 8 ဖြစ်သည်။
2. off-peak: ceil(30 ÷ 12) = 3 ဖြစ်သည်။
3. spare တစ်ခု ထည့်ပါက peak တွင် 9 ဖြစ်သည်။
4. replica 8 ခုတွင် စွမ်းရည် 96 req/s ဖြစ်သဖြင့် headroom သည် 1.1 % သာ ဖြစ်သည် —
   ဆိုလိုသည်မှာ queue wait time သည် ချက်ချင်း တိုးလာနိုင်သည့် အနေအထား ဖြစ်သည်။
5. per-replica စွမ်းရည်သည် 9 req/s သို့ ကျဆင်းပါက ceil(95 ÷ 9) = 11 ဖြစ်သည်။
6. replica 8 ခု၊ တစ်ခုလျှင် $3.10 ဖြစ်ပါက တစ်နာရီ $24.80 ဖြစ်သည်။

**အဓိပ္ပာယ် —** replica အရေအတွက်သည် per-replica စွမ်းရည်ပေါ် တိုက်ရိုက် မှီခိုသည်၊ ထို စွမ်းရည်
ကိုယ်တိုင်သည် batch policy၊ prompt အရှည်နှင့် KV cache budget အပေါ် မှီခိုသည်။ ထို့ကြောင့်
`Autoscaling` ကို မတိုင်းတာရသေးသည့် per-replica ကိန်းဂဏန်း တစ်ခုအပေါ် အခြေခံ၍ မချိန်ရ။

```bash
python3 - <<'PY'
import math
per_replica, peak, off_peak = 12.0, 95.0, 30.0
print("replicas for peak      ", math.ceil(peak / per_replica))
print("replicas for off peak  ", math.ceil(off_peak / per_replica))
print("replicas peak plus one spare", math.ceil(peak / per_replica) + 1)
print("goodput at 8 replicas  ", 8 * per_replica)
print("headroom pct at 8      ", round(100 * (8 * per_replica - peak) / peak, 1))
print("drain time s for 20 requests at 12 req/s", round(20 / per_replica, 2))
print("replicas if per replica drops to 9", math.ceil(peak / 9.0))
print("cost per hour at 3.10 USD each, 8 replicas", round(8 * 3.10, 2))
PY
```

```text
replicas for peak       8
replicas for off peak   3
replicas peak plus one spare 9
goodput at 8 replicas   96.0
headroom pct at 8       1.1
drain time s for 20 requests at 12 req/s 1.67
replicas if per replica drops to 9 11
cost per hour at 3.10 USD each, 8 replicas 24.8
```

### ၅.၂ ပြဿနာ ရှာဖွေခြင်း အဖြေများ

#### အဖြေ ၁ — Concurrency မြင့်လာသည့်အခါ throughput ပြိုလဲခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** KV cache သည် sequence အရှည်၊ layer၊ kv head နှင့် batch အပေါ်
တိုက်ရိုက် အချိုးကျ ကြီးထွားသည် (အဖြေ ၁ တွင် batch 32၊ 8k context အတွက် 40.0 GiB)။
concurrency တိုးသည့်အခါ KV cache သည် VRAM ကို အပြည့် ယူပြီး serving system သည်
request တစ်ခုကို ဖြုတ်ချကာ ၎င်း၏ KV state ကို ဖျက်သည်။ ထို request ပြန်လာသည့်အခါ
prompt ကို အစမှ ပြန်တွက်ရသဖြင့် အလုပ်ပမာဏ ထပ်တလဲလဲ တိုးပြီး throughput ကျဆင်းသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** KV cache အသုံးပြုမှုနှင့် preemption အရေအတွက်ကို တိုင်းပါ။
KV အသုံးပြုမှု 90 % ကျော်ပြီး preemption ရှိပါက အကြောင်းရင်း (၁) ဖြစ်သည်။
prefill ကြာသည့် request များ ရောက်လာစဉ်တွင် decode ရပ်တန့်သည့် အကြိမ်အရေအတွက် မြင့်ပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။ step ကြာချိန်သည် batch နှင့်အတူ linear ထက် ပိုတိုးပါက
အကြောင်းရင်း (၃) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** admission control ထည့်ပြီးနောက် throughput သည်
linear နီးပါး ပြန်တိုးပါက ပြဿနာသည် memory အပေါ် အခြေခံသည့် ဖြစ်သည်။
`Paged KV Cache` သည် block များကို ပြန်သုံးနိုင်သဖြင့် တူညီသည့် VRAM တွင် request ပိုများ ထည့်နိုင်သည်။

#### အဖြေ ၂ — TTFT မြင့်လာခြင်း၊ Tokens per Second မပြောင်းလဲခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** TTFT သည် queue ကြာချိန် နှင့် `Prefill` အပေါ် မှီခိုသည် (ဥပမာ ၁ တွင်
prompt 2,000 token ဖြင့် 706.7 ms)။ decode နှုန်းသည် `Decode Phase` ၏ step ကြာချိန် အပေါ် မှီခိုသည်။
prompt token တိုးလာပါက TTFT တိုးသော်လည်း step ကြာချိန် မပြောင်းလဲပါက generation နှုန်း မပြောင်းလဲပါ။
prefix cache hit ရှိပါက ထို prefill အလုပ်ကို ကျော်နိုင်သည် (ဥပမာ ၃ တွင် 1,500 token အတွက် 500.0 ms)။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** prompt token အရေအတွက် ပြောင်းလဲမှုကို အရင် တိုင်းပါ။
prompt token မပြောင်းလဲဘဲ TTFT တိုးပါက queue ကြာချိန်ကို တိုင်းပါ — queue တိုးနေပါက
အကြောင်းရင်း (၃) ဖြစ်သည်။ prefix cache hit rate ကျဆင်းပါက အကြောင်းရင်း (၂) ဖြစ်သည်။
prefill လည်ပတ်ချိန် ကိုယ်တိုင် တိုးပါက prefill နှင့် decode ယှဉ်ပြိုင်မှုကို စစ်ပါ (အကြောင်းရင်း ၄)။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** မျှဝေသည့် prefix ကို request တိုင်း၏ အစတွင် တူညီစွာ ထားပြီးနောက်
prefix cache hit rate ပြန်တက်ပါက prefill အလုပ် လျော့သည်။ `Chunked Prefill` ဖွင့်ပြီးနောက်
`Inter-Token Latency (ITL)` ၏ p95 ငြိမ်ပါက prefill ၏ နှောင့်နှေးမှု ပြဿနာ ဖြေရှင်းပြီး ဖြစ်သည်။

#### အဖြေ ၃ — Replica တစ်ခု၏ စွမ်းဆောင်ရည် ကွာခြင်းခြင်း

**အကြောင်းရင်း ရှင်းလင်းချက် —** `Pipeline Parallelism` တွင် idle bubble အချိုးသည်
stage အရေအတွက်နှင့် microbatch အရေအတွက်အပေါ် မှီခိုသည် — stage ၈ ခု၊ microbatch ၈ ခုတွင်
46.7 % ဖြစ်ပြီး stage ၄ ခုတွင် 27.3 % ဖြစ်သည် (ဥပမာ ၄)။ replica နှစ်ခုတွင် layout မတူပါက
ထို အချိုးသည် တိုက်ရိုက် ကွာခြင်းပြီး goodput ကွာခြင်းသည် အဖြေတွင် ပေါ်လာသည်။
`Tensor Parallelism` layout မတူခြင်းသည်လည်း collective communication ပမာဏကို ပြောင်းစေသည်။

**အစဉ်လိုက် ဆုံးဖြတ်ရန် —** replica တိုင်း၏ per-replica goodput နှင့် configuration ကို
နှိုင်းယှဉ်ပါ။ layout မတူပါက အကြောင်းရင်း (၁) ဖြစ်သည်။ model သို့မဟုတ် tokenizer version မတူပါက
အကြောင်းရင်း (၂) ဖြစ်သည်။ replica တစ်ခုသည် readiness အောင်ပြီး မကြာမီ traffic ရပါက
အကြောင်းရင်း (၃) ဖြစ်သည်။ request အရှည် ဖြန့်ကျက်မှု မညီပါက အကြောင်းရင်း (၄) ဖြစ်သည်။

**ဖြေရှင်းနည်း အတည်ပြုချက် —** layout ကို checkpoint နှင့် serving configuration နှင့်အတူ မှတ်တမ်းတင်ပြီး
replica အားလုံး တူညီစေပါက per-replica goodput သည် အတူတူ ဖြစ်လာသည်။ prefix အလိုက် routing
ထည့်ပါက `Prefix Caching` ၏ hit rate လည်း replica တိုင်းတွင် တူညီလာသည်။

### ၅.၃ ဆုံးဖြတ်ချက် အဖြေများ

#### အဖြေ ၁ — 70B topology ၏ ကိန်းဂဏန်း

**ရှင်းလင်းချက် —** weights 140.0 GB ကို tensor parallelism ၈ ဖြင့် ခွဲပါက device တိုင်း 17.5 GB ဖြစ်သည်၊
batch 8၊ 8k context တွင် KV 8.59 GB ထည့်ပါက 18.57 GB ဖြစ်သည် — 12 GB ချန်ထားသည့်
80 GB card တွင် ဝင်သည်။ collective communication သည် token တစ်ခုလျှင် 2.62 MB ဖြစ်ပြီး
600 GB/s link တွင် 4.4 µs ဖြစ်သည်၊ decode step 4.18 ms ၏ 0.105 % သာ ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** node တစ်ခုတည်းတွင် tensor parallelism ၈ ဖြင့် ဖွင့်တင်ရမည်။ pipeline ကို ရွေးပါက
microbatch ၈ ခုဖြင့် idle 46.7 % ကို ပေးဆပ်ရမည်၊ ဆိုလိုသည်မှာ တူညီသည့် hardware ဖြင့်
goodput ထက်ဝက်နီးပါး ဆုံးရှုံးသည်။ တိုင်းတာချက်တွင် 191.4 tokens/s သည် roofline အပေါ်ဘောင်
ဖြစ်သည်၊ တကယ့် တန်ဖိုးသည် 60 % ခန့်တွင် ရှိလေ့ ရှိသည်။

**တိုင်းတာမည့် metric —** per-replica `Goodput`၊ `Time per Output Token (TPOT)` ၏ p95၊
1M output token လျှင် USD — အကြောင်းမှာ ဆုံးဖြတ်ချက်တွင် ကုန်ကျစရိတ်နှင့် ဝန်ဆောင်မှု အရည်အသွေး
နှစ်ခုလုံး ပါဝင်သဖြင့် ဖြစ်သည်။

```bash
python3 - <<'PY'
params, bits = 70e9, 16
weights_gb = params * bits / 8 / 1e9
tp = 8
print("weights GB fp16            ", weights_gb)
print("per device GB at tp 8      ", round(weights_gb / tp, 2))
kv_per_token_kib, ctx, batch = 128.0, 8192, 8
kv_gb = batch * ctx * kv_per_token_kib * 1024 / 1e9
print("KV GB at batch 8, 8k ctx   ", round(kv_gb, 2))
print("per device GB weights+KV   ", round((weights_gb + kv_gb) / tp, 2))
print("fits 80 GB card, 12 GB reserve", (weights_gb + kv_gb) / tp <= 68)
bw = 3.35e12
print("roofline tps at tp 8       ", round(tp * bw / (weights_gb * 1e9), 1))
print("roofline tps at tp 8, 60 pct", round(0.6 * tp * bw / (weights_gb * 1e9), 1))
nvlink, hidden, layers = 600e9, 8192, 80
per_token_bytes = layers * 2 * hidden * 2
print("all-reduce bytes per token ", per_token_bytes)
print("link time us per token     ", round(per_token_bytes / nvlink * 1e6, 1))
print("link time vs 4.18 ms step pct", round(100 * per_token_bytes / nvlink / 0.00418, 3))
print("cost per 1M at 2.75 USD/GPU-hour, 8 GPUs, 191 tps",
      round(8 * 2.75 * 1e6 / (191.4 * 3600), 4))
print("cost per 1M at 383 tps (16 GPUs, same rate each)",
      round(16 * 2.75 * 1e6 / (382.9 * 3600), 4))
PY
```

```text
weights GB fp16             140.0
per device GB at tp 8       17.5
KV GB at batch 8, 8k ctx    8.59
per device GB weights+KV    18.57
fits 80 GB card, 12 GB reserve True
roofline tps at tp 8        191.4
roofline tps at tp 8, 60 pct 114.9
all-reduce bytes per token  2621440
link time us per token      4.4
link time vs 4.18 ms step pct 0.105
cost per 1M at 2.75 USD/GPU-hour, 8 GPUs, 191 tps 31.9285
cost per 1M at 383 tps (16 GPUs, same rate each) 31.9201
```

#### အဖြေ ၂ — Autoscaling မူဝါဒ၏ ကိန်းဂဏန်း

**ရှင်းလင်းချက် —** per-replica စွမ်းရည် 9.4 req/s ဖြစ်ပါက peak 47 req/s အတွက် replica ၅ ခု
လိုသည်၊ utilisation 100.0 % ဖြစ်သည် — ဆိုလိုသည်မှာ အနားသတ် မရှိပါ။ replica ၆ ခုဖြင့်
83.3 % ဖြစ်သည်။ replica ၄ ခုဖြင့် peak ကို ဆောင်ရွက်ပါက ကျန်သည့် 9.4 req/s သည်
queue ထဲ စုပုံပြီး request 60 ခုရှိသည့် queue သည် 6.4 s အတွင်း ပြည့်သည်။
အကြောင်းရင်း မှာ replica ၅ ခုတွင် backlog တိုးနှုန်း 0.0 req/s ဖြစ်ပြီး replica ၄ ခုတွင် 9.4 req/s ဖြစ်သည်။

**ဆုံးဖြတ်ချက် —** minimum warm capacity replica ၂ ခု၊ အများဆုံး replica ၆ ခု၊ scale-down ကို
တစ်ကြိမ်လျှင် တစ်ခုနှုန်း cooldown နှင့် လုပ်ရမည်။ ကုန်ကျစရိတ် အချက်အလက် — replica ၂ ခု
တစ်လ $4,464၊ replica ၆ ခု တစ်လ $13,392။ replica ၇ ခုအထိ တိုးခြင်းသည် တစ်လ $2,232 ပိုကုန်သော်လည်း
peak တွင် utilisation သည် 71.4 % သို့ ကျဆင်းသည် — ထို အနားသတ်သည် SLO ချိုးဖောက်မှု ဖြစ်ပြီးမှသာ
လိုအပ်သည်။

**တိုင်းတာမည့် metric —** `Goodput`၊ queue wait time ၏ p95၊ replica တိုင်း၏ readiness အောင်ချိန်၊
တစ်လလျှင် USD။ signal သည် "အသုံးဝင်သည့် အလုပ်" နှင့် ချိတ်ထားသဖြင့် CPU အသုံးပြုမှုကို
အခြေခံသည့် policy ထက် ပို၍ ယုံကြည်ရသည်။

ဤ အဖြေကို `labs/lab_autoscale.py --rps 47 --output-tokens 300 --replicas 5` ဖြင့်
ကိုယ်ပိုင် ကိန်းဂဏန်း အပေါ် ပြန်တိုင်းနိုင်သည် — ထို lab သည် per-replica စွမ်းရည်ကို
tokens/s အဖြင့် သတ်မှတ်သဖြင့် request အရေအတွက် အဖြင့် သတ်မှတ်သည့် ဤ အဖြေနှင့်
ကွာခြားမှုသည် ယူဆချက် ကွာခြင်းသာ ဖြစ်သည်။

```bash
python3 - <<'PY'
import math
per_replica, price = 9.4, 3.10
arrivals = (("off peak", 6.5), ("day", 18.0), ("evening", 31.0), ("peak", 47.0))
for name, a in arrivals:
    need = math.ceil(a / per_replica)
    print(f"{name:9} {a:5.1f} req/s -> min replicas {need}, with one spare {need + 1}")
print("utilisation at peak, 5 replicas pct", round(100 * 47 / (5 * per_replica), 1))
print("utilisation at peak, 6 replicas pct", round(100 * 47 / (6 * per_replica), 1))
print("utilisation off peak, 2 replicas pct", round(100 * 6.5 / (2 * per_replica), 1))
backlog = 47 - 4 * per_replica
print("backlog growth req/s with 4 replicas", round(backlog, 1))
print("seconds to fill a 60-request queue  ", round(60 / backlog, 1))
print("backlog growth req/s with 5 replicas", round(47 - 5 * per_replica, 1))
print("cost per hour 2 replicas", round(2 * price, 2))
print("cost per hour 5 replicas", round(5 * price, 2))
print("cost per hour 6 replicas", round(6 * price, 2))
print("monthly 6 replicas USD  ", round(6 * price * 24 * 30, 2))
print("monthly 5 replicas USD  ", round(5 * price * 24 * 30, 2))
print("monthly 2 replicas USD  ", round(2 * price * 24 * 30, 2))
print("saving of 6 vs 7 replicas per month USD",
      round((7 - 6) * price * 24 * 30, 2))
PY
```

```text
off peak    6.5 req/s -> min replicas 1, with one spare 2
day        18.0 req/s -> min replicas 2, with one spare 3
evening    31.0 req/s -> min replicas 4, with one spare 5
peak       47.0 req/s -> min replicas 5, with one spare 6
utilisation at peak, 5 replicas pct 100.0
utilisation at peak, 6 replicas pct 83.3
utilisation off peak, 2 replicas pct 34.6
backlog growth req/s with 4 replicas 9.4
seconds to fill a 60-request queue   6.4
backlog growth req/s with 5 replicas 0.0
cost per hour 2 replicas 6.2
cost per hour 5 replicas 15.5
cost per hour 6 replicas 18.6
monthly 6 replicas USD   13392.0
monthly 5 replicas USD   11160.0
monthly 2 replicas USD   4464.0
saving of 6 vs 7 replicas per month USD 2232.0
```

## Self-check

၁။ အပိုင်း ၁ ဥပမာ ၁ တွင် TTFT နှင့် စုစုပေါင်း latency အနက် မည်သည့်အရာက အကြီးမားဆုံး အပိုင်းကို ယူသည်၊
မည်သည့် အဆင့်အပေါ် မှီခိုသည်။

၂။ အပိုင်း ၁ ဥပမာ ၂ တွင် static batching ၏ လွင့်သည့် အချိုးကို မည်သည့် အချက်နှစ်ခုမှ တွက်သည်။

၃။ အပိုင်း ၅.၁ အဖြေ ၃ တွင် context ရှည်သည့်အခါ bandwidth ကို မည်သည့်အရာက လွှမ်းမိုးသည်။

၄။ အပိုင်း ၅.၁ အဖြေ ၅ တွင် batch 32 ကို SLO အတွက် မည်သောကြောင့် မရွေးရသနည်း။

၅။ အပိုင်း ၅.၂ အဖြေ ၁ တွင် throughput ပြိုလဲခြင်း၏ အဓိက ယန္တရားကို ရှင်းလင်းပါ။

<details>
<summary>အဖြေများ</summary>

၁။ စုစုပေါင်း 9.507 s အနက် decode အပိုင်းသည် 8,800 ms ဖြစ်သဖြင့် 92.6 % ကို ယူသည်။
ထို့ကြောင့် ခံစားမှုကို အဓိက ဆုံးဖြတ်သည့် အဆင့်သည် `Decode Phase` ဖြစ်သည်၊ TTFT မဟုတ်ပါ။

၂။ slot အရေအတွက် × အရှည်ဆုံး output (4 × 200 = 800) နှင့် output အရှည်များ၏ ပေါင်းလဒ် (450)
ဖြစ်သည်၊ ကွာခြားမှုကို 800 ဖြင့် စားပါက 43.8 % ဖြစ်သည်။

၃။ KV cache ၏ traffic ဖြစ်သည် — context 32,768 နှင့် batch 32 တွင် ထို အပိုင်းသည် traffic ၏ 90.8 % ကို ယူသည်။

၄။ batch 32 ၏ step ကြာချိန်သည် 74.80 ms ဖြစ်၍ 60 ms SLO ကို 24.8 % ကျော်လွန်သောကြောင့် ဖြစ်သည်။
aggregate tokens/s (427.8) မြင့်သော်လည်း per-request inter-token latency သည် SLO ကို ဖောက်ဖျက်သည်။

၅။ KV cache memory ပြည့်သည့်အခါ request များ ဖြုတ်ချခံရပြီး ၎င်းတို့၏ KV state ဖျက်ခံရသည်၊
ပြန်လာသည့်အခါ prompt ကို အစမှ ပြန်တွက်ရသဖြင့် အလုပ်ပမာဏ ထပ်တလဲလဲ တိုးလာသည်။

</details>

## References

- နယ်ပယ် အခြေခံ အချက်အလက် — [`../../terms/09_infrastructure_and_serving.md`](../../terms/09_infrastructure_and_serving.md) နှင့် `glossary/by_area/09_infrastructure_and_serving.json`။
- Source glossary — https://aiengineeringfromscratch.com/glossary (MIT)၊ `rohitg00/ai-engineering-from-scratch`။
- လက်တွေ့ lab များ — [`labs/`](labs/) (အမည်နှင့် flag — [`labs/README.md`](labs/README.md))။
- Papers — [Orca](https://www.usenix.org/conference/osdi22/presentation/yu)၊ [Sarathi-Serve](https://arxiv.org/abs/2403.02310)၊ [DistServe](https://arxiv.org/abs/2401.09670)၊ [PagedAttention](https://arxiv.org/abs/2309.06180)၊ [FlashAttention](https://arxiv.org/abs/2205.14135)၊ [Megatron-LM](https://arxiv.org/abs/1909.08053)၊ [GPipe](https://arxiv.org/abs/1811.06965)။

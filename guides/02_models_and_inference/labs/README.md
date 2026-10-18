# Labs - Area 02: Models & Inference

ဤ lab suite သည် area 02 ၏ term များ (Sampling, KV Cache, Quantization, Attention cost,
Batching, Token Budget) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။ Python standard library သာ
အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည် (deterministic)။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/02_models_and_inference/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 6/6 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 02 Models & Inference (offline, deterministic)
==========================================================================
[PASS] lab_sampling.py: [PASS] lab_sampling self-test passed.
[PASS] lab_kv_cache.py: [PASS] lab_kv_cache self-test passed.
[PASS] lab_quantization.py: [PASS] lab_quantization self-test passed.
[PASS] lab_attention_cost.py: [PASS] lab_attention_cost self-test passed.
[PASS] lab_batching.py: [PASS] lab_batching self-test passed.
[PASS] lab_context_budget.py: [PASS] lab_context_budget self-test passed.
==========================================================================
[PASS] All 6/6 labs passed successfully.
```

## lab_sampling.py - Temperature, Top-k, Top-p

Fixed 10-token logits vector (peaked middle, two tail tokens) ကို အသုံးပြုသည်။
Table တွင် token, raw logit, p(T), p(top-k), p(top-p) နှင့် cumulative sum ပြသည်။

```bash
python3 lab_sampling.py                                # default: temperature 1.0, top-k 5, top-p 0.9, seed 0
python3 lab_sampling.py --temperature 0.2 --top-k 3 --top-p 0.95 --seed 7
python3 lab_sampling.py --sweep                        # temperature 0.1 .. 2.0
python3 lab_sampling.py --interactive                  # knobs ကို လက်ဖြင့် ထည့်
python3 lab_sampling.py --self-test
python3 lab_sampling.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_sampling - temperature / top-k / top-p (deterministic, offline)
temperature=1.0  top-k=5  top-p=0.9  seed=0
Pipeline: logits -> temperature -> top-k -> top-p -> cumulative sum
--------------------------------------------------------------------------
 rank  token      logit    p(T)     p(top-k)  p(top-p)   cumsum
    1  on          4.60    0.4651    0.5319    0.5779   0.5779
    2  sat         3.40    0.1401    0.1602    0.1741   0.7519
    3  mat         3.20    0.1147    0.1312    0.1425   0.8944
    4  cat         2.90    0.0850    0.0972    0.1056   1.0000
    5  dog         2.70    0.0696    0.0796    0.0000   1.0000
    6  a           2.40    0.0515    0.0000    0.0000   1.0000
    7  ran         2.10    0.0382    0.0000    0.0000   1.0000
    8  the         2.00    0.0345    0.0000    0.0000   1.0000
    9  zebra      -1.50    0.0010    0.0000    0.0000   1.0000
   10  quokka     -2.50    0.0004    0.0000    0.0000   1.0000
--------------------------------------------------------------------------
Sampled token: on (index 4)
Candidates kept: 4/10   entropy: 1.1362 nats
မှတ်ချက် - temperature မြင့်လျှင် ဖြန့်ဖြူးမှု ပိုပြန့်သည်၊ top-k နှင့် top-p သည် အမြီးရှည် candidate များကို ဖယ်ရှားသည်။
==========================================================================
```

## lab_kv_cache.py - KV Cache memory နှင့် attention work

KV cache MB, weight MB, KV/weight ratio နှင့် per-token attention work (cached vs uncached)
ကို ပြသည်။

```bash
python3 lab_kv_cache.py                                # context 8192, layers 32, heads 32, head_dim 128, fp16, batch 1, 7B
python3 lab_kv_cache.py --context 32768 --dtype int8 --batch 8
python3 lab_kv_cache.py --sweep                        # context 1024 .. 131072
python3 lab_kv_cache.py --self-test
python3 lab_kv_cache.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_kv_cache - KV cache memory နှင့် attention အလုပ်ပမာဏ (offline, deterministic)
context=8192  layers=32  heads=32  head_dim=128  dtype=fp16  batch=1  params=7.0B
--------------------------------------------------------------------------
KV cache size            :       4,096.00 MB  (4.0000 GB)
Weight size (7.0B fp16)   :      13,351.44 MB  (13.0385 GB)
KV / weight ratio        :         0.3068
Bytes per value (fp16)   :           2.00
--------------------------------------------------------------------------
Work per generated token at n = 8192 (score pairs):
  with KV cache    :            8,192
  without cache    :       67,108,864
  ratio            :          8,192.0x  (cached O(n) vs uncached O(n^2))
--------------------------------------------------------------------------
မှတ်ချက် - KV cache သည် ထပ်တလဲလဲ တွက်ချက်မှုကို လျှော့ချသည်၊ သို့သော် sequence အရှည်၊ layer၊ batch နှင့် model configuration အပေါ် မှီခို၍ memory ကြီးထွားသည်။
==========================================================================
```

## lab_quantization.py - Symmetric group-wise quantization

seed မှ deterministic weight matrix (64 x 64) ကို ဖန်တီးပြီး bytes/weight, 7B model size,
max absolute error, RMSE, cosine similarity နှင့် matvec output error ကို ပြသည်။

```bash
python3 lab_quantization.py                            # bits 4, group-size 64, seed 0
python3 lab_quantization.py --bits 8 --group-size 32 --seed 3
python3 lab_quantization.py --sweep                    # bits 2, 3, 4, 5, 8
python3 lab_quantization.py --self-test
python3 lab_quantization.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_quantization - symmetric group-wise quantization (offline, deterministic)
bits=4  group-size=64  seed=0  matrix=64x64 weights
--------------------------------------------------------------------------
Bytes per weight              :     0.5000
7B model size at this precision:    3.5000 GB
Max absolute error            :   0.250910
RMSE                          :   0.103760
Cosine similarity to fp32     :   0.994730
Matvec output rel. error      :   0.108359
Matvec output max abs error   :   2.861553
--------------------------------------------------------------------------
မှတ်ချက် - bit အလုံးအစု လျှော့ချလျှင် memory ကျဆင်းသည်၊ quantization error တက်သည်။ bit အလုံးအစု တစ်ခုမှ တစ်ခုသို့ ရွေ့ခြင်းသည် end-to-end memory သို့မဟုတ် အရှိန် အချိုးကို အာမမခံနိုင်ပါ။
==========================================================================
```

## lab_attention_cost.py - Attention FLOPs နှင့် score memory

Attention FLOPs, n*n score-matrix memory, FFN FLOPs, dominant term နှင့် break-even
context length ကို ပြသည်။ KV cache ပါသည့် decode step တစ်ခုအတွက် ကိန်းဂဏန်းများလည်း ပါသည်။

```bash
python3 lab_attention_cost.py                          # context 8192, layers 32, heads 32, head_dim 128, fp16
python3 lab_attention_cost.py --context 65536 --heads 64
python3 lab_attention_cost.py --self-test
python3 lab_attention_cost.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_attention_cost - attention FLOPs, score memory, FFN comparison
context=8192  layers=32  heads=32  head_dim=128  dtype=fp16
d_model = 4096   d_ff = 4 * d_model = 16384
--------------------------------------------------------------------------
Assumption: attention = layers * heads * 2 * n^2 * head_dim  (per head per layer 2*n^2*d)
Attention FLOPs          :     17,592,186,044,416  (17.59 TFLOPs)
Assumption: FFN = layers * 4 * n * d_model * d_ff
FFN FLOPs                :     70,368,744,177,664  (70.37 TFLOPs)
Attention / FFN ratio    :                 0.2500
Dominant term at n=8192: FFN
Break-even context n*    :                 32,768  (n* = 2 * d_ff)
--------------------------------------------------------------------------
Score-matrix memory per head :      128.000 MB  (n*n*2.0 bytes)
Score-matrix memory total    :  131,072.000 MB  (128.000 GB, layers*heads*n*n*2.0)
--------------------------------------------------------------------------
Decode step with KV cache (8192 keys, 1 query):
  attention FLOPs        :          2,147,483,648  (2.147 GFLOPs)
  score row per head     :               0.015625 MB  (n*2.0 bytes)
  score rows total       :                 16.000 MB
  full-sequence attention:    17,592,186,044,416  -> 8,192.0x အလုပ် သက်သာသည်
==========================================================================
```

## lab_batching.py - Static vs Continuous batching

Decode loop ကို simulate လုပ်သည်။ Static batching တွင် slot သည် batch အရှည်ဆုံး request
ပြီးသည်အထိ ချုပ်ထားသည်၊ continuous batching တွင် လွတ်လာသည့် slot သည် စောင့်နေသည့်
request ကို ချက်ချင်း လက်ခံသည်။

```bash
python3 lab_batching.py                                # requests 64, slots 8, prompt 512, output 128, 2.49 USD/GPU-hour, ITL budget 50 ms
python3 lab_batching.py --requests 128 --slots 16 --output-tokens 256 --itl-budget-ms 40
python3 lab_batching.py --sweep                        # slots 1, 2, 4, 8, 16, 32
python3 lab_batching.py --self-test
python3 lab_batching.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_batching - static batching vs continuous batching
requests=64  slots=8  prompt-tokens=512  output-tokens~128  gpu-hour=2.49 USD
output lengths: min=36  max=229  mean=146.3  (seed 20240)
--------------------------------------------------------------------------
Static batching
  total tokens generated        :          9,364
  wall-clock steps              :          1,732
  TTFT first/last request (ms)  : 130.88 / 31,615.04
  mean ITL (ms, budget 50)      :          23.11
  tokens/second                 :         261.48
  goodput in ITL budget (tok/s) :         259.70
  GPU-seconds                   :         35.811
  cost per million tokens (USD) :         2.6452
--------------------------------------------------------------------------
Continuous batching
  total tokens generated        :          9,364
  wall-clock steps              :          1,252
  TTFT first/last request (ms)  : 130.88 / 30,391.04
  mean ITL (ms, budget 50)      :          27.67
  tokens/second                 :         276.30
  goodput in ITL budget (tok/s) :         276.06
  GPU-seconds                   :         33.891
  cost per million tokens (USD) :         2.5033
--------------------------------------------------------------------------
Continuous / static throughput ratio: 1.0567x  |  goodput ratio: 1.0630x
မှတ်ချက် - request အားလုံးကို t=0 တွင် တင်သွင်းသည်၊ ထို့ကြောင့် TTFT တွင် queueing အချိန် ပါဝင်သည်။ Static batching တွင် slot သည် batch အရှည်ဆုံး request ပြီးသည်အထိ ချုပ်ထားသည်။
==========================================================================
```

## lab_context_budget.py - Token budget

Token budget breakdown, fits/overflow, headroom သို့မဟုတ် shortfall, ဖြေရှင်းနည်းများ
နှင့် window ၏ KV cache MB ကို ပြသည်။

```bash
python3 lab_context_budget.py                          # window 128000, system 600, retrieved 24000, history 30000, reserve-output 4096
python3 lab_context_budget.py --window 32000 --retrieved 20000 --history 15000
python3 lab_context_budget.py --history 200000          # overflow ဖြစ်သည့် အနေအထား
python3 lab_context_budget.py --self-test
python3 lab_context_budget.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_context_budget - token budget breakdown (offline, deterministic)
window=128,000  system=600  retrieved=24,000  history=30,000  reserve-output=4,096
--------------------------------------------------------------------------
  system prompt             :        600
  retrieved context         :     24,000
  conversation history      :     30,000
  reserved for output       :      4,096
  used                      :     58,696  (45.86% of window)
  status                    :       FITS  headroom 69,304 tokens
--------------------------------------------------------------------------
Remedies (each frees tokens):
  shrink retrieved context to 8,000 tokens                   frees   16,000
  summarise history to 25% of its size                       frees   22,500
  trim the system prompt by half                             frees      300
  total freed 38,800 tokens -> used after remedies 19,896, headroom 108,104
--------------------------------------------------------------------------
KV cache this window costs :    64,000.00 MB  (62.50 GB, layers=32, heads=32, head_dim=128, fp16)
မှတ်ချက် - budget သည် reserved output ပါဝင်မှသာ လုံခြုံသည်၊ ထို့ကြောင့် reserve-output ကို နုတ်မထားရ။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (temperature 0 သည် argmax ကို
  ထိန်းသည်၊ context နှစ်ဆ ဖြစ်ပါက KV နှစ်ဆ၊ int8 သည် fp16 ၏ တစ်ဝက်၊ int8 error သည် int4
  error အောက် နိမ့်သည်၊ attention သည် quadratic တိုးသည်၊ cached decode သည် linear တိုးသည်၊
  continuous batching သည် static ထက် မြန်သည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။

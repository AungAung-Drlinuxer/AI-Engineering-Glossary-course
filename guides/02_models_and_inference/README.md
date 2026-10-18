# Area 02 — Models & Inference: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် `terms/02_models_and_inference.md` ရှိ term ၂၉ ခုကို **စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့် သင်ခန်းစာ**
အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည်
"ဤ term ကို မည်သည့် အစဉ်ဖြင့် လေ့လာမည်၊ ဘယ်လို အလုပ်လုပ်သည်၊ ဘယ်လောက် ကုန်ကျသည်" ကို ဖြေသည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၂၉ ခု (area 02 — Models & inference) |
| ဖိုင် | ၆ ခု + lab ၆ ခု + ကိန်းဂဏန်း script ၄ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py` |

## လေ့လာသည့် အစဉ် (၆ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ လုပ်ရမည့် အရာ |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_attention_cost.py --context 8192` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၅ | ပုံများကို စာရွက်ပေါ် ပြန်ဆွဲခြင်း |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃–၄ | `python3 labs/lab_sampling.py --sweep` |
| ၄ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၆–၁၀ | `python3 labs/lab_quantization.py --sweep` |
| ၅ | [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | `python3 labs/lab_kv_cache.py --sweep`၊ `lab_batching.py --sweep` |
| ၆ | [`04_exercises.md`](04_exercises.md) | တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၈ ခု |

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၂၉ ခုကို အဆင့် ၆ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၁၂ ခု — attention တွက်ချက်မှု၊ Transformer block၊ KV cache ကြီးထွားမှု၊ prefill နှင့် decode၊ sampling pipeline၊ quantization၊ MoE၊ speculative decoding၊ TTFT/ITL၊ batching |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း GPU memory / compute / latency / throughput / ကုန်ကျစရိတ် / production အပေါ် သက်ရောက်မှု + တွက်ချက်မှု ဥပမာ ၄ ခု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၆ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၈ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၅ ခု၊ ဆုံးဖြတ်ချက် ၃ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၆ ခု + `run_labs.py` (usage နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | ၀၃ ဖိုင်ရှိ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script ၄ ခု |

## Interactive lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `lab_sampling.py` | `--temperature`၊ `--top-k`၊ `--top-p`၊ `--seed` | token တိုင်း၏ ဖြစ်နိုင်ခြေ ပြောင်းလဲမှု၊ ရွေးချယ်ခံရသည့် token |
| `lab_kv_cache.py` | `--context`၊ `--layers`၊ `--heads`၊ `--head-dim`၊ `--dtype`၊ `--batch` | KV cache MB၊ weights နှင့် အချိုး၊ cache ရှိ/မရှိ အလုပ်ပမာဏ |
| `lab_quantization.py` | `--bits`၊ `--group-size`၊ `--seed` | အလေးတစ်ခုစီ ဘိုက်၊ မော်ဒယ် အရွယ်အစား၊ error နှင့် cosine similarity |
| `lab_attention_cost.py` | `--context`၊ `--layers`၊ `--heads`၊ `--head-dim` | attention FLOPs၊ score matrix memory၊ FFN နှင့် နှိုင်းယှဉ်မှု၊ break-even |
| `lab_batching.py` | `--requests`၊ `--slots`၊ `--prompt-tokens`၊ `--output-tokens`၊ `--gpu-hour-cost`၊ `--itl-budget-ms` | TTFT၊ ITL၊ tokens/s၊ goodput၊ USD / သန်းတစ်သန်း token |
| `lab_context_budget.py` | `--window`၊ `--system`၊ `--retrieved`၊ `--history`၊ `--reserve-output` | budget ကျော်လွန်မှု၊ လျှော့နည်းများ၊ window ၏ KV ကုန်ကျစရိတ် |

### Temperature ကို ပြောင်းကြည့်ခြင်း — `lab_sampling.py --sweep`

```
$ python3 lab_sampling.py --sweep
 temperature   P(top token)     entropy (nats)
        0.10         1.0000            0.0001
        0.25         0.9864            0.0864
        0.50         0.8118            0.7791
        1.00         0.4651            1.6785
        1.50         0.3259            1.9421
        2.00         0.2613            2.0562
```

**ဖတ်နည်း** — `temperature` 0.10 တွင် top token ၏ ဖြစ်နိုင်ခြေ 1.0000 ဖြစ်သဖြင့် ရလဒ်သည်
အမြဲတမ်း တူညီသည် (deterministic နီးပါး)။ 2.00 တွင် 0.2613 အထိ ကျဆင်းသဖြင့် အခြား token များ
ရွေးချယ်ခံရနိုင်သည်။ entropy သည် ထို ဖြန့်ကျက်မှုကို ကိန်းဂဏန်း အဖြစ် ပြသည်။

### Context length ကို ပြောင်းကြည့်ခြင်း — `lab_kv_cache.py --sweep`

```
$ python3 lab_kv_cache.py --sweep
  context      KV MB (fp16)   cached work   uncached work   ratio
     1,024           512.00           1,024        1,048,576    1,024x
     8,192         4,096.00           8,192       67,108,864    8,192x
    32,768        16,384.00          32,768    1,073,741,824   32,768x
   131,072        65,536.00         131,072   17,179,869,184  131,072x
```

**ဖတ်နည်း** — context နှစ်ဆ တိုးပါက KV နှစ်ဆ (linear)၊ cache မပါဘဲ တွက်သည့် အလုပ်ပမာဏ သည်
၄ ဆ (quadratic) တိုးသည်။ context 128K တွင် cache မပါဘဲ တွက်ပါက အလုပ် **131,072 ဆ**
ပိုကုန်သည် — ထို့ကြောင့် `KV Cache` သည် ရွေးချယ်မှု မဟုတ်ဘဲ မဖြစ်မနေ လိုအပ်သည့် အရာ ဖြစ်သည်။

### Quantization precision ကို ပြောင်းကြည့်ခြင်း — `lab_quantization.py --sweep`

```
$ python3 lab_quantization.py --sweep
  bits  bytes/w   7B size GB   max abs err      RMSE   cosine   matvec rel
     2   0.2500       1.7500       1.780506  0.697952  0.79938     0.562095
     4   0.5000       3.5000       0.250910  0.103760  0.99473     0.108359
     8   1.0000       7.0000       0.014007  0.005708  0.99998     0.005359
```

**ဖတ်နည်း** — 4-bit သည် fp16 နှင့် နှိုင်းယှဉ်ပါက အလေး ၄ ဆ ငယ်သည်၊ cosine similarity
0.99473 ဖြစ်သည်။ 2-bit သို့ ဆင်းပါက 0.79938 အထိ ကျဆင်းသည် — ထို့ကြောင့်
quantization အဆင့်သည် **မှတ်ဉာဏ်နှင့် အရည်အသွေး** ကို လဲလှယ်သည့် နေရာ ဖြစ်သည်။

### Batching မူဝါဒ — `lab_batching.py --sweep`

```
$ python3 lab_batching.py --sweep
  slots   static tok/s   cont tok/s   ratio   static USD/M   cont USD/M
      1         140.61        140.61    1.00x        4.9190       4.9190
      4         223.15        242.42    1.09x        3.0996       2.8532
     32         305.15        306.91    1.01x        2.2667       2.2537
```

**ဖတ်နည်း** — slot ၁ ခုတွင် နည်းလမ်း နှစ်ခု တူညီသည် (အလွတ် slot မရှိ)။ slot တိုးလာသည်နှင့်အမျှ
continuous batching ၏ အကျိုးအမြတ် ပေါ်လာသည်၊ သို့သော် slot ၃၂ တွင် ကွာခြားမှု ကျဉ်းလာသည် —
batch ကြီးလာသည့်အခါ အလွတ် slot ၏ အလွင့် အချိုးကျ လျော့သွားသည်။

### Token budget ကို ပြောင်းကြည့်ခြင်း — `lab_context_budget.py --window 32000`

```
$ python3 lab_context_budget.py --window 32000
  system prompt             :        600
  retrieved context         :     24,000
  conversation history      :     30,000
  reserved for output       :      4,096
  used                      :     58,696  (183.42% of window)
  status                    :   OVERFLOW  shortfall 26,696 tokens
Remedies (each frees tokens):
  shrink retrieved context to 8,000 tokens                   frees   16,000
  summarise history to 25% of its size                       frees   22,500
  trim the system prompt by half                             frees      300
  total freed 38,800 tokens -> used after remedies 19,896, headroom 12,104
KV cache this window costs :    16,000.00 MB  (15.62 GB, layers=32, heads=32, head_dim=128, fp16)
```

**ဖတ်နည်း** — context window သည် **အသုံးပြုနိုင်သည့် ပမာဏ** မဟုတ်၊ **ကန့်သတ်ချက်** ဖြစ်သည်။
output အတွက် ချန်ထားခြင်းကို မနုတ်ပါက budget သည် လုံခြုံမည် မဟုတ်သလို၊ window ကြီးခြင်းသည်
KV cache MB အဖြစ် တိုက်ရိုက် ကုန်ကျသည် (32K window = 15.62 GB)။

## အောက်ခံစနစ်နှင့် ချိတ်ဆက်မှု — ကိန်းဂဏန်း ဥပမာ ၄ ခု

[`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) ရှိ ဥပမာ တိုင်း၏ command ကို
ဤနေရာတွင် တိုက်ရိုက် run နိုင်သည် (script များသည် [`scripts/`](scripts/) တွင် ပါဝင်သည်) —

| ဥပမာ | Script | ရလဒ် အနှစ်ချုပ် |
|---|---|---|
| a | `scripts/ex_a_kv_cache.py` | KV cache = 0.5 MiB / token (fp16)၊ context 128K × batch 32 = 2048 GiB → int8 သုံးပါက တစ်ဝက် |
| b | `scripts/ex_b_weights.py` | 7B fp16 = 13.0 GiB၊ 4-bit = 3.3 GiB; 80 GB accelerator (64 GiB သုံးနိုင်) တွင် 4-bit 70B မော်ဒယ် 1 ခု ထည့်နိုင် |
| c | `scripts/ex_c_attention_ffn.py` | attention သည် FFN ကို ကျော်လွန်သည့် အမှတ်ကို တွက်ပြသည် (ဤ မော်ဒယ်အတွက် seq ≈ 11008) |
| d | `scripts/ex_d_cost.py` | batch 1 နှင့် batch 32 ၏ တူညီသည့် မော်ဒယ်၊ token သန်း ကုန်ကျစရိတ် ကွာခြားမှု |

**သတိထားရန်** — ထို ကိန်းဂဏန်းများသည် **ရေးသားထားသည့် ခန့်မှန်းချက်** (bandwidth၊ GPU-hour
စျေးနှုန်း၊ `d_ff`) အပေါ် အခြေခံသည်၊ benchmark တိုင်းတာမှု မဟုတ်ပါ။ ထို့ကြောင့် တန်ဖိုးများကို
`တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` ဟု မှတ်ပါ။

`lab_attention_cost.py` သည် `d_ff = 4 × d_model = 16384` ဟု ယူသည်၊ `scripts/ex_c_attention_ffn.py`
သည် 7B-class မော်ဒယ်၏ `d_ff = 11008` ကို ယူသည် — ထို့ကြောင့် break-even context သည်
32,768 နှင့် 11,008 ဟု ကွာခြားသည်။ ဤ ကွာခြားမှုသည် အမှား မဟုတ်ဘဲ **ယူဆချက် ကွာခြားမှု**
ဖြစ်သည် — အမြဲ ဖော်ပြထားသည့် ယူဆချက်နှင့် တွဲဖတ်ပါ။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --verbose          # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ lab ၆ ခု (၃ ကြိမ် စီ)
python3 verify_guide.py --labs             # lab များသာ
python3 verify_guide.py --documents        # document ဖိုင်များသာ
python3 guides/02_models_and_inference/labs/run_labs.py
```

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/02_models_and_inference.md`](../../terms/02_models_and_inference.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- area 09 (Infrastructure & serving) သည် ဤနေရာမှ ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည် — [`../../terms/09_infrastructure_and_serving.md`](../../terms/09_infrastructure_and_serving.md)

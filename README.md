# AI Engineering Glossary — English + မြန်မာ

`rohitg00/ai-engineering-from-scratch` ၏ **glossary 250 term** ကို **အင်္ဂလိပ် + မြန်မာ** နှစ်ဘာသာဖြင့်
ပြန်လည် ရေးသားထားသည့် ကိုးကားလမ်းညွှန် (reference course) ဖြစ်သည်။

Term တိုင်းအတွက် —

- **English term** — မူရင်း အမည်အတိုင်း (term များကို မြန်မာလို တိုက်ရိုက် ဘာသာမပြန်ပါ)
- **မြန်မာ** — term ၏ မြန်မာ အမည် သို့မဟုတ် အနီးစပ်ဆုံး ဖော်ပြချက်
- **ဆိုလိုသည့် အဓိပ္ပာယ်** — အင်ဂျင်နီယာ အသုံးအနှုန်းအရ တကယ် ဆိုလိုသည့် အဓိပ္ပာယ် (မြန်မာလို)
- **အရေးပါသည့် အကြောင်းရင်း** — ဘာကြောင့် အရေးပါသည် (မြန်မာလို)
- **မကြာခဏ ရောထွေးမှု**၊ **လက်တွေ့** — source တွင် ပါသည့်အခါ
- **English (source)** — မူရင်း အင်္ဂလိပ် စာသား byte တူညီစွာ
- **Related terms** နှင့် **Learn it** — ဆက်စပ် term များနှင့် source lesson လင့်

## လေ့လာလမ်းညွှန် (Guides)

Term စာရင်းသည် "ဘာလဲ" ကို ဖြေသည်။ `guides/` အောက်ရှိ လမ်းညွှန်များသည် "မည်သည့် အစဉ်ဖြင့် လေ့လာမည်၊
ဘယ်လို အလုပ်လုပ်သည်၊ ဘယ်လောက် ကုန်ကျသည်" ကို ဖြေသည်။

| လမ်းညွှန် | ဖုံးလွှမ်းသည့် နယ်ပယ် | ပါဝင်သည့် အရာ |
|---|---|---|
| [`guides/01_math_and_training/`](guides/01_math_and_training/README.md) | Math & training (term ၄၂) | အစဉ် ၆ အဆင့်၊ ပုံများ၊ lab ၃ ခု (gradient step၊ schedule၊ memory)၊ အောက်ခံစနစ်၊ လေ့ကျင့်ခန်း |
| [`guides/02_models_and_inference/`](guides/02_models_and_inference/README.md) | Models & inference (term ၂၉) | အစဉ် ၆ အဆင့်၊ ပုံ ၁၂ ခု၊ lab ၆ ခု၊ အောက်ခံစနစ်၊ လေ့ကျင့်ခန်း |
| [`guides/03_data_and_representations/`](guides/03_data_and_representations/README.md) | Data & representations (term ၁၃) | အစဉ် ၅ အဆင့်၊ tokenizer/split/pipeline lab |
| [`guides/04_retrieval_and_generation/`](guides/04_retrieval_and_generation/README.md) | Retrieval & generation (term ၁၄) | အစဉ် ၅ အဆင့်၊ index/chunking/prompt-budget lab |
| [`guides/05_prompting_and_context/`](guides/05_prompting_and_context/README.md) | Prompting & context (term ၁၅) | အစဉ် ၅ အဆင့်၊ budget/prefix-cache/prompt-shape lab |
| [`guides/06_agents_and_tools/`](guides/06_agents_and_tools/README.md) | Agents & tools (term ၂၇) | အစဉ် ၆ အဆင့်၊ agent-loop/tool-schema/concurrency lab |

### guides/02 — Models & inference

- **လေ့လာသည့် အစဉ်** — term ၂၉ ခုကို အဆင့် ၆ ဆင့် (အခြေခံ → Transformer → generative → decoding
  → ကုန်ကျစရိတ် → တိုင်းတာမှု) အဖြစ် စီထားသည်၊ term တိုင်း၏ ကြိုတင် သိရမည့် term နှင့်
  ဖွင့်ပေးသည့် အချက် ပါသည်။
- **ပုံရှင်းလင်းချက်** — attention တွက်ချက်မှု၊ Transformer block အတွင်း စီးဆင်းမှု၊ KV cache
  ကြီးထွားမှု၊ prefill/decode၊ sampling pipeline၊ quantization၊ MoE၊ speculative decoding၊
  TTFT/ITL၊ batching — Mermaid ပုံ ၁၂ ခု။
- **Interactive lab** — `lab_sampling.py` (temperature/top-k/top-p)၊ `lab_kv_cache.py`
  (context/layers/dtype/batch)၊ `lab_quantization.py` (bits)၊ `lab_attention_cost.py` (context)၊
  `lab_batching.py` (slots/requests/စျေးနှုန်း)၊ `lab_context_budget.py` (window) — တန်ဖိုး ပြောင်း၍
  ရလဒ် ကြည့်နိုင်သည်၊ offline နှင့် deterministic။
- **အောက်ခံစနစ်** — term တိုင်း GPU memory / compute / latency / throughput / ကုန်ကျစရိတ် /
  production အပေါ် သက်ရောက်မှု (၄)။
- **လေ့ကျင့်ခန်း** — လုပ်ပြထားသည့် ဥပမာ ၆ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၈ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၅ ခု၊
  ဆုံးဖြတ်ချက် ၃ ခု၊ အဖြေများ အပြည့်အစုံ။

စစ်ဆေးခြင်း — `python3 verify_guide.py --verbose` (လမ်းညွှန် တိုင်းအတွက် — ဖိုင် ၆ ခု၊ register၊ term လွှမ်းခြုံမှု၊
Mermaid ပုံ ≥ ၄ ခု၊ lab တိုင်း ၃ ကြိမ် byte-identical၊ ဖိုင်ထဲ ကူးထားသည့် run တိုင်း ပြန် run ၍ တူညီမှု၊
လမ်းညွှန် က ညွှန်သည့် lab/script ဖိုင် တိုင်း တကယ် ရှိမှု)။

**terms-only လမ်းညွှန်** — လမ်းညွှန် တစ်ခုသည် term နှင့် glossary အတိုချုံး သာ ပေးလိုလျှင် README.md ထဲ
`<!-- guide-kind: terms-only -->` ကို ထည့်ရမည်။ ထိုအခါ စစ်ဆေးမှုသည် ဖိုင် တစ်ခု၊ register၊ foreign glyph နှင့်
term လွှမ်းခြုံမှု သာ တောင်းသည် (lab၊ ပုံ၊ လေ့ကျင့်ခန်း မတောင်း)။ ဤ area 11 သည် ထို ပုံစံ ဖြစ်သည်။

## လေ့လာနယ်ပယ် ၁၂ ခု (Learning areas)

| # | Learning area | Term အရေအတွက် | ဖိုင် |
|---|---|---|---|
| 01 | Math & training | 42 | [`terms/01_math_and_training.md`](terms/01_math_and_training.md) |
| 02 | Models & inference | 29 | [`terms/02_models_and_inference.md`](terms/02_models_and_inference.md) |
| 03 | Data & representations | 13 | [`terms/03_data_and_representations.md`](terms/03_data_and_representations.md) |
| 04 | Retrieval & generation | 14 | [`terms/04_retrieval_and_generation.md`](terms/04_retrieval_and_generation.md) |
| 05 | Prompting & context | 15 | [`terms/05_prompting_and_context.md`](terms/05_prompting_and_context.md) |
| 06 | Agents & tools | 27 | [`terms/06_agents_and_tools.md`](terms/06_agents_and_tools.md) |
| 07 | Evaluation & safety | 17 | [`terms/07_evaluation_and_safety.md`](terms/07_evaluation_and_safety.md) |
| 08 | AI-native development | 23 | [`terms/08_ai_native_development.md`](terms/08_ai_native_development.md) |
| 09 | Infrastructure & serving | 18 | [`terms/09_infrastructure_and_serving.md`](terms/09_infrastructure_and_serving.md) |
| 10 | Reliability & operations | 17 | [`terms/10_reliability_and_operations.md`](terms/10_reliability_and_operations.md) |
| 11 | Security & governance | 20 | [`terms/11_security_and_governance.md`](terms/11_security_and_governance.md) |
| 12 | Multimodal systems | 15 | [`terms/12_multimodal_systems.md`](terms/12_multimodal_systems.md) |
| | **စုစုပေါင်း** | **250** | [`terms/00_index.md`](terms/00_index.md) |

Source ၏ website သည် ဤအရေအတွက်များကို ဖော်ပြသည် — Math & training ၄၂၊ Models & inference ၂၉၊ Data &
representations ၁၃၊ Retrieval & generation ၁၄၊ Prompting & context ၁၅၊ Agents & tools ၂၇၊ Evaluation & safety ၁၇၊
AI-native development ၂၃၊ Infrastructure & serving ၁၈၊ Reliability & operations ၁၇၊ Security & governance ၂၀၊
Multimodal systems ၁၅။ ဤ repository ရှိ ဖိုင်များသည် ထို စာရင်းအတိုင်း အားလုံး ပါဝင်သည်။

## ဖိုင်တည်ဆောက်ပုံ

```
AI-Engineering-Glossary-course/
├── README.md                    # ဤဖိုင်
├── COURSE_OUTLINE.md            # လေ့လာသည့် အစီအစဉ် (၄ ပတ်)
├── WRITING_RULES.md             # နှစ်ဘာသာ အရေးအသား စည်းမျဉ်း
├── glossary/
│   ├── terms.json               # source ၏ term ၂၅၀ (machine-readable)
│   ├── burmese_names.json       # term ၂၅၀ ၏ မြန်မာ အမည်
│   └── by_area/NN_<area>.json   # နယ်ပယ်အလိုက် ခွဲထားသည့် data
├── terms/
│   ├── 00_index.md              # A–Z index (term ၂၅၀ လုံး)
│   └── NN_<area>.md             # နယ်ပယ်တိုင်း၏ နှစ်ဘာသာ term စာရင်း
├── guides/                      # လေ့လာလမ်းညွှန် (နယ်ပယ်အလိုက်)
│   └── 02_models_and_inference/  # အစဉ်၊ ပုံများ၊ lab များ၊ အောက်ခံစနစ်၊ လေ့ကျင့်ခန်း
├── verify_glossary.py           # term ၂၅၀ လုံး ပြည့်စုံ/မှန်ကန်ကြောင်း စစ်ဆေးသည့် script
├── verify_guide.py              # လမ်းညွှန်နှင့် lab များ စစ်ဆေးသည့် script
└── quiz.py                      # term များမှ self-quiz ဖန်တီးသည့် script
```

## အသုံးပြုနည်း

```bash
# ၁။ ဖိုင်အားလုံး မှန်ကန်ကြောင်း စစ်ခြင်း
python3 verify_glossary.py

# ၂။ နယ်ပယ်တစ်ခုကို ဖတ်ခြင်း
#    terms/01_math_and_training.md → term တိုင်း၏ နှစ်ဘာသာ ရှင်းလင်းချက်

# ၃။ ကိုယ်တိုင် စစ်ဆေးခြင်း (self-quiz)
python3 quiz.py --area 01 --count 10
python3 quiz.py --seed 42 --count 20 --answers     # အဖြေစာရင်း ပြရန်
```

## Term တစ်ခု ဖတ်သည့်အခါ

1. **English term** ကို အရင် မှတ်ပါ (code၊ paper၊ model card တွင် ထို အမည်အတိုင်း ပေါ်သည်)
2. **ဆိုလိုသည့် အဓိပ္ပာယ်** ကို ဖတ်ပါ — colloquial အသုံးအနှုန်း မဟုတ်ဘဲ အင်ဂျင်နီယာ အဓိပ္ပာယ်
3. **မကြာခဏ ရောထွေးမှု** ကို ဖတ်ပါ — အလွယ်တကူ မှားတတ်သည့် အချက်
4. **ဆက်စပ် term များ** ကို လိုက်ဖတ်ပါ — term တစ်ခုတည်း မဟုတ်ဘဲ အစုအဖွဲ့အဖြစ် မှတ်ပါ
5. **Learn it** လင့်ရှိပါက source lesson သို့ သွား၍ လက်တွေ့ လုပ်ပါ

## လက်ရှိ အခြေအနေ (verified)

| အချက် | ရလဒ် |
|---|---|
| Term ဖိုင်များ | နယ်ပယ် ၁၂ ခု / ဖိုင် ၁၂ ခု (`terms/`) |
| Term အရေအတွက် | **၂၅၀ / ၂၅၀** |
| စာလုံး အရေအတွက် | ၄၀၅,၀၂၃ လုံး / ၃,၄၁၂ လိုင်း |
| `verify_glossary.py` | `TOTAL: 250/250 terms across 12 area file(s)` — `[PASS]` |
| Source အင်္ဂလိပ် စာသား | term တိုင်း byte တူညီစွာ ပါဝင် |
| စကားပြော ပါတ်တစ်လ်လ် / အခြားဘာသာ / emoji | သုည |
| `quiz.py` | `--self-test` အောင်မြင်၊ offline |

ဤ စာရင်းသည် source ၏ ကြေညာချက် — **term ၂၅၀၊ နယ်ပယ် ၁၂** — နှင့် တစ်ခုမှ မကွာ။

## Source နှင့် လိုင်စင်

| အချက် | တန်ဖိုး |
|---|---|
| Glossary page | https://aiengineeringfromscratch.com/glossary |
| Source repository | https://github.com/rohitg00/ai-engineering-from-scratch |
| Glossary ဖိုင် | `glossary/terms.md` (term ၂၅၀) |
| License | MIT |

အင်္ဂလိပ် စာသား (definition များ) ကို source အတိုင်း byte တူညီစွာ ထားရှိပြီး၊ မြန်မာ ဘာသာပြန်/ရှင်းလင်းချက်ကို
ထပ်ပေါင်း ရေးထားသည်။ နည်းပညာ အသုံးအနှုန်းများ (embedding, quantization, KV cache, RAG …) ကို
အင်္ဂလိပ်အတိုင်း ထားရှိသည် — မြန်မာလို တိုက်ရိုက် ဘာသာပြန်ပါက အဓိပ္ပာယ် ပျက်စီးသည်။

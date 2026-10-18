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
│   └── by_area/NN_<area>.json   # နယ်ပယ်အလိုက် ခွဲထားသည့် data
├── terms/
│   ├── 00_index.md              # A–Z index (term ၂၅၀ လုံး)
│   └── NN_<area>.md             # နယ်ပယ်တိုင်း၏ နှစ်ဘာသာ term စာရင်း
├── verify_glossary.py           # term ၂၅၀ လုံး ပြည့်စုံ/မှန်ကန်ကြောင်း စစ်ဆေးသည့် script
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

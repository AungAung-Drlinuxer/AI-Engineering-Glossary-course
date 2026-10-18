# Course Outline — AI Engineering Glossary (English + မြန်မာ)

Source — [`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch) ၏
glossary (`glossary/terms.md`)၊ term **250** ခု၊ လေ့လာနယ်ပယ် **၁၂** ခု။
Website — https://aiengineeringfromscratch.com/glossary

## ဤ course က ဘာကို ပေးသလဲ

Lesson၊ paper၊ model card သို့မဟုတ် code review တစ်ခုတွင် term တစ်ခုကို ရှင်းလင်းချက် မပါဘဲ
သုံးလာသည့်အခါ ချက်ချင်း ပြန်ရှာနိုင်သည့် **နှစ်ဘာသာ ကိုးကားလမ်းညွှန်** ဖြစ်သည်။ Term တိုင်းတွင် —

- အင်ဂျင်နီယာ အသုံးအနှုန်းအရ **တကယ် ဆိုလိုသည့် အဓိပ္ပာယ်** (လူအများ ပြောသည့် အနှစ်ချုပ်နှင့် ကွာခြားနိုင်သည်)
- **ဘာကြောင့် အရေးပါသည်** — မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်
- **မကြာခဏ ရောထွေးမှု** — အလွယ်တကူ မှားတတ်သည့် အချက်
- **လက်တွေ့** — စက်မှု အသုံးချမှု ဥပမာ
- **ဆက်စပ် term များ** — နောက်တစ်ဆင့် ဖတ်ရမည့် term များ
- **Learn it** — source ၏ သက်ဆိုင်ရာ lesson

## လေ့လာနယ်ပယ် ၁၂ ခု

| # | Learning area | Term | ဤနယ်ပယ် ဘာကို ဖုံးလွှမ်းသလဲ |
|---|---|---|---|
| 01 | Math & training | 42 | သင်္ချာ၊ optimizer၊ loss၊ gradient၊ training memory |
| 02 | Models & inference | 29 | မော်ဒယ် ဗိသုကာ၊ inference၊ tokenizer၊ quantization |
| 03 | Data & representations | 13 | data အရည်အသွေး၊ dedup၊ leakage၊ lineage |
| 04 | Retrieval & generation | 14 | embedding၊ vector search၊ chunking၊ RAG |
| 05 | Prompting & context | 15 | prompt၊ context window၊ context engineering |
| 06 | Agents & tools | 27 | agent loop၊ tool စာချုပ်၊ memory၊ MCP |
| 07 | Evaluation & safety | 17 | eval set၊ benchmark၊ calibration၊ safety |
| 08 | AI-native development | 23 | AI ဖြင့် software တည်ဆောက်သည့် လုပ်ငန်းစဉ် |
| 09 | Infrastructure & serving | 18 | serving၊ batching၊ GPU အသုံးချမှု |
| 10 | Reliability & operations | 17 | backpressure၊ timeout၊ circuit breaker၊ incident |
| 11 | Security & governance | 20 | threat model၊ permission၊ policy၊ audit |
| 12 | Multimodal systems | 15 | ရုပ်ပုံ၊ အသံ၊ ဗီဒီယို စနစ်များ |

## လေ့လာသည့် အစီအစဉ် (၄ ပတ် — တစ်နေ့ ၂၀–၃၀ မိနစ်)

| ပတ် | နယ်ပယ် | ပန်းတိုင် |
|---|---|---|
| ပတ် ၁ | 01, 02, 03 | မော်ဒယ် တည်ဆောက်မှု အခြေခံ အသုံးအနှုန်း (84 term) |
| ပတ် ၂ | 04, 05, 06 | RAG၊ prompt၊ agent — လက်တွေ့ စနစ် တည်ဆောက်သည့် term (56 term) |
| ပတ် ၃ | 07, 08, 09 | eval၊ AI-native development၊ serving (58 term) |
| ပတ် ၄ | 10, 11, 12 | ယုံကြည်စိတ်ချရမှု၊ လုံခြုံရေး၊ multimodal (52 term) |

## နေ့စဉ် လေ့လာနည်း

1. နယ်ပယ်တစ်ခုမှ term ၁၀–၁၅ ခုကို ဖတ်ခြင်း — English term → မြန်မာ ရှင်းလင်းချက် → ဆက်စပ် term
2. ဖတ်ပြီးသည့်အခါ `python3 quiz.py --area NN --count 10` ဖြင့် ကိုယ်တိုင် စစ်ခြင်း
3. မှားသည့် term များကို မှတ်စု (Obsidian) တွင် ရေးပြီး နောက်နေ့ ပြန်ဖတ်ခြင်း
4. `Learn it` လင့်ရှိသည့် term များကို source lesson တွင် လက်တွေ့ လုပ်ခြင်း

## စစ်ဆေးခြင်း

```bash
python3 verify_glossary.py                  # term ၂၅၀၊ နယ်ပယ် ၁၂၊ နှစ်ဘာသာ ပြည့်စုံမှု
python3 quiz.py --seed 7 --count 20 --answers
```

## လေ့လာလမ်းညွှန်များ (Guides)

| နယ်ပယ် | လမ်းညွှန် | Term | အဆင့် |
|---|---|---|---|
| 01 — Math & training | [`guides/01_math_and_training/README.md`](guides/01_math_and_training/README.md) | ၄၂ | ၆ |
| 02 — Models & inference | [`guides/02_models_and_inference/README.md`](guides/02_models_and_inference/README.md) | ၂၉ | ၆ |
| 03 — Data & representations | [`guides/03_data_and_representations/README.md`](guides/03_data_and_representations/README.md) | ၁၃ | ၄ |
| 04 — Retrieval & generation | [`guides/04_retrieval_and_generation/README.md`](guides/04_retrieval_and_generation/README.md) | ၁၄ | ၄ |
| 05 — Prompting & context | [`guides/05_prompting_and_context/README.md`](guides/05_prompting_and_context/README.md) | ၁၅ | ၄ |
| 06 — Agents & tools | [`guides/06_agents_and_tools/README.md`](guides/06_agents_and_tools/README.md) | ၂၇ | ၆ |
| 07 — Evaluation & safety | [`guides/07_evaluation_and_safety/README.md`](guides/07_evaluation_and_safety/README.md) | ၁၇ | ၄ |
| 08 — AI-native development | [`guides/08_ai_native_development/README.md`](guides/08_ai_native_development/README.md) | ၂၃ | ၅ |
| 09 — Infrastructure & serving | [`guides/09_infrastructure_and_serving/README.md`](guides/09_infrastructure_and_serving/README.md) | ၁၈ | ၄ |
| 10 — Reliability & operations | [`guides/10_reliability_and_operations/README.md`](guides/10_reliability_and_operations/README.md) | ၁၇ | ၄ |
| 11 — Security & governance | [`guides/11_security_and_governance/README.md`](guides/11_security_and_governance/README.md) | ၂၀ | ၅ |
| 12 — Multimodal systems | [`guides/12_multimodal_systems/README.md`](guides/12_multimodal_systems/README.md) | ၁၅ | ၄ |

လမ်းညွှန် တိုင်းသည် **terms + glossary shortcut** ပုံစံ ဖြစ်သည် — term တိုင်းကို ၃ ကြောင်း
(term ဆိုတာ ဘာလဲ၊ ဥပမာ တစ်ခု၊ အတိုင်းအတာ သို့မဟုတ် အသုံးပြုပုံ) ဖြင့် ရေးထားပြီး အဆင့် ၄–၆ ခုအဖြစ်
စီထားသည်။ `python3 verify_guide.py --verbose` ဖြင့် term ၂၅၀ လုံး ပါဝင်မှုကို စစ်ဆေးသည်။

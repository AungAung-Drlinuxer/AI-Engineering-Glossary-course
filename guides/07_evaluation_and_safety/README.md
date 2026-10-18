# Area 07 — Evaluation & Safety: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် `terms/07_evaluation_and_safety.md` ရှိ term ၁၇ ခုကို **စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့်
သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။
ဤလမ်းညွှန်သည် "ဘာကို တိုင်းတာမည်၊ မည်သည့် data အပေါ် တိုင်းတာမည်၊ output ကို မည်သို့ score မည်၊
model နှစ်ခုကို တရားမျှတစွာ မည်သို့ နှိုင်းယှဉ်မည်၊ release ပြီးနောက် မည်သို့ စောင့်ကြည့်မည်" ကို ဖြေသည်။

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အရာ

- **ဆုံးဖြတ်ချက် အစဉ်** — term ၁၇ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည်။ အဆင့်တိုင်းတွင်
  ကြိုတင် သိရမည့် term နှင့် ဖွင့်ပေးသည့် အချက် ပါဝင်သည်။
- **တိုင်းတာမှု ကိန်းဂဏန်း** — eval set အရွယ်အစား၊ pass@k၊ contamination လွှမ်းမိုးမှု၊ precision နှင့်
  recall၊ eval run ကုန်ကျစရိတ်၊ drift အတိုင်းအတာ အားလုံးကို standard library Python ဖြင့်
  တွက်ချက်ပြထားသည်။
- **ဘေးကင်းရေး ထိန်းချုပ်မှု အလွှာ** — guardrail pipeline၊ red team လုပ်ငန်းစဉ်၊ incident
  စီးဆင်းမှု နှင့် ထုတ်လုပ်မှု စောင့်ကြည့်မှုကို ပုံဖြင့် ဖော်ပြထားသည်။
- **မဖြစ်မနေ ပေါင်းစည်းသည့် အချက်** — တိုင်းတာမှု မရှိဘဲ ဘေးကင်းရေးကို သက်သေပြရန် ခက်ခဲသည်။
  ဘေးကင်းရေး စဉ်းစားချက် မရှိဘဲ တိုင်းတာမှု ရလဒ်သည် ထုတ်လုပ်မှု အရည်အသွေးကို မဖော်ပြနိုင်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၇ ခု (area 07 — Evaluation & safety) |
| အဆင့် | ၅ ဆင့် |
| ဖိုင် | ၄ ခု (ဤလမ်းညွှန်) + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု + `03_theory_to_infrastructure.md` |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 07 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

Lab တိုင်း၏ ရည်ရွယ်ချက်မှာ အဆင့်တစ်ဆင့်၏ တိုင်းတာမှုကို မိမိ လက်ဖြင့် ပြောင်းကြည့်နိုင်ရန်
ဖြစ်သည်။ Flag များသည် lab ဖိုင်၏ `--help` အတိုင်း ဖြစ်ပြီး `--sweep` သည် parameter ကို
အပိုင်းအခြားတစ်ခုလုံးအတွင်း လှည့်၍ ရလဒ်များကို ဘေးချင်း ယှဉ်ပြသည်။

| ကြိမ် | ဖတ်ရမည့် အဆင့် | လက်တွေ့ လုပ်ရမည့် အရာ |
|---|---|---|
| ၁ | အဆင့် ၁ + ၂ | `python3 labs/lab_eval_size.py --n 400 --acc-a 0.877 --acc-b 0.902` |
| ၂ | အဆင့် ၂ + ၃ | `python3 labs/lab_eval_size.py --sweep` |
| ၃ | အဆင့် ၄ | `python3 labs/lab_guardrail_cost.py --rps 40 --latency-ms 20` |
| ၄ | အဆင့် ၄ + ၅ | `python3 labs/lab_guardrail_cost.py --sweep` |
| ၅ | အဆင့် ၅ | `python3 labs/lab_drift_monitor.py --window 800 --baseline 0.912 --observed 0.871 --threshold 2` |

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၇ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၇ ခု — eval set နှင့် training data၊ contamination၊ eval harness loop၊ scoring၊ model နှိုင်းယှဉ်မှု၊ guardrail pipeline၊ red team နှင့် incident၊ drift စောင့်ကြည့်မှု |
| `03_theory_to_infrastructure.md` | တိုင်းတာမှုနှင့် ဘေးကင်းရေးသည် deployment၊ cost နှင့် operations အပေါ် သက်ရောက်မှု (တစ်ပြိုင်နက် ရေးသားနေသည်) |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| `labs/` | interactive lab သုံးခု — `lab_eval_size.py` (eval အရွယ်အစားနှင့် model ခွဲခြားနိုင်မှု)၊ `lab_guardrail_cost.py` (guardrail ၏ latency၊ throughput နှင့် ကုန်ကျစရိတ်)၊ `lab_drift_monitor.py` (window အလိုက် drift statistic နှင့် သတိပေးချက်၏ ကုန်ကျစရိတ်)။ `run_labs.py` ဖြင့် အားလုံးကို တစ်ကြိမ်တည်း run နိုင်သည် |
| `scripts/` | `03_theory_to_infrastructure.md` ရှိ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script သုံးခု |

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 07 --documents --verbose
python3 verify_guide.py --guide 07 --labs
```

`--documents` သည် ဖိုင် လေးခုစီ၏ အရှည်၊ register သန့်ရှင်းမှု၊ term လွှမ်းခြုံမှုနှင့်
Mermaid ပုံ အရေအတွက်ကို စစ်သည်။ `04_exercises.md` ရှိ ကိန်းဂဏန်း တိုင်းကို ဖော်မြူလာ၊
ယူဆချက်နှင့် ထည့်ထားသည့် output နှင့်အတူ ပေးထားသဖြင့် မိမိ စက်တွင် ပြန် run ၍ တိုက်စစ်နိုင်သည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/07_evaluation_and_safety.md`](../../terms/07_evaluation_and_safety.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- ဤနယ်ပယ်နှင့် ဆက်စပ်သည့် နယ်ပယ် — area 11 (Security & governance) နှင့် area 10 (Reliability & operations)

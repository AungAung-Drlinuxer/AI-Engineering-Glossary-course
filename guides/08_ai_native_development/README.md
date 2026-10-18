# Area 08 — AI-native development: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`terms/08_ai_native_development.md`](../../terms/08_ai_native_development.md) ရှိ term **၂၃ ခု** ကို
**ကိုးကား စာရင်း** အဖြစ်မှ **လုပ်ငန်းစဉ် တစ်ခု** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည်
"ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည် "agent တစ်ခုအား အလုပ်တစ်ခုကို မည်သို့
သတ်မှတ်သည်၊ context နှင့် နယ်နိမိတ်ကို မည်သို့ ပေးသည်၊ ထွက်ပေါ်လာသည့် patch ကို မည်သည့်
အထောက်အထားဖြင့် လက်ခံသည်၊ ထို လုပ်ငန်းစဉ်၏ ကုန်ကျစရိတ်ကို မည်သို့ တွက်သည်" ကို ဖြေသည်။

ဤနယ်ပယ်သည် မော်ဒယ် အရည်အသွေးထက် **လုပ်ငန်းစဉ် ဖွဲ့စည်းပုံ** — spec၊ context၊ နယ်နိမိတ်၊
အတည်ပြုမှု နှင့် တိုင်းတာမှု — အပေါ် အလေးထားသည်။ ထို့ကြောင့် ဤလမ်းညွှန်ရှိ ကိန်းဂဏန်း တိုင်းသည်
"token မည်မျှ ကုန်သည်၊ လူ မည်မျှ နာရီ ကုန်သည်၊ defect မည်မျှ လွတ်မြောက်သည်၊ merged change တစ်ခု
မည်မျှ ကုန်ကျသည်" ဟူသည့် မေးခွန်းများကို အဖြေပေးသည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၂၃ ခု (area 08 — AI-native development) |
| ဖိုင် | ဤ folder ရှိ document ၄ ခု (README၊ အစဉ်၊ ပုံများ၊ လေ့ကျင့်ခန်း) + `03_theory_to_infrastructure.md`၊ lab များ၊ `scripts/` |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 08 --documents --verbose` |

ဤလမ်းညွှန်၏ ဥပမာ ကိန်းဂဏန်း တိုင်းသည် ဖော်ပြထားသည့် Python block ကို run လုပ်ပါက ပြန်လည်
ရရှိသည့် output ဖြစ်သည်။ ကိန်းဂဏန်း တိုင်းသည် သတ်မှတ်ထားသည့် ယူဆချက် (assumption) အပေါ်
မှီခိုသဖြင့် ဖော်မြူလာ တစ်ခုစီနှင့်အတူ ထို ယူဆချက်ကို ဖော်ပြထားသည်။

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် အပိုင်း | လက်တွေ့ လုပ်ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_context_strategy.py --scope-files 60 --window 32000` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၄ | `python3 labs/lab_review_budget.py --generated-lines 1200 --defect-rate 0.08` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃–၄ | `python3 labs/lab_review_budget.py --generated-lines 3000 --defect-rate 0.12` |
| ၄ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၅–၈ | `python3 labs/lab_change_cost.py --tasks 100 --attempts 4 --success-rate 0.62` |
| ၅ | [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_change_cost.py --success-rate 0.45 --attempts 5`၊ `python3 labs/lab_context_strategy.py --repo-files 900 --window 128000` |

ကြိမ် တိုင်း၏ ပန်းတိုင်သည် တူညီသည် — term ဖတ်ပြီးနောက် ထို term က ကိန်းဂဏန်း အနေဖြင့်
မည်မျှ သက်ရောက်သည် ကို lab ဖြင့် တိုက်စစ်ခြင်း ဖြစ်သည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၂၃ ခုကို အဆင့် ၆ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ checkpoint မေးခွန်း၊ prerequisite graph၊ ထိုင်ရမည့် အစီအစဉ် |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၈ ခု — spec မှ patch အထိ လမ်းကြောင်း၊ agent ရရှိသည့် context အစုအဝေး၊ လူ၏ ဂိတ်ပါသည့် review လှည့်ပတ်မှု၊ test-first နှင့် test-after၊ diff review checklist၊ tool ခွင့်ပြုချက် နှင့် scope နယ်နိမိတ်၊ session များအကြား handoff၊ workflow ယုံကြည်စိတ်ချရမှု |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း repository context၊ CI၊ cost၊ လူ၏ အချိန် နှင့် production အပေါ် သက်ရောက်မှု (အပြိုင် ရေးသားနေသည်) |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု + `run_labs.py` (usage နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | `03_theory_to_infrastructure.md` ရှိ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script များ |

`03_theory_to_infrastructure.md`၊ `labs/` နှင့် `scripts/` သည် ဤ လမ်းညွှန်၏ အခြား ဖိုင်များ ဖြစ်သည်။
၎င်းတို့ကို အထက်ပါ verify command တစ်ခုတည်းဖြင့် တူညီစွာ စစ်ဆေးသည် — ကူးထားသည့် run တိုင်း
ပြန်လည် run လုပ်ပါက တူညီသည့် output ရရမည်။

## Interactive lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်ရမည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရရမည်။ သို့မှသာ မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| [`labs/lab_context_strategy.py`](labs/lab_context_strategy.py) | `--repo-files`၊ `--avg-file-tokens`၊ `--scope-files`၊ `--window`၊ `--price-per-mtok` | whole-repo context သည် window ထဲ ဆံ့မှု၊ scoped context ၏ တန်ဖိုး၊ USD / task |
| [`labs/lab_review_budget.py`](labs/lab_review_budget.py) | `--generated-lines`၊ `--review-min-per-100`၊ `--defect-rate`၊ `--reviewer-capacity-min` | review minutes၊ capacity ကျော်လွန်သည့် queue၊ လွတ်ထွက်သည့် defect၊ review USD |
| [`labs/lab_change_cost.py`](labs/lab_change_cost.py) | `--tasks`၊ `--attempts`၊ `--success-rate`၊ `--tokens-per-attempt`၊ `--price-per-mtok`၊ `--repo-hour-cost` | မျှော်မှန်း attempt၊ merged change တစ်ခုလျှင် ကုန်ကျစရိတ်၊ retry multiplier |

Lab အားလုံးကို တစ်ကြိမ်တည်း run လိုပါက —

```bash
python3 guides/08_ai_native_development/labs/run_labs.py
```

lab တိုင်းတွင် `--sweep` (knob တစ်ခုကို အပိုင်းအခြားအတွင်း လှည့်ကြည့်ခြင်း) နှင့် `--self-test`
entry point ရှိသည်။ `--self-test` ကို run လုပ်ပါက ရလဒ်သည် run တိုင်း တူညီရမည်၊
မတူပါက lab သည် တိုင်းတာမှု ကိရိယာ အဖြစ် အသုံးမဝင်ပါ။ Flag တိုင်း၏ အဓိပ္ပာယ်ကို
`python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 08 --documents --verbose   # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု ၂၃ ခု၊ Mermaid ပုံ
python3 verify_guide.py --guide 08 --labs                   # lab များ (၃ ကြိမ် စီ run)
python3 guides/08_ai_native_development/labs/run_labs.py     # lab များ၏ ရလဒ် စုစည်းမှု
```

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/08_ai_native_development.md`](../../terms/08_ai_native_development.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- area 07 (Evaluation & safety) သည် ဤနေရာ၏ verification gate များနှင့် တိုက်ရိုက် ဆက်စပ်သည် — [`../../terms/07_evaluation_and_safety.md`](../../terms/07_evaluation_and_safety.md)
- area 10 (Reliability & operations) သည် ဤနေရာမှ ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည် — [`../../terms/10_reliability_and_operations.md`](../../terms/10_reliability_and_operations.md)

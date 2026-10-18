# Area 05 — Prompting & context: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`../../terms/05_prompting_and_context.md`](../../terms/05_prompting_and_context.md) ရှိ term ၁၅ ခုကို
**စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည်
"ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည် "ဤ term ကို မည်သည့် အစဉ်ဖြင့် လေ့လာမည်၊
inference တစ်ခုစီတွင် မော်ဒယ် တကယ် မြင်သည့် အရာ သည် ဘာလဲ၊ ထို အရာကို ဘယ်လောက် ခွဲဝေမည်၊
မည်သို့ ကာကွယ်မည်" ကို ဖြေသည်။

ဤနယ်ပယ်၏ အထူးအချက်မှာ ဤသင်ခန်းစာ အားလုံးသည် **အပြင်ဘက် မှ ထိန်းချနိုင်သည့် တစ်ခုတည်းသော
အလွှာ** — prompt နှင့် context — အပေါ် ရည်ရွယ်ထားခြင်း ဖြစ်သည်။ မော်ဒယ်၏ weight ကို ပြင်ရန်
မလိုဘဲ ပြောင်းလဲနိုင်သည့် အရာ အားလုံး — ညွှန်ကြားချက်၊ ဥပမာ၊ ရယူထားသည့် အထောက်အထား၊
ကန့်သတ်ချက်၊ output ပုံစံ — သည် ဤနေရာတွင် ရှိသည်။ ထို့ကြောင့် ဤနယ်ပယ်သည် တိုင်းတာ၍ ရသည်၊
ကုန်ကျစရိတ် တွက်နိုင်သည်၊ regression test ဖြင့် ထိန်းနိုင်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၁၅ ခု (area 05 — Prompting & context) |
| အဆင့် | ၅ ဆင့် |
| ဖိုင် | document ၅ ခု (ဤ README အပါအဝင်) + lab ၃ ခု (ရေးသားနေဆဲ) |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 05 --documents --verbose` |

## လေ့လာသည့် အစဉ် (၅ ကြိမ်)

ကြိမ်တိုင်းတွင် **ဖတ်ရမည့် အပိုင်း** နှင့် **run ရမည့် lab** တွဲထားသည်။ lab များသည်
offline နှင့် deterministic ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း တူညီသည့် ရလဒ် ရသည်၊
ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | run ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁ | `python3 labs/lab_token_budget.py --window 16384` |
| ၂ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၂ နှင့် [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၃ | `python3 labs/lab_shape_prompt.py --task classify --examples 2` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_shape_prompt.py --sweep` |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄ | `python3 labs/lab_token_budget.py --sweep` နှင့် `python3 labs/lab_prefix_cache.py --calls 12000` |
| ၅ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၅ နှင့် [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_shape_prompt.py --examples 0 --cot on --seed 1` နှင့် `python3 labs/lab_prefix_cache.py --prefix-tokens 8000 --calls 500` |

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၁၅ ခုကို အဆင့် ၅ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၈ ခု — context window ကို budget အဖြစ် မြင်ခြင်း၊ prompt တည်ဆောက်ပုံ၊ request တစ်ခု၏ လည်ပတ်မှု၊ zero-shot / few-shot / chain-of-thought နှိုင်းယှဉ်ချက်၊ structured output နှင့် schema စစ်ဆေးခြင်း၊ compaction၊ prompt injection၊ prompt sensitivity အကဲဖြတ်မှု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ — ကိန်းဂဏန်း တိုင်းသည် Python run မှ ရရှိသည် |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | (တစ်ပြိုင်နက် ရေးသားနေသည် — ဤဖိုင်၏ အကြောင်းအရာကို ဤလမ်းညွှန်က မှီခို မထားပါ) |
| [`labs/`](labs/) | lab ၃ ခု (`lab_token_budget.py`၊ `lab_prefix_cache.py`၊ `lab_shape_prompt.py`) နှင့် `run_labs.py` — ရေးသားနေဆဲ ဖြစ်သည် |
| [`../../terms/05_prompting_and_context.md`](../../terms/05_prompting_and_context.md) | term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) |

## Lab များ — တစ်ပြိုင်နက် ရေးသားနေဆဲ

`labs/` folder ကို သီးခြား ရေးသားနေသည်။ ဖိုင် ၃ ခု ရှိပြီး ဖြစ်သည် — `lab_token_budget.py`၊
`lab_prefix_cache.py`၊ `lab_shape_prompt.py` — အပိုင် ဖိုင် တိုးလာနိုင်သည်။ ထို့ကြောင့်
အောက်ပါ knob များနှင့် lab အမည်များကို ကြိမ်တိုင်း၏ လမ်းညွှန်စာအဖြစ် ယူရမည်၊ ပုံသေ
စာချုပ် အဖြစ် မမှတ်ရ။ Token အားလုံးသည် `tokens = ceil(characters / 4)` ဟူသည့် estimator
မှ ရရှိသည့် ခန့်မှန်းတန်ဖိုး ဖြစ်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် | အဆင့် |
|---|---|---|---|
| `labs/lab_token_budget.py` | `--window`၊ `--system`၊ `--instructions`၊ `--examples`၊ `--retrieved`၊ `--history`၊ `--reserve`၊ `--sweep` | အပိုင်း တစ်ခုစီ၏ token၊ FITS သို့မဟုတ် OVERFLOW၊ headroom သို့မဟုတ် shortfall၊ ဖြေရှင်းနည်း တစ်ခုစီ လွတ်စေသည့် token၊ တောင်းဆိုမှု တစ်ခုစီ၏ cost | ၁၊ ၄ |
| `labs/lab_prefix_cache.py` | `--prefix-tokens`၊ `--calls`၊ `--prefill-rate`၊ `--suffix-tokens`၊ `--sweep` | cache ရှိ/မရှိ prefill token၊ saving ရာခိုင်နှုန်း၊ TTFT နှစ်မျိုး၊ cost၊ shared prefix ၏ KV | ၄ |
| `labs/lab_shape_prompt.py` | `--task`၊ `--examples`၊ `--cot`၊ `--seed`၊ `--sweep` | prompt ၏ structure tree၊ အပိုင်း တစ်ခုစီ၏ token၊ လိုအပ်သည့် အပိုင်း ပါ/မပါ စစ်ဆေးမှု | ၂၊ ၃၊ ၅ |
| `labs/run_labs.py` | — | lab တိုင်း၏ `--self-test` ကို တစ်ကြိမ် run ၍ အကျဉ်းချုပ် | အားလုံး |

## ဤလမ်းညွှန်ကို စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 05 --documents --verbose
```

စစ်ဆေးချက်များ — ဖိုင် ၄ ခု ရှိမှု၊ ဖိုင်တိုင်း ၈၀၀ အက္ခရာ ကျော်မှု၊ စကားပြော ပါတ်တစ်လ်လ်
သို့မဟုတ် အခြားဘာသာ အက္ခရာ မပါမှု၊ term ၁၅ ခုလုံး [`01_learning_sequence.md`](01_learning_sequence.md)
တွင် ပါမှု၊ Mermaid ပုံ ၄ ခု အထက် ရှိမှု။ `03_theory_to_infrastructure.md`၊ `labs/README.md`
နှင့် lab script များနှင့် ပတ်သက်သည့် စစ်ဆေးချက်များသည် `labs/` ကို ရေးသားနေသည့်
ပုဂ္ဂိုလ်ထံ ရောက်သည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/05_prompting_and_context.md`](../../terms/05_prompting_and_context.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- ဤလမ်းညွှန်၏ ကိန်းဂဏန်း အဖြေများ — [`04_exercises.md`](04_exercises.md)

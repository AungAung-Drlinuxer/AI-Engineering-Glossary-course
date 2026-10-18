# Area 01 — Math & Training: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် `terms/01_math_and_training.md` ရှိ term **၄၂** ခုကို **စာရင်း** အဖြစ်မှ **လေ့လာနိုင်သည့် သင်ခန်းစာ**
အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။ ဤလမ်းညွှန်သည်
"ဤ term များသည် training loop တစ်ခုအတွင်း မည်သည့် အစဉ်ဖြင့် ဆက်စပ်သည်၊ မည်သည့် အစိတ်အပိုင်း ပျက်ပါက
မည်သည့် လက္ခဏာ ထွက်သည်၊ ကိန်းဂဏန်း အနေဖြင့် မည်သို့ တိုင်းတာမည်" ကို ဖြေသည်။

ဤနယ်ပယ်၏ အဓိက အချက်မှာ term တိုင်း သီးခြား အလုပ်မလုပ်ခြင်း ဖြစ်သည်။ `Weight` များကို `Optimizer`
က update လုပ်သည်၊ `Optimizer` သည် `Gradient` ကို စားသုံးသည်၊ `Gradient` ကို `Backpropagation` နှင့်
`Autograd` က ထုတ်ပေးသည်၊ ထို gradient များသည် `Loss Function` နှင့် `Batch Size` အပေါ် မှီခိုသည်။
ချို့ယွင်းသည့် အစိတ်အပိုင်းကို ရှာရန် ဤကွင်းဆက် တစ်ခုလုံးကို မြင်ရမည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၄၂ ခု (area 01 — Math & training) |
| ဖိုင် | ၄ ခု (ဤ လမ်းညွှန်) + [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) + `labs/` (lab ၃ ခု + `run_labs.py`) |
| အဆင့် | ၆ အဆင့် — အဆင့်တိုင်း ယခင် အဆင့်အပေါ် မှီခိုသည် |
| ပုံ | Mermaid ပုံ ၈ ခု (`02_visual_explanations.md`) |
| လေ့ကျင့်ခန်း | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 01 --documents --verbose` |

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အချက်

Term စာရင်းတွင် term တစ်ခုစီ၏ အဓိပ္ပာယ် ရှိပြီးသား ဖြစ်သည်။ ဤလမ်းညွှန်က ထို အပေါ် ထပ်တိုးပေးသည့်
အချက် ငါးခု ရှိသည် —

1. **အစဉ်** — term ၄၂ ခုကို အဆင့် ၆ ဆင့်အဖြစ် စီထားသည်၊ အဆင့်တိုင်း ယခင်အဆင့်အပေါ် မှီခိုသည်။
2. **ပုံ** — forward/backward ၏ shape များ၊ loss landscape နှင့် gradient step၊ optimizer update trace၊
   learning rate schedule၊ regularization၊ overfitting/underfitting၊ mixed precision၊ batch size အကျိုးသက်ရောက်မှု။
3. **ကိန်းဂဏန်း** — လေ့ကျင့်ခန်း တိုင်းတွင် ဖော်မြူလာ၊ ယူဆချက်နှင့် အဖြေ အတိအကျ ပါဝင်သည်။
4. **လက္ခဏာမှ စစ်ဆေးခြင်း** — loss သည် NaN ဖြစ်ခြင်း၊ loss သည် စောစီးစွာ ရပ်တန့်ခြင်း၊ train နှင့်
   validation ကွဲထွက်ခြင်း ဟူသည့် လက္ခဏာ သုံးခုအတွက် တိုင်းတာရမည့် အချက်၊ အကြောင်းရင်း အစဉ်နှင့် ဖြေရှင်းနည်း။
5. **ဆုံးဖြတ်ချက်** — memory ကန့်သတ်ချက်အောက်တွင် micro-batch၊ gradient accumulation နှင့် learning rate ကို
   မည်သို့ ရွေးမည်၊ generalization gap အတွက် regularization ကို မည်သို့ ချိန်ညှိမည်။

## လေ့လာသည့် အစဉ် (၆ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ လုပ်ရမည့် အရာ |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `labs/lab_memory.py --params-b 1.3 --batch 8 --seq 2048` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၄ | `labs/lab_gradient_step.py --sweep` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃–၄ | `labs/lab_schedule.py --sweep` |
| ၄ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၅–၈ | `labs/lab_schedule.py --schedule cosine --steps 10 --base-lr 2e-3` |
| ၅ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၅–၆ | `labs/lab_memory.py --batch 64 --activation-checkpointing on` |
| ၆ | [`04_exercises.md`](04_exercises.md) | တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု |

Command အားလုံးကို `guides/01_math_and_training/labs/` အတွင်းမှ run ရမည် (သို့မဟုတ် ဖိုင်လမ်းကြောင်း
အပြည့်အစုံ ပေးရမည်)။ Lab အားလုံးကို တစ်ကြိမ်တည်း စစ်ရန် `python3 labs/run_labs.py` ကို run ပါ။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၄၂ ခုကို အဆင့် ၆ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၈ ခု — forward/backward shape၊ loss landscape နှင့် gradient step၊ optimizer update trace၊ learning rate schedule၊ weight decay နှင့် regularization၊ overfitting/underfitting၊ mixed precision၊ batch-size အကျိုးသက်ရောက်မှု |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း memory / compute / time-to-train / stability အပေါ် သက်ရောက်မှု + ကိန်းဂဏန်း ဥပမာ ၃ ခု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု (`lab_gradient_step.py`၊ `lab_schedule.py`၊ `lab_memory.py`) + `run_labs.py` (usage နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `labs/lab_gradient_step.py` | `--lr`၊ `--steps`၊ `--momentum`၊ `--seed`၊ `--sweep` | step တိုင်း၏ w1၊ w2၊ gradient norm နှင့် loss၊ critical lr နှင့် ၎င်း၏ အပေါ်အောက် အပြုအမူ |
| `labs/lab_schedule.py` | `--schedule`၊ `--steps`၊ `--base-lr`၊ `--warmup`၊ `--peak`၊ `--sweep` | schedule တစ်ခုစီ၏ rate ဇယား၊ max၊ min၊ mean နှင့် လျော့သည့် step အရေအတွက် |
| `labs/lab_memory.py` | `--params-b`၊ `--batch`၊ `--seq`၊ `--layers`၊ `--dtype`၊ `--activation-checkpointing`၊ `--sweep` | weights၊ gradients၊ optimizer state နှင့် activations ၏ GiB၊ total VRAM၊ recompute overhead |

### Learning rate sweep — `labs/lab_gradient_step.py --sweep`

```
        lr     final loss        max |w|     loss ratio       status
    0.0100   1.815865e-01   1.034442e+00   3.996757e-02       STABLE
    0.0500   3.470810e-02   1.034442e+00   7.639324e-03       STABLE
    0.1000   4.344602e-03   1.034442e+00   9.562558e-04       STABLE
    0.2000   5.747279e-05   1.034442e+00   1.264988e-05       STABLE
    0.2400   5.435756e-03   1.034442e+00   1.196421e-03       STABLE
    0.2500   4.280289e+00   1.034442e+00   9.421004e-01    DIVERGENT
    0.2600   2.020100e+03   2.247276e+01   4.446282e+02    DIVERGENT
    0.3000   2.097564e+12   7.241485e+05   4.616783e+11    DIVERGENT
    0.4000   1.059954e+28   5.147703e+13   2.332980e+27    DIVERGENT
```

**ဖတ်နည်း** — ဤ quadratic အတွက် critical lr သည် 0.2500 ဖြစ်သည်။ ၎င်း အောက်တွင် loss သည် ကျသည်
(lr 0.20 တွင် final loss 5.747279e-05)၊ ၎င်း အပေါ်တွင် ချဲ့ထွင်သည် (lr 0.30 တွင် 2.097564e+12)။
`Gradient Clipping` နှင့် `Warmup` လိုအပ်သည့် အခြေအနေသည် ဤဇယား၏ အောက်ခြေ အပိုင်း ဖြစ်သည်။

### Schedule နှိုင်းယှဉ်ချက် — `labs/lab_schedule.py --sweep`

```
  schedule       first lr      middle lr        last lr      drops      mean lr
  constant    0.001000000    0.001000000    0.001000000          0  0.001000000
      step    0.001000000    0.000500000    0.000250000          2  0.000583333
    cosine    0.001000000    0.000428843    0.000000000         11  0.000500000
    warmup    0.001500000    0.002382683    0.001000000          8  0.002000000
```

**ဖတ်နည်း** — schedule တိုင်းတွင် mean lr မတူညီပါ (0.001000000၊ 0.000583333၊ 0.000500000၊ 0.002000000)။
ထို့ကြောင့် schedule များကို "peak" ဖြင့် နှိုင်းယှဉ်ပါက အမှားဖြစ်စေသည် — mean lr ဖြင့်
နှိုင်းယှဉ်ရမည်။ `warmup` သည် mean lr အမြင့်ဆုံး ဖြစ်ပြီး first lr သည် 0.001500000 ဖြစ်သည်
(step 0 တွင် မဟုတ်ဘဲ step 1 မှ စတင်သည့်အတွက်)။

### Memory breakdown — `labs/lab_memory.py`

```
component (GiB)                   checkpointing=off   checkpointing=on
weights                                       2.421              2.421
gradients                                     2.421              2.421
optimizer state (Adam fp32)                   9.686              9.686
activations                                  15.564              3.113
--------------------------------------------------------------------------------------------
total VRAM                                   30.093             17.641
recompute overhead (x step FLOPs)               none              1.333
```

**ဖတ်နည်း** — checkpointing သည် activation ကို 5 ဆ လျှော့ပြီး (15.564 မှ 3.113) step FLOPs ကို
1.333 ဆ တင်သည်။ `weights`၊ `gradients` နှင့် `optimizer state` သုံးခုသည် checkpointing အပေါ်
လုံးဝ မှီခိုမှု မရှိပါ — ထို့ကြောင့် ကြိုတင် သတ်မှတ်ထားသည့် ကုန်ကျစရိတ် ဖြစ်သည်။

**ယူဆချက် ကွာခြားမှု —** `labs/lab_memory.py` သည် `d_model` ကို `params = 12 x layers x d²` မှ
ဆင်းသက်စေပြီး activation tensor factor ကို 10 (off) / 2 (on) ဟု ယူသည်။
[`04_exercises.md`](04_exercises.md) ရှိ လေ့ကျင့်ခန်း ၆ သည် activation tensor 12 ခုနှင့်
sequence 2048 ကို ကိုယ်တိုင် သတ်မှတ်သည်။ ထို့ကြောင့် total GiB တန်ဖိုးများ ကွာခြားခြင်းသည်
အမှား မဟုတ်ဘဲ **ယူဆချက် ကွာခြားမှု** ဖြစ်သည် — အမြဲ ဖော်ပြထားသည့် ယူဆချက်နှင့် တွဲဖတ်ပါ။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 01 --documents --verbose
```

ဤ command သည် ဖိုင် ရှိမှု၊ register သန့်ရှင်းမှု (စကားပြော ပါတ်တစ်လ်လ်၊ အခြားဘာသာ အက္ခရာ၊ emoji မပါမှု)၊
term ၄၂ ခုလုံး `01_learning_sequence.md` တွင် ပါမှုနှင့် `02_visual_explanations.md` တွင် Mermaid ပုံ
အနည်းဆုံး ၄ ခု ရှိမှုကို စစ်သည်။ Lab များကို စစ်ရန် `python3 verify_guide.py --guide 01 --labs --verbose`
ကို အသုံးပြုနိုင်သည် (lab တိုင်း၏ `--self-test` ကို ၃ ကြိမ် run ၍ output တူညီမှုကို စစ်သည်)။
`03_theory_to_infrastructure.md` နှင့် `scripts/` အတွက် ထုတ်ပြသည့် ပြဿနာများသည် သီးခြား
ရေးသားသူ၏ အပိုင်း ဖြစ်သည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/01_math_and_training.md`](../../terms/01_math_and_training.md)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- area 02 (Models & inference) သည် ဤနယ်ပယ်မှ ဆက်ဖတ်ရမည့် နယ်ပယ် ဖြစ်သည် — [`../../terms/02_models_and_inference.md`](../../terms/02_models_and_inference.md)
- Course outline နှင့် လေ့လာသည့် အစီအစဉ် — [`../../COURSE_OUTLINE.md`](../../COURSE_OUTLINE.md)

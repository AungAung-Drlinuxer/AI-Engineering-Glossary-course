# Area 06 — Agents & tools: လေ့လာလမ်းညွှန် (Study Guide)

ဤ folder သည် [`terms/06_agents_and_tools.md`](../../terms/06_agents_and_tools.md) ရှိ term ၂၇ ခုကို **စာရင်း** အဖြစ်မှ
**လေ့လာနိုင်သည့် သင်ခန်းစာ** အဖြစ် တိုးချဲ့ထားသည်။ Glossary entry များသည် "ဤ term ဆိုသည်မှာ ဘာလဲ" ကို ဖြေသည်။
ဤလမ်းညွှန်သည် "ဤ term များကို မည်သည့် အစဉ်ဖြင့် ဆက်စပ်မည်၊ tool call တစ်ခု၏ လမ်းကြောင်းသည် မည်သို့ ဖြစ်သည်၊
loop တစ်ခုသည် ဘယ်လောက် ကုန်ကျသည်" ကို ဖြေသည်။

## ဤလမ်းညွှန် ထပ်တိုးပေးသည့် အချက်

Glossary သည် term တိုင်းကို သီးခြားစီ ရှင်းပြသည်။ Agent စနစ် တစ်ခုကို လက်တွေ့ တည်ဆောက်သည့်အခါ
term တိုင်း သီးခြားစီ မလုပ်ဆောင်ပါ — ၎င်းတို့သည် **လည်ပတ်မှု တစ်ခုတည်း၏ အစိတ်အပိုင်းများ** ဖြစ်သည်။
ဤလမ်းညွှန်သည် ထို ဆက်စပ်မှုကို သုံးလမ်းဖြင့် ဖော်ပြသည်။

- **အစဉ် တည်ဆောက်ခြင်း** — term ၂၇ ခုကို အဆင့် ၆ ဆင့်အဖြစ် စီထားသည်။ မော်ဒယ် call တစ်ခုတည်း (one model call) မှ
  စ၍ loop တစ်ခု၊ tool contract၊ harness နှင့် state၊ memory နှင့် handoff၊ ပျက်ကျမှုနှင့် human approval၊
  နောက်ဆုံးတွင် multi-agent နှင့် routing အထိ တည်ဆောက်သည်။
- **ပုံဖြင့် မြင်ခြင်း** — Mermaid ပုံ ၈ ခုဖြင့် agent loop၊ tool contract ၏ validation path၊ turn များအကြား state၊
  harness နှင့် sandbox ၏ နယ်နိမိတ်၊ retry ဆုံးဖြတ်ချက်၊ approval gate နှင့် multi-agent routing တို့ကို ပြသည်။
- **ကိန်းဂဏန်းဖြင့် ချိန်ခြင်း** — token၊ context ကြီးထွားမှု၊ step အရေအတွက်၊ retry ဖြစ်နိုင်ခြေ၊ latency နှင့်
  cache ၏ အကျိုးအမြတ်တို့ကို Python (standard library သာ) ဖြင့် တွက်ပြထားသည်။

ဤလမ်းညွှန်သည် deployment အတွက် မဖြစ်မနေ လိုအပ်သည့် **policy** များကို ဖော်ထုတ်ပေးသည် — tool call အရေအတွက်
ကန့်သတ်ချက်၊ termination condition၊ approval gate နှင့် sandbox နယ်နိမိတ် ဖြစ်သည်။

## အခြေခံ အချက်

| အချက် | တန်ဖိုး |
|---|---|
| Term | ၂၇ ခု (area 06 — Agents & tools) |
| အဆင့် | ၆ ဆင့် |
| ဖိုင် | ၅ ခု + lab ၃ ခု + ကိန်းဂဏန်း script ၃ ခု |
| လိုအပ်သည့် အရာ | Python 3.11+၊ standard library သာ — network၊ GPU၊ API key မလိုပါ |
| Run တိုင်း | deterministic (ရလဒ် တူညီသည်)၊ offline |
| စစ်ဆေးခြင်း | `python3 verify_guide.py --guide 06 --verbose` |

## လေ့လာသည့် အစဉ် (၆ ကြိမ်)

| ကြိမ် | ဖတ်ရမည့် ဖိုင် | လက်တွေ့ run ရမည့် lab |
|---|---|---|
| ၁ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၁–၂ | `python3 labs/lab_agent_loop.py` |
| ၂ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၁–၄ | `python3 labs/lab_tool_schema.py` |
| ၃ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၃ | `python3 labs/lab_agent_loop.py --max-steps 16 --tool-calls 6 --context 8192` |
| ၄ | [`01_learning_sequence.md`](01_learning_sequence.md) အဆင့် ၄ | `python3 labs/lab_agent_loop.py --cost-budget 0.06` |
| ၅ | [`02_visual_explanations.md`](02_visual_explanations.md) ပုံ ၅–၈ | `python3 labs/lab_tool_schema.py --tools 8 --fields 6 --turns 12` |
| ၆ | [`04_exercises.md`](04_exercises.md) | `python3 labs/lab_concurrency.py` |

Lab အားလုံးကို တစ်ကြိမ်တည်း စစ်ဆေးလိုပါက `python3 labs/run_labs.py` ကို run ရမည်။

## ဖိုင်များ

| ဖိုင် | ဘာကို ပေးသည် |
|---|---|
| [`01_learning_sequence.md`](01_learning_sequence.md) | term ၂၇ ခုကို အဆင့် ၆ ဆင့်အဖြစ် အစဉ်လိုက် စီထားသည် — ကြိုတင် သိရမည့် term၊ ဖွင့်ပေးသည့် အချက်၊ အဆင့်တိုင်း၏ စစ်ဆေးမေးခွန်း၊ prerequisite graph |
| [`02_visual_explanations.md`](02_visual_explanations.md) | Mermaid ပုံ ၈ ခု — agent loop၊ tool contract နှင့် validation path၊ state၊ harness နှင့် sandbox၊ retry flow၊ approval gate၊ multi-agent routing၊ skill discovery |
| [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) | term တိုင်း runtime နှင့် ကုန်ကျစရိတ်အပေါ် သက်ရောက်မှု + ကိန်းဂဏန်း ဥပမာ ၃ ခု |
| [`04_exercises.md`](04_exercises.md) | လုပ်ပြထားသည့် ဥပမာ ၄ ခု၊ တွက်ချက်ရသည့် လေ့ကျင့်ခန်း ၆ ခု၊ ပြဿနာ ရှာဖွေခြင်း ၃ ခု၊ ဆုံးဖြတ်ချက် ၂ ခု၊ အဖြေများ အပြည့်အစုံ |
| [`labs/`](labs/) | interactive lab ၃ ခု + `run_labs.py` (usage နှင့် ရလဒ်များ — [`labs/README.md`](labs/README.md)) |
| [`scripts/`](scripts/) | `03_theory_to_infrastructure.md` ၏ ကိန်းဂဏန်း ဥပမာများကို ထုတ်ပေးသည့် script ၃ ခု |

## Lab များ — ဘာကို ပြောင်း၍ ဘာကို ကြည့်မည်

Lab တိုင်းသည် **offline နှင့် deterministic** ဖြစ်သည် — parameter ပြောင်း၍ run ပါက အချိန်တိုင်း
တူညီသည့် ရလဒ် ရသည်၊ ထို့ကြောင့် မိမိ တွက်ချက်မှုနှင့် တိုက်စစ်နိုင်သည်။

| Lab | ပြောင်းနိုင်သည့် knob | ကြည့်ရမည့် ရလဒ် |
|---|---|---|
| `lab_agent_loop.py` | `--max-steps`၊ `--tool-calls`၊ `--result-tokens`၊ `--context`၊ `--price-per-mtok`၊ `--cost-budget`၊ `--sweep` | step တိုင်း၏ prompt token၊ context ကြီးထွားမှု၊ KV MiB၊ cumulative USD၊ step budget နှင့် cost budget အနက် မည်သည့် တစ်ခုက အရင် ရပ်စေသည် |
| `lab_tool_schema.py` | `--tools`၊ `--fields`၊ `--turns`၊ `--price-per-mtok`၊ `--sweep` | turn တိုင်း ပို့သည့် schema token၊ prefix cache ဖြင့် ရရှိသည့် saving၊ malformed tool call ငါးမျိုး၏ ငြင်းပယ်သည့် အကြောင်းရင်း |
| `lab_concurrency.py` | `--sessions`၊ `--turn-tokens`၊ `--kv-per-token-mb`၊ `--gpu-memory-gb`၊ `--step-ms`၊ `--task-steps`၊ `--sweep` | session တစ်ခုလျှင် memory၊ တစ်ပြိုင်နက် ထည့်နိုင်သည့် session အရေအတွက်၊ queue၊ steps per minute နှင့် tasks per minute |

### Step budget နှင့် cost budget — `lab_agent_loop.py`

Default run တွင် step ၈ ခု ပြီးစီးသော်လည်း `--cost-budget 0.06` ဖြင့် run ပါက step ၄ တွင်
ရပ်သည်။ ဤ ကွာခြားမှုသည် **Termination Condition** ၏ အဓိကအချက် ဖြစ်သည် — မည်သည့်
ကန့်သတ်ချက်ကို အရင် ထားမည်ကို ကြိုတင် ဆုံးဖြတ်ရမည်။ cost budget သည် အရင် ရပ်စေပါက
loop သည် ပန်းတိုင် မပြည့်မီ ရပ်နိုင်သဖြင့် escalation အခြေအနေကို လည်း သတ်မှတ်ရမည်။

### Schema overhead နှင့် cache — `lab_tool_schema.py`

tool ၃ ခု၊ field ၄ ခုဖြင့် schema သည် turn တိုင်း 372 token ကျခံစေပြီး cache ဖြင့် 55.00 % သက်သာသည်။
tool ၈ ခု၊ field ၆ ခုဖြစ်ပါက 1,230 token ဖြစ်လာပြီး cache ၏ saving သည် 66.67 % သို့ တိုးသည် —
ဆိုလိုသည်မှာ prefix ကြီးလာသည့်အခါ cache ၏ အကျိုးအမြတ် ပို၍ ကြီးသည်။

### Concurrency — `lab_concurrency.py`

session 64 ခုကို တောင်းသော်လည်း KV cache ကြောင့် 11 ခုသာ ဝင်သည်၊ ကျန် 53 ခု စောင့်ရသည်။
turn token လျှော့ပါက session အရေအတွက် တိုးသည် — ထို့ကြောင့် `Agent State` နှင့် context ကို
ကျစ်လျစ်စေခြင်းသည် concurrency ကို တိုက်ရိုက် တိုးပေးသည်။

## စစ်ဆေးခြင်း

```bash
python3 verify_guide.py --guide 06 --documents --verbose   # ဖိုင်၊ register၊ term လွှမ်းခြုံမှု၊ ပုံ အရေအတွက်
python3 verify_guide.py --guide 06 --labs --verbose        # lab ၃ ခု (+ ၃ ကြိမ် စီ) နှင့် run_labs.py
python3 guides/06_agents_and_tools/labs/run_labs.py
```

`--documents` စစ်ဆေးချက်သည် [`03_theory_to_infrastructure.md`](03_theory_to_infrastructure.md) နှင့်
[`labs/`](labs/) ကိုပါ လွှမ်းခြုံသည်၊ ထို့ကြောင့် run မလုပ်မီ lab များ တည်ရှိရမည်။

## မှီခိုသည့် အခြား ဖိုင်

- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် + မြန်မာ) — [`../../terms/06_agents_and_tools.md`](../../terms/06_agents_and_tools.md)
- အခြေခံ အချက်အလက် (JSON slice) — [`../../glossary/by_area/06_agents_and_tools.json`](../../glossary/by_area/06_agents_and_tools.json)
- A–Z index — [`../../terms/00_index.md`](../../terms/00_index.md)
- Term များ၏ အောက်ခံ အခြေခံသဘောတရားများ — [`../02_models_and_inference/README.md`](../02_models_and_inference/README.md)

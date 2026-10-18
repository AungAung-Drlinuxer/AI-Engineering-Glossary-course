# Labs - Area 05: Prompting & Context

ဤ lab suite သည် area 05 ၏ term များ (Token Budget, Context Window, Prompt Cache, Few-Shot,
Chain of Thought, System Prompt, Context Engineering) ကို လက်တွေ့ တွက်ကြည့်ရန် ဖြစ်သည်။
Python standard library သာ အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည်
(deterministic)။

Token အားလုံးသည် `tokens = ceil(characters / 4)` ဟူသည့် estimator မှ ရရှိသည့် ခန့်မှန်းတန်ဖိုး
ဖြစ်သည်။ စျေးနှုန်းနှင့် rate အားလုံးကို assumption အဖြစ် မှတ်သားထားသည်၊ vendor အလိုက်
ကွာခြားသည်။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/05_prompting_and_context/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 05 Prompting & context (offline, deterministic)
==========================================================================
[PASS] lab_token_budget.py: [PASS] lab_token_budget self-test passed.
[PASS] lab_prefix_cache.py: [PASS] lab_prefix_cache self-test passed.
[PASS] lab_shape_prompt.py: [PASS] lab_shape_prompt self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_token_budget.py - Token budget

Prompt ၏ အစိတ်အပိုင်း တိုင်းအတွက် token ကို ခွဲဝေသည်။ ဇယားတွင် အစိတ်အပိုင်း အလိုက် token၊
fits/overflow အခြေအနေ၊ headroom သို့မဟုတ် shortfall၊ ဖြေရှင်းနည်း တစ်ခုစီ လွတ်စေသည့် token
နှင့် တောင်းဆိုမှု တစ်ခုစီ၏ cost ကို ပြသည်။

```bash
python3 lab_token_budget.py                                    # window 128000, retrieved 24000, history 30000
python3 lab_token_budget.py --window 32000 --retrieved 20000 --history 15000 --examples 6
python3 lab_token_budget.py --history 200000                   # overflow ဖြစ်သည့် အနေအထား
python3 lab_token_budget.py --sweep                            # history 0 .. window
python3 lab_token_budget.py --self-test
python3 lab_token_budget.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_token_budget - token budget breakdown (offline, deterministic)
window=128,000  system=500  instructions=400  examples=3 x 120  retrieved=24,000  history=30,000  reserve-output=4,096
--------------------------------------------------------------------------
  system prompt             :        500
  task instructions         :        400
  few-shot examples         :        360   (3 x 120 tokens)
  retrieved context         :     24,000
  conversation history      :     30,000
  reserved for output       :      4,096
  prompt tokens (input)     :     55,260
  used (input + reserve)    :     59,356  (46.37% of window)
  status                    :       FITS  headroom 68,644 tokens
--------------------------------------------------------------------------
Remedies (each frees tokens):
  shrink retrieved context to 8000 tokens        frees   16,000
  summarise history to 25% of its size           frees   22,500
  drop few-shot examples beyond the first        frees      240
  trim the system prompt by half                 frees      250
  total freed 38,990 tokens -> used after remedies 20,366, headroom 107,634
--------------------------------------------------------------------------
Cost per call at USD 3.00/1e6 input + USD 15.00/1e6 output (assumption):
  input 55,260 tok = USD 0.165780 ; output 4,096 tok = USD 0.061440 ; total USD 0.227220
  after remedies: input 16,270 tok = USD 0.048810 ; total USD 0.110250
မှတ်ချက် - budget သည် reserved output ပါဝင်မှသာ လုံခြုံသည်၊ ထို့ကြောင့် reserve-output ကို နုတ်မထားရ။
==========================================================================
```

`--window 32000 --retrieved 20000 --history 15000 --examples 6` ဖြင့် ပြောင်းသည့် run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_token_budget - token budget breakdown (offline, deterministic)
window=32,000  system=500  instructions=400  examples=6 x 120  retrieved=20,000  history=15,000  reserve-output=4,096
--------------------------------------------------------------------------
  system prompt             :        500
  task instructions         :        400
  few-shot examples         :        720   (6 x 120 tokens)
  retrieved context         :     20,000
  conversation history      :     15,000
  reserved for output       :      4,096
  prompt tokens (input)     :     36,620
  used (input + reserve)    :     40,716  (127.24% of window)
  status                    :   OVERFLOW  shortfall 8,716 tokens
--------------------------------------------------------------------------
Remedies (each frees tokens):
  shrink retrieved context to 8000 tokens        frees   12,000
  summarise history to 25% of its size           frees   11,250
  drop few-shot examples beyond the first        frees      600
  trim the system prompt by half                 frees      250
  total freed 24,100 tokens -> used after remedies 16,616, headroom 15,384
--------------------------------------------------------------------------
Cost per call at USD 3.00/1e6 input + USD 15.00/1e6 output (assumption):
  input 36,620 tok = USD 0.109860 ; output 4,096 tok = USD 0.061440 ; total USD 0.171300
  after remedies: input 12,520 tok = USD 0.037560 ; total USD 0.099000
မှတ်ချက် - budget သည် reserved output ပါဝင်မှသာ လုံခြုံသည်၊ ထို့ကြောင့် reserve-output ကို နုတ်မထားရ။
==========================================================================
```

## lab_prefix_cache.py - Prompt cache / prefix caching

Shared prefix တစ်ခုကို ခေါ်ဆိုမှု အများအပြား အသုံးပြုသည့်အခါ cache ရှိ/မရှိ prefill token၊
saving ရာခိုင်နှုန်း၊ TTFT နှစ်မျိုးနှင့် cost ကို ပြသည်။ Shared prefix ၏ KV ကိုလည်း ပြသည်။

```bash
python3 lab_prefix_cache.py                                   # prefix 3000, calls 100, 8000 tok/s, suffix 200
python3 lab_prefix_cache.py --prefix-tokens 8000 --calls 500 --suffix-tokens 300
python3 lab_prefix_cache.py --sweep                           # calls 1 .. 128
python3 lab_prefix_cache.py --self-test
python3 lab_prefix_cache.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_prefix_cache - prefix caching: prefill tokens, TTFT and cost (offline, deterministic)
prefix=3,000 tokens  calls=100  suffix=200 tokens/call  prefill-rate=8,000 tok/s  overhead=40 ms
--------------------------------------------------------------------------
prefill tokens without cache    :        320,000
prefill tokens with prefix cache:         23,000
prefill tokens saved            :        297,000  (92.81%)
saving per added call (calls>1)  :          2,970
--------------------------------------------------------------------------
TTFT at 8,000 tokens/s prefill:
  without cache   :      40040.0 ms
  with cache      :       2915.0 ms
  saved           :      37125.0 ms
--------------------------------------------------------------------------
cost at USD 3.00 per 1e6 prefill tokens (assumption):
  without cache   : USD     0.960000
  with cache      : USD     0.069000
  saved           : USD     0.891000
--------------------------------------------------------------------------
shared prefix KV stored once    :       1,500.00 MiB  (1.4648 GiB, reference model 0.500 MiB/token)
without sharing, 100 copies would take 146.48 GiB
မှတ်ချက် - prefix cache သည် တည်ငြိမ်သည့် prefix အတွက်သာ သက်ရောက်သည်၊ cache မမိသည့် အခြေအနေကို ပုံမှန် အဖြစ် သဘောထားရမည်။
==========================================================================
```

`--prefix-tokens 8000 --calls 500 --suffix-tokens 300` ဖြင့် ပြောင်းသည့် run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_prefix_cache - prefix caching: prefill tokens, TTFT and cost (offline, deterministic)
prefix=8,000 tokens  calls=500  suffix=300 tokens/call  prefill-rate=8,000 tok/s  overhead=40 ms
--------------------------------------------------------------------------
prefill tokens without cache    :      4,150,000
prefill tokens with prefix cache:        158,000
prefill tokens saved            :      3,992,000  (96.19%)
saving per added call (calls>1)  :          7,984
--------------------------------------------------------------------------
TTFT at 8,000 tokens/s prefill:
  without cache   :     518790.0 ms
  with cache      :      19790.0 ms
  saved           :     499000.0 ms
--------------------------------------------------------------------------
cost at USD 3.00 per 1e6 prefill tokens (assumption):
  without cache   : USD    12.450000
  with cache      : USD     0.474000
  saved           : USD    11.976000
--------------------------------------------------------------------------
shared prefix KV stored once    :       4,000.00 MiB  (3.9062 GiB, reference model 0.500 MiB/token)
without sharing, 500 copies would take 1953.12 GiB
မှတ်ချက် - prefix cache သည် တည်ငြိမ်သည့် prefix အတွက်သာ သက်ရောက်သည်၊ cache မမိသည့် အခြေအနေကို ပုံမှန် အဖြစ် သဘောထားရမည်။
==========================================================================
```

## lab_shape_prompt.py - Prompt ကို ပုံစံ ဖော်ဆောင်ခြင်း

ပုံသေ အစိတ်အပိုင်းများမှ prompt တစ်ခုကို တည်ဆောက်ပြီး token ခန့်မှန်းတန်ဖိုး၊ structure ကို tree
အဖြစ် နှင့် လိုအပ်သည့် အပိုင်း ပါ/မပါကို စည်းမျဉ်း အခြေခံ၍ စစ်ဆေးသည့် ရလဒ်ကို ပြသည်။

```bash
python3 lab_shape_prompt.py                                   # task classify, examples 2, cot off, seed 7
python3 lab_shape_prompt.py --task classify --examples 0 --cot on --seed 1
python3 lab_shape_prompt.py --task extract --examples 4 --cot on --seed 0
python3 lab_shape_prompt.py --sweep                           # examples 0 .. 5, cot off နှင့် on
python3 lab_shape_prompt.py --self-test
python3 lab_shape_prompt.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_shape_prompt - build a prompt and check its sections (offline, deterministic)
task=classify  examples=2  cot=off  seed=7
--------------------------------------------------------------------------
token estimate (estimator: tokens = ceil(characters / 4)):
  total prompt: 139 tokens
structure:
  prompt
  +-- system         32 tok  role and constraints
  +-- instructions   20 tok  task statement
  +-- format         16 tok  output format
  +-- examples       56 tok  2 demonstration(s)
  +-- cot             0 tok  not requested
  +-- input          15 tok  request text
--------------------------------------------------------------------------
required sections for task classify: system, instructions, format, examples, input
  [OK] system present
  [OK] instructions present
  [OK] format present
  [OK] examples present
  [OK] input present
  [OK] all required sections present
--------------------------------------------------------------------------
examples block: 2 x one demonstration ; cot request: absent
မှတ်ချက် - ပုံသေ အစိတ်အပိုင်းများမှ prompt တစ်ခု တည်ဆောက်သည်၊ လိုအပ်သည့် အပိုင်း အားလုံး ပါဝင်မှသာ format လိုက်နာမှုကို ယုံကြည်နိုင်သည်။
==========================================================================
```

`--task classify --examples 0 --cot on --seed 1` ဖြင့် ပြောင်းသည့် run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_shape_prompt - build a prompt and check its sections (offline, deterministic)
task=classify  examples=0  cot=on  seed=1
--------------------------------------------------------------------------
token estimate (estimator: tokens = ceil(characters / 4)):
  total prompt: 99 tokens
structure:
  prompt
  +-- system         32 tok  role and constraints
  +-- instructions   20 tok  task statement
  +-- format         16 tok  output format
  +-- cot            16 tok  reasoning request
  +-- input          15 tok  request text
--------------------------------------------------------------------------
required sections for task classify: system, instructions, format, examples, input
  [OK] system present
  [OK] instructions present
  [OK] format present
  [MISS] examples missing
  [OK] input present
  [WARN] 1 required section(s) missing: examples
--------------------------------------------------------------------------
examples block: 0 x one demonstration ; cot request: included
မှတ်ချက် - ပုံသေ အစိတ်အပိုင်းများမှ prompt တစ်ခု တည်ဆောက်သည်၊ လိုအပ်သည့် အပိုင်း အားလုံး ပါဝင်မှသာ format လိုက်နာမှုကို ယုံကြည်နိုင်သည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 05 --labs --verbose` နှင့်
  `python3 verify_guide.py --guide 05 --documents --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (budget ပြည့်လျှင် headroom
  ရှိသည်၊ overflow လျှင် shortfall တွက်သည်၊ ဖြေရှင်းနည်း တိုင်းသည် token လွတ်စေသည်၊ reserve
  output ကို နုတ်မထားရ၊ ဥပမာ တစ်ခု စီးသည် token တူညီစွာ တိုးစေသည်၊ cache သည် (calls-1)*prefix
  token ကို ချွေတာသည်၊ calls တစ်ခုတည်းတွင် ချွေတာမှု သုည ဖြစ်သည်၊ cached prefill ၏ TTFT
  သည် နိမ့်သည်၊ cot on သည် token တိုးစေသည်၊ လိုအပ်သည့် အပိုင်း မပါလျှင် စစ်ဆေးမှုက ဖော်ထုတ်သည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။

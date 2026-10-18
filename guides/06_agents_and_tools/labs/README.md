# Labs - Area 06: Agents & tools

ဤ lab suite သည် area 06 ၏ term များ (Agent Loop, Termination Condition, Token Budget,
Tool Contract, Structured Output, KV Cache, Concurrency, Agent State) ကို လက်တွေ့
တွက်ကြည့်ရန် ဖြစ်သည်။ Python standard library သာ အသုံးပြုသည်၊ network၊ GPU သို့မဟုတ်
မော်ဒယ် မလိုအပ်ပါ၊ run တိုင်း ရလဒ် တူညီသည် (deterministic)။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/06_agents_and_tools/labs
python3 run_labs.py
```

Lab တိုင်းအတွက် `--self-test` ကို run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 06 Agents & tools (offline, deterministic)
==========================================================================
[PASS] lab_agent_loop.py: [PASS] lab_agent_loop self-test passed.
[PASS] lab_tool_schema.py: [PASS] lab_tool_schema self-test passed.
[PASS] lab_concurrency.py: [PASS] lab_concurrency self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_agent_loop.py - step တိုင်း၏ token၊ context နှင့် cost

Deterministic agent loop တစ်ခုကို simulate လုပ်သည်။ Step တိုင်း prompt token အရေအတွက်၊
output token၊ context ပြီးနောက် အရှည်၊ ထို context ၏ KV MiB၊ step cost နှင့် cumulative
cost ကို ဇယားဖြင့် ပြသည်။ `--max-steps` (step budget) သို့မဟုတ် `--cost-budget`
(cost budget) အနက် မည်သည့် တစ်ခုက အရင် ရပ်စေသည်ကို အဆုံးတွင် ဖော်ပြသည်။

```bash
python3 lab_agent_loop.py                                # default: 8 steps, 3 tool calls, 900 result tokens, 4,096 context, 3.0 USD/Mtok, 0.5 USD budget
python3 lab_agent_loop.py --max-steps 16 --tool-calls 6 --result-tokens 400 --context 8192 --price-per-mtok 5.0
python3 lab_agent_loop.py --cost-budget 0.06             # cost budget က အရင် ရပ်စေသည်
python3 lab_agent_loop.py --sweep                        # step budget 2..32
python3 lab_agent_loop.py --self-test
python3 lab_agent_loop.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_agent_loop - per-step tokens, context growth and cost (offline, deterministic)
max-steps=8  tool-calls=3  result-tokens=900  context=4,096  price=3.0 USD/Mtok  cost-budget=0.5 USD
assumption: output tokens cost 5.0x input, KV 0.5 MiB/token (layers 32, heads 32, head_dim 128, fp16)
--------------------------------------------------------------------------
step  prompt-tok  out-tok  ctx-after  ctx KV MiB   step USD    cum USD  call
   1       4,096      160      5,156     2,578.0   0.014688   0.014688  tool
   2       5,156      160      6,216     3,108.0   0.017868   0.032556  tool
   3       6,216      160      7,276     3,638.0   0.021048   0.053604  tool
   4       7,276      160      7,436     3,718.0   0.024228   0.077832     -
   5       7,436      160      7,596     3,798.0   0.024708   0.102540     -
   6       7,596      160      7,756     3,878.0   0.025188   0.127728     -
   7       7,756      160      7,916     3,958.0   0.025668   0.153396     -
   8       7,916      160      8,076     4,038.0   0.026148   0.179544     -
--------------------------------------------------------------------------
stopped by: step budget at step 8 of 8 (cost budget 0.5 USD)
final context 8,076 tokens = 3.943 GiB KV ; total cost USD 0.179544
prompt tokens billed by re-sending the context: 53,448 over 8 step(s)
မှတ်ချက် - termination condition မရှိလျှင် loop သည် context နှင့် cost ကို အဆက်မပြတ် ကြီးထွားစေသည်။ step budget နှင့် cost budget နှစ်ခုလုံးကို ကြိုတင် သတ်မှတ်ရမည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--cost-budget 0.06`) ၏ အမှန်တကယ် output -
```
==========================================================================
lab_agent_loop - per-step tokens, context growth and cost (offline, deterministic)
max-steps=8  tool-calls=3  result-tokens=900  context=4,096  price=3.0 USD/Mtok  cost-budget=0.06 USD
assumption: output tokens cost 5.0x input, KV 0.5 MiB/token (layers 32, heads 32, head_dim 128, fp16)
--------------------------------------------------------------------------
step  prompt-tok  out-tok  ctx-after  ctx KV MiB   step USD    cum USD  call
   1       4,096      160      5,156     2,578.0   0.014688   0.014688  tool
   2       5,156      160      6,216     3,108.0   0.017868   0.032556  tool
   3       6,216      160      7,276     3,638.0   0.021048   0.053604  tool
   4       7,276      160      7,436     3,718.0   0.024228   0.077832     -
--------------------------------------------------------------------------
stopped by: cost budget at step 4 of 8 (cost budget 0.06 USD)
final context 7,436 tokens = 3.631 GiB KV ; total cost USD 0.077832
prompt tokens billed by re-sending the context: 22,744 over 4 step(s)
မှတ်ချက် - termination condition မရှိလျှင် loop သည် context နှင့် cost ကို အဆက်မပြတ် ကြီးထွားစေသည်။ step budget နှင့် cost budget နှစ်ခုလုံးကို ကြိုတင် သတ်မှတ်ရမည်။
==========================================================================
```

မှတ်ချက် - context သည် step တိုင်း ပြန်လည် ပေးပို့ခံရသောကြောင့် prompt token သည် step
အရေအတွက်နှင့်အတူ အလျင်အမြန် တိုးသည်။ cost budget သည် step budget ထက် အရင် ရပ်စေလျှင်
loop သည် ပန်းတိုင် မပြည့်မီ ရပ်နိုင်သည်၊ ထို့ကြောင့် escalation အခြေအနေကို
လည်း သတ်မှတ်ရမည်။

## lab_tool_schema.py - schema token အပိုနှင့် prefix cache saving

Tool တိုင်းနှင့် field တိုင်း၏ token ကုန်ကျစရိတ်ကို ပုံသေနည်းဖြင့် တွက်သည်။ Turn တိုင်း
ပေးပို့သည့် schema token၊ cumulative overhead နှင့် schema prefix ကို cache လုပ်သည့်အခါ
ရရှိသည့် saving ကို ပြသည်။ ထို့အပြင် ပုံသေ tool spec နှစ်ခု (read_file၊ search_docs)
အတွက် malformed tool call ငါးမျိုးကို deterministic validation ဖြင့် စစ်ဆေးပြီး
ငြင်းပယ်သည့် အကြောင်းရင်းကို ဖော်ပြသည်။

```bash
python3 lab_tool_schema.py                               # default: 3 tools, 4 fields, 5 turns, 3.0 USD/Mtok
python3 lab_tool_schema.py --tools 8 --fields 6 --turns 12
python3 lab_tool_schema.py --sweep                       # turns 1, 2, 4, 8, 16
python3 lab_tool_schema.py --self-test
python3 lab_tool_schema.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_tool_schema - schema tokens per turn, cache saving, call validation
tools=3  fields=4  turns=5  price=3.0 USD/Mtok
assumption: wrapper 30 + tools x (tool 42 + fields x field 18) = 372 tokens of schema, sent every turn
assumption: cache write 1.25x on turn 1, cache read 0.25x afterwards
--------------------------------------------------------------------------
turn  schema tok  sent so far   plain USD  cached USD   saved USD
   1         372          372    0.001116    0.001395   -0.000279
   2         372          744    0.002232    0.001674    0.000558
   3         372        1,116    0.003348    0.001953    0.001395
   4         372        1,488    0.004464    0.002232    0.002232
   5         372        1,860    0.005580    0.002511    0.003069
--------------------------------------------------------------------------
schema overhead over 5 turn(s): 1,860 tokens, USD 0.005580 plain vs USD 0.002511 cached (saving 55.00%)
--------------------------------------------------------------------------
deterministic validation of sample tool calls:
sample                            verdict  reason
valid read_file call                   OK  accepted
unknown tool name                  REJECT  unknown tool name: write_file
required field missing             REJECT  missing required field: path
wrong field type                   REJECT  field query must be string
unexpected field                   REJECT  unexpected field: top_k
duplicate key in args              REJECT  duplicate key: path
--------------------------------------------------------------------------
samples: 1 accepted, 5 rejected before execution
မှတ်ချက် - schema ကို turn တိုင်း ပေးပို့ခြင်းသည် token ကုန်ကျသည်၊ prefix cache ဖြင့် ပြန်လည် အသုံးပြုနိုင်သည်။ validated tool contract မပါဘဲ malformed call ကို လုပ်ဆောင်ခြင်း မပြုရ။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--tools 8 --fields 6 --turns 12`) ၏ အမှန်တကယ် output -
```
==========================================================================
lab_tool_schema - schema tokens per turn, cache saving, call validation
tools=8  fields=6  turns=12  price=3.0 USD/Mtok
assumption: wrapper 30 + tools x (tool 42 + fields x field 18) = 1230 tokens of schema, sent every turn
assumption: cache write 1.25x on turn 1, cache read 0.25x afterwards
--------------------------------------------------------------------------
turn  schema tok  sent so far   plain USD  cached USD   saved USD
   1       1,230        1,230    0.003690    0.004613   -0.000923
   2       1,230        2,460    0.007380    0.005535    0.001845
   3       1,230        3,690    0.011070    0.006457    0.004613
   4       1,230        4,920    0.014760    0.007380    0.007380
   5       1,230        6,150    0.018450    0.008303    0.010148
   6       1,230        7,380    0.022140    0.009225    0.012915
   7       1,230        8,610    0.025830    0.010148    0.015682
   8       1,230        9,840    0.029520    0.011070    0.018450
   9       1,230       11,070    0.033210    0.011992    0.021218
  10       1,230       12,300    0.036900    0.012915    0.023985
  11       1,230       13,530    0.040590    0.013838    0.026752
  12       1,230       14,760    0.044280    0.014760    0.029520
--------------------------------------------------------------------------
schema overhead over 12 turn(s): 14,760 tokens, USD 0.044280 plain vs USD 0.014760 cached (saving 66.67%)
--------------------------------------------------------------------------
deterministic validation of sample tool calls:
sample                            verdict  reason
valid read_file call                   OK  accepted
unknown tool name                  REJECT  unknown tool name: write_file
required field missing             REJECT  missing required field: path
wrong field type                   REJECT  field query must be string
unexpected field                   REJECT  unexpected field: top_k
duplicate key in args              REJECT  duplicate key: path
--------------------------------------------------------------------------
samples: 1 accepted, 5 rejected before execution
မှတ်ချက် - schema ကို turn တိုင်း ပေးပို့ခြင်းသည် token ကုန်ကျသည်၊ prefix cache ဖြင့် ပြန်လည် အသုံးပြုနိုင်သည်။ validated tool contract မပါဘဲ malformed call ကို လုပ်ဆောင်ခြင်း မပြုရ။
==========================================================================
```

မှတ်ချက် - schema သည် ကျစ်လျစ်ပါက turn တိုင်း၏ overhead ကျဆင်းသည်၊ prefix caching သည်
ထို overhead ကို 75 ရာခိုင်နှုန်း ကန့်သတ်ချက်အထိ လျှော့ချသည်။

## lab_concurrency.py - session၊ memory၊ queue နှင့် throughput

တစ်ပြိုင်နက် run သည့် agent session များ၏ memory ကို တွက်သည်။ Session တစ်ခုလျှင်
memory၊ session အားလုံးအတွက် လိုအပ်သည့် memory၊ accelerator တစ်လုံးပေါ် တွင် နေရာရသည့်
session အရေအတွက်၊ စောင့်နေသည့် queue၊ ထို့ကြောင့် ဖြစ်ပေါ်သည့် throughput
(steps per minute နှင့် tasks per minute) ကို ပြသည်။

```bash
python3 lab_concurrency.py                               # default: 64 sessions, 8,192 turn tokens, 0.5 MiB/token, 80 GB, step 1.2 s
python3 lab_concurrency.py --sessions 32 --turn-tokens 4096 --step-ms 900 --task-steps 6
python3 lab_concurrency.py --sweep                       # sessions 8..128
python3 lab_concurrency.py --self-test
python3 lab_concurrency.py --help
```

Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_concurrency - sessions, KV memory, queue and throughput (offline, deterministic)
sessions=64  turn-tokens=8,192  kv-per-token=0.5 MiB  gpu-memory=80 GB  step=1.2 s
assumption: weights 14 GiB, reserved 16 GiB, per-session overhead 0.25 GiB, task 10 steps
--------------------------------------------------------------------------
  gpu memory                 :     80.000 GB
  usable after reserve+weight:     50.000 GiB
  memory per session         :      4.250 GiB  (0.25 overhead + 4.000 KV)
  memory for all sessions    :    272.000 GiB
  sessions that fit          :         11
  queue                      :         53 session(s) wait (11 served in parallel)
  steps per minute           :     550.00
  tasks per minute           :      55.00 (task = 10 steps = 12 s)
  queue clears in            :       60.0 s
--------------------------------------------------------------------------
မှတ်ချက် - ဤ session အရေအတွက်ကို one accelerator ပေါ် တွင် မထားနိုင်ပါ၊ turn တိုင်း context တစ်ခုလုံးကို ပြန်လည် ပေးပို့သောကြောင့် KV cache သည် concurrency ကို ကန့်သတ်သည်။
==========================================================================
```

Knob ပြောင်းထားသည့် run (`--sessions 32 --turn-tokens 4096 --step-ms 900 --task-steps 6`) ၏ အမှန်တကယ် output -
```
==========================================================================
lab_concurrency - sessions, KV memory, queue and throughput (offline, deterministic)
sessions=32  turn-tokens=4,096  kv-per-token=0.5 MiB  gpu-memory=80 GB  step=0.9 s
assumption: weights 14 GiB, reserved 16 GiB, per-session overhead 0.25 GiB, task 6 steps
--------------------------------------------------------------------------
  gpu memory                 :     80.000 GB
  usable after reserve+weight:     50.000 GiB
  memory per session         :      2.250 GiB  (0.25 overhead + 2.000 KV)
  memory for all sessions    :     72.000 GiB
  sessions that fit          :         22
  queue                      :         10 session(s) wait (22 served in parallel)
  steps per minute           :   1,466.67
  tasks per minute           :     244.44 (task = 6 steps = 5.4 s)
  queue clears in            :        5.4 s
--------------------------------------------------------------------------
မှတ်ချက် - ဤ session အရေအတွက်ကို one accelerator ပေါ် တွင် မထားနိုင်ပါ၊ turn တိုင်း context တစ်ခုလုံးကို ပြန်လည် ပေးပို့သောကြောင့် KV cache သည် concurrency ကို ကန့်သတ်သည်။
==========================================================================
```

မှတ်ချက် - session တစ်ခုသည် task တစ်ခုလုံး အတွင်း context တစ်ခုလုံးကို ကိုင်ထားသည်၊
ထို့ကြောင့် concurrency ကို KV cache က ကန့်သတ်သည်။ session ထပ်တိုးခြင်းသည်
throughput ကို မတိုးစေဘဲ queue ကိုသာ ရှည်စေသည်။

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 06 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (step တိုင်း context ကြီးထွားသည်၊
  tool call ပိုလျှင် context ပိုကြီးသည်၊ cost budget သည် အရင် ရပ်စေသည်၊ schema token သည်
  tool နှင့် field အပေါ် linear ဖြစ်သည်၊ malformed call အားလုံး ငြင်းပယ်ခံရသည်၊
  session memory သည် context အပေါ် linear ဖြစ်သည်၊ context ရှည်လျှင် session နည်းသည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
- စျေးနှုန်း၊ KV byte ပမာဏ၊ step အချိန်နှင့် throughput အားလုံးသည် ယူဆချက် (assumption)
  ဖြစ်သည်၊ hardware၊ provider နှင့် configuration အလိုက် ကွာခြားသည်။

# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၆ — Agents & tools ၏ term ၂၇ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။ agent engineering ၏ ဝေါဟာရတိုင်းသည် နောက်ဆုံးတွင် ကိန်းဂဏန်း တစ်ခုအပေါ် ရောက်သည် — turn တိုင်း၏ context token အရေအတွက်၊ step တစ်ခု၏ latency၊ တစ်ပြိုင်နက် ထိန်းနိုင်သည့် session အရေအတွက်၊ သို့မဟုတ် task တစ်ခု၏ USD cost ဖြစ်သည်။ ထိုကိန်းကို မတွက်လျှင် agent တစ်ခု၏ ကုန်ကျစရိတ်နှင့် ရပ်တန့်ချိန်ကို ခန့်မှန်းခြင်း မပြုနိုင်ပါ။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/06_agents_and_tools/scripts/` အောက်ရှိ Python script များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုသည်၊ မော်ဒယ် ကို ခေါ်ယူခြင်း မရှိပါ၊ network ကို မသုံးပါ၊ run တိုင်း ရလဒ် တူညီသည်။ စျေးနှုန်း၊ KV byte ပမာဏ၊ context အရှည်၊ step အရေအတွက် စသည့် ယူဆချက် တိုင်းကို script ၏ ဖော်ပြချက်နှင့် ဤစာတမ်းတွင် `assumption` အဖြစ် တိကျစွာ မှတ်တမ်းတင်ထားသည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

**GPU memory (context growth နှင့် KV cache)** — accelerator တစ်လုံးပေါ် တွင် တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ inference တွင် ၎င်းကို weight၊ KV cache၊ activation နှင့် runtime buffer တို့ ခွဲယူသည်။ Agent အခြေအနေတွင် KV cache သည် turn အရေအတွက်နှင့် context အရှည်အလိုက် ကြီးထွားသည်၊ ဥပမာ (က) တွင် reference model ၏ KV cache သည် token တစ်လုံးလျှင် 0.500 MiB ဖြစ်ပြီး turn ၁၂ ခုပြီးနောက် 6.699 GiB သို့ ရောက်သည်။ ဤဝင်ရိုးသည် အမာခံ ကန့်သတ်ချက် ဖြစ်သည်၊ ပြည့်လျှင် session အသစ် လက်မခံနိုင်တော့ပါ။

**compute (FLOPs utilisation)** — tool schema ကို process လုပ်ခြင်း၊ ရှည်လျားသည့် prompt ကို prefill လုပ်ခြင်းနှင့် output ထုတ်လုပ်ခြင်းအတွက် လိုအပ်သည့် arithmetic ပမာဏ ဖြစ်သည်။ agent တွင် compute သည် step တိုင်း prompt တစ်ခုလုံးကို ပြန်လည် process လုပ်ရသောကြောင့် token အရေအတွက်နှင့် တိုက်ရိုက် အချိုးကျသည်။ prompt caching သည် ဤ compute ကို ချွေတာသည့် အဓိက knob ဖြစ်သည်။

**latency per step နှင့် per task** — step တစ်ခုသည် မော်ဒယ် ခေါ်ယူမှု တစ်ကြိမ် (သို့မဟုတ် အနည်းငယ်) နှင့် tool လုပ်ဆောင်မှု တစ်ခု ပါဝင်သည့် အလှည့် တစ်ခု ဖြစ်သည်။ task တစ်ခု၏ latency သည် step latency × step အရေအတွက် နှင့် queue တွင် စောင့်သည့် အချိန် ပေါင်းလဒ် ဖြစ်သည်။ ထို့ကြောင့် step အရေအတွက်ကို ကန့်သတ်ခြင်းသည် task latency ကို ကန့်သတ်ခြင်း ဖြစ်သည်၊ ဥပမာ (ဂ) တွင် step တစ်ခု ၁.၂ စက္ကန့် ယူသောကြောင့် ၁၀ step task တစ်ခုသည် ၁၂ စက္ကန့် ဖြစ်သည်။

**throughput of concurrent sessions** — တစ်စက္ကန့် သို့မဟုတ် တစ်မိနစ်အတွင်း run နိုင်သည့် step အရေအတွက်နှင့် ပြီးစီးသည့် task အရေအတွက် ဖြစ်သည်။ agent session တစ်ခုသည် task တစ်ခုလုံး အတွင်း context တစ်ခုလုံးကို ကိုင်ထားသောကြောင့် concurrency သည် KV cache ဖြင့် ကန့်သတ်ခံရသည်၊ ဥပမာ (ဂ) တွင် 32,768-token session ၆၄ ခုအတွက် session ၃ ခုသာ တစ်ပြိုင်နက် နေရာရပြီး ကျန် ၆၁ ခုသည် queue တွင် စောင့်သည်။

**cost per task (သို့မဟုတ် per million tokens)** — task တစ်ခုအတွက် ကျသင့်သည့် ငွေပမာဏ ဖြစ်သည်။ prompt token၊ output token နှင့် ထို token များ၏ စျေးနှုန်းဖြင့် တွက်သည်။ agent တွင် prompt token သည် step တိုင်း ပြန်လည် ပေးပို့သောကြောင့် output token ထက် အဆများစွာ ပိုသည်၊ ဥပမာ (ခ) တွင် step ၁၀ ခုအတွင်း prompt token 53,500 ခု ကျသင့်သည်။ prefix caching သည် ဤကိန်းကို တိုက်ရိုက် လျှော့ချသည်။

**production consequence (ကျိုးပျက်သည့် အပုံစံ)** — ဝင်ရိုး တစ်ခုကို လျစ်လျူရှုလျှင် ထုတ်လုပ်မှုတွင် မည်သည့် အရာ ကျိုးပျက်သည်ကို ဆိုလိုသည်။ KV cache ကို မတွက်လျှင် session လက်ခံနိုင်မှု ကျဆင်းသည်၊ termination condition မရှိလျှင် loop သည် cost budget ကို ဖြုန်းတီးသည်၊ tool contract မရှိလျှင် malformed call သည် စနစ်အဆင့်သို့ ရောက်သည်။ ဤစာတမ်းရှိ ဇယားတိုင်းတွင် ဤဝင်ရိုးကို အတိအကျ ဖော်ပြထားသည်။

## ၂။ Master table — term ၂၇ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Agent | latency per task | step အရေအတွက်က task ကုန်ကျစရိတ်ကို ဆုံးဖြတ်သည် | steps per task | step ကန့်သတ်ချက် မရှိလျှင် latency နှင့် cost ခန့်မှန်းခြင်း မပြုနိုင် |
| Agent Harness | cost per task | context စုစည်းမှုနှင့် limit ချမှတ်မှုက prompt token ကို ဆုံးဖြတ်သည် | prompt tokens per step | harness မတူလျှင် model တူသော်လည်း cost per task ကွာသည် |
| Agent Memory | GPU memory | prompt ထဲ ထည့်မည့်အစား ပြင်ပတွင် သိမ်းဆည်းသည် | retrieved memory tokens | မှတ်ဉာဏ် မရွေးချယ်လျှင် context window ပြည့်ပိတ်သည် |
| Agent State | latency per task | transcript မှ progress ပြန်တည်ဆောက်မှုကို ရှောင်သည် | state bytes, resume steps | state မရှိလျှင် ရှည်ကြာသည့် task ကို resume လုပ်ခြင်း မပြုနိုင် |
| Agent Skill | cost per task | လိုအပ်သည့်အခါမှ workflow ကို context ထဲ ထည့်သည် | skill body tokens loaded | activate ပြီးသည့် skill တိုင်း prompt token စားသည် |
| Approval Gate | latency per task | လူ၏ အတည်ပြုချက် စောင့်ဆိုင်းချိန် တိုးသည် | approval wait seconds | gate မရှိလျှင် ပြန်လည် မဖျက်နိုင်သည့် ဘေးထွက်ဆိုးကျိုး ဖြစ်နိုင် |
| Checkpoint | latency per task | crash ပြီးနောက် ပြန်လုပ်ရမည့် step ကို ဖျက်သည် | replay tokens avoided | checkpoint မရှိလျှင် crash တိုင်း task ကို အစမှ ပြန်လုပ်ရသည် |
| Compensating Action | cost per task | ဆန့်ကျင်သည့် လုပ်ဆောင်ချက် တစ်ခု ထပ်ဆောင်း လိုသည် | compensation calls per task | compensation မရှိလျှင် ဘေးထွက်ဆိုးကျိုး ကျန်ရစ်သည် |
| Delegation | throughput | subtask များကို တစ်ပြိုင်နက် run စေသည် | concurrent subtasks | scope contract မရှိလျှင် ရလဒ် ပေါင်းစပ်ခြင်း မပြုနိုင် |
| Durable Execution | latency per task | transition တိုင်း persist လုပ်ခြင်း ကုန်ကျသည် | persisted transitions | replay မရှိလျှင် အတည်ပြုပြီး ဘေးထွက်ဆိုးကျိုး ထပ်ဖြစ်သည် |
| Function Calling | cost per task | schema နှင့် tool result token ကုန်ကျသည် | schema + result tokens | validate မလုပ်လျှင် tool call သည် လုံခြုံရေး နယ်နိမိတ် ဖြစ်မလာ |
| Human-in-the-Loop (HITL) | throughput | လူ၏ ဆုံးဖြတ်ချိန်က throughput ကို ကန့်သတ်သည် | human decisions per task | စစ်ဆေးသူ မလုံလောက်လျှင် queue ရှည်သည် |
| MCP (Model Context Protocol) | cost per task | tool discovery ကို စာချုပ်တစ်ခုတည်းဖြင့် စံပြုသည် | discovered tool tokens | discovery token မတွက်လျှင် prefix ကြီးလာသည် |
| Multi Round-Trip Request (MRTR) | latency per step | round trip အပို တစ်ကြိမ် လိုသည် | round trips per request | input_required ကို မကိုင်တွယ်လျှင် tool call မပြီးမြောက် |
| Orchestration | latency per task | အဆင့် အစဉ်၊ retry နှင့် ရပ်ခြင်းကို ဆုံးဖြတ်သည် | steps and retries | retry နှင့် termination မသတ်မှတ်လျှင် cost ပေါက်ကြွ |
| Planning | cost per task | မှားသော step ကို ကြိုတင် တားဆီးသည် | plan length, replans | plan မစစ်လျှင် မပြန်နိုင်သည့် လုပ်ဆောင်ချက် အရင် ဖြစ်နိုင် |
| ReAct | latency per step | observation တိုင်း round trip နှင့် token အပိုဖြစ်စေသည် | observation tokens per step | loop ကန့်သတ်ချက် မရှိလျှင် context ကြီးထွားသည် |
| Sandbox | cost per task | သီးခြားခွဲထုတ်သည့် container ဖန်တီးမှု ကုန်ကျသည် | container starts per task | isolation မရှိလျှင် သက်ရောက်မှု အတိုင်းအတာ ကြီးသည် |
| Skill Bundle | cost per task | bundle အပြည့်အစုံ တပ်ဆင်ခြင်း disk ကုန်ကျသည် | bundle bytes installed | entry file သာ ကူးလျှင် workflow ကျိုးပျက်သည် |
| Skill Catalog | cost per task | catalog entry တိုင်းက prompt token စားသည် | catalog tokens in prompt | catalog ကို မတိုင်းလျှင် system prompt ကြီးလာသည် |
| Skill Discovery | latency per task | root ရှာဖွေမှုသည် စတင်ချိန် အချိန်ယူသည် | discovery ms at start-up | malformed package ကို မဖော်ထုတ်လျှင် routing မှားသည် |
| Skill Invocation | cost per task | activate လုပ်သည့် skill ၏ body token ကုန်ကျသည် | skill body tokens | argument binding မစစ်လျှင် မှားသော tool ခေါ်ယူမှု ဖြစ်သည် |
| Stateless MCP | throughput | connection affinity ကို ဖယ်ရှားသည် | workers per request | affinity ရှိလျှင် horizontal routing ခက်သည် |
| Structured Output | cost per task | schema က prompt token အပို လိုအပ်သည် | schema tokens, retries | parse မှားလျှင် application ကျိုးပျက်သည် |
| Swarm | cost per task | agent အချင်းချင်း မက်ဆေ့ချ် ဖလှယ်မှု ကုန်ကျသည် | messages per task | topology နှင့် termination မသတ်မှတ်လျှင် ခန့်မှန်းခြင်း မပြုနိုင် |
| Termination Condition | cost per task | budget ကုန်ဆုံးသည့်နေရာတွင် ရပ်စေသည် | max steps, cost ceiling | condition မရှိလျှင် loop နှင့် cost ပေါက်ကြွ |
| Tool Contract | cost per task | validation သည် rejected call အပေါ် token ကုန်ကျသည် | rejected calls per task | contract မရှိလျှင် error ကို စနစ်အဆင့်တွင် မဖော်ထုတ်နိုင် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု ခြောက်ခုဖြင့် စုစည်းထားသည် — (က) harness နှင့် loop၊ (ခ) state၊ memory နှင့် ခံတည်မှု၊ (ဂ) tool နယ်နိမိတ်၊ (ဃ) လုံခြုံရေး နှင့် ထိန်းချုပ်မှု၊ (င) skill အစုအဝေး၊ (စ) multi-agent နှင့် လွှဲအပ်မှု။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — harness နှင့် loop

#### Agent

Agent သည် ပန်းတိုင်တစ်ခုဆီသို့ လုပ်ဆောင်ချက်များ ရွေးချယ်ပြီး tool သို့မဟုတ် environment ၏ ရလဒ်များကို လေ့လာကာ orchestration policy တစ်ခုအောက်တွင် ဆက်လက်လုပ်ဆောင်သည့် software စနစ် ဖြစ်သည်။ ထို့ကြောင့် ၎င်း၏ အခြေခံ အရင်းအမြစ်သည် step အရေအတွက် ဖြစ်သည်၊ ဥပမာ (က) တွင် step ၈ ခုက task တစ်ခုကို ကိုယ်စားပြုပြီး prompt token 53,448 ခု ကုန်ကျသည်။ step တိုင်းသည် အပို latency နှင့် အပို prompt token ကို ဆိုလိုသောကြောင့် step ကန့်သတ်ချက်သည် ကုန်ကျစရိတ် ကန့်သတ်ချက် ဖြစ်လာသည်။ production တွင် agent တစ်ခုကို မော်ဒယ် တစ်ခုအဖြစ် မတိုင်းရ၊ စနစ် တစ်ခုအဖြစ် တိုင်းရမည်။

#### Agent Harness

Agent Harness သည် context စုစည်းခြင်း၊ tool ဖော်ထုတ်ခြင်း၊ state စီမံခြင်း၊ ကန့်သတ်ချက် ချမှတ်ခြင်း၊ trace မှတ်တမ်းတင်ခြင်းနှင့် ဆက်လုပ်ခြင်း၊ ပြန်လည်ကြိုးစားခြင်း၊ မေးမြန်းခြင်း သို့မဟုတ် ရပ်တန့်ခြင်းတို့ကို ဆုံးဖြတ်သည့် runtime ဖြစ်သည်။ ၎င်းသည် step တိုင်း၏ prompt token အရေအတွက်ကို ဆုံးဖြတ်သောကြောင့် cost per task ကို တိုက်ရိုက် ရွေ့လျားစေသည်၊ ဥပမာ (ခ) တွင် context စုစည်းမှုတွင် prefix 4,000 token ပါဝင်ခြင်းသည် task တစ်ခုလျှင် USD 0.178500 ဖြစ်စေသည်။ harness တစ်ခုတည်းကိုသာ ပြောင်းလဲခြင်းဖြင့် ကုန်ကျစရိတ် ကြီးစွာ ကွာခြားနိုင်သည်။

#### Orchestration

Orchestration သည် မော်ဒယ် နှင့် tool အဆင့်များအကြား အစဉ်လိုက်ခြင်း၊ အခန်းကိုင်းခွဲခြင်း၊ လွှဲအပ်ခြင်း၊ ပြန်လည်ကြိုးစားခြင်း၊ ရပ်တန့်ခြင်း နှင့် အဆုံးသတ်ခြင်းတို့ကို ပြုလုပ်သည့် control logic ဖြစ်သည်။ retry တစ်ကြိမ်တိုင်းသည် မော်ဒယ် ခေါ်ယူမှု တစ်ကြိမ် ဖြစ်သောကြောင့် retry policy သည် cost per task ၏ အဓိက အချက် ဖြစ်သည်။ ဥပမာ (က) တွင် step တိုင်း၏ prompt ကို ပြန်လည် ပေးပို့ရသောကြောင့် retry တစ်ခုသည် prompt တစ်ခုလုံး၏ token ကို ထပ်ကုန်သည်။ production တွင် transition တိုင်းကို persist လုပ်ခြင်းနှင့် retry အရေအတွက် ကန့်သတ်ခြင်းသည် မရှိမဖြစ် ဖြစ်သည်။

#### Planning

Planning သည် လက်ရှိ state မှ ပန်းတိုင်ဆီသို့ ရောက်ရန် လုပ်ဆောင်ချက်များ၏ အစဉ်နှင့် မှီခိုမှုများကို တည်ဆောက်ခြင်း သို့မဟုတ် ပြန်လည်ပြင်ဆင်ခြင်း ဖြစ်သည်။ အစီအစဉ် တစ်ခုသည် plan token အပို ကုန်ကျသော်လည်း မှားသော step များကို လျှော့ချသောကြောင့် စုစုပေါင်း step အရေအတွက်ကို ကျဆင်းစေနိုင်သည်။ အစီအစဉ်တွင် မှီခိုမှု အစဉ် မှန်ကန်ခြင်းသည် ပြန်လည် မဖျက်နိုင်သည့် လုပ်ဆောင်ချက် မစတင်မီ စစ်ဆေးရမည့် အချက် ဖြစ်သည်။ production တွင် အစီအစဉ်တိုင်းကို ရရှိနိုင်သည့် tool နှင့် permission နှင့် ကိုက်ညီမှု စစ်ဆေးရမည်။

#### ReAct

ReAct သည် နောက် အဆင့် မဆုံးဖြတ်မီ ကျိုးကြောင်းဆင်ခြင်မှု၊ တိကျသည့် လုပ်ဆောင်ချက် တစ်ခုနှင့် environment မှ ပြန်လည်ပေးအပ်သည့် observation တို့ကို တစ်လှည့်စီ ရောနှောသည့် ပုံစံ ဖြစ်သည်။ observation တိုင်းသည် context ထဲ ဝင်လာသော token ဖြစ်သောကြောင့် turn တိုင်း၏ context အရှည်ကို တိုးစေသည်၊ ဥပမာ (က) တွင် tool result 900 token ကို အပြည့် ထည့်လျှင် turn တိုင်း token 1,060 တိုးပြီး KV 530.0 MiB ကုန်သည်။ အနှစ်ချုပ် (digest) 180 token ဖြင့် အစားထိုးလျှင် တိုးမှုသည် 340 token သို့ ကျဆင်းသည်။ production တွင် loop ကန့်သတ်ချက်နှင့် observation အရှည် ကန့်သတ်ချက်ကို တွဲဖက် သတ်မှတ်ရမည်။

#### Termination Condition

Termination Condition သည် agent run တစ်ခုကို အောင်မြင်သည့်အခါ၊ ကျရှုံးသည့်အခါ၊ budget ကုန်ဆုံးသည့်အခါ သို့မဟုတ် escalation လိုအပ်သည့်အခါ ရပ်စေသည့် တိကျပြတ်သားသည့် စည်းမျဉ်း ဖြစ်သည်။ ၎င်းသည် ကုန်ကျစရိတ်၏ အထက်ကန့်သတ်ချက် ဖြစ်သည်၊ ဥပမာ (က) တွင် step budget ၈ ခုနှင့် cost budget USD 0.50 ကို တွဲဖက် သတ်မှတ်ထားသည်။ ကန့်သတ်ချက် မရှိလျှင် context နှင့် cost နှစ်ခုလုံး အဆက်မပြတ် တိုးလာသည်၊ `lab_agent_loop.py --sweep` က step ၃၂ ခုတွင် cost budget က အရင် ရပ်စေသည်ကို ပြသည်။ production တွင် အောင်မြင်မှု အထောက်အထား၊ အများဆုံး အဆင့်၊ ကုန်ကျစရိတ် ကန့်သတ်ချက်နှင့် escalation အခြေအနေများကို loop မစတင်မီ သတ်မှတ်ရမည်။

### မိသားစု (ခ) — state၊ memory နှင့် ခံတည်မှု

#### Agent State

Agent State သည် agent သည် အဆင့်များအကြား သယ်ဆောင်သည့် တိကျပြတ်သားသည့် data ဖြစ်သည် — လက်ရှိ ရည်မှန်းချက်၊ ပြီးစီးပြီးသား လုပ်ဆောင်ချက်များ၊ tool ရလဒ်များ၊ ကျန်ရှိသည့် မေးခွန်းများ၊ budget နှင့် အတည်ပြုချက်များ ဖြစ်သည်။ state ကို သီးသန့် သိမ်းဆည်းထားလျှင် transcript အပြည့်အစုံကို prompt ထဲ ထည့်ရန် မလိုသောကြောင့် token ချွေတာသည်။ production တွင် typed object အဖြစ် သိမ်းဆည်းထားသည့် state သည် process ပျက်ကျမှုကို ကျော်လွန်၍ task ကို ပြန်လည်စတင်နိုင်စေသည်။

#### Agent Memory

Agent Memory သည် မော်ဒယ်၏ အပြင်ဘက်တွင် သိမ်းဆည်းထားပြီး နောက်ပိုင်း agent အဆင့်များတွင် အသုံးပြုရန် ရွေးချယ်ထားသည့် အချက်အလက်များ ဖြစ်သည် — ယခင်ဆုံးဖြတ်ချက်များ၊ အသုံးပြုသူ၏ နှစ်သက်မှုများ၊ task episode များ ဖြစ်သည်။ ၎င်းသည် context window တစ်ခုထက် ကျော်လွန်၍ ဆက်လက်တည်ရှိမှု ပေးသည့်အတွက် context မပြည့်စေရန် ထိန်းပေးသည်။ production တွင် မှတ်ဉာဏ်ကို ရွေးချယ်၍ လိုအပ်သည့်အခါမှ ပြန်ရယူရမည်၊ မဟုတ်လျှင် prompt token ကို မလိုအပ်ဘဲ တိုးစေသည်။

#### Checkpoint

Checkpoint သည် သိရှိထားပြီးသည့် နယ်နိမိတ် တစ်ခုမှ ပြန်လည်စတင်ရန် အသုံးပြုသည့် တည်မြဲသည့် snapshot တစ်ခု ဖြစ်သည်။ workflow တွင် operational state နှင့် artifact ရည်ညွှန်းချက်များကို၊ မော်ဒယ် training တွင် parameter၊ optimizer state နှင့် data position တို့ကို သိမ်းဆည်းသည်။ ချွေတာသည့် ကိန်းသည် ပြန်လည်လုပ်ရမည့့် step ၏ အချိန်နှင့် token ဖြစ်သည်၊ ဥပမာ (က) တွင် step တစ်ခုလျှင် prompt token ခန့်မှန်းခြေ ၇,၀၀၀ ခန့် ကုန်သောကြောင့် step ၅ ခုကို ပြန်လုပ်ခြင်းသည် prompt token ၃၅,၀၀၀ ခန့် ဆုံးရှုံးမှု ဖြစ်သည်။ production တွင် အတည်ပြုပြီးသည့် အဆင့် တစ်ခုပြီးတိုင်း checkpoint သိမ်းရမည်။

#### Durable Execution

Durable Execution သည် workflow ၏ state နှင့် ပြီးစီးပြီးသား အဆင့်များကို process ပျက်ကျခြင်း၊ ပြန်လည်စတင်ခြင်း သို့မဟုတ် ရှည်ကြာသည့် စောင့်ဆိုင်းမှုများ ကျော်လွန်၍ တည်ရှိနေစေသည်။ transition တိုင်းကို persist လုပ်ခြင်းသည် write အပို ကုန်ကျသော်လည်း အတည်ပြုပြီးသား ဘေးထွက်ဆိုးကျိုးကို ပြန်လည် မလုပ်ခြင်းဖြင့် ကုန်ကျစရိတ်ကို ပို၍ ချွေတာသည်။ ဤအလွှာသည် ဘေးထွက်ဆိုးကျိုးများအတွက် idempotency နှင့် compensation စည်းမျဉ်းများကို အစားမထိုးနိုင်ပါ။ production တွင် workflow transition တိုင်း persist လုပ်ခြင်းနှင့် ပြင်ပ write များအတွက် idempotency key အသုံးပြုခြင်းသည် အခြေခံ လိုအပ်ချက် ဖြစ်သည်။

#### Compensating Action

Compensating Action သည် မူရင်း လုပ်ဆောင်ချက်ကို atomic အနေဖြင့် ပြန်လည် ဖျက်သိမ်းခြင်း မပြုနိုင်သည့်အခါ ပြီးမြောက်သွားသည့် ဘေးထွက်ဆိုးကျိုးကို အဓိပ္ပာယ်အားဖြင့် ဆန့်ကျင်ဖျက်ပစ်သည့် လုပ်ဆောင်ချက် တစ်ခု ဖြစ်သည်။ ၎င်းသည် လုပ်ငန်း လုပ်ဆောင်ချက် အသစ်တစ်ခု ဖြစ်သောကြောင့် tool call အပို ကုန်ကျပြီး ကိုယ်တိုင် ချို့ယွင်းနိုင်သည်။ အဆင့်များစွာပါသည့် agent workflow များသည် database နှင့် ပြင်ပ service များကို ဖြတ်ကျော်သောကြောင့် transaction တစ်ခုတည်းဖြင့် ပြန်လည် ဖျက်သိမ်းခြင်း မပြုနိုင်ပါ။ production တွင် compensation တိုင်းကို ခြေရာခံခြင်း၊ monitoring ပြုလုပ်ခြင်းနှင့် escalation လမ်းကြောင်း ထားရှိခြင်း လိုအပ်သည်။

### မိသားစု (ဂ) — tool နယ်နိမိတ်

#### Tool Contract

Tool Contract သည် tool နယ်နိမိတ် တစ်ခုအတွက် ပြည့်စုံသည့် သဘောတူညီချက် ဖြစ်သည် — ရည်ရွယ်ချက်၊ typed input များ၊ output များ၊ validation၊ permission များ၊ ဘေးထွက်ဆိုးကျိုးများ၊ အမှားများ၊ timeout များ၊ idempotency နှင့် ခေါ်သူထံ ပြန်လည်ပေးအပ်သည့် အထောက်အထား တို့ ဖြစ်သည်။ schema တစ်ခုသည် field များကို ဖော်ပြရုံသာ ဖြစ်ပြီး contract တစ်ခုသည် မည်သည့်အခါ လုံခြုံသည်ကို ဆုံးဖြတ်သည်။ production တွင် contract မရှိလျှင် malformed call သည် လုပ်ဆောင်မှု အလွှာသို့ ရောက်သည်၊ `lab_tool_schema.py` သည် ဤကဲ့သို့ call ငါးမျိုးကို run မတိုင်မီ ငြင်းပယ်သည်ကို ပြသည်။

#### Function Calling

Function Calling သည် မော်ဒယ်တစ်ခုသည် tool တစ်ခုကို အမည်တပ်ပြီး ၎င်း၏ argument များ ပါဝင်သည့် ဖွဲ့စည်းထားသည့် တောင်းဆိုမှုကို ထုတ်လွှတ်သည့် provider သို့မဟုတ် application interface တစ်ခု ဖြစ်သည်။ application code သည် တောင်းဆိုမှုကို validate လုပ်ပြီး လုပ်ဆောင်ချက်ကို ဆောင်ရွက်ကာ ရလဒ်ကို နောက် မော်ဒယ် အဆင့်တစ်ခုအတွက် ပြန်လည်ပေးအပ်နိုင်သည်။ ဤဆက်သွယ်မှု တိုင်းသည် prompt token နှင့် output token ကို ထပ်တိုးစေသည်၊ ဥပမာ (က) တွင် tool result 900 token သည် တစ်ကြိမ် ကုန်သောအခါ KV cache 450.0 MiB တိုးစေသည်။ production တွင် မော်ဒယ်၏ တောင်းဆိုမှုကို မည်သို့ လုပ်ဆောင်မည်ကို ယုံကြည်စိတ်ချရသည့့် code က ဆုံးဖြတ်ရမည်။

#### Structured Output

Structured Output သည် မော်ဒယ် ရလဒ်ကို စက်ဖတ်နိုင်သည့် schema တစ်ခုနှင့် ကိုက်ညီအောင် ကန့်သတ်ခြင်း သို့မဟုတ် validate လုပ်ခြင်း ဖြစ်သည်။ ၎င်းသည် format မရှင်းလင်းမှုကို လျှော့ချပြီး field အဆင့် validation နှင့် ပြန်လည်ကြိုးစားမှုကို ဖြစ်နိုင်စေသည်၊ သို့သော် schema ကိုယ်တိုင်သည် prompt token အပို လိုအပ်သည်။ schema နှင့် ကိုက်ညီသည့် ရလဒ်တွင် မှားယွင်းသည့် တန်ဖိုးများ ရှိနိုင်ဆဲ ဖြစ်သောကြောင့် ၎င်းသည် အချက်အလက် မှန်ကန်မှု စစ်ဆေးခြင်း မဟုတ်ပါ။ production တွင် schema မကိုက်ညီသည့် တုံ့ပြန်မှု တိုင်းကို ငြင်းပယ်ရမည်။

#### MCP (Model Context Protocol)

MCP သည် host တစ်ခုသည် tool များ၊ resource များ၊ prompt များနှင့် extension များကို ဖော်ထုတ်သည့် server များထံ ချိတ်ဆက်ရန် အသုံးပြုသည့် ဖွင့်ထားသည့် JSON-RPC protocol တစ်ခု ဖြစ်သည်။ revision 2026-07-28 တွင် request တိုင်းသည် initialization handshake ကို မမှီခိုဘဲ ၎င်း၏ protocol version နှင့် client capabilities များကို သယ်ဆောင်သည်။ discovery ကို စံပြုခြင်းသည် tool ဖော်ပြချက်၏ token ကို ခန့်မှန်းနိုင်စေသည်၊ ဥပမာ (ခ) တွင် prefix 4,000 token ၏ တစ်စိတ်တစ်ပိုင်း ဖြစ်သည်။ production တွင် မည်သည့် tool ကို ခေါ်ရန် လုံခြုံသည်ကို MCP က ဆုံးဖြတ်ပေးသည် မဟုတ်ပါ။

#### Stateless MCP

Stateless MCP သည် request တိုင်းသည် `params._meta` တွင် protocol version နှင့် client capabilities ကို သယ်ဆောင်ပြီး ရလဒ်များသည် တိကျပြတ်သားသည့် `resultType` ကို သယ်ဆောင်သည့် MCP 2026-07-28 ပုံစံ ဖြစ်သည်။ initialization handshake၊ connection သို့မဟုတ် `Mcp-Session-Id` ဖြင့် key လုပ်ထားသည့် protocol state မရှိပါ။ ဤအချက်သည် worker တိုင်း request တစ်ခုကို လွတ်လပ်စွာ လုပ်ဆောင်နိုင်စေသောကြောင့် horizontal scale လုပ်ခြင်းကို ရိုးရှင်းစေသည်။ production တွင် ဤပုံစံသည် application state၊ transport connection နှင့် တိကျပြတ်သားသည့် handle များကို ဖယ်ရှားခြင်း မပြုပါ။

#### Multi Round-Trip Request (MRTR)

MRTR သည် လုပ်ဆောင်မှု တစ်ခုသည် `resultType: input_required` ကို `inputRequests` နှင့်တကွ ပြန်လည်ပေးအပ်ပြီးနောက် client သည် မူရင်း method ကို `inputResponses` နှင့် ပြန်လည်ပေးအပ်ထားသည့် `requestState` အတိအက်ဖြင့် ပြန်လည်ကြိုးစားသည့် တောင်းဆိုမှု ပုံစံ ဖြစ်သည်။ round trip တစ်ကြိမ် အပိုဖြစ်သောကြောင့် step latency တိုးပြီး prompt token ကို ထပ်ကုန်စေသည်။ stateless server သည် server-initiated exchange သို့မဟုတ် protocol session state မလိုဘဲ အသုံးပြုသူ၊ မော်ဒယ် သို့မဟုတ် root input ကို တောင်းဆိုနိုင်သည်။ production တွင် `requestState` ကို မယုံကြည်ရသည့် data အဖြစ် သတ်မှတ်ရမည်။

### မိသားစု (ဃ) — လုံခြုံရေး နှင့် ထိန်းချုပ်မှု

#### Approval Gate

Approval Gate သည် အကျိုးဆက် ကြီးမားသည့် လုပ်ဆောင်ချက် တစ်ခုကို အခွင့်အာဏာရှိသူ တစ်ဦး သို့မဟုတ် policy တစ်ခုက ခွင့်ပြုချက် မပေးမချင်း ပိတ်ဆို့ထားသည့် control point တစ်ခု ဖြစ်သည်။ ပြန်လည် ဖျက်သိမ်းနိုင်သည့် လုပ်ငန်းများအတွက် automation ကို ထိန်းသိမ်းထားရင်း မသေချာသည့် ဆုံးဖြတ်ချက်များ၏ သက်ရောက်နိုင်သည့် အတိုင်းအတာကို ကန့်သတ်ပေးသည်။ ၎င်း၏ ကုန်ကျစရိတ်သည် စောင့်ဆိုင်းချိန် ဖြစ်သည်၊ ထို့ကြောင့် gate အရေအတွက်ကို သတိထား သတ်မှတ်ရမည်။ production တွင် production လုပ်ဆောင်မှု တိုင်းအတွက် owner တစ်ဦး၏ အတည်ပြုချက် လိုအပ်ရမည်။

#### Human-in-the-Loop (HITL)

Human-in-the-Loop (HITL) သည် AI ဖြင့် မောင်းနှင်သည့် လုပ်ငန်းစဉ် တစ်ခုအတွင်း သတ်မှတ်ထားသည့် အချက်များတွင် လူတစ်ဦးက ဆုံးဖြတ်ချက်၊ အမှားပြင်ဆင်မှု၊ အတည်ပြုချက် သို့မဟုတ် escalation တို့ကို ပေးအပ်သည့် workflow တည်ဆောက်ပုံ တစ်ခု ဖြစ်သည်။ လူ၏ ပါဝင်မှုသည် သက်ရောက်မှု ကြီးမားသည့်၊ မရှင်းလင်းသည့် သို့မဟုတ် ပြန်လည်ဖျက်သိမ်း၍ မရနိုင်သည့် နယ်နိမိတ်များတွင် အသုံးဝင်ဆုံး ဖြစ်သည်။ ဤအလွှာသည် throughput ကို လူ၏ အရှိန်ဖြင့် ကန့်သတ်သောကြောင့် စစ်ဆေးသူ အရေအတွက်ကို capacity plan တွင် ထည့်ရမည်။ HITL သည် စနစ်တစ်ခုကို အလိုအလျောက် လုံခြုံစေသည် မဟုတ်ပါ။

#### Sandbox

Sandbox သည် agent တစ်ခု၏ file များ၊ process များ၊ network ပန်းတိုင်များ၊ credential များနှင့် host အရင်းအမြစ်များသို့ ဝင်ရောက်နိုင်မှုကို ကန့်သတ်ထားသည့် သီးခြားခွဲထုတ်ထားသည့် လုပ်ဆောင်မှု ပတ်ဝန်းကျင် တစ်ခု ဖြစ်သည်။ ထုတ်လုပ်ထားသည့့် code နှင့် tool call များသည် မှားယွင်းနိုင် သို့မဟုတ် အန္တရာယ်ရှိနိုင်သောကြောင့် isolation သည် သက်ရောက်နိုင်သည့် အတိုင်းအတာကို ကန့်သတ်ပြီး စွန့်ပစ်နိုင်သည့် verification ကို လက်တွေ့ကျစေသည်။ ၎င်း၏ ကုန်ကျစရိတ်သည် container တစ်ခုစီ၏ start-up အချိန်နှင့် resource ဖြစ်သည်။ production တွင် read-only base၊ ကန့်သတ်ထားသည့် writable workspace နှင့် မပါဝင်သည့့် production secret တို့ဖြင့် run ရမည်။

### မိသားစု (င) — skill အစုအဝေး

#### Agent Skill

Agent Skill သည် entry point သည် `SKILL.md` ဖြစ်သည့်၊ ရှာဖွေတွေ့ရှိနိုင်သည့် လုပ်ငန်းစဉ် ညွှန်ကြားချက် directory တစ်ခု ဖြစ်ပြီး ကိုက်ညီသည့် runtime တစ်ခုက အဆင့်လိုက် load လုပ်နိုင်သည့် ရွေးချယ်နိုင်သည့် reference များ၊ script များနှင့် asset များ ပါဝင်နိုင်သည်။ progressive disclosure ကြောင့် skill body ၏ token သည် လိုအပ်သည့်အခါမှ prompt token အဖြစ် ရောက်လာသည်။ ထို့ကြောင့် catalog ၏ အရွယ်အစားနှင့် body ၏ အရွယ်အစားကို ခွဲခြား တိုင်းရမည်။ production တွင် skill activate လုပ်ခြင်းသည် context ကို ပေးအပ်ရုံသာ ဖြစ်ပြီး permission သို့မဟုတ် sandbox ကို မဖန်တီးပါ။

#### Skill Bundle

Skill Bundle သည် `SKILL.md` နှင့် workflow လိုအပ်သည့် reference၊ script၊ asset၊ fixture သို့မဟုတ် အဖော် file အားလုံး အပါအဝင် ပြည့်စုံသည့် တပ်ဆင်နိုင်သည့် skill directory တစ်ခု ဖြစ်သည်။ entry file ကိုသာ ကူးယူခြင်းသည် ပျောက်ဆုံးနေသည့် အရင်းအမြစ်များကို ညွှန်သည့် သို့မဟုတ် အဆုံးအဖြတ်ပေးသည့် code ဆုံးရှုံးသည့် ညွှန်ကြားချက်များကို ချန်ထားနိုင်သည်။ တပ်ဆင်မှု၏ ကုန်ကျစရိတ်သည် bundle ၏ byte ပမာဏနှင့် hash မှတ်တမ်းတင်ခြင်း ဖြစ်သည်။ production တွင် bundle ကို ယူနစ်တစ်ခုအဖြစ် တပ်ဆင်ပြီး source revision ကို မှတ်တမ်းတင်ရမည်။

#### Skill Catalog

Skill Catalog သည် အရည်အချင်းပြည့်မီသည့် skill များ၏ မော်ဒယ် မြင်နိုင်သည့် ကျစ်လျစ်သည့် စာရင်း ဖြစ်ပြီး များသောအားဖြင့် name၊ description နှင့် source identifier ကဲ့သို့သော routing metadata များ ပါဝင်သည်။ catalog entry တိုင်းသည် prompt ထဲ တွင် တည်ရှိနေသော token ဖြစ်သောကြောင့် entry အရေအတွက်သည် system prompt ၏ အရွယ်အစားကို ဆုံးဖြတ်သည်၊ ဥပမာ (ခ) တွင် prefix 4,000 token ၏ တစ်စိတ်တစ်ပိုင်း ဖြစ်သည်။ production တွင် catalog ကို validate လုပ်ခြင်း၊ duplicate-name policy သတ်မှတ်ခြင်းနှင့် serialized catalog budget တိုင်းတာခြင်း လိုအပ်သည်။

#### Skill Discovery

Skill Discovery သည် သတ်မှတ်ထားသည့် root များကို ရှာဖွေခြင်း၊ skill directory များ ဖော်ထုတ်ခြင်း၊ package contract validate လုပ်ခြင်း၊ scope နှင့် provenance တွဲဖက်ခြင်း၊ collision ဖြေရှင်းခြင်းနှင့် catalog entry များ ထုတ်ဝေခြင်းတို့ကို ပြုလုပ်သည့် runtime pipeline တစ်ခု ဖြစ်သည်။ ၎င်းသည် စတင်ချိန်တွင် အချိန်ကုန်သော်လညး် routing မစတင်မီ မှားယွင်းသည့် package များကို ရောဂါရှာဖွေနိုင်စေသည်။ production တွင် ရှာဖွေမည့် scope၊ symlink အပြုအမူနှင့် resource escape ကို ငြင်းပယ်သည့် စည်းမျဉ်းကို ကြေညာရမည်။

#### Skill Invocation

Skill Invocation သည် အရည်အချင်းပြည့်မီသည့် လူတစ်ဦး၊ မော်ဒယ်၊ application တစ်ခု သို့မဟုတ် အခြား skill တစ်ခုက skill တစ်ခုကို ရွေးချယ်ပြီး ၎င်း၏ ညွှန်ကြားချက်များကို လုပ်ငန်း context ထဲ ဝင်ရောက်စေသည့် runtime မှ ဖြတ်ကူးစေသည့် လုပ်ငန်းစဉ် တစ်ခု ဖြစ်သည်။ တိကျပြတ်သားသည့် အသုံးပြုသူ ဝင်ရောက်ခွင့်၊ မော်ဒယ် routing၊ activation၊ argument binding၊ tool permission နှင့် execution တို့သည် မတူညီသည့် ချို့ယွင်းမှု ပုံစံများရှိသည့် သီးခြား ဆုံးဖြတ်ချက်များ ဖြစ်သည်။ production တွင် ရွေးချယ်ထားသည့် package အမှတ်အသားကို မှတ်တမ်းတင်ရမည်။

### မိသားစု (စ) — multi-agent နှင့် လွှဲအပ်မှု

#### Delegation

Delegation သည် ကန့်သတ်ထားသည့် subtask တစ်ခုကို အခြား လူတစ်ဦး သို့မဟုတ် agent တစ်ခုထံ လိုအပ်သည့် context၊ အခွင့်အာဏာ၊ output contract နှင့် ပြန်လည်ပေးအပ်ရမည့် အခြေအနေများနှင့်တကွ လွှဲအပ်ခြင်း ဖြစ်သည်။ subtask များကို တစ်ပြိုင်နက် run စေခြင်းဖြင့် throughput ကို တိုးစေသော်လည်း subtask တိုင်း၏ prompt token ကုန်ကျစရိတ် သည် သီးခြားစီ ပေါ်လာသည်။ တိကျပြတ်သားသည့် delegation သည် ပိုင်ဆိုင်မှုနှင့် scope ကို မဆုံးရှုံးဘဲ အထူးပြုလုပ်ခြင်းကို ဖြစ်နိုင်စေသည်။ production တွင် လက်ခံသူအား scope contract နှင့် သတ်မှတ်ထားသည့် handoff မပါဘဲ မလွှဲအပ်ရ။

#### Swarm

Swarm သည် ဒေသခံ agent ဆုံးဖြတ်ချက်များနှင့် မက်ဆေ့ချ် ဖလှယ်မှုသည် စနစ်အဆင့် အပြုအမူကို ဖြစ်ပေါ်စေသည့် ချိတ်ဆက်မှု လျော့ရဲရဲ multi-agent ပုံစံ တစ်ခု ဖြစ်သည်။ agent အရေအတွက် တိုးလာသည်နှင့်အမျှ မက်ဆေ့ချ် အရေအတွက်နှင့် စုစုပေါင်း prompt token သည် အလျင်အမြန် တိုးလာသည်။ topology၊ state ပိုင်ဆိုင်မှုနှင့် အဆုံးသတ်ခြင်း စည်းမျဉ်းများကို မသတ်မှတ်ထားပါက အပြုအမူကို ခန့်မှန်းနိုင်ခြင်း မရှိပါ။ production တွင် ဤသုံးချက်ကို အတိအကျ ဖော်ပြရမည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။

### (က) context နှင့် KV cache ကြီးထွားမှု — turn ၁၂ ခု၊ tool-result အပြည့် နှင့် digest

ဖော်မြူလာ — `KV bytes = 2 (K နှင့် V) × layers × heads × head_dim × sequence_length × bytes_per_element`။ ယူဆချက် — layers 32၊ heads 32၊ head_dim 128၊ fp16 (2 byte/element)၊ base prompt 1,000 token၊ turn တိုင်း assistant 120 + tool call 40 token၊ tool result 900 token၊ digest 180 token။

```text
$ python3 guides/06_agents_and_tools/scripts/ex_a_context_kv.py
reference model: layers=32 heads=32 head_dim=128 fp16=2 B -> 524288 B/token = 0.500 MiB/token
turns=12  base prompt=1000  assistant=120  tool call=40  tool result=900  digest=180

turn     raw tokens  summ tokens   raw KV MiB  summ KV MiB    ratio
-------------------------------------------------------------------
1              2060         2060       1030.0       1030.0    1.000
2              3120         2400       1560.0       1200.0    1.300
3              4180         2740       2090.0       1370.0    1.526
4              5240         3080       2620.0       1540.0    1.701
5              6300         3420       3150.0       1710.0    1.842
6              7360         3760       3680.0       1880.0    1.957
7              8420         4100       4210.0       2050.0    2.054
8              9480         4440       4740.0       2220.0    2.135
9             10540         4780       5270.0       2390.0    2.205
10            11600         5120       5800.0       2560.0    2.266
11            12660         5460       6330.0       2730.0    2.319
12            13720         5800       6860.0       2900.0    2.366

final turn 12: raw 13720 tokens = 6.699 GiB KV | summarised 5800 tokens = 2.832 GiB KV
KV saved at turn 12: 3960.0 MiB (3.867 GiB), ratio raw/summarised = 2.366
growth per turn: raw +1060 tokens (+530.0 MiB), summarised +340 tokens (+170.0 MiB)
summarisation work assumed: 11 calls x (900 read + 180 write) = 11880 extra tokens
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ tool result ကို အပြည့် ထည့်လျှင် turn တိုင်း token 1,060 တိုးပြီး KV 530.0 MiB ကုန်သည်၊ digest ဖြင့် အစားထိုးလျှင် တိုးမှုသည် token 340 နှင့် KV 170.0 MiB သို့ ကျဆင်းသည်။ သို့သော် digest သည် အခမဲ့ မဟုတ်ပါ၊ script က ပြသည့်အတိုင်း summarisation ၁၁ ကြိမ်အတွက် token 11,880 အပို ကုန်သည်၊ ထို့ကြောင့် ၎င်းသည် ချွေတာမှုနှင့် အချက်အလက် ဆုံးရှုံးမှုအကြား လဲလှယ်မှု ဖြစ်သည်။

### (ခ) task တစ်ခု၏ cost — step ၁၀ ခု၊ prefix caching မပါ နှင့် ပါ

ယူဆချက် — step ၁၀ ခု၊ step တိုင်း ပေးပို့သည့် တူညီသည့် prefix 4,000 token (system prompt နှင့် tool schema)၊ step တိုင်း conversation သို့ 300 token တိုးသည်၊ step တိုင်း output 120 token၊ input USD 3.00/Mtok နှင့် output USD 15.00/Mtok၊ cache write 1.25x (ပထမ ရေးသွင်းမှု) နှင့် cache read 0.25x (နောက်ပိုင်း turn များ)။

```text
$ python3 guides/06_agents_and_tools/scripts/ex_b_cost_per_task.py
task: 10 steps, shared prefix 4000 tokens, +300 tokens per step, 120 output tokens per step
assumed price: input 3.00 USD/Mtok, output 15.00 USD/Mtok, cache write 1.25x, cache read 0.25x

step      prompt plain step USD cached step USD    plain cum   cached cum
-------------------------------------------------------------------------
1           4000       0.013800       0.016800     0.013800     0.016800
2           4300       0.014700       0.005700     0.028500     0.022500
3           4600       0.015600       0.006600     0.044100     0.029100
4           4900       0.016500       0.007500     0.060600     0.036600
5           5200       0.017400       0.008400     0.078000     0.045000
6           5500       0.018300       0.009300     0.096300     0.054300
7           5800       0.019200       0.010200     0.115500     0.064500
8           6100       0.020100       0.011100     0.135600     0.075600
9           6400       0.021000       0.012000     0.156600     0.087600
10          6700       0.021900       0.012900     0.178500     0.100500

final step prompt 6700 tokens (4000 prefix + 2700 accumulated)
prompt tokens billed over the task: plain 53500, cached-equivalent 27500.0 (-48.60%)
cost per task: plain USD 0.178500, cached USD 0.100500, saved USD 0.078000 (43.70%)
if the prefix grows to 8000 tokens the saving per task becomes USD 0.156000
```

ဤဥပမာက ပြသည့် အဓိက အချက်မှာ prompt token သည် output token ထက် အဆများစွာ ပိုသောကြောင့် task ကုန်ကျစရိတ်ကို prompt ၏ token အရေအတွက်က ဆုံးဖြတ်ခြင်း ဖြစ်သည်။ တူညီသည့် prefix ကို ပြန်လည် အသုံးပြုလျှင် task တစ်ခုလျှင် USD 0.078000 (43.70%) ချွေတာသည်။

### (ဂ) concurrency နှင့် GPU memory — session အရေအတွက်၊ context အရှည်အလိုက်

ယူဆချက် — accelerator 80 GB၊ runtime အတွက် 16 GiB သီးသန့်၊ weight 14.0 GiB၊ KV 0.5 MiB/token၊ session တစ်ခုလျှင် overhead 0.25 GiB၊ step တစ်ခု ၁.၂ စက္ကန့်၊ task တစ်ခု step ၁၀ ခု။

```text
$ python3 guides/06_agents_and_tools/scripts/ex_c_concurrency.py
gpu 80 GB, reserved 16.0 GiB, weights 14.0 GiB -> usable 50.0 GiB
KV 0.50 MiB/token, per-session overhead 0.25 GiB, step 1.2 s, task 10 steps

context  sessions  per-session  requested GiB      fit    queue
---------------------------------------------------------------
4096            1        2.250           2.25        1        0
4096            8        2.250          18.00        8        0
4096           32        2.250          72.00       22       10
4096           64        2.250         144.00       22       42
8192            1        4.250           4.25        1        0
8192            8        4.250          34.00        8        0
8192           32        4.250         136.00       11       21
8192           64        4.250         272.00       11       53
32768           1       16.250          16.25        1        0
32768           8       16.250         130.00        3        5
32768          32       16.250         520.00        3       29
32768          64       16.250        1040.00        3       61

context   requested   served    queue   steps/min   tasks/min
-------------------------------------------------------------
4096              8        8        0      400.00       40.00
4096             32       22       10     1100.00      110.00
4096             64       22       42     1100.00      110.00
8192              8        8        0      400.00       40.00
8192             32       11       21      550.00       55.00
8192             64       11       53      550.00       55.00
32768             8        3        5      150.00       15.00
32768            32        3       29      150.00       15.00
32768            64        3       61      150.00       15.00

case 32768-token sessions: per-session 16.250 GiB -> 3 sessions fit, 61 of 64 wait
throughput at 1.2 s/step: 150.00 steps/min = 15.00 tasks/min (a 10-step task)
halving the context to 16384 tokens: per-session 8.250 GiB -> 6 sessions fit (2.00x)
memory per session at 32768 tokens is 98% KV cache and 2% overhead
```

ဤဥပမာက ပြသည့် အဓိက အချက်မှာ agent session တစ်ခုသည် task တစ်ခုလုံး အတွင်း context တစ်ခုလုံးကို ကိုင်ထားသောကြောင့် concurrency သည် KV cache ၏ လက်အောက်တွင် ရှိခြင်း ဖြစ်သည်။ 32,768-token session များတွင် session ၃ ခုသာ နေရာရပြီး throughput သည် steps/min 150.00 တွင် ပြည့်သွားသည်၊ session ထပ်တိုးခြင်းသည် queue ကိုသာ ရှည်စေသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Step budget နှင့် cost budget သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Termination Condition၊ Agent၊ Orchestration၊ Agent Harness။ သက်သေပြသည့် မက်ထရစ် — steps per task နှင့် USD per task။ ဥပမာ (ခ) က step ၁၀ ခုတွင် prompt token 53,500 ခု ကုန်သည်ဟု ပြသည်၊ `lab_agent_loop.py --sweep` က cost budget က အရင် ရပ်စေသည့် အခြေအနေကို ပြသည်။

**၂။ Context ကြီးထွားမှု ထိန်းချုပ်ခြင်း** — မှီခိုသည့် term များ — ReAct၊ Agent Memory၊ Agent State၊ Function Calling။ သက်သေပြသည့် မက်ထရစ် — turn တိုင်း တိုးသည့် token နှင့် KV MiB။ ဥပမာ (က) က turn တိုင်း token 1,060 (KV 530.0 MiB) မှ token 340 (KV 170.0 MiB) သို့ လျှော့ချနိုင်သည်ကို ပြသည်။

**၃။ Prompt prefix caching ဖွင့်ခြင်း** — မှီခိုသည့် term များ — Agent Harness၊ Tool Contract၊ MCP၊ Structured Output။ သက်သေပြသည့် မက်ထရစ် — cache hit rate နှင့် USD per task။ ဥပမာ (ခ) က USD 0.178500 မှ USD 0.100500 သို့ ကျဆင်းသည်ကို ပြသည်၊ prefix တိုးလျှင် ချွေတာမှုလည်း တိုးသည်။

**၄။ Concurrency နှင့် queue သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Agent State၊ Checkpoint၊ Sandbox၊ Delegation။ သက်သေပြသည့် မက်ထရစ် — sessions that fit၊ queue အရှည်နှင့် tasks/min။ ဥပမာ (ဂ) က session ၆၄ ခု တောင်းဆိုလျှင် session ၃ ခုသာ ဝန်ဆောင်နိုင်ပြီး ကျန် ၆၁ ခု စောင့်သည်ကို ပြသည်။

**၅။ Tool နယ်နိမိတ် စစ်ဆေးခြင်း** — မှီခိုသည့် term များ — Tool Contract၊ Structured Output၊ Function Calling၊ Approval Gate၊ Human-in-the-Loop (HITL)။ သက်သေပြသည့် မက်ထရစ် — rejected calls per task နှင့် approval အရေအတွက်။ `lab_tool_schema.py` က malformed call ငါးမျိုးကို run မတိုင်မီ ငြင်းပယ်သည်ကို ပြသည်။

**၆။ Skill catalog budget တိုင်းတာခြင်း** — မှီခိုသည့် term များ — Skill Catalog၊ Skill Discovery၊ Skill Invocation၊ Agent Skill၊ Skill Bundle။ သက်သေပြသည့် မက်ထရစ် — catalog token နှင့် discovery အချိန်။ `lab_tool_schema.py --sweep` က cached prefix ၏ ချွေတာမှုသည် turn အရေအတွက်နှင့်အတူ 75% ကန့်သတ်ချက်သို့ ချဉ်းကပ်သည်ကို ပြသည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/06_agents_and_tools/labs/lab_agent_loop.py`၊ `lab_tool_schema.py` နှင့် `lab_concurrency.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/06_agents_and_tools.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/06_agents_and_tools.json`။

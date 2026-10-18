# 06 — Agents & tools

ဤစာစုသည် AI Engineering Glossary ၏ နယ်ပယ် 06 — Agents & tools အတွက် ဖြစ်သည်။ Agent တစ်ခုသည် မော်ဒယ် တစ်ခုတည်း မဟုတ်ပါ။ ၎င်းသည် ပန်းတိုင်တစ်ခုဆီသို့ လုပ်ဆောင်ချက်များ ရွေးချယ်ပြီး tool သို့မဟုတ် environment ၏ ရလဒ်များကို လေ့လာကာ orchestration policy တစ်ခုအောက်တွင် ဆက်လက်လုပ်ဆောင်သည့် software စနစ် တစ်ခု ဖြစ်သည်။ ဤနယ်ပယ်တွင် ထို စနစ်ကို တည်ဆောက်ရန်၊ မောင်းနှင်ရန်၊ လုံခြုံစေရန်နှင့် စစ်ဆေးရန် လိုအပ်သည့် ဝေါဟာရ ၂၇ ခုကို စုစည်းထားသည်။

ဤ term များသည် တစ်ခုနှင့်တစ်ခု တွဲဖက်အသုံးပြုရန် ဖြစ်သည်။ Agent Harness နှင့် Agent State သည် agent တစ်ခု၏ လုပ်ငန်းလည်ပတ်မှုကို ထိန်းချုပ်သည်။ Tool Contract၊ Function Calling၊ Structured Output နှင့် MCP တို့သည် မော်ဒယ်နှင့် ပြင်ပလောကကြား နယ်နိမိတ်ကို သတ်မှတ်သည်။ Checkpoint၊ Durable Execution နှင့် Compensating Action တို့သည် ပျက်ကျမှုနှင့် ချို့ယွင်းမှုများကို ကျော်လွန်စေသည်။ Approval Gate၊ Human-in-the-Loop၊ Sandbox နှင့် Termination Condition တို့သည် လုံခြုံရေး နယ်နိမိတ်ကို ထိန်းသိမ်းသည်။ Agent Skill အစုအဝေး (Skill Bundle၊ Skill Catalog၊ Skill Discovery၊ Skill Invocation) သည် ပြန်လည်အသုံးပြုနိုင်သည့် လုပ်ငန်းစဉ် အသိပညာကို package လုပ်ပေးသည်။ ဤ term များကို သီးခြားစီ မဟုတ်ဘဲ စနစ် တစ်ခုအဖြစ် နားလည်မှသာ ယုံကြည်စိတ်ချရသည့် agent များ တည်ဆောက်နိုင်မည် ဖြစ်သည်။

Entry တစ်ခုကို ဖတ်သည့်အခါ မြန်မာ အမည်၊ ဆိုလိုသည့် အဓိပ္ပာယ်၊ အရေးပါသည့် အကြောင်းရင်း၊ မကြာခဏ ရောထွေးမှု၊ လက်တွေ့အသုံးချမှု၊ ဆက်စပ် term များနှင့် လေ့လာရန် လင့်တို့ကို အစဉ်လိုက် ဖတ်ရမည်။ English (source) field တွင် မူရင်း အင်္ဂလိပ် စာသားကို တိုက်ရိုက် ထည့်သွင်းထားသည်။ Technical term (agent loop၊ tool contract၊ MCP၊ harness၊ state machine၊ approval gate၊ sandbox စသည်) များကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိသည်။ source တွင် မပါသည့် field များ (ဥပမာ မကြာခဏ ရောထွေးမှု၊ လက်တွေ့၊ Learn it) ကို လုံးဝ ချန်လှပ်ထားသည်။


### Agent

**မြန်မာ:** Agent (ပန်းတိုင်ဆီသို့ လုပ်ဆောင်ချက်များ ရွေးချယ်၍ ဆောင်ရွက်သည့် စနစ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်တစ်ခုအား ပန်းတိုင်တစ်ခုဆီသို့ လုပ်ဆောင်ချက်များ ရွေးချယ်စေပြီး tool သို့မဟုတ် environment ၏ ရလဒ်များကို လေ့လာစေကာ orchestration policy တစ်ခုအောက်တွင် ဆက်လက်လုပ်ဆောင်စေသည့် software စနစ် ဖြစ်သည်။ Agent တစ်ခုသည် loop တစ်ခု၊ state machine တစ်ခု၊ workflow engine တစ်ခု သို့မဟုတ် လူ၏ အတည်ပြုချက်များကို အသုံးပြုနိုင်သည်။ မော်ဒယ်သည် အစိတ်အပိုင်း တစ်ခုသာ ဖြစ်ပြီး စနစ် တစ်ခုလုံး မဟုတ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** ယုံကြည်စိတ်ချရမှုသည် မော်ဒယ်ကို ဝန်းရံထားသည့် harness၊ tool contract များ၊ state၊ permission များနှင့် verification များမှ ရရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** Autonomy ဆိုသည်မှာ လွှဲအပ်ထားသည့် အခွင့်အာဏာ၏ အတိုင်းအတာ တစ်ခု ဖြစ်ပြီး agent တိုင်း၏ မဖြစ်မနေ လိုအပ်သည့် ဂုဏ်သတ္တိ မဟုတ်ပါ။
- **လက်တွေ့:** Coding agent တစ်ခုသည် repository context ကို ဖတ်ရှုပြီး patch တစ်ခု အဆိုပြုကာ sandbox အတွင်း test များ လုပ်ဆောင်ပြီးနောက် deployment မပြုမီ အတည်ပြုချက်အတွက် ရပ်တန့်သည်။
- **ဆက်စပ် term များ:** Agent Harness, Agent State, Tool Contract, Human-in-the-Loop (HITL)
- **Learn it:** [The Agent Loop](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/01-the-agent-loop/)
- **English (source):** A software system that lets a model select actions toward a goal, observe tool or environment results, and continue under an orchestration policy. An agent may use a loop, a state machine, a workflow engine, or human approvals. The model is one component, not the entire system. Reliability comes from the harness, tool contracts, state, permissions, and verification around the model.

### Agent Harness

**မြန်မာ:** Agent Harness (မော်ဒယ်ကို ဝန်းရံသည့် runtime)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** context များ စုစည်းပေးခြင်း၊ tool များ ဖော်ထုတ်ပေးခြင်း၊ state ကို စီမံခြင်း၊ ကန့်သတ်ချက်များ ချမှတ်ခြင်း၊ trace များ မှတ်တမ်းတင်ခြင်းနှင့် agent သည် ဆက်လက်လုပ်ဆောင်မည်၊ ပြန်လည်ကြိုးစားမည်၊ မေးမြန်းမည် သို့မဟုတ် ရပ်တန့်မည်ကို ဆုံးဖြတ်ပေးခြင်းတို့ကို ပြုလုပ်သည့် မော်ဒယ်ပတ်လည်ရှိ runtime ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မော်ဒယ် တူညီသည့် စနစ် နှစ်ခုသည် ၎င်းတို့၏ harness များက context၊ tool၊ feedback နှင့် လုံခြုံရေး နယ်နိမိတ်များကို မတူညီစွာ ပေးအပ်သောကြောင့် စွမ်းဆောင်ရည် အလွန်ကွာခြားနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Harness သည် prompt template ထက် ကျယ်ပြန့်ပြီး ပြီးပြည့်စုံသည့် product ထက် ကျဉ်းမြောင်းသည်။
- **လက်တွေ့:** သင့် harness သည် agent ကို tool call ငါးခုအထိသာ ကန့်သတ်နိုင်သည်၊ လက်ခံသည့် patch တစ်ခုစီပြီးနောက် checkpoint တစ်ခု သိမ်းဆည်းနိုင်သည်၊ ပြီးစီးမှု မတိုင်မီ အောင်မြင်သည့် test command တစ်ခု လိုအပ်နိုင်သည်။
- **ဆက်စပ် term များ:** Agent, Tool Contract, Agent State, Verification Gate, Sandbox
- **Learn it:** [Minimal Agent Workbench](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/32-minimal-agent-workbench/)
- **English (source):** The runtime around a model that assembles context, exposes tools, manages state, enforces limits, records traces, and decides when the agent should continue, retry, ask, or stop. Two systems using the same model can perform very differently because their harnesses provide different context, tools, feedback, and safety boundaries.

### Agent Memory

**မြန်မာ:** Agent Memory (agent ၏ မှတ်ဉာဏ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်၏ အပြင်ဘက်တွင် သိမ်းဆည်းထားပြီး နောက်ပိုင်း agent အဆင့်များတွင် အသုံးပြုရန် ရွေးချယ်ထားသည့် အချက်အလက်များ ဖြစ်သည် — ဥပမာ ယခင်ဆုံးဖြတ်ချက်များ၊ အသုံးပြုသူ၏ နှစ်သက်မှုများ၊ task episode များ သို့မဟုတ် အတည်ပြုပြီး အချက်အလက်များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အတိတ် ဖြစ်ရပ်တိုင်းကို prompt တိုင်းထဲ ထည့်ရန် မလိုဘဲ context window တစ်ခုထက် ကျော်လွန်၍ agent အား ဆက်လက်တည်ရှိမှု ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Agent memory သည် agent state နှင့် တူညီသည် မဟုတ်ပါ။ State သည် လက်ရှိ run ကို ခြေရာခံသည်။ Memory သည် ဖြစ်နိုင်သည့် အနာဂတ် run များအတွက် ရွေးချယ်ထားသည့် အချက်အလက်များကို ထိန်းသိမ်းသည်။
- **လက်တွေ့:** ကျစ်လျစ်သည့် task ရလဒ်ကို provenance နှင့်တကွ သိမ်းဆည်းပြီး သက်ဆိုင်သည့်အခါမှသာ ပြန်လည်ရယူရမည်၊ တည်မြဲသည့် ကိုယ်ရေးအချက်အလက်များကို အသုံးပြုသူ စစ်ဆေးနိုင် သို့မဟုတ် ပြင်ဆင်နိုင်ရမည်။
- **ဆက်စပ် term များ:** Agent State, Context Engineering, Checkpoint, Semantic Cache
- **English (source):** Information stored outside the model and selected for use in later agent steps, such as prior decisions, user preferences, task episodes, or verified facts. It gives an agent continuity beyond one context window without forcing every past event into every prompt.

### Agent State

**မြန်မာ:** Agent State (agent သယ်ဆောင်သည့် အခြေအနေ အချက်အလက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** agent သည် အဆင့်များအကြား သယ်ဆောင်သည့် တိကျပြတ်သားသည့် data ဖြစ်သည် — ဥပမာ လက်ရှိ ရည်မှန်းချက်၊ ပြီးစီးပြီးသား လုပ်ဆောင်ချက်များ၊ tool ရလဒ်များ၊ ဖြေဆိုရန် ကျန်ရှိသည့် မေးခွန်းများ၊ budget များ၊ အတည်ပြုချက်များနှင့် artifact ရည်ညွှန်းချက်များ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** တိကျပြတ်သားသည့် state သည် ရှည်လျားသည့် task များကို ပြန်လည်စတင်နိုင်၊ စစ်ဆေးနိုင်ဖြစ်စေပြီး transcript မှ တိုးတက်မှုကို မော်ဒယ်က ပြန်လည်တည်ဆောက်ရမှုအပေါ် မှီခိုမှု လျော့နည်းစေသည်။
- **မကြာခဏ ရောထွေးမှု:** State သည် conversation history နှင့် တူညီသည် မဟုတ်ပါ။ Transcript သည် အထောက်အထား ဖြစ်သည်။ State သည် နောက်တွင် မည်သည့်အရာ ဖြစ်လာမည်ကို ဆုံးဖြတ်ရန် အသုံးပြုသည့် ကျစ်လျစ်သည့် လုပ်ငန်းလည်ပတ်မှု မှတ်တမ်း ဖြစ်သည်။
- **လက်တွေ့:** ရွေးချယ်ထားသည့် issue၊ ပြောင်းလဲထားသည့် file များ၊ နောက်ဆုံး test ရလဒ်နှင့် ကျန်ရှိသည့် စစ်ဆေးမှုများကို လုပ်ဆောင်ချက် တစ်ခုစီပြီးနောက် update လုပ်သည့် typed object တစ်ခုတွင် သိမ်းဆည်းရမည်။
- **ဆက်စပ် term များ:** Checkpoint, Durable Execution, Context Engineering, Handoff
- **Learn it:** [Repository Memory and State](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/34-repo-memory-and-state/)
- **English (source):** The explicit data an agent carries across steps, such as the current objective, completed actions, tool results, open questions, budgets, approvals, and artifact references. Explicit state makes long tasks resumable, inspectable, and less dependent on the model reconstructing progress from a transcript.

### Agent Skill

**မြန်မာ:** Agent Skill (agent အသုံးပြုနိုင်သည့် လုပ်ငန်းစဉ် ကျွမ်းကျင်မှု အစုအဝေး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** entry point သည် `SKILL.md` ဖြစ်သည့်၊ ရှာဖွေတွေ့ရှိနိုင်သည့် လုပ်ငန်းစဉ် ညွှန်ကြားချက် directory တစ်ခု ဖြစ်ပြီး ၎င်းနှင့် ကိုက်ညီသည့် runtime တစ်ခုက အဆင့်လိုက် load လုပ်နိုင်သည့် ရွေးချယ်နိုင်သည့် reference များ၊ script များနှင့် asset များ ပါဝင်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ပြန်လည်အသုံးပြုနိုင်သည့် task အသိပညာကို စကားဝိုင်း တစ်ခုမှ သီးခြားခွဲထုတ်၍ package လုပ်ပေးပြီး နက်ရှိုင်းသည့် context နှင့် အဆုံးအဖြတ်ပေးသည့် helper များကို လိုအပ်သည့်အခါ အသုံးပြုနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Skill တစ်ခု activate လုပ်ခြင်းသည် context ကို ပေးအပ်သည်။ ၎င်းသည် tool တစ်ခု ဖော်ထုတ်ခြင်း၊ permission ပေးခြင်း၊ sandbox တစ်ခု ဖန်တီးခြင်း သို့မဟုတ် ရလဒ်လုပ်ငန်း မှန်ကန်ကြောင်း သက်သေပြခြင်း မပြုပါ။
- **လက်တွေ့:** ကျစ်လျစ်သည့် name နှင့် routing description ကို ထုတ်ဝေရမည်၊ activate ပြီးနောက်မှသာ workflow ကို load လုပ်ရမည်၊ task သည် သက်ဆိုင်ရာ အခန်းကိုင်းသို့ ရောက်သည့်အခါ branch-specific reference များကို ဖတ်ရမည်။
- **ဆက်စပ် term များ:** Skill Bundle, Skill Catalog, Skill Invocation, Progressive Disclosure, MCP (Model Context Protocol)
- **Learn it:** [Agent Skills: Portable Contract and Runtime Boundary](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/22-skills-and-agent-sdks/)
- **English (source):** A discoverable directory of procedural instructions whose entry point is `SKILL.md`, with optional references, scripts, and assets that a compatible runtime can load in stages. It packages reusable task knowledge separately from one conversation while keeping deeper context and deterministic helpers available on demand.

### Approval Gate

**မြန်မာ:** Approval Gate (အတည်ပြုချက် ဂိတ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အကျိုးဆက် ကြီးမားသည့် လုပ်ဆောင်ချက် တစ်ခုကို အခွင့်အာဏာရှိသူ တစ်ဦး သို့မဟုတ် policy တစ်ခုက ခွင့်ပြုချက် မပေးမချင်း ပိတ်ဆို့ထားသည့် control point တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ပြန်လည်ဖျက်သိမ်းနိုင်သည့် လုပ်ငန်းများအတွက် automation ကို ထိန်းသိမ်းထားရင်း မသေချာသည့် မော်ဒယ် ဆုံးဖြတ်ချက်များ၏ ထိခိုက်နိုင်သည့် အတိုင်းအတာကို ကန့်သတ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Approval gate သည် လုပ်ဆောင်ချက် တစ်ခု ခွင့်ပြုထားခြင်း ရှိမရှိကို မေးသည်။ Verification gate သည် ထို လုပ်ဆောင်ချက် မှန်ကန်ကြောင်း အထောက်အထား ပြသနိုင် ရှိမရှိကို မေးသည်။
- **လက်တွေ့:** agent အား database migration တစ်ခု ရေးဆွဲစေပြီး စွန့်ပစ်နိုင်သည့် database တစ်ခုပေါ်တွင် run စေနိုင်သည်၊ သို့သော် production တွင် လုပ်ဆောင်မှု တိုင်းအတွက် owner တစ်ဦး၏ အတည်ပြုချက် လိုအပ်ရမည်။
- **ဆက်စပ် term များ:** Human-in-the-Loop (HITL), Verification Gate, Least Privilege
- **Learn it:** [Verification Gates](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/38-verification-gates/)
- **English (source):** A control point that blocks a consequential action until an authorized person or policy grants permission. It limits the blast radius of uncertain model decisions while preserving automation for reversible work.

### Checkpoint

**မြန်မာ:** Checkpoint (ပြန်လည်စတင်နိုင်သည့် မှတ်တိုင်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သိရှိထားပြီးသည့် နယ်နိမိတ် တစ်ခုမှ ပြန်လည်စတင်ရန် အသုံးပြုသည့် တည်မြဲသည့် snapshot တစ်ခု ဖြစ်သည်။ Workflow တစ်ခုတွင် operational state နှင့် artifact ရည်ညွှန်းချက်များကို သိမ်းဆည်းသည်။ မော်ဒယ် training တွင် parameter များ၊ optimizer state၊ scheduler state နှင့် training position တို့ကို သိမ်းဆည်းနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ရှည်ကြာသည့် workflow များနှင့် training run များသည် ပြီးစီးပြီးသား လုပ်ငန်းများကို ပြန်လည်လုပ်ဆောင်ခြင်း သို့မဟုတ် တန်ဖိုးကြီးသည့် တိုးတက်မှုကို ဆုံးရှုံးခြင်းမရှိဘဲ ရပ်တန့်မှုမှ ပြန်လည်ကောင်းမွန်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Workflow checkpoint နှင့် model-training checkpoint သည် ပြန်လည်ကောင်းမွန်ရေး ရည်မှန်းချက် တူညီသည်၊ သို့သော် ထိန်းသိမ်းသည့် state မတူညီပါ။ မည်သည့် တစ်ခုမှ transcript သက်သက် သို့မဟုတ် resume metadata မပါသည့် weights file သက်သက် မဟုတ်ပါ။
- **လက်တွေ့:** အတည်ပြုပြီးသည့် အဆင့် တစ်ခုပြီးနောက် agent ၏ လက်ခံပြီးသား patch နှင့် test အထောက်အထားကို သိမ်းဆည်းရမည်၊ သို့မဟုတ် shutdown မပြုမီ training run ၏ weights၊ optimizer state၊ random state နှင့် data position တို့ကို သိမ်းဆည်းရမည်။
- **ဆက်စပ် term များ:** Agent State, Durable Execution, Parameter, Optimizer
- **Learn it:** [Checkpoint Save and Resume](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/19-capstone-projects/47-checkpoint-save-resume/); [Repository Memory and State](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/34-repo-memory-and-state/)
- **English (source):** A durable snapshot used to resume from a known boundary. In a workflow, it stores operational state and artifact references. In model training, it can store parameters, optimizer state, scheduler state, and the training position. Long-running workflows and training runs can recover from interruption without replaying completed work or losing expensive progress.

### Compensating Action

**မြန်မာ:** Compensating Action (ပြီးမြောက်သွားသည့် ဘေးထွက်ဆိုးကျိုးကို ဆန့်ကျင်ဖျက်ပစ်သည့် လုပ်ဆောင်ချက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မူရင်း လုပ်ဆောင်ချက်ကို atomic အနေဖြင့် ပြန်လည်ဖျက်သိမ်းနိုင်ခြင်း မရှိသည့်အခါ ပြီးမြောက်သွားပြီးသည့် ဘေးထွက်ဆိုးကျိုးကို အဓိပ္ပာယ်အားဖြင့် ဆန့်ကျင်ဖျက်ပစ်သည့် တမင်ပြုလုပ်သည့် လုပ်ဆောင်ချက် တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အဆင့်များစွာပါသည့် agent workflow များသည် database များနှင့် ပြင်ပ service များကို ဖြတ်ကျော်သောကြောင့် နောက်ပိုင်းတွင် ဖြစ်ပေါ်သည့် ချို့ယွင်းမှုတစ်ခုသည် အစောပိုင်း စာရေးသွင်းမှုများကို transaction တစ်ခုတည်းဖြင့် ပြန်လည်ဖျက်သိမ်းနိုင်ခြင်း မရှိပါ။
- **မကြာခဏ ရောထွေးမှု:** Compensation သည် လုပ်ငန်း လုပ်ဆောင်ချက် အသစ်တစ်ခု ဖြစ်ပြီး အချိန်ခရီးသွားခြင်း မဟုတ်ပါ။ ၎င်းသည် ချို့ယွင်းနိုင်သောကြောင့် idempotency၊ monitoring နှင့် escalation လိုအပ်သည်။
- **လက်တွေ့:** booking workflow တစ်ခုသည် card ကို ငွေဖြတ်ပြီးနောက် ကြိုတင်မှာယူမှု မအောင်မြင်ပါက ခြေရာခံနိုင်သည့် refund တစ်ခု ထုတ်ပေးပြီး မှတ်တမ်းကို ဖျက်ပစ်မည့်အစား ဖြစ်ရပ် နှစ်ခုလုံးကို ထိန်းသိမ်းရမည်။
- **ဆက်စပ် term များ:** Durable Execution, Idempotency, Checkpoint, Approval Gate
- **English (source):** A deliberate operation that semantically counteracts a completed side effect when the original operation cannot be rolled back atomically. Multi-step agent workflows cross databases and external services where a later failure cannot undo earlier writes through one transaction.

### Delegation

**မြန်မာ:** Delegation (လုပ်ငန်း လွှဲအပ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကန့်သတ်ထားသည့် subtask တစ်ခုကို အခြား လူတစ်ဦး သို့မဟုတ် agent တစ်ခုထံ လိုအပ်သည့် context၊ အခွင့်အာဏာ၊ output contract နှင့် ပြန်လည်ပေးအပ်ရမည့် အခြေအနေများနှင့်တကွ လွှဲအပ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** တိကျပြတ်သားသည့် delegation သည် ပိုင်ဆိုင်မှု၊ scope သို့မဟုတ် ရလဒ်များကို ပေါင်းစည်းနိုင်စွမ်း မဆုံးရှုံးဘဲ အထူးပြုလုပ်ခြင်းနှင့် အပြိုင်လုပ်ဆောင်ခြင်းကို ဖြစ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** အခြား agent တစ်ခုထံ မရှင်းလင်းသည့် မက်ဆေ့ချ် ပေးပို့ခြင်းသည် ယုံကြည်စိတ်ချရသည့် delegation မဟုတ်ပါ။ လက်ခံသူသည် scope contract နှင့် သတ်မှတ်ထားသည့် handoff ကို လိုအပ်သည်။
- **လက်တွေ့:** reviewer agent တစ်ခုအား တိကျသည့် file များ၊ rubric၊ အထောက်အထားနှင့် သတ်မှတ်ချိန်ကို ပေးအပ်ပြီး အဓိက artifact ကို တိတ်ဆိတ်စွာ ပြင်ဆင်ခြင်းမပြုဘဲ တွေ့ရှိချက်များကို ပြန်လည်ပေးအပ်ရန် လိုအပ်ရမည်။
- **ဆက်စပ် term များ:** Scope Contract, Handoff, Reviewer Agent, Orchestration
- **English (source):** Assigning a bounded subtask to another person or agent together with the needed context, authority, output contract, and return conditions. Explicit delegation enables specialization and parallel work without losing ownership, scope, or the ability to integrate results.

### Durable Execution

**မြန်မာ:** Durable Execution (ခံတည်သည့် လုပ်ငန်းစဉ် ဆောင်ရွက်မှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** workflow တစ်ခု၏ state နှင့် ပြီးစီးပြီးသား အဆင့်များသည် process ပျက်ကျခြင်း၊ ပြန်လည်စတင်ခြင်း သို့မဟုတ် ရှည်ကြာသည့် စောင့်ဆိုင်းမှုများကို ကျော်လွန်၍ တည်ရှိနေစေပြီး အတည်ပြုပြီးသား ဘေးထွက်ဆိုးကျိုးများကို ပြန်လည်လုပ်ဆောင်ခြင်း မရှိစေရန် workflow ကို run စေခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** agent task များသည် မော်ဒယ် call များ၊ tool များ၊ အတည်ပြုချက်များနှင့် ပြင်ပ စနစ်များကို ဖြတ်ကျော်လေ့ ရှိသည်။ ယာယီ process တစ်ခုတည်းသည် တိုးတက်မှု၏ တစ်ခုတည်းသော မှတ်တမ်း မဖြစ်သင့်ပါ။
- **မကြာခဏ ရောထွေးမှု:** Durable execution သည် လုပ်ဆောင်မှု တိုင်းကို အလိုအလျောက် လုံခြုံစေသည် မဟုတ်ပါ။ ဘေးထွက်ဆိုးကျိုးများအတွက် idempotency နှင့် compensation စည်းမျဉ်းများ လိုအပ်ဆဲ ဖြစ်သည်။
- **လက်တွေ့:** workflow transition တိုင်းကို persist လုပ်ရမည်၊ ပြင်ပ write များအတွက် idempotency key များ အသုံးပြုရမည်၊ worker ပြန်လည်စတင်ပြီးနောက် နောက်ဆုံး checkpoint မှ ပြန်လည်စတင်ရမည်။
- **ဆက်စပ် term များ:** Checkpoint, Agent State, Idempotency, Approval Gate
- **English (source):** Running a workflow so its state and completed steps survive process crashes, restarts, or long waits without redoing confirmed side effects. Agent tasks often span model calls, tools, approvals, and external systems. A transient process should not be the only record of progress.

### Function Calling

**မြန်မာ:** Function Calling (မော်ဒယ်မှ function ခေါ်ယူ တောင်းဆိုခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်တစ်ခုသည် tool တစ်ခုကို အမည်တပ်ပြီး ၎င်း၏ argument များ ပါဝင်သည့် ဖွဲ့စည်းထားသည့် တောင်းဆိုမှုကို ထုတ်လွှတ်သည့် provider သို့မဟုတ် application interface တစ်ခု ဖြစ်သည်။ Application code သည် တောင်းဆိုမှုကို validate လုပ်ပြီး လုပ်ဆောင်ချက်ကို ဆောင်ရွက်ကာ ရလဒ်ကို နောက် မော်ဒယ် အဆင့်တစ်ခုအတွက် ပြန်လည်ပေးအပ်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Function calling သည် မော်ဒယ်နှင့် ပြင်ပ လုပ်ဆောင်ချက်များကြား ဖွဲ့စည်းထားသည့် ဆက်သွယ်မှု နယ်နိမိတ်ကို ပေးအပ်ပြီး application code သည် လုပ်ဆောင်ချက်ကို အတည်ပြုပြီးမှ ဆောင်ရွက်ရမည် ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** မော်ဒယ်သည် function call တစ်ခုကို တောင်းဆိုသည်။ သင့်၏ ယုံကြည်စိတ်ချရသည့် code သည် ၎င်းကို လုပ်ဆောင်မည်၊ မည်သို့ လုပ်ဆောင်မည်ကို ဆုံးဖြတ်သည်။ Function calling သက်သက်သည် ပြည့်စုံသည့် agent တစ်ခု မဟုတ်ပါ။
- **ဆက်စပ် term များ:** Structured Output, Tool Contract, Agent, MCP (Model Context Protocol) ## G
- **Learn it:** [Function Calling](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/09-function-calling/)
- **English (source):** A provider or application interface through which a model emits a structured request naming a tool and its arguments. Application code validates the request, performs the operation, and can return the result for another model step.

### Human-in-the-Loop (HITL)

**မြန်မာ:** Human-in-the-Loop (HITL) (လူက AI လုပ်ငန်းစဉ်အတွင်း ပါဝင်ဆုံးဖြတ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** AI ဖြင့် မောင်းနှင်သည့် လုပ်ငန်းစဉ် တစ်ခုအတွင်း သတ်မှတ်ထားသည့် အချက်များတွင် လူတစ်ဦးက ဆုံးဖြတ်ချက်၊ အမှားပြင်ဆင်မှု၊ အတည်ပြုချက် သို့မဟုတ် escalation တို့ကို ပေးအပ်သည့် workflow တည်ဆောက်ပုံ တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** လူ၏ ပါဝင်မှုသည် အဆင့်တိုင်းပြီးနောက် မသတ်မှတ်ထားသည့် fallback အနေဖြင့် မဟုတ်ဘဲ သက်ရောက်မှု ကြီးမားသည့်၊ မရှင်းလင်းသည့် သို့မဟုတ် ပြန်လည်ဖျက်သိမ်း၍ မရနိုင်သည့် နယ်နိမိတ်များတွင် အသုံးဝင်ဆုံး ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** HITL သည် စနစ်တစ်ခုကို အလိုအလျောက် လုံခြုံစေသည် မဟုတ်ပါ။ စစ်ဆေးသူများသည် အချိန်၊ context၊ အခွင့်အာဏာနှင့် ရှင်းလင်းသည့် ဆုံးဖြတ်ချက် စံနှုန်း လိုအပ်သည်။
- **လက်တွေ့:** agent သည် ပုံမှန် တောင်းဆိုမှုများကို အလိုအလျောက် အမျိုးအစားခွဲစေနိုင်သည်၊ သို့သော် မသေချာသည့် သို့မဟုတ် တန်ဖိုးကြီးသည့် အမှုများကို အထောက်အထားနှင့် အဆိုပြုထားသည့် လုပ်ဆောင်ချက်နှင့်တကွ စစ်ဆေးသူတစ်ဦးထံ လမ်းကြောင်းလွှဲရမည်။
- **ဆက်စပ် term များ:** Approval Gate, Verification Gate, Agent, Guardrails
- **English (source):** A workflow design in which a person supplies judgment, correction, approval, or escalation at defined points in an AI-driven process. Human involvement is most useful at high-impact, ambiguous, or irreversible boundaries, not as an undefined fallback after every step.

### MCP (Model Context Protocol)

**မြန်မာ:** MCP (Model Context Protocol) (မော်ဒယ်နှင့် context ချိတ်ဆက်သည့် စံ protocol)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** host တစ်ခုသည် သတ်မှတ်ထားသည့် request၊ result၊ discovery နှင့် transport contract များမှတစ်ဆင့် tool များ၊ resource များ၊ prompt များနှင့် extension များကို ဖော်ထုတ်သည့် server များထံ ချိတ်ဆက်ရန် အသုံးပြုသည့် ဖွင့်ထားသည့် JSON-RPC protocol တစ်ခု ဖြစ်သည်။ Revision 2026-07-28 တွင် request တိုင်းသည် initialization handshake သို့မဟုတ် protocol session ကို မှီခိုမည့်အစား ၎င်း၏ protocol version နှင့် client capabilities များကို သယ်ဆောင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** MCP သည် မော်ဒယ် အခြေပြု application များနှင့် ပြင်ပ tool နှင့် context ရင်းမြစ်များကြား ချိတ်ဆက်မှုကို စံချိန်တစ်ခုတည်း ဖြစ်စေပြီး discovery နှင့် exchange လုပ်ငန်းများကို ကြိုတင်သတ်မှတ်ထားသည့် စာချုပ်များအပေါ် တည်ဆောက်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** MCP သည် discovery နှင့် exchange ကို စံပြုပေးသည်။ မည်သည့် tool ကို ခေါ်ရန် လုံခြုံသည်ကို ဆုံးဖြတ်ခြင်း၊ permission ပေးခြင်း သို့မဟုတ် application တစ်ခုကို တိကျသည့် state handle များ အသုံးပြုခြင်းမှ တားမြစ်ခြင်း မပြုပါ။
- **ဆက်စပ် term များ:** Stateless MCP, Multi Round-Trip Request (MRTR), Function Calling, Tool Contract, Least Privilege
- **Learn it:** [Model Context Protocol](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/14-model-context-protocol/)
- **English (source):** An open JSON-RPC protocol for a host to connect to servers that expose tools, resources, prompts, and extensions through defined request, result, discovery, and transport contracts. In revision 2026-07-28, every request carries its protocol version and client capabilities instead of relying on an initialization handshake or protocol session.

### Multi Round-Trip Request (MRTR)

**မြန်မာ:** Multi Round-Trip Request (MRTR) (အသွားအပြန် အကြိမ်များစွာ တောင်းဆိုမှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လုပ်ဆောင်မှု တစ်ခုသည် `resultType: input_required` ကို `inputRequests` တစ်ခု သို့မဟုတ် တစ်ခုထက်ပို၍နှင့်တကွ ပြန်လည်ပေးအပ်ပြီးနောက် client သည် မူရင်း method ကို `inputResponses` နှင့် ပြန်လည်ပေးအပ်ထားသည့် `requestState` အတိအက်နှင့်တကွ ပြန်လည်ကြိုးစားသည့် MCP တောင်းဆိုမှု ပုံစံ တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** stateless server တစ်ခုသည် server-initiated JSON-RPC ဖလှယ်မှုကို ဖွင့်ခြင်း သို့မဟုတ် protocol session state သိမ်းဆည်းခြင်း မပြုဘဲ အသုံးပြုသူ၊ မော်ဒယ် သို့မဟုတ် root input ကို တောင်းဆိုနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** `requestState` သည် မယုံကြည်ရသည့် round-trip data ဖြစ်သည်။ authorization သို့မဟုတ် လုပ်ငန်း ဆုံးဖြတ်ချက်များအတွက် အသုံးမပြုမီ integrity ကို ကာကွယ်ရမည်၊ server-side session identifier အနေဖြင့် မသဘောထားရ။
- **လက်တွေ့:** `tools/call` မှ input request တစ်ခု ပြန်လည်ပေးအပ်ရမည်၊ ခွင့်ပြုထားသည့် response ကို host တွင် စုဆောင်းရမည်၊ ထို tool call ကို JSON-RPC id အသစ်တစ်ခုဖြင့် ပြန်လည်ကြိုးစားရမည်။
- **ဆက်စပ် term များ:** Stateless MCP, MCP (Model Context Protocol), Human-in-the-Loop (HITL), Tool Contract
- **Learn it:** [MCP Roots and Elicitation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/12-mcp-roots-and-elicitation/)
- **English (source):** An MCP request pattern in which an operation returns `resultType: input_required` with one or more `inputRequests`, then the client retries the original method with `inputResponses` and the exact returned `requestState`. It lets a stateless server request user, model, or root input without opening a server-initiated JSON-RPC exchange or storing protocol session state.

### Orchestration

**မြန်မာ:** Orchestration (လုပ်ငန်းစဉ် စီစဉ်မောင်းနှင်မှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်နှင့် tool အဆင့်များအကြား လုပ်ငန်းများကို အစဉ်လိုက် စီစဉ်ခြင်း၊ အခန်းကိုင်းခွဲခြင်း၊ လွှဲအပ်ခြင်း၊ ပြန်လည်ကြိုးစားခြင်း၊ ရပ်တန့်ခြင်း၊ ပြန်လည်စတင်ခြင်းနှင့် အဆုံးသတ်ခြင်းတို့ကို ပြုလုပ်သည့် control logic ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ယုံကြည်စိတ်ချရသည့် agent အပြုအမူသည် မော်ဒယ်၏ အပြင်ဘက်ရှိ တိကျပြတ်သားသည့် workflow ဆုံးဖြတ်ချက်များအပေါ် မှီခိုသည်၊ အထူးသဖြင့် task များတွင် မှီခိုမှုများ သို့မဟုတ် အကျိုးဆက် ကြီးမားသည့် ဘေးထွက်ဆိုးကျိုးများ ရှိသည့်အခါ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Orchestration သည် autonomy သို့မဟုတ် multi-agent စနစ်များနှင့် အဓိပ္ပာယ် တူညီသည် မဟုတ်ပါ။ agent တစ်ခုတည်းကို အဆုံးအဖြတ်ပေးသည့် workflow တစ်ခုဖြင့် orchestrate လုပ်နိုင်သည်။
- **လက်တွေ့:** တည်ငြိမ်သည့် အဆင့်များကို workflow သို့မဟုတ် state machine အနေဖြင့် ရေးသွင်းရမည်၊ ကန့်သတ်ထားသည့် ဆုံးဖြတ်ချက်များကို မော်ဒယ်ထံ ဖော်ထုတ်ရမည်၊ ပြင်ပ write မပြုမီ transition များကို persist လုပ်ရမည်။
- **ဆက်စပ် term များ:** Agent Harness, Planning, Delegation, Durable Execution
- **English (source):** The control logic that sequences, branches, delegates, retries, pauses, resumes, and terminates work across model and tool steps. Reliable agent behavior depends on explicit workflow decisions outside the model, especially when tasks have dependencies or consequential side effects.

### Planning

**မြန်မာ:** Planning (လုပ်ဆောင်ချက် အစီအစဉ် ရေးဆွဲခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လက်ရှိ state မှ ပန်းတိုင်တစ်ခုဆီသို့ ရွေ့လျားရန် ရည်ရွယ်သည့် လုပ်ဆောင်ချက်များ၏ အစဉ်နှင့် မှီခိုမှုများကို တည်ဆောက်ခြင်း၊ ရွေးချယ်ခြင်း သို့မဟုတ် ပြန်လည်ပြင်ဆင်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** တိကျပြတ်သားသည့် အစီအစဉ်များသည် agent သည် ကုန်ကျစရိတ် ကြီးမားသည့် သို့မဟုတ် ပြန်လည်ဖျက်သိမ်း၍ မရနိုင်သည့် လုပ်ဆောင်ချက်များကို မစတင်မီ ယူဆချက်များနှင့် အစဉ်လိုက်ဖြစ်မှုကို မြင်သာအောင် ဖြစ်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** ထုတ်လုပ်ထားသည့် အစီအစဉ်တစ်ခုသည် အဆိုပြုချက် တစ်ခု ဖြစ်ပြီး အဆင့်များ ဖြစ်နိုင်ခြေ ရှိမှု၊ လုံလောက်မှု သို့မဟုတ် လုံခြုံမှုကို သက်သေပြချက် မဟုတ်ပါ။
- **လက်တွေ့:** မှီခိုမှုကို သိရှိသည့် တိုတောင်းသည့် အစီအစဉ် တစ်ခု တောင်းခံရမည်၊ ရရှိနိုင်သည့် tool များနှင့် permission များနှင့် ကိုက်ညီမှုကို စစ်ဆေးရမည်၊ လေ့လာတွေ့ရှိချက်များက ယူဆချက်တစ်ခုကို မမှန်တော့ကြောင်း ပြသည့်အခါ ပြန်လည်အစီအစဉ်ဆွဲရမည်။
- **ဆက်စပ် term များ:** Agent State, ReAct, Orchestration, Verification Gate
- **English (source):** Constructing, selecting, or revising a sequence of actions and dependencies intended to move from the current state to a goal. Explicit plans make assumptions and ordering visible before an agent commits to expensive or irreversible actions.

### ReAct

**မြန်မာ:** ReAct (ကျိုးကြောင်းဆင်ခြင်မှုနှင့် လုပ်ဆောင်မှု ရောနှောသည့် ပုံစံ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** နောက် အဆင့်ကို မဆုံးဖြတ်မီ task ကျိုးကြောင်းဆင်ခြင်မှု၊ တိကျသည့် လုပ်ဆောင်ချက် တစ်ခုနှင့် environment မှ ပြန်လည်ပေးအပ်သည့် observation တို့ကို တစ်လှည့်စီ ရောနှောပေးသည့် agent ပုံစံ တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** environment feedback သည် ယူဆချက်များကို ပြင်ဆင်ပေးနိုင်ပြီး မော်ဒယ်ကို ပြည်တွင်း ဖန်တီးမှုသက်သက်ဖြင့် task တစ်ခုလုံးကို ပြီးစီးရန် တွန်းအားပေးခြင်းအစား နောက်ပိုင်း ဆုံးဖြတ်ချက်များကို အခြေခံကျစေသည်။
- **မကြာခဏ ရောထွေးမှု:** ReAct သည် prompting နှင့် control ပုံစံ တစ်ခု ဖြစ်ပြီး autonomy၊ မှန်ကန်မှု သို့မဟုတ် လုံခြုံသည့် tool အသုံးပြုမှုကို အာမခံချက် မဟုတ်ပါ။
- **လက်တွေ့:** အနည်းငယ်သော typed tool များကို ဖော်ထုတ်ရမည်၊ တိုတောင်းသည့် observation များ ပြန်လည်ပေးအပ်ရမည်၊ loop ကို ကန့်သတ်ရမည်၊ ပုဂ္ဂလိက ကျိုးကြောင်းဆင်ခြင်မှု trace များကို သိမ်းဆည်းခြင်းအစား နောက်ဆုံး artifact ကို verify လုပ်ရမည်။
- **ဆက်စပ် term များ:** Agent, Function Calling, Planning, Grounding
- **English (source):** An agent pattern that interleaves task reasoning, a concrete action, and an observation returned by the environment before deciding the next step. Environment feedback can correct assumptions and ground later decisions instead of forcing the model to complete the entire task from internal generation alone.

### Sandbox

**မြန်မာ:** Sandbox (သီးခြားခွဲထုတ်ထားသည့် လုံခြုံသည့် လုပ်ဆောင်မှု ပတ်ဝန်းကျင်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** agent တစ်ခု၏ file များ၊ process များ၊ network ပန်းတိုင်များ၊ credential များနှင့် host အရင်းအမြစ်များသို့ ဝင်ရောက်နိုင်မှုကို ကန့်သတ်ထားသည့် သီးခြားခွဲထုတ်ထားသည့် လုပ်ဆောင်မှု ပတ်ဝန်းကျင် တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထုတ်လုပ်ထားသည့် code နှင့် tool call များသည် မှားယွင်းနိုင် သို့မဟုတ် အန္တရာယ်ရှိနိုင်သည်။ သီးခြားခွဲထုတ်ခြင်းသည် ၎င်းတို့၏ သက်ရောက်နိုင်သည့် အတိုင်းအတာကို ကန့်သတ်ပြီး စွန့်ပစ်နိုင်သည့် verification ကို လက်တွေ့ကျစေသည်။
- **မကြာခဏ ရောထွေးမှု:** Sandbox သည် သက်ရောက်မှုကို လျော့နည်းစေသည်။ ၎င်းအတွင်းရှိ code မှန်ကန်သည် သို့မဟုတ် အန္တရာယ်ကင်းသည်ကို သက်သေပြခြင်း မပြုပါ။
- **လက်တွေ့:** ephemeral container တစ်ခုတွင် read-only base၊ ကန့်သတ်ထားသည့် စာရေးနိုင်သည့် workspace၊ production secret မပါခြင်းနှင့် တိကျပြတ်သားသည့် network allowlist တို့ဖြင့် test များ run ရမည်။
- **ဆက်စပ် term များ:** Least Privilege, Approval Gate, Coding Agent, Guardrails
- **Learn it:** [Production Agent Runtimes](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/29-production-runtimes/)
- **English (source):** An isolated execution environment that restricts an agent's access to files, processes, network destinations, credentials, and host resources. Generated code and tool calls can be wrong or malicious. Isolation limits their reach and makes disposable verification practical.

### Skill Bundle

**မြန်မာ:** Skill Bundle (skill အစုအဝေး အပြည့်အစုံ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** `SKILL.md` နှင့် workflow လိုအပ်သည့် reference၊ script၊ asset၊ fixture သို့မဟုတ် အဖော် file အားလုံး အပါအဝင် ပြည့်စုံသည့် တပ်ဆင်နိုင်သည့် skill directory တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** entry file ကိုသာ ကူးယူခြင်းသည် ပျောက်ဆုံးနေသည့် အရင်းအမြစ်များကို ညွှန်းသည့် သို့မဟုတ် workflow မှီခိုသည့် အဆုံးအဖြတ်ပေးသည့် code ဆုံးရှုံးသည့်၊ မှန်ကန်ပုံရသည့် ညွှန်ကြားချက်များကို ချန်ထားနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** `SKILL.md` သည် entry point ဖြစ်ပြီး artifact တစ်ခုလုံး မဖြစ်မနေ မဟုတ်ပါ။
- **လက်တွေ့:** သစ်ပင်ကို ယူနစ်တစ်ခုအနေဖြင့် တပ်ဆင်ရမည်၊ hash များနှင့် source revision ကို မှတ်တမ်းတင်ရမည်၊ တပ်ဆင်ထားသည့် မိတ္တူကို validate လုပ်ရမည်၊ ရှိပြီးသား bundle ကို အစားထိုးမီ collision များကို ပြသရမည်။
- **ဆက်စပ် term များ:** Agent Skill, Skill Catalog, Reproducible Build, Provenance Attestation
- **Learn it:** [Skill Evals, Packaging, and Portability](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/27-skill-evals-packaging-and-portability/)
- **English (source):** The complete installable skill directory, including `SKILL.md` and every reference, script, asset, fixture, or companion file required by the workflow. Copying only the entry file can leave valid-looking instructions that point to missing resources or lose the deterministic code the workflow depends on.

### Skill Catalog

**မြန်မာ:** Skill Catalog (skill များ၏ စာရင်းအညွှန်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အရည်အချင်းပြည့်မီသည့် skill များ၏ မော်ဒယ် မြင်နိုင်သည့် ကျစ်လျစ်သည့် စာရင်း ဖြစ်ပြီး များသောအားဖြင့် skill body အားလုံးမဟုတ်ဘဲ name၊ description နှင့် အတွင်းပိုင်း source identifier ကဲ့သို့သော routing metadata များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Catalog သည် agent အား တပ်ဆင်ထားသည့် package တိုင်းကို လုပ်ငန်း context ထဲ ထည့်ရန် မလိုဘဲ သက်ဆိုင်သည့် လုပ်ငန်းစဉ်များကို ရှာဖွေတွေ့ရှိနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Catalog entry တစ်ခု ရှိခြင်းသည် skill ရှာဖွေတွေ့ရှိနိုင်သည် ဟု အဓိပ္ပာယ်ရသည်။ Body active ဖြစ်သည် သို့မဟုတ် ၎င်း၏ tool များ ခွင့်ပြုထားသည် ဟု မဆိုလိုပါ။
- **လက်တွေ့:** package များကို အရင် validate လုပ်ရမည်၊ တိကျပြတ်သားသည့် duplicate-name policy ကို ကျင့်သုံးရမည်၊ serialized catalog budget ကို တိုင်းတာရမည်၊ တိုချုံ့ခြင်း၊ ချန်လှပ်ခြင်း သို့မဟုတ် ဖုံးလွှမ်းခံရသည့် entry များအတွက် diagnostic များ ထိန်းသိမ်းရမည်။
- **ဆက်စပ် term များ:** Skill Discovery, Skill Invocation, Progressive Disclosure, Token Budget
- **Learn it:** [Skill Discovery and Progressive Disclosure](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure/)
- **English (source):** The compact model-visible inventory of eligible skills, usually containing routing metadata such as name, description, and an internal source identifier rather than every skill body. A catalog lets an agent discover relevant procedures without loading every installed package into the working context.

### Skill Discovery

**မြန်မာ:** Skill Discovery (skill များ ရှာဖွေတွေ့ရှိခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် root များကို ရှာဖွေခြင်း၊ ဖြစ်နိုင်သည့် skill directory များကို ဖော်ထုတ်ခြင်း၊ ၎င်းတို့၏ package contract ကို validate လုပ်ခြင်း၊ scope နှင့် provenance ကို တွဲဖက်ခြင်း၊ collision များကို ဖြေရှင်းခြင်းနှင့် သတ်မှတ်ချက် ပြည့်မီသည့် catalog entry များကို ထုတ်ဝေခြင်းတို့ကို ပြုလုပ်သည့် runtime pipeline တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အဆုံးအဖြတ်ပေးသည့် discovery သည် မော်ဒယ် routing မစတင်မီ ပျောက်ဆုံးခြင်း၊ ပုံပျက်ခြင်း၊ ဖုံးလွှမ်းခံရခြင်းနှင့် မလုံခြုံသည့် package များကို ရောဂါရှာဖွေနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Skill discovery သည် `SKILL.md` ဟု အမည်တပ်ထားသည့် filename များကို ကန့်သတ်ချက်မရှိ ထပ်ခါတလဲလဲ ရှာဖွေခြင်း မဟုတ်ပါ။ တပ်ဆင်သည့် တည်နေရာများနှင့် ဦးစားပေးအစဉ်သည် runtime policy ဖြစ်သည်။
- **လက်တွေ့:** ရှာဖွေမည့် scope များနှင့် duplicate အပြုအမူကို ကြေညာရမည်၊ symlink များကို မည်သို့ ကိုင်တွယ်မည်ကို ဆုံးဖြတ်ရမည်၊ resource escape များကို ငြင်းပယ်ရမည်၊ candidate တစ်ခုစီ လက်ခံခြင်း သို့မဟုတ် ငြင်းပယ်ခြင်း၏ အကြောင်းရင်းကို log မှတ်ရမည်။
- **ဆက်စပ် term များ:** Skill Catalog, Skill Bundle, Progressive Disclosure, Trust Boundary
- **Learn it:** [Skill Discovery and Progressive Disclosure](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure/)
- **English (source):** A runtime pipeline that searches configured roots, identifies candidate skill directories, validates their package contract, attaches scope and provenance, resolves collisions, and publishes eligible catalog entries. Deterministic discovery makes missing, malformed, shadowed, and unsafe packages diagnosable before model routing begins.

### Skill Invocation

**မြန်မာ:** Skill Invocation (skill ကို အသုံးချ ခေါ်ယူခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အရည်အချင်းပြည့်မီသည့် လူတစ်ဦး၊ မော်ဒယ်၊ application တစ်ခု သို့မဟုတ် အခြား skill တစ်ခုက skill တစ်ခုကို ရွေးချယ်ပြီး ၎င်း၏ ညွှန်ကြားချက်များကို လုပ်ငန်း context ထဲ ဝင်ရောက်စေသည့် runtime မှ ဖြတ်ကူးစေသည့် လုပ်ငန်းစဉ် တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** တိကျပြတ်သားသည့် အသုံးပြုသူ ဝင်ရောက်ခွင့်၊ သွယ်ဝိုက်သည့် မော်ဒယ် routing၊ activation၊ argument binding၊ tool permission နှင့် execution တို့သည် မတူညီသည့် ချို့ယွင်းမှု ပုံစံများရှိသည့် သီးခြား ဆုံးဖြတ်ချက်များ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Invocation သည် ညွှန်ကြားချက်များကို activate လုပ်သည်။ ၎င်းသည် command တစ်ခုကို အလိုအလျောက် လုပ်ဆောင်ခြင်း သို့မဟုတ် approval နှင့် sandbox policy ကို ကျော်လွန်ခြင်း မပြုပါ။
- **လက်တွေ့:** actor policy ကို သတ်မှတ်ရမည်၊ description များကို အပြုသဘောနှင့် နီးစပ်သော်လည်း မကိုက်ညီသည့် တောင်းဆိုမှုများဖြင့် အကဲဖြတ်ရမည်၊ ရွေးချယ်ထားသည့် package အမှတ်အသားကို မှတ်တမ်းတင်ရမည်၊ host-specific invocation field များကို စမ်းသပ်ပြီးသား adapter များတွင် ထားရှိရမည်။
- **ဆက်စပ် term များ:** Agent Skill, Skill Catalog, Approval Gate, Sandbox
- **Learn it:** [Skill Invocation and Routing](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/25-skill-invocation-and-routing/)
- **English (source):** The runtime-mediated process in which an eligible human, model, application, or other skill selects a skill and causes its instructions to enter the working context. Explicit user access, implicit model routing, activation, argument binding, tool permission, and execution are separate decisions with different failure modes.

### Stateless MCP

**မြန်မာ:** Stateless MCP (protocol session state မထိန်းသိမ်းသည့် MCP)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** request တိုင်းသည် `params._meta` တွင် protocol version နှင့် client capabilities များကို သယ်ဆောင်ပြီး ရလဒ်များသည် တိကျပြတ်သားသည့် `resultType` ကို သယ်ဆောင်သည့် MCP 2026-07-28 တောင်းဆိုမှု ပုံစံ ဖြစ်သည်။ initialization handshake၊ connection သို့မဟုတ် `Mcp-Session-Id` ဖြင့် key လုပ်ထားသည့် protocol state မရှိပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** worker တိုင်းသည် request တစ်ခုကို ၎င်း၏ အကြောင်းအရာများနှင့် authorization context မှ validate လုပ်ပြီး လုပ်ဆောင်နိုင်သည်၊ ထို့ကြောင့် ဖုံးကွယ်ထားသည့် connection affinity ကို ရှောင်ရှားနိုင်ပြီး အလျားလိုက် routing ကို စဉ်းစားရ ပိုမိုလွယ်ကူစေသည်။
- **မကြာခဏ ရောထွေးမှု:** Stateless MCP သည် protocol session များကို ဖယ်ရှားသည်။ application state၊ transport connection များ၊ streaming response များ၊ task များ သို့မဟုတ် တိကျပြတ်သားသည့် handle များကို မဖယ်ရှားပါ။
- **လက်တွေ့:** `server/discover` ကို အကောင်အထည်ဖော်ရမည်၊ call တိုင်းတွင် request metadata ကို ပြန်လည်တည်ဆောက်ရမည်၊ transport header များကို JSON-RPC body နှင့် ကိုက်ညီမှု စစ်ဆေးရမည်၊ ဆက်လက်တည်ရှိမှု လိုအပ်သည့်အခါ server မှ ထုတ်ပေးသည့် application handle များကို သာမန် tool argument များအနေဖြင့် ပေးအပ်ရမည်။
- **ဆက်စပ် term များ:** MCP (Model Context Protocol), Multi Round-Trip Request (MRTR), Tool Contract, Idempotency
- **Learn it:** [MCP Fundamentals](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/06-mcp-fundamentals/)
- **English (source):** The MCP 2026-07-28 request model in which every request carries the protocol version and client capabilities in `params._meta`, while results carry an explicit `resultType`; no protocol state is keyed by an initialization handshake, connection, or `Mcp-Session-Id`. Any worker can validate and process a request from its contents and authorization context, which avoids hidden connection affinity and makes horizontal routing easier to reason about.

### Structured Output

**မြန်မာ:** Structured Output (schema နှင့် ကိုက်ညီအောင် ဖွဲ့စည်းထားသည့် မော်ဒယ် ရလဒ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** application code သည် လွတ်လပ်သည့် စကားပြေ စာသားကို ခွဲခြမ်းစိတ်ဖြာရန် မလိုဘဲ field များကို အသုံးပြုနိုင်ရန် မော်ဒယ် ရလဒ်ကို စက်ဖတ်နိုင်သည့် schema တစ်ခုနှင့် ကိုက်ညီအောင် ကန့်သတ်ခြင်း သို့မဟုတ် validate လုပ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် မော်ဒယ်နှင့် software အကြား နယ်နိမိတ်တွင် ပုံစံ မရှင်းလင်းမှုကို လျော့နည်းစေပြီး field အဆင့် validation နှင့် ပြန်လည်ကြိုးစားမှုများကို ဖြစ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Schema နှင့် ကိုက်ညီသည့် ရလဒ်တွင် မှားယွင်းသည့် တန်ဖိုးများ ရှိနိုင်ဆဲ ဖြစ်သည်။ ဖွဲ့စည်းပုံသည် အချက်အလက် မှန်ကန်မှု စစ်ဆေးခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** ခွင့်ပြုထားသည့် severity enum၊ evidence array နှင့် nullable escalation reason ပါဝင်သည့် incident triage ရလဒ်တစ်ခုကို လိုအပ်ရမည်၊ schema မကိုက်ညီသည့် တုံ့ပြန်မှု တိုင်းကို ငြင်းပယ်ရမည်။
- **ဆက်စပ် term များ:** Function Calling, Tool Contract, Verification Gate
- **Learn it:** [Structured Outputs](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/03-structured-outputs/)
- **English (source):** Model output constrained or validated against a machine-readable schema so application code can consume fields without parsing free-form prose. It reduces format ambiguity at the model-to-software boundary and enables field-level validation and retries.

### Swarm

**မြန်မာ:** Swarm (ဗဟို ထိန်းချုပ်မှု တစ်ခုတည်း မရှိသည့် agent အစုအဝေး)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဒေသခံ agent ဆုံးဖြတ်ချက်များနှင့် မက်ဆေ့ချ် ဖလှယ်မှုသည် စနစ်အဆင့် အပြုအမူကို ဖြစ်ပေါ်စေသည့် ချိတ်ဆက်မှု လျော့ရဲရဲ multi-agent ပုံစံ တစ်ခု ဖြစ်သည်။ ထို ဝေါဟာရကို တစ်သမတ်တည်း မဟုတ်ဘဲ အသုံးပြုသည့်အတွက် အမှန်တကယ် topology၊ state ပိုင်ဆိုင်မှုနှင့် အဆုံးသတ်ခြင်း စည်းမျဉ်းများကို သတ်မှတ်ရမည်။
- **အရေးပါသည့် အကြောင်းရင်း:** multi-agent ပုံစံများတွင် topology၊ state ပိုင်ဆိုင်မှုနှင့် အဆုံးသတ်ခြင်း စည်းမျဉ်းများကို မသတ်မှတ်ထားပါက အပြုအမူကို ခန့်မှန်းနိုင်ခြင်း မရှိသောကြောင့် ၎င်းတို့ကို တိကျစွာ ဖော်ပြရန် လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** အမည်တပ်ထားသည့် agent အများအပြား ရှိခြင်းသည် အသုံးဝင်သည့် အထူးပြုလုပ်မှု သို့မဟုတ် ပေါ်ပေါက်လာသည့် ဟန်ချက်ညီမှုကို အာမခံခြင်း မပြုပါ။
- **ဆက်စပ် term များ:** Agent, Reviewer Agent, Handoff, Agent State
- **English (source):** A loosely coordinated multi-agent pattern in which local agent decisions and message exchange produce system-level behavior. The term is used inconsistently, so the actual topology, state ownership, and termination rules must be specified.

### Termination Condition

**မြန်မာ:** Termination Condition (ရပ်တန့်စေသည့် အခြေအနေ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** agent run တစ်ခုသည် အောင်မြင်သည့်အခါ၊ ကျရှုံးသည့်အခါ၊ budget ကုန်ဆုံးသည့်အခါ၊ လုံခြုံသည့် နယ်နိမိတ်သို့ ရောက်သည့်အခါ သို့မဟုတ် escalation လိုအပ်သည့်အခါ ၎င်းကို အဆုံးသတ်စေသည် သို့မဟုတ် ရပ်တန့်စေသည့် တိကျပြတ်သားသည့် စည်းမျဉ်း တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** termination condition မရှိပါက agent သည် loop ဖြစ်ခြင်း၊ ဘေးထွက်ဆိုးကျိုးများ ထပ်ခါတလဲလဲ ဖြစ်ခြင်း၊ budget ဖြုန်းတီးခြင်း သို့မဟုတ် ပန်းတိုင်ကို မပြည့်မီဘဲ ပြီးစီးပြီဟု ဆိုခြင်းတို့ ဖြစ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Stop sequence သည် စာသား ထုတ်လုပ်ခြင်းကို အဆုံးသတ်သည်။ Termination condition သည် task သို့မဟုတ် workflow ရပ်သင့် မရပ်သင့်ကို ဆုံးဖြတ်သည်။
- **လက်တွေ့:** loop မစတင်မီ အောင်မြင်မှု အထောက်အထား၊ အများဆုံး အဆင့်နှင့် ကုန်ကျစရိတ်၊ ပြန်လည်ကြိုးစား၍ မရနိုင်သည့် အမှားများနှင့် escalation အခြေအနေများကို သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Agent Harness, Token Budget, Verification Gate, Stop Sequence
- **English (source):** An explicit rule that ends or pauses an agent run when it succeeds, fails, exhausts a budget, reaches a safe boundary, or requires escalation. Without a termination condition, an agent can loop, repeat side effects, waste budget, or claim completion without satisfying the goal.

### Tool Contract

**မြန်မာ:** Tool Contract (tool နယ်နိမိတ်၏ ပြည့်စုံသည့် စာချုပ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** tool နယ်နိမိတ် တစ်ခုအတွက် ပြည့်စုံသည့် သဘောတူညီချက် ဖြစ်သည် — ရည်ရွယ်ချက်၊ typed input များ၊ output များ၊ validation၊ permission များ၊ ဘေးထွက်ဆိုးကျိုးများ၊ အမှားများ၊ timeout များ၊ idempotency နှင့် ခေါ်သူထံ ပြန်လည်ပေးအပ်သည့် အထောက်အထား တို့ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** schema တစ်ခုသည် မော်ဒယ်အား မည်သည့် field များ ရှိသည်ကို ပြောသည်။ Contract တစ်ခုသည် စနစ်အား tool သည် မည်သည့်အခါ လုံခြုံသည်နှင့် ချို့ယွင်းမှုများကို မည်သို့ ကိုင်တွယ်ရမည်ကို ပြောသည်။
- **မကြာခဏ ရောထွေးမှု:** JSON Schema တစ်ခုသည် tool contract ၏ အစိတ်အပိုင်း တစ်ခု ဖြစ်ပြီး စာချုပ် တစ်ခုလုံး မဟုတ်ပါ။
- **လက်တွေ့:** ခွင့်ပြုထားသည့် root၊ မျှော်မှန်းထားသည့် base revision၊ အများဆုံး အရွယ်အစား၊ dry-run mode၊ တိကျပြတ်သားသည့် conflict error များနှင့် ပြန်လည်ပေးအပ်သည့် patch hash ပါဝင်သည့် file-write tool တစ်ခုကို သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Function Calling, Structured Output, Least Privilege, Idempotency
- **Learn it:** [Tool Use and Function Calling](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/06-tool-use-and-function-calling/)
- **English (source):** The complete agreement for a tool boundary: purpose, typed inputs, outputs, validation, permissions, side effects, errors, timeouts, idempotency, and evidence returned to the caller. A schema tells a model what fields exist; a contract tells the system when the tool is safe and how failures must be handled.

## Self-check

<details>
<summary>အဖြေများ ကြည့်ရန်</summary>

၁။ Agent တစ်ခုနှင့် မော်ဒယ် တစ်ခု၏ ကွာခြားချက်ကား အဘယ်နည်း။
မော်ဒယ်သည် Agent ၏ အစိတ်အပိုင်း တစ်ခုသာ ဖြစ်သည်။ Agent သည် လုပ်ဆောင်ချက်များ ရွေးချယ်ခြင်း၊ tool သို့မဟုတ် environment ရလဒ်များ လေ့လာခြင်းနှင့် orchestration policy တစ်ခုအောက်တွင် ဆက်လက်လုပ်ဆောင်ခြင်းတို့ကို စီမံသည့် စနစ် တစ်ခု ဖြစ်သည်။

၂။ Approval Gate နှင့် Verification Gate သည် မည်သို့ ကွာခြားသနည်း။
Approval Gate သည် လုပ်ဆောင်ချက် တစ်ခု ခွင့်ပြုထားခြင်း ရှိမရှိကို မေးသည်။ Verification Gate သည် အထောက်အထားဖြင့် ထို လုပ်ဆောင်ချက် မှန်ကန်ကြောင်း ပြသနိုင် ရှိမရှိကို မေးသည်။

၃။ Agent Memory နှင့် Agent State သည် မည်သို့ ကွာခြားသနည်း။
State သည် လက်ရှိ run ကို ခြေရာခံသည်။ Memory သည် ဖြစ်နိုင်သည့် အနာဂတ် run များအတွက် ရွေးချယ်ထားသည့် အချက်အလက်များကို ထိန်းသိမ်းသည်။

၄။ Sandbox သည် မည်သည့်အရာကို အာမခံသည်၊ မည်သည့်အရာကို အာမခံခြင်း မပြုသနည်း။
Sandbox သည် သက်ရောက်မှု အတိုင်းအတာကို လျော့နည်းစေသည်။ ၎င်းအတွင်းရှိ code မှန်ကန်သည် သို့မဟုတ် အန္တရာယ်ကင်းသည်ကို အာမခံခြင်း မပြုပါ။

၅။ Tool Contract တစ်ခုတွင် JSON Schema တစ်ခုတည်း လုံလောက်ပါသလား။
မလုံလောက်ပါ။ Schema သည် ရှိသည့် field များကို ဖော်ပြရုံသာ ဖြစ်သည်။ Contract တွင် ရည်ရွယ်ချက်၊ validation၊ permission၊ ဘေးထွက်ဆိုးကျိုး၊ အမှား၊ timeout၊ idempotency နှင့် ခေါ်သူထံ ပြန်လည်ပေးအပ်သည့် အထောက်အထား တို့ ပါဝင်ရမည်။

</details>

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)
- Source repository: [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) (MIT License)
- [The Agent Loop](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/01-the-agent-loop/)
- [Minimal Agent Workbench](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/32-minimal-agent-workbench/)
- [Tool Use and Function Calling](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/06-tool-use-and-function-calling/)
- [Verification Gates](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/38-verification-gates/)
- [Model Context Protocol](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/14-model-context-protocol/)
- [MCP Fundamentals](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/13-tools-and-protocols/06-mcp-fundamentals/)

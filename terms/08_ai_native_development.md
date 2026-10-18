# 08 — AI-native development

ဤဖိုင်သည် **AI-native development** နယ်ပယ်မှ စုစုပေါင်း **term ၂၃ ခု** ကို English + မြန်မာ နှစ်ဘာသာဖြင့်
စုစည်းထားသည့် ကိုးကားလမ်းညွှန် ဖြစ်သည်။ ဤနယ်ပယ်သည် AI ဖြင့် software ကို တည်ဆောက်သည့် လုပ်ငန်းစဉ် —
ဆိုလိုသည်မှာ coding agent များအား repository context ပေးခြင်း၊ ၎င်းတို့ ထုတ်လုပ်သည့် patch များကို
စစ်ဆေးခြင်း နှင့် ပြီးစီးမှုကို အထောက်အထားဖြင့် အတည်ပြုခြင်း — ကို ဖုံးလွှမ်းသည်။

ဤ term များကို တစ်စုတစ်စည်း လေ့လာရန် လိုအပ်သည်။ Coding agent တစ်ခု၏ အထွက်သည် patch ဖြစ်ပြီး၊ ထို patch ကို
reviewer agent၊ scope contract နှင့် verification gate များဖြင့် စစ်ဆေးရသည်။ ထို လုပ်ငန်းစဉ်တစ်လျှောက်
cost per successful task၊ observability နှင့် trace များက စနစ် တကယ် အလုပ်လုပ်ခြင်း ရှိ၊ မရှိ ကို
တိုင်းတာပေးသည်။ ထို့ကြောင့် ဤနယ်ပယ်သည် မော်ဒယ် အရည်အသွေးထက် လုပ်ငန်းစဉ် ဖွဲ့စည်းပုံ —
context၊ နယ်နိမိတ်၊ verification နှင့် ထိန်းချုပ်မှု — အပေါ် အလေးထားသည်။

ဤနယ်ပယ်သည် လုံခြုံရေး နယ်ပယ်နှင့် ကွာခြားသည်။ ဤနေရာတွင် ခွင့်ပြုချက် စည်းမျဉ်းများ နှင့် အန္တရာယ်
ပုံစံကို မဟုတ်ဘဲ၊ agent များ နှင့် လူများ ပူးပေါင်း၍ အလုပ်တစ်ခုကို မည်သို့ သတ်မှတ်သည်၊ လွှဲပြောင်းသည်၊
စစ်ဆေးသည် နှင့် တိုင်းတာသည် ကို အဓိက ထားသည်။

term တစ်ခုချင်းစီကို အောက်ပါ ပုံစံဖြင့် ဖတ်ရမည်။ **မြန်မာ** သည် term ၏ မြန်မာ အမည် သို့မဟုတ်
အနီးစပ်ဆုံး ဖော်ပြချက် ဖြစ်သည်။ **ဆိုလိုသည့် အဓိပ္ပာယ်** သည် source ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ်ကို
ရှင်းလင်းသည်။ **အရေးပါသည့် အကြောင်းရင်း** သည် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည် ကို ဆိုသည်။
**မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** သည် မှားတတ်သည့် အချက် နှင့် လက်တွေ့ အသုံးချမှု ဥပမာကို
ပေးသည်။ **ဆက်စပ် term များ** နှင့် **Learn it** သည် နောက်တစ်ဆင့် ဖတ်ရမည့် လမ်းကို ပြသည်။
**English (source)** သည် source ၏ မူရင်း အင်္ဂလိပ် စာသား ဖြစ်ပြီး၊ စကားလုံး တစ်လုံးမျှ
မပြင်ဘဲ ထားရှိသည်။

### Backpressure

**မြန်မာ:** နောက်သို့ ဖိအား ထိန်းချုပ်ခြင်း (Backpressure)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အောက်ပိုင်း component တစ်ခုသည် လက်ရှိ နှုန်းအတိုင်း လုပ်ငန်းကို လုံခြုံစွာ မလုပ်ဆောင်နိုင်သည့်အခါ အပေါ်ပိုင်း (upstream) အလုပ်ကို နှေးကွေးစေခြင်း သို့မဟုတ် လက်မခံဘဲ ပယ်ချခြင်းဖြင့် flow ကို ထိန်းချုပ်သည့် ယန္တရား ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Backpressure မရှိပါက တန်းစီနေသည့် agent run များ၊ tool call များ သို့မဟုတ် stream ဖြင့် ပို့သည့် event များသည် memory ကို ကုန်ဆုံးစေနိုင်သည်၊ rate limit ကို ကျော်လွန်စေနိုင်သည်၊ retry များကို ပို၍ ဆိုးရွားစွာ မြှင့်တင်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Backpressure သည် ပျက်ကွက်မှု မဖြစ်မီတွင် capacity ကို ကာကွယ်သည်။ Circuit breaker သည် dependency တစ်ခု ကျန်းမာမှု မရှိတော့ကြောင်း ပျက်ကွက်မှုများ ပေါ်ထွက်ပြီးမှ ခေါ်ဆိုမှုများကို ရပ်တန့်သည်။
- **လက်တွေ့:** evaluator queue သည် ၎င်း၏ အကန့်အသတ်သို့ ရောက်သည့်အခါ agent job အသစ်များကို ခေတ္တရပ်ဆိုင်းခြင်း သို့မဟုတ် အကန့်အသတ်မရှိသည့် အလုပ်ကို လက်ခံခြင်းအစား ပြန်လုပ်နိုင်သည့် တုံ့ပြန်ချက် ပြန်ပေးခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Rate Limit, Retry with Backoff, Circuit Breaker
- **English (source):** A flow-control mechanism that slows or rejects upstream work when a downstream component cannot process it safely at the current rate. Without backpressure, queued agent runs, tool calls, or streamed events can exhaust memory, exceed rate limits, and amplify retries.

### Circuit Breaker

**မြန်မာ:** ဆားကစ် ချိုးသည့် ယန္တရား (Circuit Breaker)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပျက်ကွက်မှုများ သတ်မှတ်ထားသည့် အဆင့်တစ်ခုကို ကျော်လွန်သည့်အခါ dependency တစ်ခုသို့ ခေါ်ဆိုမှုများကို ခေတ္တရပ်ဆိုင်းပြီး၊ ထို့နောက် dependency ပြန်လည် ကောင်းမွန်လာခြင်း ရှိ၊ မရှိ စမ်းသပ် စစ်ဆေးသည့် ယုံကြည်စိတ်ချရမှု ထိန်းချုပ်ကိရိယာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မော်ဒယ် သို့မဟုတ် tool ၏ ထပ်ခါတလဲလဲ ပျက်ကွက်မှုများသည် ကျန်စနစ် တစ်ခုလုံးတွင် latency၊ budget နှင့် capacity ကို မစားသုံးစေရန် ကာကွယ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Circuit breaker သည် dependency ၏ ကျန်းမာမှုကို တုံ့ပြန်သည်။ Rate limit သည် ခွင့်ပြုထားသည့် request ပမာဏ ကို ထိန်းချုပ်သည်။
- **လက်တွေ့:** provider timeout များ ထပ်ခါတလဲလဲ ဖြစ်ပြီးနောက် breaker ကို ဖွင့်ခြင်း၊ fail over လုပ်ခြင်း သို့မဟုတ် ထိန်းချုပ်ထားသည့် တုံ့ပြန်ချက် ပြန်ပေးခြင်း ပြုလုပ်ပြီး၊ cooldown ကာလ ပြီးနောက် အကန့်အသတ်ရှိသည့် ကျန်းမာရေး စမ်းသပ်မှုကို ခွင့်ပြုရမည်။
- **ဆက်စပ် term များ:** Retry with Backoff, Rate Limit, Model Router, Backpressure
- **English (source):** A reliability control that temporarily stops calls to a dependency after failures cross a threshold, then probes whether the dependency has recovered. It prevents repeated model or tool failures from consuming latency, budget, and capacity across the rest of the system.

### Coding Agent

**မြန်မာ:** ကုဒ် လုပ်ငန်းအတွက် အထူးပြုထားသည့် agent (Coding Agent)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** repository ကို စစ်ဆေးနိုင်ခြင်း၊ ဖိုင်များ တည်းဖြတ်နိုင်ခြင်း၊ development tool များ လုပ်ဆောင်နိုင်ခြင်း နှင့် ၎င်းတို့၏ output များကို အသုံးပြု၍ သတ်မှတ်ထားသည့် အင်ဂျင်နီယာ လုပ်ငန်းတစ်ခုကို တိုးတက်စေနိုင်ခြင်း စသည့် software လုပ်ငန်းအတွက် အထူးပြုထားသည့် agent ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်း၏ တန်ဖိုးသည် ကုဒ် ထုတ်လုပ်နိုင်သည့် အရည်အသွေးအပေါ်တွင်သာ မဟုတ်ဘဲ repository context၊ tool ခွင့်ပြုချက်များ၊ review နယ်နိမိတ်များ နှင့် verification အပေါ်တွင်လည်း မူတည်သည်။
- **မကြာခဏ ရောထွေးမှု:** စာသား အကြံပြုချက်သာ ပေးသည့် coding assistant သည် agent ဖြစ်ရန် မလိုအပ်ပါ။ agent သည် tool များမှတစ်ဆင့် လုပ်ဆောင်ပြီး ရလဒ်များကို စောင့်ကြည့်သည်။
- **လက်တွေ့:** agent အား issue တစ်ခု၊ scope contract တစ်ခု၊ repository လမ်းညွှန်ချက်များ နှင့် test command တစ်ခု ပေးပြီး၊ ထွက်ပေါ်လာသည့် patch နှင့် အထောက်အထားကို လက်ခံမီ review လုပ်ရမည်။
- **ဆက်စပ် term များ:** Agent Harness, Repository Map, Patch, Scope Contract, Reviewer Agent
- **Learn it:** [Skill Discovery and Progressive Disclosure](../phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure/)
- **English (source):** An agent specialized for software work that can inspect a repository, edit files, run development tools, and use their outputs to advance a scoped engineering task. Its value depends on repository context, tool permissions, review boundaries, and verification, not only code generation quality.

### Cost per Successful Task

**မြန်မာ:** အောင်မြင်သည့် လုပ်ငန်း တစ်ခုအလိုက် ကုန်ကျစရိတ် (Cost per Successful Task)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် အောင်မြင်မှု စံချိန်စံညွှန်းကို ဖြည့်ဆည်းသည့် လုပ်ငန်း အရေအတွက်ဖြင့် စုစုပေါင်း စနစ် ကုန်ကျစရိတ်ကို စားခြင်း ဖြစ်သည်။ ထိုတွင် retry များ၊ ကျရှုံးသည့် run များ၊ tool အသုံးပြုမှု နှင့် evaluation အတွက် အပိုကုန်ကျစရိတ်များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စျေးသက်သာသည့် မော်ဒယ် ခေါ်ဆိုမှုတစ်ခုသည် မကြာခဏ ကျရှုံးခြင်း သို့မဟုတ် လူဖြင့် ထပ်ခါတလဲလဲ ပြုပြင်ရခြင်း ဖြစ်ပါက ကုန်ကျစရိတ် ကြီးမားသည့် workflow တစ်ခု ဖြစ်လာနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Cost per token သည် အသုံးပြုမှုကို တိုင်းတာသည်။ Cost per successful task သည် အသုံးဝင်သည့် ရလဒ်များကို တိုင်းတာသည်။
- **လက်တွေ့:** provider ကောက်ခံငွေ နှင့် အခြေခံအဆောက်အအုံ ကုန်ကျစရိတ်ကို repository လုပ်ငန်း ၁၀၀ ခုတွင် တိုင်းတာပြီး၊ test နှင့် review အောင်မြင်သည့် patch အရေအတွက်ဖြင့် စားရမည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Retry with Backoff, Model Router, Verification Gate
- **English (source):** Total system cost divided by the number of tasks that satisfy a defined success criterion, including retries, failed runs, tool use, and evaluation overhead. A cheap model call can produce an expensive workflow if it fails often or requires repeated human correction.

### Flaky Test

**မြန်မာ:** မတည်ငြိမ်သည့် test (Flaky Test)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကုဒ် သို့မဟုတ် ရည်ရွယ်ထားသည့် test ပတ်ဝန်းကျင်တွင် သက်ဆိုင်သည့် ပြောင်းလဲမှု မရှိဘဲ တူညီသည့် run များတွင် အောင်နိုင်ခြင်း နှင့် ကျရှုံးခြင်း နှစ်မျိုးလုံး ဖြစ်နိုင်သည့် test ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Flakiness သည် verification gate များကို အားနည်းစေပြီး၊ တကယ့် ပျက်ကွက်မှုများကို လူများ သို့မဟုတ် agent များ လျစ်လျူရှုစေရန် သို့မဟုတ် မှားယွင်းသည့် အောင်မြင်မှု ရသည်အထိ ထပ်ခါတလဲလဲ လုပ်စေရန် လေ့ကျင့်ပေးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** ရံဖန်ရံခါ ပေါ်သည့် product bug ကို အမြဲတမ်း ဖော်ထုတ်ပြသည့် test သည် အဖိုးတန်သည့် အထောက်အထား ဖြစ်ပြီး၊ flaky test ဖြစ်ရန် မလိုအပ်ပါ။
- **လက်တွေ့:** ကျရှုံးသည့် seed နှင့် ပတ်ဝန်းကျင်ကို ထိန်းသိမ်းထားခြင်း၊ ပိုင်ရှင် နှင့် သတ်မှတ်ရက် ရှိမှသာ quarantine လုပ်ခြင်း ပြုလုပ်ပြီး၊ ထိန်းချုပ်မထားသည့် အချိန်၊ concurrency၊ network၊ အစဉ်လိုက်မှု သို့မဟုတ် shared state မှီခိုမှုများကို ပြုပြင်ရမည်။
- **ဆက်စပ် term များ:** Regression Test, Test Oracle, Retry with Backoff, Verification Gate
- **English (source):** A test that can pass and fail across equivalent runs without a relevant change to the code or intended test environment. Flakiness weakens verification gates and can train people or agents to ignore real failures or retry until they obtain a false pass.

### Handoff

**မြန်မာ:** လုပ်ငန်း လွှဲပြောင်းအပ်ခြင်း (Handoff)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လူများ သို့မဟုတ် agent များအကြား လုပ်ငန်းတစ်ခုကို ဖွဲ့စည်းပုံကျကျ လွှဲပြောင်းခြင်းဖြစ်ပြီး၊ ပန်းတိုင်၊ လက်ရှိ အခြေအနေ၊ အထောက်အထား၊ ဆုံးဖြတ်ချက်များ၊ ကန့်သတ်ချက်များ နှင့် ကျန်ရှိသည့် အလုပ်များကို ထိန်းသိမ်းပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ကောင်းမွန်သည့် handoff သည် နောက်လုပ်သူအား ရှည်လျားသည့် transcript တစ်ခုလုံးမှ လုပ်ငန်းတစ်ခုလုံးကို ပြန်လည် တည်ဆောက်ရခြင်း သို့မဟုတ် ပြီးစီးပြီးသား လုပ်ဆောင်မှုများကို ထပ်လုပ်ရခြင်းမှ ကာကွယ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Summary သည် မည်သည့် အရာ ဖြစ်ပွားခဲ့သည်ကို ဆိုသည်။ Handoff သည် မည်သည့် အခြေအနေက အခွင့်အာဏာ ရှိသည်နှင့် နောက်တွင် မည်သည့် အရာ လုပ်ရမည်ကို ထပ်မံ ဆိုသည်။
- **လက်တွေ့:** လက်ခံထားသည့် အစီအစဉ်၊ ပြောင်းလဲထားသည့် ဖိုင်များ၊ test command များ နှင့် ရလဒ်များ၊ မဖြေရှင်းရသေးသည့် အန္တရာယ်များ နှင့် နောက်တွင် လုပ်ဆောင်ရမည့် တိကျသည့် လုပ်ဆောင်ချက်ကို ကျစ်လျစ်သည့် task packet တစ်ခုအတွင်း လွှဲပြောင်းရမည်။
- **ဆက်စပ် term များ:** Agent State, Checkpoint, Scope Contract, Progressive Disclosure
- **Learn it:** [Multi-Session Handoff](../phases/14-agent-engineering/40-multi-session-handoff/)
- **English (source):** A structured transfer of a task between people or agents that preserves the objective, current state, evidence, decisions, constraints, and remaining work. A good handoff prevents the next worker from reconstructing the entire task from a long transcript or repeating completed actions.

### Idempotency

**မြန်မာ:** တူညီသည့် လုပ်ဆောင်ချက် ထပ်လုပ်လျှင် အကျိုးသက်ရောက်မှု မထပ်ခြင်း (Idempotency)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တူညီသည့် identity ဖြင့် တူညီသည့် လုပ်ဆောင်ချက်ကို ထပ်ခါတလဲလဲ လုပ်သည့်အခါ ပထမဆုံး အောင်မြင်စွာ လုပ်ဆောင်ပြီးသည့် အကျိုးသက်ရောက်မှုထက် ပို၍ ဘေးထွက် အကျိုးသက်ရောက်မှု မဖြစ်ပေါ်စေသည့် ဂုဏ်သတ္တိ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဖြန့်ကျက်ထားသည့် agent စနစ်များတွင် retry လုပ်ခြင်းသည် သာမန် ဖြစ်သည်။ Idempotency မရှိပါက မသေချာသည့် တုံ့ပြန်ချက် တစ်ခုသည် ငွေပေးချေမှု၊ comment၊ deployment သို့မဟုတ် record များကို ထပ်နှစ်ဆ ဖြစ်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Idempotency သည် တုံ့ပြန်ချက်တိုင်း byte တစ်လုံးမျှ မတူကွာခြားမှု မရှိရမည်ဟု မဆိုလိုပါ။ ရည်ရွယ်ထားသည့် အခြေအနေ ပြောင်းလဲမှု ထပ်နှစ်ဆ မဖြစ်ခြင်းကို ဆိုလိုသည်။
- **လက်တွေ့:** tool request တစ်ခုတွင် idempotency key တစ်ခု တွဲထည့်ပြီး၊ ပြီးစီးသည့် ရလဒ်ကို မှတ်တမ်းတင်ထားရမည်။ သို့မှသာ retry သည် ရေးသားမှုကို ထပ်လုပ်ခြင်းအစား ထိုရလဒ်ကို ပြန်ပေးမည် ဖြစ်သည်။
- **ဆက်စပ် term များ:** Retry with Backoff, Durable Execution, Checkpoint
- **English (source):** The property that repeating the same operation with the same identity does not create additional side effects beyond the first successful application. Retries are normal in distributed agent systems. Without idempotency, one uncertain response can duplicate payments, comments, deployments, or records.

### Model Router

**မြန်မာ:** မော်ဒယ် ရွေးချယ်ပေးသည့် component (Model Router)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** capability၊ latency၊ ကုန်ကျစရိတ်၊ context အရွယ်အစား၊ policy နှင့် လက်ရှိ ရရှိနိုင်မှု စသည့် လိုအပ်ချက်များကို အသုံးပြု၍ request တစ်ခုအတွက် မော်ဒယ် သို့မဟုတ် provider ကို ရွေးချယ်သည့် component ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မတူညီသည့် လုပ်ငန်းများ နှင့် ပျက်ကွက်မှု အခြေအနေများသည် မတူညီသည့် မော်ဒယ်များကို အသုံးပြုရန် အကြောင်းပြသည်။ routing သည် request တိုင်းကို အကြီးမားဆုံး ရွေးချယ်မှုသို့ ပို့ခြင်းမရှိဘဲ ရလဒ် အရည်အသွေးကို မြှင့်တင်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Routing သည် policy ဆုံးဖြတ်ချက် ဖြစ်သည်။ ကျပန်း load balancing သည် traffic ကို ခွဲဝေပေးရုံသာ ဖြစ်သည်။
- **လက်တွေ့:** အန္တရာယ် နည်းသည့် extraction ကို မြန်သည့် မော်ဒယ်သို့ ပို့ခြင်း၊ ရှုပ်ထွေးသည့် code review ကို ပိုအားကောင်းသည့် မော်ဒယ်သို့ ပို့ခြင်း ပြုလုပ်ပြီး၊ တူညီသည့် data policy ကို ဖြည့်ဆည်းသည့် provider များသို့သာ fail over လုပ်ရမည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Circuit Breaker, Rate Limit, Cost per Successful Task
- **English (source):** A component that selects a model or provider for a request using requirements such as capability, latency, cost, context size, policy, and current availability. Different tasks and failure conditions justify different models, and routing can improve outcome quality without sending every request to the largest option.

### Observability

**မြန်မာ:** စောင့်ကြည့် နားလည်နိုင်စွမ်း (Observability)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မှတ်တမ်းတင်ထားသည့် input၊ output၊ အခြေအနေ ပြောင်းလဲမှုများ၊ tool ခေါ်ဆိုမှုများ၊ အချိန်တိုင်းတာမှုများ၊ ကုန်ကျစရိတ်များ၊ error များ နှင့် evaluation အချက်ပြမှုများမှ AI စနစ်တစ်ခု၏ အပြုအမူကို နားလည်နိုင်သည့် စွမ်းရည် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** AI ပျက်ကွက်မှုများသည် မော်ဒယ်၊ retrieval၊ tool များ နှင့် orchestration ကို ဖြတ်ကျော် ဖြစ်ပွားတတ်သည်။ ပျက်ကွက်သည့် နယ်နိမိတ်ကို ရှာဖွေရန် ဆက်စပ်နေသည့် အထောက်အထား လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Logging သည် event များကို စုဆောင်းသည်။ Observability သည် ထို event များကို ဖွဲ့စည်းပုံကျပြီး အပြန်အလှန် ဆက်စပ်မှု ရှိစေကာ လုပ်ငန်း မေးခွန်းများကို ဖြေနိုင်အောင် ပြုလုပ်သည်။
- **လက်တွေ့:** retrieval၊ မော်ဒယ် ခေါ်ဆိုမှု၊ tool လုပ်ဆောင်မှု၊ ခွင့်ပြုချက်များ နှင့် နောက်ဆုံး အမှတ်ပေးခြင်း တစ်လျှောက် trace ID တစ်ခုကို မှတ်တမ်းတင်ပြီး၊ redaction နှင့် ဝင်ရောက်မှု ထိန်းချုပ်ချက်များကို ကျင့်သုံးရမည်။
- **ဆက်စပ် term များ:** Trace, Evaluation (Eval), Agent State, Time to First Token (TTFT)
- **Learn it:** [Agent Observability Platforms](../phases/14-agent-engineering/24-agent-observability-platforms/)
- **English (source):** The ability to understand an AI system's behavior from recorded inputs, outputs, state transitions, tool calls, timings, costs, errors, and evaluation signals. AI failures often span model, retrieval, tools, and orchestration. You need correlated evidence to locate the failing boundary.

### Patch

**မြန်မာ:** ဖိုင် ပြင်ဆင်မှု အစုအဝေး (Patch)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သိထားသည့် base revision တစ်ခုနှင့် နှိုင်းယှဉ်၍ ထည့်သည့် စာကြောင်းများ နှင့် ဖြတ်သည့် စာကြောင်းများအဖြစ် ဖော်ပြလေ့ရှိသည့်၊ ဖိုင်တစ်ခု သို့မဟုတ် တစ်ခုထက်ပိုသည့် ဖိုင်များသို့ ပြောင်းလဲမှုများကို review လုပ်နိုင်သည့် ပုံစံဖြင့် ဖော်ပြချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Patch သည် လူများ နှင့် agent များအား working directory တစ်ခုလုံးကို လက်ခံရမည့်အစား ကျဉ်းမြောင်းသည့် artifact တစ်ခုကို စစ်ဆေးခြင်း၊ test လုပ်ခြင်း၊ အသုံးချခြင်း သို့မဟုတ် ပယ်ချခြင်း ပြုလုပ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Patch သည် ဖိုင် ပြောင်းလဲမှုများကို ဖမ်းယူသည်၊ ၎င်းတို့ကို ဖြန့်ချိရန် လိုအပ်သည့် ကျိုးကြောင်းဆင်ခြင်မှု၊ test အထောက်အထား သို့မဟုတ် ခွင့်ပြုချက်ကို ဖမ်းယူခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** coding agent အား unified diff ပြန်ပေးရန် တောင်းဆိုပြီး၊ ၎င်းသည် ခွင့်ပြုထားသည့် ဖိုင်များကိုသာ ထိခြင်း ရှိ၊ မရှိ နှင့် မျှော်လင့်သည့် commit အပေါ် သန့်ရှင်းစွာ အသုံးချနိုင်ခြင်း ရှိ၊ မရှိ စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Worktree, Scope Contract, Regression Test
- **Learn it:** [Workbench for Real Repositories](../phases/14-agent-engineering/41-workbench-for-real-repos/)
- **English (source):** A reviewable representation of changes to one or more files, usually expressed as additions and deletions against a known base revision. A patch gives people and agents a narrow artifact to inspect, test, apply, or reject without accepting an entire working directory.

### Progressive Disclosure

**မြန်မာ:** အဆင့်လိုက် ဖော်ထုတ်ပေးခြင်း (Progressive Disclosure)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လူတစ်ဦး သို့မဟုတ် မော်ဒယ်တစ်ခုအား အနည်းဆုံး အသုံးဝင်သည့် context ကို အရင်ပေးပြီး၊ လုပ်ငန်း သို့မဟုတ် အထောက်အထား လိုအပ်လာသည့်အခါမှ ပိုမို နက်ရှိုင်းသည့် အသေးစိတ်ကို ဖော်ထုတ်ပေးခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် context ဆူညံမှု နှင့် ကုန်ကျစရိတ်ကို ကန့်သတ်ထားပြီး၊ ယုံကြည်ရသည့် အသေးစိတ်ကို လိုအပ်သည့်အခါ ရရှိနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Progressive disclosure သည် အသေးစိတ်သို့ အဆင့်လိုက် ဝင်ရောက်ခြင်း ဖြစ်သည်၊ ဆုံးဖြတ်ချက်အတွက် လိုအပ်သည့် အချက်အလက်ကို တမင်တကာ မပေးခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** coding agent အား repository စည်းမျဉ်းများ နှင့် map တစ်ခုကို အရင်ပေးပြီး၊ သက်ဆိုင်သည့် module ကို ဖော်ထုတ်ပြီးနောက်မှသာ implementation ဖိုင်များကို အပြည့်အစုံ load လုပ်ရမည်။
- **ဆက်စပ် term များ:** Context Engineering, Repository Map, Token Budget, Handoff
- **Learn it:** [Workbench for Real Repositories](../phases/14-agent-engineering/41-workbench-for-real-repos/)
- **English (source):** Supplying a person or model with the minimum useful context first, then revealing deeper detail when the task or evidence requires it. It limits context noise and cost while keeping authoritative detail available on demand.

### Rate Limit

**မြန်မာ:** နှုန်း ကန့်သတ်ချက် (Rate Limit)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် အချိန် သို့မဟုတ် capacity အပိုင်းအခြားအတွင်း request များ၊ token များ၊ တစ်ပြိုင်နက် လုပ်ဆောင်သည့် အလုပ်များ သို့မဟုတ် အခြား အရင်းအမြစ် တစ်ခုကို အများဆုံး ခွင့်ပြုသည့် policy ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် provider များ နှင့် မိမိ စနစ်ကို ဝန်ပိမှု၊ မထိန်းချုပ်နိုင်သည့် အသုံးစရိတ် နှင့် တရားမျှတမှု မရှိသည့် အရင်းအမြစ် အသုံးပြုမှုမှ ကာကွယ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Rate limit သည် ခွင့်ပြုထားသည့် အသုံးပြုမှုကို ထိန်းချုပ်သည်။ Backpressure သည် အောက်ပိုင်း capacity ကန့်သတ်ချက်များကို စနစ်တစ်လျှောက် ဖြန့်ဝေပေးသည်။
- **လက်တွေ့:** tenant တစ်ခုချင်းအလိုက် token နှင့် concurrency ကန့်သတ်ချက်များကို ကျင့်သုံးခြင်း၊ provider ၏ retry metadata ကို ဖတ်ခြင်း နှင့် ပိုလျှံသည့် အလုပ်ကို ကြိုတင်ခန့်မှန်းနိုင်သည့် ပုံစံဖြင့် တန်းစီခြင်း သို့မဟုတ် ပယ်ချခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Backpressure, Retry with Backoff, Circuit Breaker
- **English (source):** A policy that caps requests, tokens, concurrent work, or another resource within a defined time or capacity window. It protects providers and your own system from overload, uncontrolled spend, and unfair resource use.

### Regression Test

**မြန်မာ:** ပြန်ဖြစ်မှု ကာကွယ်သည့် test (Regression Test)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အလုပ်လုပ်ကြောင်း သိထားသည့် အပြုအမူကို ကာကွယ်ပေးသည့် ထပ်ခါတလဲလဲ လုပ်နိုင်သည့် စစ်ဆေးမှု ဖြစ်သည်။ အထူးသဖြင့် ကုဒ်၊ prompt၊ မော်ဒယ်၊ retrieval သို့မဟုတ် tool ပြောင်းလဲမှုများ ပြီးနောက်တွင် အရေးပါသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** AI စနစ် ပြောင်းလဲမှုများသည် ပျမ်းမျှ အရည်အသွေးကို မြှင့်တင်စဉ် အရင် ပြင်ပြီးသား ပျက်ကွက်မှုတစ်ခုကို တိတ်ဆိတ်စွာ ပြန်လည် ဖြစ်ပေါ်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Regression test သည် သတ်မှတ်ထားသည့် မျှော်လင့်အပြုအမူတစ်ခုကို ကာကွယ်သည်။ ကျယ်ပြန့်သည့် benchmark သည် ပိုမို ကျယ်သည့် လုပ်ငန်း ပြန့်ကျဲမှုအပေါ် စွမ်းဆောင်ရည်ကို ခန့်မှန်းသည်။
- **လက်တွေ့:** ပြုပြင်ပြီးသား prompt-injection ဖြစ်ရပ်တစ်ခုကို အမြဲတမ်း eval case အဖြစ် ပြောင်းလဲပြီး၊ နောက် deployment မတိုင်မီ ၎င်း အောင်ရမည် ဖြစ်သည်။
- **ဆက်စပ် term များ:** Eval Set, Verification Gate, Patch, Evaluation (Eval)
- **Learn it:** [Eval-Driven Agent Development](../phases/14-agent-engineering/30-eval-driven-agent-development/)
- **English (source):** A repeatable check that protects behavior known to work, especially after code, prompt, model, retrieval, or tool changes. AI system changes can improve average quality while silently reintroducing a previously fixed failure.

### Repository Instructions

**မြန်မာ:** repository လမ်းညွှန် စည်းမျဉ်းများ (Repository Instructions)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** coding agent များအား repository တစ်ခု မည်သို့ ဖွဲ့စည်းထားသည်၊ မည်သည့် command နှင့် စည်းမျဉ်းများ သက်ဆိုင်သည်၊ မည်သည့် နယ်နိမိတ်များကို လေးစားရမည် နှင့် အလုပ်ကို မည်သို့ စစ်ဆေးရမည် ကို ပြောပြသည့် version control ဖြင့် စီမံထားသည့် လမ်းညွှန်ချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ထပ်ခါတလဲလဲ နှုတ်ဖြင့် ပြောဆိုရသည့် အဖွဲ့အစည်း အတွင်းသိ အသိပညာကို ကုဒ်နှင့်အတူ လိုက်ပါပြီး ပရောဂျက် အခွဲအလိုက် ကွာခြားနိုင်သည့် local context အဖြစ် ပြောင်းလဲပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Repository instructions သည် source code နှင့် လူဖတ်သည့် documentation ကို ဖြည့်စွက်ပေးသည်၊ user ၏ လက်ရှိ တောင်းဆိုမှုကို ကျော်လွှားခြင်း သို့မဟုတ် agent များ လိုက်နာမည်ဟု အာမခံခြင်း မပြုပါ။
- **လက်တွေ့:** repository အမြစ်တွင် `AGENTS.md` ကို ထားရှိခြင်း၊ ခွဲထားသည့် directory များအတွက် ပိုကျဉ်းသည့် ဖိုင်များ ထပ်ထည့်ခြင်း ပြုလုပ်ပြီး၊ တိကျသည့် build၊ test၊ generated-file၊ security နှင့် contribution စည်းမျဉ်းများကို ထည့်သွင်းရမည်။
- **ဆက်စပ် term များ:** Repository Map, Scope Contract, Coding Agent, Progressive Disclosure
- **English (source):** Version-controlled guidance that tells coding agents how a repository is organized, which commands and conventions apply, what boundaries to respect, and how to verify work. It turns repeated tribal knowledge into local context that travels with the code and can vary by subproject.

### Repository Map

**မြန်မာ:** repository မြေပုံ (Repository Map)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** repository တစ်ခု၏ အရေးပါသည့် directory များ၊ ပိုင်ဆိုင်မှု နယ်နိမိတ်များ၊ entry point များ၊ build command များ၊ test များ၊ generated ဖိုင်များ နှင့် local လမ်းညွှန်ချက်များကို ကျစ်လျစ်စွာ ထိန်းသိမ်းထားသည့် ဖော်ပြချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် coding agent အား ကြီးမားသည့် ဖိုင်များ မဖွင့်မီ သို့မဟုတ် မှားသည့် subsystem ကို မတည်းဖြတ်မီ မှန်ကန်သည့် အထောက်အထားကို ရှာတွေ့နိုင်ရန် ကူညီသည်။
- **မကြာခဏ ရောထွေးမှု:** အကြမ်းဖျင်း ဖိုင် tree သည် အမည်များကို ပြသည်။ repository map သည် မည်သည့် path များ အရေးပါသည် နှင့် လုပ်ငန်းတစ်ခုနှင့် မည်သို့ ဆက်စပ်သည်ကို ရှင်းပြသည်။
- **လက်တွေ့:** tree နှင့် manifest များမှ index တစ်ခု ထုတ်လုပ်ပြီး၊ module နယ်နိမိတ်များ နှင့် validation command များအကြောင်း ယုံကြည်ရသည့် မှတ်စုများဖြင့် ဖြည့်စွက်ရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Progressive Disclosure, Scope Contract, Context Engineering
- **Learn it:** [Repository Memory and State](../phases/14-agent-engineering/34-repo-memory-and-state/)
- **English (source):** A compact, maintained description of a repository's important directories, ownership boundaries, entry points, build commands, tests, generated files, and local instructions. It helps a coding agent find the right evidence before loading large files or editing the wrong subsystem.

### Reproducible Build

**မြန်မာ:** ပြန်လည် ထုတ်လုပ်၍ ရသည့် build (Reproducible Build)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကြေညာထားသည့် source၊ ပတ်ဝန်းကျင် နှင့် လမ်းညွှန်ချက်များကို သီးခြားစီ ပြန်လည် လုပ်ဆောင်သည့်အခါ သတ်မှတ်ထားသည့် artifact များကို bit တစ်လုံးမျှ မကွာဘဲ တူညီစွာ ထုတ်လုပ်နိုင်သည့် build ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် artifact တစ်ခုကို မူလ ထုတ်လုပ်ခဲ့သည့် စက် သို့မဟုတ် agent ကို ကျော်လွန်၍ စစ်ဆေးနိုင်စေပြီး၊ ဖုံးကွယ်နေသည့် build input များကို ဖော်ထုတ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** နှစ်ကြိမ် အောင်မြင်သည့် build သည် ထပ်လုပ်နိုင်သည့် အထောက်အထား ဖြစ်သည်၊ သို့သော် reproducibility အတွက် ကြေညာထားသည့် သီးခြား အခြေအနေများ နှင့် တူညီသည့် output များ လိုအပ်သည်။
- **လက်တွေ့:** toolchain နှင့် dependency များကို pin လုပ်ခြင်း၊ timestamp နှင့် မတည်ငြိမ်သည့် အစဉ်လိုက်မှုများကို ဖယ်ရှားခြင်း၊ ပတ်ဝန်းကျင်ကို မှတ်တမ်းတင်ခြင်း ပြုလုပ်ပြီး၊ သီးခြားစီ ပြန်လည် ထုတ်လုပ်သည့် artifact digest များကို နှိုင်းယှဉ်ရမည်။
- **ဆက်စပ် term များ:** Repository Instructions, Verification Gate, Provenance Attestation, Software Bill of Materials (SBOM)
- **English (source):** A build whose declared source, environment, and instructions can be independently rerun to produce bit-for-bit identical specified artifacts. It makes an artifact verifiable beyond the machine or agent that originally produced it and exposes hidden build inputs.

### Retry with Backoff

**မြန်မာ:** ကြားချိန် တိုးမြှင့်၍ ပြန်လုပ်ခြင်း (Retry with Backoff)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ယာယီ ပျက်ကွက်သည့် လုပ်ဆောင်ချက်ကို တစ်ဆင့်ချင်း ပိုရှည်သည့် ကြားချိန်များဖြင့် ထပ်လုပ်ခြင်း ဖြစ်ပြီး၊ များသောအားဖြင့် ကျပန်း jitter နှင့် တင်းကျပ်သည့် retry အရေအတွက် ကန့်သတ်ချက် ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ချက်ချင်း တစ်ပြိုင်နက် ပြန်လုပ်သည့် retry များသည် ပျက်ယွင်းမှုကို ပို၍ ဆိုးစေနိုင်သည်၊ rate limit များကို ကုန်ဆုံးစေနိုင်သည် နှင့် ဘေးထွက် အကျိုးသက်ရောက်မှုများကို ထပ်နှစ်ဆ ဖြစ်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** အမြဲတမ်း ဖြစ်သည့် validation သို့မဟုတ် ခွင့်ပြုချက် error များကို ပြန်မလုပ်ရ၊ ထပ်နှစ်ဆ ဖြစ်မှု ကာကွယ်သည့် နည်းလမ်း မရှိဘဲ idempotency မရှိသည့် လုပ်ဆောင်ချက်များကို ပြန်မလုပ်ရ။
- **လက်တွေ့:** provider timeout တစ်ခုကို ကန့်သတ်ထားသည့် exponential ကြားချိန်များဖြင့် ပြန်လုပ်ခြင်း၊ server ၏ retry လမ်းညွှန်ချက်ကို လိုက်နာခြင်း နှင့် ရေးသားမှု တစ်ခုခုအတွက် idempotency key ကို ပြန်အသုံးပြုခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Idempotency, Rate Limit, Circuit Breaker, Backpressure
- **English (source):** Repeating a failed transient operation after progressively longer delays, usually with randomized jitter and a strict retry limit. Immediate synchronized retries can worsen an outage, consume rate limits, and duplicate side effects.

### Reviewer Agent

**မြန်မာ:** ပြန်လည် စစ်ဆေးသည့် agent (Reviewer Agent)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အခြား agent တစ်ခု၏ artifact သို့မဟုတ် ဆုံးဖြတ်ချက်ကို တိကျသည့် စံချိန်စံညွှန်းများအပေါ် စစ်ဆေးပြီး၊ တွေ့ရှိချက်များ သို့မဟုတ် အဆုံးအဖြတ်တစ်ခုကို ပြန်ပေးရန် တာဝန်ပေးထားသည့် agent ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အခန်းကဏ္ဍ ခွဲခြားထားခြင်းသည် ချန်လှပ်ထားမှုများကို ဖမ်းမိနိုင်သည်၊ သို့သော် reviewer သည် သီးခြားလွတ်လပ်သည့် အထောက်အထား နှင့် တိကျသည့် rubric ရရှိမှသာ အကျိုးရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** ဒုတိယ မော်ဒယ် ခေါ်ဆိုမှုတစ်ခုသည် အလိုအလျောက် လွတ်လပ်သည် သို့မဟုတ် မှန်ကန်သည် မဟုတ်ပါ။ မျှဝေထားသည့် context၊ မော်ဒယ်၏ bias နှင့် မပီပြင်သည့် စံချိန်စံညွှန်းများသည် တူညီသည့် အမှားကို ပြန်ဖြစ်စေနိုင်သည်။
- **လက်တွေ့:** agent တစ်ခုက patch တစ်ခု ထုတ်လုပ်ပြီးနောက်၊ သီးခြား reviewer တစ်ခုအား diff၊ scope contract၊ repository စည်းမျဉ်းများ နှင့် test output ပေးပြီး၊ စာကြောင်း တိကျသည့် တွေ့ရှိချက်များ တောင်းခံရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Verification Gate, Scope Contract, LLM-as-a-Judge
- **Learn it:** [Reviewer Agent](../phases/14-agent-engineering/39-reviewer-agent/)
- **English (source):** An agent assigned to inspect another agent's artifact or decision against explicit criteria and return findings or a verdict. Separation of roles can catch omissions, but it only helps when the reviewer receives independent evidence and a concrete rubric.

### Scope Contract

**မြန်မာ:** လုပ်ငန်း နယ်ပယ် သဘောတူညီချက် (Scope Contract)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လုပ်ငန်းတစ်ခု၏ ပန်းတိုင်၊ ခွင့်ပြုထားသည့် နှင့် တားမြစ်ထားသည့် မျက်နှာပြင်များ၊ မျှော်လင့်သည့် artifact များ၊ verification လိုအပ်ချက်များ နှင့် ရပ်တန့်မည့် အခြေအနေများကို သတ်မှတ်သည့် တိကျသည့် သဘောတူညီချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် agent အား ကျဉ်းမြောင်းသည့် ပြင်ဆင်မှုကို review မလုပ်နိုင်သည့် ပြန်လည် ဖွဲ့စည်းမှုအဖြစ် ပြောင်းလဲခြင်း သို့မဟုတ် အထောက်အထား မရှိဘဲ ပြီးစီးပြီဟု ဆိုခြင်းမှ ကာကွယ်သည်။
- **မကြာခဏ ရောထွေးမှု:** လုပ်ငန်း ဖော်ပြချက်သည် မည်သည့် အရာကို လိုချင်သည်ကို ဆိုသည်။ Scope contract သည် နယ်နိမိတ်များ နှင့် သက်သေကို ထပ်မံ သတ်မှတ်သည်။
- **လက်တွေ့:** parser module နှင့် ၎င်း၏ test များကိုသာ ပြောင်းလဲခွင့်ပြုခြင်း၊ public API များ ကိုက်ညီမှု ရှိရမည် နှင့် အမည်ဖော်ပြထားသည့် test suite အောင်ရမည် ဟု သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Patch, Verification Gate, Handoff
- **Learn it:** [Scope Contracts](../phases/14-agent-engineering/36-scope-contracts/)
- **English (source):** A concrete agreement that defines a task's goal, allowed and forbidden surfaces, expected artifacts, verification requirements, and stopping conditions. It prevents an agent from turning a narrow fix into an unreviewable refactor or from claiming completion without evidence.

### Semantic Cache

**မြန်မာ:** အဓိပ္ပာယ် နီးစပ်မှုအလိုက် cache (Semantic Cache)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရွေးချယ်ထားသည့် ကိုယ်စားပြုပုံစံ နှင့် ကန့်သတ်တန်ဖိုးတစ်ခုအောက်တွင် request အသစ်တစ်ခုကို လုံလောက်စွာ ဆင်တူသည်ဟု သတ်မှတ်သည့်အခါ ယခင် ရလဒ်ကို ပြန်လည် အသုံးပြုသည့် cache ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ထပ်ခါတလဲလဲ ရည်ရွယ်ချက်များအတွက် latency နှင့် ကုန်ကျစရိတ်ကို လျှော့ချနိုင်သည်၊ သို့သော် မှားယွင်းသည့် ကိုက်ညီမှုတစ်ခုသည် ခေတ်မမီတော့သည့် သို့မဟုတ် user အတွက် မသင့်လျော်သည့် output ကို ပြန်ပေးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Semantic similarity သည် request နှစ်ခုတွင် တူညီသည့် မှန်ကန်သည့် အဖြေ ရှိသည်ဟု အာမခံခြင်း မပြုပါ။ Semantic cache သည် ယခင် ရလဒ်ကို ပြန်အသုံးပြုသည်၊ prefix caching သည် တိကျသည့် token ၏ KV state ကို ပြန်အသုံးပြုသည်၊ prompt caching သည် provider သို့မဟုတ် application ၏ အရည်အချင်း စည်းမျဉ်းများကို လိုက်နာသည်။
- **လက်တွေ့:** အန္တရာယ် နည်းသည့် FAQ အဖြေများကို ပုံမှန်ပြုလုပ်ထားသည့် ရည်ရွယ်ချက်အလိုက် cache လုပ်ခြင်း၊ key တွင် tenant နှင့် policy version ကို ထည့်သွင်းခြင်း ပြုလုပ်ပြီး၊ ပုဂ္ဂိုလ်ရေး သို့မဟုတ် အချိန်နှင့် သက်ဆိုင်သည့် request များအတွက် cache ကို ကျော်လွှားရမည်။
- **ဆက်စပ် term များ:** Prompt Cache, Embedding, Cost per Successful Task, Grounding
- **English (source):** A cache that reuses a previous result when a new request is judged sufficiently similar under a chosen representation and threshold. It can reduce latency and cost for repeated intents, but an incorrect match can return stale or user-inappropriate output.

### Test Oracle

**မြန်မာ:** test အတွက် အမှန်စံ (Test Oracle)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စောင့်ကြည့်ရသည့် program အပြုအမူ မှန်ကန်ခြင်း ရှိ၊ မရှိ ဆုံးဖြတ်ရန် အသုံးပြုသည့် ယန္တရား၊ သတ်မှတ်ချက်၊ ရည်ညွှန်းမှု၊ invariant သို့မဟုတ် လူ၏ ဆုံးဖြတ်ချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** test input များ ထုတ်လုပ်နိုင်ခြင်းဖြင့် မလုံလောက်ပါ။ အလိုအလျောက် verification အတွက် ရလဒ်တစ်ခုချင်းစီကို အမျိုးအစားခွဲရန် လွတ်လပ်သည့် အခြေခံတစ်ခု လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** ကုဒ်ကို ရေးသည့် မော်ဒယ်ကို ၎င်း၏ ကိုယ်ပိုင် output မှန်ကန်သည်၊ မမှန်ကန် မေးခြင်းဖြင့် လွတ်လပ်သည့် oracle အဖြစ် သဘောထားရမည် မဟုတ်ပါ။
- **လက်တွေ့:** လုပ်ဆောင်နိုင်သည့် invariant များ၊ ရည်ညွှန်း implementation များ၊ schema များ နှင့် deterministic ဖြစ်သည့် မျှော်လင့် output များကို ဦးစားပေးအသုံးပြုပြီး၊ လူ၏ ဆုံးဖြတ်ချက် လိုအပ်နေသည့် နေရာများကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Regression Test, Verification Gate, Eval Set, Human-in-the-Loop (HITL)
- **English (source):** The mechanism, specification, reference, invariant, or human judgment used to decide whether observed program behavior is correct. Generating test inputs is not enough; automated verification requires an independent basis for classifying each result.

### Trace

**မြန်မာ:** ဆက်စပ် ခြေရာမှတ်တမ်း (Trace)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ် ခေါ်ဆိုမှုများ၊ retrieval၊ tool များ၊ အခြေအနေ ပြောင်းလဲမှုများ၊ retry များ၊ ခွင့်ပြုချက်များ နှင့် evaluation များ တစ်လျှောက် request တစ်ခု သို့မဟုတ် လုပ်ငန်းတစ်ခု၏ ဆက်စပ်နေသည့် မှတ်တမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** လုပ်ငန်းစဉ် တစ်ဆင့်ချင်းစီတွင် အချိန်၊ ကုန်ကျစရိတ် နှင့် ပျက်ကွက်မှု မည်သည့် နေရာမှ ဝင်ရောက်လာသည်ကို ပြန်လည် တည်ဆောက်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Trace သည် လုပ်ငန်း ဆိုင်ရာ အထောက်အထားကို မှတ်တမ်းတင်ရမည်၊ ဖုံးကွယ်ထားသည့် မော်ဒယ် ကျိုးကြောင်းဆင်ခြင်မှု၊ secret များ သို့မဟုတ် redact မလုပ်ရသေးသည့် အရေးပါသည့် အကြောင်းအရာများကို ဖော်ထုတ်ခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** agent harness တစ်လျှောက် trace identifier တစ်ခုကို ဖြန့်ဝေပြီး၊ မော်ဒယ် နှင့် tool လုပ်ဆောင်ချက် တစ်ခုချင်းစီအတွက် redact လုပ်ထားသည့် span များ တွဲထည့်ရမည်။
- **ဆက်စပ် term များ:** Observability, Agent State, Time to First Token (TTFT), Evaluation (Eval)
- **Learn it:** [OpenTelemetry GenAI Conventions](../phases/14-agent-engineering/23-otel-genai-conventions/)
- **English (source):** A correlated record of one request or task across model calls, retrieval, tools, state transitions, retries, approvals, and evaluations. It lets you reconstruct where time, cost, and failure entered a multi-step workflow.

### Worktree

**မြန်မာ:** Git worktree — သီးခြား working directory (Worktree)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Git တွင် repository တစ်ခု နှင့် branch သို့မဟုတ် commit တစ်ခုနှင့် ချိတ်ဆက်ထားသည့် working directory တစ်ခု ဖြစ်ပြီး၊ object storage ကို မျှဝေသုံးစွဲသော်လည်း ကိုယ်ပိုင် checked-out ဖိုင်များ နှင့် index ရှိသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** သီးခြား worktree များသည် လူများ နှင့် agent များအား checkout တစ်ခုတည်းကို ခဏခဏ လဲလှယ်ခြင်း သို့မဟုတ် ထပ်ရေးခြင်း မရှိဘဲ တစ်ပြိုင်နက် အလုပ်လုပ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** Worktree သည် checked-out ဖိုင်များကို သီးခြားခွဲခြားပေးသည်၊ စက်ပေါ်ရှိ process၊ port၊ cache၊ database သို့မဟုတ် secret တိုင်းကို သီးခြားခွဲခြားပေးခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** coding agent တစ်ခုချင်းစီအား အမည်ပေးထားသည့် feature branch နှင့် တိကျသည့် worktree path ပေးပြီး၊ ပုံမှန် Git history အတိုင်း patch များကို review လုပ်ပြီး ပေါင်းစည်းရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Patch, Scope Contract, Handoff
- **Learn it:** [Workbench for Real Repositories](../phases/14-agent-engineering/41-workbench-for-real-repos/)
- **English (source):** In Git, a working directory attached to a repository and branch or commit, with shared object storage but its own checked-out files and index. Separate worktrees let people and agents work concurrently without constantly switching or overwriting one checkout.

## Self-check

1. Backpressure နှင့် Circuit Breaker သည် မည်သည့် အချက်တွင် ကွာခြားသည်။
2. Coding agent တစ်ခု၏ တန်ဖိုးကို မော်ဒယ် အရည်အသွေး တစ်ခုတည်းဖြင့် အဘယ်ကြောင့် တိုင်းတာ၍ မရသနည်း။
3. Cost per successful task နှင့် cost per token သည် မည်သည့် အရာကို ကွာခြားစွာ တိုင်းတာသည်။
4. Idempotency မရှိဘဲ retry လုပ်ခြင်းသည် မည်သည့် အန္တရာယ် ဖြစ်စေနိုင်သည်၊ မည်သို့ ကာကွယ်ရမည်နည်း။
5. Reviewer agent တစ်ခု ထည့်သွင်းခြင်းဖြင့် အမှားများကို အမြဲ ဖမ်းမိနိုင်သည်ဟု အဘယ်ကြောင့် ဆို၍ မရသနည်း။

<details>
<summary>အဖြေများ</summary>

1. Backpressure သည် အောက်ပိုင်း component ၏ capacity ကန့်သတ်ချက်ကို အပေါ်ပိုင်းသို့ ဖြန့်ဝေပြီး၊
   ပျက်ကွက်မှု မဖြစ်မီတွင် ကာကွယ်သည်။ Circuit Breaker သည် dependency တစ်ခု ကျန်းမာမှု မရှိတော့ကြောင်း
   ပျက်ကွက်မှုများ ပေါ်ထွက်ပြီးမှ ခေါ်ဆိုမှုများကို ရပ်တန့်ပြီး၊ cooldown ကာလ ပြီးနောက်
   ကျန်းမာရေး စမ်းသပ်မှု ပြုလုပ်သည်။
2. ၎င်း၏ တန်ဖိုးသည် ကုဒ် ထုတ်လုပ်နိုင်မှုအပေါ်တွင်သာ မူတည်သည်မဟုတ်ဘဲ repository context၊
   tool ခွင့်ပြုချက်များ၊ review နယ်နိမိတ်များ နှင့် verification အပေါ်တွင်လည်း မူတည်သည်။
   ထို့ကြောင့် scope contract၊ test command နှင့် အထောက်အထား မပါဘဲ တိုင်းတာ၍ မရပါ။
3. Cost per token သည် အသုံးပြုမှု (usage) ကို တိုင်းတာသည်။ Cost per successful task သည်
   သတ်မှတ်ထားသည့် အောင်မြင်မှု စံကို ဖြည့်ဆည်းသည့် လုပ်ငန်း အရေအတွက်ဖြင့် စုစုပေါင်း ကုန်ကျစရိတ်ကို
   စားခြင်းဖြစ်ပြီး၊ retry၊ ကျရှုံးသည့် run နှင့် လူ၏ ပြုပြင်မှု အားလုံး ပါဝင်သည်။
4. Idempotency မရှိပါက မသေချာသည့် retry တစ်ခုသည် ငွေပေးချေမှု၊ comment၊ deployment သို့မဟုတ်
   record များကို ထပ်နှစ်ဆ ဖြစ်စေနိုင်သည်။ ကာကွယ်ရန် tool request တွင် idempotency key တွဲထည့်ပြီး
   ပြီးစီးသည့် ရလဒ်ကို မှတ်တမ်းတင်ထားသည်။ သို့မှသာ retry သည် ရေးသားမှုကို ထပ်လုပ်ခြင်းအစား
   ထိုရလဒ်ကို ပြန်ပေးသည်။
5. ဒုတိယ မော်ဒယ် ခေါ်ဆိုမှုတစ်ခုသည် အလိုအလျောက် လွတ်လပ်သည် သို့မဟုတ် မှန်ကန်သည် မဟုတ်ပါ။
   မျှဝေထားသည့် context၊ မော်ဒယ်၏ bias နှင့် မပီပြင်သည့် စံချိန်စံညွှန်းများသည် တူညီသည့် အမှားကို
   ပြန်ဖြစ်စေနိုင်သည်။ ထို့ကြောင့် reviewer သည် သီးခြားလွတ်လပ်သည့် အထောက်အထား နှင့်
   တိကျသည့် rubric ရရှိရန် လိုအပ်သည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository (MIT) — https://github.com/rohitg00/ai-engineering-from-scratch
- Course outline — `COURSE_OUTLINE.md` (area 08 — AI-native development, 23 term)

Source lesson လင့်များ —

- [Skill Discovery and Progressive Disclosure](../phases/13-tools-and-protocols/24-skill-discovery-and-progressive-disclosure/)
- [Multi-Session Handoff](../phases/14-agent-engineering/40-multi-session-handoff/)
- [Agent Observability Platforms](../phases/14-agent-engineering/24-agent-observability-platforms/)
- [Workbench for Real Repositories](../phases/14-agent-engineering/41-workbench-for-real-repos/)
- [Eval-Driven Agent Development](../phases/14-agent-engineering/30-eval-driven-agent-development/)
- [Repository Memory and State](../phases/14-agent-engineering/34-repo-memory-and-state/)
- [Reviewer Agent](../phases/14-agent-engineering/39-reviewer-agent/)
- [Scope Contracts](../phases/14-agent-engineering/36-scope-contracts/)
- [OpenTelemetry GenAI Conventions](../phases/14-agent-engineering/23-otel-genai-conventions/)

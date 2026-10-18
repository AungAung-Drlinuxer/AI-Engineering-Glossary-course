AI Engineering Glossary သင်တန်း၏ နယ်ပယ် ၀၇ — Evaluation & safety (အကဲဖြတ်တိုင်းတာခြင်းနှင့် ဘေးကင်းရေး) တွင် term ၁၇ ခု ပါဝင်သည်။ ဤနယ်ပယ်သည် စနစ်တစ်ခု၏ အပြုအမူကို တိုင်းတာခြင်း၊ တိုင်းတာမှု ရလဒ်များကို ယုံထိုက်မှု ရှိစေခြင်း၊ ပြောင်းလဲလာသည့် အခြေအနေများတွင် စွမ်းဆောင်ရည် ကျမသွားစေရန် စောင့်ကြည့်ခြင်းနှင့် တိုက်ခိုက်မှုများမှ ကာကွယ်ခြင်းတို့ကို ဖော်ပြသည်။

Evaluation နှင့် safety ကို သီးခြားမခွဲနိုင်သည်။ တိုင်းတာမှု မရှိပါက ဘေးကင်းရေးကို သက်သေပြရန် ခက်ခဲသည်၊ ဘေးကင်းရေး စဉ်းစားချက် မရှိပါက တိုင်းတာမှု ရလဒ်သည် ထုတ်လုပ်မှု အရည်အသွေးကို မဖော်ပြနိုင်သည်။ ဤ term များသည် တစ်ခုနှင့်တစ်ခု မှီခိုနေသည် — eval set မရှိဘဲ regression ကို မဖမ်းဆုပ်နိုင်သကဲ့သို့ guardrail မရှိဘဲ prompt injection ကို မကာကွယ်နိုင်ပါ။

Term တစ်ခုစီကို အောက်ပါ ပုံစံဖြင့် ဖော်ပြထားသည် — **မြန်မာ** တွင် အမည် သို့မဟုတ် အနီးစပ်ဆုံး ဖော်ပြချက်၊ **ဆိုလိုသည့် အဓိပ္ပာယ်** တွင် source ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ်၊ **အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်တွင် မည်သို့ သက်ရောက်သည်၊ **မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** တွင် source ဖော်ပြသည့် ကွာခြားချက်နှင့် လုပ်ဆောင်ရမည့် အချက်များ၊ **ဆက်စပ် term များ** တွင် ဆက်စပ် ဝေါဟာရများ၊ နောက်ဆုံးတွင် **English (source)** အနေဖြင့် source ၏ မူရင်း အင်္ဂလိပ် စာသား အတိအကျ ပါဝင်သည်။

### Alignment

**မြန်မာ:** ရည်မှန်းချက်၊ ကန့်သတ်ချက်နှင့် လူသား ဦးစားပေးချက်များနှင့် ကိုက်ညီအောင် ချိန်ညှိခြင်း (Alignment)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Model သို့မဟုတ် AI စနစ်တစ်ခုသည် မျှော်လင့်ထားသည့် အခြေအနေများတွင်ဖြစ်စေ၊ ရန်လိုသည့် (adversarial) အခြေအနေများတွင်ဖြစ်စေ ရည်ရွယ်သည့် ပန်းတိုင်၊ ကန့်သတ်ချက်နှင့် လူသား၏ ဦးစားပေးချက်များနှင့် ကိုက်ညီသည့် အပြုအမူ ပြသစေရန် ဆောင်ရွက်သည့် လုပ်ငန်းစဉ် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စနစ်တစ်ခုသည် သတ်မှတ်ထားသည့် metric ကို အကောင်းဆုံးဖြစ်အောင် လုပ်ဆောင်နေစဉ် အသုံးပြုသူ၏ အမှန်တကယ် ရည်ရွယ်ချက်ကို ချိုးဖောက်နိုင်သည်။ ထို့ကြောင့် alignment အတွက် evaluation၊ oversight နှင့် စနစ် ထိန်းချုပ်မှုများလည်း လိုအပ်သည်။
- **ဆက်စပ် term များ:** Guardrails, Evaluation (Eval), Human-in-the-Loop (HITL)
- **English (source):** The effort to make a model or AI system behave in ways that match intended goals, constraints, and human preferences across both expected and adversarial situations. A system can optimize the stated metric while violating the user's real intent, so alignment requires evaluation, oversight, and system controls as well as model training.

### Benchmark Contamination

**မြန်မာ:** စံညွှန်း တိုင်းတာမှုတွင် ညစ်ညမ်းမှု (Benchmark Contamination)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Evaluation အတွက် အသုံးပြုသည့် နမူနာများနှင့် တိုင်းတာခံ စနစ်ကို pretrain၊ tune၊ prompt၊ select သို့မဟုတ် အခြားနည်းဖြင့် ပိုမိုကောင်းမွန်စေရန် အသုံးပြုခဲ့သည့် data အကြား ထပ်နေမှု သို့မဟုတ် အချက်အလက် ယိုစိမ့်မှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Contamination ရှိပါက benchmark score သည် မမြင်ဖူးသေးသည့် အလုပ်များသို့ generalize လုပ်နိုင်စွမ်းကို မဖော်ပြဘဲ ယခင် ကြုံဖူးမှုကိုသာ ထင်ဟပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Contamination သည် အတိအကျ ကူးချခြင်းထက် ကျယ်ပြန့်သည်။ စကားပြန်ရေးချက်များ၊ အဖြေသော့များ၊ benchmark metadata နှင့် ထပ်တလဲလဲ prompt tuning လုပ်ခြင်းတို့သည်လည်း evaluation အချက်အလက်ကို ယိုစိမ့်စေနိုင်သည်။
- **လက်တွေ့:** Dataset ဇစ်မြစ်ကို ခြေရာခံခြင်း၊ training အရင်းအမြစ်များတွင် အတိအကျနှင့် အနီးစပ်ဆုံး ထပ်နေသည့် အရာများကို ရှာဖွေခြင်း၊ သီးသန့် test case များကို ချန်လှပ်ထားခြင်းနှင့် public eval များကို အသစ်ရေးသားသည့် နမူနာများဖြင့် အသစ်ပြန်လည် ပြုလုပ်ခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Data Leakage, Data Deduplication, Eval Set, Exact Match (EM)
- **English (source):** Overlap or information leakage between evaluation examples and data used to pretrain, tune, prompt, select, or otherwise improve the evaluated system. Contamination can make a benchmark score reflect prior exposure rather than the ability to generalize to unseen tasks.

### Calibration

**မြန်မာ:** ယုံကြည်မှုအဆင့် ချိန်ညှိမှု (Calibration)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စနစ်တစ်ခုက ဖော်ပြသည့် ယုံကြည်မှုအဆင့် (confidence) နှင့် ထို confidence အဆင့်ရှိ ခန့်မှန်းချက်များ အမှန်ဖြစ်သည့် လက်တွေ့ အကြိမ်အရေအတွက် (observed frequency) အကြား ကိုက်ညီမှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စနစ်တစ်ခုသည် ပျမ်းမျှအားဖြင့် တိကျနိုင်သော်လည်း လူများ ယင်း၏ score ကို မှီခိုသည့် အခြေအနေများတွင် အန္တရာယ်ရှိလောက်အောင် ယုံကြည်မှု လွန်ကဲနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Calibration သည် confidence ၏ ယုံထိုက်မှုကို တိုင်းတာသည့် အရာ ဖြစ်သည်၊ ခြုံငုံ တိကျမှု၊ factuality သို့မဟုတ် reasoning အရည်အသွေး မဟုတ်သည်။
- **လက်တွေ့:** ခန့်မှန်းချက်များကို confidence အဆင့်အလိုက် အုပ်စုဖွဲ့ခြင်း၊ confidence နှင့် လက်တွေ့ တိကျမှုကို နှိုင်းယှဉ်ခြင်း၊ ကွာဟမှု လက်မခံနိုင်လောက်ပါက recalibrate လုပ်ခြင်း သို့မဟုတ် အဖြေပေးခြင်းမှ ရှောင်ကြဉ်ခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Softmax, Evaluation (Eval), Precision & Recall, Logits
- **English (source):** The agreement between a system's stated confidence and the observed frequency with which predictions at that confidence are correct. A system can be accurate on average yet dangerously overconfident on the cases where people rely on its score.

### Distribution Shift

**မြန်မာ:** ဖြန့်ဖြူးမှု ပြောင်းလဲမှု (Distribution Shift)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စနစ်တစ်ခုကို တည်ဆောက်ရန် သို့မဟုတ် evaluate လုပ်ရန် အသုံးပြုသည့် data distribution နှင့် deploy လုပ်ပြီးနောက် ကြုံတွေ့ရသည့် distribution အကြား ကွာခြားမှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Model တစ်ခုသည် held-out test များကို အောင်နိုင်သော်လည်း အသုံးပြုသူ၊ အလုပ်၊ ဘာသာစကား၊ tool သို့မဟုတ် လည်ပတ်မှု အခြေအနေများ ပြောင်းလဲသည့်အခါ ကျရှုံးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Distribution shift သည် model drift အမြဲတမ်း မဟုတ်သည်။ Model သည် မပြောင်းလဲဘဲ ၎င်း၏ ပတ်ဝန်းကျင် သို့မဟုတ် အသုံးပြုသူအုပ်စု ပြောင်းလဲနိုင်သည်။
- **လက်တွေ့:** မျှော်လင့်ထားသည့် deployment slice များကို သတ်မှတ်ခြင်း၊ slice အလိုက် စွမ်းဆောင်ရည်နှင့် input လက္ခဏာများကို စောင့်ကြည့်ခြင်း၊ ကျရှုံးမှု အသစ်များကို version စီမံထားသည့် eval set ထဲသို့ ထည့်သွင်းခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Dataset Split, Eval Set, Overfitting, Model Card
- **English (source):** A difference between the data distribution used to build or evaluate a system and the distribution it encounters after deployment. A model can pass held-out tests yet fail when users, tasks, language, tools, or operating conditions change.

### Eval Set

**မြန်မာ:** စစ်ဆေးတိုင်းတာသည့် အစု (Eval Set)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် စွမ်းရည် သို့မဟုတ် အန္တရာယ်တစ်ခုနှင့် ဆန့်ကျင်စွာ AI စနစ်တစ်ခုကို တိုင်းတာရန် အသုံးပြုသည့် input များ၊ မျှော်လင့်ထားသည့် ဂုဏ်သတ္တိများ၊ scoring rule များနှင့် metadata တို့ကို စုစည်းထားသည့် version စီမံထားသော အစု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထပ်ခါတလဲလဲ အသုံးပြုနိုင်သည့် အစုတစ်ခုသည် မရေရာသည့် အရည်အသွေး အဆိုများကို နှိုင်းယှဉ်နိုင်သည့် အထောက်အထား အဖြစ် ပြောင်းလဲပေးပြီး prompt၊ model၊ tool သို့မဟုတ် retrieval ပြောင်းလဲပြီးနောက် regression များကို ဖမ်းဆုပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Development eval သည် ထပ်ခါတလဲလဲ ပြုပြင်တိုးတက်စေရန် လမ်းညွှန်သည်။ Final held-out test သည် ရွေးချယ်မှုများ သတ်မှတ်ပြီးနောက် စွမ်းဆောင်ရည်ကို ခန့်မှန်းသည်။ Standardized benchmark သည် မျှဝေထားသည့် protocol အောက်တွင် နှိုင်းယှဉ်မှုကို ပံ့ပိုးသည်။ Held-out set တစ်ခုခုကို ထပ်ခါတလဲလဲ ချိန်ညှိခြင်းသည် test အချက်အလက် ယိုစိမ့်စေပြီး ရလဒ်များကို ဖောင်းပွစေသည်။
- **လက်တွေ့:** ကိုယ်စားပြုနိုင်သည့် support မေးခွန်းများ၊ adversarial ညွှန်ကြားချက်များ၊ မျှော်လင့်ထားသည့် citation များနှင့် failure label များကို development နမူနာများနှင့် သီးခြားဖြစ်သည့်၊ ပြန်လည်စစ်ဆေးထားသည့် dataset တွင် ထိန်းသိမ်းရမည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Regression Test, LLM-as-a-Judge, Verification Gate
- **Learn it:** [Eval-Driven Agent Development](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/30-eval-driven-agent-development/)
- **English (source):** A versioned collection of inputs, expected properties, scoring rules, and metadata used to measure an AI system against a defined capability or risk. A repeatable set turns vague quality claims into comparable evidence and catches regressions after prompts, models, tools, or retrieval change.

### Evaluation (Eval)

**မြန်မာ:** အကဲဖြတ်တိုင်းတာခြင်း (Evaluation / Eval)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရှင်းလင်းသည့် အောင်မြင်မှု စံနှုန်းများ၊ data၊ scorer များနှင့် ပြန်လည်စစ်ဆေးသည့် လုပ်ထုံးလုပ်နည်းများကို အသုံးပြု၍ ကိုယ်စားပြုသည့် အလုပ်များတွင် model သို့မဟုတ် စနစ်၏ အပြုအမူကို တိုင်းတာသည့် သတ်မှတ်ထားသော လုပ်ငန်းစဉ် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** demo အနည်းငယ်မှ ပုဂ္ဂလဒိဋ္ဌိ ခံစားချက်ဖြင့်သာ အောင်မြင်မှုကို သတ်မှတ်ပါက ယုံကြည်စိတ်ချရမှုကို တိုးတက်စေနိုင်မည် မဟုတ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Benchmark score သည် evaluation ရလဒ် တစ်ခုသာ ဖြစ်သည်၊ production အရည်အသွေး၏ ပြည့်စုံသည့် ဖော်ပြချက် မဟုတ်သည်။
- **လက်တွေ့:** retrieval ပြောင်းလဲခြင်းမတိုင်မီနှင့် အပြီးတွင် အသုံးပြုသူ support scenario တူညီသည့် အစုကို run ခြင်း၊ မှန်ကန်မှုနှင့် citation ပံ့ပိုးမှုကို score ခြင်း၊ ကျရှုံးမှုများကို အမျိုးအစားအလိုက် စစ်ဆေးခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Eval Set, LLM-as-a-Judge, Cost per Successful Task, Regression Test
- **Learn it:** [LLM Evaluation](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/10-evaluation/)
- **English (source):** A defined process for measuring model or system behavior on representative tasks using explicit success criteria, data, scorers, and review procedures. You cannot improve reliability if success is only a subjective impression from a few demos.

### Exact Match (EM)

**မြန်မာ:** အတိအကျ ကိုက်ညီမှု (Exact Match / EM)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** output တစ်ခု၏ ပုံမှန်ပြုလုပ်ထားသည့် ပုံစံ (normalized representation) သည် လက်ခံထားသည့် အကိုးအကား အဖြေနှင့် အတိအကျ တူညီသည့်အခါတွင်သာ မှန်ကန်သည်ဟု ရေတွက်သည့် metric ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Canonical အဖြေ တစ်ခုတည်းရှိသည့် အလုပ်များအတွက် ၎င်းသည် deterministic ဖြစ်ပြီး audit လုပ်ရန် လွယ်ကူသည်၊ သို့သော် partial credit ကို ဖော်ပြခြင်း မရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** Exact-match score နည်းခြင်းသည် ထိခိုက်မှုမရှိသည့် format ကွာခြားမှုများကြောင့် ဖြစ်နိုင်သည်၊ အပြန်အလှန်အားဖြင့် string ကိုက်ညီခြင်းသည် အခြေအနေအတွင်း ပံ့ပိုးမှုမရှိခြင်း သို့မဟုတ် အန္တရာယ်မကင်းခြင်း ဖြစ်နိုင်သေးသည်။
- **လက်တွေ့:** Evaluation မတိုင်မီ normalization နှင့် လက်ခံသည့် အကိုးအကား အားလုံးကို သတ်မှတ်ခြင်း၊ output များစွာ မှန်ကန်နိုင်သည့်အခါ exact match ကို အလုပ်နှင့်ဆိုင်သည့် စစ်ဆေးမှုများနှင့် တွဲဖက်အသုံးပြုခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** ROUGE, Eval Set, Structured Output, Pass@k
- **English (source):** A metric that counts an output as correct only when its normalized representation exactly equals an accepted reference answer. It is deterministic and easy to audit for tasks with one canonical answer, but it exposes no partial credit.

### Guardrails

**မြန်မာ:** အကာအရံ ထိန်းချုပ်မှုများ (Guardrails)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** input များ၊ tool အသုံးပြုမှု၊ output များ၊ permission များနှင့် escalation တို့ကို ကန့်သတ်သည့် စနစ် ထိန်းချုပ်မှုများ ဖြစ်သည်။ ၎င်းတို့တွင် schema များ၊ policy စစ်ဆေးမှုများ၊ classifier များ၊ allowlist များ၊ sandboxing၊ approval များနှင့် လုပ်ဆောင်ပြီးနောက် စစ်ဆေးမှုများ ပါဝင်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မည်သည့် filter တစ်ခုတည်းမှ ကျရှုံးမှု ပုံစံ အားလုံးကို ဖုံးလွှမ်းနိုင်ခြင်း မရှိသည့်အတွက် အန္တရာယ်အလိုက် ထိန်းချုပ်မှုများကို အလွှာလိုက် စီစဉ်ရမည်။
- **မကြာခဏ ရောထွေးမှု:** Guardrails သည် အန္တရာယ်ကို လျှော့ချသည်၊ AI စနစ်တစ်ခု ဘေးကင်းသည်ဟု သက်သေပြခြင်း မဟုတ်သည်။
- **ဆက်စပ် term များ:** Least Privilege, Approval Gate, Sandbox, Evaluation (Eval)
- **Learn it:** [Guardrails](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/12-guardrails/)
- **English (source):** System controls that constrain inputs, tool use, outputs, permissions, and escalation. They can include schemas, policy checks, classifiers, allowlists, sandboxing, approvals, and post-action verification. No single filter covers all failure modes, so controls should be layered according to risk.

### Hallucination

**မြန်မာ:** အခြေအမြစ်မရှိသည့် လွဲမှားဖော်ပြချက် (Hallucination)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မှားယွင်းသည့်၊ ရရှိနိုင်သည့် အထောက်အထားဖြင့် ပံ့ပိုးမှုမရှိသည့် သို့မဟုတ် အလုပ်၏ အမှန်တရား အရင်းအမြစ်နှင့် ကိုက်ညီမှုမရှိသည့် ဖန်တီးထုတ်လုပ်သည့် အကြောင်းအရာ ဖြစ်သည်။ Output သည် ချောမွေ့ပြီး model သည် လှည့်ဖြားရန် မရည်ရွယ်သည့်အခါများတွင်ပင် ၎င်းသည် ပေါ်ပေါက်နိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဖော်ပြချက်တစ်ခုသည် training data တွင် ပါဝင်ခဲ့ခြင်း ရှိ မရှိကို ပုံမှန်အားဖြင့် စစ်ဆေးနိုင်ခြင်း မရှိသည့်အတွက် production စစ်ဆေးမှုများသည် ပံ့ပိုးမှု၊ မှန်ကန်မှုနှင့် ခြေရာခံနိုင်မှုတို့ကို အဓိကထားရမည်။
- **မကြာခဏ ရောထွေးမှု:** Hallucination သည် output အရည်အသွေး ကျရှုံးမှု ဖြစ်သည်၊ model ၏ ရည်ရွယ်ချက်ကို ရောဂါရှာဖွေတွေ့ရှိခြင်း မဟုတ်သည်။
- **လက်တွေ့:** အချက်အလက်ဆိုင်ရာ အဖြေများအတွက် citation ဖြင့် အထောက်အထား တောင်းဆိုခြင်း၊ citation တစ်ခုစီသည် ဆက်စပ်သည့် အဆိုကို အမှန်တကယ် ပံ့ပိုးခြင်း ရှိ မရှိ evaluate လုပ်ခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Grounding, RAG (Retrieval-Augmented Generation), Verification Gate
- **English (source):** Generated content that is false, unsupported by the available evidence, or inconsistent with the task's source of truth. It can arise even when the output is fluent and the model is not attempting to deceive. You usually cannot inspect whether a statement existed in training data, so production checks should focus on support, correctness, and traceability.

### Least Privilege

**မြန်မာ:** အနည်းဆုံး ခွင့်ပြုချက် (Least Privilege)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Model၊ agent၊ tool သို့မဟုတ် အသုံးပြုသူတစ်ဦးအား လက်ရှိ အလုပ်အတွက် လိုအပ်သည့် permission များကိုသာ၊ ထို permission များ လိုအပ်သည့် ကာလအတွက်သာ ပေးအပ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Model များသည် အမှားလုပ်မိနိုင်သည် သို့မဟုတ် အန္တရာယ်ရှိသည့် ညွှန်ကြားချက်များကို လိုက်နာမိနိုင်သည်။ ကျဉ်းမြောင်းသည့် permission များသည် တစ်ခုတည်းသော ကျရှုံးမှုတစ်ခုက ဖြစ်ပေါ်စေနိုင်သည့် ထိခိုက်မှုကို လျှော့ချသည်။
- **မကြာခဏ ရောထွေးမှု:** Authentication သည် အထောက်အထား (identity) ကို သက်သေပြသည်။ Least privilege သည် ထို identity က မည်သည့်အရာ လုပ်နိုင်သည်ကို ကန့်သတ်သည်။
- **လက်တွေ့:** Documentation agent တစ်ခုအား source file များအတွက် read access နှင့် branch တစ်ခုအတွက် write access ပေးအပ်သော်လည်း production credential သို့မဟုတ် merge permission ပေးအပ်ခြင်း မပြုရ။
- **ဆက်စပ် term များ:** Sandbox, Approval Gate, Prompt Injection, Tool Contract
- **English (source):** Giving a model, agent, tool, or user only the permissions required for the current task, for only as long as those permissions are needed. Models can make mistakes or follow malicious instructions. Narrow permissions reduce the damage any one failure can cause.

### LLM-as-a-Judge

**မြန်မာ:** LLM ဖြင့် အကဲဖြတ်သူ (LLM-as-a-Judge)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဘာသာစကား model တစ်ခုကို အသုံးပြု၍ အခြား စနစ်တစ်ခု၏ output ကို rubric တစ်ခုနှင့် ဆန့်ကျင်စွာ score ပေးခြင်း၊ နှိုင်းယှဉ်ခြင်း၊ အမျိုးအစားခွဲခြင်း သို့မဟုတ် ဝေဖန်ခြင်း ပြုလုပ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ရှင်းလင်းမှု သို့မဟုတ် ညွှန်ကြားချက် လိုက်နာမှုကဲ့သို့ exact-match test အဖြစ် ဖော်ပြရန် ခက်ခဲသည့် ဂုဏ်သတ္တိများကို evaluation ပြုလုပ်ခြင်းကို ၎င်းသည် scale ချပေးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Judge model သည် ground truth မဟုတ်သည်။ ၎င်းသည် အစဉ်လိုက်မှု၊ စကားလုံး များပြားမှု၊ စတိုင်၊ prompt အရေးအသား သို့မဟုတ် မျှဝေသည့် model ကျရှုံးမှုများကြောင့် bias ဖြစ်နိုင်သည်။
- **လက်တွေ့:** သီးခြား evaluator model တစ်ခုအား အလုပ်၊ လျာထားချက် အဖြေ၊ အကိုးအကား အထောက်အထားနှင့် ဖွဲ့စည်းထားသည့် rubric ပေးအပ်ပြီး ၎င်း၏ score များကို လူသား ပြန်လည်စစ်ဆေးထားသည့် နမူနာများနှင့် ချိန်ညှိရမည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Eval Set, Verification Gate, Precision & Recall
- **Learn it:** [Eval-Driven Agent Development](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/30-eval-driven-agent-development/)
- **English (source):** Using a language model to score, compare, classify, or critique another system's output against a rubric. It can scale evaluation of qualities that are difficult to express as exact-match tests, such as clarity or instruction adherence.

### Model Card

**မြန်မာ:** Model အချက်အလက် ကတ် (Model Card)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Model တစ်ခု၏ ရည်ရွယ်ထားသည့် အသုံးပြုမှုများ၊ evaluation အခြေအနေများ၊ စွမ်းဆောင်ရည် လက္ခဏာများ၊ ကန့်သတ်ချက်များနှင့် သက်ဆိုင်သည့် ကျင့်ဝတ် သို့မဟုတ် ဘေးကင်းရေး စဉ်းစားချက်များကို ဖော်ပြသည့် ဖွဲ့စည်းထားသော အစီရင်ခံစာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် အောက်ပိုင်း တည်ဆောက်သူများအား တင်ပြထားသည့် အထောက်အထားသည် ၎င်းတို့၏ အသုံးပြုသူများနှင့် deployment အခြေအနေများအတွက် သက်ဆိုင်ခြင်း ရှိ မရှိ ဆုံးဖြတ်ရန် အခြေခံအချက် ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Model card သည် အထောက်အထားနှင့် ကန့်သတ်ချက်များကို ဆက်သွယ်ဖော်ပြသည်၊ လက်မှတ်အတည်ပြုချက်၊ အာမခံချက်၊ စနစ် threat model သို့မဟုတ် deployment အလိုက် evaluation ၏ အစားထိုး မဟုတ်သည်။
- **လက်တွေ့:** Model version၊ training နှင့် evaluation နယ်ပယ်၊ အုပ်စုခွဲ ရလဒ်များ၊ သိရှိထားသည့် ကျရှုံးမှု ပုံစံများ၊ တားမြစ်ထားသည့် အသုံးပြုမှုများနှင့် အဆိုတစ်ခုစီ၏ ရက်စွဲကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Eval Set, Dataset Split, Distribution Shift, Alignment
- **English (source):** A structured report describing a model's intended uses, evaluation conditions, performance characteristics, limitations, and relevant ethical or safety considerations. It gives downstream builders context for deciding whether reported evidence applies to their users and deployment conditions.

### Pass@k

**မြန်မာ:** Pass@k (k ကြိမ် နမူနာယူခြင်းအတွင်း အောင်မြင်မှု အချိုးအစား)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အလုပ်အစုတစ်ခုအတွင်း k အကြိမ် နမူနာယူထားသည့် လျာထားချက်များထဲမှ အနည်းဆုံး တစ်ခုသည် သတ်မှတ်ထားသည့် မှန်ကန်မှု စစ်ဆေးမှုကို အောင်မြင်သည့် အလုပ်များ၏ အချိုးအစား ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** လျာထားချက်တစ်ခုစီကို အလိုအလျောက် စစ်ဆေးနိုင်သည့် verifier ရှိသည့် code ဖန်တီးခြင်းကဲ့သို့ အလုပ်များအတွက် အကြိမ်များစွာ နမူနာယူခြင်း၏ တန်ဖိုးကို ၎င်းသည် တိုင်းတာသည်။
- **မကြာခဏ ရောထွေးမှု:** Pass@k သည် တစ်ကြိမ်တည်း အောင်မြင်မှု တိကျမှု မဟုတ်သည်၊ ပိုမိုမြင့်မားသည့် score သည် ပိုမိုကောင်းမွန်သည့် ပထမဆုံး အဖြေကို မဆိုလိုဘဲ ပိုမိုကြီးမားသည့် attempt budget ကို ထင်ဟပ်နိုင်သည်။
- **လက်တွေ့:** သတ်မှတ်ထားသည့် configuration အောက်တွင် လျာထားချက်များကို သီးခြားစီ ဖန်တီးခြင်း၊ တစ်ခုစီအပေါ် တူညီသည့် သီးသန့် test များ run ခြင်း၊ sampling နှင့် estimator အသေးစိတ်နှင့်အတူ k ကို အစီရင်ခံခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Coding Agent, Regression Test, Eval Set, Test Oracle
- **English (source):** Across a task set, the fraction of tasks for which at least one of k sampled candidates passes a defined correctness test. It measures the value of sampling several attempts for tasks such as code generation where an automatic verifier can check each candidate.

### Precision & Recall

**မြန်မာ:** တိကျမှုနှင့် ဖမ်းယူနိုင်မှု (Precision & Recall)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** Precision သည် အမှတ်အသားပြုထားသည့် အရာများထဲမှ မည်မျှ မှန်ကန်သည်ကို မေးသည်။ Recall သည် သက်ဆိုင်သည့် အရာများထဲမှ မည်မျှ ရှာတွေ့သည်ကို မေးသည်။ သတ်မှတ်ထားသည့် scoring model တစ်ခုအတွက် ဆုံးဖြတ်ချက် threshold ကို ပြောင်းလဲသည့်အခါ recall တိုးတက်လာခြင်းသည် precision ကို မကြာခဏ လျှော့ချသည်၊ အပြန်အလှန်လည်း ဖြစ်သည်။ ပိုမိုကောင်းမွန်သည့် model သည် နှစ်ခုလုံးကို တိုးတက်စေနိုင်သည်။ F1 သည် ၎င်းတို့၏ harmonic mean ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Precision နှင့် recall သည် ဆန့်ကျင်ဘက် ဦးတည်ချက် ရှိသည့် metric နှစ်ခု ဖြစ်သည့်အတွက် တိုင်းတာမှုတွင် မည်သည့်အရာကို ဦးစားပေးသည်ကို ရှင်းလင်းစွာ သတ်မှတ်ရန် လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** မှန်ကန်သည့် threshold နှင့် metric သည် အမှား တစ်ခုစီ၏ ကုန်ကျစရိတ်နှင့် ပစ်မှတ် class ၏ အဖြစ်အများအပြားအပေါ် မူတည်သည်။
- **ဆက်စပ် term များ:** Eval Set, Semantic Search, Guardrails
- **English (source):** Precision asks how many flagged items were correct; recall asks how many relevant items were found. When you change the decision threshold for one fixed scoring model, improving recall often lowers precision and vice versa. A better model can improve both. F1 is their harmonic mean.

### Prompt Injection

**မြန်မာ:** Prompt ထည့်သွင်း တိုက်ခိုက်မှု (Prompt Injection)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ယုံကြည်စိတ်ချရခြင်း မရှိသည့် အကြောင်းအရာတစ်ခုက model အား ရည်ရွယ်ထားသည့် ညွှန်ကြားချက်များကို လျစ်လျူရှုစေခြင်း၊ data ကို ဖော်ထုတ်စေခြင်း၊ tool များကို အလွဲသုံးစေခြင်း သို့မဟုတ် အသုံးပြုသူ၏ ပန်းတိုင်အပြင်ဘက် လုပ်ဆောင်ချက်များ လုပ်ဆောင်စေခြင်းတို့ဖြင့် လွှမ်းမိုးသည့် တိုက်ခိုက်မှု သို့မဟုတ် ကျရှုံးမှု ပုံစံ ဖြစ်သည်။ ထို အကြောင်းအရာသည် အသုံးပြုသူထံမှ တိုက်ရိုက် သို့မဟုတ် retrieved page များ၊ file များ၊ message များ သို့မဟုတ် tool output မှတစ်ဆင့် သွယ်ဝိုက်၍ ရောက်ရှိနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** Model များသည် ညွှန်ကြားချက်များနှင့် data ကို တူညီသည့် ဘာသာစကား လမ်းကြောင်းဖြင့် လုပ်ဆောင်သည့်အတွက် input filtering တစ်ခုတည်းဖြင့် အန္တရာယ်ရှိသည့် ညွှန်ကြားချက် တစ်ခုစီကို တရားဝင် အကြောင်းအရာများနှင့် ယုံကြည်စိတ်ချစွာ ခွဲခြားနိုင်မည် မဟုတ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Prompt injection သည် SQL injection နှင့် နည်းပညာအရ တူညီသည့် လုပ်ငန်းစဉ် မဟုတ်သည်၊ ပိုမိုခိုင်မာသည့် system prompt သည်လည်း ပြည့်စုံသည့် ကာကွယ်မှု မဟုတ်သည်။
- **လက်တွေ့:** ပြင်ပ အကြောင်းအရာကို ယုံကြည်စိတ်ချရခြင်း မရှိသည့် အရာအဖြစ် သတ်မှတ်ခြင်း၊ ၎င်းကို အခွင့်အာဏာ သက်ရောက်သည့် ညွှန်ကြားချက်များနှင့် သီးခြားထားခြင်း၊ tool permission များကို အနည်းဆုံးဖြစ်စေခြင်း၊ အကျိုးသက်ရောက်မှုရှိသည့် ရေးသားမှုများအတွက် approval တောင်းခံခြင်းနှင့် output များနှင့် လုပ်ဆောင်ချက်များကို စစ်ဆေးခြင်း ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Least Privilege, Sandbox, Approval Gate, Tool Contract
- **Learn it:** [Prompt Injection Defense](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/27-prompt-injection-defense/)
- **English (source):** An attack or failure mode in which untrusted content influences a model to disregard intended instructions, expose data, misuse tools, or take actions outside the user's goal. The content can arrive directly from a user or indirectly through retrieved pages, files, messages, or tool output. Models process instructions and data through the same language channel, so input filtering alone cannot reliably separate every malicious instruction from legitimate content.

### ROUGE

**မြန်မာ:** ROUGE (အကိုးအကား ထပ်တူမှု တိုင်းတာသည့် metric အုပ်စု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** n-gram ထပ်တူမှု သို့မဟုတ် longest common subsequence ကဲ့သို့ အစိတ်အပိုင်းများကို အသုံးပြု၍ ဖန်တီးထားသည့် စာသားကို အကိုးအကား စာသားနှင့် နှိုင်းယှဉ်သည့် metric အုပ်စု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ROUGE သည် အနှစ်ချုပ် (summary) များအတွက် မကြာခဏ အသုံးပြုသည့် အကိုးအကား ထပ်တူမှု metric ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** မျက်နှာပြင်အဆင့် ထပ်တူမှုသည် အဓိပ္ပာယ် တူညီမှုကို လွတ်သွားနိုင်ပြီး အချက်အလက် အရည်အသွေးကို သက်သေမပြဘဲ ကူးချထားသည့် စကားလုံးများကို ဆုချနိုင်သည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Precision & Recall, LLM-as-a-Judge
- **English (source):** A family of metrics that compares generated text with reference text using units such as n-gram overlap or longest common subsequence.

### Verification Gate

**မြန်မာ:** စစ်ဆေးမှု ဂိတ် (Verification Gate)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် အထောက်အထားသည် မှန်ကန်မှု သို့မဟုတ် အရည်အသွေး စံနှုန်းတစ်ခုကို ဖြည့်ဆည်းသည်အထိ တိုးတက်မှုကို တားဆီးသည့် ထိန်းချုပ်မှု အမှတ် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် model ၏ ပြီးစီးပြီဟူသည့် အဆိုကို အထောက်အထား အခြေခံသည့် ဆုံးဖြတ်ချက် အဖြစ် ပြောင်းလဲပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Verification သည် အထောက်အထားသည် စံနှုန်းများနှင့် ကိုက်ညီခြင်း ရှိ မရှိ စစ်ဆေးသည်။ Approval သည် အထောက်အထားကို သိရှိပြီးဖြစ်သည့်အခါတွင်ပင် ဆက်လက်လုပ်ဆောင်ရန် အခွင့်အာဏာ ပေးအပ်သည်။
- **လက်တွေ့:** Patch သက်ရောက်ခြင်း၊ နယ်ပယ်သတ်မှတ်ထားသည့် test များ အောင်မြင်ခြင်း၊ တားမြစ်ထားသည့် file များ မပြောင်းလဲခြင်းနှင့် လိုအပ်သည့် artifact များ တည်ရှိခြင်း မပြီးမချင်း coding အလုပ်တစ်ခုကို ပြီးစီးခွင့် မပြုရ။
- **ဆက်စပ် term များ:** Approval Gate, Regression Test, Scope Contract, Structured Output
- **Learn it:** [Verification Gates](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/38-verification-gates/)
- **English (source):** A control point that blocks progress until defined evidence satisfies a correctness or quality criterion. It converts a model's claim of completion into an evidence-backed decision.

## Self-check

1. Evaluation နှင့် safety ကို အဘယ်ကြောင့် အတူတကွ လေ့လာရသနည်း။
2. Eval set နှင့် benchmark ကွာခြားချက်ကား အဘယ်နည်း။
3. Calibration နှင့် လုံးဝ တိကျမှု (overall accuracy) ကွာခြားချက်ကား အဘယ်နည်း။
4. Guardrails သည် ဘေးကင်းရေးကို သက်သေပြနိုင်သလား။
5. Verification gate နှင့် approval gate ကွာခြားချက်ကား အဘယ်နည်း။

<details>
<summary>အဖြေများ</summary>

1. တိုင်းတာမှု မရှိဘဲ ဘေးကင်းရေးကို သက်သေပြရန် ခက်ခဲသည့်အတွက်လည်းကောင်း၊ စနစ်တစ်ခုသည် သတ်မှတ် metric ကို အကောင်းဆုံးဖြစ်စေနေစဉ် အသုံးပြုသူ၏ ရည်ရွယ်ချက်ကို ချိုးဖောက်နိုင်သည့်အတွက်လည်းကောင်း နှစ်ခုကို အတူတကွ လေ့လာရသည်။ Alignment အတွက် evaluation၊ oversight နှင့် စနစ် ထိန်းချုပ်မှုများ လိုအပ်သည်။

2. Eval set သည် သတ်မှတ်ထားသည့် စွမ်းရည် သို့မဟုတ် အန္တရာယ်တစ်ခုအတွက် version စီမံထားသည့် input၊ မျှော်လင့်ချက်၊ scoring rule နှင့် metadata အစု ဖြစ်သည်။ Standardized benchmark သည် မျှဝေထားသည့် protocol အောက်တွင် နှိုင်းယှဉ်မှုကို ပံ့ပိုးသည်။ Held-out set တစ်ခုခုကို ထပ်ခါတလဲလဲ ချိန်ညှိခြင်းသည် test အချက်အလက် ယိုစိမ့်စေပြီး ရလဒ်ကို ဖောင်းပွစေသည်။

3. Calibration သည် ဖော်ပြသည့် confidence နှင့် ထို confidence အဆင့်ရှိ ခန့်မှန်းချက်များ အမှန်ဖြစ်သည့် အကြိမ်အရေအတွက် အကြား ကိုက်ညီမှုကို တိုင်းတာသည်။ ခြုံငုံ တိကျမှုကို မတိုင်းတာသည်။ စနစ်တစ်ခုသည် ပျမ်းမျှအားဖြင့် တိကျနိုင်သော်လည်း ယုံကြည်မှု လွန်ကဲနိုင်သည်။

4. မပြနိုင်သည်။ Guardrails သည် အန္တရာယ်ကို လျှော့ချသည့် စနစ် ထိန်းချုပ်မှုများ ဖြစ်သည်၊ AI စနစ်တစ်ခု ဘေးကင်းသည်ဟု သက်သေပြခြင်း မဟုတ်သည်။ မည်သည့် filter တစ်ခုတည်းမှ ကျရှုံးမှု ပုံစံ အားလုံးကို မဖုံးလွှမ်းနိုင်သည့်အတွက် ထိန်းချုပ်မှုများကို အလွှာလိုက် စီစဉ်ရမည်။

5. Verification သည် သတ်မှတ်ထားသည့် အထောက်အထားသည် မှန်ကန်မှု သို့မဟုတ် အရည်အသွေး စံနှုန်းကို ဖြည့်ဆည်းခြင်း ရှိ မရှိ စစ်ဆေးသည်။ Approval သည် အထောက်အထားကို သိရှိပြီးဖြစ်သည့်အခါတွင်ပင် ဆက်လက်လုပ်ဆောင်ရန် အခွင့်အာဏာ ပေးအပ်သည်။
</details>

## References

- Source glossary: https://aiengineeringfromscratch.com/glossary
- LLM Evaluation: ../phases/11-llm-engineering/10-evaluation/
- Guardrails: ../phases/11-llm-engineering/12-guardrails/
- Eval-Driven Agent Development: ../phases/14-agent-engineering/30-eval-driven-agent-development/
- Prompt Injection Defense: ../phases/14-agent-engineering/27-prompt-injection-defense/
- Verification Gates: ../phases/14-agent-engineering/38-verification-gates/
- Investigating Data Contamination in Modern Benchmarks for Large Language Models: https://arxiv.org/abs/2311.09783
- On Calibration of Modern Neural Networks: https://proceedings.mlr.press/v70/guo17a.html
- WILDS: https://proceedings.mlr.press/v139/koh21a.html
- SQuAD: https://aclanthology.org/D16-1264/
- Model Cards for Model Reporting: https://dl.acm.org/doi/10.1145/3287560.3287596
- Evaluating Large Language Models Trained on Code: https://arxiv.org/abs/2107.03374
- OWASP prompt injection guidance: https://genai.owasp.org/llmrisk/llm01-prompt-injection/


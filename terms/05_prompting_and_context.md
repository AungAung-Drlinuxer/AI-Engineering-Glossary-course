# 05 — Prompting & context

ဤစာစုသည် AI Engineering Glossary ၏ နယ်ပယ် 05 — Prompting & context အတွက် ဖြစ်သည်။ မော်ဒယ် တစ်ခု၏ ရလဒ်သည် မော်ဒယ်၏ weight များအပေါ်တွင်သာ မူတည်သည်သာ မဟုတ်ပါ။ inference တစ်ခုစီတွင် ၎င်းအား ပေးအပ်သည့် ညွှန်ကြားချက်များ၊ ဥပမာများ၊ အထောက်အထားများ၊ state နှင့် output ကန့်သတ်ချက်များအပေါ်တွင်လည်း မူတည်သည်။ ဤနယ်ပယ်တွင် ထို ညွှန်ကြားချက်နှင့် context ကို စီစဉ်ခြင်း၊ တောင်းဆိုခြင်း၊ ချုံ့ခြင်း၊ တိုင်းတာခြင်းနှင့် ကန့်သတ်ခြင်းအတွက် ဝေါဟာရ ၁၅ ခုကို စုစည်းထားသည်။

term များကို အစုအဝေး အနေဖြင့် ဖတ်နိုင်သည်။ Prompt Engineering၊ Zero-Shot၊ Few-Shot နှင့် Chain of Thought တို့သည် မော်ဒယ်အား မည်သို့ တောင်းဆိုမည်ကို ဖော်ပြသည်။ Context Window၊ Token Budget၊ Context Engineering နှင့် Context Compression တို့သည် ထို တောင်းဆိုမှုအတွက် ရရှိသည့် နေရာ အတိုင်းအတာနှင့် ရွေးချယ်မှုကို ဖော်ပြသည်။ Instruction Following၊ Instruction Hierarchy နှင့် System Prompt တို့သည် လိုက်နာမှုနှင့် အခွင့်အာဏာ နယ်နိမိတ်ကို ဖော်ပြသည်။ In-Context Learning၊ Prompt Sensitivity၊ Prompt Cache နှင့် Lost in the Middle တို့သည် လက်တွေ့ လုပ်ငန်းလည်ပတ်မှုတွင် တွေ့ရသည့် အပြုအမူ ပုံစံများနှင့် ကန့်သတ်ချက်များကို ဖော်ပြသည်။ ဤ term များကို သီးခြားစီ မဟုတ်ဘဲ တစ်ခုနှင့်တစ်ခု ဆက်စပ်နေသည့် စနစ် တစ်ခုအဖြစ် နားလည်မှသာ ယုံကြည်စိတ်ချရသည့် မော်ဒယ် အခြေပြု စနစ်များကို တည်ဆောက်နိုင်မည် ဖြစ်သည်။

Entry တစ်ခုကို ဖတ်သည့်အခါ မြန်မာ အမည်၊ ဆိုလိုသည့် အဓိပ္ပာယ်၊ အရေးပါသည့် အကြောင်းရင်း၊ မကြာခဏ ရောထွေးမှု၊ လက်တွေ့၊ ဆက်စပ် term များနှင့် လေ့လာရန် လင့်တို့ကို အစဉ်လိုက် ဖတ်ရမည်။ English (source) field တွင် မူရင်း အင်္ဂလိပ် စာသားကို တိုက်ရိုက် ထည့်သွင်းထားသည်။ Technical term (context window၊ prompt၊ system prompt၊ few-shot၊ retrieval၊ prompt injection၊ token budget စသည်) များကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိသည်။ source တွင် မပါသည့် field များ (ဥပမာ မကြာခဏ ရောထွေးမှု၊ လက်တွေ့၊ Learn it) ကို လုံးဝ ချန်လှပ်ထားသည်။

### Chain of Thought (CoT)

**မြန်မာ:** Chain of Thought (CoT) (ကျိုးကြောင်းဆင်ခြင်မှုကို အဆင့်လိုက် ဖော်ပြခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဖြေဆိုချက် မထုတ်လုပ်မီ task တစ်ခုကို အစိတ်အပိုင်းများ ခွဲခြမ်းရန် အသုံးပြုသည့် ကြားခံ ကျိုးကြောင်းဆင်ခြင်မှု ဖြစ်သည်။ prompt တစ်ခုသည် မြင်နိုင်သည့် rationale ကို တောင်းဆိုနိုင်ပြီး စနစ် အချို့သည် အသုံးပြုသူထံ ပြန်လည် မပေးအပ်သည့် internal reasoning ကို အသုံးပြုသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အဆင့်များစွာ ပါဝင်သည့် task များတွင် decomposition သည် အထောက်အကူ ဖြစ်နိုင်သည်၊ သို့သော် ချောမွေ့သည့် rationale တစ်ခုသည် ဖြေဆိုချက် မှန်ကန်ကြောင်း သို့မဟုတ် ထို စာသားသည် မော်ဒယ်၏ အတွင်းပိုင်း တွက်ချက်မှုကို သစ္စာရှိစွာ ကိုယ်စားပြုကြောင်း သက်သေ မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** Chain of thought သည် tool များ၊ test များ သို့မဟုတ် ပြင်ပ စစ်ဆေးမှုအတွက် အစားထိုး တစ်ခု မဟုတ်ပါ။
- **လက်တွေ့:** ကျစ်လျစ်သည့် အစီအစဉ် တစ်ခု တောင်းခံရမည်၊ ရလဒ်ကို သီးခြားစီ စစ်ဆေးရမည်၊ ရှည်လျားသည့် reasoning transcript အပေါ် မှီခိုခြင်းအစား စစ်ဆေးနိုင်သည့် တွက်ချက်မှုများ သို့မဟုတ် ကိုးကားချက်များကို တောင်းဆိုရမည်။
- **ဆက်စပ် term များ:** Prompt Engineering, Verification Gate, Evaluation (Eval)
- **Learn it:** [Few-Shot and Chain of Thought](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/02-few-shot-cot/)
- **English (source):** Intermediate reasoning used to decompose a task before producing an answer. A prompt can request a visible rationale, while some systems use internal reasoning that is not returned to the user. Decomposition can help on multi-step tasks, but a fluent rationale is not proof that the answer is correct or that the text faithfully represents the model's internal computation.

### Context Compression

**မြန်မာ:** Context Compression (context ၏ token ပမာဏကို ချုံ့ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** နောက်ပိုင်း မော်ဒယ် ဆုံးဖြတ်ချက် တစ်ခုအတွက် လိုအပ်သည့် အချက်အလက်ကို ထိန်းသိမ်းရန် ကြိုးစားရင်း ရင်းမြစ် အကြောင်းအရာ၏ token ပမာဏကို လျှော့ချခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ချုံ့ခြင်းသည် ရှည်လျားသည့် task များကို budget အတွင်း ထည့်သွင်းနိုင်စေသည်၊ သို့သော် ချန်လှပ်လိုက်သည့် အသေးစိတ် တိုင်းသည် မော်ဒယ်တွင် အထောက်အထား၊ ကန့်သတ်ချက် သို့မဟုတ် မဖြေရှင်းရသေးသည့် state များ ဆုံးရှုံးနိုင်သည့် အန္တရာယ်ကို ဖန်တီးသည်။
- **မကြာခဏ ရောထွေးမှု:** မူရင်း အပြည့်အစုံကို ထိန်းသိမ်းထားခြင်း မရှိပါက ချုံ့ခြင်းသည် lossy ဖြစ်သည်။ ပိုတိုသည့် summary တစ်ခုသည် အလိုအလျောက် ညီမျှသည့် context မဟုတ်ပါ။
- **လက်တွေ့:** အတည်ပြုပြီး အချက်အလက်များနှင့် identifier များကို စာလုံးတိုင်း ထိန်းသိမ်းရမည်၊ ထပ်နေသည့် မှတ်တမ်းကို အနှစ်ချုပ်ရမည်၊ source ညွှန်းချက်များကို တွဲဖက်ရမည်၊ ချုံ့ထားသည့် context ကို ကိုယ်စားပြုသည့် task များတွင် စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Token Budget, Context Engineering, Progressive Disclosure, Handoff
- **English (source):** Reducing the token footprint of source material while attempting to preserve the information required for a later model decision. Compression can make long tasks fit within budget, but every omitted detail creates a risk that the model loses evidence, constraints, or unresolved state.

### Context Engineering

**မြန်မာ:** Context Engineering (မော်ဒယ်သို့ ပေးအပ်သည့် အချက်အလက် ပတ်ဝန်းကျင်ကို ဖွဲ့စည်းခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ညွှန်ကြားချက်များ၊ ရွေးချယ်ထားသည့် file များ၊ ရယူထားသည့် အထောက်အထားများ၊ tool ရလဒ်များ၊ ဥပမာများ၊ state နှင့် output ကန့်သတ်ချက်များ အပါအဝင် အဆင့်တိုင်းတွင် မော်ဒယ်အား ပေးအပ်သည့် အချက်အလက် ပတ်ဝန်းကျင် အပြည့်အစုံကို စီစဉ် ဖွဲ့စည်းခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** သက်ဆိုင်သည့် အထောက်အထားများ ပျောက်ဆုံးခြင်း၊ ခေတ်မမီတော့ခြင်း၊ အစဉ်လွဲနေခြင်း သို့မဟုတ် ဆူညံသံများဖြင့် ဖုံးလွှမ်းခံရခြင်းတို့ကြောင့် မော်ဒယ် စွမ်းဆောင်ရည် မကြာခဏ ကျရှုံးသည်။
- **မကြာခဏ ရောထွေးမှု:** Prompt engineering သည် ညွှန်ကြားချက်၏ စကားလုံး ရွေးချယ်မှုကို အာရုံစိုက်သည်။ Context engineering သည် မည်သည့် အထောက်အထားနှင့် state များ မော်ဒယ်၏ working context ထဲသို့ ဝင်ရောက်မည်ကိုလည်း ဆုံးဖြတ်သည်။
- **လက်တွေ့:** ပန်းတိုင်၊ repository စည်းမျဉ်းများ၊ သက်ဆိုင်သည့် interface များ၊ လတ်တလော tool output နှင့် မဖြေရှင်းရသေးသည့် ဆုံးဖြတ်ချက်များ ပါဝင်သည့် ကျစ်လျစ်သည့် task packet တစ်ခုကို တည်ဆောက်ရမည်၊ ထို့နောက် state ပြောင်းလဲသည့်အခါ ၎င်းကို update လုပ်ရမည်။
- **ဆက်စပ် term များ:** Context Window, Progressive Disclosure, Agent State, Repository Map
- **Learn it:** [Context Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/05-context-engineering/)
- **English (source):** Designing the full information environment supplied to a model at each step, including instructions, selected files, retrieved evidence, tool results, examples, state, and output constraints. Model performance often fails because relevant evidence is missing, stale, badly ordered, or overwhelmed by noise.

### Context Window

**မြန်မာ:** Context Window (inference တစ်ခုအတွက် ရရှိသည့် token နေရာ အတိုင်းအတာ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တိကျသည့် မော်ဒယ်နှင့် API contract တစ်ခုအောက်တွင် မော်ဒယ် inference တစ်ခုအတွက် ရရှိနိုင်သည့် အများဆုံး token ပမာဏ ဖြစ်သည်။ ထို ပမာဏတွင် system ညွှန်ကြားချက်များ၊ message များ၊ ရယူထားသည့် အကြောင်းအရာ၊ tool ဖလှယ်မှုများနှင့် ထုတ်လုပ်သည့် output တို့ ပါဝင်နိုင်ပြီး provider အလိုက် တွက်ချက်မှုနှင့် output ကန့်သတ်ချက်များ ကွာခြားသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စကားဝိုင်း မှတ်တမ်းသည် application က ၎င်းကို ပေးပို့သည့်အခါ သို့မဟုတ် ပြန်လည် တည်ဆောက်သည့်အခါမှသာ ရရှိသည်။ window ကြီးသည့်တိုင် ထည့်သွင်းထားသည့် အသေးစိတ် တိုင်းကို ယုံကြည်စိတ်ချစွာ အသုံးပြုမည်ဟု အာမခံခြင်း မပြုပါ။
- **မကြာခဏ ရောထွေးမှု:** Context သည် inference တစ်ခုအတွက် ယာယီ input ဖြစ်သည်။ ခံတည်သည့် memory ကို မော်ဒယ်၏ အပြင်ဘက်တွင် သိမ်းဆည်းပြီး နောက်ပိုင်း context ထဲသို့ ရွေးချယ် ပြန်လည် ထည့်သွင်းသည်။
- **ဆက်စပ် term များ:** Token Budget, Context Engineering, Prompt Cache, Agent State
- **Learn it:** [Context Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/05-context-engineering/)
- **English (source):** The maximum token capacity available to one model inference under a specific model and API contract. The capacity may include system instructions, messages, retrieved content, tool exchanges, and generated output, with provider-specific accounting and output limits. Conversation history is only available when the application sends or reconstructs it. A large window does not guarantee that every included detail will be used reliably.

### Few-Shot

**မြန်မာ:** Few-Shot (ဥပမာ အနည်းငယ် ပေးအပ်သည့် နည်းလမ်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်သည် လိုလားသည့် task၊ format သို့မဟုတ် ဆုံးဖြတ်ချက် နယ်နိမိတ်ကို ကောက်ချက်ချနိုင်ရန် ပစ်မှတ် input မတိုင်မီ ဥပမာ အနည်းငယ်ကို ထည့်သွင်းသည့် in-context learning ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဥပမာ အရေအတွက် တစ်သမတ်တည်း ထက် ဥပမာ၏ အရည်အသွေးနှင့် လွှမ်းခြုံမှုက ပို၍ အရေးပါသည်။ ညံ့ဖျင်းသည့် သို့မဟုတ် ဆန့်ကျင်နေသည့် demonstration များသည် ယုံကြည်စိတ်ချရမှုကို လျှော့ချနိုင်သည်။
- **ဆက်စပ် term များ:** Zero-Shot, In-Context Learning, Prompt Engineering, Context Window
- **English (source):** In-context learning that includes a small set of demonstrations before the target input so the model can infer the desired task, format, or decision boundary. Example quality and coverage matter more than a universal example count. Poor or contradictory demonstrations can reduce reliability.

### In-Context Learning

**မြန်မာ:** In-Context Learning (context အတွင်းမှ လိုက်လျောညီထွေ သင်ယူခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သာမန် parameter update မပြုဘဲ လက်ရှိ input တွင် ပေးအပ်ထားသည့် ညွှန်ကြားချက်များ၊ ဥပမာများ သို့မဟုတ် ပုံစံများမှ မော်ဒယ်တစ်ခု မိမိ၏ အပြုအမူကို လိုက်လျောညီထွေ ပြောင်းလဲခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ကြိုတင် လေ့ကျင့်ထားသည့် မော်ဒယ် တစ်ခုသည် ၎င်း၏ weight များကို မပြောင်းလဲဘဲ context မှ task အသစ် တစ်ခုကို မည်သို့ လုပ်ဆောင်နိုင်သည်ကို ၎င်းက ရှင်းလင်းစေသည်။
- **မကြာခဏ ရောထွေးမှု:** In-context learning သည် ယာယီ conditioning ဖြစ်ပြီး fine-tuning၊ ခံတည်သည့် memory သို့မဟုတ် မော်ဒယ်သည် ရည်ရွယ်သည့် စည်းမျဉ်းကို ကောက်ချက်ချခဲ့သည့် သက်သေ မဟုတ်ပါ။
- **လက်တွေ့:** ကိုယ်စားပြုသည့် demonstration များကို ပစ်မှတ် input မတိုင်မီ ထားရမည်၊ အစဉ်နှင့် format မူကွဲများကို စမ်းသပ်ရမည်၊ အကဲဖြတ်သည့် ဥပမာများကို demonstration များနှင့် သီးခြားခွဲထားရမည်။
- **ဆက်စပ် term များ:** Few-Shot, Zero-Shot, Context Window, Prompt Engineering
- **English (source):** A model adapting its behavior from instructions, examples, or patterns supplied in the current input without an ordinary parameter update. It explains how one pretrained model can perform a new task from context while keeping its weights unchanged.

### Instruction Following

**မြန်မာ:** Instruction Following (ညွှန်ကြားချက်ကို လိုက်နာနိုင်စွမ်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဖော်ပြထားသည့် task နှင့် ကန့်သတ်ချက်များကို ပြည့်မီသည့် အပြုအမူသို့ သဘာဝဘာသာ ညွှန်ကြားချက်များနှင့် ပေးအပ်ထားသည့် context ကို ချိတ်ဆက်ပေးသည့် မော်ဒယ် စွမ်းရည် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဘာသာစကား ထုတ်လုပ်ခြင်းသည် အသုံးပြုသူ တောင်းဆိုသည့် လုပ်ဆောင်ချက်၊ format၊ နယ်နိမိတ် သို့မဟုတ် ဦးစားပေး အစဉ်ကို မလိုက်နာဘဲ ချောမွေ့နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Instruction following သည် အချက်အလက် မှန်ကန်မှု၊ alignment သို့မဟုတ် ညွှန်ကြားချက် ဟု ထင်ရသည့် စာသား တိုင်းကို လိုက်နာခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** ဆန့်ကျင်နေသည့် ကန့်သတ်ချက်များ၊ format လိုအပ်ချက်များ၊ မသက်ဆိုင်သည့် context နှင့် ငြင်းပယ်သည့် အမှုများကို အသုံးပြု၍ ညွှန်ကြားချက် လိုက်နာမှုကို ဖြေဆိုချက် အရည်အသွေးနှင့် သီးခြားစီ အကဲဖြတ်ရမည်။
- **ဆက်စပ် term များ:** SFT (Supervised Fine-Tuning), Prompt Engineering, Instruction Hierarchy, Alignment
- **English (source):** A model capability to map natural-language directions and supplied context to behavior that satisfies the stated task and constraints. Language generation can be fluent without obeying the user's requested operation, format, boundaries, or priorities.

### Instruction Hierarchy

**မြန်မာ:** Instruction Hierarchy (ညွှန်ကြားချက်များ၏ အခွင့်အာဏာ အဆင့်လိုက် အစဉ်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** application policy၊ အသုံးပြုသူများနှင့် မယုံကြည်ရသည့် ရယူထားသည့် အကြောင်းအရာ ကဲ့သို့ အခွင့်အာဏာ မတူညီသည့် ရင်းမြစ်များမှ ညွှန်ကြားချက်များကြား ပဋိပက္ခများကို ဖြေရှင်းသည့် စည်းမျဉ်း အစု တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** agent စနစ်များသည် ယုံကြည်ရသည့် ပန်းတိုင်များနှင့် ပြင်ပ စာသားများကို ရောနှောထားသောကြောင့် အခွင့်အာဏာ နည်းသည့် အကြောင်းအရာသည် အခွင့်အာဏာ မြင့်သည့် ကန့်သတ်ချက်များနှင့် ပဋိပက္ခဖြစ်သည့်အခါ မော်ဒယ်နှင့် harness သည် တိကျသည့် တုံ့ပြန်မှု တစ်ခုကို လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Instruction hierarchy သည် အပြုအမူကို တိုးတက်စေနိုင်သည်၊ သို့သော် လုံခြုံရေး နယ်နိမိတ် တစ်ခု မဟုတ်ပါ။ least privilege နှင့် အတည်ပြုချက် ထိန်းချုပ်မှုများက အကျိုးဆက်များကို ကန့်သတ်ဆဲ ဖြစ်သည်။
- **လက်တွေ့:** မယုံကြည်ရသည့် tool output ကို data အနေဖြင့် အမှတ်အသားပြုရမည်၊ ထို အကြောင်းအရာ၏ အပြင်ဘက်တွင် ဦးစားပေး မြင့်သည့် ကန့်သတ်ချက်များကို ထိန်းသိမ်းရမည်၊ တိုက်ရိုက်နှင့် သွယ်ဝိုက်သည့် ပဋိပက္ခ အမှုများကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** System Prompt, Prompt Injection, Least Privilege, Tool Contract
- **English (source):** A rule set for resolving conflicts among instructions from sources with different authority, such as application policy, users, and untrusted retrieved content. Agent systems mix trusted goals with external text, so the model and harness need a defined response when lower-authority content conflicts with higher-authority constraints.

### Lost in the Middle

**မြန်မာ:** Lost in the Middle (အလယ်ပိုင်းတွင် အထောက်အထား ပျောက်ဆုံးသည့် ပုံစံ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အထောက်အထား၏ တည်နေရာအလိုက် မော်ဒယ် စွမ်းဆောင်ရည် ပြောင်းလဲပြီး သက်ဆိုင်သည့် အချက်အလက်သည် အစနှင့် အဆုံးကြား တွင် ရှိသည့်အခါ ကျဆင်းနိုင်သည့် long-context ကျရှုံးမှု ပုံစံ တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အထောက်အထားကို context window အတွင်း ထည့်သွင်းနိုင်ခြင်းသည် မော်ဒယ်က တည်နေရာ တိုင်းကို ညီမျှသည့် ယုံကြည်စိတ်ချရမှုဖြင့် အသုံးပြုမည်ဟု အာမခံခြင်း မပြုပါ။
- **မကြာခဏ ရောထွေးမှု:** ၎င်းသည် လေ့လာ တွေ့ရှိထားသည့် အပြုအမူ ပုံစံ တစ်ခု ဖြစ်ပြီး မော်ဒယ်၊ task သို့မဟုတ် တည်နေရာ တိုင်းကို တူညီစွာ သက်ရောက်သည့် ပုံသေ နိယာမ တစ်ခု မဟုတ်ပါ။
- **လက်တွေ့:** အထောက်အထား တည်နေရာ များစွာကို စမ်းသပ်ရမည်၊ အာရုံလွဲစေသည့် အရာများကို လျှော့ချရမည်၊ ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် ကန့်သတ်ချက်များကို ထင်ရှားနေဆဲ နေရာတွင် ထားရှိရမည်၊ ဖြေဆိုချက်များကို ရင်းမြစ်နှင့် ကိုက်ညီမှု စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Context Window, Context Engineering, Eval Set, Grounding
- **English (source):** A long-context failure pattern in which model performance changes with evidence position and can degrade when relevant information sits between the beginning and end. Fitting evidence inside the context window does not guarantee that the model will use every position with equal reliability.

### Prompt Cache

**မြန်မာ:** Prompt Cache (တူညီသည့် prompt အစိတ်အပိုင်းကို ပြန်လည်အသုံးပြုခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တူညီသည့် သို့မဟုတ် အရည်အချင်း ပြည့်မီသည့် prompt prefix တစ်ခုအတွက် provider-side သို့မဟုတ် application-side တွက်ချက်မှုကို ပြန်လည် အသုံးပြုခြင်းဖြင့် ထပ်တလဲလဲ inference သည် preprocessing လုပ်ငန်း အချို့ကို ရှောင်ရှားစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** provider ၏ cache စာချုပ်ကို ပြည့်မီသည့်အခါ တည်ငြိမ်သည့် ညွှန်ကြားချက်များနှင့် ကြီးမားသည့် မျှဝေသည့် စာရွက်စာတမ်းများသည် ထပ်တလဲလဲ ခေါ်ဆိုမှုများတွင် ပိုမို သက်သာခြင်း သို့မဟုတ် လျင်မြန်ခြင်း ဖြစ်လာနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Prompt cache သည် provider သို့မဟုတ် application ၏ ပြန်လည် အသုံးပြုမှု စာချုပ် တစ်ခု ဖြစ်ပြီး အတွင်းပိုင်းတွင် prefix caching ကို အသုံးပြုနိုင်သည်။ Prefix caching သည် အရည်အချင်း ပြည့်မီသည့် တိကျသည့် token တူညီသည့် KV state ကို အထူး အသုံးပြုသည်၊ semantic caching သည် လုံလောက်စွာ ဆင်တူသည့် တောင်းဆိုမှု တစ်ခုအတွက် ယခင် ရလဒ်ကို ပြန်လည် အသုံးပြုသည်။
- **လက်တွေ့:** တည်ငြိမ်သည့် policy စာသားကို တောင်းဆိုမှုနှင့် သီးခြားဖြစ်သည့် အကြောင်းအရာ မတိုင်မီ ထားရမည်၊ cache-hit metadata ကို စောင့်ကြည့်ရမည်၊ အရည်အချင်းနှင့် သက်တမ်းသည် provider အလိုက် ကွာခြားသည့်အတွက် miss များကို ပုံမှန် အဖြစ် သဘောထားရမည်။
- **ဆက်စပ် term များ:** Semantic Cache, Prefix Caching, KV Cache, Time to First Token (TTFT)
- **Learn it:** [Prompt Caching](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/15-prompt-caching/)
- **English (source):** Reuse of provider-side or application-side computation for an identical or eligible prompt prefix so repeated inference avoids some preprocessing work. Stable instructions and large shared documents can become cheaper or faster across repeated calls when the provider's cache contract is satisfied.

### Prompt Engineering

**မြန်မာ:** Prompt Engineering (prompt ကို စီစဉ် တည်ဆောက်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် task တစ်ခုတွင် အပြုအမူ တိုးတက်စေရန် မော်ဒယ်နှင့် ထိတွေ့သည့် ညွှန်ကြားချက်များ၊ ဥပမာများ၊ ကန့်သတ်ချက်များနှင့် output လိုအပ်ချက်များကို စီစဉ် တည်ဆောက်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မော်ဒယ်အား မည်သည့် task ဖြစ်သည်၊ မည်သည့် ဒေတာ ပေးအပ်ထားသည်၊ မည်သည့် format နှင့် ကန့်သတ်ချက်များကို လိုက်နာရမည်ကို တိကျစွာ သတ်မှတ်ပေးခြင်းသည် အပြုအမူကို တိုးတက်စေသည့် အခြေခံ လုပ်ငန်း ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Prompt ၏ စကားလုံး ရွေးချယ်မှုသည် ပျောက်ဆုံးနေသည့် အထောက်အထား၊ မလုံခြုံသည့် permission၊ ညံ့ဖျင်းသည့် tool contract သို့မဟုတ် မရှိသည့် evaluation တို့ကို ဖြည့်ဆည်းပေးနိုင်ခြင်း မရှိပါ။
- **ဆက်စပ် term များ:** Context Engineering, Few-Shot, System Prompt, Structured Output
- **Learn it:** [Prompt Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/01-prompt-engineering/)
- **English (source):** Designing model-facing instructions, examples, constraints, and output requirements to improve behavior on a defined task.

### Prompt Sensitivity

**မြန်မာ:** Prompt Sensitivity (prompt ပြောင်းလဲမှုအပေါ် ရလဒ် ကွဲပြားမှု)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရည်ရွယ်သည့် task ကို မပြောင်းလဲဘဲ prompt ၏ စကားလုံး၊ အစဉ်၊ format သို့မဟုတ် ဥပမာများကို ပြောင်းလဲခြင်းကြောင့် ဖြစ်ပေါ်သည့် မော်ဒယ် output သို့မဟုတ် တိုင်းတာသည့် စွမ်းဆောင်ရည်၏ ကွဲပြားမှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အဆင်ပြေသည့် စကားလုံး ဖွဲ့စည်းမှု တစ်ခုအောက်တွင် အောင်မြင်သည့် စနစ် တစ်ခုသည် အမှန်တကယ် အသုံးပြုသူများအတွက် ယုံကြည်စိတ်ချရနိုင် မရှိနိုင် သို့မဟုတ် အကဲဖြတ်မှုတွင် လွဲမှားစေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** Sensitivity သည် prompt ချို့ယွင်းမှု တိုင်း မဟုတ်ပါ။ ၎င်းသည် မရှင်းလင်းမှု၊ မော်ဒယ်၏ ခိုင်မာမှု အားနည်းမှု၊ မတည်ငြိမ်သည့် decoding သို့မဟုတ် မလုံလောက်သည့် scoring စည်းမျဉ်းတို့ကို ဖော်ထုတ်နိုင်သည်။
- **လက်တွေ့:** အဓိပ္ပာယ် တူညီသည့် prompt မူကွဲများ ဖန်တီးရမည်၊ အမှု အလိုက် ကွဲပြားမှုကို တိုင်းတာရမည်၊ eval set တစ်ခုပေါ်တွင် prompt တစ်ခုကို အကောင်းဆုံး ဖြစ်အောင် ပြုပြင်ခြင်းအစား မူကွဲများကို regression test များတွင် ထိန်းသိမ်းရမည်။
- **ဆက်စပ် term များ:** Prompt Engineering, Eval Set, Regression Test, Few-Shot
- **English (source):** Variation in model output or measured performance caused by changes to prompt wording, order, formatting, or examples that preserve the intended task. A system that succeeds under one convenient phrasing may be unreliable for real users or misleading in evaluation.

### System Prompt

**မြန်မာ:** System Prompt (application မှ ပေးအပ်သည့် အခြေခံ ညွှန်ကြားချက်)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ထို provider ၏ instruction hierarchy အတွင်း အပြုအမူနှင့် ကန့်သတ်ချက်များကို တည်ထောင်ရန် application မှ ပေးအပ်သည့် provider မှ သတ်မှတ်ထားသည့် ညွှန်ကြားချက် message တစ်ခု သို့မဟုတ် configuration တစ်ခု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** System ညွှန်ကြားချက်များသည် အပြုအမူကို လမ်းညွှန်နိုင်သည်၊ သို့သော် ၎င်းတို့သည် လျှို့ဝှက်နေမည်ဟု အာမခံခြင်း မပြုပြီး လုံခြုံရေး နယ်နိမိတ် အနေဖြင့် သဘောထားရမည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** ဦးစားပေး စည်းမျဉ်းများ၊ message role များ၊ ဆက်လက် တည်ရှိမှုနှင့် မြင်နိုင်မှုတို့သည် API အလိုက် ကွာခြားသည်။ လက်ရှိ provider စာချုပ်ကို စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Prompt Engineering, Prompt Injection, Context Engineering, Guardrails
- **Learn it:** [Instructions as Executable Constraints](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/33-instructions-as-executable-constraints/)
- **English (source):** A provider-defined instruction message or configuration supplied by the application to establish behavior and constraints within that provider's instruction hierarchy. System instructions can guide behavior, but they are not guaranteed to remain secret and should not be treated as a security boundary.

### Token Budget

**မြန်မာ:** Token Budget (token ပမာဏကို ကြိုတင် ခွဲဝေသတ်မှတ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ညွှန်ကြားချက်များ၊ အထောက်အထား၊ မှတ်တမ်း၊ tool ရလဒ်များ၊ reasoning သို့မဟုတ် working space နှင့် output တို့အကြား token ပမာဏကို တိကျစွာ ခွဲဝေ သတ်မှတ်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထည့်သွင်းသည့် token တိုင်းသည် context ပမာဏ၊ latency နှင့် ကုန်ကျစရိတ် အတွက် ယှဉ်ပြိုင်သည်။ budget သတ်မှတ်ခြင်းသည် တန်ဖိုးမြင့်သည့် အထောက်အထားကို ဦးစွာ ထိန်းသိမ်းရန် သင့်အား တွန်းအားပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** Token budget သည် အစီအစဉ် ဆွဲသည့် ကန့်သတ်ချက် တစ်ခု ဖြစ်သည်။ ၎င်းသည် မော်ဒယ်၏ အများဆုံး context window နှင့် တူညီသည် မဟုတ်ပါ။
- **လက်တွေ့:** output ပမာဏကို ဖယ်ထားရမည်၊ ရယူထားသည့် chunk များကို ကန့်သတ်ရမည်၊ ဟောင်းသည့် tool ရလဒ်များကို state အဖြစ် အနှစ်ချုပ်ရမည်၊ မော်ဒယ်၏ ကန့်သတ်ချက် မရောက်မီ ရပ်တန့်ရမည် သို့မဟုတ် ချုံ့ရမည်။
- **ဆက်စပ် term များ:** Context Window, Context Engineering, Progressive Disclosure, Cost per Successful Task
- **Learn it:** [Context Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/05-context-engineering/)
- **English (source):** An explicit allocation of token capacity across instructions, evidence, history, tool results, reasoning or working space, and output. Every included token competes for context capacity, latency, and cost. Budgeting forces you to preserve high-value evidence first.

### Zero-Shot

**မြန်မာ:** Zero-Shot (ဥပမာ မပေးဘဲ လုပ်ဆောင်သည့် နည်းလမ်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လက်ရှိ input တွင် task-specific demonstration များ မထည့်ဘဲ ညွှန်ကြားချက်များ သို့မဟုတ် task ဖွဲ့စည်းမှုမှ task တစ်ခုကို လုပ်ဆောင်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ညွှန်ကြားချက်သက်သက်နှင့် task ဖွဲ့စည်းမှုဖြင့် task အသစ် တစ်ခုကို လုပ်ဆောင်ခြင်းသည် လက်ရှိ input အတွင်း demonstration များ မလိုဘဲ မော်ဒယ်၏ စွမ်းရည်ကို အသုံးချသည့် နည်းလမ်း တစ်ခု ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** Zero-shot သည် မော်ဒယ်တွင် သက်ဆိုင်သည့် pretraining၊ instruction tuning၊ tool သို့မဟုတ် ရယူထားသည့် context မရှိခဲ့သည်ဟု မဆိုလိုပါ။
- **ဆက်စပ် term များ:** Few-Shot, Prompt Engineering, Transfer Learning
- **English (source):** Performing a task from instructions or task framing without including task-specific demonstrations in the immediate input.

## Self-check

<details>
<summary>အဖြေများ ကြည့်ရန်</summary>

၁။ Context Window နှင့် Token Budget သည် မည်သို့ ကွာခြားသနည်း။
Context Window သည် မော်ဒယ်နှင့် API contract တစ်ခုအောက်တွင် ရရှိနိုင်သည့် အများဆုံး token စွမ်းရည် ဖြစ်သည်။ Token Budget သည် ထို စွမ်းရည်အတွင်း ညွှန်ကြားချက်၊ အထောက်အထား၊ မှတ်တမ်း၊ tool ရလဒ်၊ reasoning နှင့် output တို့အတွက် token ကို ကြိုတင် ခွဲဝေသတ်မှတ်သည့် အစီအစဉ် ဆွဲသည့် ကန့်သတ်ချက် ဖြစ်သည်။

၂။ Zero-Shot နှင့် Few-Shot သည် မည်သို့ ကွာခြားသနည်း။
Zero-Shot သည် လက်ရှိ input တွင် task-specific demonstration များ မထည့်ဘဲ ညွှန်ကြားချက်များ သို့မဟုတ် task ဖွဲ့စည်းမှုဖြင့် လုပ်ဆောင်သည်။ Few-Shot သည် ပစ်မှတ် input မတိုင်မီ ဥပမာ အနည်းငယ် ထည့်သွင်း၍ လိုလားသည့် task၊ format သို့မဟုတ် ဆုံးဖြတ်ချက် နယ်နိမိတ်ကို မော်ဒယ် ကောက်ချက်ချစေသည်။

၃။ Chain of Thought သည် ဖြေဆိုချက် မှန်ကန်ကြောင်း သက်သေပါသလား။
မပါ။ ချောမွေ့သည့် rationale တစ်ခုသည် ဖြေဆိုချက် မှန်ကန်ကြောင်း သို့မဟုတ် ထို စာသားသည် မော်ဒယ်၏ အတွင်းပိုင်း တွက်ချက်မှုကို သစ္စာရှိစွာ ကိုယ်စားပြုကြောင်း သက်သေ မဟုတ်ပါ။ Chain of thought သည် tool များ၊ test များ သို့မဟုတ် ပြင်ပ စစ်ဆေးမှုအတွက် အစားထိုး တစ်ခု မဟုတ်ပါ။

၄။ Prompt Engineering နှင့် Context Engineering သည် မည်သို့ ကွာခြားသနည်း။
Prompt Engineering သည် ညွှန်ကြားချက်၏ စကားလုံး ရွေးချယ်မှုနှင့် ဖွဲ့စည်းမှုကို အာရုံစိုက်သည်။ Context Engineering သည် မည်သည့် အထောက်အထားနှင့် state များ မော်ဒယ်၏ working context ထဲသို့ ဝင်ရောက်မည်ကိုလည်း ဆုံးဖြတ်သည်။

၅။ Instruction Hierarchy သည် လုံခြုံရေး နယ်နိမိတ် တစ်ခု ဖြစ်ပါသလား။
မဖြစ်ပါ။ ၎င်းသည် အပြုအမူကို တိုးတက်စေနိုင်သည်၊ သို့သော် least privilege နှင့် အတည်ပြုချက် ထိန်းချုပ်မှုများကသာ အကျိုးဆက်များကို ကန့်သတ်သည်။

</details>

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)
- Source repository: [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) (MIT License)
- [Few-Shot and Chain of Thought](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/02-few-shot-cot/)
- [Prompt Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/01-prompt-engineering/)
- [Context Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/05-context-engineering/)
- [Prompt Caching](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/15-prompt-caching/)
- [Instructions as Executable Constraints](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/14-agent-engineering/33-instructions-as-executable-constraints/)
- [LLMLingua](https://arxiv.org/abs/2310.05736)
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)
- [Finetuned Language Models Are Zero-Shot Learners](https://arxiv.org/abs/2109.01652)
- [The Instruction Hierarchy](https://arxiv.org/abs/2404.13208)
- [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/)
- [ProSA](https://aclanthology.org/2024.findings-emnlp.108/)

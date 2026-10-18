# 10 — Reliability & operations

ဤနယ်ပယ်သည် model သို့မဟုတ် အပလီကေးရှင်း တစ်ခုကို ထုတ်လုပ်မှု (production) တွင် တည်ငြိမ်စွာ လည်ပတ်စေရန် လိုအပ်သည့် အလေ့အကျင့်များကို ဖုံးလွှမ်းသည် — စွမ်းရည် ကုန်ခန်းသည့်အခါ မည်သည့် အလုပ်ကို လက်ခံမည်၊ မည်သည့် အလုပ် ကို ငြင်းပယ်မည်၊ ချို့ယွင်းမှု ဖြစ်သည့်အခါ မည်သို့ တုံ့ပြန်မည်၊ ထို ချို့ယွင်းမှုမှ မည်သို့ သင်ယူမည် ဆိုသည့် မေးခွန်းများ ဖြစ်သည်။ **Infrastructure & serving** (နယ်ပယ် ၉) သည် request တစ်ခုကို မည်သို့ အမြန်ဆုံး ပြီးမြောက်စေမည်ကို ဖြေဆိုသည်။ ဤနယ်ပယ် ၁၀ သည် ထို စနစ်ကို **မဖြစ်မနေ ပျက်ကွက်ခြင်း၊ ဖိအား လွန်ကဲခြင်းနှင့် ပြောင်းလဲမှု အန္တရာယ်** အောက်တွင် အသုံးပြုသူထံ ကတိပြုထားသည့် ဝန်ဆောင်မှု အဆင့်ကို ထိန်းသိမ်းစေမည့် နည်းလမ်းများကို ဖြေဆိုသည်။

Term ၁၇ ခုကို မိသားစု လေးခုအဖြစ် စုစည်းနိုင်သည်။ ပထမ — **ဝန်ပို ထိန်းချုပ်မှု (overload) မိသားစု**: **Admission Control**၊ **Load Shedding**၊ **Retry Budget**၊ **Saturation**။ ဤ term များသည် demand သည် စွမ်းရည်ထက် များလာသည့်အခါ စနစ် တစ်ခုလုံး ပြိုလဲခြင်းကို ရပ်တန့်ရန် လိုအပ်သည့် နယ်နိမိတ်များကို သတ်မှတ်သည်။ ဒုတိယ — **ဝန်ဆောင်မှု အဆင့် တိုင်းတာမှု မိသားစု**: **Service Level Indicator (SLI)**၊ **Service Level Objective (SLO)**၊ **Error Budget**၊ **Availability**၊ **Tail Latency**။ ဤ term များသည် \"ကောင်းသည်\" ဆိုသည့် စကားလုံးကို တိုင်းတာနိုင်သည့် ကိန်းဂဏန်းများအဖြစ် ခွဲခြားပေးသည်။

တတိယ — **ပြောင်းလဲမှု ထုတ်လွှတ်မှု (change) မိသားစု**: **Canary Release**၊ **Shadow Traffic**၊ **Rollback**၊ **Readiness Probe**။ ဤ term များသည် version အသစ် တစ်ခုကို အသုံးပြုသူ အားလုံးထံ မပို့မီ အန္တရာယ် ကို မည်သို့ ကန့်သတ်မည်ကို ဖော်ပြသည်။ စတုတ္ထ — **ချို့ယွင်းမှု တုံ့ပြန်မှု မိသားစု**: **Incident Response**၊ **Postmortem**၊ **Deadline Propagation**၊ **Graceful Degradation**။ ဤ term များသည် တစ်ခုခု မှားယွင်းပြီးသားအခါ ဆုံးရှုံးမှုကို မည်သို့ ထိန်းချုပ်မည်၊ သင်ခန်းစာကို မည်သို့ ရေရှည် တည်တံ့စေမည်ကို ရှင်းလင်းသည်။

Entry တစ်ခုကို ဖတ်သည့်အခါ **ဆိုလိုသည့် အဓိပ္ပာယ်** ဖြင့် စတင်ရမည် — ၎င်းသည် source ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ် ဖြစ်သည်။ ထို့နောက် **အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်အပေါ် မည်သို့ သက်ရောက်သည်ကို ကြည့်ရမည်။ **မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** စာကြောင်းများသည် source တွင် ပါသည့်အခါသာ ပေါ်လာသည်။ Technical term များ (circuit breaker၊ backpressure၊ timeout၊ retry storm၊ SLO၊ incident၊ degradation၊ queue၊ capacity) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိထားသည်။

### Admission Control

**မြန်မာ:** ဝင်ခွင့် ထိန်းချုပ်မှု (admission control)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စနစ်၏ လက်ရှိ စွမ်းရည်၊ priority နှင့် policy အောက်တွင် request တစ်ခုသည် ကန့်သတ်ထားသည့် queue သို့မဟုတ် ဝန်ဆောင်မှုထဲသို့ ဝင်ခွင့် ရမည် သို့မဟုတ် မရမည်ကို လက်ခံမှု မပြုမီ အဆင့်တွင် ဆုံးဖြတ်ပေးသည့် gate ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ထိန်းချုပ်ထားသည့် နယ်နိမိတ် တစ်ခုတွင် ပိုလွန်သည့် အလုပ်ကို ငြင်းပယ်ခြင်းဖြင့် ဝင်ခွင့် ရပြီးသား request များကို queue ကြီးထွားမှု၊ timeout cascade နှင့် အရင်းအမြစ် ကုန်ခန်းမှုတို့မှ ကာကွယ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** admission control သည် လက်ခံမှု မပြုမီ အလုပ်လုပ်သည်။ load shedding သည် ingress၊ queue များ၊ dependency များ သို့မဟုတ် အခြား overload နယ်နိမိတ်များတွင် အလုပ်ကို ငြင်းပယ် သို့မဟုတ် ဖယ်ရှားနိုင်သည်။
- **လက်တွေ့:** request ၏ ကုန်ကျစရိတ်ကို ခန့်မှန်းရမည်၊ tenant နှင့် စနစ် စွမ်းရည်ကို စစ်ဆေးရမည်၊ လိုအပ်သည့် budget ကို atomically သိမ်းဆည်းရမည်၊ ငြင်းပယ်သည့်အခါ overload ဖြစ်နေသည့် နယ်ပယ်ကို ဖော်ထုတ်ရမည်။ အခြေအနေသည် ယာယီ ဖြစ်ပြီး caller ၏ retry budget က နောက်တစ်ကြိမ် ကြိုးစားမှုကို ခွင့်ပြုသည့်အခါမှသာ retry အကြံပြုချက် ပေးရမည်။
- **ဆက်စပ် term များ:** Load Shedding, Backpressure, Rate Limit, Saturation
- **English (source):** A pre-acceptance gate that decides whether a request may enter a bounded queue or service under the system's current capacity, priority, and policy. Rejecting excess work at a controlled boundary protects admitted requests from queue growth, timeout cascades, and resource exhaustion.

### Availability

**မြန်မာ:** ရရှိနိုင်မှု (availability)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် တိုင်းတာမှု နယ်နိမိတ် တစ်ခုအောက်တွင် အသုံးပြုသူများသည် သတ်မှတ်ထားသည့် လက်ခံနိုင်သည့် ဝန်ဆောင်မှုကို ရရှိနိုင်သည့် အကျုံးဝင်သည့် ဝန်ဆောင်မှု အပြန်အလှန် ဆက်သွယ်မှုများ သို့မဟုတ် အချိန် ကာလများ၏ အချိုးအစား ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဝန်ဆောင်မှု process လည်ပတ်နေသော်လည်း အသုံးပြုသူများသည် အသုံးဝင်သည့် request များကို မပြီးမြောက်နိုင်သေးသည့် အခြေအနေ ရှိနိုင်သည်။ ထို့ကြောင့် availability ကို process uptime တစ်ခုတည်းနှင့် မချိတ်ဆက်ဘဲ အသုံးပြုသူ မြင်တွေ့နိုင်သည့် အောင်မြင်မှုနှင့် ချိတ်ဆက်ရမည်။
- **မကြာခဏ ရောထွေးမှု:** availability သည် reliability ရလဒ် တစ်ခု ဖြစ်သည်။ ၎င်းသည် latency၊ correctness၊ safety သို့မဟုတ် အသုံးပြုသူ အုပ်စု တိုင်း၏ အတွေ့အကြုံကို ဖော်ပြသည် မဟုတ်ပါ။
- **လက်တွေ့:** အကျုံးဝင်သည့် ဖြစ်ရပ်များနှင့် လက်ခံနိုင်သည့် ရလဒ်များကို သတ်မှတ်ရမည်၊ မှတ်တမ်းတင်ထားသည့် အခြေအနေများကိုသာ ဖယ်ထားရမည်၊ သတ်မှတ်ထားသည့် window တစ်ခုအတွင်း indicator ကို တွက်ချက်ရမည်၊ စုစုပေါင်း ချို့ယွင်းမှုများနှင့် ကြာရှည်သည့် တစ်စိတ်တစ်ပိုင်း ယုတ်လျော့မှု နှစ်ခုလုံးကို စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Service Level Indicator (SLI), Service Level Objective (SLO), Error Budget, Incident Response
- **English (source):** The proportion of eligible service interactions or time windows in which users can obtain the defined acceptable service under a stated measurement boundary. A service can be running while users still cannot complete useful requests, so availability must be tied to user-visible success rather than process uptime alone.

### Canary Release

**မြန်မာ:** canary ဖြင့် ထုတ်လွှတ်ခြင်း (canary release)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** rollout ကို ချဲ့ထွင်မည့် အရှေ့တွင် version အသစ်တစ်ခုကို traffic သို့မဟုတ် infrastructure ၏ ကန့်သတ်ထားသည့် အစိတ်အပိုင်း တစ်ခုသို့သာ ဖော်ထုတ်ပေးသည့် deployment နည်းဗျူဟာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ချို့ယွင်းချက်များ၏ သက်ရောက်မှုကို ကန့်သတ်ပေးပြီး model၊ prompt၊ agent သို့မဟုတ် ဝန်ဆောင်မှု အသစ်သည် အသုံးပြုသူ အားလုံးထံ မရောက်မီ ထုတ်လုပ်မှု အထောက်အထားကို ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** canary release သည် ဖော်ထုတ်မှုကို ကန့်သတ်သည်။ deployment မလုပ်မီ စမ်းသပ်မှု၊ အတည်ပြုချက် သို့မဟုတ် rollback ပြင်ဆင်မှုတို့ကို အစားထိုးသည် မဟုတ်ပါ။
- **လက်တွေ့:** အကျုံးဝင်သည့် အုပ်စု ငယ်တစ်ခုကို release ထံသို့ route လုပ်ရမည်၊ အရည်အသွေးနှင့် လည်ပတ်မှု metric များကို control နှင့် နှိုင်းယှဉ်ရမည်၊ ကြိုတင် သတ်မှတ်ထားသည့် ချို့ယွင်းချက်များ ပေါ်ပေါက်ပါက ရပ်တန့်ရမည် သို့မဟုတ် rollback လုပ်ရမည်။
- **ဆက်စပ် term များ:** Evaluation (Eval), Observability, Rollback, Verification Gate
- **English (source):** A deployment strategy that exposes a new version to a limited slice of traffic or infrastructure before expanding the rollout. It limits the impact of defects and gives you production evidence before the new model, prompt, agent, or service reaches everyone.

### Deadline Propagation

**မြန်မာ:** deadline ကို ဆက်လက် ပေးပို့ခြင်း (deadline propagation)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မူလ request သည် အသုံးဝင်စွာ မည်မျှ ကြာကြာ စောင့်နိုင်သေးသည်ကို dependency တစ်ခုချင်းက သိရှိစေရန် ကျန်ရှိသည့် end-to-end အချိန် budget ကို downstream ခေါ်ဆိုမှုများထံ ပေးပို့ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** သီးခြားချင်း သတ်မှတ်ထားသည့် timeout များသည် အသုံးပြုသူ၏ deadline ကို ကျော်လွန်နိုင်ပြီး၊ ရလဒ်သည် အသုံးဝင်တော့မည် မဟုတ်သည့်တိုင် စွန့်ပစ်ထားသည့် အလုပ်များက စွမ်းရည်ကို စားသုံးနေစေသည်။
- **မကြာခဏ ရောထွေးမှု:** deadline သည် အကြွင်းမဲ့ (absolute) သို့မဟုတ် ကျန်ရှိသည့် ပြီးစီးမှု နယ်နိမိတ် ဖြစ်သည်။ retry delay သည် နောက်တစ်ကြိမ် ကြိုးစားမှု မည်သည့်အခါ စတင်မည်ကို ထိန်းချုပ်ပြီး၊ ထို budget တစ်ခုတည်းအတွင်းတွင် ပါဝင်ရမည်။
- **လက်တွေ့:** ingress တွင် request deadline တစ်ခုတည်း သတ်မှတ်ရမည်၊ downstream ခေါ်ဆိုမှု တစ်ခုချင်းအတွက် ကုန်ဆုံးသွားသည့် အချိန်ကို နုတ်ရမည်၊ သက်တမ်း ကုန်ဆုံးသွားသည့် အလုပ်ကို ပလပ်ဖျက်ရမည်၊ budget ကို မည်သည့် နယ်နိမိတ်က ကုန်ဆုံးစေသည်ကို မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Retry with Backoff, Retry Budget, Tail Latency, Service Level Objective (SLO)
- **English (source):** Passing the remaining end-to-end time budget to downstream calls so each dependency knows how long the original request can still usefully wait. Independent timeouts can exceed the user's deadline and leave abandoned work consuming capacity after the result is no longer useful.

### Error Budget

**မြန်မာ:** အမှား ခွင့်ပြု budget (error budget)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဝန်ဆောင်မှု အဆင့် ပန်းတိုင် (service-level objective) က သတ်မှတ်ထားသည့် တိုင်းတာမှု window အတွင်းတွင် ထို ပန်းတိုင် မကုန်ဆုံးမီ အလုပ်မအောင်မြင်သည့် ဝန်ဆောင်မှုမည်မျှကို ခွင့်ပြုသည်ကို ဖော်ပြသည့် ပမာဏ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် reliability အလုပ်နှင့် ထုတ်ကုန် အလုပ်အတွက် မျှဝေသည့် ဆုံးဖြတ်ချက် နယ်နိမိတ် တစ်ခုကို ပေးသည် — အသုံးပြုသူ မြင်တွေ့နိုင်သည့် ချို့ယွင်းမှုက ထို budget ကို စားသုံးနေချိန်တွင် အန္တရာယ်ကို နှေးစေရမည် ဖြစ်ပြီး၊ ကျန်ရှိသည့် budget ကို ပြောင်းလဲမှုအပေါ် သုံးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** error budget သည် incident များ ဖြစ်ပေါ်စေရန် ခွဲတမ်း (quota) မဟုတ်ပါ။ ၎င်းသည် အသုံးပြုသူထံ အခြေပြုသည့် reliability ပန်တိုင်မှ ဆင်းသက်လာသည့် လည်ပတ်မှု policy ဖြစ်သည်။
- **လက်တွေ့:** budget ကို SLO မှ ဆင်းသက်ရမည်၊ အကြောင်းရင်းနှင့် အသုံးပြုသူ အုပ်စု အလိုက် burn ကို ခြေရာခံရမည်၊ ကုန်ဆုံးမီ release လုပ်ဆောင်ချက်များကို သတ်မှတ်ရမည်၊ incident တစ်ခုအတွက် စာရင်း တွက်ချက်မှုကို ပြန်လည် သတ်မှတ်ခြင်းကို ရှောင်ရမည်။
- **ဆက်စပ် term များ:** Service Level Objective (SLO), Service Level Indicator (SLI), Availability, Incident Response
- **English (source):** The amount of unsuccessful service allowed by a service-level objective over its measurement window before the objective is exhausted. It gives reliability and product work a shared decision boundary: teams can spend remaining budget on change while slowing risk when user-visible failure consumes it.

### Graceful Degradation

**မြန်မာ:** ညင်သာစွာ အရည်အသွေး လျှော့ချခြင်း (graceful degradation)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** စွမ်းရည် သို့မဟုတ် dependency များ ချို့ယွင်းသည့်အခါ request တိုင်းကို ချို့ယွင်းစေမည့်အစား ရွေးချယ်နိုင်သည့် အရည်အသွေး၊ feature၊ freshness သို့မဟုတ် workload တို့ကို လျှော့ချ၍ ကန့်သတ်ထားသည့် အဓိက ဝန်ဆောင်မှုကို ထိန်းသိမ်းခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** AI စနစ်များသည် နှေးကွေးသည့် သို့မဟုတ် ချို့ယွင်းနိုင်သည့် အစိတ်အပိုင်း အတော်များများအပေါ် မှီခိုလေ့ ရှိသည်။ ထို့ကြောင့် တိကျစွာ သတ်မှတ်ထားသည့် လျှော့ချ mode တစ်ခုသည် တစ်စိတ်တစ်ပိုင်း ချို့ယွင်းချိန်တွင် အဓိက အသုံးပြုသူ ရလဒ်များကို ကာကွယ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** graceful degradation သည် ဘာမျှ မဖြစ်သကဲ့သို့ ပိုဆိုးသည့် အဖြေကို တိတ်ဆိတ်စွာ ပြန်ပေးခြင်း မဟုတ်ပါ။ လည်ပတ်မှု ရှုထောင့်မှ မြင်တွေ့နိုင်မှု (visibility) ကို အမြဲ လိုအပ်သည်။ လျှော့ချ mode သည် ရလဒ် သို့မဟုတ် ဝန်ဆောင်မှု ကတိကို သိသိသာသာ ပြောင်းလဲသည့်အခါ အသုံးပြုသူများကို အသိပေးရမည်။
- **လက်တွေ့:** မည်သည့် စွမ်းဆောင်ရည်များကို ပိတ်နိုင်သည်ကို ကြိုတင် သတ်မှတ်ရမည်၊ လျှော့ချ mode ကို လည်ပတ်မှု ရှုထောင့်မှ မြင်နိုင်စေရမည်၊ safety စစ်ဆေးမှုများကို ကာကွယ်ရမည်၊ dependency ချို့ယွင်းမှုအောက်တွင် fallback ကို စမ်းသပ်ရမည်၊ ဝန်ဆောင်မှု အပြည့်အဝကို တမင်တကာ ပြန်လည် ရယူရမည်။ correctness၊ safety၊ freshness သို့မဟုတ် ကတိပြုထားသည့် သဘောတူညီချက် သိသိသာသာ ပြောင်းလဲသည့်အခါ အသုံးပြုသူများကို အသိပေးရမည်။
- **ဆက်စပ် term များ:** Circuit Breaker, Load Shedding, Model Router, Availability
- **Learn it:** [Production LLM Application](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/13-production-app/)
- **English (source):** Preserving a bounded core service when capacity or dependencies are impaired by reducing optional quality, features, freshness, or workload instead of failing every request. AI systems often depend on several slow or fallible components, so an explicit reduced mode can protect essential user outcomes during partial failure.

### Incident Response

**မြန်မာ:** incident တုံ့ပြန်မှု (incident response)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဝန်ဆောင်မှု၊ data၊ safety သို့မဟုတ် security ကို ခြိမ်းခြောက်သည့် ဖြစ်ရပ်တစ်ခုကို ဖော်ထုတ်ခြင်း၊ ခွဲခြမ်းစိတ်ဖြာခြင်း၊ ထိန်းချုပ်ခြင်း၊ ပြန်လည် ကောင်းမွန်စေခြင်း၊ ဆက်သွယ် အသိပေးခြင်းနှင့် သင်ယူခြင်းတို့ကို ညှိနှိုင်းစွာ လုပ်ဆောင်သည့် လုပ်ငန်းစဉ် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** incident ဖြစ်နေစဉ်တွင် ရှင်းလင်းသည့် တာဝန်ခွဲဝေမှုနှင့် အထောက်အထားသည် ကြံဖန် ဖြေရှင်းမှုထက် ပို၍ အရေးပါသည် — အထူးသဖြင့် model အပြုအမူနှင့် ဖြန့်ကျက်ထားသည့် dependency များက ချို့ယွင်းနေသည့် နယ်နိမိတ်ကို ဖုံးကွယ်သည့်အခါ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** incident response သည် ဖြစ်ရပ်နှင့် ၎င်း၏ အကျိုးဆက်များကို စီမံသည်။ root-cause analysis နှင့် ရေရှည် ကာကွယ်မှုသည် ချက်ချင်း ဝန်ဆောင်မှု ပြန်လည် ရရှိပြီးမှ ဆက်လက် လုပ်ဆောင်ရသည်။
- **လက်တွေ့:** severity နှင့် command တာဝန်များကို သတ်မှတ်ရမည်၊ trace များနှင့် audit မှတ်တမ်းများကို ထိန်းသိမ်းရမည်၊ အန္တရာယ်ရှိသည့် လုပ်ဆောင်ချက်များကို ရပ်တန့်ရမည်၊ သက်ရောက်မှုကို ဆက်သွယ် အသိပေးရမည်၊ ပြန်လည် ကောင်းမွန်မှုကို စစ်ဆေးရမည်၊ ပြုပြင်ရေး အလုပ်များကို အပြီးသတ် လိုက်ပါ ဆောင်ရွက်ရမည်။
- **ဆက်စပ် term များ:** Observability, Audit Log, Postmortem, Availability
- **Learn it:** [SRE for AI](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/23-sre-for-ai/)
- **English (source):** The coordinated process for detecting, analyzing, containing, recovering from, communicating, and learning from an event that threatens service, data, safety, or security. During an incident, clear roles and evidence matter more than improvised heroics, especially when model behavior and distributed dependencies obscure the failing boundary.

### Load Shedding

**မြန်မာ:** ဝန် ဖြန့်ချခြင်း — ဝန်ပိုကို ငြင်းပယ်ခြင်း (load shedding)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** demand သည် အသုံးဝင်သည့် ရလဒ် ထုတ်လုပ်နိုင်သည့် ရရှိနိုင်သည့် စွမ်းရည်ထက် ကျော်လွန်သည့်အခါ overload နယ်နိမိတ် တစ်ခု သို့မဟုတ် အတော်များများတွင် ရွေးချယ်ထားသည့် အလုပ်ကို တမင်တကာ ငြင်းပယ်ခြင်း၊ ချပစ်ခြင်း သို့မဟုတ် ပလပ်ဖျက်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** overload ဖြစ်နေစဉ် request တိုင်းကို ဆက်လက် လက်ခံနေခြင်းသည် queueing ကို တိုးမြင့်စေပြီး၊ request အားလုံးနီးပါးသည် deadline ကို လွန်ဆန်စေကာ ပြန်လည် ကောင်းမွန်ရန် ပို၍ ခက်ခဲစေသည်။
- **မကြာခဏ ရောထွေးမှု:** load shedding သည် လက်ခံပြီးသား အလုပ်တွင်သာ ကန့်သတ်သည် မဟုတ်ပါ။ admission control သည် အထူးသဖြင့် လက်ခံမှု မပြုမီ gate ဖြစ်ပြီး၊ rate limiting သည် စွမ်းရည် ကျန်ရှိနေသည့်တိုင် အသုံးပြုမှု policy ကို ပြဋ္ဌာန်းနိုင်သည်။
- **လက်တွေ့:** အကြောင်းအရာ အရှိဆုံး နယ်နိမိတ်တွင် shed လုပ်ရမည်၊ ဖြစ်နိုင်သည့်အခါ high-priority အလုပ်နှင့် လက်ခံပြီးသား အလုပ်ကို ထိန်းသိမ်းရမည်၊ overload ဖြစ်နေသည့် နယ်ပယ်ကို ဖော်ထုတ်ရမည်၊ အခြေအနေသည် ယာယီ ဖြစ်ပြီး request သည် ၎င်း၏ retry budget အတွင်း ရှိနေသည့်အခါမှသာ တုံ့ပြန်မှုကို retryable အဖြစ် သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Admission Control, Backpressure, Rate Limit, Graceful Degradation
- **English (source):** Deliberately rejecting, dropping, or cancelling selected work at one or more overload boundaries when demand exceeds the capacity available to produce useful results. Continuing to accept every request during overload can increase queueing until nearly all requests miss their deadlines and recovery becomes harder.

### Postmortem

**မြန်မာ:** incident နောက်ပိုင်း သုံးသပ်ချက် (postmortem)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သက်ရောက်မှု၊ ဖော်ထုတ်မှု၊ တုံ့ပြန်မှု၊ အထောက်အကူပြု အခြေအနေများ၊ ပြန်လည် ကောင်းမွန်မှုနှင့် ပိုင်ရှင် သတ်မှတ်ထားသည့် နောက်ဆက်တွဲ လုပ်ဆောင်ချက်များကို ရှင်းလင်းပြီး၊ ခွဲခြမ်းစိတ်ဖြာမှုအစား လူတစ်ဦးကို အပြစ်တင်ခြင်းကို အစားမထိုးသည့် ရေရှည် တည်တံ့သည့် incident မှတ်တမ်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ဖြေရှင်းပြီးသား ပြတ်တောက်မှုတစ်ခုသည် အထောက်အထား အဖြစ် တန်ဖိုး ရှိနေသေးသည်။ စနစ်၏ အခြေအနေများနှင့် ဆုံးဖြတ်ချက်များကို မှတ်တမ်းတင်ခြင်းသည် ဖြစ်ရပ် တစ်ခုကို ပြန်ဖြစ်မှု လျှော့ချပြီး တုံ့ပြန်ချိန် တိုစေသည့် တိုးတက်မှုများအဖြစ် ပြောင်းလဲပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** postmortem သည် အစည်းအဝေး မှတ်တမ်း သို့မဟုတ် လူတစ်ဦး၏ အမှား ရှာဖွေခြင်း မဟုတ်ပါ။ ၎င်းသည် စမ်းသပ်နိုင်သည့် စနစ် တိုးတက်မှုများကို ထုတ်ပေးရမည်။
- **လက်တွေ့:** timeline ကို trace များနှင့် log များမှ တည်ဆောက်ရမည်၊ အစပြုသည့် ဖြစ်ရပ်များနှင့် အထောက်အကူပြု အခြေအနေများကို ခွဲခြားရမည်၊ ရက်စွဲ ပါသည့် လုပ်ဆောင်ချက်များကို တာဝန်ပေးရမည်၊ လုပ်ဆောင်ချက် တစ်ခုချင်းက သက်ဆိုင်ရာ control ကို ပြောင်းလဲခဲ့သလား ပြန်လည် သုံးသပ်ရမည်။
- **ဆက်စပ် term များ:** Incident Response, Regression Test, Audit Log, Observability
- **English (source):** A durable incident record that explains impact, detection, response, contributing conditions, recovery, and owned follow-up actions without assigning blame as a substitute for analysis. A resolved outage still has value as evidence. Capturing system conditions and decisions turns one event into improvements that reduce recurrence and response time.

### Readiness Probe

**မြန်မာ:** အသင့်ဖြစ်မှု စစ်ဆေးချက် (readiness probe)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဝန်ဆောင်မှု instance တစ်ခုသည် လက်ရှိတွင် request များကို လက်ခံနိုင်သလား မလက်ခံနိုင်သလားကို traffic လမ်းကြောင်း ချထားသည့် အလွှာထံ ပြောပြသည့် ရောဂါ စစ်ဆေးချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** process တစ်ခု အသက်ရှင်နေသော်လည်း ၎င်း၏ model unload ဖြစ်နေခြင်း၊ dependency များ မရရှိနိုင်ခြင်း သို့မဟုတ် warmup မပြီးစီးခြင်း ဖြစ်နိုင်သည်။ ထို့ကြောင့် traffic ကို စောလွန်းစွာ ပို့လွှတ်ခြင်းသည် ရှောင်လွှဲနိုင်သည့် ချို့ယွင်းမှုများကို ဖြစ်ပေါ်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** readiness သည် traffic ရရှိခွင့် (traffic eligibility) ကို ထိန်းချုပ်သည်။ liveness သည် process ကို restart လုပ်သင့်/မသင့် ဆုံးဖြတ်သည်။ နှစ်ခုစလုံးသည် model တုံ့ပြန်မှု တိုင်း မှန်ကန်မည်ဟု သက်သေမပြပါ။
- **လက်တွေ့:** ဝန်ဆောင်မှု ပေးရန် လိုအပ်သည့် အနည်းဆုံး dependency များကို စစ်ဆေးရမည်၊ startup နှင့် draining အချိန်များတွင် readiness ကို မအောင်မြင်စေရမည်၊ probe ကို ကုန်ကျစရိတ် နည်းစေရမည်၊ readiness false ဖြစ်ခြင်းကြောင့်သာ process ကို restart လုပ်ခြင်း မပြုရ။
- **ဆက်စပ် term များ:** Autoscaling, Model Serving, Availability, Graceful Degradation
- **Learn it:** [Production LLM Application](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/13-production-app/)
- **English (source):** A diagnostic that tells the traffic-routing layer whether a service instance is currently able to accept requests. A process can be alive while its model is unloaded, dependencies are unavailable, or warmup is incomplete, so sending traffic too early creates avoidable failures.

### Retry Budget

**မြန်မာ:** retry ခွင့်ပြု budget (retry budget)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မူလ request များနှင့် နှိုင်းယှဉ်သည့် အနေဖြင့် သို့မဟုတ် အချိန် window တစ်ခုအတွင်း ဖော်ပြသည့် retry traffic အပေါ် သတ်မှတ်ထားသည့် ကန့်သတ်ချက် ဖြစ်ပြီး၊ retry များက စွမ်းရည်ကို အကန့်အသတ်မရှိ မစားသုံးစေရန် တားဆီးပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** dependency တစ်ခု နှေးကွေးသည့်အခါ သို့မဟုတ် ချို့ယွင်းသည့်အခါ ကန့်သတ်မထားသည့် retry များသည် စနစ်တွင် လွတ်လပ်သည့် စွမ်းရည် အနည်းဆုံး ဖြစ်နေသည့် အချိန်တွင် ဝန်ကို ဆတိုးမြှင့်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** retry budget သည် အပိုကြိုးစားမှုများကို ကန့်သတ်သည်။ error budget သည် SLO က ခွင့်ပြုသည့် အသုံးပြုသူ မြင်တွေ့နိုင်သည့် မယုံကြည်ရမှုကို တိုင်းတာသည်။
- **လက်တွေ့:** retry များကို ပထမ ကြိုးစားမှုများနှင့် သီးခြား ရေတွက်ရမည်၊ ဝန်ဆောင်မှုနှင့် tenant အလိုက် ကန့်သတ်ရမည်၊ deadline များကို လိုက်နာရမည်၊ jitter ထည့်ထားသည့် backoff ကို သုံးရမည်၊ ယာယီ မဟုတ်သည့် သို့မဟုတ် idempotent မဟုတ်သည့် ချို့ယွင်းမှုများအတွက် retry လုပ်ခြင်းကို ရပ်ရမည်။
- **ဆက်စပ် term များ:** Retry with Backoff, Error Budget, Rate Limit, Admission Control
- **English (source):** A bound on retry traffic, usually expressed relative to original requests or over a time window, that prevents retries from consuming unbounded capacity. When a dependency slows or fails, unrestricted retries multiply load exactly when the system has the least spare capacity.

### Rollback

**မြန်မာ:** ယခင် version သို့ ပြန်လှည့်ခြင်း (rollback)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လက်ရှိ release သည် လည်ပတ်မှု၊ အရည်အသွေး သို့မဟုတ် safety သတ်မှတ်ချက်များကို ချိုးဖောက်သည့်အခါ ယခင် သိရှိပြီးသား deployment သို့မဟုတ် configuration ကို ပြန်လည် ရယူခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** agent နှင့် model ပြောင်းလဲမှုများသည် deployment မလုပ်မီ အကဲဖြတ်မှု ရှိသည့်တိုင် ထုတ်လုပ်မှုတွင် ချို့ယွင်းနိုင်သည်။ ထို့ကြောင့် ပြန်လည် ကောင်းမွန်စေမှုကို rollout မလုပ်မီ ကြိုတင် ရေးဆွဲရမည်။
- **မကြာခဏ ရောထွေးမှု:** code rollback သည် database migration၊ ပြင်ပ အကျိုးဆက် (external side effect)၊ cache ထုတ်ထားသည့် ရလဒ်များ သို့မဟုတ် ချို့ယွင်းသည့် release က ရေးထားသည့် data များကို အလိုအလျောက် ပြန်လှန်ပေးသည် မဟုတ်ပါ။
- **လက်တွေ့:** version သတ်မှတ်ထားသည့် artifact များနှင့် configuration ကို ထိန်းသိမ်းရမည်၊ rollback trigger များကို သတ်မှတ်ရမည်၊ command နှင့် data အကျိုးသက်ရောက်မှုများကို လေ့ကျင့် စမ်းသပ်ရမည်၊ ပြန်လည် ရယူပြီးနောက် ဝန်ဆောင်မှု ကျန်းမာမှုကို စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Canary Release, Checkpoint, Regression Test, Durable Execution
- **English (source):** Restoring a previously known deployment or configuration when the current release violates operational, quality, or safety criteria. Agent and model changes can fail in production despite pre-deployment evaluation, so recovery must be designed before rollout.

### Saturation

**မြန်မာ:** စွမ်းရည် ပြည့်ဝမှု (saturation)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကန့်သတ်ထားသည့် အရင်းအမြစ် သို့မဟုတ် ဝန်ဆောင်မှု တစ်ခုသည် ၎င်း၏ စွမ်းရည်ကို ကုန်ဆုံးသွားသည့် အတိုင်းအတာ ဖြစ်ပြီး၊ ချက်ချင်း မစတင်နိုင်သည့် queue တွင် စောင့်နေသည့် အလုပ်များလည်း ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** memory၊ accelerator slot၊ queue depth သို့မဟုတ် downstream quota တစ်ခုသည် အသုံးဝင်သည့် throughput ကို ကန့်သတ်နေပြီ ဖြစ်နေချိန်တွင် utilization တစ်ခုတည်းက လက်ခံနိုင်သည့် အနေအထား ပေါ်နေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** saturation သည် တစ်ကမ္ဘာလုံး သက်ဆိုင်သည့် ရာခိုင်နှုန်း တစ်ခု မဟုတ်ပါ။ ကန့်သတ်သည့် အရင်းအမြစ်နှင့် ၎င်း၏ queueing အပြုအမူသည် workload နှင့် ဗိသုကာအပေါ် မူတည်သည်။
- **လက်တွေ့:** အဓိက အရင်းအမြစ် တစ်ခုချင်းကို ဖော်ထုတ်ရမည်၊ တက်ကြွနေသည့် အလုပ်နှင့် စောင့်နေသည့် အလုပ်ကို တိုင်းတာရမည်၊ saturation ကို tail latency နှင့် error များနှင့် ဆက်စပ်ရမည်၊ queue သည် မတည်ငြိမ်သည့် ကြီးထွားမှု အဆင့်သို့ မရောက်မီ alert လုပ်ရမည်။
- **ဆက်စပ် term များ:** Observability, Autoscaling, Backpressure, Tail Latency
- **English (source):** The degree to which a constrained resource or service has exhausted its capacity, including queued work that cannot begin promptly. Utilization alone can appear acceptable while memory, accelerator slots, queue depth, or a downstream quota is already limiting useful throughput.

### Service Level Indicator (SLI)

**မြန်မာ:** ဝန်ဆောင်မှု အဆင့် ညွှန်ကိန်း (service level indicator, SLI)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် အသုံးပြုသူနှင့် သက်ဆိုင်သည့် နယ်နိမိတ်တွင် ဝန်ဆောင်မှု အပြုအမူကို တိုင်းတာသည့် အရေအတွက် အတိုင်းအတာ ဖြစ်သည် — ဥပမာ အောင်မြင်သည့် request အချိုးအစား သို့မဟုတ် သတ်မှတ်ချက် အဆင့်အောက် ရှိသည့် latency။
- **အရေးပါသည့် အကြောင်းရင်း:** reliability ဆွေးနွေးမှုများသည် လေ့လာတွေ့ရှိသည့် အပြုအမူ၊ အကျုံးဝင်သည့် ဖြစ်ရပ်များနှင့် တိုင်းတာမှု အမှတ်တို့ ရှင်းလင်းသည့်အခါမှသာ လုပ်ဆောင်နိုင်သည့် အဆင့်သို့ ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** SLI သည် တိုင်းတာမှု ဖြစ်သည်။ SLO သည် ထို တိုင်းတာမှုအပေါ် သတ်မှတ်ထားသည့် ကာလတစ်ခုအတွင်း ကျင့်သုံးသည့် ပန်းတိုင် ဖြစ်သည်။
- **လက်တွေ့:** numerator၊ denominator၊ ဖယ်ထားသည့် အခြေအနေများ၊ data အရင်းအမြစ်နှင့် aggregation window ကို သတ်မှတ်ရမည်၊ ထို့နောက် indicator သည် အသုံးပြုသူများ တကယ် ကြုံတွေ့သည့် ရလဒ်ကို ခြေရာခံကြောင်း အတည်ပြုရမည်။
- **ဆက်စပ် term များ:** Service Level Objective (SLO), Availability, Tail Latency, Observability
- **English (source):** A quantitative measure of service behavior at a defined user-relevant boundary, such as successful request ratio or latency below a threshold. Reliability discussions become actionable only when the observed behavior, eligible events, and measurement point are explicit.

### Service Level Objective (SLO)

**မြန်မာ:** ဝန်ဆောင်မှု အဆင့် ပန်းတိုင် (service level objective, SLO)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် လူအုပ်စု (population) နှင့် တိုင်းတာမှု window တစ်ခုအတွင်း ဝန်ဆောင်မှု အဆင့် ညွှန်ကိန်း တစ်ခုအတွက် သတ်မှတ်ထားသည့် ပန်းတိုင် အတိုင်းအတာ သို့မဟုတ် သတ်မှတ်ချက် အဆင့် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် မျှော်လင့်ထားသည့် အသုံးပြုသူ ရလဒ်ကို စောင့်ကြည့်မှု၊ စွမ်းရည်၊ release အန္တရာယ်နှင့် incident ဆုံးဖြတ်ချက်များအတွက် လည်ပတ်မှု နယ်နိမိတ် တစ်ခုအဖြစ် ပြောင်းလဲပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** SLO သည် အတွင်းပိုင်း reliability ပန်းတိုင် ဖြစ်သည်။ စာချုပ်အခြေခံ ဝန်ဆောင်မှု အဆင့် သဘောတူညီချက် (service-level agreement) တွင် လျော်ကြေးများ ပါဝင်နိုင်ပြီး မတူညီသည့် အဓိပ္ပာယ်ဖွင့်ဆိုချက်များကို သုံးနိုင်သည်။
- **လက်တွေ့:** အသုံးပြုသူများ ဂရုစိုက်သည့် indicator ကို ရွေးရမည်၊ လက်ရှိ စွမ်းဆောင်ရည်အစား ထုတ်ကုန် လိုအပ်ချက်များမှ ပန်းတိုင်ကို သတ်မှတ်ရမည်၊ window နှင့် ဖယ်ထားသည့် အခြေအနေများကို သတ်မှတ်ရမည်၊ error-budget policy တစ်ခုကို ချိတ်ဆက်ရမည်။
- **ဆက်စပ် term များ:** Service Level Indicator (SLI), Error Budget, Availability, Goodput
- **Learn it:** [Inference Metrics and Goodput](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/08-inference-metrics-goodput/)
- **English (source):** A target range or threshold for a service-level indicator over a stated population and measurement window. It translates an expected user outcome into an operating boundary for monitoring, capacity, release risk, and incident decisions.

### Shadow Traffic

**မြန်မာ:** အရိပ် traffic (shadow traffic)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** လက်ရှိ request traffic ၏ မိတ္တူကို လေ့လာမှုအတွက် ကိုယ်စားလှယ် (candidate) စနစ်တစ်ခုထံ ပို့လွှတ်ခြင်း ဖြစ်ပြီး၊ ကိုယ်စားလှယ်၏ တုံ့ပြန်မှုသည် အဓိက အသုံးပြုသူ တုံ့ပြန်မှု လမ်းကြောင်း၏ အပြင်တွင် ရှိနေသည်။ မိတ္တူ request သည် အမှန်တကယ် လည်ပတ်နေသေးသည့်အတွက် ၎င်း၏ အကျိုးဆက်များကို သီးခြားခွဲထားရမည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် ကိုယ်စားလှယ်ကို တကယ့် input ပုံစံများနှင့် ဝန်အောက်တွင် ဖော်ထုတ်ပေးပြီး၊ အသုံးပြုသူ အပေါ် သက်ရောက်မှုကို ကန့်သတ်ထားသည်။ ထို့ကြောင့် ဖန်တီးထားသည့် စမ်းသပ်မှုများတွင် မပါသည့် ချို့ယွင်းမှုများကို ဖော်ထုတ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** ကိုယ်စားလှယ်၏ တုံ့ပြန်မှုကို အဓိက လမ်းကြောင်းပြင်ပတွင် ထားရှိခြင်းသည် လည်ပတ်မှုကို အကျိုးဆက် ကင်းစေသည် မဟုတ်ပါ။ canary release သည် မတူညီသည် — ၎င်းသည် traffic ၏ ထိန်းချုပ်ထားသည့် အချိုးအစားအတွက် တကယ့် အသုံးပြုသူများကို ကိုယ်စားလှယ်မှ ဝန်ဆောင်ပေးသည်။
- **လက်တွေ့:** ထိခိုက်နိုင်သည့် field များကို ဖယ်ရှားရမည် သို့မဟုတ် tokenize လုပ်ရမည်၊ tool များနှင့် dependency များကို sandbox သို့မဟုတ် no-op ပန်းတိုင်များထံ route လုပ်ရမည်၊ စွမ်းဆောင်ရည် နယ်နိမိတ်များတွင် write များကို ပိတ်ရမည်၊ request ဆက်စပ်မှု (correlation) ကို ထိန်းသိမ်းရမည်၊ shadow ဝန်သည် အသုံးပြုသူ traffic နှင့် အပြိုင်အဆိုင် မဖြစ်စေရန် တားဆီးရမည်။
- **ဆက်စပ် term များ:** Canary Release, Evaluation (Eval), Trace, Model Serving
- **Learn it:** [Shadow, Canary, and Progressive Delivery](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/20-shadow-canary-progressive/)
- **English (source):** A copy of live request traffic sent to a candidate system for observation while the candidate response remains outside the primary user response path. Because the copied request still executes, its side effects must be isolated. It exposes the candidate to real input shapes and load while limiting user impact, which can reveal failures absent from synthetic tests.

### Tail Latency

**မြန်မာ:** အမြီး latency — အနှေးဆုံး request များ၏ latency (tail latency)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** အနှေးဆုံး request အစိတ်အပိုင်း ကြုံတွေ့ရသည့် latency ဖြစ်ပြီး၊ သတ်မှတ်ထားသည့် workload နှင့် အချိန် window တစ်ခုအောက်တွင် မြင့်မားသည့် percentile တစ်ခုဖြင့် အများအားဖြင့် အနှစ်ချုပ် ဖော်ပြသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** queueing၊ contention၊ retry သို့မဟုတ် ကွဲပြားသည့် request ကုန်ကျစရိတ်တို့ကြောင့် အဓိပ္ပာယ် ရှိသည့် အသုံးပြုသူ အုပ်စုတစ်ခုသည် ပို၍ ကြာကြာ စောင့်နေချိန်တွင် ပျှမ်းမျှများသည် ကျန်းမာနေသည့်ဟု ပေါ်နေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** tail latency သည် အနှေးဆုံး request တစ်ခုတည်း မဟုတ်သလို၊ percentile၊ လူအုပ်စု နှင့် တိုင်းတာမှု နယ်နိမိတ် မပါဘဲ အဓိပ္ပာယ် မရှိပါ။
- **လက်တွေ့:** route နှင့် workload အလိုက် percentile အတော်များများကို ဖော်ပြရမည်၊ timeout များကို မှတ်တမ်းတင်ထားသည့် စည်းမျဉ်းအရ ဖြတ်တောက်ထားသည့် (censored) သို့မဟုတ် မအောင်မြင်သည့် လေ့လာတွေ့ရှိချက်များအဖြစ် ထားရှိရမည်၊ နှေးကွေးသည့် request များကို dependency များတစ်လျှောက် ခြေရာခံရမည်။
- **ဆက်စပ် term များ:** Time to First Token (TTFT), Time per Output Token (TPOT), Saturation, Goodput
- **Learn it:** [Inference Metrics and Goodput](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/08-inference-metrics-goodput/)
- **English (source):** The latency experienced by the slowest portion of requests, commonly summarized with a high percentile under a stated workload and time window. Averages can look healthy while a meaningful group of users waits much longer because of queueing, contention, retries, or variable request cost.

## Self-check

1. Admission Control နှင့် Load Shedding ကွာခြားချက်သည် အဘယ်နည်း။
2. SLI၊ SLO နှင့် Error Budget တို့ အချင်းချင်း မည်သို့ ဆက်စပ်သနည်း။
3. Canary Release နှင့် Shadow Traffic တို့ အသုံးပြုသူအပေါ် သက်ရောက်မှု ကွာခြားချက်ကား အဘယ်နည်း။
4. Deadline Propagation သည် retry delay နှင့် မည်သို့ ဆက်စပ်သနည်း။
5. Readiness Probe နှင့် liveness ၏ တာဝန် ကွာခြားချက်သည် အဘယ်နည်း။

<details>
<summary>အဖြေများ</summary>

1. Admission Control သည် လက်ခံမှု မပြုမီ အဆင့်တွင် အလုပ်လုပ်သည့် gate ဖြစ်ပြီး၊ request တစ်ခု ဝင်ခွင့် ရ/မရ ကို ဆုံးဖြတ်သည်။ Load Shedding သည် ingress၊ queue များ၊ dependency များ သို့မဟုတ် အခြား overload နယ်နိမိတ်များတွင် အလုပ်ကို ငြင်းပယ် သို့မဟုတ် ဖယ်ရှားနိုင်သည် — လက်ခံပြီးသား အလုပ်အပေါ်တွင်လည်း သက်ရောက်နိုင်သည်။
2. SLI သည် တိုင်းတာမှု (ဥပမာ အောင်မြင်သည့် request အချိုးအစား) ဖြစ်သည်။ SLO သည် ထို တိုင်းတာမှုအပေါ် သတ်မှတ်ထားသည့် လူအုပ်စုနှင့် window တစ်ခုအတွင်း ကျင့်သုံးသည့် ပန်းတိုင် ဖြစ်သည်။ Error Budget သည် ထို SLO က ခွင့်ပြုသည့် မအောင်မြင်မှု ပမာဏ ဖြစ်ပြီး၊ SLO မှ ဆင်းသက်သည်။
3. Canary Release သည် traffic ၏ ထိန်းချုပ်ထားသည့် အချိုးအစား တစ်ခုအတွက် တကယ့် အသုံးပြုသူများကို version အသစ်မှ ဝန်ဆောင်ပေးသည်။ Shadow Traffic သည် အသုံးပြုသူ အပေါ် သက်ရောက်မှု မရှိစေရန် ကိုယ်စားလှယ်၏ တုံ့ပြန်မှုကို အဓိက လမ်းကြောင်းပြင်ပတွင် ထားရှိသည်။ သို့သော် မိတ္တူ request သည် လည်ပတ်နေသေးသည့်အတွက် ၎င်း၏ အကျိုးဆက်များကို သီးခြားခွဲထားရမည်။
4. Deadline သည် ကျန်ရှိသည့် ပြီးစီးမှု နယ်နိမိတ် ဖြစ်သည်။ Retry delay သည် နောက်တစ်ကြိမ် ကြိုးစားမှု မည်သည့်အခါ စတင်မည်ကို ထိန်းချုပ်ပြီး၊ ထို deadline budget တစ်ခုတည်းအတွင်းတွင် ပါဝင်ရမည်။ ထို့ကြောင့် independent timeout များသည် အသုံးပြုသူ၏ deadline ကို ကျော်လွန်နိုင်သည်။
5. Readiness Probe သည် traffic ရရှိခွင့်ကို ထိန်းချုပ်သည် — instance တစ်ခု request များ လက်ခံနိုင်သလား ဆုံးဖြတ်သည်။ Liveness သည် process ကို restart လုပ်သင့်/မသင့် ဆုံးဖြတ်သည်။ Readiness false ဖြစ်ခြင်းကြောင့်သာ process ကို restart လုပ်ခြင်း မပြုရ။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT)
- Lessons — [Production LLM Application](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/13-production-app/), [SRE for AI](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/23-sre-for-ai/), [Inference Metrics and Goodput](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/08-inference-metrics-goodput/), [Shadow, Canary, and Progressive Delivery](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/17-infrastructure-and-production/20-shadow-canary-progressive/)
- Papers and documentation — [Google SRE: Handling Overload](https://sre.google/sre-book/handling-overload/), [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/), [Google SRE Workbook: Error Budget Policy](https://sre.google/workbook/error-budget-policy/), [Google SRE: Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/), [Google SRE: Managing Incidents](https://sre.google/sre-book/managing-incidents/), [Google SRE: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/), [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/), [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final), [Kubernetes Deployments: Canary Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#canary-deployment), [Kubernetes Deployments: Rolling Back](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment), [Kubernetes Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/), [gRPC Deadlines](https://grpc.io/docs/guides/deadlines/), [Istio Traffic Mirroring](https://istio.io/latest/docs/tasks/traffic-management/mirroring/), [The Tail at Scale](https://research.google/pubs/the-tail-at-scale/)

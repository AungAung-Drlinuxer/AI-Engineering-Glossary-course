# Area 10 — ပုံရှင်းလင်းချက်များ (Visual Explanations)

Reliability term များကို စာဖြင့်သာ ဖတ်ပါက "မည်သည့် နေရာတွင် စတင် ပျက်သည်၊ မည်သည့် အစိတ်အပိုင်းက
မည်သည့် အစိတ်အပိုင်းကို ကာကွယ်သည်" ဟူသည့် ဆက်စပ်မှု မမြင်ရပါ။ ဤဖိုင်သည် ထို ဆက်စပ်မှုကို ပုံ ၇ ခုဖြင့်
ပြသည် — request လမ်းကြောင်း၏ ချို့ယွင်းသည့် အမှတ်များ၊ queue ပေါ်ရှိ backpressure နှင့် load shedding၊
circuit breaker အခြေအနေစက်၊ timeout နှင့် jitter ပါသည့် retry၊ degradation လှေကား၊ incident timeline နှင့်
SLO error budget အထိ ဖြစ်သည်။

**ပုံများ ကြည့်နည်း** — ဤဖိုင်ကို GitHub တွင် ဖတ်ပါက Mermaid ပုံများ အလိုအလျောက် render ဖြစ်သည်။
ဒေသအတွင်း ဖတ်လိုပါက VS Code ၏ Mermaid extension သို့မဟုတ် mermaid.live တွင် ```mermaid``` block ကို
ကူးထည့်ပါ။

## ၁။ Request လမ်းကြောင်းနှင့် ၎င်း၏ ချို့ယွင်းသည့် အမှတ်များ

```mermaid
flowchart LR
    U["အသုံးပြုသူ"] --> GW["gateway<br/>rate limit"]
    GW --> AD["Admission Control<br/>pre-acceptance gate"]
    AD --> Q["queue<br/>စောင့်ဆိုင်းမှု စုပုံသည်"]
    Q --> APP["အပလီကေးရှင်း<br/>deadline ကို စောင့်ကြည့်သည်"]
    APP --> RET["retrieval dependency"]
    APP --> MDL["model server"]
    APP --> STORE["cache / store"]
    RET --> ANS["အဖြေ"]
    MDL --> ANS
    STORE --> ANS
    F1["ချို့ယွင်းသည့် အမှတ် ၁<br/>demand သည် စွမ်းရည်ကို ကျော်လွန်သည်"]
    F2["ချို့ယွင်းသည့် အမှတ် ၂<br/>queue ကြီးထွား၍ deadline ကုန်သည်"]
    F3["ချို့ယွင်းသည့် အမှတ် ၃<br/>dependency တစ်ခု နှေးကွေး/ချို့ယွင်းသည်"]
    F4["ချို့ယွင်းသည့် အမှတ် ၄<br/>retry များက ဝန်ကို ဆတိုးမြှင့်သည်"]
    F1 -.-> AD
    F2 -.-> Q
    F3 -.-> RET
    F4 -.-> MDL
```

**ဘာကို ကြည့်ရမည်** — ချို့ယွင်းမှု တိုင်းသည် **လမ်းကြောင်းတစ်လျှောက် တစ်နေရာတွင်** ရှိသည်၊
"စနစ် ပျက်သည်" ဟူသည့် အခြေအနေ တစ်ခု မဟုတ်ပါ။ `F1` သည် ingress တွင် စတင်ပြီး `F2` သည်
queue တွင်၊ `F3` သည် dependency တွင်၊ `F4` သည် ပထမ သုံးခု၏ အကျိုးဆက်အဖြစ် ပေါ်လာသည်။
တုံ့ပြန်မှု တိုင်းကို **အစောဆုံး အချက်အလက် ရရှိသည့် နယ်နိမိတ်** တွင် လုပ်ရမည် — `F3` ကို
`ANS` အဆင့်တွင်မှ ကိုင်တွယ်ပါက capacity ကုန်ပြီးသား ဖြစ်နေလိမ့်မည်။
**သက်ဆိုင်သည့် term** — Admission Control, Load Shedding, Deadline Propagation, Saturation, Tail Latency

## ၂။ Queue ပေါ်ရှိ backpressure နှင့် load shedding

```mermaid
flowchart TD
    IN["ဝင်လာသည့် request<br/>arrival rate တိုးသည်"] --> GATE{"Admission Control<br/>budget ကျန်သေးလား"}
    GATE -->|"ကျန်သည်"| QIN["queue ထဲ ထည့်သည်"]
    GATE -->|"မကျန်"| SHED["shed<br/>overload scope ကို ဖော်ထုတ်၍ ငြင်းပယ်"]
    QIN --> QDEPTH{"queue depth သည်<br/>သတ်မှတ်ချက် ကျော်လွန်ပြီလား"}
    QDEPTH -->|"မကျော်သေး"| WORK["ဆောင်ရွက်ခြင်း"]
    QDEPTH -->|"ကျော်လွန်"| DROP["low-priority အလုပ်ကို ဖယ်ရှား"]
    WORK --> OK["deadline အတွင်း ပြီးသည်"]
    WORK -->|"နှေးလာသည်"| BP["backpressure<br/>caller ကို နှေးစေသည်"]
    BP --> GATE
    DROP --> QDEPTH
```

**ဘာကို ကြည့်ရမည်** — backpressure သည် **အလုပ်ကို ငြင်းပယ်ခြင်း မဟုတ်ဘဲ လက်ခံနှုန်းကို
နှေးစေခြင်း** ဖြစ်သည် — downstream က "နောက်မပို့ပါနှင့်" ဟု signal ပြန်ပေးသည့် လမ်း ဖြစ်သည်။
load shedding သည် ထို လုပ်ငန်းစဉ်၏ နောက်ဆုံး အဆင့် ဖြစ်သည် — ငြင်းပယ်ခြင်း၊ ချပစ်ခြင်း သို့မဟုတ်
ပလပ်ဖျက်ခြင်း ဖြစ်သည်။ ပထမ ဆုံးသော အဆင့် (`GATE`) သည် လက်ခံမှု **မပြုမီ** အလုပ်လုပ်သဖြင့်
queue ကြီးထွားမှုကို ဖြစ်မလာမီ ရပ်တန့်စေသည်။ ငြင်းပယ်သည့်အခါ အခြေအနေသည် ယာယီ ဖြစ်ပြီး
caller ၏ retry budget က ခွင့်ပြုသည့်အခါမှသာ retryable အဖြစ် သတ်မှတ်ရမည်။
**သက်ဆိုင်သည့် term** — Admission Control, Load Shedding, Retry Budget, Saturation, Graceful Degradation

## ၃။ Circuit breaker အခြေအနေစက် (closed၊ open၊ half-open)

```mermaid
stateDiagram-v2
    [*] --> closed
    closed --> closed: အောင်မြင်သည့် ခေါ်ဆိုမှုများ
    closed --> open: သတ်မှတ်ထားသည့် window အတွင်း failure rate သတ်မှတ်ချက် ကျော်လွန်
    open --> half_open: cooldown ကုန်ဆုံး
    half_open --> closed: probe များ လုံလောက်စွာ အောင်မြင်
    half_open --> open: probe ကျဆင်းမှု များသည်၊ cooldown ပြန်စ
    open --> open: ခေါ်ဆိုမှုကို ချက်ချင်း ငြင်းပယ်၊ dependency ကို မထိခိုက်စေ
    note right of open
        ဤအခြေအနေတွင် ငြင်းပယ်ခြင်းသည်
        graceful degradation ကို ဖွင့်ပေးသည်
    end note
```

**ဘာကို ကြည့်ရမည်** — circuit breaker သည် **ချို့ယွင်းနေသည့် dependency ကို ခေါ်ဆိုမှုများဖြင့်
ထပ်မံ တိုက်ခိုက်ခြင်း** ကို ရပ်တန့်သည့် နည်းလမ်း ဖြစ်သည်။ `closed` သည် ပုံမှန် လည်ပတ်မှု၊ `open`
သည် ခေါ်ဆိုမှုကို ချက်ချင်း ငြင်းပယ်၍ dependency ကို အသက်ရှူခွင့် ပေးသည့် အခြေအနေ၊ `half_open` သည်
probe အနည်းငယ်ဖြင့် ပြန်လည် ကောင်းမွန်မှုကို စမ်းသပ်သည့် အခြေအနေ ဖြစ်သည်။ half-open တွင်
probe အရေအတွက် ကန့်သတ်ချက် **မရှိပါက** breaker သည် ဝန်ကို ပြန်လည် တိုးပေးသဖြင့် အန္တရာယ်ရှိသည်။
**သက်ဆိုင်သည့် term** — Graceful Degradation, Readiness Probe, Retry Budget, Availability, Tail Latency

## ၄။ Timeout နှင့် jitter ပါသည့် retry

```mermaid
sequenceDiagram
    participant C as Caller (deadline 2000 ms)
    participant A as service
    participant D as dependency
    C->>A: request (t = 0)
    Note over C: deadline တစ်ခုတည်း — 2000 ms
    A->>D: ခေါ်ဆိုမှု (remaining budget 1800 ms)
    D--xA: timeout (t = 1400 ms)
    Note over C,A: ကျန်ရှိသည့် budget 600 ms
    A->>A: backoff 200 ms + jitter 0 .. 100 ms
    A->>D: retry (t = 1700 ms)
    D--xA: timeout ထပ်ဖြစ် (t = 2000 ms တွင် ပလပ်ဖျက်)
    Note over C,A: budget ကုန် — အလုပ်ကို စွန့်ပစ်သည်
```

**ဘာကို ကြည့်ရမည်** — retry တစ်ကြိမ် လုပ်ရန် **အချိန် သုံးခု** လိုသည် — backoff၊ jitter နှင့်
ခေါ်ဆိုမှု ကိုယ်တိုင်၏ ကြာချိန်။ သုံးခုလုံးသည် မူလ deadline ၏ ကျန်ရှိသည့် budget ထဲတွင် ပါရမည်။
jitter မထည့်ပါက client များအားလုံး တစ်ချိန်တည်း ပြန်လည် ကြိုးစားသဖြင့် dependency အပေါ်
လှိုင်း (thundering herd) ဖြစ်စေသည်။ `Deadline Propagation` မရှိပါက dependency တိုင်းသည်
မိမိ၏ timeout ကို သီးခြား ရေတွက်သဖြင့် အသုံးပြုသူ deadline ကို ကျော်လွန်သည့် အလုပ်များ
capacity ကို စားသုံးနေစေသည်။
**သက်ဆိုင်သည့် term** — Deadline Propagation, Retry Budget, Tail Latency, Service Level Objective (SLO)

## ၅။ Degradation လှေကား — အရည်အသွေး အပြည့်မှ cached အဖြေအထိ

```mermaid
flowchart TD
    L0["အဆင့် ၀ — အရည်အသွေး အပြည့်<br/>အပြည့်အစုံ model၊ လက်ရှိ data၊ feature အားလုံး"] --> L1["အဆင့် ၁ — optional feature ပိတ်<br/>အညွှန်း၊ အကြံပြုချက်၊ အပိုဆောင်း ခေါ်ဆိုမှုများ ရပ်"]
    L1 --> L2["အဆင့် ၂ — အလုပ်ပမာဏ လျှော့<br/>batch သေးစေ၊ output အရှည် ကန့်သတ်၊ retry ရပ်"]
    L2 --> L3["အဆင့် ၃ — ကုန်ကျစရိတ် နည်းသည့် လမ်းကြောင်း<br/>model router က မော်ဒယ် အသေးသို့ ပို့"]
    L3 --> L4["အဆင့် ၄ — cached သို့မဟုတ် ရှေးဟောင်း အဖြေ<br/>freshness လျော့သည်၊ အသုံးပြုသူကို အသိပေးရမည်"]
    L4 --> L5["အဆင့် ၅ — အဓိက အဖြေ မပေးနိုင်<br/>ရှင်းလင်းသည့် မက်ဆေ့ခ်ျ နှင့် retry အကြံပြုချက်"]
    SAFE["safety စစ်ဆေးမှုများ — လျှော့ချ mode တိုင်းတွင် မပိတ်ရ"] -.-> L2
    SAFE -.-> L3
    SAFE -.-> L4
    VIS["operator visibility<br/>လျှော့ချ mode ကို metric နှင့် log တွင် မြင်ရမည်"] -.-> L1
    VIS -.-> L4
```

**ဘာကို ကြည့်ရမည်** — လှေကား အဆင့် တိုင်းသည် **ကြိုတင် သတ်မှတ်ထားရမည့် ဆုံးဖြတ်ချက်** ဖြစ်သည် —
အကျပ်အတည်း ဖြစ်နေစဉ်တွင် ဆုံးဖြတ်နိုင်မည် မဟုတ်ပါ။ အောက်သို့ ဆင်းသည့် အဆင့် တိုင်းတွင်
အသုံးပြုသူ ရလဒ်သည် သိသိသာသာ ပြောင်းလဲသဖြင့် မြင်တွေ့နိုင်မှု (visibility) နှင့် အသိပေးခြင်း
လိုအပ်သည်။ လျှော့ချ mode သည် "ဘာမျှ မဖြစ်သကဲ့သို့" ပိုဆိုးသည့် အဖြေကို တိတ်ဆိတ်စွာ
ပြန်ပေးခြင်း မဟုတ်ပါ။ ဝန်ဆောင်မှု အပြည့်အဝကို **တမင်တကာ** ပြန်လည် ရယူရမည်။
**သက်ဆိုင်သည့် term** — Graceful Degradation, Load Shedding, Readiness Probe, Availability, Incident Response

## ၆။ Incident timeline — alert မှ postmortem အထိ

```mermaid
flowchart LR
    T0["t + 0<br/>alert ဖြစ်သည်<br/>SLI ကျဆင်းမှုကို ဖမ်းမိသည်"] --> T1["t + 4 min<br/>acknowledge နှင့် triage<br/>severity၊ incident commander သတ်မှတ်"]
    T1 --> T2["t + 6 min<br/>ဆက်သွယ် အသိပေး<br/>သက်ရောက်မှုကို ကြေညာ"]
    T2 --> T3["t + 16 min<br/>mitigate<br/>rollback၊ canary ရပ်၊ shed ဖွင့်"]
    T3 --> T4["t + 24 min<br/>recovery စစ်ဆေး<br/>SLI ပြန်တက်၊ error rate ကျ"]
    T4 --> T5["t + 1 day<br/>postmortem<br/>timeline၊ အကြောင်းရင်း၊ လုပ်ဆောင်ချက်"]
    T5 --> T6["ရက်စွဲပါ လုပ်ဆောင်ချက်များ<br/>အပြီးသတ် လိုက်ပါ ဆောင်ရွက်"]
    T5 -.-> T0
```

**ဘာကို ကြည့်ရမည်** — timeline ကို **အပိုင်း လေးပိုင်း** ခွဲကြည့်ရမည် — ဖော်ထုတ်ချိန် (t + 0 မှ t + 4)၊
ထိန်းချုပ်ချိန် (t + 4 မှ t + 16)၊ ပြန်လည် ကောင်းမွန်ချိန် (t + 16 မှ t + 24) နှင့် သင်ယူချိန် (t + 24 မှ
postmortem)။ error budget ကို စားသုံးသည့် ပမာဏသည် **အပိုင်းတိုင်း၏ ကြာချိန်** အပေါ် တိုက်ရိုက်
မူတည်သည်၊ ထို့ကြောင့် detect ချိန် တိုစေခြင်းသည် recovery လျင်မြန်စေခြင်းနှင့် တူညီသည့် တန်ဖိုး
ရှိသည်။ postmortem သည် timeline ကို trace နှင့် log များမှ တည်ဆောက်ပြီး **လုပ်ဆောင်ချက် တစ်ခုချင်းက
သက်ဆိုင်ရာ control ကို ပြောင်းလဲခဲ့သလား** ပြန်လည် သုံးသပ်ရမည်။
**သက်ဆိုင်သည့် term** — Incident Response, Postmortem, Error Budget, Service Level Indicator (SLI), Rollback

## ၇။ SLO နှင့် ၎င်း၏ error budget

```mermaid
flowchart TD
    SLI["Service Level Indicator (SLI)<br/>အောင်မြင်သည့် request အချိုးအစား<br/>numerator၊ denominator၊ exclusions သတ်မှတ်သည်"] --> SLO["Service Level Objective (SLO)<br/>ဥပမာ 99.9% / 30 days<br/>population နှင့် window ပါရမည်"]
    SLO --> BUD["Error Budget<br/>(1 − SLO) × eligible<br/>ဥပမာ 0.1% × 2,000,000 = 2,000 request<br/>= 43.2 မိနစ်"]
    BUD --> BURN["burn rate<br/>budget ကုန်သည့် အရှိန်နှင့်<br/>တစ်နာရီအတွင်း ကုန်သည့် %"]
    BURN --> P1["fast burn<br/>1 h window တွင် 2% ကုန်သည်<br/>burn 14.4 x → page"]
    BURN --> P2["slow burn<br/>6 h window တွင် 5% ကုန်သည်<br/>burn 6 x → ticket"]
    BURN --> P3["budget ကုန်ဆုံး<br/>release လုပ်ဆောင်ချက်များ ရပ်၊<br/>reliability အလုပ်သို့ ဦးစားပေး ပြောင်း"]
    P3 --> REVIEW["policy ပြန်လည် သုံးသပ်ခြင်း<br/>SLO သည် လက်ရှိ စွမ်းဆောင်ရည်အတွက်<br/>လက်တွေ့ကျ/မကျ စစ်သည်"]
```

**ဘာကို ကြည့်ရမည်** — error budget သည် SLO မှ **ဆင်းသက်** လာသည့် ပမာဏ ဖြစ်သည်၊ သီးခြား
သတ်မှတ်သည့် ကိန်းဂဏန်း မဟုတ်ပါ။ burn rate သည် ထို budget ကို မည်သည့် အရှိန်ဖြင့်
စားသုံးနေသည်ကို ပြသဖြင့် **တူညီသည့် ပမာဏ** ကို အချိန်နှစ်မျိုးဖြင့် တိုင်းတာနိုင်သည် — အမြန်
ဖြစ်ပွားသည့် incident နှင့် နှေးကွေးစွာ တိုးလာသည့် ယုတ်လျော့မှု နှစ်မျိုးလုံးကို မြင်နိုင်ရမည်။
window တို (1 h) ပါက ဖော်ထုတ်မှု မြန်သည်၊ သို့သော် ဆူညံသံ (noise) များသည်၊ window ရှည် (6 h)
ပါက တည်ငြိမ်သည်၊ သို့သော် အန္တရာယ်ကို နောက်ကျမှ သိသည် — ထို့ကြောင့် window နှစ်ခုကို
တွဲသုံးရသည်။
**သက်ဆိုင်သည့် term** — Service Level Indicator (SLI), Service Level Objective (SLO), Error Budget, Availability, Incident Response

## ပုံတိုင်းနှင့် term ချိတ်ဆက်မှု

| ပုံ | ပြသည့် အကြောင်းအရာ | သက်ဆိုင်သည့် term |
|---|---|---|
| ၁ | Request လမ်းကြောင်းနှင့် ချို့ယွင်းသည့် အမှတ် ၄ ခု | Admission Control, Load Shedding, Deadline Propagation, Saturation, Tail Latency |
| ၂ | Queue ပေါ်ရှိ backpressure နှင့် load shedding | Admission Control, Load Shedding, Retry Budget, Saturation, Graceful Degradation |
| ၃ | Circuit breaker — closed၊ open၊ half-open | Graceful Degradation, Readiness Probe, Retry Budget, Availability, Tail Latency |
| ၄ | Timeout နှင့် jitter ပါသည့် retry | Deadline Propagation, Retry Budget, Tail Latency, Service Level Objective (SLO) |
| ၅ | Degradation လှေကား — အရည်အသွေး အပြည့်မှ cached အဖြေအထိ | Graceful Degradation, Load Shedding, Readiness Probe, Availability, Incident Response |
| ၆ | Incident timeline — alert မှ postmortem အထိ | Incident Response, Postmortem, Error Budget, Service Level Indicator (SLI), Rollback |
| ၇ | SLO နှင့် error budget၊ burn rate policy | Service Level Indicator (SLI), Service Level Objective (SLO), Error Budget, Availability, Incident Response |

## နောက်တစ်ဆင့်

- ကိန်းဂဏန်း အဖြစ် မြင်လိုပါက — [`04_exercises.md`](04_exercises.md) (error budget၊ queueing latency၊ timeout budget၊ alert နှုန်း)
- အဆင့်လိုက် ဖတ်ရန် — [`01_learning_sequence.md`](01_learning_sequence.md)
- Term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် — [`../../terms/10_reliability_and_operations.md`](../../terms/10_reliability_and_operations.md)

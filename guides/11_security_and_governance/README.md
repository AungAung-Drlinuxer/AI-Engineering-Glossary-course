# Area 11 — Security & Governance (terms + glossary shortcut)

<!-- guide-kind: terms-only -->

ဤဖိုင်သည် area 11 ၏ term ၂၀ ခုကို **အဓိပ္ပာယ် အတိုချုံး (shortcut)** ဖြင့် ဖတ်ရန် ဖြစ်သည်။
term တိုင်းတွင် English အမည်၊ မြန်မာ အမည်နှင့် အဓိပ္ပာယ် ၁–၃ ကြောင်း သာ ပါသည်။
term ၂၀ ခုကို အဆင့် ၅ ခုအဖြစ် စီထားသည် — ဘာကို ကာကွယ်သည်၊ မည်သူက ဘာလုပ်နိုင်သည်၊
data ကိုယ်တိုင် ကာကွယ်ခြင်း၊ သက်သေပြခြင်း၊ တိုက်ခိုက်မှု စမ်းသပ်ခြင်း ဖြစ်သည်။

## ၁။ ကာကွယ်ရမည့် အရာနှင့် ရန်သူ

### Threat Model
**မြန်မာ:** အန္တရာယ် ပုံစံ ရေးဆွဲခြင်း
ကာကွယ်ရမည့် asset၊ trust boundary၊ ဖြစ်နိုင်သည့် ရန်သူနှင့် တိုက်ခိုက်သည့် လမ်းကြောင်းများကို မှတ်တမ်းတင်ထားသည့် ဖော်ပြချက် ဖြစ်သည်။ control တစ်ခုကို မည်သည့်အရာကို ကာကွယ်သည်၊ မည်သူကို ဆန့်ကျင်သည် ကို မဖော်ပြဘဲ အကဲဖြတ်နိုင်မည် မဟုတ်ပါ။
ဆက်စပ် — Least Privilege, Prompt Injection, Sandbox, Red Teaming

### AI Risk Assessment
**မြန်မာ:** AI အန္တရာယ် အကဲဖြတ်ခြင်း
AI စနစ်တစ်ခုသည် လူ၊ အဖွဲ့အစည်းနှင့် ပတ်ဝန်းကျင်အပေါ် မည်သို့ သက်ရောက်နိုင်သည်ကို ခွဲခြမ်းစိတ်ဖြာထားသည့် မှတ်တမ်း ဖြစ်သည်။ context၊ hazard၊ ဖြစ်နိုင်ခြေ၊ သက်ရောက်မှု၊ control၊ residual risk နှင့် စောင့်ကြည့်ရန် တာဝန်ရှိသူများ ပါဝင်သည်။
ဆက်စပ် — Threat Model, Guardrails, Human-in-the-Loop (HITL), Data Classification

### Trust Boundary
**မြန်မာ:** ယုံကြည်မှု နယ်နိမိတ်
ယုံကြည်မှု ယူဆချက် မတူညီသည့် component များ သို့မဟုတ် လုပ်ဆောင်သူများအကြား data၊ ညွှန်ကြားချက်၊ identity သို့မဟုတ် အာဏာ ဖြတ်ကူးသည့် မျက်နှာပြင် ဖြစ်သည်။ ထို ဖြတ်ကူးသည့် နေရာတိုင်းတွင် authenticate၊ validate နှင့် permission ကန့်သတ်မှု လိုသည်။
ဆက်စပ် — Threat Model, Least Privilege, Sandbox, Indirect Prompt Injection

### Data Classification
**မြန်မာ:** data အဆင့်တန်း သတ်မှတ်ခြင်း
data ကို sensitivity သို့မဟုတ် သက်ရောက်မှု အဆင့်တန်းများအဖြစ် သတ်မှတ်ခြင်း ဖြစ်သည်။ ထိုသို့ သတ်မှတ်မှသာ ကိုင်တွယ်ခြင်း၊ access၊ ထိန်းသိမ်းခြင်းနှင့် မျှဝေခြင်း စည်းမျဉ်းများသည် ဖော်ထုတ်ခံရမှု၏ အကျိုးဆက်အတိုင်း လိုက်နာစေသည်။
ဆက်စပ် — Data Minimization, Trust Boundary, Least Privilege, Audit Log

## ၂။ မည်သူက ဘာလုပ်နိုင်သည်

### Zero Trust
**မြန်မာ:** zero trust (ယုံကြည်မှု သုည ပုံစံ)
network တည်နေရာ သို့မဟုတ် asset ပိုင်ဆိုင်မှုမှ သွယ်ဝိုက် ယုံကြည်မှု မပေးသည့် လုံခြုံရေး model ဖြစ်သည်။ access တောင်းခံမှု တိုင်းကို identity၊ device၊ resource၊ policy နှင့် လက်ရှိ context အလိုက် အကဲဖြတ်သည်။
ဆက်စပ် — Least Privilege, Trust Boundary, Approval Gate, Audit Log

### Separation of Duties
**မြန်မာ:** တာဝန် ခွဲခြားခြင်း
ပဋိပက္ခ ဖြစ်သည့် တာဝန်များ သို့မဟုတ် အာဏာများကို အမှီအခိုကင်းသည့် role များအကြား ခွဲဝေခြင်း ဖြစ်သည်။ ထို့ကြောင့် principal တစ်ခုတည်းသည် အန္တရာယ်မြင့်သည့် လုပ်ဆောင်ချက်ကို အဆိုပြုခြင်း၊ အတည်ပြုခြင်းနှင့် ဆောင်ရွက်ခြင်း အားလုံး မလုပ်နိုင်ပါ။
ဆက်စပ် — Approval Gate, Reviewer Agent, Audit Log, Least Privilege

### Defense in Depth
**မြန်မာ:** အလွှာလိုက် ကာကွယ်မှု
system boundary အများအပြားတွင် တစ်ခုနှင့်တစ်ခု အမှီအခိုကင်းသည့် preventive၊ detective နှင့် corrective control များကို အသုံးပြုခြင်း ဖြစ်သည်။ ထို့ကြောင့် control တစ်ခု ပျက်ကွက်လျှင် ရလဒ်ကို ၎င်းတစ်ခုတည်းက မဆုံးဖြတ်နိုင်ပါ။
ဆက်စပ် — Guardrails, Sandbox, Least Privilege, Trust Boundary

### Data Exfiltration
**မြန်မာ:** data ခွင့်ပြုချက်မရှိဘဲ ယူဆောင်ခြင်း
ကာကွယ်ထားသည့် data ကို လက်ခံခွင့် မရှိသည့် လူ၊ tool၊ service သို့မဟုတ် သိုလှောင်ရာ နေရာသို့ ခွင့်ပြုချက် မရှိဘဲ လွှဲပြောင်းခြင်း ဖြစ်သည်။ မူလ data store မပျက်စီးဘဲ ရှိနေသည့် အချိန်တွင်ပင် agent ၏ စာသား၊ tool argument၊ URL သို့မဟုတ် log မှတစ်ဆင့် secret များ ဖော်ထုတ်ခံရနိုင်သည်။
ဆက်စပ် — Trust Boundary, Least Privilege, Indirect Prompt Injection, Audit Log

## ၃။ data ကိုယ်တိုင် ကာကွယ်ခြင်း

### Data Minimization
**မြန်မာ:** data အနည်းဆုံး အသုံးပြုခြင်း
သတ်မှတ်ထားသည့် ရည်ရွယ်ချက် တစ်ခုအတွက် လိုအပ်သည့် ပမာဏအတိုင်းသာ စုဆောင်းခြင်း၊ ဆောင်ရွက်ခြင်း၊ ဖော်ထုတ်ခြင်းနှင့် ထိန်းသိမ်းခြင်းကို ကန့်သတ်ခြင်း ဖြစ်သည်။ prompt၊ trace၊ cache သို့မဟုတ် tool call ထဲသို့ ထည့်သည့် မလိုအပ်သည့် field တိုင်းသည် ဖော်ထုတ်ခံရမှုကို တိုးစေသည်။
ဆက်စပ် — Purpose Limitation, Data Classification, Least Privilege, Context Engineering

### Purpose Limitation
**မြန်မာ:** ရည်ရွယ်ချက် ကန့်သတ်မှု
personal data ကို သတ်မှတ်ပြီး ရှင်းလင်းသည့် ရည်ရွယ်ချက်များအတွက်သာ စုဆောင်းခြင်းနှင့် အသုံးပြုခြင်း ဖြစ်သည်။ workflow တစ်ခုအတွက် လက်ခံနိုင်သည့် data သည် model training၊ evaluation သို့မဟုတ် မသက်ဆိုင်သည့် analytics အတွက် တိတ်ဆိတ်စွာ ပြန်လည် အသုံးပြုသည့်အခါ အန္တရာယ် ဖြစ်လာသည်။
ဆက်စပ် — Data Minimization, Data Classification, AI Risk Assessment, Audit Log

### Data Lineage
**မြန်မာ:** data ဆင်းသက်မှု လမ်းကြောင်း
data artifact တစ်ခုသည် source၊ transformation၊ join၊ filter၊ version နှင့် နောက်ဆက်တွဲ အသုံးပြုမှုများကို ဖြတ်သန်း၍ မည်သို့ ဆင်းသက်လာသည်ကို မှတ်တမ်းတင်ထားခြင်း ဖြစ်သည်။ source တစ်ခုကို ပြင်ဆင်ခြင်း သို့မဟုတ် ရုပ်သိမ်းခြင်း ဖြစ်သည့်အခါ သက်ရောက်နိုင်သည့် dataset၊ embedding၊ evaluation နှင့် model artifact များကို ဖော်ထုတ်ပေးသည်။
ဆက်စပ် — Data Provenance, Datasheet for Datasets, Audit Log, Content Provenance

### Datasheet for Datasets
**မြန်မာ:** dataset အတွက် datasheet
dataset တစ်ခု၏ ရည်ရွယ်ချက်၊ ဖွဲ့စည်းမှု၊ စုဆောင်းသည့် လုပ်ငန်းစဉ်၊ preprocessing၊ အသုံးပြုမှု၊ ဖြန့်ဖြူးမှုနှင့် သိရှိထားသည့် ကန့်သတ်ချက်များကို ဖွဲ့စည်းထားသည့် အတိုင်း မှတ်တမ်းတင်ခြင်း ဖြစ်သည်။ dataset တစ်ခုသည် ရရှိနိုင်သည် ဆိုသည့် အချက်တစ်ချက်တည်းဖြင့် ဘေးကင်းသည် မဟုတ်ပါ။
ဆက်စပ် — Data Lineage, Data Provenance, Model Card, Dataset Split

## ၄။ ဖြစ်ပွားခဲ့သည့် အရာ သက်သေပြခြင်း

### Audit Log
**မြန်မာ:** စစ်ဆေးစာရင်း မှတ်တမ်း
မည်သူ သို့မဟုတ် မည်သည့် အရာက ဆောင်ရွက်ခဲ့သည်၊ မည်သည့်အရာ ပြောင်းလဲခဲ့သည်၊ မည်သည့်အချိန်တွင် ဖြစ်ပွားခဲ့သည်နှင့် ရရှိသည့် status ကို ကြာရှည်ခံ၍ access control ဖြင့် ကာကွယ်ထားသည့် မှတ်တမ်း ဖြစ်သည်။ အကျိုးဆက် ရှိသည့် agent လုပ်ဆောင်ချက်များအတွက် performance debug လုပ်ခြင်းထက် ကျော်လွန်သည့် အထောက်အထား လိုသည်။
ဆက်စပ် — Trace, Observability, Approval Gate, Provenance Attestation

### Content Provenance
**မြန်မာ:** အကြောင်းအရာ၏ မူလဇာစ်မြစ်
media တစ်ခု သို့မဟုတ် digital content တစ်ခု၏ မူလရင်းမြစ်နှင့် တည်းဖြတ်မှု သမိုင်းကြောင်းအပေါ် စစ်ဆေး အတည်ပြုနိုင်သည့် အချက်အလက် ဖြစ်သည်။ မည်သူ ကြေညာခဲ့သည် နှင့် မှတ်တမ်းကို ပြောင်းလဲခဲ့မှု ရှိမရှိ ကို အတည်ပြုနိုင်သည်၊ သို့သော် content မှန်ကန်သည် ဆိုသည်ကို သက်သေမပြနိုင်ပါ။
ဆက်စပ် — Data Provenance, Provenance Attestation, Audit Log, Grounding

### Provenance Attestation
**မြန်မာ:** မူလဇာစ်မြစ် အတည်ပြုချက်
artifact တစ်ခုကို မည်သို့၊ မည်သည့်နေရာတွင်၊ မည်သည့်အချိန်တွင်၊ မည်သည့် input များမှ ထုတ်လုပ်ခဲ့သည်ဆိုသည့် ကြေညာချက်များနှင့် ချိတ်ဆက်ပေးသည့်၊ စစ်မှန်ကြောင်း အတည်ပြုထားသည့် machine-readable metadata ဖြစ်သည်။ လက်မှတ် မထိုးထားသည့် build note ကို ယုံကြည်ခြင်းအစား supply-chain ကြေညာချက်များကို စစ်ဆေးနိုင်စေသည်။
ဆက်စပ် — Data Provenance, Reproducible Build, Audit Log, Verification Gate

### Software Bill of Materials (SBOM)
**မြန်မာ:** software အစိတ်အပိုင်း စာရင်း
product တစ်ခု သို့မဟုတ် artifact တစ်ခုနှင့် သက်ဆိုင်သည့် software component များနှင့် ၎င်းတို့၏ ဆက်စပ်မှုများကို ဖွဲ့စည်းထားသည့် စာရင်း ဖြစ်သည်။ version၊ supplier၊ license နှင့် identifier များ ပါဝင်လေ့ ရှိသည်။ vulnerability တစ်ခု ပေါ်ပေါက်သည့်အခါ သက်ရောက်သည့် dependency များကို အကဲဖြတ်ရန် ထို စာရင်း လိုသည်။
ဆက်စပ် — Provenance Attestation, Reproducible Build, Data Provenance, Audit Log

## ၅။ တိုက်ခိုက်မှု စမ်းသပ်ခြင်း

### Indirect Prompt Injection
**မြန်မာ:** သွယ်ဝိုက် prompt injection
သုံးစွဲသူ၏ ညွှန်ကြားချက်မှတစ်ဆင့် တိုက်ရိုက် မဟုတ်ဘဲ စနစ်က ရယူသည် သို့မဟုတ် လေ့လာသည် ဖြစ်သည့် အကြောင်းအရာ (webpage၊ document၊ email၊ ရုပ်ပုံ အတွင်း စာသား သို့မဟုတ် tool ရလဒ်) မှတစ်ဆင့် ပို့ဆောင်သည့် prompt-injection တိုက်ခိုက်မှု ဖြစ်သည်။ သယ်ဆောင်သည့် လမ်းကြောင်း ကွာခြားရုံသာ ဖြစ်သည်၊ ပိုအားနည်းသည့် တိုက်ခိုက်မှု မဟုတ်ပါ။
ဆက်စပ် — Prompt Injection, Instruction Hierarchy, Trust Boundary, Data Exfiltration

### Jailbreak
**မြန်မာ:** jailbreak (မော်ဒယ်၏ ကန့်သတ်ချက် ကျော်လွှားခြင်း)
မော်ဒယ်၏ training သို့မဟုတ် application control များ ကာကွယ်ရန် ရည်ရွယ်ထားသည့် အပြုအမူကို ထုတ်လုပ်စေရန် ရည်ရွယ်သည့် ရန်လိုသည့် input သို့မဟုတ် အပြန်အလှန် ဆက်သွယ်သည့် နည်းဗျူဟာ ဖြစ်သည်။ အောင်မြင်သည့် jailbreak များသည် ကြေညာထားသည့် policy နှင့် တကယ့် အပြုအမူအကြား ကွာဟချက်ကို ဖော်ထုတ်ပေးသည်။
ဆက်စပ် — Prompt Injection, Red Teaming, Guardrails, Eval Set

### Membership Inference
**မြန်မာ:** အဖွဲ့ဝင်ဖြစ်မှု ခန့်မှန်းသည့် တိုက်ခိုက်မှု
မော်ဒယ်၏ output များ သို့မဟုတ် အခြား ရရှိနိုင်သည့် အချက်ပြမှုများကို လေ့လာ၍ record တစ်ခု သည် training data ထဲတွင် ပါဝင်ခဲ့သည် မပါဝင်ခဲ့သည် ကို ခန့်မှန်းသည့် တိုက်ခိုက်မှု ဖြစ်သည်။ record ကို စာလုံးတစ်လုံးမှ မပြန်ထုတ်သည့် အခြေအနေတွင်ပင် ခွဲခြားနိုင်သည့် အပြုအမူက sensitive dataset တွင် ပါဝင်ခဲ့မှုကို ဖော်ထုတ်နိုင်သည်။
ဆက်စပ် — Data Leakage, Data Minimization, Eval Set, Data Classification

### Red Teaming
**မြန်မာ:** red teaming (ရန်လို စမ်းသပ်ခြင်း)
ခွင့်ပြုချက် ရရှိသည့် စမ်းသပ်သူများသည် မှတ်တမ်းတင်ထားသည့် ရည်မှန်းချက်၊ အန္တရာယ် ယူဆချက်၊ အခြေအနေနှင့် အထောက်အထားများကို အသုံးပြု၍ ပျက်ကွက်မှုများကို ရှာဖွေသည့် ဖွဲ့စည်းထားသည့် ရန်လို စမ်းသပ်ခြင်း လုပ်ငန်းစဉ် ဖြစ်သည်။ အတည်ပြုပြီးသည့် ပျက်ကွက်မှုများကို regression eval များအဖြစ် ပြောင်းလဲသိမ်းဆည်းသည်။
ဆက်စပ် — Threat Model, Guardrails, Prompt Injection, Eval Set

## မှီခိုသည့် ဖိုင်

- term တိုင်း၏ အပြည့်အစုံ အဓိပ္ပာယ် (အင်္ဂလိပ် source အပါ) — [`../../terms/11_security_and_governance.md`](../../terms/11_security_and_governance.md)
- Source glossary — [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) (MIT, `rohitg00/ai-engineering-from-scratch`)

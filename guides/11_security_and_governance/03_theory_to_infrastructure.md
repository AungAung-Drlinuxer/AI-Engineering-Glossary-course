# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၁၁ ၏ term ၂၀ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။
လုံခြုံရေးနှင့် အုပ်ချုပ်မှု term တစ်ခုသည် မူဝါဒ စာတမ်းအတွင်းသာ မကျန်ရပါ။ ၎င်းသည်
memory သို့မဟုတ် isolation နယ်နိမိတ်၊ enforcement overhead၊ latency၊ audited traffic ၏
throughput၊ ထိန်းချုပ်မှုနှင့် ဖြစ်ရပ် (incident) ၏ ကုန်ကျစရိတ်၊ သို့မဟုတ် ထုတ်လုပ်မှု
အကျိုးဆက် အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းဂဏန်း တစ်ခုစီသည်
ထုတ်လုပ်မှု အခြေအနေတွင် တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/11_security_and_governance/scripts/` အောက်ရှိ Python script သုံးခုမှ
ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုသည်၊ offline
ဖြစ်သည်၊ deterministic ဖြစ်သည်၊ network သို့မဟုတ် accelerator မလိုအပ်ပါ။ ဤစာတမ်းသည်
benchmark ရလဒ် များကို ဖော်ပြခြင်း မပြုပါ။ ဖော်ပြသည့် တန်ဖိုး အားလုံးသည် ဖော်မြူလာ
နှင့် ယူဆချက် (assumption) မှ တွက်ချက်ထားသည့် တန်ဖိုးများ ဖြစ်သည်။ rate၊ စျေးနှုန်း
နှင့် likelihood တိုင်းကို assumption ဟု မှတ်သားထားသည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**memory and isolation boundary** — သိုလှောင်ထားသည့် byte ပမာဏ၊ ထိန်းသိမ်းထားသည့်
metadata အရေအတွက်၊ သို့မဟုတ် လက်လှမ်းမီနိုင်သည့် resource scope ဖြစ်သည်။ audit log
နှင့် data lineage metadata သည် ဤဝင်ရိုးကို တိုးစေပြီး data minimization နှင့်
least privilege သည် ဤဝင်ရိုးကို လျှော့စေသည်။ ဤဝင်ရိုးသည် နယ်နိမိတ် တစ်ခုအတွင်း
မည်သည့် data နှင့် မည်သည့် authority ကို ထည့်ထားသည်ကို ဖော်ပြသည်။

**compute and enforcement overhead** — စစ်ဆေးမှု၊ လက်မှတ်ထိုးမှု (signature) နှင့်
စာရွက်စာတမ်း ထုတ်လုပ်မှုအတွက် ကုန်သည့် CPU သို့မဟုတ် accelerator အချိန် ဖြစ်သည်။
defense in depth ကဲ့သို့ အလွှာ တိုးလျှင် ဤ overhead တိုးသည်၊ သို့သော် ဤ overhead သည်
request တစ်ခုစီ၏ လမ်းကြောင်းတွင် မဖြစ်မနေ ပါဝင်သည် မဟုတ်ပါ။ build-time နှင့်
online enforcement ကို ဤနေရာတွင် ခွဲခြားရမည်။

**latency of a policy or redaction check** — request တစ်ခု၏ တိုက်ရိုက် လမ်းကြောင်းတွင်
မူဝါဒ သို့မဟုတ် redaction စစ်ဆေးမှု ထည့်လျှင် တိုးလာသည့် မီလီစက္ကန့် ဖြစ်သည်။
p50 နှင့် p95 နှစ်မျိုးဖြင့် တိုင်းတာသည်၊ အကြောင်းမှာ queueing ကြောင့် အမြီးပိုင်း
နှောင့်နှေးမှုသည် မျှော်မှန်း တန်ဖိုးထက် ပိုမြင့်နိုင်သည်။ ဤဝင်ရိုးသည်
အသုံးပြုသူ ခံစားရသည့် latency နှင့် တိုက်ရိုက် ဆက်စပ်သည်။

**throughput of audited traffic** — တစ်စက္ကန့် သို့မဟုတ် တစ်ရက် လျှင် မှတ်တမ်းတင်ရမည့်
event အရေအတွက် ဖြစ်သည်။ audited traffic တိုးလျှင် log ပမာဏ၊ သိုလှောင်မှု နှင့်
စုံစမ်းစစ်ဆေးမှု လုပ်နိုင်စွမ်း လိုအပ်ချက် တိုးသည်။ ဤကိန်းသည် request rate နှင့်
တစ်ခု အစီအစဉ်အတိုင်း ကြီးထွားသည်။

**cost of controls and of incidents** — ထိန်းချုပ်မှု တစ်ခု ထည့်ခြင်း၏ တစ်နှစ်
ကုန်ကျစရိတ် နှင့် ထိုထိန်းချုပ်မှု မရှိလျှင် ဖြစ်နိုင်သည့် မျှော်မှန်း ဆုံးရှုံးမှု ဖြစ်သည်။
break-even ကုန်ကျစရိတ်သည် ဤနှစ်ခုကို နှိုင်းယှဉ်သည့် ကိန်း ဖြစ်သည်။ ဤဝင်ရိုးသည်
ငွေကြေး ဆုံးဖြတ်ချက် ဖြစ်သည့်အတွက် လုံခြုံရေး အဖွဲ့ နှင့် ထုတ်ကုန် အဖွဲ့ အတူတကွ
ဆုံးဖြတ်ရမည့် အချက် ဖြစ်သည်။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် deployment တွင် မည်သည့်
အရာ ကျိုးပျက်မည်၊ သို့မဟုတ် မည်သူ ထိခိုက်မည်ကို ဆိုလိုသည်။ ကျိုးပျက်မှုသည်
service ရပ်တန့်ခြင်း ဖြစ်နိုင်သည်၊ ဒေတာ ပေါက်ကြားခြင်း သို့မဟုတ် စစ်ဆေးစစ်မှု
မဖြေနိုင်ခြင်း လည်း ဖြစ်နိုင်သည်။ ဤဝင်ရိုးသည် ကျန်ဝင်ရိုး ငါးခုကို မည်သည့်
ဦးစားပေး အစီအစဉ်ဖြင့် ဖြေရှင်းမည်ကို ဆုံးဖြတ်သည်။

## ၂။ Master table — term ၂၀ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| AI Risk Assessment | cost of controls and of incidents | ခွဲခြမ်းစိတ်ဖြာမှု အချိန် ကုန်သည်၊ ဖြစ်ရပ် ကုန်ကျစရိတ် လျော့သည် | မျှော်မှန်း ဆုံးရှုံးမှု USD/year | ထိန်းချုပ်မှု ဘတ်ဂျက် ခွဲဝေမှုကို ဆုံးဖြတ်သည် |
| Audit Log | throughput of audited traffic | သိုလှောင်မှု နှင့် စျေးနှုန်း တိုးသည် | records/day၊ storage GB၊ USD/month | စုံစမ်းစစ်ဆေးနိုင်မှုကို ထိန်းသိမ်းသည် |
| Content Provenance | compute and enforcement overhead | လက်မှတ်ထိုးခြင်း နှင့် စစ်ဆေးခြင်း compute ကုန်သည် | signing နှင့် verification ms per artifact | သက်သေ မရှိလျှင် platform က ငြင်းပယ်သည် |
| Data Classification | memory and isolation boundary | class အလိုက် သိုလှောင်မှု နှင့် access scope ကွဲသည် | protected bytes per class | class မခွဲလျှင် ထိန်းချုပ်မှု အားလုံး တူညီစွာ ခံရသည် |
| Data Exfiltration | production consequence | allowlist နှင့် outbound စစ်ဆေးမှု ကုန်သည် | unauthorized egress events/day | ကာကွယ်ထားသည့် ဒေတာ ပြင်ပသို့ ထွက်သည် |
| Data Lineage | memory and isolation boundary | metadata သိုလှောင်မှု တိုးသည် | lineage edges per artifact | source ပြင်ဆင်လျှင် derivative ကို ရှာနိုင်သည် |
| Data Minimization | memory and isolation boundary | field လျှော့လျှင် byte လျော့သည် | retained bytes per purpose | မလိုအပ်သည့် field သည် ထိတွေ့နိုင်မှု ဖြစ်လာသည် |
| Datasheet for Datasets | cost of controls and of incidents | စာရွက်စာတမ်း ထုတ်လုပ်မှု ကုန်သည် | documented fields ÷ dataset version | မှားယွင်းသည့် အသုံးပြုမှုကို လျှော့သည် |
| Defense in Depth | compute and enforcement overhead | အလွှာ တိုးလျှင် compute နှင့် latency တိုးသည် | layers × per-layer overhead | အလွှာ တစ်ခု ကျရှုံးလျှင် အခြား အလွှာ ကာကွယ်သည် |
| Indirect Prompt Injection | latency of a policy or redaction check | retrieved content စစ်ဆေးမှု latency ထည့်သည် | added p50 နှင့် p95 ms | ခွင့်မပြုသည့် tool call ကို ဖြစ်စေသည် |
| Jailbreak | compute and enforcement overhead | adversarial eval compute ကုန်သည် | attack cases per release | eval မရှိလျှင် မူဝါဒ ကွာဟမှု ထုတ်လုပ်မှုသို့ ရောက်သည် |
| Membership Inference | cost of controls and of incidents | privacy test ကုန်ကျစရိတ် ကုန်သည် | TPR at fixed FPR | training data ပါဝင်မှု ပေါက်ကြားသည် |
| Provenance Attestation | compute and enforcement overhead | build-time signing နှင့် verify compute ကုန်သည် | attestation bytes per artifact | လက်မှတ် မရှိလျှင် release ကို ပိတ်သည် |
| Purpose Limitation | memory and isolation boundary | purpose မကိုက်သည့် data ကို ခွဲထားသည် | purposes per dataset | မူဝါဒ ချိုးဖောက်မှုကို တားဆီးသည် |
| Red Teaming | cost of controls and of incidents | authorized testing အချိန် ကုန်သည် | confirmed failures per cycle | မသိရှိသေးသည့် အားနည်းချက်ကို ဖော်ထုတ်သည် |
| Separation of Duties | throughput of audited traffic | အတည်ပြုချက် အဆင့် တိုးလျှင် approval throughput ကျသည် | approvals per hour | တစ်ဦးတည်း ပြီးဆုံးအောင် လုပ်နိုင်ခြင်းကို ဖျက်သည် |
| Software Bill of Materials (SBOM) | compute and enforcement overhead | SBOM generate နှင့် verify compute ကုန်သည် | components per release | အားနည်းချက် ပေါ်လျှင် ထိခိုက်သည့် component ကို ရှာနိုင်သည် |
| Threat Model | cost of controls and of incidents | ခွဲခြမ်းစိတ်ဖြာမှု အချိန် ကုန်သည် | credible attack paths per system | ထိန်းချုပ်မှု မည်သည့် အပေါ် ဦးစားပေးရမည်ကို ဆုံးဖြတ်သည် |
| Trust Boundary | memory and isolation boundary | နယ်နိမိတ် တိုင်းတွင် validation လိုသည် | boundary crossings per request | မှားယွင်းသည့် authority စီးဝင်မှုကို တားဆီးသည် |
| Zero Trust | latency of a policy or redaction check | request တိုင်း authorization စစ်ဆေးသည် | added ms per request | network ပေါ် အခြေခံသည့် ယုံကြည်မှုကို ဖျက်သည် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု လေးခုဖြင့် စုစည်းထားသည် — (က) အန္တရာယ် ခွဲခြမ်းစိတ်ဖြာမှု၊
(ခ) ဒေတာ အုပ်ချုပ်မှု၊ (ဂ) နယ်နိမိတ် နှင့် အခွင့်အာဏာ၊ (ဃ) သက်သေ နှင့် ဇာစ်မြစ်။
ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — အန္တရာယ် ခွဲခြမ်းစိတ်ဖြာမှု (risk and adversarial analysis)

#### AI Risk Assessment

AI Risk Assessment သည် AI စနစ် တစ်ခုသည် လူ၊ အဖွဲ့အစည်း နှင့် ပတ်ဝန်းကျင်အပေါ်
မည်သို့ သက်ရောက်နိုင်သည်ကို context၊ hazard၊ likelihood၊ impact၊ control၊
residual risk နှင့် monitoring တာဝန် တို့ဖြင့် မှတ်တမ်းတင်သည့် ခွဲခြမ်းစိတ်ဖြာမှု ဖြစ်သည်။
၎င်းသည် ကြိုတင်သတ်မှတ် ယူဆချက် အောက်တွင် ဆုံးဖြတ်ချက် တစ်ခုကို ထောက်ပံ့သည်၊
တစ်ကြိမ်တည်း ပေးသည့် လုံခြုံရေး လက်မှတ် မဟုတ်ပါ။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့်
၎င်းသည် မျှော်မှန်း ဆုံးရှုံးမှု (likelihood × impact) ကို ကိန်းဂဏန်း ဖြစ်စေပြီး
ထိန်းချုပ်မှု ဘတ်ဂျက် ခွဲဝေမှုကို အခြေခံပေးသည်။ ဥပမာ (ဂ) တွင် likelihood 0.25၊
impact 400000 USD ဖြစ်လျှင် ထိန်းချုပ်မှု မရှိသည့် မျှော်မှန်း ဆုံးရှုံးမှုသည်
100000.00 USD/year ဖြစ်သည်။

#### Threat Model

Threat Model သည် ကာကွယ်ရမည့် asset၊ trust boundary၊ ရန်သူ၊ ရန်သူ၏ စွမ်းရည်
ယူဆချက်၊ attack path၊ impact နှင့် စီစဉ်ထားသည့် control တို့ကို မှတ်တမ်းတင်သည့်
အကောင့် ဖြစ်သည်။ ထိန်းချုပ်မှု တစ်ခုကို မည်သည့် အရာကို ကာကွယ်သည်၊ မည်သူ့ဆီမှ
ကာကွယ်သည် ဆိုသည်ကို မဖော်ပြဘဲ အကဲမဖြတ်နိုင်ပါ။ ၎င်းသည် ဖြစ်နိုင်သည့် အန္တရာယ်
များကို ဦးစားပေးသည်၊ စနစ် လုံခြုံသည်ဟု သက်သေပြသည့် စာရင်း မဟုတ်ပါ။
အခြေခံအဆောက်အအုံ ဆုံးဖြတ်ချက် အတွက် ၎င်းသည် credible attack path အရေအတွက်ကို
ပြင်ဆင်ရမည့် အလုပ်အဖြစ် ပြောင်းလဲပေးသည်။

#### Red Teaming

Red Teaming သည် ခွင့်ပြုချက် ရရှိသည့် စမ်းသပ်သူများက မှတ်တမ်းတင်ထားသည့်
ရည်မှန်းချက်၊ ယူဆချက်၊ case နှင့် သက်သေ တို့ဖြင့် အားနည်းချက်များကို ရှာဖွေသည့်
စနစ်တကျ ရန်လိုသည့် စမ်းသပ်မှု ဖြစ်သည်။ သာမန် အရည်အသွေး စမ်းသပ်မှုသည်
ခြယ်လှယ်မှု၊ အလွဲသုံးမှု နှင့် ထိန်းချုပ်မှု ကျော်လွှားရန် ကြိုးစားမှု အောက်တွင်
စနစ် မည်သို့ ပြုမူသည်ကို တွေ့ရှိလေ့ မရှိပါ။ တွေ့ရှိသည့် အားနည်းချက် တိုင်းကို
versioned regression eval အဖြစ် ပြောင်းလဲရမည်၊ အကြောင်းမှာ ၎င်းတို့သည်
နောက်ထပ် release တွင် ပြန်မပေါ်စေရန် စစ်ဆေးရမည် ဖြစ်သည်။

#### Jailbreak

Jailbreak သည် model သို့မဟုတ် application ၏ control များ တားဆီးရန် ရည်ရွယ်ထားသည့်
အပြုအမူကို ထုတ်လုပ်စေရန် ကြိုးစားသည့် ရန်လိုသည့် input သို့မဟုတ် ဆက်သွယ်မှု
နည်းဗျူဟာ ဖြစ်သည်။ အောင်မြင်သည့် jailbreak သည် ကြေညာထားသည့် မူဝါဒ နှင့်
အမှန်တကယ် အပြုအမူ အကြား ကွာဟမှုကို ဖော်ထုတ်သည်။ model သည် tool သို့မဟုတ်
ကာကွယ်ထားသည့် ဒေတာကို ထိန်းချုပ်နိုင်သည့်အခါ ဤကွာဟမှု၏ အကျိုးဆက် ကြီးမားလာသည်။
ထုတ်လုပ်မှု တွင် ၎င်းသည် eval set အသစ် တစ်ခု ထည့်ရမည့် အချက် ဖြစ်ပြီး
eval compute ကုန်ကျစရိတ်ကို ဖြစ်စေသည်။

#### Indirect Prompt Injection

Indirect Prompt Injection သည် user ၏ တိုက်ရိုက် အမိန့် မှ မဟုတ်ဘဲ စနစ်က ရှာဖွေ
သို့မဟုတ် တွေ့ရှိသည့် content (webpage၊ document၊ email၊ ရုပ်ပုံ စာသား၊ tool result)
မှတစ်ဆင့် ပို့ဆောင်သည့် prompt injection attack ဖြစ်သည်။ agent သည် ခွင့်ပြုချက်
ရှိသည့် အလုပ်ကို လုပ်ဆောင်နေစဉ် ရန်သူ ထိန်းချုပ်သည့် အမိန့်များကို ကြုံတွေ့နိုင်ပြီး
ထို content ကို အခွင့်အာဏာ ရှိသည့် လမ်းညွှန်ချက် အဖြစ် မှားယွင်းစွာ ယူဆနိုင်သည်။
အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ကာကွယ်မှုသည် retrieved content ကို untrusted data
အဖြစ် တံဆိပ်တပ်ခြင်း နှင့် tool permission ကို ကျဉ်းခြင်း ဖြစ်သည်၊ ၎င်းသည် request
လမ်းကြောင်းတွင် latency အသစ် တစ်ခု ထည့်သည်။

#### Membership Inference

Membership Inference သည် အခြေခံ record တစ်ခု သည် model ၏ training data တွင်
ပါဝင်ခဲ့သည် မပါဝင်ခဲ့သည် ကို model output သို့မဟုတ် အခြား လက်လှမ်းမီသည့် အချက်များမှ
ခန့်မှန်းသည့် attack ဖြစ်သည်။ model က record ကို စာလုံးအလိုက် ပြန်ထုတ် မထုတ်
ပါဘဲ ခွဲခြားနိုင်သည့် အပြုအမူ ရှိလျှင် training data ပါဝင်မှု အချက်အလက် ပေါက်ကြားသည်။
လက်တွေ့ အကဲဖြတ်မှုသည် member နှင့် non-member ကို အမှန်တကယ် query မျက်နှာပြင်
အောက်တွင် စမ်းသပ်ပြီး ယုံကြည်မှု အချက်ပြမှု (confidence signal) ကို လျှော့ချသည်။
၎င်းသည် ကိုယ်ရေးလုံခြုံမှု ကာကွယ်မှု တစ်ခု၏ ကုန်ကျစရိတ်ကို တွက်ချက်ရန်
အခြေခံပေးသည်။

### မိသားစု (ခ) — ဒေတာ အုပ်ချုပ်မှု (data governance)

#### Data Classification

Data Classification သည် ဒေတာကို မှတ်တမ်းတင်ထားသည့် sensitivity သို့မဟုတ် impact
class များအဖြစ် သတ်မှတ်သည်၊ ထို့ကြောင့် handling၊ access၊ retention၊ sharing နှင့်
incident စည်းမျဉ်းများသည် ပေါက်ကြားမှု သို့မဟုတ် ဆုံးရှုံးမှု၏ အကျိုးဆက် အတိုင်း
လိုက်နာသည်။ AI pipeline တစ်ခုသည် source document၊ prompt၊ trace နှင့် generated
artifact များကို တူညီသည့် အရေးပါမှုအဖြစ် သတ်မှတ်ထားလျှင် သင့်လျော်သည့်
ထိန်းချုပ်မှုကို ကျင့်သုံးနိုင်မည် မဟုတ်ပါ။ အခြေခံအဆောက်အအုံ တွင် class တိုင်းသည်
သိုလှောင်မှု နေရာ၊ access scope နှင့် retention ကာလ ကို ဆုံးဖြတ်သည့်အတွက်
သိုလှောင်ထားသည့် byte ပမာဏကို တိုက်ရိုက် ရွေ့လျားစေသည်။

#### Data Minimization

Data Minimization သည် ကိုယ်ရေး ဒေတာအတွက် သတ်မှတ်ထားသည့် ရည်ရွယ်ချက်အတွက်
လိုအပ်သည့် အတိုင်းအတာအထိသာ စုဆောင်းခြင်း၊ လုပ်ဆောင်ခြင်း၊ ဖော်ထုတ်ခြင်း နှင့်
သိုလှောင်ခြင်းကို ကန့်သတ်သည်။ သိမ်းဆည်းထားသည့် byte တိုင်း၊ prompt၊ trace၊
cache သို့မဟုတ် tool call တွင် ထည့်ထားသည့် field တိုင်းသည် ကိုယ်ရေးလုံခြုံမှု
ထိတွေ့နိုင်မှု နှင့် အလွဲသုံးစားမှု သို့မဟုတ် ချိုးဖောက်ခံရမှု၏ ဖြစ်နိုင်သည့်
အကျိုးသက်ရောက်မှုကို တိုးစေသည်။ လျှော့ချခြင်းသည် ဒေတာ လုံးဝ မသိမ်းဆည်းခြင်း
မဟုတ်ပါ၊ ဒေတာ အစိတ်အပိုင်း တိုင်းကို ရည်ရွယ်ချက် နှင့် တိုက်ဆိုင်စစ်ဆေးနိုင်ခြင်း
ဖြစ်သည်။ ထို့ကြောင့် ၎င်းသည် memory and isolation boundary ဝင်ရိုးကို တိုက်ရိုက်
လျှော့ချသည်။

#### Purpose Limitation

Purpose Limitation သည် ကိုယ်ရေး ဒေတာကို သတ်မှတ်ထားသည့် တိကျသည့်
ရည်ရွယ်ချက်များအတွက်သာ စုဆောင်းခြင်း နှင့် အသုံးပြုခြင်းကို ကန့်သတ်သည်၊
ရည်ရွယ်ချက် အသစ် တစ်ခုအတွက် သင့်လျော်သည့် သို့မဟုတ် ခွင့်ပြုထားသည့်
အခြေခံ မရှိလျှင် ထို အသုံးပြုမှုကို ခွင့်မပြုပါ။ workflow တစ်ခုအတွက်
လက်ခံနိုင်သည့် ဒေတာသည် model training၊ evaluation၊ personalization သို့မဟုတ်
ဆက်စပ်မှု မရှိသည့် analytics အတွက် တိတ်ဆိတ်စွာ ပြန်လည် အသုံးပြုသည့်အခါ
ကိုယ်ရေးလုံခြုံမှု နှင့် အုပ်ချုပ်မှု အန္တရာယ် ဖြစ်ပေါ်စေသည်။ အခြေခံအဆောက်အအုံ တွင်
purpose တိုင်းကို dataset နှင့် တွဲဖက် မှတ်တမ်းတင်ပြီး pipeline အသစ် တစ်ခု
မဝင်မီ စစ်ဆေးရမည်။

#### Data Lineage

Data Lineage သည် ဒေတာ artifact တစ်ခုသည် source၊ transformation၊ join၊ filter၊
version နှင့် downstream အသုံးပြုမှု တစ်လျှောက် မည်သို့ ဆင်းသက်လာသည်ကို
မှတ်တမ်းတင်သည်။ source တစ်ခုကို ပြင်ဆင်သည့်အခါ၊ ပြန်လည် ရုပ်သိမ်းသည့်အခါ
သို့မဟုတ် မလုံခြုံသည်ဟု တွေ့ရှိသည့်အခါ lineage သည် မည်သည့် dataset၊ embedding၊
evaluation နှင့် model artifact များ ထိခိုက်နိုင်သည်ကို ဖော်ထုတ်ပေးသည်။ လက်တွေ့
ကျင့်သုံးမှုတွင် input နှင့် output တိုင်းကို တည်ငြိမ်သည့် identifier ပေး၍
transformation တိုင်းကို မှတ်တမ်းတင်ရမည်။ ဤ metadata သည် memory and isolation
boundary ဝင်ရိုးကို တိုးစေသည်၊ သို့သော် မရှိလျှင် ပြင်ဆင်မှု တစ်ခု၏ အကျိုးသက်ရောက်မှုကို
ခန့်မှန်း၍ မရနိုင်ပါ။

#### Datasheet for Datasets

Datasheet for Datasets သည် dataset တစ်ခု၏ motivation၊ composition၊ စုဆောင်းမှု
လုပ်ငန်းစဉ်၊ preprocessing၊ အသုံးပြုမှုများ၊ distribution၊ maintenance နှင့် သိရှိထားသည့်
ကန့်သတ်ချက်များကို ဖွဲ့စည်းတည်ဆောက်ထားသည့် စာရွက်စာတမ်း ဖြစ်သည်။ dataset တစ်ခု
ရရှိနိုင်ခြင်းသည် ၎င်း လုံခြုံသည် သို့မဟုတ် သင့်လျော်သည်ဟု မဆိုလိုပါ၊
နောက်ဆက်တွဲ တည်ဆောက်သူများသည် ၎င်း မည်သို့ ဖန်တီးခဲ့သည်နှင့် ၎င်း၏
ယူဆချက်များ မည်သည့်နေရာတွင် ကျိုးပျက်သည်ကို သက်သေ လိုအပ်သည်။
၎င်းသည် license၊ အရည်အသွေး အာမခံချက် သို့မဟုတ် deployment သီးသန့်
အကဲဖြတ်မှု အစားထိုး မဟုတ်ပါ။ ထုတ်လုပ်မှု တွင် ၎င်းသည် ဒေတာ အသုံးပြုမှု
ဆုံးဖြတ်ချက် တိုင်း၏ ကုန်ကျစရိတ်ကို လျှော့ချပေးသည်။

### မိသားစု (ဂ) — နယ်နိမိတ် နှင့် အခွင့်အာဏာ (boundary and authority)

#### Trust Boundary

Trust Boundary သည် ဒေတာ၊ အမိန့်၊ identity သို့မဟုတ် အခွင့်အာဏာသည် မတူညီသည့်
ယုံကြည်မှု ယူဆချက် အောက်တွင် လည်ပတ်သည့် component သို့မဟုတ် principal များ
အကြား ဖြတ်ကူးသည့် မျက်နှာပြင် ဖြစ်သည်။ နယ်နိမိတ် ဖြတ်ကူးမှု တစ်ခုသည်
စနစ်က actor ကို authenticate လုပ်ရမည့်၊ ဒေတာကို validate လုပ်ရမည့်၊
permission ကို ကန့်သတ်ရမည့် နှင့် မည်သည့် အခိုင်အမာ ချက်သည် အပြုအမူကို
သက်ရောက်နိုင်သည်ကို ဆုံးဖြတ်ရမည့် နေရာ ဖြစ်သည်။ network နယ်နိမိတ်သည်
တစ်မျိုးတည်း မဟုတ်ပါ၊ ခွင့်ပြုချက် ရှိသည့် agent context ထဲသို့ ဝင်လာသည့်
မယုံကြည်ရသည့် document စာသား လည်း နယ်နိမိတ် တစ်ခုကို ဖြတ်ကူးသည်။
ထို့ကြောင့် ၎င်းသည် memory and isolation boundary ဝင်ရိုး၏ အခြေခံ အချက်
ဖြစ်သည်။

#### Zero Trust

Zero Trust သည် network တည်နေရာ သို့မဟုတ် asset ပိုင်ဆိုင်မှုမှ တစ်ဆင့်
သွယ်ဝိုက် ယုံကြည်မှု မပေးဘဲ access request တိုင်းကို identity၊ device၊ resource၊
policy နှင့် လက်ရှိ context အပေါ် အခြေခံ၍ အကဲဖြတ်သည့် လုံခြုံရေး model
ဖြစ်သည်။ AI tool နှင့် agent များသည် local file၊ cloud service၊ model နှင့်
ပြင်ပ content တို့ကို ဖြတ်ကူးသည့်အတွက် ယုံကြည်ရသည့် အတွင်းပိုင်း network သည်
အခွင့်အာဏာ အတွက် အလွန်ကျယ်ပြန့်သည့် အခြေခံ ဖြစ်လာသည်။ ၎င်းသည်
မည်သည့် အရာကိုမျှ မယုံကြည်ခြင်း သို့မဟုတ် automation အားလုံးကို ပိတ်ဆို့ခြင်း
မဟုတ်ပါ၊ ယုံကြည်မှု ဆုံးဖြတ်ချက်တိုင်းကို တိကျစွာ သတ်မှတ်ခြင်း၊ scope ကန့်သတ်ခြင်း
နှင့် အဆက်မပြတ် စစ်ဆေးနိုင်ခြင်း ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့်
request တိုင်း authorization စစ်ဆေးခြင်းသည် latency ထည့်သည်။

#### Separation of Duties

Separation of Duties သည် ကွဲလွဲသည့် တာဝန် သို့မဟုတ် အခွင့်အာဏာကို
အမှီအခိုကင်းသည့် role များအကြား ခွဲဝေသည်၊ ထို့ကြောင့် principal တစ်ခုတည်းသည်
အခြား အခွင့်အာဏာ ရှိသည့် ဆုံးဖြတ်ချက် တစ်ခု မပါဘဲ အန္တရာယ် ကြီးသည့်
လုပ်ဆောင်မှု တစ်ခုကို ပြီးမြောက်အောင် လုပ်နိုင်မည် မဟုတ်ပါ။ ချိုးဖောက်ခံရသည့်
account သို့မဟုတ် မှားယွင်းသည့် agent သည် အန္တရာယ် ကြီးသည့် ပြောင်းလဲမှု တစ်ခုကို
အဆိုပြုခြင်း၊ အတည်ပြုခြင်း၊ ဆောင်ရွက်ခြင်း နှင့် ဖုံးကွယ်ခြင်း အားလုံးကို
လုပ်နိုင်ရမည် မဟုတ်ပါ။ ထို့ကြောင့် ၎င်းသည် audited traffic ၏ throughput ကို
ရွေ့လျားစေသည် — အတည်ပြုချက် အဆင့် တစ်ခု တိုးလျှင် တစ်နာရီ အတည်ပြုနိုင်သည့်
အရေအတွက် ကျဆင်းသည်။

#### Data Exfiltration

Data Exfiltration သည် ကာကွယ်ထားသည့် ဒေတာကို စနစ် သို့မဟုတ် trust zone မှ
လက်ခံခွင့် မရှိသည့် လူ၊ tool၊ service သို့မဟုတ် သိုလှောင်မှု နေရာသို့ ခွင့်မပြုဘဲ
ပို့ဆောင်ခြင်း ဖြစ်သည်။ agent တစ်ခုသည် မူရင်း ဒေတာ သိုလှောင်မှု မထိခိုက်ဘဲပင်
generated text၊ tool argument၊ URL၊ log သို့မဟုတ် side effect မှတစ်ဆင့်
လျှို့ဝှက်ချက်များကို ဖော်ထုတ်နိုင်သည်။ exfiltration သည် ခွင့်မပြုသည့်
ရွေ့လျားမှု သို့မဟုတ် ဖော်ထုတ်မှု အကြောင်း ဖြစ်သည်၊ ခွင့်ပြုချက် ရှိသည့်
component တစ်ခုက ဒေတာကို ပုံမှန် ရယူခြင်း သည် exfiltration မဟုတ်ပါ။
၎င်းသည် production consequence အဖြစ် အများဆုံး ပေါ်လာသည်၊ အကြောင်းမှာ
မည်သည့် ကိန်းဂဏန်း မျဉ်းကိုမျှ မချိုးဖောက်ဘဲ ဖော်ထုတ်မှု ဖြစ်ပေါ်နိုင်သည်။

#### Defense in Depth

Defense in Depth သည် လုံခြုံရေး နယ်နိမိတ် အများအပြားတွင် အမှီအခိုကင်းသည့်
preventive၊ detective နှင့် corrective control များကို သုံးသည်၊ ထို့ကြောင့်
control တစ်ခု ကျရှုံးခြင်းသည် ရလဒ်ကို ဆုံးဖြတ်နိုင်မည် မဟုတ်ပါ။ AI စနစ်များသည်
probabilistic model၊ မယုံကြည်ရသည့် content၊ tool နှင့် ပြင်ပ service များကို
ပေါင်းစပ်ထားသည့်အတွက် filter တစ်ခုတည်း သို့မဟုတ် prompt တစ်ခုတည်းသည်
လုံလောက်သည့် လုံခြုံရေး နယ်နိမိတ် မဟုတ်ပါ။ control အရေအတွက် များခြင်းသည်
အလိုအလျောက် ကောင်းသည့် အချက် မဟုတ်ပါ၊ အလွှာ တိုင်းသည် မတူညီသည့်
failure mode ကို ဖြေရှင်းရမည်။ အခြေခံအဆောက်အအုံ တွင် အလွှာ တိုးလျှင်
enforcement overhead နှင့် latency နှစ်ခုလုံး တိုးသည်။

### မိသားစု (ဃ) — သက်သေ နှင့် ဇာစ်မြစ် (evidence and provenance)

#### Audit Log

Audit Log သည် လုံခြုံရေး သို့မဟုတ် တာဝန်ခံမှုနှင့် ဆိုင်သည့် event များကို
တည်တံ့ပြီး access control ရှိသည့် မှတ်တမ်းအဖြစ် သိမ်းဆည်းသည် — မည်သူ သို့မဟုတ်
မည်သည့် အရာက လုပ်ဆောင်ခဲ့သည်၊ မည်သည့် အရာ ပြောင်းလဲခဲ့သည်၊ မည်သည့် အချိန်တွင်
ဖြစ်ခဲ့သည် နှင့် ရလဒ် status ပါဝင်သည်။ အကျိုးသက်ရောက်မှု ကြီးသည့် agent
လုပ်ဆောင်မှုများသည် performance debugging အပြင် စုံစမ်းစစ်ဆေးမှု၊ မူဝါဒ
ပြန်လည် သုံးသပ်မှု နှင့် တာဝန်ခံမှု ကို ထောက်ပံ့သည့် သက်သေ လိုအပ်သည်။
trace သည် execute လမ်းကြောင်း တစ်ခုတည်းကို ရှာဖွေရန် ကူညီသည်၊ audit log သည်
execution များနှင့် ကာလ အလိုက် တာဝန်ခံမှုအတွက် လိုအပ်သည့် event များကို
ထိန်းသိမ်းသည်။ ထို့ကြောင့် ၎င်း၏ record ပမာဏသည် request rate နှင့်
တိုက်ရိုက် အချိုးကျသည်။

#### Provenance Attestation

Provenance Attestation သည် artifact တစ်ခုကို ၎င်း မည်သို့၊ မည်သည့်နေရာ၊
မည်သည့် အချိန်၊ မည်သည့် input များမှ ထုတ်လုပ်ခဲ့သည်ဆိုသည့် အခိုင်အမာ ချက်
များနှင့် ချိတ်ဆက်သည့် authenticated နှင့် machine-readable metadata ဖြစ်သည်။
၎င်းသည် automated policy နှင့် reviewer များကို unsigned build note ကို
ယုံကြည်ရမည့်အစား supply-chain အခိုင်အမာ ချက်များကို စစ်ဆေးနိုင်စေသည်။
လက်မှတ် (signature) သည် attester ကို ခွဲခြားပြီး integrity ကို ကာကွယ်သည်၊
သို့သော် attestation အတွင်းရှိ အခိုင်အမာ ချက် တိုင်း မှန်သည်ဟု သက်သေပြသည်
မဟုတ်ပါ။ အခြေခံအဆောက်အအုံ တွင် ၎င်းသည် build system မှ generate လုပ်သည့်
compute ကုန်ကျစရိတ် နှင့် release မတိုင်မီ verify လုပ်သည့် compute
ကုန်ကျစရိတ် နှစ်ခုကို ဖြစ်စေသည်။

#### Content Provenance

Content Provenance သည် media သို့မဟုတ် အခြား digital content တစ်ခု၏
မူရင်း နှင့် တည်းဖြတ် ရာဇဝင် အကြောင်း စစ်ဆေးနိုင်သည့် အချက်အလက် ဖြစ်သည် —
ပါဝင်သည့် actor၊ tool၊ transformation နှင့် ချိတ်ဆက်ထားသည့် အခိုင်အမာ ချက်
များ ပါဝင်သည်။ generative စနစ်များသည် ပုံပန်းသဏ္ဌာန် အားဖြင့်သာ
မူရင်း အခိုင်အမာ ချက်များကို ခန့်မှန်းရန် ခက်ခဲစေသည့်အတွက် သုံးစွဲသူများနှင့်
platform များသည် content မည်သို့ ထုတ်လုပ်ခဲ့သည်ကို စစ်ဆေးနိုင်သည့် သက်သေ
လိုအပ်သည်။ provenance သည် မည်သူက ရာဇဝင် တစ်ခုကို အခိုင်အမာ ဆိုခဲ့သည်နှင့်
မှတ်တမ်း ပြောင်းလဲခံရသည် မခံရသည် ကို သက်သေပြနိုင်သည်၊ ဖော်ပြထားသည့်
ဖြစ်ရပ် မှန်သည်ဟု သို့မဟုတ် content သည် အန္တရာယ် ကင်းသည်ဟု သက်သေပြသည်
မဟုတ်ပါ။ လက်တွေ့ တွင် ၎င်းသည် artifact တိုင်းအတွက် signing နှင့် verification
 overhead ကို ဖြစ်စေသည်။

#### Software Bill of Materials (SBOM)

Software Bill of Materials (SBOM) သည် product သို့မဟုတ် artifact တစ်ခုနှင့်
ဆက်စပ်သည့် software component နှင့် ဆက်စပ်မှုများ၏ ဖွဲ့စည်းတည်ဆောက်ထားသည့်
စာရင်း ဖြစ်သည်၊ version၊ supplier၊ license နှင့် identifier များ ပါဝင်လေ့ရှိသည်။
software ပြောင်းလဲသည့်အခါ သို့မဟုတ် အားနည်းချက် ပေါ်ပေါက်သည့်အခါ ထိခိုက်သည့်
dependency၊ license တာဝန် နှင့် supply-chain ထိတွေ့နိုင်မှုကို အကဲဖြတ်ရန်
component စာရင်း လိုအပ်သည်။ SBOM သည် စာရင်း ဖြစ်သည်၊ component များ
လုံခြုံသည်၊ license မှန်ကန်သည် သို့မဟုတ် အမှန်တကယ် ပါဝင်သည်ဟု
သက်သေပြသည် မဟုတ်ပါ၊ generation နှင့် provenance ကို ယုံကြည်ရမည်
ဖြစ်သည်။ အခြေခံအဆောက်အအုံ တွင် ၎င်းသည် trusted build အတွင်း generate လုပ်ခြင်း
နှင့် policy check တွင် verify လုပ်ခြင်း compute ကို တိုးစေသည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍
ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး
deterministic ဖြစ်သည်။

### (က) Guardrail သို့မဟုတ် redaction အဆင့် တစ်ခု၏ latency နှင့် throughput ကုန်ကျစရိတ်

ဖော်မြူလာ — `total_check_ms = base_check_ms + pattern_count × ms_per_pattern`၊
`ceiling_req_s = workers ÷ ((base_service_ms + total_check_ms) ÷ 1000)`။
ယူဆချက် — requests_per_s 120၊ workers 32၊ base_service_ms 90၊ pattern_count 12၊
ms_per_pattern 0.15၊ p95_factor 1.8၊ false_positive_rate 0.004၊
usd_per_false_redaction 0.35။ false positive နှင့် စျေးနှုန်း အားလုံးသည်
assumption ဖြစ်သည်၊ `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

```text
$ python3 guides/11_security_and_governance/scripts/ex_a_guardrail_cost.py
======================================================================================================
ex_a_guardrail_cost - guardrail / redaction အဆင့် တစ်ခု၏ latency နှင့် throughput ကုန်ကျစရိတ်
(assumption) requests_per_s=120  workers=32  base_service_ms=90.0  pattern_count=12
(assumption) ms_per_pattern=0.15  p95_factor=1.8  false_positive_rate=0.004  usd_per_false_redaction=0.35
------------------------------------------------------------------------------------------------------
Guardrail tier              check_ms  added_p50  added_p95  ceiling_req_s  vs_base  false/day  usd/day
regex redaction only            1.80       1.80       3.24          348.6    0.980   41,472.0 14515.20
regex + small classifier       13.80      13.80      24.84          308.3    0.867   41,472.0 14515.20
regex + classifier + judge    146.80     146.80     264.24          135.1    0.380   41,472.0 14515.20
------------------------------------------------------------------------------------------------------
baseline ceiling with no guardrail at all = 355.6 req/s (workers=32, base_service_ms=90.0)
false redactions per day = 120 req/s * 86400 s * 0.004 = 41,472.0 requests, cost 14,515.20 USD/day
မှတ်ချက် - guardrail အဆင့် တစ်ခုစီသည် request တိုင်း၏ လမ်းကြောင်းတွင် latency ထည့်သည်၊ ceiling သည် worker အရေအတွက်ကို request တစ်ခုလျှင် ကုန်သည့် အချိန်ဖြင့် စားသည့် တန်ဖိုး ဖြစ်သည်။ false redaction ၏ ကုန်ကျစရိတ်သည် လုပ်ငန်း အခြေအနေအလိုက် ကွာခြားသည်။
======================================================================================================
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ regex redaction တစ်လုံးတည်းသည် ceiling ကို
355.6 req/s မှ 348.6 req/s သို့သာ လျှော့သည်၊ သို့သော် LLM judge ပါဝင်သည့်
အလွှာ တစ်ခု ထည့်လျှင် ceiling သည် 135.1 req/s သို့ ကျဆင်းသည်။ ထို့ကြောင့်
guardrail အလွှာ တိုင်း၏ latency ကို မတိုင်းဘဲ အလွှာ ထည့်ခြင်းသည် capacity
ဆုံးဖြတ်ချက်ကို မှားယွင်းစေသည်။

### (ခ) audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်

ဖော်မြူလာ — `records_per_day = requests_per_day × records_per_request`၊
`storage_bytes = bytes_per_day × retention_days × sampling_rate`။
ယူဆချက် — requests_per_day 2000000၊ records_per_request 3၊ bytes_per_record 1200၊
storage_usd_per_gb_month 0.023၊ sampling_rate 0.10၊ 1 GB သည် 10^9 byte။
retention အခြေခံသည် steady state ဖြစ်သည်၊ စျေးနှုန်းသည် provider နှင့်
tier အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

```text
$ python3 guides/11_security_and_governance/scripts/ex_b_audit_volume.py
======================================================================================================
ex_b_audit_volume - audit log ပမာဏ၊ သိုလှောင်မှု နှင့် ကုန်ကျစရိတ်
(assumption) requests_per_day=2,000,000  records_per_request=3  bytes_per_record=1200
(assumption) storage_usd_per_gb_month=0.023  sampling_rate=0.1  (1 GB = 10^9 bytes)
------------------------------------------------------------------------------------------------------
records per day              :      6,000,000
volume per day               :           7.20 GB/day   (7,200,000,000 bytes)
full-fidelity retention 365 days : 2,628.00 GB      60.44 USD/month
------------------------------------------------------------------------------------------------------
retention_days     records_held   storage_GB  monthly_usd  sampled_GB  sampled_usd
            30      180,000,000       216.00         4.97       21.60         0.50
            90      540,000,000       648.00        14.90       64.80         1.49
           180    1,080,000,000     1,296.00        29.81      129.60         2.98
           365    2,190,000,000     2,628.00        60.44      262.80         6.04
           730    4,380,000,000     5,256.00       120.89      525.60        12.09
------------------------------------------------------------------------------------------------------
sampling 10% of records keeps 10% of the volume and 10% of the monthly cost; the discarded records cannot answer an investigation that needs them.
မှတ်ချက် - retention_days တိုးလျှင် သိုလှောင်မှု တိုးသည်၊ sampling သည် ကုန်ကျစရိတ်ကို လျှော့သည်၊ သို့သော် မှတ်တမ်း ပြည့်စုံမှုကို လျှော့သည်။ storage စျေးနှုန်းသည် provider နှင့် tier အလိုက် ကွာခြားသည်။
======================================================================================================
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ request rate 2000000/day တွင် record 6000000/day
ဖြစ်ပေါ်ပြီး 365 ရက် သိမ်းဆည်းလျှင် 2628.00 GB နှင့် 60.44 USD/month ဖြစ်သည်။
sampling 10% သည် ကုန်ကျစရိတ်ကို 6.04 USD/month သို့ လျှော့သည်၊ သို့သော်
မှတ်တမ်း 90% သည် စုံစမ်းစစ်ဆေးမှုအတွက် ပြန်ရယူနိုင်ခြင်း မရှိတော့ပါ။

### (ဂ) ထိန်းချုပ်မှု တစ်ခု၏ မျှော်မှန်း ဆုံးရှုံးမှု လျော့ချမှုနှင့် break-even ကုန်ကျစရိတ်

ဖော်မြူလာ — `loss_without = likelihood × impact`၊
`loss_with(e) = likelihood × (1 - e) × impact`၊
`break_even_control_cost = loss_without - loss_with(e)`။
ယူဆချက် — incidents_per_year 0.25၊ impact_usd 400000၊ control_effectiveness 0.80၊
control_cost_usd_per_year 60000။ likelihood နှင့် impact သည် assumption ဖြစ်သည်။

```text
$ python3 guides/11_security_and_governance/scripts/ex_c_control_roi.py
======================================================================================================
ex_c_control_roi - ထိန်းချုပ်မှု တစ်ခု၏ မျှော်မှန်း ဆုံးရှုံးမှု လျော့ချမှုနှင့် break-even ကုန်ကျစရိတ်
(assumption) incidents_per_year=0.25  impact_usd=400,000  control_effectiveness=0.8  control_cost_usd_per_year=60,000
------------------------------------------------------------------------------------------------------
expected loss without control        :     100,000.00 USD/year
expected loss with control           :      20,000.00 USD/year
expected loss reduction              :      80,000.00 USD/year
break-even control cost              :      80,000.00 USD/year
net benefit at the stated cost       :      20,000.00 USD/year
benefit / cost ratio                 :           1.33
------------------------------------------------------------------------------------------------------
effectiveness   loss_with_usd   reduction_usd  net_benefit_usd  worth_it
         0.00      100,000.00            0.00       -60,000.00        no
         0.20       80,000.00       20,000.00       -40,000.00        no
         0.40       60,000.00       40,000.00       -20,000.00        no
         0.60       40,000.00       60,000.00             0.00        no
         0.80       20,000.00       80,000.00        20,000.00       yes
         0.90       10,000.00       90,000.00        30,000.00       yes
         0.95        5,000.00       95,000.00        35,000.00       yes
------------------------------------------------------------------------------------------------------
the control pays for itself while effectiveness stays above 0.60 at this likelihood and impact
မှတ်ချက် - likelihood နှင့် impact သည် ခန့်မှန်း ယူဆချက် ဖြစ်သည်၊ effectiveness ကို red team နှင့် monitoring ဖြင့် တိုင်းတာရမည်။ residual risk ကို မှတ်တမ်းတင်ထားရမည်။
======================================================================================================
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ ထိန်းချုပ်မှု မရှိလျှင် မျှော်မှန်း ဆုံးရှုံးမှုသည်
100000.00 USD/year ဖြစ်ပြီး effectiveness 0.80 ဖြင့် ၎င်းသည် 20000.00 USD/year သို့
ကျဆင်းသည်၊ ထို့ကြောင့် break-even ကုန်ကျစရိတ်သည် 80000.00 USD/year ဖြစ်သည်။
effectiveness 0.60 တွင် net benefit သည် သုည ဖြစ်သည့်အတွက် ထို အခြေအနေတွင်
ထိန်းချုပ်မှု သည် ကုန်ကျစရိတ် နှင့် တူညီသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ guardrail အလွှာ ရွေးချယ်ခြင်း** — မှီခိုသည့် term များ — Indirect Prompt Injection၊
Jailbreak၊ Defense in Depth၊ Trust Boundary။ သက်သေပြသည့် မက်ထရစ် — added p50
နှင့် p95 latency၊ throughput ceiling။ ဥပမာ (က) က LLM judge အလွှာ ထည့်လျှင်
ceiling သည် 355.6 မှ 135.1 req/s သို့ ကျဆင်းသည်ဟု ပြသည်၊ ထို့ကြောင့်
အလွှာ တိုင်းကို capacity budget နှင့် တွဲဖက် အကဲဖြတ်ရမည်။

**၂။ audit log retention နှင့် sampling သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ —
Audit Log၊ Data Classification၊ Separation of Duties၊ Provenance Attestation။
သက်သေပြသည့် မက်ထရစ် — records/day၊ storage GB၊ USD/month။ ဥပမာ (ခ) အရ
2000000 request/day တွင် 365 ရက် retention သည် 2628.00 GB နှင့် 60.44 USD/month
ဖြစ်သည်၊ မည်သည့် event ကို sampling လုပ်နိုင်သည်ကို class အလိုက်
ရေးမှတ်ထားရမည်။

**၃။ redaction pattern အရေအတွက် သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ —
Data Exfiltration၊ Data Minimization၊ Content Provenance။ သက်သေပြသည့် မက်ထရစ် —
false positive rate၊ false redactions/day နှင့် ၎င်းတို့၏ ကုန်ကျစရိတ်။
pattern တစ်ခု တိုးလျှင် latency သည် 0.15 ms တိုးသည်၊ ထို့ကြောင့် pattern
စာရင်းကို မှတ်တမ်းတင်ထားသည့် redaction နှုန်း နှင့် တွဲဖက် အကဲဖြတ်ရမည်။

**၄။ tool permission scope သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Trust Boundary၊
Zero Trust၊ Data Exfiltration၊ Indirect Prompt Injection။ သက်သေပြသည့် မက်ထရစ် —
reachable tool-scope pairs၊ scope reduction ရာခိုင်နှုန်း နှင့် risk reduction။
ဥပမာ lab တွင် tools 12 နှင့် data_scopes 9 သည် 108 tool-scope pair ဖြစ်ပြီး
least privilege သည် ၎င်းကို 48 သို့ ကျဉ်းစေသည်။

**၅။ ဒေတာ classification နှင့် purpose limitation ကို pipeline တွင် ထည့်ခြင်း** —
မှီခိုသည့် term များ — Data Classification၊ Purpose Limitation၊ Data Minimization၊
Data Lineage၊ Datasheet for Datasets။ သက်သေပြသည့် မက်ထရစ် — purpose တိုင်းအတွက်
သိုလှောင်ထားသည့် byte၊ lineage coverage ရာခိုင်နှုန်း။ label မရှိသည့် artifact
သည် ထိန်းချုပ်မှု မည်သည့် အဆင့်ကို ခံရမည်ကို မဆုံးဖြတ်နိုင်ပါ။

**၆။ ထိန်းချုပ်မှု တစ်ခု ထည့်ခြင်း သို့မဟုတ် မထည့်ခြင်း** — မှီခိုသည့် term များ —
AI Risk Assessment၊ Threat Model၊ Red Teaming၊ Membership Inference။
သက်သေပြသည့် မက်ထရစ် — မျှော်မှန်း ဆုံးရှုံးမှု လျော့ချမှု နှင့် break-even
ကုန်ကျစရိတ်။ ဥပမာ (ဂ) အရ effectiveness 0.60 အောက် ကျဆင်းလျှင် ထို
ထိန်းချုပ်မှုသည် ကုန်ကျစရိတ်ကို ပြန်မရနိုင်တော့ပါ။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/11_security_and_governance/labs/lab_redaction_path.py`၊
`guides/11_security_and_governance/labs/lab_audit_volume.py`၊ `guides/11_security_and_governance/labs/lab_blast_radius.py` တို့ဖြင့်
လက်တွေ့ စမ်းသပ်နိုင်သည်။ lab တိုင်းသည် `--sweep` နှင့် `--self-test` ကို
ထောက်ပံ့သည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ်
မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/11_security_and_governance.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/11_security_and_governance.json`။

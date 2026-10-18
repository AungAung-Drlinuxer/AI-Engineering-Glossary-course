# Security & Governance — လုံခြုံရေးနှင့် အုပ်ချုပ်မှု

ဤနယ်ပယ်တွင် **term ၂၀** ခု ပါဝင်သည် — AI အန္တရာယ် အကဲဖြတ်ခြင်း၊ audit မှတ်တမ်း၊ မူလဇာစ်မြစ် အတည်ပြုချက်၊ data ကာကွယ်ရေး
(data classification၊ data minimization၊ purpose limitation)၊ ရန်လိုသူကို ခုခံသည့် စမ်းသပ်ခြင်း (threat model၊ red teaming၊ jailbreak၊ indirect
prompt injection)၊ အာဏာ ကန့်သတ်ခြင်း (least privilege ဆိုင်ရာ control၊ separation of duties၊ zero trust) နှင့် supply-chain
အတည်ပြုမှု (provenance attestation၊ SBOM) တို့ ဖြစ်သည်။ AI စနစ်တစ်ခုသည် စွမ်းရည် မြင့်မားလာသည့်အခါ ၎င်းသည် ကာကွယ်ထားသည့်
data ကို ဖတ်နိုင်သည်၊ tool များကို ခေါ်နိုင်သည်၊ ပြင်ပသို့ ရေးသွင်းနိုင်သည်။ ထို့ကြောင့် လုံခြုံရေးနှင့် အုပ်ချုပ်မှုသည် အပိုဆောင်း
အလှဆင်မှု မဟုတ်တော့ဘဲ စနစ်၏ တည်ဆောက်ပုံ အစိတ်အပိုင်း ဖြစ်လာသည်။

ဤ term များသည် တစ်ခုနှင့်တစ်ခု ဆက်စပ်နေသည် — threat model သည် မည်သည့်အရာကို ကာကွယ်သည်၊ မည်သူကို ဆန့်ကျင်သည် ကို
သတ်မှတ်ပေးသည်။ trust boundary သည် မည်သည့် နေရာတွင် data၊ ညွှန်ကြားချက်နှင့် အာဏာ ဖြတ်ကူးသည် ကို ဖော်ပြသည်။
defense in depth၊ least privilege နှင့် zero trust သည် ထို နေရာများတွင် control များကို မည်သို့ စီစဉ်ရမည် ကို သတ်မှတ်သည်။
audit log၊ data lineage နှင့် provenance attestation သည် ဖြစ်ပွားခဲ့သည့် အရာအားလုံးအတွက် အထောက်အထား ထိန်းသိမ်းသည်။
term တစ်ခုတည်းကို ဖတ်ခြင်းထက် ဤ အစုအဖွဲ့ အဖြစ် ဖတ်ခြင်းက စနစ်တစ်ခုလုံး၏ ကာကွယ်မှု ပုံစံကို မြင်နိုင်စေသည်။

ဖတ်ရှုသည့် အစဉ်မှာ — English term → မြန်မာ အမည် → ဆိုလိုသည့် အဓိပ္ပာယ် → အရေးပါသည့် အကြောင်းရင်း → မကြာခဏ ရောထွေးမှု →
လက်တွေ့ → ဆက်စပ် term များ → English (source) ဖြစ်သည်။ `English (source)` field သည် source glossary ၏ မူရင်း စာသား
ဖြစ်သည့်အတွက် မြန်မာ ရှင်းလင်းချက်နှင့် တွဲဖတ်ပါက အသုံးအနှုန်း ကွာခြားမှုကို ရှင်းလင်းစွာ မြင်နိုင်သည်။ မြန်မာ စာကြောင်းအတွင်း
technical term များ (threat model၊ least privilege၊ trust boundary၊ audit log၊ data exfiltration၊ policy၊ redaction) ကို
အင်္ဂလိပ်အတိုင်း ထားရှိသည်။

### AI Risk Assessment

**မြန်မာ:** AI အန္တရာယ် အကဲဖြတ်ခြင်း

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** AI စနစ်တစ်ခုသည် လူများ၊ အဖွဲ့အစည်းများနှင့် ပတ်ဝန်းကျင်အပေါ် မည်သို့ သက်ရောက်နိုင်သည်ကို မှတ်တမ်းတင်ထားသည့် ခွဲခြမ်းစိတ်ဖြာမှု ဖြစ်သည်။ ထို ခွဲခြမ်းစိတ်ဖြာမှုတွင် context၊ hazard များ၊ ဖြစ်နိုင်ခြေ (likelihood)၊ သက်ရောက်မှု (impact)၊ control များ၊ residual risk နှင့် စောင့်ကြည့်ရန် တာဝန်ရှိသူများ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** model ၏ စွမ်းရည်တစ်ခုတည်းက အန္တရာယ်ကို မဆုံးဖြတ်နိုင်ပါ။ deploy လုပ်သည့် context၊ ထိခိုက်ခံရသည့် လူအုပ်စုများ၊ လူ၏ အာဏာ၊ data နှင့် စနစ် ချိတ်ဆက်မှုများသည် သက်ရောက်မှုနှင့် လိုအပ်သည့် control နှစ်မျိုးလုံးကို ပြောင်းလဲစေသည်။
- **မကြာခဏ ရောထွေးမှု:** risk assessment သည် သတ်မှတ်ထားသည့် ယူဆချက်များအောက်တွင် ဆုံးဖြတ်ချက်တစ်ခုကို ပံ့ပိုးပေးသည်။ ၎င်းသည် တစ်ကြိမ်တည်း ရရှိသည့် safety certificate သို့မဟုတ် hazard အားလုံးကို ရှာတွေ့ပြီးကြောင်း အထောက်အထား မဟုတ်ပါ။
- **လက်တွေ့:** ရည်ရွယ်ထားသည့် အသုံးပြုမှုနှင့် ထိခိုက်ခံရသည့် ပုဂ္ဂိုလ်များကို သတ်မှတ်ခြင်း၊ ဖြစ်နိုင်ခြေရှိသည့် ပျက်ကွက်မှုနှင့် အလွဲသုံးစားလုပ်မှု အခြေအနေများကို ဖော်ထုတ်ခြင်း၊ control တိုင်းအတွက် ပိုင်ရှင် သတ်မှတ်ခြင်း၊ residual risk ကို မှတ်တမ်းတင်ခြင်း၊ အရေးကြီး ပြောင်းလဲမှုများအတွက် review trigger သတ်မှတ်ခြင်း တို့ကို ပြုလုပ်ရမည်။
- **ဆက်စပ် term များ:** Threat Model, Guardrails, Human-in-the-Loop (HITL), Data Classification
- **English (source):** A documented analysis of how an AI system can affect people, organizations, and environments, including context, hazards, likelihood, impact, controls, residual risk, and monitoring responsibilities. Model capability alone does not determine risk. Deployment context, affected groups, human authority, data, and system integrations change both the harms and the controls required.

### Audit Log

**မြန်မာ:** စစ်ဆေးစာရင်း မှတ်တမ်း (audit log)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** security သို့မဟုတ် တာဝန်ခံမှုနှင့် သက်ဆိုင်သည့် ဖြစ်ရပ်များကို ကြာရှည်ခံ၍ access control ဖြင့် ကာကွယ်ထားသည့် မှတ်တမ်း ဖြစ်သည်။ မည်သူ သို့မဟုတ် မည်သည့် အရာက ဆောင်ရွက်ခဲ့သည်၊ မည်သည့် အရာ ပြောင်းလဲခဲ့သည်၊ မည်သည့် အချိန်တွင် ဖြစ်ပွားခဲ့သည်၊ ရရှိသည့် အခြေအနေ (status) မည်သို့ ဖြစ်သည် ဆိုသည်တို့ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အကျိုးဆက် ရှိသည့် agent လုပ်ဆောင်ချက်များအတွက် စုံစမ်းစစ်ဆေးခြင်း၊ policy ပြန်လည် သုံးသပ်ခြင်းနှင့် တာဝန်ခံမှုကို ပံ့ပိုးသည့် အထောက်အထား လိုအပ်သည်။ ထို အထောက်အထားသည် performance ကို debug လုပ်ခြင်းထက် ကျော်လွန်သည်။
- **မကြာခဏ ရောထွေးမှု:** trace သည် execution path တစ်ခုကို ရောဂါရှာဖွေရန် ကူညီသည်။ audit log သည် execution အများနှင့် အချိန်ကြာလာသည့်အခါ တာဝန်ခံမှုအတွက် လိုအပ်သည့် ဖြစ်ရပ်များကို ထိန်းသိမ်းသည်။
- **လက်တွေ့:** tool ခွင့်ပြုချက် (authorization)၊ approval ဆုံးဖြတ်ချက်များ၊ ပြင်ပသို့ ရေးသွင်းမှုများ၊ policy version များနှင့် artifact identifier များကို မှတ်တမ်းတင်ရမည်။ တစ်ချိန်တည်းတွင် secret များကို redact လုပ်ရမည် ဖြစ်ပြီး log access ကို ကန့်သတ်ရမည်။
- **ဆက်စပ် term များ:** Trace, Observability, Approval Gate, Provenance Attestation
- **English (source):** A durable, access-controlled record of security- or accountability-relevant events, including who or what acted, what changed, when it happened, and the resulting status. Consequential agent actions need evidence that supports investigation, policy review, and responsibility beyond performance debugging.

### Content Provenance

**မြန်မာ:** အကြောင်းအရာ၏ မူလဇာစ်မြစ် (content provenance)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** media တစ်ခု သို့မဟုတ် အခြား digital content တစ်ခု၏ မူလရင်းမြစ်နှင့် တည်းဖြတ်မှု သမိုင်းကြောင်းအပေါ် စစ်ဆေး အတည်ပြုနိုင်သည့် အချက်အလက် ဖြစ်သည်။ ၎င်းတွင် ပါဝင်ခဲ့သည့် လုပ်ဆောင်သူများ၊ tool များ၊ ပြောင်းလဲမှုများနှင့် ချိတ်တွဲထားသည့် ကြေညာချက် (assertion) များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** generative စနစ်များကြောင့် မူလရင်းမြစ် ကြေညာချက်များကို အသွင်အပြင် သက်သက်ဖြင့် ခန့်မှန်းရန် ခက်ခဲလာသည့်အတွက် သုံးစွဲသူများနှင့် platform များသည် content ကို မည်သို့ ထုတ်လုပ်ခဲ့သည်ကို စစ်ဆေးနိုင်သည့် အထောက်အထား လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** provenance သည် သမိုင်းကြောင်းကို မည်သူ ကြေညာခဲ့သည် နှင့် မှတ်တမ်းကို ပြောင်းလဲခဲ့မှု ရှိမရှိ ကို အတည်ပြုနိုင်သည်။ သို့သော် ဖော်ပြထားသည့် ဖြစ်ရပ် မှန်ကန်သည် သို့မဟုတ် content သည် အန္တရာယ် ကင်းသည် ဆိုသည်ကို သက်သေမပြနိုင်ပါ။
- **လက်တွေ့:** provenance ကြေညာချက်များကို content နှင့် ချိတ်ဆက်ရမည်၊ ထိန်းချုပ်ထားသည့် identity ဖြင့် လက်မှတ်ထိုးရမည်၊ ပြောင်းလဲမှု သမိုင်းကြောင်းကို ထိန်းသိမ်းရမည်၊ အထောက်အထား မရှိသည့် သို့မဟုတ် အတည်ပြုနိုင်မည် မဟုတ်သည့် အခါ ရှင်းလင်းစွာ ဖော်ပြရမည်။
- **ဆက်စပ် term များ:** Data Provenance, Provenance Attestation, Audit Log, Grounding
- **Learn it:** [Watermarking, SynthID, Stable Signature, and C2PA](../phases/18-ethics-safety-alignment/23-watermarking-synthid-stable-signature-c2pa/)
- **English (source):** Verifiable information about the origin and editing history of a piece of media or other digital content, including the actors, tools, transformations, and assertions attached to it. Generative systems make origin claims difficult to infer from appearance alone, so consumers and platforms need inspectable evidence about how content was produced.

### Data Classification

**မြန်မာ:** data အဆင့်တန်း သတ်မှတ်ခြင်း (data classification)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** data ကို မှတ်တမ်းတင်ထားသည့် sensitivity သို့မဟုတ် သက်ရောက်မှု အဆင့်တန်းများအဖြစ် သတ်မှတ်ခြင်း ဖြစ်သည်။ ထိုသို့ သတ်မှတ်ခြင်းဖြင့် ကိုင်တွယ်ခြင်း၊ access၊ ထိန်းသိမ်းခြင်း၊ မျှဝေခြင်းနှင့် incident ဆိုင်ရာ စည်းမျဉ်းများသည် ဖော်ထုတ်ခံရခြင်း သို့မဟုတ် ဆုံးရှုံးခြင်း၏ အကျိုးဆက်များအတိုင်း လိုက်နာစေသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** source document များ၊ prompt များ၊ trace များနှင့် generate လုပ်ထားသည့် artifact များကို တူညီသည့် sensitivity အနေဖြင့် သတ်မှတ်ထားပါက AI pipeline သည် အချိုးကျသည့် control များကို ကျင့်သုံးနိုင်မည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** data classification သည် ကာကွယ်ရေး လိုအပ်ချက်များကို ဖော်ပြသည်။ ၎င်းသည် machine-learning classification task နှင့် တူညီသည် မဟုတ်ပါ၊ data မှန်ကန်သည် ဆိုသည့် ကြေညာချက်လည်း မဟုတ်ပါ။
- **လက်တွေ့:** data ကို ingestion အချိန်တွင် classify လုပ်ရမည်၊ label ကို ဆင်းသက်လာသည့် artifact များအထိ သယ်ဆောင်ရမည်၊ tool များနှင့် destination များကို class အလိုက် ကန့်သတ်ရမည်၊ transformation သို့မဟုတ် aggregation ပြီးနောက် label များ မည်သို့ ပြောင်းလဲသည်ကို သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Data Minimization, Trust Boundary, Least Privilege, Audit Log
- **English (source):** Assigning data to documented sensitivity or impact classes so handling, access, retention, sharing, and incident rules follow the consequences of disclosure or loss. An AI pipeline cannot apply proportionate controls if source documents, prompts, traces, and generated artifacts are treated as equally sensitive.

### Data Exfiltration

**မြန်မာ:** data ခွင့်ပြုချက်မရှိဘဲ ယူဆောင်ခြင်း (data exfiltration)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကာကွယ်ထားသည့် data ကို စနစ်တစ်ခု သို့မဟုတ် trust zone တစ်ခုမှ လက်ခံခွင့် မရှိသည့် လူ၊ tool၊ service သို့မဟုတ် သိုလှောင်ရာ နေရာတစ်ခုသို့ ခွင့်ပြုချက် မရှိဘဲ လွှဲပြောင်းခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မူလ data store မပျက်စီးဘဲ ရှိနေသည့် အချိန်တွင်ပင် agent သည် generate လုပ်ထားသည့် စာသား၊ tool argument များ၊ URL များ၊ log များ သို့မဟုတ် ဘေးထွက် သက်ရောက်မှုများမှတစ်ဆင့် secret များကို ဖော်ထုတ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** exfiltration သည် ခွင့်ပြုချက် မရှိသည့် ရွေ့လျားမှု သို့မဟုတ် ဖော်ထုတ်မှုနှင့် သက်ဆိုင်သည်။ ခွင့်ပြုချက် ရှိသည့် component တစ်ခုမှ data ကို ပုံမှန် ရယူခြင်း (retrieval) သည် exfiltration မဟုတ်ပါ။ သို့သော် နောက်ပိုင်း အသုံးပြုမှုသည် exfiltration ဖြစ်လာနိုင်သည်။
- **လက်တွေ့:** ဖတ်နိုင်သည့် data ကို အနည်းဆုံးဖြစ်စေရမည်၊ destination များကို allowlist ဖြင့် သတ်မှတ်ရမည်၊ အပြင်သို့ ထွက်သည့် tool call များကို စစ်ဆေးရမည်၊ sensitive field များကို redact လုပ်ရမည်၊ trust boundary များကို ဖြတ်ကူးသည့် ပုံမှန်မဟုတ်သည့် transfer များအတွက် alert ထုတ်ရမည်။
- **ဆက်စပ် term များ:** Trust Boundary, Least Privilege, Indirect Prompt Injection, Audit Log
- **Learn it:** [EchoLeak and CVEs for AI](../phases/18-ethics-safety-alignment/25-echoleak-cves-for-ai/)
- **English (source):** Unauthorized transfer of protected data from a system or trust zone to a person, tool, service, or storage location that is not permitted to receive it. An agent can expose secrets through generated text, tool arguments, URLs, logs, or side effects even when the original data store remains intact.

### Data Lineage

**မြန်မာ:** data ဆင်းသက်မှု လမ်းကြောင်း (data lineage)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** data artifact တစ်ခုသည် source များ၊ transformation များ၊ join များ၊ filter များ၊ version များနှင့် နောက်ဆက်တွဲ အသုံးပြုမှုများကို ဖြတ်သန်း၍ မည်သို့ ဆင်းသက်လာသည်ကို မှတ်တမ်းတင်ထားခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** source တစ်ခုကို ပြင်ဆင်ခြင်း၊ ရုပ်သိမ်းခြင်း သို့မဟုတ် အန္တရာယ်ရှိသည်ဟု တွေ့ရှိခြင်း ဖြစ်သည့်အခါ lineage က မည်သည့် dataset များ၊ embedding များ၊ evaluation များနှင့် model artifact များ သက်ရောက်နိုင်သည်ကို ဖော်ထုတ်ပေးသည်။
- **မကြာခဏ ရောထွေးမှု:** data provenance သည် မူလရင်းမြစ်နှင့် ထိန်းသိမ်းမှုကို ကျယ်ပြန့်စွာ ရှင်းလင်းသည်။ lineage သည် data artifact များအကြား transformation လမ်းကြောင်းနှင့် မှီခိုမှုများကို အလေးပေးသည်။
- **လက်တွေ့:** input နှင့် output များအတွက် တည်ငြိမ်သည့် identifier ပေးရမည်၊ transformation နှင့် version တိုင်းကို မှတ်တမ်းတင်ရမည်၊ parent-child ဆက်စပ်မှုကို ထိန်းသိမ်းရမည်၊ သက်ရောက်သည့် source တစ်ခုကို ၎င်း၏ ဆင်းသက်လာသည့် artifact တိုင်းအထိ ခြေရာခံနိုင်ခြင်း ရှိမရှိ စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Data Provenance, Datasheet for Datasets, Audit Log, Content Provenance
- **English (source):** A record of how a data artifact was derived across sources, transformations, joins, filters, versions, and downstream uses. When a source is corrected, revoked, or found unsafe, lineage identifies which datasets, embeddings, evaluations, and model artifacts may be affected.

### Data Minimization

**မြန်မာ:** data အနည်းဆုံး အသုံးပြုခြင်း (data minimization)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** personal data အတွက် သတ်မှတ်ထားသည့် ရည်ရွယ်ချက် တစ်ခုအတွက် လိုအပ်သည့် ပမာဏအတိုင်းသာ စုဆောင်းခြင်း၊ ဆောင်ရွက်ခြင်း၊ ဖော်ထုတ်ခြင်းနှင့် ထိန်းသိမ်းခြင်းကို ကန့်သတ်ခြင်း ဖြစ်သည်။ အဖွဲ့များသည် တူညီသည့် စည်းကမ်းကို sensitive ဖြစ်သည့် personal မဟုတ်သည့် data အတွက်လည်း အင်ဂျင်နီယာ control တစ်ခုအဖြစ် ကျင့်သုံးနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** prompt၊ trace၊ cache သို့မဟုတ် tool call ထဲသို့ ထည့်သည့် မလိုအပ်သည့် field တိုင်းသည် privacy ဖော်ထုတ်ခံရမှုနှင့် အလွဲသုံးစားလုပ်မှု သို့မဟုတ် compromise ဖြစ်မှု၏ ဖြစ်နိုင်သည့် သက်ရောက်မှုကို တိုးစေသည်။
- **မကြာခဏ ရောထွေးမှု:** minimization သည် data လုံးဝ မသိမ်းဆည်းခြင်း မဟုတ်ပါ။ data element၊ အသုံးပြုမှု၊ လက်ခံသူနှင့် ထိန်းသိမ်းသည့် ကာလ တိုင်းကို ကြေညာထားသည့် ရည်ရွယ်ချက်နှင့် ကိုက်ညီကြောင်း အကြောင်းပြနိုင်ခြင်းကို ဆိုလိုသည်။
- **လက်တွေ့:** မစုဆောင်းမီ လိုအပ်သည့် field များကို သတ်မှတ်ရမည်၊ အစောဆုံး boundary တွင် redact သို့မဟုတ် aggregate လုပ်ရမည်၊ ထိန်းသိမ်းသည့် ကန့်သတ်ချက် သတ်မှတ်ရမည်၊ optional context သည် တိုင်းတာထားသည့် task ရလဒ်ကို တိုးတက်စေသည် ရှိမရှိ အတည်ပြုပြီးမှ ဆက်လက် သိမ်းဆည်းရမည်။
- **ဆက်စပ် term များ:** Purpose Limitation, Data Classification, Least Privilege, Context Engineering
- **English (source):** For personal data, limiting what is collected, processed, exposed, and retained to what is necessary for a specified purpose. Teams can apply the same discipline to sensitive non-personal data as an engineering control. Every unnecessary field placed in a prompt, trace, cache, or tool call increases privacy exposure and the possible impact of misuse or compromise.

### Datasheet for Datasets

**မြန်မာ:** dataset အတွက် datasheet

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** dataset တစ်ခု၏ ရည်ရွယ်ချက် (motivation)၊ ဖွဲ့စည်းမှု၊ စုဆောင်းသည့် လုပ်ငန်းစဉ်၊ preprocessing၊ အသုံးပြုမှုများ၊ ဖြန့်ဖြူးမှု၊ ထိန်းသိမ်းမှုနှင့် သိရှိထားသည့် ကန့်သတ်ချက်များကို ဖွဲ့စည်းထားသည့် အတိုင်း မှတ်တမ်းတင်ခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** dataset တစ်ခုသည် ရရှိနိုင်သည် ဆိုသည့် အချက်တစ်ချက်တည်းဖြင့် ဘေးကင်းသည် သို့မဟုတ် သင့်လျော်သည် မဟုတ်ပါ။ ဆင်းသက် တည်ဆောက်သူများသည် ၎င်းကို မည်သို့ ဖန်တီးခဲ့သည် နှင့် ၎င်း၏ ယူဆချက်များ မည်သည့်နေရာတွင် ချို့ယွင်းသည် ဆိုသည့် အထောက်အထား လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** datasheet သည် အထောက်အထားနှင့် ရည်ရွယ်ထားသည့် အသုံးပြုမှုကို မှတ်တမ်းတင်သည်။ ၎င်းသည် license၊ အရည်အသွေး အာမခံချက် သို့မဟုတ် deployment အလိုက် evaluation ကို အစားထိုးခြင်း မဟုတ်ပါ။
- **လက်တွေ့:** datasheet ကို version သတ်မှတ်ထားသည့် dataset နှင့်အတူ ထုတ်ဝေရမည်၊ မေးခွန်း ဖြေနိုင်သူများကို ဖော်ထုတ်ရမည်၊ ဖယ်ထုတ်ထားသည့် လူအုပ်စုများနှင့် transformation များကို မှတ်တမ်းတင်ရမည်၊ dataset ပြောင်းလဲသည့်အခါ စာရွက်စာတမ်းကို ပြန်လည် ပြင်ဆင်ရမည်။
- **ဆက်စပ် term များ:** Data Lineage, Data Provenance, Model Card, Dataset Split
- **Learn it:** [Model, System, and Dataset Cards](../phases/18-ethics-safety-alignment/26-model-system-dataset-cards/)
- **English (source):** Structured documentation of a dataset's motivation, composition, collection process, preprocessing, uses, distribution, maintenance, and known limitations. A dataset is not safe or suitable merely because it is available. Downstream builders need evidence about how it was created and where its assumptions break.

### Defense in Depth

**မြန်မာ:** အလွှာလိုက် ကာကွယ်မှု (defense in depth)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** system boundary အများအပြားတွင် တစ်ခုနှင့်တစ်ခု အမှီအခိုကင်းသည့် preventive၊ detective နှင့် corrective control များကို အသုံးပြုခြင်း ဖြစ်သည်။ ထိုသို့ အသုံးပြုခြင်းဖြင့် control တစ်ခု ပျက်ကွက်လျှင် ရလဒ်ကို ၎င်းတစ်ခုတည်းက မဆုံးဖြတ်နိုင်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** AI စနစ်များသည် probabilistic model များ၊ ယုံကြည်မှု မထားနိုင်သည့် အကြောင်းအရာများ၊ tool များနှင့် ပြင်ပ service များကို ပေါင်းစပ်ထားသည့်အတွက် filter တစ်ခုတည်း သို့မဟုတ် prompt တစ်ခုတည်းသည် လုံခြုံရေး boundary အဖြစ် မလုံလောက်ပါ။
- **မကြာခဏ ရောထွေးမှု:** control ပိုများလျှင် အလိုအလျောက် ပိုကောင်းသည် မဟုတ်ပါ။ အလွှာများသည် မတူညီသည့် failure mode များကို ကိုင်တွယ်ရမည် ဖြစ်ပြီး တူညီသည့် ယူဆချက်ကို ထပ်ကျော့ခြင်း မဟုတ်ဘဲ စမ်းသပ်နိုင်သည့် အနေအထားတွင် ရှိရမည်။
- **လက်တွေ့:** instruction ဆိုင်ရာ control များကို ကျဉ်းမြောင်းသည့် permission များ၊ sandboxing၊ schema validation၊ အကျိုးဆက် ရှိသည့် လုပ်ဆောင်ချက်များအတွက် approval၊ monitoring နှင့် စမ်းသပ်ပြီးသည့် recovery လမ်းကြောင်းတို့နှင့် တွဲဖက်ရမည်။
- **ဆက်စပ် term များ:** Guardrails, Sandbox, Least Privilege, Trust Boundary
- **English (source):** Using independent preventive, detective, and corrective controls at several system boundaries so one failed control does not determine the outcome. AI systems combine probabilistic models, untrusted content, tools, and external services, making any single filter or prompt an inadequate security boundary.

### Indirect Prompt Injection

**မြန်မာ:** သွယ်ဝိုက် prompt injection

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သုံးစွဲသူ၏ ညွှန်ကြားချက်မှတစ်ဆင့် တိုက်ရိုက် မဟုတ်ဘဲ စနစ်က ရယူသည် သို့မဟုတ် လေ့လာသည် ဖြစ်သည့် အကြောင်းအရာ (webpage၊ document၊ email၊ ရုပ်ပုံ အတွင်း စာသား သို့မဟုတ် tool ရလဒ်) မှတစ်ဆင့် ပို့ဆောင်သည့် prompt-injection တိုက်ခိုက်မှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** agent သည် ခွင့်ပြုထားသည့် task တစ်ခုကို ဆောင်ရွက်စဉ် တိုက်ခိုက်သူ ထိန်းချုပ်ထားသည့် ညွှန်ကြားချက်များကို ကြုံတွေ့နိုင်ပြီး ထို အကြောင်းအရာကို အာဏာပါသည့် လမ်းညွှန်ချက်အဖြစ် မှားယွင်း သတ်မှတ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** indirect သည် ပို့ဆောင်သည့် လမ်းကြောင်းကို ဖော်ပြသည်၊ ပိုအားနည်းသည့် တိုက်ခိုက်မှုကို မဆိုလိုပါ။ ရယူထားသည့် အကြောင်းအရာ အတွင်း ဝှက်ထားသည့် ညွှန်ကြားချက်သည် သုံးစွဲသူ၏ တိုက်ရိုက် prompt ကဲ့သို့ပင် အကျိုးဆက် ရှိနိုင်သည်။
- **လက်တွေ့:** ပြင်ပ အကြောင်းအရာကို ယုံကြည်မှု မထားနိုင်သည့် data အဖြစ် label တပ်ရမည်၊ ၎င်းကို ညွှန်ကြားချက်များနှင့် ခွဲခြားရမည်၊ tool permission များကို အနည်းဆုံးဖြစ်စေရမည်၊ အကျိုးဆက် ရှိသည့် လုပ်ဆောင်ချက်များအတွက် approval တောင်းရမည်၊ အန္တရာယ်ရှိသည့် ရယူထားသည့် အကြောင်းအရာများကို regression test များတွင် ထည့်သွင်းရမည်။
- **ဆက်စပ် term များ:** Prompt Injection, Instruction Hierarchy, Trust Boundary, Data Exfiltration
- **Learn it:** [Indirect Prompt Injection](../phases/18-ethics-safety-alignment/15-indirect-prompt-injection/)
- **English (source):** A prompt-injection attack delivered through content the system retrieves or observes, such as a webpage, document, email, image text, or tool result, rather than directly through the user's instruction. An agent can encounter attacker-controlled instructions while performing an authorized task and mistake that content for authority-bearing guidance.

### Jailbreak

**မြန်မာ:** jailbreak (မော်ဒယ်၏ ကန့်သတ်ချက် ကျော်လွှားခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်၏ training သို့မဟုတ် application control များက ကာကွယ်ရန် ရည်ရွယ်ထားသည့် အပြုအမူကို ထုတ်လုပ်စေရန် ရည်ရွယ်သည့် ရန်လိုသည့် input သို့မဟုတ် အပြန်အလှန် ဆက်သွယ်သည့် နည်းဗျူဟာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အောင်မြင်သည့် jailbreak များသည် ကြေညာထားသည့် policy နှင့် တကယ့် အပြုအမူအကြား ကွာဟချက်ကို ဖော်ထုတ်ပေးသည်။ မော်ဒယ်သည် tool များ သို့မဟုတ် ကာကွယ်ထားသည့် data ကို ထိန်းချုပ်သည့်အခါ ထို ကွာဟချက်သည် ပို၍ အကျိုးဆက် ရှိလာနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** jailbreak သည် မော်ဒယ် သို့မဟုတ် စနစ်၏ အပြုအမူ ကန့်သတ်ချက်များကို ပစ်မှတ်ထားသည်။ prompt injection သည် ညွှန်ကြားချက် လိုက်နာမှုကို လမ်းလွဲစေပြီး များသောအားဖြင့် တိုက်ခိုက်သူ၏ ပန်းတိုင်ဆီသို့ ဦးတည်စေသည်။ အပြန်အလှန် ဆက်သွယ်မှု တစ်ခုတွင် နှစ်မျိုးလုံး ပါဝင်နိုင်သည်။
- **လက်တွေ့:** တားမြစ်ထားသည့် အပြုအမူများမှ test family များကို ထုတ်ယူရမည်၊ format နှင့် အပြန်အလှန် ဆက်သွယ်မှု အရှည်ကို ပြောင်းလဲရမည်၊ refusal နှင့် အန္တရာယ်ရှိသည့် ဖြည့်စွက်မှု နှစ်မျိုးလုံးကို တိုင်းတာရမည်၊ အတည်ပြုပြီးသည့် ပျက်ကွက်မှုများကို version သတ်မှတ်ထားသည့် adversarial eval များအဖြစ် ပြောင်းလဲရမည်။
- **ဆက်စပ် term များ:** Prompt Injection, Red Teaming, Guardrails, Eval Set
- **Learn it:** [Jailbreak Taxonomy](../phases/19-capstone-projects/82-jailbreak-taxonomy/)
- **English (source):** An adversarial input or interaction strategy intended to make a model produce behavior that its training or application controls are designed to prevent. Successful jailbreaks expose gaps between stated policy and actual behavior, and they can become more consequential when the model controls tools or protected data.

### Membership Inference

**မြန်မာ:** အဖွဲ့ဝင်ဖြစ်မှု ခန့်မှန်းသည့် တိုက်ခိုက်မှု (membership inference)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မော်ဒယ်၏ output များ သို့မဟုတ် အခြား ရရှိနိုင်သည့် အချက်ပြမှုများကို လေ့လာ၍ record တစ်ခု သို့မဟုတ် ဥပမာတစ်ခုသည် မော်ဒယ်၏ training data ထဲတွင် ပါဝင်ခဲ့သည် မပါဝင်ခဲ့သည် ကို ခန့်မှန်းသည့် တိုက်ခိုက်မှု ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မော်ဒယ်သည် record တစ်ခုကို စာလုံးတစ်လုံးမှ မပြန်ထုတ်သည့် အခြေအနေတွင်ပင် ခွဲခြားနိုင်သည့် အပြုအမူသည် sensitive dataset တစ်ခုတွင် ပါဝင်ခဲ့မှုနှင့် ပတ်သက်သည့် အချက်အလက်ကို ဖော်ထုတ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** membership inference သည် record တစ်ခု training တွင် ပါဝင်ခဲ့သည် မပါဝင်ခဲ့သည် ကို မေးသည်။ model extraction သည် မော်ဒယ်၏ အပြုအမူကို ပြန်ထုတ်ရန် ကြိုးစားသည်။ တိုက်ရိုက် memorization စစ်ဆေးမှုသည် အကြောင်းအရာကို ပြန်လည် ရယူနိုင်သည် မရယူနိုင်သည် ကို စမ်းသပ်သည်။
- **လက်တွေ့:** အမှန်တကယ် query interface အောက်တွင် ကိုယ်စားပြုသည့် member နှင့် non-member များကို စမ်းသပ်ရမည်၊ မလိုအပ်သည့် confidence အချက်ပြမှုများကို ကန့်သတ်ရမည်၊ data ဖော်ထုတ်ခံရမှုကို လျှော့ချရမည်၊ privacy ကာကွယ်မှုများကို အသုံးဝင်မှု လိုအပ်ချက်များနှင့် ချိန်ဆ၍ အကဲဖြတ်ရမည်။
- **ဆက်စပ် term များ:** Data Leakage, Data Minimization, Eval Set, Data Classification
- **Learn it:** [Differential Privacy for LLMs](../phases/18-ethics-safety-alignment/22-differential-privacy-for-llms/)
- **English (source):** An attack that estimates whether a particular record or example was included in a model's training data by observing model outputs or other accessible signals. Even when the model does not reproduce a record verbatim, distinguishable behavior can reveal information about participation in a sensitive dataset.

### Provenance Attestation

**မြန်မာ:** မူလဇာစ်မြစ် အတည်ပြုချက် (provenance attestation)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** artifact တစ်ခုကို ၎င်းကို မည်သို့၊ မည်သည့်နေရာတွင်၊ မည်သည့်အချိန်တွင်၊ မည်သည့် input များမှ ထုတ်လုပ်ခဲ့သည်ဆိုသည့် ကြေညာချက်များနှင့် ချိတ်ဆက်ပေးသည့်၊ စစ်မှန်ကြောင်း အတည်ပြုထားသည့် machine-readable metadata ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် automated policy နှင့် သုံးသပ်သူများအား လက်မှတ် မထိုးထားသည့် build note ကို ယုံကြည်ခြင်းအစား supply-chain ကြေညာချက်များကို စစ်ဆေးနိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** လက်မှတ် (signature) သည် attester ကို ဖော်ထုတ်ပြီး integrity ကို ကာကွယ်သည်။ attestation အတွင်းရှိ ကြေညာချက် တိုင်းသည် မှန်ကန်သည် ဆိုသည်ကို သက်သေမပြနိုင်ပါ။
- **လက်တွေ့:** build system အတွင်းတွင် attestation ကို ဖန်တီးရမည်၊ ၎င်းကို artifact digest များနှင့် ချိတ်ဆက်ရမည်၊ ထိန်းချုပ်ထားသည့် identity ဖြင့် လက်မှတ်ထိုးရမည်၊ ထုတ်ဝေမီ စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Data Provenance, Reproducible Build, Audit Log, Verification Gate
- **English (source):** Authenticated, machine-readable metadata that binds an artifact to claims about how, where, when, and from which inputs it was produced. It lets automated policy and reviewers verify supply-chain claims instead of trusting an unsigned build note.

### Purpose Limitation

**မြန်မာ:** ရည်ရွယ်ချက် ကန့်သတ်မှု (purpose limitation)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** personal data အတွက် သတ်မှတ်ထားပြီး ရှင်းလင်းသည့် ရည်ရွယ်ချက်များအတွက်သာ စုဆောင်းခြင်းနှင့် အသုံးပြုခြင်း ဖြစ်သည်။ အသုံးပြုမှု အသစ်တစ်ခုတွင် သင့်လျော်စွာ ကိုက်ညီသည့် သို့မဟုတ် ခွင့်ပြုချက် ရရှိသည့် အခြေခံ အကြောင်းရင်း ရှိပါက ခြွင်းချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** workflow တစ်ခုအတွက် လက်ခံနိုင်သည့် data သည် မော်ဒယ် training၊ evaluation၊ personalization သို့မဟုတ် မသက်ဆိုင်သည့် analytics အတွက် တိတ်ဆိတ်စွာ ပြန်လည် အသုံးပြုသည့်အခါ privacy နှင့် governance အန္တရာယ် ဖြစ်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** purpose limitation သည် data ကို မည်သည့် အတွက် အသုံးပြုသည် ကို ထိန်းချုပ်သည်။ data minimization သည် ထို ရည်ရွယ်ချက်အတွက် တကယ် လိုအပ်သည့် data ပမာဏကို ထိန်းချုပ်သည်။
- **လက်တွေ့:** dataset တိုင်းနှင့်အတူ ရည်ရွယ်ချက်ကို မှတ်တမ်းတင်ရမည်၊ pipeline အသစ်များကို access မပေးမီ ထို ရည်ရွယ်ချက်နှင့် ကိုက်ညီမှုကို စစ်ဆေးရမည်၊ ကိုက်ညီမှု မရှိသည့် အသုံးပြုမှုများကို ခွဲခြားရမည်၊ ရည်ရွယ်ချက် ပြောင်းလဲသည့်အခါ မှတ်တမ်းတင်ထားသည့် ဆုံးဖြတ်ချက် လိုအပ်သည်။
- **ဆက်စပ် term များ:** Data Minimization, Data Classification, AI Risk Assessment, Audit Log
- **English (source):** For personal data, collecting and using it only for specified, explicit purposes unless a new use has an appropriate compatible or authorized basis. Data that was acceptable for one workflow can create privacy and governance risk when silently reused for model training, evaluation, personalization, or unrelated analytics.

### Red Teaming

**မြန်မာ:** red teaming (ရန်လို စမ်းသပ်ခြင်း)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ခွင့်ပြုချက် ရရှိသည့် စမ်းသပ်သူများသည် မှတ်တမ်းတင်ထားသည့် ရည်ရွယ်ချက်များ၊ အန္တရာယ် ယူဆချက်များ၊ အခြေအနေများနှင့် အထောက်အထားများကို အသုံးပြု၍ ပျက်ကွက်မှုများကို ရှာဖွေသည့် ဖွဲ့စည်းထားသည့် ရန်လို စမ်းသပ်ခြင်း လုပ်ငန်းစဉ် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ပုံမှန် အရည်အသွေး စမ်းသပ်မှုများသည် ခြယ်လှယ်ခြင်း၊ အလွဲသုံးစားလုပ်ခြင်း၊ ပန်းတိုင် ပဋိပက္ခများ သို့မဟုတ် control များကို ကျော်လွှားရန် စိတ်ပိုင်းဖြတ်ထားသည့် ကြိုးစားမှုများအောက်တွင် စနစ် မည်သို့ ပြုမူသည်ကို များသောအားဖြင့် မစူးစမ်းပါ။
- **မကြာခဏ ရောထွေးမှု:** jailbreak prompt စာရင်းတစ်ခုသည် ပြည့်စုံသည့် red-team အစီအစဉ် မဟုတ်ပါ။ red teaming သည် မသိရသေးသည့် ပျက်ကွက်မှုများ မရှိကြောင်း သက်သေမပြနိုင်ပါ။
- **လက်တွေ့:** တိုက်ခိုက်မှုများကို threat model မှ ထုတ်ယူရမည်၊ သီးခြားခွဲထားသည့် ပတ်ဝန်းကျင်တွင် လုပ်ဆောင်ရမည်၊ ပြန်လည် ထုတ်လုပ်နိုင်သည့် အခြေအနေများကို မှတ်တမ်းတင်ရမည်၊ အလွှာအလိုက် ပြုပြင်ရမည်၊ အတည်ပြုပြီးသည့် ပျက်ကွက်မှုများကို regression eval များအဖြစ် ပြောင်းလဲရမည်။
- **ဆက်စပ် term များ:** Threat Model, Guardrails, Prompt Injection, Eval Set
- **English (source):** A structured adversarial testing process in which authorized testers seek failures using documented objectives, threat assumptions, cases, and evidence. Ordinary quality tests rarely explore how a system behaves under manipulation, misuse, conflicting goals, or determined attempts to bypass controls.

### Separation of Duties

**မြန်မာ:** တာဝန် ခွဲခြားခြင်း (separation of duties)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပဋိပက္ခ ဖြစ်သည့် တာဝန်များ သို့မဟုတ် အာဏာများကို အမှီအခိုကင်းသည့် အခန်းကဏ္ဍများအကြား ခွဲဝေခြင်း ဖြစ်သည်။ ထိုသို့ ခွဲဝေခြင်းဖြင့် principal တစ်ခုတည်းသည် အခြား ခွင့်ပြုချက် ရရှိသည့် ဆုံးဖြတ်ချက်တစ်ခု မပါဘဲ အန္တရာယ်မြင့်သည့် လုပ်ဆောင်ချက်ကို အပြီးသတ် ဆောင်ရွက်နိုင်မည် မဟုတ်ပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** ပျက်စီးသွားသည့် account တစ်ခု သို့မဟုတ် မှားယွင်းသည့် agent သည် အကျိုးဆက် ရှိသည့် ပြောင်းလဲမှု တစ်ခုတည်းကို အဆိုပြုခြင်း၊ အတည်ပြုခြင်း၊ ဆောင်ရွက်ခြင်းနှင့် ဖုံးကွယ်ခြင်း တို့ကို လုပ်နိုင်သည့် အခြေအနေ မရှိရမည်။
- **မကြာခဏ ရောထွေးမှု:** separation of duties သည် ပဋိပက္ခ ဖြစ်သည့် အာဏာအပေါ် အခြေခံသည်။ တူညီသည့် credential များကို မျှဝေ အသုံးပြုသည့် လူများ သို့မဟုတ် agent များအကြား အလုပ်ကို ခွဲဝေပေးခြင်း သက်သက် မဟုတ်ပါ။
- **လက်တွေ့:** artifact ဖန်တီးခြင်းနှင့် ထုတ်ဝေသည့် အတည်ပြုချက်ကို ခွဲခြားရမည်၊ မတူညီသည့် identity များ အသုံးပြုရမည်၊ ဆုံးဖြတ်ချက် နှစ်ခုလုံးကို audit log တွင် ထိန်းသိမ်းရမည်၊ အရေးပေါ် access ကို သတ်မှတ်ပြီး နောက်ပိုင်းတွင် ပြန်လည် သုံးသပ်ရမည်။
- **ဆက်စပ် term များ:** Approval Gate, Reviewer Agent, Audit Log, Least Privilege
- **English (source):** Dividing conflicting responsibilities or authority across independent roles so one principal cannot complete a high-risk action without another authorized decision. A compromised account or mistaken agent should not be able to propose, approve, execute, and conceal the same consequential change.

### Software Bill of Materials (SBOM)

**မြန်မာ:** software အစိတ်အပိုင်း စာရင်း (SBOM)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ထုတ်ကုန် တစ်ခု သို့မဟုတ် artifact တစ်ခုနှင့် သက်ဆိုင်သည့် software component များနှင့် ၎င်းတို့၏ ဆက်စပ်မှုများကို ဖွဲ့စည်းထားသည့် စာရင်း ဖြစ်သည်။ များသောအားဖြင့် version၊ supplier၊ license နှင့် identifier များ ပါဝင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** software ပြောင်းလဲသည့်အခါ သို့မဟုတ် vulnerability များ ပေါ်ပေါက်သည့်အခါ သက်ရောက်သည့် dependency များ၊ license တာဝန်များနှင့် supply-chain ဖော်ထုတ်ခံရမှုကို အကဲဖြတ်ရန် component စာရင်း လိုအပ်သည်။
- **မကြာခဏ ရောထွေးမှု:** SBOM သည် စာရင်းတစ်ခု ဖြစ်သည်။ ဖန်တီးမှုနှင့် provenance သည် ယုံကြည်စိတ်ချရသည် မဟုတ်ပါက component များ လုံခြုံသည်၊ license မှန်ကန်သည် သို့မဟုတ် တကယ် ရှိသည် ဆိုသည့် အထောက်အထား မဟုတ်ပါ။
- **လက်တွေ့:** SBOM ကို ယုံကြည်ရသည့် build အတွင်းတွင် ဖန်တီးရမည်၊ ထုတ်ဝေသည့် artifact နှင့် ချိတ်ဆက်ရမည်၊ policy စစ်ဆေးမှုများတွင် စစ်ရမည်၊ dependency သို့မဟုတ် packaging ပြောင်းလဲသည့် တိုင်း ပြန်လည် ပြင်ဆင်ရမည်။
- **ဆက်စပ် term များ:** Provenance Attestation, Reproducible Build, Data Provenance, Audit Log
- **English (source):** A structured inventory of software components and relationships associated with a product or artifact, often including versions, suppliers, licenses, and identifiers. You need a component inventory to assess affected dependencies, license obligations, and supply-chain exposure when software changes or vulnerabilities emerge.

### Threat Model

**မြန်မာ:** အန္တရာယ် ပုံစံ ရေးဆွဲခြင်း (threat model)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ကာကွယ်ရမည့် asset များ၊ trust boundary များ၊ ဖြစ်နိုင်သည့် ရန်သူများ၊ ယူဆထားသည့် စွမ်းရည်များ၊ တိုက်ခိုက်သည့် လမ်းကြောင်းများ၊ သက်ရောက်မှုများနှင့် စီစဉ်ထားသည့် control များကို မှတ်တမ်းတင်ထားသည့် ဖော်ပြချက် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** လုံခြုံရေး control များသည် မည်သည့်အရာကို ကာကွယ်သည်၊ မည်သူကို ဆန့်ကျင်သည်၊ မည်သည့် ယူဆချက်များအောက်တွင် ဆိုသည်တို့ကို မဖော်ပြဘဲ အကဲဖြတ်နိုင်မည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** threat model သည် ဖြစ်နိုင်ခြေရှိသည့် အန္တရာယ်များကို ဦးစားပေး စီစဉ်သည်။ ၎င်းသည် စနစ် လုံခြုံကြောင်း သက်သေပြသည့် စစ်ဆေးစာရင်း သို့မဟုတ် အနာဂတ် တိုက်ခိုက်မှု တိုင်းကို ကြိုတင် ခန့်မှန်းသည့် အရာ မဟုတ်ပါ။
- **လက်တွေ့:** data နှင့် အာဏာကို model၊ retrieval၊ tool များ၊ သုံးစွဲသူများနှင့် ပြင်ပ service များအကြား mapping လုပ်ရမည်။ ထို့နောက် ဖြစ်နိုင်ခြေရှိသည့် အလွဲသုံးစားလုပ်သည့် လမ်းကြောင်းများကို red-team အခြေအနေများနှင့် လျော့ပါးစေသည့် နည်းလမ်းများအဖြစ် ပြောင်းလဲရမည်။
- **ဆက်စပ် term များ:** Least Privilege, Prompt Injection, Sandbox, Red Teaming
- **English (source):** A documented account of protected assets, trust boundaries, potential adversaries, assumed capabilities, attack paths, impacts, and planned controls. Security controls cannot be judged without stating what they defend, against whom, and under which assumptions.

### Trust Boundary

**မြန်မာ:** ယုံကြည်မှု နယ်နိမိတ် (trust boundary)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** မတူညီသည့် ယုံကြည်မှု ယူဆချက်များအောက်တွင် လည်ပတ်သည့် component များ သို့မဟုတ် principal များအကြား data၊ ညွှန်ကြားချက်၊ identity သို့မဟုတ် အာဏာ ဖြတ်ကူးသည့် ကြားခံ မျက်နှာပြင် (interface) ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** boundary ဖြတ်ကူးသည့် နေရာသည် စနစ်က လုပ်ဆောင်သူများကို စစ်မှန်ကြောင်း အတည်ပြုရမည်၊ data ကို validate လုပ်ရမည်၊ permission များကို ကန့်သတ်ရမည်၊ မည်သည့် ကြေညာချက်များက လုပ်ဆောင်မှုကို သက်ရောက်နိုင်သည်ကို ဆုံးဖြတ်ရမည့် နေရာ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** network boundary သည် trust boundary အမျိုးအစားများအနက် တစ်မျိုးသာ ဖြစ်သည်။ ယုံကြည်မှု မထားနိုင်သည့် document စာသားသည် အာဏာ ရှိသည့် agent context ထဲသို့ ဝင်လာခြင်းသည်လည်း boundary တစ်ခုကို ဖြတ်ကူးခြင်း ဖြစ်သည်။
- **လက်တွေ့:** သုံးစွဲသူများ၊ model context၊ retrieval source များ၊ tool များ၊ network များနှင့် data store များ ပတ်လည်တွင် boundary များကို ရေးဆွဲရမည်။ ထို့နောက် ဖြတ်ကူးမှု တိုင်းအတွက် validation နှင့် authorization ကို သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Threat Model, Least Privilege, Sandbox, Indirect Prompt Injection
- **Learn it:** [Jailbreak Taxonomy](../phases/19-capstone-projects/82-jailbreak-taxonomy/)
- **English (source):** An interface where data, instructions, identity, or authority crosses between components or principals that operate under different trust assumptions. A boundary crossing is where the system must authenticate actors, validate data, constrain permissions, and decide which claims can influence action.

### Zero Trust

**မြန်မာ:** zero trust (ယုံကြည်မှု သုည ပုံစံ)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** network တည်နေရာ သို့မဟုတ် asset ပိုင်ဆိုင်မှုမှ သွယ်ဝိုက် ယုံကြည်မှု တစ်စုံတစ်ရာ မပေးသည့် လုံခြုံရေး model ဖြစ်သည်။ အစား ၎င်းသည် access တောင်းခံမှု တိုင်းကို identity၊ device၊ resource၊ policy နှင့် လက်ရှိ context တို့နှင့် ချိန်ဆ၍ အကဲဖြတ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** AI tool များနှင့် agent များသည် local file များ၊ cloud service များ၊ မော်ဒယ်များနှင့် ပြင်ပ အကြောင်းအရာများကို ဖြတ်ကူးသည့်အတွက် ယုံကြည်ရသည့် internal network ဆိုသည်မှာ အာဏာအတွက် ကျယ်ပြန့်လွန်းသည့် အခြေခံ ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** zero trust သည် မည်သည့်အရာကိုမျှ မယုံကြည်ခြင်း သို့မဟုတ် automation အားလုံးကို ပိတ်ခြင်း မဟုတ်ပါ။ ယုံကြည်မှု ဆုံးဖြတ်ချက်များကို ရှင်းလင်းစွာ ဖော်ပြခြင်း၊ နယ်ပယ် သတ်မှတ်ခြင်းနှင့် အဆက်မပြတ် စစ်ဆေးနိုင်ခြင်းကို ဆိုလိုသည်။
- **လက်တွေ့:** လုပ်ဆောင်သူနှင့် workload တိုင်းကို authenticate လုပ်ရမည်၊ resource လုပ်ဆောင်ချက် တိုင်းကို authorize လုပ်ရမည်၊ သက်တမ်းတို credential များ ထုတ်ပေးရမည်၊ access ကို segment ခွဲရမည်၊ policy နှင့် သက်ဆိုင်သည့် အချက်ပြမှုများကို အဆက်မပြတ် မှတ်တမ်းတင်ပြီး ပြန်လည် အကဲဖြတ်ရမည်။
- **ဆက်စပ် term များ:** Least Privilege, Trust Boundary, Approval Gate, Audit Log
- **Learn it:** [Security, Secrets, and Audit](../phases/17-infrastructure-and-production/25-security-secrets-audit/)
- **English (source):** A security model that grants no implicit trust from network location or asset ownership and instead evaluates each access request against identity, device, resource, policy, and current context. AI tools and agents span local files, cloud services, models, and external content, so a trusted internal network is too broad a basis for authority.

## Self-check

၁။ threat model နှင့် AI risk assessment သည် မည်သို့ ကွာခြားသနည်း။
၂။ audit log သည် trace နှင့် မည်သို့ ကွာခြားသနည်း။
၃။ trust boundary ကို ဖြတ်ကူးသည့် အခါ စနစ်က မည်သည့် အရာများကို စစ်ဆေးရမည်နည်း။
၄။ indirect prompt injection သည် prompt injection နှင့် မည်သို့ ကွာခြားသနည်း။
၅။ data minimization နှင့် purpose limitation သည် မည်သည့် မေးခွန်းကို အသီးသီး ဖြေသနည်း။

<details>
<summary>အဖြေများ</summary>

၁။ threat model သည် ကာကွယ်ရမည့် asset၊ trust boundary၊ ရန်သူနှင့် တိုက်ခိုက်သည့် လမ်းကြောင်းကို ဖော်ပြပြီး
ဖြစ်နိုင်ခြေရှိသည့် အန္တရာယ်များကို ဦးစားပေး စီစဉ်သည်။ AI risk assessment သည် deploy လုပ်သည့် context၊
ထိခိုက်ခံရသည့် လူအုပ်စုများ၊ control များ၊ residual risk နှင့် စောင့်ကြည့်ရန် တာဝန်များအထိ ပါဝင်သည့်
မှတ်တမ်းတင်ထားသည့် ခွဲခြမ်းစိတ်ဖြာမှု ဖြစ်သည်။ အနှစ်ချုပ်အားဖြင့် threat model သည် ရန်သူနှင့် လမ်းကြောင်းကို
ဖော်ပြသည်၊ risk assessment သည် ဆုံးဖြတ်ချက်အတွက် အန္တရာယ် အဆင့်ကို အကဲဖြတ်သည်။

၂။ trace သည် execution path တစ်ခုကို ရောဂါရှာဖွေရန် ကူညီသည်။ audit log သည် execution အများနှင့်
အချိန်ကြာလာသည့်အခါ တာဝန်ခံမှုအတွက် လိုအပ်သည့် ဖြစ်ရပ်များကို ကြာရှည်ခံ၍ access control ဖြင့်
ထိန်းသိမ်းသည်။

၃။ လုပ်ဆောင်သူများကို authenticate လုပ်ခြင်း၊ data ကို validate လုပ်ခြင်း၊ permission များကို ကန့်သတ်ခြင်း၊
မည်သည့် ကြေညာချက်များက လုပ်ဆောင်မှုကို သက်ရောက်နိုင်သည်ကို ဆုံးဖြတ်ခြင်း တို့ ဖြစ်သည်။

၄။ indirect သည် ပို့ဆောင်သည့် လမ်းကြောင်းကို ဖော်ပြသည် — တိုက်ခိုက်မှုသည် သုံးစွဲသူ၏ ညွှန်ကြားချက်မှ
မဟုတ်ဘဲ စနစ်က ရယူသည် သို့မဟုတ် လေ့လာသည် ဖြစ်သည့် အကြောင်းအရာ (webpage၊ document၊ email၊
tool ရလဒ်) မှတစ်ဆင့် လာသည်။ ပိုအားနည်းသည့် တိုက်ခိုက်မှု မဆိုလိုပါ။

၅။ data minimization သည် ရည်ရွယ်ချက် တစ်ခုအတွက် မည်မျှ data လိုအပ်သည် ကို ထိန်းချုပ်သည်။
purpose limitation သည် ထို data ကို မည်သည့် အတွက် အသုံးပြုသည် ကို ထိန်းချုပ်သည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT license)
- Source ဖိုင် — `glossary/terms.md`

Term တိုင်း၏ ကိုးကား —

- **AI Risk Assessment** — [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- **Audit Log** — [NIST SP 800-92](https://csrc.nist.gov/pubs/sp/800/92/final)
- **Content Provenance** — [C2PA Technical Specification](https://c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html)
- **Data Classification** — [NIST SP 1800-39 Initial Public Draft: Data Classification Practices](https://www.nccoe.nist.gov/sites/default/files/2026-02/nist-sp-1800-39-ipd.pdf); [NIST FIPS 199: Federal Information and Information System Categorization](https://csrc.nist.gov/pubs/fips/199/final)
- **Data Exfiltration** — [NIST SP 800-53 Rev. 5: AC-4 Information Flow Enforcement](https://csrc.nist.gov/files/pubs/sp/800/53/r5/upd1/final/docs/sp800-53r5-controls.xlsx)
- **Data Lineage** — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- **Data Minimization** — [General Data Protection Regulation, Article 5(1)(c)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Datasheet for Datasets** — [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)
- **Defense in Depth** — [NIST Glossary: Defense in Depth](https://csrc.nist.gov/glossary/term/defense_in_depth)
- **Indirect Prompt Injection** — [Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173)
- **Jailbreak** — [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043)
- **Membership Inference** — [Membership Inference Attacks Against Machine Learning Models](https://doi.org/10.1109/SP.2017.41)
- **Provenance Attestation** — [SLSA Software Attestations](https://slsa.dev/spec/v1.2/attestation-model)
- **Purpose Limitation** — [General Data Protection Regulation, Article 5(1)(b)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- **Red Teaming** — [Red Teaming Language Models with Language Models](https://arxiv.org/abs/2202.03286)
- **Separation of Duties** — [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Software Bill of Materials (SBOM)** — [SPDX 3.0.1 specification](https://spdx.github.io/spdx-spec/v3.0/)
- **Threat Model** — [NIST SP 800-154](https://csrc.nist.gov/pubs/sp/800/154/ipd); [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.600-1.pdf)
- **Trust Boundary** — [Microsoft Learn: Trust Boundary, the Trust Zone Change Element](https://learn.microsoft.com/en-us/training/modules/tm-create-a-threat-model-using-foundational-data-flow-diagram-elements/6-trust-boundary-the-trust-zone-change-element); [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- **Zero Trust** — [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)

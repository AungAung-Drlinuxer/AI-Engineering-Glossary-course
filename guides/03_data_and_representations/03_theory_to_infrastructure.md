# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၃ ၏ term ၁၃ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။ အချက်အလက်နှင့် ကိုယ်စားပြုမှု (data and representations) ဆိုင်ရာ ဆုံးဖြတ်ချက် တစ်ခုသည် စာတမ်းအတွင်း သီအိုရီ အဖြစ်သာ မကျန်ရပါ။ ၎င်းသည် သိုလှောင်မှု ပမာဏ၊ accelerator အလုပ်ပမာဏ၊ လေ့ကျင့်မှု လုပ်ဆောင်ရန် အချိန်၊ data pipeline ၏ စွမ်းဆောင်ရည် သို့မဟုတ် epoch တစ်ခု၏ ကုန်ကျစရိတ် အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းဂဏန်း တစ်ခုစီသည် ထုတ်လုပ်မှု အခြေအနေတွင် တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/03_data_and_representations/scripts/` အောက်ရှိ Python script များနှင့် `guides/03_data_and_representations/labs/` အောက်ရှိ lab များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ script များနှင့် lab များသည် standard library သာ အသုံးပြုပြီး offline တွင် deterministic ဖြစ်သည်။ ကုန်ကျစရိတ်၊ bandwidth နှင့် စျေးနှုန်း အပေါ် မှီခိုသည့် တန်ဖိုးတိုင်းကို `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်` ဟု မှတ်သားထားသည်။ ဤစာတမ်းသည် အတိုင်းအတာ တိုင်းတာမှု (benchmark) ရလဒ် များကို ဖော်ပြခြင်း မပြုပါ။ ဖော်ပြသည့် တန်ဖိုး အားလုံးသည် ဖော်မြူလာ နှင့် ယူဆချက် (assumption) မှ တွက်ချက်ထားသည့် တန်ဖိုးများ ဖြစ်သည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**storage and VRAM** — disk ပေါ်တွင် သို့မဟုတ် accelerator ၏ memory ပေါ်တွင် တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ corpus အပြည့်အစုံ၊ token id shard များ၊ embedding matrix၊ output layer နှင့် logits tensor အားလုံး ဤဝင်ရိုးထဲတွင် ရေတွက်သည်။ VRAM ပြည့်လျှင် အလုပ်လုပ်နိုင်ခြင်း ရပ်တန့်သည်၊ ထို့ကြောင့် ဤဝင်ရိုးသည် အမာခံ ကန့်သတ်ချက် ဖြစ်သည်။

**compute** — တောင်းဆိုမှု သို့မဟုတ် step တစ်ခုအတွက် လိုအပ်သည့် floating-point operation ပမာဏ ဖြစ်သည်။ တူညီသည့် ရလဒ်အတွက် FLOPs နည်းခြင်းသည် စရိတ် နည်းခြင်း ဖြစ်သည်။ ဤဝင်ရိုးတွင် ကိန်းဂဏန်း ရွေ့လျားမှုသည် accelerator အရေအတွက် နှင့် လုပ်ဆောင်ချိန် ကို ဆုံးဖြတ်သည်။

**ingestion and training wall-clock** — corpus ကို ရယူခြင်း၊ သန့်စင်ခြင်း၊ သိမ်းဆည်းခြင်း နှင့် လေ့ကျင့်ခြင်း အားလုံး ပြီးစီးရန် လိုအပ်သည့် အချိန် ဖြစ်သည်။ ဤဝင်ရိုးသည် ကုန်ကျစရိတ် နှင့် လုပ်ဆောင်နိုင်သည့် စမ်းသပ်မှု အရေအတွက် ကို တိုက်ရိုက် သတ်မှတ်သည်။

**data pipeline throughput** — data ပြင်ဆင်ရေး လမ်းကြောင်း (encode၊ pack၊ shard ဖတ်ခြင်း၊ batch အဖြစ် စုခြင်း) သည် တစ်စက္ကန့်လျှင် token မည်မျှ ပေးနိုင်သည်ကို တိုင်းတာသည်။ ၎င်းသည် accelerator လိုအပ်ချက်အောက် ကျဆင်းလျှင် accelerator သည် အားလပ်နေသည်၊ ဆိုလိုသည်မှာ ဝယ်ထားသည့် compute ကို မသုံးရခြင်း ဖြစ်သည်။

**cost per token or per epoch** — ထုတ်လုပ်မှု ကုန်ကျစရိတ်ကို token အရေအတွက် သို့မဟုတ် epoch အရေအတွက်ဖြင့် စားထားသည့် တန်ဖိုး ဖြစ်သည်။ တူညီသည့် စာသားအတွက် token အရေအတွက် ကွာခြားလျှင် ကုန်ကျစရိတ် လည်း ကွာခြားသည်၊ ထို့ကြောင့် ဤဝင်ရိုးသည် tokenizer နှင့် data ရွေးချယ်မှု အပေါ် တိုက်ရိုက် မှီခိုသည်။ စျေးနှုန်း အပေါ် မှီခိုသည့် တန်ဖိုးတိုင်းသည် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် ထုတ်လုပ်မှု တွင် မည်သည့် အရာ ကျိုးပျက်မည်ကို ဆိုလိုသည်။ ဥပမာ evaluation split ထဲမှ အချက်အလက် ယိုစိမ့်လျှင် model မကောင်းခြင်း မဟုတ်ဘဲ တိုင်းတာသည့် ကိန်း မှားလာခြင်းသည် ထုတ်လုပ်မှု အကျိုးဆက် ဖြစ်သည်။

## ၂။ Master table — term ၁၃ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Byte Pair Encoding (BPE) | cost per token or per epoch | merge တိုးလျှင် vocabulary ကြီးပြီး တူညီသည့် စာသားအတွက် token ကျဆင်းသည် | burmese 136 → 110 tokens (merges 0 → 10); vocabulary 60 → 70 | tokenizer ကို version မမှတ်လျှင် ကုန်ကျစရိတ် တွက်ချက်မှု မှား |
| Cosine Similarity | compute | နှိုင်းယှဉ်မှု တစ်ခုစီသည် d_model အလျား၏ multiply-add လိုသည် | d_model = 4096 multiply-add per comparison | vector store သည် candidate အရေအတွက်ဖြင့် ကုန်ကျစရိတ် သတ်မှတ်သည် |
| Data Deduplication | ingestion and training wall-clock | ထပ်တူ token ဖယ်ရှားခြင်းဖြင့် လေ့ကျင့်ရမည့် token လျော့သည် | unique tokens 20,480,000,000 → 16,793,600,000 (18.0% drop) | dedupe မလုပ်လျှင် memorization တက်ပြီး evaluation သည် အမှန်တကယ်ထက် ကောင်းဟန် ထင်ရသည် |
| Data Leakage | production consequence | အကောင်းဘက် လွန်ကဲသည့် metric ကို ဖန်တီးသည် | reported − clean accuracy = +0.0354 | deployment တွင် ထို metric ပြိုလဲပြီး အမှန်တကယ် မမြင်ဖူးသည့် input များတွင် ကျရှုံးသည် |
| Data Provenance | production consequence | ရလဒ် ပြန်လည် ဖန်တီးနိုင်မှုကို ဝယ်ယူသည် | artifact တိုင်း၏ lineage record ရာခိုင်နှုန်း | source ပြောင်းလျှင် ထိခိုက်သည့် data ကို ဖယ်ရှားနိုင်ခြင်း ပျောက်သည် |
| Dataset Split | production consequence | ရွေးချယ်ရာတွင် အသုံးပြုသည့် အထောက်အထားနှင့် သက်သေကို ခွဲထားသည် | contamination rate 15.75% (row split) → 0.00% (group split) | split မှားလျှင် evaluation သည် လွန်ကဲသည့် ယုံကြည်စရာ ဖြစ်လာ |
| Embedding | storage and VRAM | vocabulary × d_model matrix ကို VRAM ပေါ် ထားသည် | tied 1,000.00 MiB / untied 2,000.00 MiB (vocab 128000, d 4096) | vocabulary ကြီးလျှင် accelerator တစ်လုံးပေါ် တွင် မဆံ့ |
| Feature | compute | classical ML တွင် လက်ဖြင့် တည်ဆောက်သည်၊ deep learning တွင် network က သင်ယူသည် | per-example FLOPs | feature ရွေးချယ်မှုသည် training budget အပေါ် တိုက်ရိုက် ကျသည် |
| Latent Space | storage and VRAM | latent dimension က representation တစ်ခု၏ byte ကို ဆုံးဖြတ်သည် | d_model 1024 → 8192 သည် matrix parameter 131,072,000 → 1,048,576,000 | latent ကြီးလျှင် step တိုင်း၏ VRAM တက် |
| Tensor | storage and VRAM | shape × data type = byte | logits tensor 15.625 MiB (seq 1) → 125.000 GiB (seq 8192, batch 32) | dtype နှင့် shape ကို မစစ်လျှင် accelerator တွင် OOM ဖြစ်သည် |
| Token | cost per token or per epoch | target tokenizer အလိုက် တူညီသည့် byte မှ token အရေအတွက် ကွာခြားသည် | bytes/token 2.49 (overall), burmese 1.2, english 4.0 (ex_a) | provider tool နှင့် ကိုယ်ပိုင် tokenizer ရောထွေးလျှင် ကုန်ကျစရိတ် မှား |
| Tokenization | data pipeline throughput | encode ကုန်ကျစရိတ်သည် accelerator ကို ကျွေးနိုင်မှုကို ဆုံးဖြတ်သည် | 20 µs/token → utilisation 66.29%; ≤ 10 µs/token → 100.00% | encoder နှေးလျှင် accelerator အားလပ်နေပြီး ကုန်ကျစရိတ် မလျော့ |
| Vocabulary | storage and VRAM | vocabulary က embedding အရွယ်အစား နှင့် output layer memory ကို ဆုံးဖြတ်သည် | vocab 128000 → 524,288,000 parameter; 7.0B model ၏ 14.98% | vocabulary နှင့် model weight ကို တွဲမထားလျှင် weight ကို မသုံးနိုင် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု သုံးခုဖြင့် စုစည်းထားသည် — (က) token နှင့် စာသား ကိုယ်စားပြုမှု၊ (ခ) vector နှင့် ကိုယ်စားပြုမှု၊ (ဂ) data တည်ငြိမ်မှုနှင့် ခြေရာခံမှု။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — token နှင့် စာသား ကိုယ်စားပြုမှု

#### Tokenization

Tokenization သည် input representation တစ်ခုကို model လက်ခံသည့် အစဉ်လိုက် token identifier များအဖြစ် ပြောင်းလဲသည့် အလွှာ ဖြစ်သည်။ ဤအလွှာသည် sequence အရှည်၊ vocabulary နယ်နိမိတ်၊ ကုန်ကျစရိတ် တွက်ချက်မှု၊ truncation အပြုအမူ နှင့် embedding မပြုမီ စာသား သို့မဟုတ် code ၏ ပုံစံ အားလုံးကို ဆုံးဖြတ်သည်၊ ထို့ကြောင့် ၎င်း၏ primary axis သည် data pipeline throughput ဖြစ်သည်။ lab_pipeline_budget တွင် encoder သည် token တစ်လုံးလျှင် 20 မိုက်ခရိုစက္ကန့် ကုန်ကျလျှင် accelerator utilisation သည် 66.29% သို့ ကျဆင်းပြီး wall clock သည် 111.11 h ဖြစ်သည်၊ 10 မိုက်ခရိုစက္ကန့် အောက် ကျဆင်းလျှင် utilisation သည် 100.00% ရောက်ပြီး wall clock သည် 73.65 h ဖြစ်သည်။ data engineer သည် pipeline ပေးနိုင်မှုကို tokens/s အဖြစ် တိုင်း၍ accelerator လိုအပ်ချက် နှင့် တိုက်ရိုက် နှိုင်းယှဉ်ရမည်။

#### Token

Token သည် model-specific tokenizer က ထုတ်ပေးသည့် integer identifier တစ်ခု ဖြစ်သည်။ ၎င်းသည် စကားလုံး တစ်လုံးလုံး၊ စကားလုံး၏ အစိတ်အပိုင်း၊ punctuation၊ whitespace၊ byte sequence သို့မဟုတ် special control symbol ဖြစ်နိုင်သည်။ token အရေအတွက်သည် language၊ content နှင့် tokenizer အလိုက် ကွာခြားသည့် character-to-token ratio အပေါ် မှီခိုသည့်အတွက် ၎င်းသည် cost per token ဝင်ရိုး၏ အခြေခံ ယူနစ် ဖြစ်သည်။ ဥပမာ (က) တွင် 96 GiB corpus ၏ ပျမ်းမျှသည် token တစ်လုံးလျှင် 2.49 byte ဖြစ်ပြီး စုစုပေါင်း token သည် 41,354,399,392 ဖြစ်သည်၊ burmese အပိုင်းသည် token တစ်လုံးလျှင် 1.2 byte သာ ရှိသည်။ ထို့ကြောင့် တူညီသည့် byte ပမာဏအတွက် မြန်မာ စာသားသည် token ပို လိုသည်၊ ဤအချက်သည် ကုန်ကျစရိတ် ခန့်မှန်းမှုတွင် ပါဝင်ရမည်။

#### Vocabulary

Vocabulary သည် token identifier များနှင့် tokenizer က ထုတ်နိုင်သည့် ယူနစ်များအကြား အကန့်အသတ် ရှိသည့် mapping ဖြစ်ပြီး သာမန် token များ၊ byte-level token များ နှင့် special control token များ ပါဝင်သည်။ ၎င်း၏ အရွယ်အစားသည် embedding matrix နှင့် output layer memory ကို တိုက်ရိုက် ဆုံးဖြတ်သည့်အတွက် primary axis သည် storage and VRAM ဖြစ်သည်။ ဥပမာ (ခ) တွင် vocabulary 128000 နှင့် d_model 4096 အတွက် matrix တစ်ခုလျှင် 524,288,000 parameter ဖြစ်ပြီး fp16 တွင် 1,000.00 MiB ဖြစ်သည်၊ embedding နှင့် output layer ကို မတွဲထားလျှင် 2,000.00 MiB ဖြစ်ပြီး 7.0B model ၏ 14.98% ဖြစ်သည်။ ထို့ကြောင့် vocabulary ရွေးချယ်မှုသည် multilingual coverage နှင့် VRAM အကြား လဲလှယ်မှု ဖြစ်သည်။

#### Byte Pair Encoding (BPE)

BPE သည် training text အတွင်း မကြာခဏ ဆက်တွဲ ဖြစ်ပေါ်နေသည့် အနီးကပ် ယူနစ်များကို အကြိမ်ကြိမ် merge လုပ်ခြင်းဖြင့် ပုံသေ vocabulary တစ်ခုကို တည်ဆောက်သည့် subword-tokenization နည်းလမ်း ဖြစ်သည်။ merge တစ်ခုစီသည် vocabulary ထဲသို့ ယူနစ် တစ်ခု ထည့်သည့်အတွက် merge အရေအတွက်သည် vocabulary အရွယ်အစား နှင့် sequence အရှည် နှစ်ခုလုံးကို တစ်ပြိုင်နက် ရွေ့လျားစေသည်။ ဥပမာ lab_tokenizer ၏ sweep တွင် merge 0 မှ 20 သို့ ရွေ့လျှင် burmese စာသားသည် token 136 မှ 97 သို့ ကျဆင်းပြီး vocabulary သည် 60 မှ 80 သို့ တက်သည်၊ english စာသားသည် token 86 မှ 63 သို့ ကျဆင်းသည်။ ဤလဲလှယ်မှုသည် cost per token (sequence အရှည်) နှင့် storage and VRAM (embedding အရွယ်အစား) အကြား ဆုံးဖြတ်ချက် ဖြစ်သည်။

### မိသားစု (ခ) — vector နှင့် ကိုယ်စားပြုမှု

#### Embedding

Embedding သည် discrete အရာဝတ္ထုများကို continuous space အတွင်းရှိ dense vector များသို့ mapping လုပ်သည့် သင်ယူထားသည့် အလွှာ ဖြစ်ပြီး ဆင်တူသည့် အရာဝတ္ထုများသည် အတူတကွ နီးကပ်စွာ ရောက်ရှိသည်။ ၎င်း၏ parameter အရေအတွက်သည် vocabulary × d_model ဖြစ်သည့်အတွက် primary axis သည် storage and VRAM ဖြစ်သည်။ ဥပမာ (ခ) တွင် tied matrix တစ်ခုသည် 1,000.00 MiB ဖြစ်ပြီး output layer ကို သီးခြား ထားလျှင် 2,000.00 MiB ဖြစ်သည်။ ထို့အပြင် embedding space တစ်ခုအတွင်း အကွာအဝေးသည် အခြား space တစ်ခုသို့ ကူးယူ အသုံးပြု၍ မရပါ၊ ထို့ကြောင့် similarity ကိန်းများကို model version နှင့် တွဲဖက် မှတ်တမ်းတင်ရမည်။

#### Cosine Similarity

Cosine Similarity သည် vector နှစ်ခု၏ normalized dot product ဖြစ်ပြီး ပမာဏ မဟုတ်ဘဲ ဦးတည်ချက်ကို နှိုင်းယှဉ်သည်၊ real-valued vector များအတွက် -1 မှ 1 အထိ တန်ဖိုး ရှိသည်။ နှိုင်းယှဉ်မှု တစ်ခုစီသည် d_model အလျား၏ multiply-add အလုပ်ပမာဏကို လိုအပ်သည့်အတွက် ၎င်း၏ primary axis သည် compute ဖြစ်သည်။ ဥပမာ (ခ) တွင် d_model 4096 ဖြစ်လျှင် vector တစ်စုံ နှိုင်းယှဉ်မှုတိုင်းသည် 4096 multiply-add ဖြစ်သည်၊ vector store သည် candidate သန်းချီကို စစ်လျှင် အလုပ်ပမာဏသည် သန်းချီဖြစ်လာသည်။ သို့သော် ဆင်တူမှု မြင့်မားခြင်းသည် embedding model နှင့် data distribution ကို အခြေခံ၍သာ အဓိပ္ပာယ် ရှိသည်၊ ထို့ကြောင့် cosine ကိန်းကို အချက်အလက်အရ တူညီမှု၏ သက်သေအဖြစ် မကောက်ချရ။ retrieval engineer သည် metric၊ model version နှင့် threshold သုံးခုကို တစ်စုတစ်စည်း မှတ်တမ်းတင်ရမည်။

#### Feature

Feature သည် အချက်အလက်၏ တိုင်းတာနိုင်သည့် ပိုင်ဆိုင်မှု တစ်ခုချင်း ဖြစ်သည်။ classical ML တွင် feature များကို လက်ဖြင့် တည်ဆောက်ရပြီး deep learning တွင် network သည် raw data မှ အလိုအလျောက် သင်ယူသည်။ ဤကွာခြားချက်သည် per-example FLOPs နှင့် အင်ဂျင်နီယာ အချိန်ကို ရွေ့လျားစေသည့်အတွက် primary axis သည် compute ဖြစ်သည်။ ဥပမာ (က) တွင် training cost သည် token အရေအတွက် နှင့် parameter အရေအတွက်ဖြင့် တွက်သည်၊ feature အရေအတွက် တိုးလျှင် step တိုင်း၏ FLOPs လည်း တိုးသည်။ ထို့ကြောင့် feature ရွေးချယ်မှုသည် budget အပေါ် တိုက်ရိုက် ကျသည်။

#### Latent Space

Latent Space သည် coordinate များက model အတွက် အသုံးဝင်သည့် အချက်များကို encode လုပ်ထားသည့် သင်ယူထားသည့် representation space ဖြစ်သည်။ ၎င်းသည် input ထက် dimension နည်းနိုင်သော်လည်း compression သည် representation တိုင်းအတွက် မဖြစ်မနေ မလိုအပ်ပါ။ latent dimension သည် representation တစ်ခု၏ byte ပမာဏကို ဆုံးဖြတ်သည့်အတွက် primary axis သည် storage and VRAM ဖြစ်သည်။ ဥပမာ (ခ) တွင် d_model 1024 မှ 8192 သို့ ရွေ့လျှင် matrix parameter သည် 131,072,000 မှ 1,048,576,000 သို့ ၈ ဆ တက်သည်။ ထို့ကြောင့် latent resolution သည် အရည်အသွေး နှင့် memory အကြား ချိန်ညှိရမည့် knob ဖြစ်သည်။

#### Tensor

Tensor သည် shape၊ data type နှင့် device placement ပါဝင်သည့် typed array ဖြစ်ပြီး framework များသည် input၊ parameter၊ activation နှင့် gradient များကို ၎င်းဖြင့် ကိုယ်စားပြုသည်။ ၎င်း၏ byte ပမာဏသည် shape × data type ဖြစ်သည့်အတွက် primary axis သည် storage and VRAM ဖြစ်သည်။ automatic-differentiation metadata သည် framework နှင့် operation အပေါ် မူတည်သည်၊ tensor တိုင်း၏ ပင်ကို ဂုဏ်သတ္တိ မဟုတ်ပါ။ ဥပမာ (ခ) တွင် vocabulary 128000၊ batch 32၊ fp32 logits tensor သည် sequence 1 တွင် 15.625 MiB ဖြစ်ပြီး sequence 8192 တွင် 125.000 GiB ဖြစ်သည်။ ထို့ကြောင့် dtype နှင့် shape ကို ကြိုတင် စစ်ဆေးခြင်းသည် OOM ကို တားဆီးသည့် အလေ့အကျင့် ဖြစ်သည်။

### မိသားစု (ဂ) — data တည်ငြိမ်မှုနှင့် ခြေရာခံမှု

#### Dataset Split

Dataset Split သည် နမူနာများကို fitting၊ development ဆုံးဖြတ်ချက်များ နှင့် နောက်ဆုံး evaluation အတွက် သီးခြား subset များအဖြစ် မှတ်တမ်းတင် ခွဲခြားထားသည့် အပိုင်းအခြား ဖြစ်သည်။ ၎င်း၏ ရည်ရွယ်ချက်မှာ စနစ် တစ်ခုကို ရွေးချယ်ရာတွင် အသုံးပြုသည့် အထောက်အထားက generalization သက်သေအဖြစ် ထပ်မံ မထမ်းဆောင်နိုင်ရန် ဖြစ်သည့်အတွက် primary axis သည် production consequence ဖြစ်သည်။ ဥပမာ lab_split_leak တွင် ကျပန်း row split သည် အနီးစပ်ဆုံး တူညီသည့် နမူနာများကို နယ်နိမိတ် ဖြတ်ကျော်စေပြီး contamination rate သည် 15.75% ဖြစ်သည်၊ entity group အလိုက် ခွဲခြားလျှင် 0.00% ဖြစ်သည်။ ထို့ကြောင့် split ယူနစ်သည် deployment ယူနစ် ဖြစ်ရမည်။

#### Data Leakage

Data Leakage သည် training အတွင်း သို့မဟုတ် feature တည်ဆောက်မှုအတွင်း တကယ့် prediction အချိန်တွင် ရရှိနိုင်မည် မဟုတ်သည့် အချက်အလက် ကို လည်းကောင်း၊ သီးခြား ဖယ်ထားသည့် evaluation နယ်နိမိတ်အတွင်း ပါဝင်သည့် အချက်အလက် ကို လည်းကောင်း မရည်ရွယ်ဘဲ အသုံးပြုခြင်း ဖြစ်သည်။ ၎င်းသည် အကောင်းဘက် လွန်ကဲသည့် metric များကို ဖန်တီးပြီး deployment တွင် ထို metric များ ပြိုလဲသည့်အတွက် primary axis သည် production consequence ဖြစ်သည်။ ဥပမာ lab_split_leak တွင် ယိုစိမ့်မှုရှိသည့် val record များသည် accuracy ကို +0.0354 မြှင့်ပြသည်၊ ဥပမာ (ဂ) တွင် 3.5% ယိုစိမ့်မှုသည် perplexity ကို 6.3747% ကောင်းသည်ဟု ထင်ရစေသည်။ ထို့ကြောင့် preprocessor များကို fit မလုပ်မီ data ကို split လုပ်ရမည်။

#### Data Deduplication

Data Deduplication သည် dataset တစ်ခုအတွင်း သို့မဟုတ် dataset များအကြား exact နှင့် near-duplicate နမူနာများကို ရှာဖွေပြီး ဖယ်ရှားခြင်း ဖြစ်သည်။ ၎င်းသည် လေ့ကျင့်ရမည့် token အရေအတွက်ကို လျှော့ချပြီး ingestion နှင့် training wall-clock ကို ရွေ့လျားစေသည့်အတွက် primary axis သည် ingestion and training wall-clock ဖြစ်သည်။ ဥပမာ (ဂ) တွင် 18.0% ဖယ်ရှားခြင်းသည် corpus ကို token 20,480,000,000 မှ 16,793,600,000 သို့ လျှော့ချသည်၊ သို့သော် တူညီသည့် token budget အောက်တွင် unique data အပေါ် pass အရေအတွက်သည် 1.2195 epoch သို့ တက်သည်။ ထို့ကြောင့် dedupe သည် wall-clock ကို ချွေတာသော်လည်း effective epoch တိုးလာခြင်းကို မှတ်တမ်းတင်ရမည်။

#### Data Provenance

Data Provenance သည် အချက်အလက်သည် မည်သည့်နေရာမှ မူလ ဖြစ်ပေါ်ခဲ့သည်၊ မည်သူ သို့မဟုတ် မည်သည့် အရာက ၎င်းကို အသွင်ပြောင်းခဲ့သည်၊ မည်သည့် version များကို အသုံးပြုခဲ့သည်ကို ခြေရာခံနိုင်သည့် အချက်အလက် ဖြစ်သည်။ ၎င်းသည် ရလဒ် ပြန်လည် ဖန်တီးနိုင်မှု၊ အသုံးပြုမှု ကန့်သတ်ချက် လိုက်နာမှု နှင့် ညစ်ညမ်းမှု စုံစမ်းနိုင်မှုကို ဖြစ်စေသည့်အတွက် primary axis သည် production consequence ဖြစ်သည်။ ဥပမာ (ဂ) ၏ dedupe စည်းမျဉ်းသည် မည်သည့် နမူနာကို မည်သည့် version က ဖယ်ရှားခဲ့သည်ကို ပြန်ပြနိုင်မှသာ ယုံကြည်စိတ်ချရသည်။ source URL တစ်ခုတည်းသည် provenance အပြည့်အစုံ မဟုတ်ပါ၊ collection အချိန်၊ လိုင်စင် အခြေအနေ၊ filtering နှင့် အသွင်ပြောင်းမှု အားလုံး ပါဝင်ရမည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။

### (က) Corpus → token အရေအတွက် → storage → လေ့ကျင့်မှု ကုန်ကျစရိတ်

ဖော်မြူလာ — `tokens = bytes ÷ bytes_per_token`၊ `storage = tokens × bytes_per_token_id`၊ `FLOPs = 6 × parameters × tokens × epochs`၊ `cost = FLOPs ÷ (peak × MFU × accelerators) ÷ 3600 × accelerators × price`။ ယူဆချက် — corpus 96 GiB UTF-8၊ bytes/token သည် english 4.0၊ burmese 1.2၊ code 3.5၊ token id သည် uint32 (4 byte) သို့မဟုတ် uint16 (2 byte)၊ model 7.0B parameter၊ accelerator 256 လုံး၊ peak 990 TFLOP/s၊ MFU 0.35၊ epoch 4၊ စျေးနှုန်း USD 2.50 per accelerator-hour။

```text
$ python3 guides/03_data_and_representations/scripts/ex_a_corpus_cost.py
reference corpus: 96.0 GiB of raw UTF-8 text (one pass)

modality     share    bytes (GiB)  bytes/token             tokens
english      60.0%         57.600          4.0        15461882265
burmese      25.0%         24.000          1.2        21474836480
code         15.0%         14.400          3.5         4417680647
total       100.0%         96.000         2.49        41354399392

storage for the same one pass:
  raw UTF-8 text              :     96.000 GiB
  token ids as uint32 (4 B)   :    154.057 GiB
  token ids as uint16 (2 B)   :     77.029 GiB   (only if vocabulary < 65536)

training model: 7.0B parameters, 42,000,000,000 FLOPs per token (forward + backward)
cluster: 256 accelerators x 990 TFLOP/s peak, MFU 0.35 -> 88.70 PFLOP/s
epochs=4   price=USD 2.50 per accelerator-hour

tokens seen over 4 epoch(s)  :       165417597571
training FLOPs                :         6.9475e+21
wall clock                    :              21.76 h
accelerator-hours             :            5569.62
cost                          :           13924.04 USD
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ corpus ၏ byte သည် token အရေအတွက်သို့ တိုက်ရိုက် မပြောင်းလဲခြင်း ဖြစ်သည်။ တူညီသည့် 96 GiB အတွက် burmese သည် token 21,474,836,480 ပေးပြီး english သည် token 15,461,882,265 ပေးသည်၊ ဆိုလိုသည်မှာ မြန်မာ စာသားအတွက် ကုန်ကျစရိတ် ခန့်မှန်းမှုသည် byte အပေါ် တွက်လျှင် လျော့နည်းသည်။

### (ခ) Vocabulary အရွယ်အစား → embedding နှင့် output layer memory

ဖော်မြူလာ — `matrix params = vocabulary × d_model`၊ `bytes = params × bytes_per_parameter`၊ `logits bytes = batch × sequence × vocabulary × 4`။ ယူဆချက် — fp16 (2 byte/parameter)၊ model 7.0B parameter၊ logits ကို fp32 score အဖြစ် ရေတွက်သည်။

```text
$ python3 guides/03_data_and_representations/scripts/ex_b_vocab_memory.py
assumptions: 7.0B reference model, fp16 (2 B/parameter)
             embedding and output matrices are vocabulary x d_model

d_model = 4096, vocabulary sweep:
vocab        matrix params     tied MiB   untied MiB share of model
32000            131072000       250.00       500.00        3.74%
64000            262144000       500.00      1000.00        7.49%
128000           524288000      1000.00      2000.00       14.98%
256000          1048576000      2000.00      4000.00       29.96%

vocabulary = 128000, d_model sweep (untied embedding + output layer):
d_model      matrix params   untied MiB share of model
1024             131072000       500.00        3.74%
2048             262144000      1000.00        7.49%
4096             524288000      2000.00       14.98%
8192            1048576000      4000.00       29.96%

logits tensor at vocabulary 128000, batch 32, fp32 (4 B per score):
  sequence 1              16384000 B =    15.625 MiB =    0.015 GiB
  sequence 8192       134217728000 B = 128000.000 MiB =  125.000 GiB

bytes of the two matrices at vocabulary 128000, d_model 4096:
  tied   :    1000.00 MiB
  untied :    2000.00 MiB  (+1000.00 MiB for the second copy)
```

ဤဇယားက vocabulary တစ်ခုတည်းဖြင့် ဆုံးဖြတ်ချက် နှစ်ခု ကွဲထွက်သည်ကို ပြသည် — memory (embedding နှင့် output matrix) နှင့် compute (logits projection အပေါ် ကျသည့် score tensor)။ sequence 8192 တွင် logits tensor တစ်ခုတည်းသည် 125.000 GiB ဖြစ်သည်၊ ဤအချက်က output အပိုင်းကို တစ်ပြိုင်နက် ရေတွက်သည့် အခြေအနေတွင် VRAM သည် အမာခံ ကန့်သတ်ချက် ဖြစ်လာသည်ကို ပြသည်။

### (ဂ) Deduplication နှင့် leakage ၏ effective epoch အပေါ် သက်ရောက်မှု

ဖော်မြူလာ — `effective epochs = token budget ÷ unique tokens`၊ `reported loss = (1 − leak) × clean loss + leak × leaked loss`၊ `perplexity = exp(loss)`။ ယူဆချက် — corpus သည် document 40,000,000၊ document တစ်ခုလျှင် token 512၊ exact copy 11.0% နှင့် near-duplicate 7.0% ဖယ်ရှားသည်၊ evaluation split သည် deduped document ၏ 1.0%၊ ယိုစိမ့်မှု 3.5%၊ clean loss 1.9320 nats နှင့် leaked document loss 0.0500 nats ကို ယူဆချက် အဖြစ် သတ်မှတ်သည် (တိုင်းတာမှု မဟုတ်ပါ)။

```text
$ python3 guides/03_data_and_representations/scripts/ex_c_dedup_epochs.py
raw corpus            : 40000000 documents, 20480000000 tokens
deduplication drops   : 11.0% exact + 7.0% near-duplicate = 18.0% of documents
unique corpus left    : 32800000 documents, 16793600000 tokens

token budget (one pass over the raw corpus) : 20480000000 tokens
passes over unique data                     : 1.2195 epochs
tokens re-read from duplicated material     : 3686399999

evaluation split      : 328000 documents, 167936000 tokens
leaked documents      : 11480  (3.50% of the split)
leaked training tokens: 5877760  (0.0287% of the budget)

assumed clean loss 1.9320 nats ; assumed leaked-document loss 0.0500 nats
reported loss over the whole split          : 1.86613 nats
understatement of loss                      : 0.06587 nats
perplexity, clean material                  : 6.9033
perplexity, split as reported               : 6.4632
apparent perplexity gain                    : 6.3747%
```

ဤတွက်ချက်မှုက အချက် နှစ်ခုကို ပြသည် — ပထမ၊ dedupe လုပ်ခြင်းသည် လေ့ကျင့်ရမည့် token ကို 18.0% လျှော့ချသော်လည်း တူညီသည့် budget အောက်တွင် unique data အပေါ် pass အရေအတွက်ကို 1.2195 epoch သို့ တင်သည်၊ ဆိုလိုသည်မှာ effective epoch ကို မှတ်တမ်းတင်ရမည်။ ဒုတိယ၊ 3.5% ယိုစိမ့်မှုသည် validation perplexity ကို 6.9033 မှ 6.4632 သို့ လျော့ပြပြီး 6.3747% ကောင်းသည်ဟု ထင်ရစေသည်၊ deployment တွင် ထို အကျိုးအမြတ် ပျောက်သည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Tokenizer သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Tokenization၊ Token၊ Vocabulary၊ Byte Pair Encoding (BPE)။ သက်သေပြသည့် မက်ထရစ် — bytes/token နှင့် sequence အရှည်။ ဥပမာ (က) အရ 96 GiB corpus ၏ ပျမ်းမျှသည် token တစ်လုံးလျှင် 2.49 byte ဖြစ်ပြီး burmese အပိုင်းသည် 1.2 byte ဖြစ်သည်၊ ထို့ကြောင့် tokenizer ရွေးချယ်မှုသည် ကုန်ကျစရိတ် ခန့်မှန်းမှုကို တိုက်ရိုက် ဆုံးဖြတ်သည်။

**၂။ Vocabulary အရွယ်အစား သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Vocabulary၊ Embedding၊ Latent Space၊ Tensor။ သက်သေပြသည့် မက်ထရစ် — embedding နှင့် output layer ၏ parameter အရေအတွက် နှင့် VRAM MiB။ ဥပမာ (ခ) အရ vocabulary 128000 သည် tied တွင် 1,000.00 MiB နှင့် untied တွင် 2,000.00 MiB ဖြစ်ပြီး 7.0B model ၏ 14.98% ဖြစ်သည်၊ ထို့ကြောင့် vocabulary သည် memory ဆုံးဖြတ်ချက် ဖြစ်သည်။

**၃။ Deduplication မူဝါဒ သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Data Deduplication၊ Data Provenance၊ Dataset Split။ သက်သေပြသည့် မက်ထရစ် — unique token အရေအတွက် နှင့် effective epoch အရေအတွက်။ ဥပမာ (ဂ) အရ 18.0% ဖယ်ရှားခြင်းသည် token ကို 16,793,600,000 သို့ လျှော့ချပြီး effective epoch ကို 1.2195 သို့ တင်သည်၊ ထို့ကြောင့် dedupe စည်းမျဉ်း နှင့် version ကို မှတ်တမ်းတင်ရမည်။

**၄။ Split ယူနစ် သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Dataset Split၊ Data Leakage၊ Data Deduplication။ သက်သေပြသည့် မက်ထရစ် — contamination rate နှင့် reported − clean ကွာခြားချက်။ ဥပမာ lab_split_leak အရ row split ၏ contamination rate သည် 15.75% ဖြစ်ပြီး entity group split တွင် 0.00% ဖြစ်သည်၊ ထို့ကြောင့် split ကို correlation ရှိသည့် row အလိုက် မခွဲရ။

**၅။ Pipeline သည် accelerator ကို ကျွေးနိုင်မှု သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Tokenization၊ Tensor၊ Token၊ Feature။ သက်သေပြသည့် မက်ထရစ် — encode မိုက်ခရိုစက္ကန့်/token၊ accelerator utilisation၊ wall clock နာရီ။ ဥပမာ lab_pipeline_budget အရ 20 မိုက်ခရိုစက္ကန့်/token တွင် utilisation သည် 66.29% ဖြစ်ပြီး wall clock သည် 111.11 h ဖြစ်သည်၊ 10 မိုက်ခရိုစက္ကန့် အောက်တွင် utilisation သည် 100.00% နှင့် wall clock သည် 73.65 h ဖြစ်သည်။

**၆။ Provenance၊ dtype နှင့် version သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Data Provenance၊ Tensor၊ Vocabulary၊ Byte Pair Encoding (BPE)၊ Embedding။ သက်သေပြသည့် မက်ထရစ် — artifact တိုင်း၏ lineage record ရာခိုင်နှုန်း နှင့် dtype အတွက် လိုအပ်သည့် byte။ ဥပမာ (ခ) အရ dtype တစ်ခု ပြောင်းလျှင် logits tensor ၏ byte သည် တိုက်ရိုက် ပြောင်းလဲသည်၊ ထို့ကြောင့် dtype၊ shape နှင့် source version ကို artifact နှင့်တကွ မှတ်တမ်းတင်ရမည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/03_data_and_representations/labs/lab_tokenizer.py`၊ `lab_split_leak.py` နှင့် `lab_pipeline_budget.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/03_data_and_representations.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/03_data_and_representations.json`။
- ဤနယ်ပယ်၏ lab suite — `guides/03_data_and_representations/labs/README.md`။

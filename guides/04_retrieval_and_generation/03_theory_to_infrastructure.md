# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၄ ၏ term ၁၄ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။
Retrieval & generation term တစ်ခုသည် စာတမ်းအတွင်း သီအိုရီ အဖြစ်သာ မကျန်ရပါ။ ၎င်းသည် index
memory (RAM/VRAM) ပမာဏ၊ embedding နှင့် search အတွက် compute၊ retrieval latency နှင့်
generation latency အချိုး၊ queries per second (QPS)၊ သို့မဟုတ် cost per thousand queries
အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းဂဏန်း တစ်ခုစီသည် ထုတ်လုပ်မှု အခြေအနေတွင်
တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/04_retrieval_and_generation/scripts/` အောက်ရှိ
Python script များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ ၎င်း script များသည် standard library သာ
အသုံးပြုပြီး deterministic ဖြစ်သည်။ vendor စျေးနှုန်း၊ hardware သို့မဟုတ် library version
အပေါ် မှီခိုသည့် တန်ဖိုးတိုင်းကို ယူဆချက် (assumption) အဖြစ် အမည်တပ်၍ ဖော်ပြထားသည်။ ဤစာတမ်းသည်
benchmark ရလဒ် များကို ဖော်ပြခြင်း မပြုပါ၊ ဖော်မြူလာ နှင့် ယူဆချက် မှ တွက်ချက်ထားသည့် တန်ဖိုးများ
ကိုသာ ဖော်ပြသည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**index memory (RAM/VRAM)** — vector များ၊ index structure (graph edge၊ centroid၊ posting list)
နှင့် metadata အားလုံး နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ ဤဝင်ရိုးသည် accelerator memory ပေါ်တွင်သာ
မဟုတ်ဘဲ host RAM ပေါ်တွင်လည်း တည်ရှိနိုင်သည်။ Index သည် memory အပေါ် မဆံ့လျှင် ဝန်ဆောင်နိုင်သည့်
copy အရေအတွက် လျော့သွားပြီး QPS ကျဆင်းသည်၊ ထို့ကြောင့် ၎င်းသည် capacity ဆုံးဖြတ်ချက် ဖြစ်သည်။

**compute for embedding and search** — အပိုင်း နှစ်ပိုင်း ပါဝင်သည်။ ပထမ အပိုင်းသည် query ကို
vector အဖြစ် ပြောင်းလဲသည့် encoder forward pass ဖြစ်ပြီး တောင်းဆိုမှု တိုင်းတွင် တစ်ကြိမ်
လုပ်ဆောင်ရသည်။ ဒုတိယ အပိုင်းသည် query vector ကို candidate vector များနှင့် နှိုင်းယှဉ်သည့်
distance တွက်ချက်မှု ဖြစ်ပြီး candidate အရေအတွက်နှင့် dimension အပေါ် အချိုးကျ ကြီးထွားသည်။
ဤနှစ်ပိုင်းကို ခွဲခြား မတိုင်းလျှင် latency ၏ လည်ပင်းကျဉ်းသည့် အပိုင်းကို မတွေ့ရနိုင်ပါ။

**retrieval latency vs generation latency** — retrieval latency သည် query တင်သည့် အချိန်မှ
အထောက်အထား ရွေးချယ်ပြီးသည့် အချိန်အထိ ကာလ ဖြစ်သည်။ generation latency သည် ထို အထောက်အထား
ရရှိပြီးနောက် token များ ထုတ်လုပ်သည့် ကာလ ဖြစ်သည်။ ပထမတစ်ခုသည် မီလီစက္ကန့် ဆယ်ဂဏန်း
အတွင်း ရှိပြီး ဒုတိယတစ်ခုသည် မီလီစက္ကန့် ထောင်ဂဏန်း ဖြစ်နိုင်သည်။ ဤအချိုးကို မတွက်လျှင်
retrieval ကို အလွန်အကျွံ optimize လုပ်မိခြင်း ဖြစ်နိုင်သည်။

**queries per second (QPS)** — တစ်စက္ကန့်လျှင် ဝန်ဆောင်နိုင်သည့် retrieval query အရေအတွက်
ဖြစ်သည်။ ၎င်းသည် worker တစ်ခုစီ၏ latency ၏ ပြောင်းပြန် တန်ဖိုးနှင့် concurrency အရေအတွက်
မြှောက်လဒ် ဖြစ်သည်။ QPS သည် retrieval server အရေအတွက်ကို ဆုံးဖြတ်သည့်အတွက် capacity planning
၏ အဓိက ကိန်း ဖြစ်သည်။

**cost per thousand queries** — တောင်းဆိုမှု တစ်ထောင်အတွက် ကုန်ကျသည့် ဒေါ်လာ တန်ဖိုး ဖြစ်သည်။
အဓိကအချက် နှစ်ခုက ၎င်းကို ဆုံးဖြတ်သည် — server တစ်နာရီ စျေးနှုန်း နှင့် ထို စျေးနှုန်းအောက်တွင်
ရရှိသည့် QPS။ Retrieval ကုန်ကျစရိတ်သည် generation ကုန်ကျစရိတ် အောက် အလွန်နည်းသော်လည်း
prompt token များဖြင့် ကုန်ကျစရိတ်ကို ပြန်လည် တိုးစေနိုင်သည်။ စျေးနှုန်းသည် vendor နှင့် region
အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် deployment တွင် မည်သည့် အရာ
ကျိုးပျက်မည်ကို ဆိုလိုသည်။ ဥပမာ probe parameter ကို မှတ်တမ်းမတင်ဘဲ recall@k ကျဆင်းခြင်းသည်
အသုံးပြုသူထံ အထောက်အထား မရောက်ခြင်း အဖြစ် ပေါ်လာသည်၊ ထို့ကြောင့် ၎င်းသည် ဆုံးဖြတ်ချက် တစ်ခု
ဖြစ်လာသည်။

## ၂။ Master table — term ၁၄ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Approximate Nearest Neighbor (ANN) | retrieval latency | candidate အားလုံးကို မတွက်ဘဲ latency နှင့် compute ကို ချွေတာသည် | candidates visited (250000 မှ 176) | probe ကို မှတ်တမ်းမတင်လျှင် recall@k ကျဆင်းမှုကို မတွေ့ရ |
| BM25 | compute for embedding and search | query embedding မလိုဘဲ lexical scoring ဖြင့် ရှာသည် | embedding call 0၊ posting list ရှည် | embedding service ကျလျှင်လည်း exact-term ရှာဖွေမှု ဆက်လုပ် |
| Chunking | index memory | chunk ကြီးလျှင် vector အရေအတွက် နည်း၍ index memory ချွေတာသည် | chunk အရေအတွက် (107143 မှ 13393) | chunk ကြီးလွန်းလျှင် prompt token ဖောင်းပွပြီး ကုန်ကျစရိတ် တိုး |
| Dense Retrieval | compute for embedding and search | candidate တိုင်းကို distance ဖြင့် အစဉ်သတ်မှတ်သည် | candidate အားလုံး × dim | embedding version ပြောင်းလျှင် index ပြန်တည်ဆောက်ရသည် |
| Grounding | cost per thousand queries | အထောက်အထား ပိုထည့်လျှင် prompt token နှင့် ကုန်ကျစရိတ် တိုးသည် | ကိုးကားသည့် အပိုင်း အရေအတွက် | citation စစ်ဆေးမှု မရှိလျှင် မထောက်ခံသည့် အဆိုများ ကျန်ရစ် |
| HNSW | index memory | graph edge ဖြင့် latency ကို ချွေတာပြီး edge memory ကို စားသည် | M (node တစ်ခုစီ၏ edge အရေအတွက်) | embedding version ပြောင်းလျှင် index ပြန်တည်ဆောက်ရမည် |
| Hybrid Retrieval | retrieval latency | ရှာဖွေမှု နှစ်လမ်းကို တစ်ပြိုင်နက် run ၍ rank ပေါင်းသည် | list တစ်ခုစီမှ candidate အရေအတွက် | လမ်းနှစ်ခုလုံး ကျလျှင် retrieval အပြည့်အဝ ရပ်တန့်သည် |
| Maximum Marginal Relevance (MMR) | compute for embedding and search | novelty တွက်ရန် candidate အတွင်း pairwise similarity လိုသည် | relevance-diversity အလေးချိန်၊ selected အရေအတွက် | diversity ကို လိုက်လျှင် relevance ထိပ်ဆုံး ကျဆင်းနိုင် |
| RAG (Retrieval-Augmented Generation) | cost per thousand queries | retrieval ကုန်ကျစရိတ်ကို generation ကုန်ကျစရိတ်အပေါ် ထပ်တိုးသည် | prompt token + output token | retrieval နှင့် grounding ကို ခွဲခြား မတိုင်းလျှင် အမှား ရှာမရ |
| Recall@K | production consequence | retrieval အဆင့် ပေးသည့် candidate အရည်အသွေးကို တိုင်းသည် | relevant item နှင့် top k ၏ ဆုံမှတ် အချိုး | recall@k မြင့်ခြင်းသည် grounded ဖြစ်ခြင်းကို အာမမခံ |
| Reciprocal Rank Fusion (RRF) | compute for embedding and search | raw score ကို normalize မလုပ်ဘဲ rank ချင်းပေါင်းသည် | fusion constant၊ list အရေအတွက် | input list အားလုံးတွင် မပါသည့် item ကို ပြန်မရနိုင် |
| Reranker | retrieval latency | ရှာပြီးသား candidate သေးငယ်တစ်ခုကို ဖြည့်စွက် compute ဖြင့် ပြန်စီသည် | candidate အရေအတွက် × pair scoring | context budget နှင့် မတွဲလျှင် ကောင်းသည့် အထောက်အထား လွတ်နိုင် |
| Semantic Search | compute for embedding and search | query တိုင်းအတွက် encoder forward pass လိုသည် | query embedding latency (5.0 ms) | embedding service သည် လည်ပင်းကျဉ်းသည့် အပိုင်း ဖြစ်လာသည် |
| Vector Database | index memory | vector နှင့် metadata ကို ရေရှည် သိမ်းဆည်းသည် | vector အရေအတွက် × dim × byte | index ကို memory ပေါ် မတင်နိုင်လျှင် QPS ကျဆင်းသည် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု လေးခုဖြင့် စုစည်းထားသည် — (က) ရှာဖွေမှု အခြေခံ၊ (ခ) index နှင့်
သိုလှောင်မှု၊ (ဂ) အစဉ်သတ်မှတ်မှုနှင့် အကဲဖြတ်မှု၊ (ဃ) စနစ် ပုံစံ။ ဤအုပ်စုခွဲမှုသည်
အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — ရှာဖွေမှု အခြေခံ (retrieval signals)

#### Semantic Search

Semantic Search သည် query နှင့် candidate များကို embedding space တစ်ခုအတွင်း ကိုယ်စားပြုပြီး
vector-similarity function တစ်ခုဖြင့် အစဉ်သတ်မှတ်သည်။ အခြေခံအဆောက်အအုံ အရ ၎င်း၏ အဓိက
ကုန်ကျစရိတ်သည် query embedding ဖြစ်သည်၊ ဥပမာ (ခ) တွင် query တစ်ခုလျှင် 5.0 ms ဖြစ်ပြီး
ရှာဖွေမှု တစ်ခုလုံး၏ 85.9 ရာခိုင်နှုန်း ဖြစ်သည်။ ဆိုလိုသည်မှာ distance တွက်ချက်မှုကို
မည်မျှ လျှော့လျှော့ embedding step သည် အောက်ခြေ ကန့်သတ်ချက် ဖြစ်နေသည်။ serving engineer
သည် encoder ကို cache လုပ်ခြင်း၊ batch လုပ်ခြင်းနှင့် ပိုသေးငယ်သည့် model ရွေးချယ်ခြင်းတို့ဖြင့်
ဤ 5.0 ms ကို ဆုံးဖြတ်ရမည်။

#### Dense Retrieval

Dense Retrieval သည် query နှင့် candidate အားလုံးကို vector အဖြစ် embed လုပ်ပြီး candidate
တိုင်းကို similarity function ဖြင့် အစဉ်သတ်မှတ်သည့် ပထမအဆင့် retrieval ဖြစ်သည်။ ၎င်းသည်
collection တစ်ခုလုံးကို ရှာဖွေသောကြောင့် exact scan ၏ compute သည် candidate အရေအတွက် × dim
အပေါ် အချိုးကျ ကြီးထားသည်၊ ဥပမာ (ခ) တွင် vector 250000 နှင့် dim 768 အတွက် 37.20 ms ဖြစ်သည်။
ဤတန်ဖိုးသည် ရှာဖွေမှု တစ်ခုစီတွင် ထပ်ခါတလဲလဲ ကုန်ကျသည့်အတွက် QPS ကို တိုက်ရိုက် ဆုံးဖြတ်သည်။
serving engineer သည် dense retrieval ကို ပထမအဆင့် အဖြစ် ထားရှိပြီး candidate လွှမ်းခြုံမှုကို
recall@k ဖြင့် စစ်ဆေးရမည်။

#### BM25

BM25 သည် query term ကိုက်ညီမှုမှ document အမှတ်ကို တွက်သည့် lexical ranking function ဖြစ်ပြီး
term ၏ ရှားပါးမှု၊ ထပ်ခါတလဲလဲ ပါဝင်မှုနှင့် document အရှည်တို့ကို ထည့်သွင်းစဉ်းစားသည်။ အခြေခံ
အဆောက်အအုံ အရ ၎င်း၏ အကျိုးအမြတ်မှာ query embedding လုံးဝ မလိုခြင်း ဖြစ်သည်၊ ဆိုလိုသည်မှာ
embedding service ကျဆင်းနေချိန်တွင်လည်း exact identifier ရှာဖွေမှု ဆက်လုပ်နိုင်သည်။ ဤနည်းလမ်းသည်
ပို့စ်တင်စာရင်း ဖတ်ခြင်းသာ လိုသောကြောင့် latency သည် အလွန်နည်းပြီး concurrency မြင့်စွာ
ဝန်ဆောင်နိုင်သည်။ serving engineer သည် BM25 ကို dense retrieval နှင့် တွဲဖက် run ၍
fallback အဖြစ် သတ်မှတ်ရမည်။

#### Hybrid Retrieval

Hybrid Retrieval သည် နည်းလမ်း အမျိုးမျိုးမှ signal များကို — အများအားဖြင့် lexical matching
နှင့် dense-vector similarity — ပေါင်းစပ်ခြင်း သို့မဟုတ် ပြန်စီခြင်း မပြုမီ ပေါင်းစပ်အသုံးပြုသည်။
ထုတ်လုပ်မှု အမြင်ဖြင့် ၎င်းသည် latency ကို နှစ်လမ်း (သို့မဟုတ် ထိုထက်ပို) ပေါင်းထည့်သော်လည်း
exact identifier နှင့် semantic paraphrase နှစ်မျိုးလုံးကို လွှမ်းခြုံစေသည်။ ရှာဖွေမှု တစ်လမ်း
တည်းဖြင့် recall@k သည် မြင့်သည်ဟု ယူဆလျှင် ဤအပိုဆောင်း latency သည် အလဟဿ ဖြစ်နိုင်သည်။
serving engineer သည် လမ်းတစ်ခုစီ၏ latency နှင့် ပေါင်းစပ်ပြီးနောက် recall@k ကို တစ်ပြိုင်နက်
တိုင်းတာရမည်။

### မိသားစု (ခ) — index နှင့် သိုလှောင်မှု (index and storage)

#### Vector Database

Vector Database သည် vector representation များအပေါ် nearest-neighbor query များကို ပံ့ပိုးသည့်
storage နှင့် indexing စနစ် ဖြစ်ပြီး metadata filtering၊ persistence နှင့် approximate index
များ ပါဝင်သည်။ ၎င်းသည် dense retrieval လုပ်ငန်းစဉ်၏ index အလွှာ ဖြစ်သည့်အတွက် index memory
ဝင်ရိုးကို ပိုင်ဆိုင်သည်၊ ဥပမာ (က) တွင် vector 250000၊ dim 768 အတွက် fp16 366.21 MiB၊
int8 183.11 MiB ဖြစ်သည်။ metadata 96 byte/chunk သည် precision မည်သို့ဖြစ်စေ မပြောင်းလဲဘဲ
0.02 GiB ကျန်နေသည်၊ ဤအချက်က precision လျှော့ချခြင်းသည် အလုံးစုံ index memory ကို အချိုးကျ
လျော့ချပေးသည်မဟုတ်သည်ကို ပြသည်။ serving engineer သည် vector byte နှင့် metadata byte ကို
ခွဲခြား တွက်ရမည်။

#### HNSW

HNSW သည် vector များကို အလွှာလိုက် proximity graph များတွင် စီစဉ်ပြီး ကြမ်းတမ်းသည့် အထက်လွှာ
များမှ အသေးစိတ် အောက်လွှာများဆီသို့ ရှာဖွေသည့် approximate-nearest-neighbor index ဖြစ်သည်။
ထို့ကြောင့် ၎င်း၏ အကျိုးအမြတ်သည် visited candidate အရေအတွက် ကျဆင်းခြင်း ဖြစ်ပြီး ကုန်ကျစရိတ်သည်
edge အရေအတွက်အလိုက် တိုးလာသည့် index memory ဖြစ်သည်။ ဤအချက်က HNSW သည် retrieval latency
ဝင်ရိုးနှင့် index memory ဝင်ရိုး နှစ်ခုလုံးကို တစ်ပြိုင်နက် ရွေ့လျားစေသည်ကို ပြသည်။
embedding version ပြောင်းလဲသည့်အခါ graph သည် အပြည့်အဝ ပြန်တည်ဆောက်ရသည့်အတွက် ၎င်းသည်
capacity event တစ်ခု ဖြစ်သည်။ serving engineer သည် construction parameter နှင့် query parameter
နှစ်မျိုးလုံးကို latency၊ memory နှင့် recall@k ရည်မှန်းချက်အပေါ် tune လုပ်ရမည်။

#### Approximate Nearest Neighbor (ANN)

Approximate Nearest Neighbor (ANN) သည် query ကို သိမ်းဆည်းထားသည့် vector တိုင်းနှင့်
အပြည့်အစုံ နှိုင်းယှဉ်ခြင်း မပြုဘဲ အနီးစပ်ဆုံး ဖြစ်နိုင်သည့် vector များကို ပြန်လည် ပေးအပ်သည့်
ရှာဖွေမှု နည်းလမ်း ဖြစ်သည်။ ဥပမာ (ခ) တွင် ရှာဖွေမှု တစ်ခုစီ၏ distance တွက်ချက်မှုသည်
250000 မှ 176 သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ collection ၏ 0.070 ရာခိုင်နှုန်းသာ ဖတ်သည်။
ဤ approximation သည် latency ကို ချွေတာသော်လည်း recall@k ကို 1 အောက်သို့ ကျဆင်းစေသည်၊
lab တွင် chunks 4096 အတွက် probe 2 ဖြင့် recall@10 သည် 0.8750 ဖြစ်သည်။ serving engineer
သည် latency ကို recall@k နှင့် တွဲဖက်ပြီးသာ တင်ပြရမည်၊ true neighbor တိုင်း တွေ့သည်ဟု
ယူဆရမည် မဟုတ်ပါ။

### မိသားစု (ဂ) — အစဉ်သတ်မှတ်မှုနှင့် အကဲဖြတ်မှု (ranking and measurement)

#### Reranker

Reranker သည် query နှင့် candidate တစ်ခုချင်းစီအကြား ပိုကြွယ်ဝသည့် နှိုင်းယှဉ်မှုကို အသုံးပြု၍
candidate set သေးငယ်တစ်ခုကို ပြန်စီပေးသည့် ဒုတိယအဆင့် model သို့မဟုတ် scoring function
ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အရ ၎င်း၏ ကုန်ကျစရိတ်သည် candidate အရေအတွက်နှင့် အချိုးကျသည်၊
ဆိုလိုသည်မှာ candidate 50 ကို cross-encoder ဖြင့် စစ်ခြင်းသည် distance တွက်ချက်မှု 50 ခု
ထပ်တိုးခြင်း ဖြစ်သည်။ ၎င်းသည် collection တစ်ခုလုံးကို ရှာဖွေခြင်း မပြုသောကြောင့် recall@k
ကို မြှင့်ပေးသည်မဟုတ်ဘဲ ရှာပြီးသား candidate များအတွင်း အစဉ်ကိုသာ မြှင့်ပေးသည်။ serving
engineer သည် reranking ကို context budget နှင့် တွဲဖက်၍ မည်သည့် အထောက်အထား prompt ထဲ
ရောက်မည်ကို ဆုံးဖြတ်ရမည်။

#### Reciprocal Rank Fusion (RRF)

Reciprocal Rank Fusion (RRF) သည် result list အများအပြားကို ပေါင်းစပ်သည့် rank-fusion နည်းလမ်း
ဖြစ်ပြီး list တစ်ခုချင်းစီတွင် item တစ်ခု၏ rank နှင့်အမျှ လျော့နည်းသွားသည့် ပါဝင်မှုများကို
ပေါင်းခြင်းဖြင့် ပေါင်းစပ်သည်။ ထို့ကြောင့် ၎င်း၏ compute ကုန်ကျစရိတ်သည် list အရေအတွက်နှင့်
candidate အရေအတွက်အပေါ်သာ မှီခိုပြီး score များ၏ စကေး အပေါ် မမှီခိုပါ။ ဤအချက်သည် RRF ကို
BM25 နှင့် dense retrieval ၏ score အလွန်ကွာခြားသည့် အခြေအနေတွင် အသုံးဝင်စေသည်၊ အကြောင်းမှာ
နှစ်ခုလုံးကို normalize လုပ်စရာ မလိုပါ။ serving engineer သည် fusion လုပ်ပြီးနောက် ရလဒ်ကို
retriever တစ်ခုချင်းစီနှင့် နှိုင်းယှဉ် အကဲဖြတ်ရမည်။

#### Maximum Marginal Relevance (MMR)

Maximum Marginal Relevance (MMR) သည် query နှင့် သက်ဆိုင်မှုကို ရွေးချယ်ပြီးသား item များနှင့်
နှိုင်းယှဉ်သည့် အသစ်အဆန်းမှု (novelty) နှင့် မျှတစေသည့် ရွေးချယ်မှု စည်းမျဉ်း ဖြစ်သည်။
၎င်း၏ compute ကုန်ကျစရိတ်သည် candidate အတွင်း pairwise similarity တွက်ချက်မှု ဖြစ်ပြီး
selected အရေအတွက်နှင့် candidate အရေအတွက် မြှောက်လဒ် အပေါ် မှီခိုသည်။ ဤအပိုဆောင်း
တွက်ချက်မှုသည် prompt token ကို မတိုးစေဘဲ ကန့်သတ်ထားသည့် context ဘက်ဂျက်အတွင်း ကွဲပြားသည့်
အထောက်အထား ပိုပါဝင်စေသည်။ serving engineer သည် relevance-diversity အလေးချိန်ကို မှတ်တမ်းတင်၍
အဖြေ အရည်အသွေးနှင့် source လွှမ်းခြုံမှု နှစ်မျိုးလုံးကို အကဲဖြတ်ရမည်။

#### Recall@K

Recall@K သည် query တစ်ခုအတွက် `|relevant items intersecting the top k| / |relevant items|`
ဖြစ်ပြီး dataset အမှတ်တစ်ခုသည် ထို per-query တန်ဖိုးများကို သတ်မှတ်ထားသည့် စည်းမျဉ်း တစ်ခုအောက်
တွင် စုစည်းပေးသည်။ ဤတန်ဖိုးသည် retrieval အဆင့်တစ်ခုက downstream reranking သို့မဟုတ်
generation အတွက် သက်ဆိုင်သည့် candidate များ လုံလောက်စွာ ပေးနိုင်ခြင်း ရှိ/မရှိကို ဖော်ပြသည်။
အခြေခံအဆောက်အအုံ အရ ၎င်းသည် ပိုက်လိုင်း၏ ပထမ အဆင့်ကို တိုင်းတာသည့် ကိန်း ဖြစ်ပြီး latency
သို့မဟုတ် ကုန်ကျစရိတ်ကို တိုက်ရိုက် မဖော်ပြပါ။ lab တွင် chunks 1024 မှ 8192 သို့ တိုးလျှင်
probe 2 ဖြင့် recall@k သည် 0.9750 မှ 0.7625 သို့ ကျဆင်းသည်၊ ဆိုလိုသည်မှာ collection ကြီးလာသည့်အခါ
probe ကို ပြန်တွက်ရမည် ဖြစ်သည်။ serving engineer သည် relevance judgment၊ k၊ aggregation
နည်းလမ်းနှင့် သက်ဆိုင်သည့် item မရှိသည့် query များအတွက် မူဝါဒ တစ်ခုကို သတ်မှတ်ရမည်။

### မိသားစု (ဃ) — စနစ် ပုံစံ (system patterns)

#### Chunking

Chunking သည် index မပြုမီ source material ကို ရှာဖွေနိုင်သည့် ယူနစ်များအဖြစ် ခွဲခြားခြင်း
ဖြစ်သည်။ chunk နယ်နိမိတ်၊ overlap၊ metadata နှင့် document တည်ဆောက်ပုံတို့က retrieval သည်
prompt ကို အလွန်အကျွံ ဖြည့်တင်းခြင်း မရှိဘဲ လုံလောက်သည့် context ပေးနိုင်ခြင်း ရှိ/မရှိကို
ဆုံးဖြတ်သည်။ ဥပမာ (က) တွင် token 12000000 ရှိသည့် source အတွက် chunk အရွယ်အစား 128 မှ 1024
သို့ တိုးလျှင် chunk အရေအတွက်သည် 107143 မှ 13393 သို့ ကျဆင်းပြီး index သည် 156.95 MiB မှ
19.62 MiB သို့ ကျဆင်းသည်။ သို့သော် chunk ကြီးလွန်းလျှင် retrieved token တိုင်းတွင် အသုံးမဝင်သည့်
စာသား ပါလာသဖြင့် prompt token နှင့် ကုန်ကျစရိတ် တိုးသည်။ serving engineer သည် heading နှင့်
code block များကို မပျက်စီးစေဘဲ ထိန်းသိမ်း၍ အရွယ်အစားကို tune ရမည်။

#### RAG (Retrieval-Augmented Generation)

RAG သည် တောင်းဆိုချက်တစ်ခုနှင့် သက်ဆိုင်သည့် အထောက်အထားကို ရှာဖွေပြီး ရွေးချယ်ထားသည့်
အကြောင်းအရာကို generative model ထံ ၎င်းက ဖြေကြားခြင်း သို့မဟုတ် လုပ်ဆောင်ခြင်း မပြုမီ
ပေးအပ်သည့် စနစ် ပုံစံ ဖြစ်သည်။ ဤနေရာတွင် ကုန်ကျစရိတ် နှစ်ပိုင်း ပေါင်းလာသည် — retrieval ၏
QPS ကုန်ကျစရိတ် နှင့် prompt token ကြီးထွားမှုကြောင့် generation ၏ input ကုန်ကျစရိတ်။
ဥပမာ (ဂ) တွင် chunk 400 token အတွက် k ကို 2 မှ 10 သို့ တိုးလျှင် prompt တန်ဖိုးသည်
1260 မှ 4460 token သို့ တိုးပြီး input ကုန်ကျစရိတ်သည် ကုန်ကျစရိတ် per 1000 queries တွင်
2.5200 USD မှ 8.9200 USD သို့ တိုးသည်။ ထို့ကြောင့် RAG ၏ ကုန်ကျစရိတ် ဆုံးဖြတ်ချက်သည်
retrieval latency မဟုတ်ဘဲ k ဖြစ်လာသည်။ serving engineer သည် retrieval နှင့် grounding ကို
ခွဲခြား၍ အကဲဖြတ်ရမည်။

#### Grounding

Grounding သည် generate လုပ်ထားသည့် အဖြေ သို့မဟုတ် လုပ်ဆောင်မှုကို စနစ်က ဖော်ထုတ်၍
စစ်ဆေးနိုင်သည့် အထောက်အထား၊ state သို့မဟုတ် observation များနှင့် ချိတ်ဆက်ပေးခြင်း
ဖြစ်သည်။ ဤချိတ်ဆက်မှုသည် အထောက်အထား မရှိသည့် အဆိုများကို ဖော်ထုတ်ရ ပိုလွယ်ကူစေသော်လည်း
ကိုးကားရန် လိုအပ်သည့် အပိုင်းများက prompt token ကို တိုးစေသည်။ ဆိုလိုသည်မှာ ground ဖြစ်မှုကို
တိုးခြင်းသည် ကုန်ကျစရိတ် နှင့် လဲလှယ်ခြင်း ဖြစ်သည်။ prompt ထဲသို့ document ထည့်ခြင်းသည်
grounding အတွက် အခွင့်အလမ်း တစ်ခု ဖန်တီးပေးသော်လည်း model က ၎င်းတို့ကို မှန်ကန်စွာ
အသုံးပြုမည်ဟု အာမမခံပါ။ serving engineer သည် policy အပိုင်း ကိုးကားမှုကို တောင်းဆိုပြီး
မထောက်ခံသည့် အဆိုများကို ပယ်ချရမည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့်
ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။

### (က) Index memory — stated corpus တစ်ခုအတွက် fp32၊ fp16၊ int8 နှင့် dimension၊ chunk size ၏ သက်ရောက်မှု

ယူဆချက် — chunk 250000 ခု၊ dim 768၊ metadata 96 byte/chunk (id 8 byte + source offset နှင့်
label 88 byte)။ ဖော်မြူလာ — `vector_bytes = chunks × dim × bytes_per_element`၊
`index_bytes = vector_bytes + chunks × metadata_bytes`။ fp32 = 4 byte/element၊ fp16 = 2 byte၊
int8 = 1 byte။ ထို့အပြင် source token 12000000 အတွက် chunk size ၏ သက်ရောက်မှုကို
overlap = chunk ၏ 12.5 ရာခိုင်နှုန်း ဖြင့် တွက်သည်။

```text
$ python3 guides/04_retrieval_and_generation/scripts/ex_a_index_memory.py
reference corpus: chunks=250000  dim=768  metadata=96 B/chunk (assumption)

precision   B/elem    vector MiB    vector GiB     index GiB
fp32             4        732.42        0.7153        0.7376
fp16             2        366.21        0.3576        0.3800
int8             1        183.11        0.1788        0.2012

dimension sweep at fp16 (chunks=250000):
       dim    vector MiB    vector GiB     index GiB
       256        122.07        0.1192        0.1416
       384        183.11        0.1788        0.2012
       768        366.21        0.3576        0.3800
      1536        732.42        0.7153        0.7376

chunk size effect (source=12000000 tokens, overlap=12.5% of chunk, fp16, dim=768):
  chunk  overlap   stride     chunks   index MiB vectors/1k tok
    128       16      112     107143      156.95          8.93
    256       32      224      53572       78.47          4.46
    512       64      448      26786       39.24          2.23
   1024      128      896      13393       19.62          1.12

note: metadata is 96 B/chunk and does not change with precision; it is 0.02 GiB.
```

ဤတန်ဖိုးများသည် ဖော်မြူလာ အရသာ တွက်ချက်ထားခြင်း ဖြစ်ပြီး vector database ကိုယ်တိုင်၏
index structure (graph edge၊ centroid) နှင့် runtime buffer များ မပါဝင်ပါ၊ ထို့ကြောင့်
`တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

### (ခ) Retrieval latency နှင့် queries per second — stated index တစ်ခုအတွက် k အလိုက်၊ ထို retrieval မှ feed လုပ်သည့် generation step နှင့် နှိုင်းယှဉ်ခြင်း

ယူဆချက် — vector 250000 ခု၊ dim 768။ distance တစ်ခုလျှင် 2 × dim FLOPs၊ worker တစ်ခုစီ၏
scalar distance throughput 12.0 GFLOP/s။ ANN သည် candidate 96 + 8k ခုကို လည်ပတ်ပြီး traversal
အတွက် 0.60 ms ထပ်ကျသည်။ exact scan သည် candidate 250000 ခုလုံး လည်ပတ်သည်။ query embedding
5.0 ms၊ metadata filter နှင့် dedup 0.20 ms။ server တစ်ခုလျှင် worker 4 ခု၊ server စျေးနှုန်း
0.90 USD/hour။ generation step သည် first token 420 ms နှင့် output token 220 ခုကို 11 ms စီ
ထုတ်သည် (စုစုပေါင်း 2840 ms)။ ဤနှုန်းတန်ဖိုး အားလုံးသည် ယူဆချက် ဖြစ်သည်၊ တိုင်းတာမှု မဟုတ်ပါ။

```text
$ python3 guides/04_retrieval_and_generation/scripts/ex_b_latency_qps.py
index: 250000 vectors, dim=768 ; candidates visited by ANN = 96 + 8*k (assumption)
generation step it feeds: 420 ms to first token + 220 output tokens x 11 ms = 2840 ms

  k     ANN ms   ANN QPS    share %  ANN USD/1k q        ANN USD/1M q
  2     5.8143     688.0       0.20      0.000363                0.36
  5     5.8174     687.6       0.20      0.000364                0.36
 10     5.8225     687.0       0.20      0.000364                0.36

exact scan for reference: 37.2000 ms, 107.5 QPS, 1.29% of end to end, 0.002325 USD/1k queries

embedding share of the ANN query: 5.0 ms of 5.8225 ms = 85.9%
candidates visited: k=10 -> 176 of 250000 = 0.070% of the collection
workers needed for 50 ANN queries/s at k=10: 0.3
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ retrieval latency သည် end-to-end အချိန်၏ 0.20 ရာခိုင်နှုန်းသာ
ဖြစ်ခြင်း ဖြစ်သည်။ ထို့ကြောင့် retrieval ၏ အခန်းကဏ္ဍသည် latency မဟုတ်ဘဲ QPS နှင့်
ကုန်ကျစရိတ် ဖြစ်လာသည်၊ ဤနေရာတွင် exact scan သည် ANN ထက် 6.4 ဆ ပိုကုန်ကျသည်။

### (ဂ) Prompt token နှင့် retrieved chunk တစ်ခုစီ ထပ်တိုးသည့် ကုန်ကျစရိတ် — k = 2၊ 5၊ 10

ယူဆချက် — chunk အရွယ်အစား 400 token၊ system prompt 400 token၊ မေးခွန်း 60 token၊ အဖြေ 300
token။ စျေးနှုန်း — input 2.00 USD per 1M tokens၊ output 8.00 USD per 1M tokens။

```text
$ python3 guides/04_retrieval_and_generation/scripts/ex_c_prompt_cost.py
assumptions: chunk=400 tokens, system=400, question=60, answer=300 tokens
prices: input 2.00 USD per 1M tokens, output 8.00 USD per 1M tokens (assumption)

  k   retrieved  prompt tok  USD/1k input   USD/1k total     added USD/1k
  2         800        1260        2.5200         4.9200           1.6000
  5        2000        2460        4.9200         7.3200           4.0000
 10        4000        4460        8.9200        11.3200           8.0000

cost of one retrieved chunk of 400 tokens = 0.00080000 USD per query = 0.8000 USD per 1000 queries
retrieved context as a share of the prompt at k=5: 81.3%
prompt growth k=2 -> k=10: 1260 -> 4460 tokens (3.54x)

chunk size effect at k=5:
  chunk   retrieved  prompt tok    USD/1k input
    200        1000        1460          2.9200
    400        2000        2460          4.9200
    800        4000        4460          8.9200
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ retrieved chunk တစ်ခုသည် prompt တွင် 400 token ဖြည့်ခြင်းဖြင့်
query တစ်ထောင်လျှင် 0.8000 USD ကို တိုက်ရိုက် ထပ်တိုးစေခြင်း ဖြစ်သည်။ k ကို 2 မှ 5 သို့
တိုးခြင်းသည် retrieval latency ကို မပြောင်းလဲစေဘဲ prompt ကုန်ကျစရိတ်ကို 1.6 ဆ ဖြစ်စေသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Index precision နှင့် memory budget သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Vector
Database၊ Dense Retrieval၊ Semantic Search၊ HNSW။ သက်သေပြသည့် မက်ထရစ် — dtype အလိုက် index
bytes နှင့် vector အရေအတွက်။ ဥပမာ (က) က int8 သည် fp16 ၏ တစ်ဝက်ဖြစ်သော်လည်း metadata သည်
0.02 GiB ကျန်နေသည်ကို ပြသည်၊ ထို့ကြောင့် memory budget ကို vector၊ structure နှင့် metadata
သုံးပိုင်း ခွဲ၍ တွက်ရမည်။

**၂။ ANN parameter နှင့် recall@k ရည်မှန်းချက် ချိန်ညှိခြင်း** — မှီခိုသည့် term များ —
Approximate Nearest Neighbor (ANN)၊ HNSW၊ Recall@K၊ Vector Database။ သက်သေပြသည့် မက်ထရစ် —
candidate visited အရေအတွက်၊ work ratio နှင့် recall@k။ lab_vector_index တွင် chunks 8192 နှင့်
probe 2 ဖြင့် distance scan သည် 544 ခုသာ ဖြစ်ပြီး (15.06x ချွေတာသည်) recall@10 သည် 0.7625
ဖြစ်သည်၊ ဆိုလိုသည်မှာ ချွေတာမှုနှင့် recall ကို တစ်ပြိုင်နက် တင်ပြရမည် ဖြစ်သည်။

**၃။ Chunking မဟာဗျူဟာ သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Chunking၊ Reranker၊
Grounding၊ Vector Database။ သက်သေပြသည့် မက်ထရစ် — chunk အရေအတွက်၊ စာကြောင်း ဖြတ်ခံရသည့်
နယ်နိမိတ် အရေအတွက်နှင့် index MiB။ lab_chunking တွင် chunk 256 မှ 512 သို့ တိုးလျှင် index
ကုန်ကျစရိတ် ကျဆင်းသော်လည်း နယ်နိမိတ် အားလုံးနီးပါးသည် စာကြောင်းကို ဖြတ်နေဆဲ ဖြစ်သည်။

**၄။ Retrieval လမ်းကြောင်း တစ်ခု သို့မဟုတ် နှစ်ခု သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ —
BM25၊ Dense Retrieval၊ Hybrid Retrieval၊ Reciprocal Rank Fusion (RRF)၊ Reranker။ သက်သေပြသည့်
မက်ထရစ် — retriever တစ်ခုချင်းစီ၏ recall@k၊ ပေါင်းစပ်ပြီးနောက် recall@k နှင့် latency။
ဥပမာ (ခ) အရ distance တွက်ချက်မှု တစ်ခုလျှင် 0.0013 ms သာ ကုန်ကျသည့်အတွက် hybrid လမ်းတစ်ခု
ထပ်တိုးခြင်း၏ latency ကုန်ကျစရိတ်ကို တိုင်းတာ၍ ဆုံးဖြတ်ရမည်။

**၅။ Prompt budget နှင့် k သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — RAG၊ Chunking၊ Maximum
Marginal Relevance (MMR)၊ Grounding။ သက်သေပြသည့် မက်ထရစ် — prompt token၊ history အတွက်
ကျန်နေရာ (headroom) သို့မဟုတ် လွန်ကျွံမှု (overflow) နှင့် cost per thousand queries။
lab_prompt_budget တွင် window 9000၊ chunk 800 ဖြင့် k = 10 တွင် history နေရာ 1508 token လွန်ကျွံသည်၊
ဆိုလိုသည်မှာ k ကို memory အခြေအနေဖြင့် ကန့်သတ်ရမည် ဖြစ်သည်။

**၆။ Retrieval latency နှင့် generation latency SLO ခွဲခြား သတ်မှတ်ခြင်း** — မှီခိုသည့်
term များ — Semantic Search၊ Approximate Nearest Neighbor (ANN)၊ Reranker၊ Recall@K၊ RAG။
သက်သေပြသည့် မက်ထရစ် — retrieval ms၊ QPS နှင့် end-to-end အချိန်အတွင်း retrieval ရာခိုင်နှုန်း။
ဥပမာ (ခ) အရ ANN query တစ်ခုသည် 5.8225 ms ဖြစ်ပြီး generation သည် 2840 ms ဖြစ်သည်၊ ထို့ကြောင့်
SLO သည် generation အပေါ် ဦးစားပေးရမည် ဖြစ်သည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/04_retrieval_and_generation/labs/lab_vector_index.py`၊
`lab_chunking.py`၊ `lab_prompt_budget.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ဤစာတမ်းရှိ
ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary)
  — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/04_retrieval_and_generation.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/04_retrieval_and_generation.json`။

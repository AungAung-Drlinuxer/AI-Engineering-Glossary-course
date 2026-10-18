# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၉ ၏ term ၁၈ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။ ဤနယ်ပယ်သည် သင်တန်းပေးပြီးသား model တစ်ခုကို တကယ် အလုပ်လုပ်စေသည့် အလွှာ ဖြစ်သည် — request လက်ခံခြင်း၊ schedule လုပ်ခြင်း၊ accelerator ပေါ်တွင် လည်ပတ်စေခြင်း၊ ရလဒ် ပြန်ပေးခြင်း။ term တစ်ခုစီသည် accelerator memory၊ compute အသုံးပြုမှု အချိုး၊ latency၊ throughput၊ goodput သို့မဟုတ် serving cost အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းတစ်ခုစီသည် ထုတ်လုပ်မှု အခြေအနေတွင် တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/09_infrastructure_and_serving/scripts/` အောက်ရှိ Python script များမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။ bandwidth၊ memory bandwidth အသုံးပြုမှု အချိုး၊ GPU-hour စျေးနှုန်းနှင့် KV-cache geometry အားလုံးကို assumption အဖြစ် ဖော်ပြထားသည်၊ အကြောင်းမှာ ၎င်းတို့သည် GPU model၊ vendor၊ region နှင့် library version အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။ ဤစာတမ်းရှိ တန်ဖိုးများသည် benchmark တိုင်းတာမှု မဟုတ်ဘဲ ဖော်မြူလာနှင့် ယူဆချက်မှ တွက်ချက်ထားသည့် roofline ခန့်မှန်းချက် ဖြစ်သည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**accelerator memory (VRAM)** — accelerator တစ်လုံး၏ memory ပေါ်တွင် တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ weight၊ KV cache၊ activation နှင့် runtime buffer အားလုံး ပါဝင်သည်။ VRAM ပြည့်လျှင် serving သည် throughput ကျခြင်းဖြင့် မဟုတ်ဘဲ အလုပ်လုပ်နိုင်ခြင်း ရပ်တန့်ခြင်းဖြင့် ကျိုးပျက်သည်၊ ထို့ကြောင့် ဤဝင်ရိုးသည် အမာခံ ကန့်သတ်ချက် ဖြစ်သည်။

**compute utilisation** — တောင်းဆိုမှု တစ်ခုအတွက် လိုအပ်သည့် floating-point operation ပမာဏနှင့် accelerator ၏ peak စွမ်းရည်ကို နှိုင်းယှဉ်သည့် အချိုး ဖြစ်သည်။ prefill သည် compute အပေါ် ဖိအား သက်ရောက်ပြီး decode သည် memory bandwidth အပေါ် ဖိအား သက်ရောက်သည်၊ utilisation နည်းခြင်းသည် hardware ရှိပြီး အလုပ်မဖြစ်ခြင်း ဖြစ်သည်၊ ဆိုလိုသည်မှာ ပိုသည့် စရိတ် ဖြစ်သည်။

**latency (TTFT နှင့် inter-token)** — အစိတ်အပိုင်း နှစ်ခုဖြင့် တိုင်းတာသည်။ **TTFT (Time to First Token)** သည် request တင်သည့် အချိန်မှ ပထမဆုံး output token ရရှိသည့် အချိန်အထိ ကာလ ဖြစ်သည်၊ ၎င်းတွင် queueing၊ prefill နှင့် network ပါဝင်သည်။ **inter-token latency** သည် output token တစ်လုံးနှင့် နောက် တစ်လုံးအကြား ကာလ ဖြစ်ပြီး decode အရှိန်ကို ဖော်ပြသည်။ ဤနှစ်တန်ဖိုးသည် မတူညီသည့် ကျိုးပျက်မှု နှစ်မျိုးကို ဖော်ထုတ်သည်။

**throughput နှင့် goodput** — throughput သည် အချိန် တစ်ယူနစ်အတွင်း ထုတ်လုပ်သည့် output token အရေအတွက် ဖြစ်သည်။ goodput သည် သတ်မှတ်ထားသည့် ဝန်ဆောင်မှု ကန့်သတ်ချက်များ — ဥပမာ TTFT နှင့် per-token latency ပန်းတိုင် နှစ်ခုလုံး — ပြည့်မီသည့် request များ၏ နှုန်း ဖြစ်သည်။ raw throughput မြင့်တက်နေစဉ် goodput ကျဆင်းနိုင်သည်၊ ထို့ကြောင့် goodput သည် capacity ဆုံးဖြတ်ချက်၏ တကယ့် အခြေခံ ဖြစ်သည်။

**cost per million tokens** — accelerator အချိန်၏ ကုန်ကျစရိတ်ကို ထုတ်လုပ်သည့် token အရေအတွက်ဖြင့် စားခြင်း ဖြစ်သည်။ အဓိကအချက် နှစ်ခုက ၎င်းကို ဆုံးဖြတ်သည် — accelerator တစ်နာရီ စျေးနှုန်း နှင့် ထိုစျေးနှုန်းအောက်တွင် ရရှိသည့် tokens/s။ စျေးနှုန်းသည် vendor နှင့် region အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် deployment တွင် မည်သည့် အရာ ကျိုးပျက်မည်ကို ဆိုလိုသည်။ ဥပမာ KV-cache memory ကို မစီမံလျှင် batch အရေအတွက် ကျဆင်းခြင်းနှင့် queue ကြီးထွားခြင်းသည် ထုတ်လုပ်မှု အကျိုးဆက် ဖြစ်သည်။

## ၂။ Master table — term ၁၈ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Autoscaling | cost per million tokens | replica အရေအတွက်ကို ချိန်ညှင်း၍ over- နှင့် under-provisioning ကို ဖြေရှင်း | required replicas at target utilisation (4) | queue ကြီးထွားလျှင် စျေးနှုန်း မဟုတ်ဘဲ latency ပျက်သည် |
| Chunked Prefill | latency (inter-token) | ရှည်သည့် prompt ၏ prefill ကို အပိုင်းခွဲ၍ decode နှင့် ရောစပ်သည် | decode stall အကြိမ် | tail latency ကို ထိန်းသည်၊ schedule ရှုပ်ထွေးမှု တိုးသည် |
| Continuous Batching | throughput | iteration နယ်နိမိတ်တွင် request ထည့်/ဖယ်၍ accelerator ကို အလုပ်ဖြစ်နေစေသည် | tokens/s | တိုတောင်းသည့် request သည် အရှည်ဆုံး request အတွက် မစောင့်ရပါ |
| Decode Phase | latency (inter-token) | token တစ်လုံးချင်း ထုတ်၍ memory bandwidth အပေါ် မှီခိုသည် | ITL နှင့် step time | decode ကို prefill နှင့် ခွဲ၍ တိုင်းတာရမည် |
| Disaggregated Serving | cost per million tokens | prefill pool နှင့် decode pool ကို သီးခြား provision လုပ်သည် | pool တစ်ခုချင်း၏ token throughput | state transfer ကုန်ကျစရိတ်ကို ထည့်တွက်ရမည် |
| Dynamic Batching | throughput | queue ရှိ request များမှ batch ဖွဲ့၍ utilisation မြှင့်သည် | batch size နှင့် queue delay | traffic ကျဲလျှင် latency ပိုဆိုးနိုင်သည် |
| Expert Parallelism | accelerator memory | expert များကို device များအကြား ဖြန့်၍ total parameter ကို ထမ်းသည် | device တစ်လုံးလျှင် total params | routing communication သည် latency ဖြစ်လာသည် |
| FlashAttention | accelerator memory | attention matrix အပြည့်ကို တည်ဆောက်ခြင်း မပြုဘဲ tile ခွဲသည် | peak attention memory | long context တွင် အကျိုးအမြတ် သိသာသည် |
| Goodput | throughput နှင့် goodput | SLO ပြည့်မီသည့် request ကိုသာ ရေတွက်သည် | SLO ပြည့်မီသည့် req/s | raw throughput မြင့်သော်လည်း goodput ကျနိုင်သည် |
| Inter-Token Latency (ITL) | latency | token နှစ်ခုအကြား ကွာဟမှုကို တိုင်းတာသည် | ပထမနောက်ပိုင်း token တစ်လုံးအတွက် t_i - t_(i-1) | decode stall နှင့် streaming jitter ကို ဖော်ထုတ်သည် |
| Model Serving | production consequence | version၊ schedule၊ cancel နှင့် response boundary ကို စီမံသည် | ပြန်ပေးသည့် request rate | မလုပ်ဆောင်လျှင် model ကောင်းသော်လည်း product ကို မယုံရ |
| Paged KV Cache | accelerator memory | block အခြေခံ allocation ဖြင့် fragmentation ကို လျှော့သည် | အသုံးဝင်သည့် KV blocks နှင့် batch | batch အရေအတွက် တိုးလာသည် |
| Pipeline Parallelism | accelerator memory | layer အုပ်စုများကို device များအကြား ခွဲသည် | stage အရေအတွက်နှင့် bubble ရာခိုင်နှုန်း | device တစ်လုံး memory ထက် ကြီးသည့် model ကို တင်နိုင်သည် |
| Prefill | latency (TTFT) | prompt token အားလုံးကို တစ်ပြိုင်နက် တွက်သည် | prompt tokens နှင့် TTFT | စတင်ချိန် latency ကို ဆုံးဖြတ်သည် |
| Prefix Caching | cost per million tokens | တူညီသည့် prefix ၏ prefill ကို ကျော်လွှားသည် | cache hit rate | ပြန်သုံးမှု မကိုက်ညီလျှင် အကျိုးမရှိပါ |
| Tensor Parallelism | compute utilisation | layer အတွင်း tensor operation ကို device များအကြား ခွဲသည် | collective communication traffic | interconnect မကောင်းလျှင် communication က လွှမ်းမိုးသည် |
| Time per Output Token (TPOT) | latency | ပထမ token နောက်ပိုင်း ကြားကာလများ၏ ပျမ်းမျှ | (t_N - t_1) / (N - 1) | စတင်ချိန် latency တစ်ခုတည်းက generation ကို မဖော်ပြပါ |
| Tokens per Second (TPS) | throughput | scope နှင့် workload အောက်တွင် ထုတ်လုပ်မှုကို တိုင်းတာသည် | output tokens/s | scope မဖော်ပြလျှင် နှိုင်းယှဉ်၍ မရပါ |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု ငါးခုဖြင့် စုစည်းထားသည် — (က) အချိန်စီစဉ်မှု၊ (ခ) ဖြန့်ကျက်မှု၊ (ဂ) memory၊ (ဃ) တိုင်းတာမှု၊ (င) runtime နှင့် control။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — အချိန်စီစဉ်မှု (scheduling)

#### Continuous Batching

Continuous Batching သည် ပုံသေ batch တစ်ခုအတွင်းရှိ request အားလုံး ပြီးဆုံးသည်အထိ မစောင့်ဘဲ iteration နယ်နိမိတ်များတွင် generation request များကို ထည့်သွင်း သို့မဟုတ် ဖယ်ရှားပေးသည့် serving scheduler ဖြစ်သည်။ autoregressive request များ၏ output အရှည် မတူညီသည့်အတွက် တိုတောင်းသည့် request များသည် အရှည်ဆုံး request အတွက် စောင့်စရာ မလိုတော့ပါ။ accelerator သည် အလုပ်ဖြစ်နေသည့် အချိန် တိုးလာသည့်အတွက် ၎င်းသည် throughput ဝင်ရိုး၏ အဓိက knob ဖြစ်သည်။ serving engineer သည် စွမ်းရည် လွတ်လာသည့်အခါ request အသစ် လက်ခံမှုနှင့် live batch သို့မဟုတ် KV-cache budget ပြည့်လျှင် backpressure ထည့်မှုကို တွဲ၍ သတ်မှတ်ရမည်။

#### Dynamic Batching

Dynamic Batching သည် queue တွင် စောင့်နေသည့် request များမှ inference batch များကို ကိုက်ညီသည့် shape၊ အများဆုံး အရွယ်အစား၊ priority နှင့် ခွင့်ပြုထားသည့် queue ကြာချိန် အလိုက် ဖွဲ့စည်းသည့် runtime policy ဖြစ်သည်။ request များကို အတွဲလိုက် စုခြင်းသည် hardware အသုံးချမှုကို တိုးတက်စေနိုင်သော်လည်း traffic ကျဲပါးသည့်အခါ သို့မဟုတ် request များ သိသိသာသာ ကွာခြားသည့်အခါ batch အတွက် စောင့်ခြင်းသည် latency ကို ပိုဆိုးစေနိုင်သည်။ ထို့ကြောင့် queue-delay ကန့်သတ်ချက်နှင့် batch အများဆုံး အရွယ်အစားကို တိုင်းတာထားသည့် latency ပန်းတိုင်များမှ ဆုံးဖြတ်ရမည်။ ဤ policy သည် လည်ပတ်မှု မစမီ အဆင့်တွင် batch ဖွဲ့သည်၊ လည်ပတ်နေစဉ်အတွင်း batch ၏ အဖွဲ့ဝင်များကို ပြောင်းလဲသည့် Continuous Batching နှင့် ကွာခြားသည်။

#### Chunked Prefill

Chunked Prefill သည် ရှည်လျားသည့် prompt တစ်ခု၏ prefill အလုပ်ကို schedule လုပ်နိုင်သည့် အပိုင်းအစငယ်များအဖြစ် ခွဲပေးသည့် serving နည်းစနစ် ဖြစ်သည်။ ထိုသို့ ခွဲခြင်းဖြင့် prompt ကို စီမံသည့် အလုပ်သည် အခြား request များ၏ decode အလုပ်နှင့် အလှည့်ကျ ရောနှောနိုင်သည်။ မခွဲပါက ရှည်လျားသည့် prompt တစ်ခုသည် accelerator ကို သိမ်းပိုက်ထားနိုင်ပြီး တက်ကြွနေသည့် generation များကို နှောင့်နှေးစေကာ စုစုပေါင်း throughput ကျန်းမာနေသည့်တိုင် tail latency ညံ့ဖျင်းနိုင်သည်။ ၎င်းသည် schedule လုပ်သည့် ပုံစံကို ပြောင်းလဲခြင်းသာ ဖြစ်သည်၊ model ၏ context window ကို မတိုးချဲ့ပါ။ serving engineer သည် scheduling overhead နှင့် prefill ပြီးစီးမှု၊ decode latency၊ goodput တို့ကို ရောနှောသည့် prompt အရှည်များအောက်တွင် နှိုင်းယှဉ်ရမည်။

#### Prefill

Prefill သည် ပေးထားသည့် input token အားလုံးကို စီမံ၍ ၎င်းတို့၏ representation များနှင့် နောက်ဆက်တွဲ autoregressive generation အတွက် လိုအပ်သည့် attention state ကို ထုတ်လုပ်သည့် ကနဦး inference အဆင့် ဖြစ်သည်။ prompt tokens အားလုံးကို တစ်ပြိုင်နက် တွက်သည့်အတွက် ၎င်းသည် compute အပေါ် ဖိအား သက်ရောက်ပြီး TTFT ကို တိုက်ရိုက် ဆုံးဖြတ်သည်။ prompt ပုံစံ၊ queueing နှင့် cache ပြန်သုံးမှုတို့သည် prefill ကုန်ကျစရိတ်ကို ပြောင်းလဲသည်၊ ထို့ကြောင့် prefill သည် decode နှင့် compute အတွက် ယှဉ်ပြိုင်ပုံ မတူပါ။ serving engineer သည် prompt တိုကန် အရေအတွက်နှင့် prefill latency ကို မှတ်တမ်းတင်ပြီး queue ကြာချိန်နှင့် လည်ပတ်ချိန်ကို ခွဲထားရမည်။

#### Decode Phase

Decode Phase သည် input prefix ကို စီမံပြီးနောက် token အသစ်များကို တစ်လှမ်းချင်း ထုတ်လုပ်သည့် autoregressive inference ၏ ထပ်ခါတလဲလဲ လုပ်ဆောင်ရသည့် အဆင့် ဖြစ်သည်။ ၎င်း၏ အလုပ်သည် prefill နှင့် compute၊ memory နှင့် scheduling အပြုအမူ ကွာခြားသည့်အတွက် စုစုပေါင်း latency ကိန်းတစ်ခုတည်းက တကယ့် bottleneck ကို ဖုံးကွယ်နိုင်သည်။ decode အဆင့်တိုင်းသည် token တစ်လုံးလျှင် weight byte အားလုံးကို ပြန်ဖတ်သည့်အတွက် memory bandwidth အပေါ် မှီခိုပြီး inter-token latency ကို ဆုံးဖြတ်သည်။ serving engineer သည် inter-token latency နှင့် output throughput ကို သီးခြား တိုင်းတာပြီး KV-cache နေရာ ယူထားမှုကို ထည့်သွင်းရမည်။

### မိသားစု (ခ) — ဖြန့်ကျက်မှု (parallelism)

#### Tensor Parallelism

Tensor Parallelism သည် model layer တစ်ခုအတွင်းရှိ tensor operation များကို device များအကြား ပိုင်းခြားပြီး layer တွက်ချက်မှုအတွင်း ကျသွားသည့် ရလဒ် အစိတ်အပိုင်းများကို collective communication ဖြင့် ပေါင်းစပ်ပေးသည်။ ၎င်းသည် layer တစ်ခုအား device အတော်များများ၏ memory နှင့် compute ကို အသုံးပြုနိုင်စေသည့်အတွက် compute utilisation ကို မြှင့်စေသည်။ သို့သော် interconnect သို့မဟုတ် partition မသင့်လျော်သည့်အခါ အကြိမ်များစွာ communication လုပ်ရခြင်းက လွှမ်းမိုးနိုင်သည်။ serving engineer သည် partition dimension များကို model shape များနှင့် ကိုက်ညီစေပြီး rank များကို အမြန်သည့် interconnect တွင် ထားရမည်။

#### Pipeline Parallelism

Pipeline Parallelism သည် ဆက်တိုက် လိုက်နာရသည့် model layer အုပ်စုများကို device များအကြား ပိုင်းခြားပြီး microbatch များ သို့မဟုတ် request များကို ထို အဆင့်များမှတစ်ဆင့် pipeline တစ်ခုကဲ့သို့ ရွှေ့ပေးသည်။ ၎င်းသည် device တစ်ခု၏ memory ထက် ကြီးသည့် model များကို ထည့်သွင်းနိုင်စေသည့်အတွက် accelerator memory ဝင်ရိုးကို ဖွင့်ပေးသည်။ သို့သော် အဆင့်များ မညီမျှမှု၊ pipeline bubble၊ activation လွှဲပြောင်းမှုများနှင့် failure ညှိနှိုင်းမှုတို့သည် အသုံးဝင်သည့် စွမ်းဆောင်ရည်ကို သက်ရောက်သည်။ serving engineer သည် အဆင့်တစ်ခုချင်း၏ ကုန်ကျစရိတ်ကို ညီမျှစေပြီး အားလပ်ချိန်နှင့် interconnect traffic ကို တိုင်းတာရမည်။

#### Expert Parallelism

Expert Parallelism သည် mixture-of-experts subnetwork များကို device များအကြား ဖြန့်ဝေပြီး token တစ်ခုချင်း ရွေးချယ်ထားသည့် expert များကို လက်ခံဆောင်ရွက်သည့် device များဆီသို့ ၎င်း token ၏ activation များကို route လုပ်ပေးသည်။ ကျဲပါးသည့် expert များသည် token တိုင်းအတွက် expert တိုင်းကို လည်ပတ်စေခြင်း မပြုဘဲ model စွမ်းရည်ကို တိုးမြှင့်ပေးသည်၊ သို့သော် routing သည် communication၊ load-balance နှင့် placement ကန့်သတ်ချက်များကို ဖြစ်ပေါ်စေသည်။ total parameter သည် VRAM ကို ဆုံးဖြတ်ပြီး active parameter သည် compute ကို ဆုံးဖြတ်သည့်အတွက် ဤနှစ်ကိန်းကို ခွဲခြား မှတ်တမ်းတင်ရမည်။ serving engineer သည် expert အလိုက် token ဖြန့်ဝေမှုကို တိုင်းတာပြီး traffic သည် expert လိုအပ်ချက်ကို မညီမျှစွာ ဖြစ်ပေါ်စေသည့်အခါ အရည်အသွေးကို စမ်းသပ်ရမည်။

### မိသားစု (ဂ) — memory

#### Paged KV Cache

Paged KV Cache သည် attention state ကို ပုံသေ အရွယ်အစား block များတွင် သိမ်းဆည်းပြီး logical sequence နေရာများကို physical block များသို့ map လုပ်ပေးသည့် KV-cache memory manager ဖြစ်သည်၊ sequence တစ်ခုချင်းအတွက် ဆက်တိုက် allocation တစ်ခုတည်း လိုအပ်ခြင်း မရှိပါ။ sequence အရှည် မတူညီမှုသည် fragmentation နှင့် ခန့်မှန်းမရသည့် ကြီးထွားမှုကို ဖြစ်ပေါ်စေသည့်အတွက် block အခြေခံ allocation သည် အသုံးဝင်သည့် memory ကို တိုးတက်စေပြီး ပြောင်းလွယ်သည့် sharing ကို ဖြစ်နိုင်စေသည်။ အသုံးဝင်သည့် memory တိုးလာသည့်အတွက် တူညီသည့် accelerator ပေါ်တွင် batch အရေအတွက် တိုးလာသည်။ ၎င်းသည် runtime attention-state memory ကို စီမံသည်၊ model parameter များကို disk သို့ မရွှေ့သလို model ၏ context limit ကို လည်း မတိုးချဲ့ပါ။ serving engineer သည် block size ကို workload တိုင်းတာမှုများမှ ရွေးပြီး memory ဖိအားအောက်တွင် cancellation နှင့် prefix sharing ကို စမ်းသပ်ရမည်။

#### Prefix Caching

Prefix Caching သည် တူညီပြီး သတ်မှတ်ချက် ပြည့်မီသည့် token prefix တစ်ခုအတွက် ထုတ်လုပ်ထားသည့် KV-cache block များကို request များအကြား ပြန်လည် အသုံးပြုခြင်း ဖြစ်သည်၊ ထိုသို့ဖြင့် serving runtime သည် ထပ်ခါတလဲလဲ prefix တွက်ချက်မှုကို ကျော်လွှားနိုင်သည်။ မျှဝေသည့် system instruction၊ template သို့မဟုတ် document များသည် prefill အလုပ်ကို အတော်အသင့် စားသုံးနိုင်သည့်အတွက် cache hit rate သည် cost per million tokens အပေါ် တိုက်ရိုက် သက်ရောက်သည်။ ပြန်သုံးမှုသည် token sequence များနှင့် cache သတ်မှတ်ချက် ကိုက်ညီသည့်အခါမှသာ အကျိုးရှိသည်၊ မကိုက်ညီလျှင် အကျိုးအမြတ် မရှိပါ။ ၎င်းသည် တိကျသည့် token prefix များအတွက် runtime attention state ကို ပြန်သုံးခြင်း ဖြစ်ပြီး ပိုမို ကျယ်ပြန့်သည့် provider သဘောတူညီချက်နှင့် မတူပါ။ serving engineer သည် တည်ငြိမ်သည့် token များကို request သီးသန့် အကြောင်းအရာ မတိုင်မီ ထားပြီး tenant ဆိုင်ရာ state ကို သီးခြားထားရမည်။

#### FlashAttention

FlashAttention သည် accelerator memory အလွှာများအကြား လွှဲပြောင်းမှုများကို လျှော့ချရန် တွက်ချက်မှုကို tile များအဖြစ် ခွဲ၍ လုပ်ဆောင်သည့် တိကျသည့် attention algorithm ဖြစ်သည်၊ attention matrix အပြည့်ကို high-bandwidth memory တွင် အမှန်တကယ် တည်ဆောက်ထားရန် မလိုအပ်စေပါ။ အထူးသဖြင့် ရှည်လျားသည့် sequence များတွင် attention သည် ဂဏန်း တွက်ချက်မှုထက် memory လှုပ်ရှားမှုကြောင့် ကန့်သတ်ခံရနိုင်သည့်အတွက် IO ကို သိသည့် kernel သည် အသုံးဝင်သည့် အမြန်နှုန်းနှင့် memory စွမ်းရည်ကို တိုးတက်စေသည်။ တွက်ချက်သည့် နည်းလမ်းကို ပြောင်းလဲသော်လည်း ရည်မှန်းသည့် သင်္ချာ attention ရလဒ်ကို မပြောင်းလဲပါ။ serving engineer သည် model ၏ shape၊ mask၊ dtype နှင့် hardware တို့ ထောက်ပံ့သည့် kernel ကို အသုံးပြုပြီး paper ရလဒ်ကို ပုံသေ multiplier အဖြစ် ကိုးကားမည့်အစား end-to-end latency ကို benchmark လုပ်ရမည်။

### မိသားစု (ဃ) — တိုင်းတာမှု (measurement)

#### Goodput

Goodput သည် သတ်မှတ်ထားသည့် workload တစ်ခုအောက်တွင် သတ်မှတ်ထားသည့် ဝန်ဆောင်မှု ကန့်သတ်ချက်များ — ဥပမာ TTFT နှင့် per-token latency ပန်းတိုင် နှစ်ခုလုံး — ပြည့်မီသည့် ပြီးစီးသွားသည့် request များ၏ နှုန်း ဖြစ်သည်။ ကုန်ကြမ်း throughput မြင့်တက်နေစဉ် အသုံးပြုသူများသည် နှေးကွေးသည့် request များကို ပိုမို ကြုံတွေ့နိုင်သည့်အတွက် goodput သည် ဝန်ဆောင်မှု သဘောတူညီချက် ပြည့်မီသည့် အလုပ်ကိုသာ ရေတွက်သည်။ ၎င်းသည် ပြီးစီးသည့် throughput အားလုံး မဟုတ်သလို model တစ်ခု၏ အားလုံးအတွက် တူညီသည့် ဂုဏ်သတ္တိလည်း မဟုတ်ပါ။ serving engineer သည် request ဖြန့်ဝေမှု ပုံစံနှင့် latency သတ်မှတ်ချက်များကို ကြေညာပြီး ကိုက်ညီသည့် ပြီးစီးမှုများကိုသာ ရေတွက်ရမည်။

#### Tokens per Second (TPS)

Tokens per Second သည် သတ်မှတ်ထားသည့် scope နှင့် workload တစ်ခုအောက်တွင် serving စနစ် တစ်ခုသည် အချိန် တစ်ယူနစ်အတွင်း output token မည်မျှ ထုတ်လုပ်သည်ကို ဖော်ပြသည့် throughput အတိုင်းအတာ ဖြစ်သည်။ ၎င်းသည် စတင်ချိန် latency ကို ဖြည့်စွက်ပေးပြီး output စပြီးနောက် generation မည်မျှ မြန်သည်ကို ပြသသည်။ လက်တွေ့ နှိုင်းယှဉ်မှုတွင် များစွာ အသုံးပြုခံရသော တိုင်းတာမှု ဖြစ်သည့်အတွက် ဖော်ပြချက် မပြည့်စုံလျှင် လွဲမှားသည့် ဆုံးဖြတ်ချက် ဖြစ်စေသည်။ serving engineer သည် TPS သည် request တစ်ခုချင်းအတွက် ဟုတ်သည် သို့မဟုတ် စုစုပေါင်း ဟုတ်သည်၊ prefill ကို ဖယ်ထားသည် သို့မဟုတ် သီးခြား ဖော်ပြသည်၊ batch၊ concurrency၊ sequence အရှည်များနှင့် hardware ကို ဖော်ပြရမည်။

#### Time per Output Token (TPOT)

Time per Output Token သည် `N > 1` output token ရှိသည့် request တစ်ခုအတွက် ပထမ token နောက်ပိုင်း ကြားကာလများ၏ ပျမ်းမျှ — `(t_N - t_1) / (N - 1)` — ဖြစ်ပြီး စနစ် ဖြန့်ဝေမှု ပုံစံများသည် ထို request တစ်ခုချင်း ပျမ်းမျှများကို စုစည်းသည်။ အသုံးပြုသူသည် ပထမ token ကို လျင်မြန်စွာ ရရှိသော်လည်း ကျန် အဖြေသည် နှေးကွေးစွာ စီးဆင်းနိုင်သည့်အတွက် စတင်ချိန် latency တစ်ခုတည်းက generation တုံ့ပြန်မှုကို ဖော်ပြပေးနိုင်သည် မဟုတ်ပါ။ ၎င်းသည် request တစ်ခုချင်း ပျမ်းမျှ ဖြစ်ပြီး inter-token latency တစ်ခုချင်းသည် ဆက်တိုက် token နှစ်ခုအကြား ကွာဟချက် တစ်ခု ဖြစ်သည်။ serving engineer သည် TPOT ကို request တစ်ခုချင်းအတွက် သီးခြား တွက်ပြီး output အရှည်နှင့် concurrency အလိုက် percentile များကို ဖော်ပြရမည်။

#### Inter-Token Latency (ITL)

Inter-Token Latency သည် request တစ်ခုအတွက် output token နှစ်ခု ဆက်တိုက် ရောက်ရှိသည့် အချိန် အစီအစဉ် နှစ်ခုအကြား ကြာချိန် ဖြစ်သည်၊ ပထမမဟုတ်သည့် output token တစ်ခုအတွက် `t_i - t_(i-1)` ဟု တွက်ချက်သည်။ token ကြား ကွာဟမှု တစ်ခုချင်းသည် decode ရပ်တန့်မှုများနှင့် streaming တုန်ခါမှုကို ဖော်ထုတ်ပေးသည်၊ request တစ်ခုချင်း ပျမ်းမျှက ထို အချက်များကို ဖုံးကွယ်နိုင်သည်၊ အထူးသဖြင့် batching၊ preemption သို့မဟုတ် ရောနှော workload များအောက်တွင် ဖြစ်သည်။ ၎င်းသည် ဆက်တိုက် token များအကြား ကြားကာလ တစ်ခု ဖြစ်ပြီး time per output token သည် ထို ကြားကာလများ၏ request တစ်ခုချင်း ပျမ်းမျှ ဖြစ်သည်။ serving engineer သည် ပထမ token နောက်ပိုင်း ကြားကာလ တစ်ခုချင်းကို ၎င်း၏ request နှင့် token နေရာ နှင့်အတူ မှတ်တမ်းတင်ပြီး request နယ်နိမိတ်များကို ရောစပ်ပစ်ခြင်း မပြုရပါ။

### မိသားစု (င) — runtime နှင့် control

#### Model Serving

Model Serving သည် version သတ်မှတ်ထားသည့် model artifact များကို ဖွင့်တင်ပေးပြီး inference request များကို လက်ခံကာ လည်ပတ်မှုကို schedule လုပ်ပြီး အရင်းအမြစ်များကို စီမံကာ လုပ်ငန်း သဘောတူညီချက် အောက်တွင် ရလဒ်များကို ပြန်ပေးသည့် runtime နှင့် API အလွှာ ဖြစ်သည်။ စွမ်းရည်ကောင်းသည့် model တစ်ခုသည် queueing၊ batching၊ placement၊ versioning၊ cancellation နှင့် ဖြေကြားမှု နယ်နိမိတ်များကို အင်ဂျင်နီယာ နည်းဖြင့် ရှင်းလင်းစွာ မလုပ်ဆောင်ပါက ယုံကြည်မရသည့် ထုတ်ကုန် ဖြစ်စေနိုင်သည့်အတွက် ၎င်းသည် production consequence ဝင်ရိုး၏ အခြေခံ ဖြစ်သည်။ ၎င်းသည် inference တစ်ခါ ခေါ်ခြင်းထက် ပိုကျယ်ပြန့်ပြီး retrieval၊ tool၊ policy နှင့် user state ပါဝင်သည့် အပလီကေးရှင်း တစ်ခုလုံးထက် ကျဉ်းမြောင်းသည်။ serving engineer သည် model နှင့် tokenizer version များကို pin လုပ်ပြီး readiness နှင့် latency signal များကို ဖော်ထုတ်ရမည်။

#### Disaggregated Serving

Disaggregated Serving သည် prefill အလုပ်နှင့် decode အလုပ်ကို သီးခြား စီစဉ်ပေးထားသည့် worker pool များတွင် လည်ပတ်စေပြီး လိုအပ်သည့် attention state ကို ထို pool များအကြား လွှဲပြောင်းပေးသည့် serving ဗိသုကာ ဖြစ်သည်။ prefill နှင့် decode သည် hardware အပေါ် ဖိအား သက်ရောက်ပုံ မတူညီသည့်အတွက် သီးခြား pool များသည် တစ်ခုတည်းသော queue တွင် ယှဉ်ပြိုင်ရမည့်အစား မိမိတို့၏ bottleneck အလိုက် အရွယ်အစား သတ်မှတ်နိုင်၊ schedule လုပ်နိုင်သည်။ disaggregation သည် runtime အဆင့်များကို ခွဲထုတ်ခြင်း ဖြစ်သည်၊ အဆင့်တစ်ခုအတွင်း model တစ်ခုကို shard များအဖြစ် ခွဲခြင်း မဟုတ်ပါ။ serving engineer သည် state လွှဲပြောင်းမှု ကုန်ကျစရိတ်ကို တိုင်းတာပြီး pool တစ်ခုချင်းကို ၎င်း၏ demand signal မှ scale လုပ်ရမည်။

#### Autoscaling

Autoscaling သည် တောင်းဆိုမှု၊ အရင်းအမြစ် အသုံးပြုမှု သို့မဟုတ် application metric များမှ လေ့လာတွေ့ရှိချက်အပေါ် အခြေခံ၍ serving worker များ၏ အရေအတွက် သို့မဟုတ် စွမ်းရည်ကို သတ်မှတ်ထားသည့် အတိုင်းအတာ အတွင်း ပြောင်းလဲပေးသည့် control loop ဖြစ်သည်။ AI workload များသည် လူကိုယ်တိုင် စီစဉ်ပေးသည့် provisioning ထက် ပိုမြန်စွာ ပြောင်းလဲနိုင်သော်လည်း scaling ဆုံးဖြတ်ချက်များတွင် model ဖွင့်တင်ရန် ကြာချိန်၊ accelerator ရရှိနိုင်မှု၊ queueing နှင့် request တစ်ခု၏ ကုန်ကျစရိတ်တို့ကို ထည့်သွင်း စဉ်းစားရမည်။ autoscaling သည် စွမ်းရည်ကို ထပ်တိုး သို့မဟုတ် လျှော့ချသည်၊ overload ဖြစ်နေသည့် dependency ကို ပိုမြန်စေသည် မဟုတ်သလို လိုအပ်သည့် hardware ကို အချိန်မီ ရရှိမည်ဟုလည်း အာမခံသည် မဟုတ်ပါ။ serving engineer သည် အသုံးဝင်သည့် အလုပ် — goodput — နှင့် ချိတ်ဆက်ထားသည့် demand signal မှ scale လုပ်ပြီး replica အသစ်များသည် traffic မရရှိမီ readiness check များ အောင်မြင်ကြောင်း စစ်ဆေးရမည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။

### (က) ဝန်ဆောင်မှု ပေးသည့် model ၏ memory budget — weight၊ KV cache၊ activation

ဖော်မြူလာ — `weights = params_b * 1e9 * bytes_per_element`၊ `kv_per_seq = 2 * layers * heads * head_dim * context * bytes_per_element`၊ `activations = batch * context * d_model * ACTIVATION_FACTOR * bytes_per_element`၊ `total = weights + batch * kv_per_seq + batch * act_per_seq`။ ယူဆချက် (assumption) — params 8.0B၊ layers 32၊ heads 32၊ head_dim 128 (d_model 4096)၊ context 8192၊ fp16 သည် 2 byte/element၊ activation factor 4.0၊ memory budget 72.000 GiB။

```text
$ python3 guides/09_infrastructure_and_serving/scripts/ex_a_memory_budget.py
reference serving geometry: params=8.0B layers=32 heads=32 head_dim=128 d_model=4096 context=8192 dtype=fp16
assumption: fp16 = 2.000 bytes per parameter and per KV element; activation workspace = batch * context * d_model * 4.00 * bytes
weights on the accelerator        =    16000000000 B =   14.901 GiB
KV cache per sequence             =     4294967296 B =    4.000 GiB
activation workspace per sequence =      268435456 B =    0.250 GiB
memory budget (stated)            =    77309411328 B =   72.000 GiB

batch    KV total GiB    act GiB    total GiB   fits   headroom GiB
1               4.000      0.250       19.151    yes         52.849
8              32.000      2.000       48.901    yes         23.099
32            128.000      8.000      150.901     no        -78.901
64            256.000     16.000      286.901     no       -214.901
128           512.000     32.000      558.901     no       -486.901

largest batch that fits 72.000 GiB with these weights = 13
memory per sequence beyond the weights = 4.250 GiB (KV 4.000 + activations 0.250)
doubling the batch doubles KV cache and activation memory but not the weights; KV cache grows with context, weights do not
```

ဤဇယားက batch အရေအတွက်နှင့် memory ၏ ဆက်စပ်မှုကို ပြသည် — weight byte သည် batch အပေါ် မမှီခိုပါ၊ သို့သော် KV cache နှင့် activation သည် batch တစ်လုံးလျှင် 4.250 GiB တိုးသည်။ 72.000 GiB budget အောက်တွင် တင်နိုင်သည့် အကြီးဆုံး batch သည် 13 ဖြစ်ပြီး batch 32 သည် 150.901 GiB လိုအပ်သည့်အတွက် လုံးဝ မဆံ့ပါ။ ထို့ကြောင့် batch ကို ကြီးစေသည့် မည်သည့် ဆုံးဖြတ်ချက်မဆို accelerator အရေအတွက် သို့မဟုတ် KV precision နှင့် တွဲဖက် သတ်မှတ်ရမည်။

### (ခ) Roofline ခန့်မှန်းချက် — tokens/s နှင့် cost per million tokens

ဖော်မြူလာ — `bytes_per_step = weight_bytes + batch * kv_bytes_per_token`၊ `tokens/s = batch * bandwidth / bytes_per_step`၊ `achieved = ceiling * efficiency`၊ `cost_per_million = price_per_hour / (tokens_per_s * 3600) * 1e6`။ ယူဆချက် (assumption) — bandwidth 3350.0 GB/s၊ memory bandwidth အသုံးပြုမှု အချိုး 75.0%၊ params 8.0B fp16၊ KV token တစ်လုံးလျှင် 524288 B (32L/32H/128D)၊ GPU-hour စျေးနှုန်း USD 2.50။

```text
$ python3 guides/09_infrastructure_and_serving/scripts/ex_b_roofline.py
roofline estimate - memory bandwidth bound decode (not a benchmark)
assumption: bandwidth=3350.0 GB/s  achieved=75.0%  GPU-hour price=USD 2.50  KV=524288 B per token per sequence
weights = 16000000000 B = 16.000 GB (fp16)

batch      bytes/step    tok/s ceiling   tok/s achieved   USD/1e6 tokens
1          1.6001e+10            209.4            157.0           4.4225
8          1.6004e+10           1674.6           1255.9           0.5529
32         1.6017e+10           6693.0           5019.7           0.1383
64         1.6034e+10          13372.0          10029.0           0.0692
128        1.6067e+10          26688.1          20016.0           0.0347

cost ratio batch 1 / batch 128 = 127.47x
the weight bytes are shared by every sequence in the batch, so batch size sets cost per million tokens until KV cache dominates the step
assumption: bandwidth, efficiency and price are stated inputs and vary by accelerator, vendor and region
```

ရလဒ်က ပြသည့် အဓိက အချက်မှာ batch 1 မှ batch 128 သို့ ရွေ့လျှင် cost per million tokens သည် 127.47 ဆ ကျဆင်းခြင်း ဖြစ်သည်၊ အကြောင်းမှာ weight byte သည် sequence အရေအတွက်ဖြင့် အကြိမ်များစွာ ပြန်လည် အသုံးပြုခံရခြင်း ဖြစ်သည်။ ဤအကျိုးအမြတ်သည် VRAM (KV cache) နှင့် latency (batch အတွင်း စောင့်ချိန်) ဖြင့် ဝယ်ယူရသည်။ bandwidth၊ efficiency နှင့် စျေးနှုန်း အားလုံးသည် stated assumption ဖြစ်သည့်အတွက် ဤကိန်းများကို vendor တစ်ခုမှ တစ်ခုသို့ တိုက်ရိုက် သယ်ဆောင်၍ မရပါ။

### (ဂ) Replica အရေအတွက်နှင့် ကုန်ကျစရိတ် — arrival rate၊ output အရှည်၊ per-replica throughput

ဖော်မြူလာ — `offered_load = rps * output_tokens`၊ `effective_per_replica = replica_tps * target_utilisation`၊ `required = ceil(offered_load / effective_per_replica)`၊ `queue_growth = max(0, offered_load - replicas * replica_tps) / output_tokens`။ ယူဆချက် (assumption) — rps 12.0၊ output tokens 220၊ per-replica throughput 900.0 tokens/s၊ target utilisation 0.75၊ GPU-hour စျေးနှုန်း USD 2.50။

```text
$ python3 guides/09_infrastructure_and_serving/scripts/ex_c_replicas.py
replica sizing - arrival rate 12.0 req/s, 220 output tokens, 900 tokens/s per replica
assumptions: target utilisation=0.75  GPU-hour price=USD 2.50
offered load = 12.0 req/s * 220 tokens = 2640.0 output tokens/s
effective capacity per replica at the target = 675.0 tokens/s
required replicas for the target utilisation = 4

replicas   utilisation  served tok/s     queue req/s      USD/hour     USD/1e6 tokens
2                1.467        1800.0           3.818          5.00             0.7716
3                0.978        2640.0           0.000          7.50             0.7891
4                0.733        2640.0           0.000         10.00             1.0522
5                0.587        2640.0           0.000         12.50             1.3152
6                0.489        2640.0           0.000         15.00             1.5783

over-provisioning cost: each replica above 4 is unused capacity = USD 2.50/hour idle
under-provisioning cost: at 2 replicas the queue grows 3.818 requests/s = 229 requests queued in 60 s
requirement 4 replicas at USD 2.50/hour = USD 10.00/hour, 1.0522 USD per million output tokens at this load
under-provisioning costs latency (the queue is unbounded), over-provisioning costs USD/hour; both are visible in this table
```

offered load သည် 2640.0 output tokens/s ဖြစ်ပြီး target utilisation အောက်တွင် ထမ်းရန် replica 4 လုံး လိုသည်ကို ဇယားက ပြသည်။ replica 2 လုံးဖြင့် utilisation သည် 1.467 ဖြစ်လာပြီး queue သည် တစ်စက္ကန့်လျှင် 3.818 request ကြီးထွားသည်၊ ဆိုလိုသည်မှာ latency သည် အကန့်အသတ်မရှိ တိုးလာသည်။ replica 5 နှင့် 6 တွင် utilisation ကျသော်လည်း USD per million tokens သည် အချိုးကျ တိုးသည်၊ ထို့ကြောင့် under-provisioning နှင့် over-provisioning နှစ်ခုလုံးသည် တိုင်းတာနိုင်သည့် ကုန်ကျစရိတ် ဖြစ်သည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် ထုတ်လုပ်မှု ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Batching policy သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Continuous Batching၊ Dynamic Batching၊ Decode Phase၊ Prefill။ သက်သေပြသည့် မက်ထရစ် — tokens/s၊ inter-token latency နှင့် queue delay။ ဥပမာ (ခ) က batch 128 တွင် 39865.6 tokens/s ရရှိပြီး batch 1 တွင် 157.0 tokens/s သာ ရရှိသည်ဟု ပြသည်၊ သို့သော် batch ကြီးလျှင် inter-token latency နှင့် KV VRAM တိုးသည်။

**၂။ KV memory နှင့် context limit သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Paged KV Cache၊ Prefix Caching၊ Prefill။ သက်သေပြသည့် မက်ထရစ် — sequence တစ်ခုလျှင် KV GiB နှင့် တင်နိုင်သည့် အကြီးဆုံး batch။ ဥပမာ (က) က context 8192 တွင် KV cache သည် sequence တစ်ခုလျှင် 4.000 GiB ဖြစ်ပြီး 72.000 GiB budget အောက်တွင် batch 13 အထိသာ ဆံ့သည်ဟု ပြသည်။

**၃။ Parallelism strategy ရွေးချယ်ခြင်း** — မှီခိုသည့် term များ — Tensor Parallelism၊ Pipeline Parallelism၊ Expert Parallelism။ သက်သေပြသည့် မက်ထရစ် — device တစ်လုံးလျှင် parameter ပမာဏ၊ collective communication traffic နှင့် pipeline bubble ရာခိုင်နှုန်း။ ဤဆုံးဖြတ်ချက်သည် memory နှင့် compute နှစ်ခုလုံးအပေါ် တစ်ပြိုင်နက် သက်ရောက်သည်။

**၄။ Prefill နှင့် decode ကို ခွဲခြင်း** — မှီခိုသည့် term များ — Disaggregated Serving၊ Chunked Prefill၊ Prefill၊ Decode Phase။ သက်သေပြသည့် မက်ထရစ် — TTFT၊ inter-token latency နှင့် pool တစ်ခုချင်း၏ utilisation။ state လွှဲပြောင်းမှု ကုန်ကျစရိတ်ကို ထည့်သွင်းစဉ်းစားပြီး ပုံစံချထားသည့် chunk များဖြင့် စမ်းသပ်ရမည်။

**၅။ Autoscaling policy နှင့် headroom သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Autoscaling၊ Goodput၊ Tokens per Second (TPS)၊ Time per Output Token (TPOT)၊ Inter-Token Latency (ITL)။ သက်သေပြသည့် မက်ထရစ် — required replicas၊ utilisation၊ queue growth၊ scale-up time နှင့် USD/hour။ ဥပမာ (ဂ) က queue ကြီးထွားသည့် အခြေအနေတွင် replica နှစ်လုံး ထပ်တိုးရန် scale-up time 90.0 s လိုသည်ဟု ပြသည်၊ ထို့ကြောင့် cold start ကို ထည့်တွက်ပြီး warm capacity သတ်မှတ်ရမည်။

**၆။ Cost monitoring နှင့် goodput သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Model Serving၊ Goodput၊ Tokens per Second (TPS)၊ Prefix Caching၊ FlashAttention။ သက်သေပြသည့် မက်ထရစ် — cost per million output tokens (input နှင့် output ခွဲခြား၍) နှင့် SLO ပြည့်မီသည့် request နှုန်း။ raw throughput အမြင့်ဆုံး ဆက်တင်သည် goodput အမြင့်ဆုံး ဆက်တင် မဖြစ်နိုင်သည့်အတွက် နှစ်ကိန်းကို တွဲ၍ တိုင်းတာရမည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/09_infrastructure_and_serving/labs/lab_serving_memory.py`၊ `lab_roofline.py`၊ `lab_autoscale.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ဤစာတမ်းရှိ ကိန်းဂဏန်းများသည် ထို lab များ ရှိခြင်း အပေါ် မှီခိုသည် မဟုတ်ပါ။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/09_infrastructure_and_serving.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/09_infrastructure_and_serving.json`။

# 09 — Infrastructure & serving

ဤနယ်ပယ်သည် သင်တန်းပေးပြီးသား model တစ်ခုကို အသုံးပြုသူ တောင်းဆိုမှုများအတွက် တကယ် အလုပ်လုပ်စေသည့် အဆင့်ကို ဖုံးလွှမ်းသည် — inference request များ လက်ခံခြင်း၊ schedule လုပ်ခြင်း၊ accelerator ပေါ်တွင် လည်ပတ်စေခြင်း၊ ရလဒ် ပြန်ပေးခြင်း။ **Model Serving** သည် ဤအလွှာ၏ အမည် ဖြစ်ပြီး၊ **autoscaling** နှင့် readiness စစ်ဆေးမှုများသည် ထို အလွှာတစ်ဝိုက်တွင် လည်ပတ်သည့် ထိန်းချုပ်မှု များ ဖြစ်သည်။ ဤနယ်ပယ်ရှိ term များကို မသိပါက model တစ်ခု၏ အရည်အသွေး ကောင်းနေသည့်တိုင် တကယ့် ထုတ်ကုန်တွင် တုံ့ပြန်မှု နှေးကွေးခြင်း၊ ကုန်ကျစရိတ် မြင့်မားခြင်း ဖြစ်ပေါ်နိုင်သည်။

Term ၁၈ ခုသည် အဓိက မိသားစု သုံးခုအဖြစ် စုစည်းနိုင်သည်။ ပထမ — အချိန်စီစဉ်မှု (scheduling) မိသားစု: **Continuous Batching**၊ **Dynamic Batching**၊ **Chunked Prefill**၊ **Prefill** နှင့် **Decode Phase**။ ဒုတိယ — စွမ်းရည် ဖြန့်ကျက်မှု (parallelism) မိသားစု: **Tensor Parallelism**၊ **Pipeline Parallelism**၊ **Expert Parallelism**။ တတိယ — ထို နှစ်ခုကို ချိတ်ဆက်ပေးသည့် memory မိသားစု: **KV Cache** ကို စီမံသည့် **Paged KV Cache**၊ ထပ်ခါတလဲလဲ အလုပ် လျှော့ချသည့် **Prefix Caching** နှင့် attention တွက်ချက်မှုကို memory လှုပ်ရှားမှု လျှော့ချ၍ လုပ်ဆောင်သည့် **FlashAttention** တို့ ဖြစ်သည်။

ကျန် term များသည် တိုင်းတာမှုနှင့် ဆုံးဖြတ်ချက် အတွက် ဖြစ်သည် — **Goodput**၊ **Tokens per Second (TPS)**၊ **Time per Output Token (TPOT)** နှင့် **Inter-Token Latency (ITL)** တို့သည် "မြန်သည်" ဟူသည့် စကားလုံးကို တိကျသည့် အတိုင်းအတာ များအဖြစ် ခွဲခြားပေးသည်။ ထို အတိုင်းအတာများ မရှိဘဲ scaling၊ batching သို့မဟုတ် parallelism ဆုံးဖြတ်ချက် တစ်ခုမျှ ခိုင်မာစွာ ချနိုင်မည် မဟုတ်ပါ။ **Disaggregated Serving** နှင့် **Autoscaling** သည် ထို တိုင်းတာမှုများအပေါ် အခြေခံ၍ ဗိသုကာ နှင့် စွမ်းရည် ကို ချိန်ညှိသည့် နေရာတွင် ရှိသည်။

Entry တစ်ခုကို ဖတ်သည့်အခါ **ဆိုလိုသည့် အဓိပ္ပာယ်** ဖြင့် စတင်ပါ — ၎င်းသည် source ၏ အင်ဂျင်နီယာ အဓိပ္ပာယ် ဖြစ်သည်။ ထို့နောက် **အရေးပါသည့် အကြောင်းရင်း** တွင် မည်သည့် စနစ်အပေါ် မည်သို့ သက်ရောက်သည်ကို ကြည့်ပါ။ **မကြာခဏ ရောထွေးမှု** နှင့် **လက်တွေ့** စာကြောင်းများသည် source တွင် ပါသည့်အခါသာ ပေါ်လာသည်။ Technical term များ (throughput၊ latency၊ continuous batching၊ KV cache၊ autoscaling၊ vLLM၊ CUDA၊ GPU memory) ကို မြန်မာ စာကြောင်းအတွင်း အင်္ဂလိပ်အတိုင်း ထားရှိထားသည်။

### Autoscaling

**မြန်မာ:** အလိုအလျောက် စွမ်းရည် ချိန်ညှိခြင်း (autoscaling)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တောင်းဆိုမှု (demand)၊ အရင်းအမြစ် အသုံးပြုမှု သို့မဟုတ် application metric များမှ လေ့လာတွေ့ရှိချက်အပေါ် အခြေခံ၍ serving worker များ၏ အရေအတွက် သို့မဟုတ် စွမ်းရည်ကို သတ်မှတ်ထားသည့် အတိုင်းအတာ (configured bounds) အတွင်း ပြောင်းလဲပေးသည့် control loop ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** AI workload များသည် လူကိုယ်တိုင် စီစဉ်ပေးသည့် provisioning ထက် ပိုမြန်စွာ ပြောင်းလဲနိုင်သည်။ သို့သော် scaling ဆုံးဖြတ်ချက်များတွင် model ဖွင့်တင်ရန် ကြာချိန်၊ accelerator ရရှိနိုင်မှု၊ queueing နှင့် request တစ်ခု၏ ကုန်ကျစရိတ်တို့ကို ထည့်သွင်း စဉ်းစားရမည်။
- **မကြာခဏ ရောထွေးမှု:** autoscaling သည် စွမ်းရည်ကို ထပ်တိုး သို့မဟုတ် လျှော့ချသည်။ overload ဖြစ်နေသည့် dependency ကို ပိုမြန်စေသည် မဟုတ်သလို၊ လိုအပ်သည့် hardware ကို အချိန်မီ ရရှိမည်ဟုလည်း အာမခံသည် မဟုတ်ပါ။
- **လက်တွေ့:** အသုံးဝင်သည့် အလုပ် (useful work) နှင့် ချိတ်ဆက်ထားသည့် demand signal မှ scale လုပ်ရမည်။ အနည်းဆုံး warm capacity ကို သတ်မှတ်ရမည်၊ scale-down အပြောင်းအလဲ (churn) ကို ကန့်သတ်ရမည်၊ replica အသစ်များသည် traffic မရရှိမီ readiness check များ အောင်မြင်ကြောင်း စစ်ဆေးရမည်။
- **ဆက်စပ် term များ:** Model Serving, Saturation, Readiness Probe, Backpressure
- **Learn it:** [GPU Autoscaling on Kubernetes](../phases/17-infrastructure-and-production/03-gpu-autoscaling-kubernetes/)
- **English (source):** A control loop that changes the number or capacity of serving workers from observed demand, resource use, or application metrics within configured bounds. AI workloads can change faster than manual provisioning, but scaling decisions must account for model-load time, accelerator availability, queueing, and request cost.

### Chunked Prefill

**မြန်မာ:** အပိုင်းခွဲ prefill (chunked prefill)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ရှည်လျားသည့် prompt တစ်ခု၏ prefill အလုပ်ကို schedule လုပ်နိုင်သည့် အပိုင်းအစ (chunk) ငယ်များအဖြစ် ခွဲပေးသည့် serving နည်းစနစ် ဖြစ်သည်။ ထိုသို့ ခွဲခြင်းဖြင့် prompt ကို စီမံသည့် အလုပ်သည် အခြား request များ၏ decode အလုပ်နှင့် အလှည့်ကျ ရောနှောနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မခွဲပါက ရှည်လျားသည့် prompt တစ်ခုသည် accelerator ကို သိမ်းပိုက်ထားနိုင်ပြီး၊ တက်ကြွနေသည့် generation များကို နှောင့်နှေးစေသည်။ စုစုပေါင်း throughput ကျန်းမာနေသည့်တိုင် tail latency ညံ့ဖျင်းနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** chunked prefill သည် prompt တွက်ချက်မှုကို schedule လုပ်သည့် ပုံစံကို ပြောင်းလဲသည်။ အသုံးပြုသူ၏ context ကို အဓိပ္ပာယ် သီးသန့်သည့် chunk များအဖြစ် ခွဲသည် မဟုတ်သလို၊ model ၏ context window ကိုလည်း ပြောင်းလဲသည် မဟုတ်ပါ။
- **လက်တွေ့:** တိုင်းတာထားသည့် workload များမှ chunk policy ကို ရွေးချယ်ရမည်၊ scheduling overhead ကို ထည့်သွင်း စဉ်းစားရမည်၊ ရောနှောသည့် prompt အရှည်များအောက်တွင် prefill ပြီးစီးမှု၊ decode latency နှင့် goodput ကို နှိုင်းယှဉ်ရမည်။
- **ဆက်စပ် term များ:** Prefill, Decode Phase, Dynamic Batching, Tail Latency
- **Learn it:** [vLLM Serving Internals](../phases/17-infrastructure-and-production/04-vllm-serving-internals/)
- **English (source):** A serving technique that divides a long prompt's prefill work into smaller schedulable pieces so prompt processing can interleave with decode work from other requests. One long prompt can otherwise occupy the accelerator and delay active generations, producing poor tail latency even when total throughput looks healthy.

### Continuous Batching

**မြန်မာ:** အဆက်မပြတ် batch စီစဉ်ခြင်း (continuous batching)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပုံသေ batch တစ်ခုအတွင်းရှိ request အားလုံး ပြီးဆုံးသည်အထိ မစောင့်ဘဲ၊ iteration နယ်နိမိတ် (iteration boundary) များတွင် generation request များကို ထည့်သွင်း သို့မဟုတ် ဖယ်ရှားပေးသည့် serving scheduler ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** autoregressive request များသည် output အရှည် မတူညီကြသည်။ ထို့ကြောင့် continuous batching သည် တိုတောင်းသည့် request များကို အရှည်ဆုံး request အတွက် စောင့်စေခြင်း မပြုဘဲ accelerator များကို အသုံးချနေစေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** continuous batching သည် inference scheduling policy ဖြစ်သည်။ gradient accumulation မဟုတ်သလို၊ training batch-size နည်းစနစ်လည်း မဟုတ်ပါ။
- **လက်တွေ့:** စွမ်းရည် လွတ်လာသည့်အခါ request အသစ်များကို လက်ခံရမည်၊ request တစ်ခုချင်း၏ latency ကို ခြေရာခံရမည်၊ live batch သို့မဟုတ် KV-cache budget ပြည့်သည့်အခါ backpressure ထည့်ရမည်။
- **ဆက်စပ် term များ:** Dynamic Batching, Decode Phase, Backpressure, Rate Limit
- **English (source):** A serving scheduler that adds and removes generation requests at iteration boundaries instead of waiting for every request in a fixed batch to finish. Autoregressive requests produce different output lengths, so continuous batching can keep accelerators utilized without forcing short requests to wait for the longest one.

### Decode Phase

**မြန်မာ:** decode အဆင့် (decode phase)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** input prefix ကို စီမံပြီးနောက် token အသစ်များကို တစ်လှမ်းချင်း ထုတ်လုပ်သည့် autoregressive inference ၏ ထပ်ခါတလဲလဲ လုပ်ဆောင်ရသည့် အဆင့် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** decode အလုပ်သည် prefill နှင့် compute၊ memory နှင့် scheduling အပြုအမူ ကွာခြားသည်။ ထို့ကြောင့် စုစုပေါင်း latency ကိန်းတစ်ခုတည်းက တကယ့် serving bottleneck ကို ဖုံးကွယ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** decode phase သည် encoder-decoder model ၏ decoder အစိတ်အပိုင်း မဟုတ်ပါ။ runtime ရှိ generation အဆင့်ကို အမည်ပေးခြင်း ဖြစ်သည်။
- **လက်တွေ့:** inter-token latency နှင့် output throughput ကို သီးခြား တိုင်းတာရမည်၊ KV-cache နေရာ ယူထားမှု (occupancy) ကို ထည့်သွင်းရမည်၊ တက်ကြွသည့် decode များသည် prefill အသစ်များနှင့် စွမ်းရည် မျှဝေသည့် ရောနှော workload များကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Prefill, Autoregressive, KV Cache, Time per Output Token (TPOT)
- **Learn it:** [Disaggregated Prefill and Decode](../phases/17-infrastructure-and-production/17-disaggregated-prefill-decode/)
- **English (source):** The iterative stage of autoregressive inference that generates new tokens one step at a time after the input prefix has been processed. Decode work has different compute, memory, and scheduling behavior from prefill, so one aggregate latency number can hide the actual serving bottleneck.

### Disaggregated Serving

**မြန်မာ:** ခွဲထားသည့် serving ဗိသုကာ (disaggregated serving)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** prefill အလုပ်နှင့် decode အလုပ်ကို သီးခြား စီစဉ်ပေးထားသည့် worker pool များတွင် လည်ပတ်စေပြီး၊ လိုအပ်သည့် attention state ကို ထို pool များအကြား လွှဲပြောင်းပေးသည့် serving ဗိသုကာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** prefill နှင့် decode သည် hardware အပေါ် ဖိအား သက်ရောက်ပုံ မတူညီကြသည်။ ထို့ကြောင့် သီးခြား pool များသည် တစ်ခုတည်းသော queue တွင် ယှဉ်ပြိုင်ရမည့်အစား မိမိတို့၏ bottleneck အလိုက် အရွယ်အစား သတ်မှတ်နိုင်၊ schedule လုပ်နိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** disaggregation သည် runtime အဆင့်များကို ခွဲထုတ်သည်။ အဆင့်တစ်ခုအတွင်း model တစ်ခုကို tensor သို့မဟုတ် pipeline-parallel shard များအဖြစ် ခွဲသည် မဟုတ်ပါ။
- **လက်တွေ့:** state လွှဲပြောင်းမှု ကုန်ကျစရိတ်ကို တိုင်းတာရမည်၊ request များကို ကိုက်ညီသည့် model version များမှတစ်ဆင့် route လုပ်ရမည်၊ pool တစ်ခုချင်းကို ၎င်း၏ demand signal မှ scale လုပ်ရမည်၊ အဆင့်များအကြား failure recovery ကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Prefill, Decode Phase, Model Serving, Goodput
- **Learn it:** [Disaggregated Prefill and Decode](../phases/17-infrastructure-and-production/17-disaggregated-prefill-decode/)
- **English (source):** A serving architecture that runs prefill and decode work in separately provisioned worker pools and transfers the required attention state between them. Prefill and decode stress hardware differently, so independent pools can be sized and scheduled for their own bottlenecks instead of competing in one queue.

### Dynamic Batching

**မြန်မာ:** လိုက်လျောညီထွေ batch ဖွဲ့ခြင်း (dynamic batching)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** queue တွင် စောင့်နေသည့် request များမှ inference batch များကို ကိုက်ညီသည့် shape၊ အများဆုံး အရွယ်အစား၊ priority နှင့် ခွင့်ပြုထားသည့် queue ကြာချိန် (queue delay) အလိုက် ဖွဲ့စည်းသည့် runtime policy ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** request များကို အတွဲလိုက် စုခြင်းသည် hardware အသုံးချမှုကို တိုးတက်စေနိုင်သည်။ သို့သော် traffic ကျဲပါးသည့်အခါ သို့မဟုတ် request များ သိသိသာသာ ကွာခြားသည့်အခါ batch အတွက် စောင့်ခြင်းသည် latency ကို ပိုဆိုးစေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** dynamic batching သည် queue တွင် ရှိသည့် အလုပ်များမှ batch များကို စုစည်းသည်။ continuous batching သည် autoregressive generation လည်ပတ်နေစဉ်အတွင်း batch ၏ အဖွဲ့ဝင်များကို ပြောင်းလဲသည်။
- **လက်တွေ့:** တိုင်းတာထားသည့် latency ပန်းတိုင်များမှ queue-delay နှင့် batch ကန့်သတ်ချက်များကို သတ်မှတ်ရမည်၊ မကိုက်ညီသည့် request shape များကို ခွဲထားရမည်၊ လက်တွေ့ ရောက်ရှိသည့် နှုန်းများ (arrival rate) တွင် throughput နှင့် tail latency ကို နှိုင်းယှဉ်ရမည်။
- **ဆက်စပ် term များ:** Admission Control, Continuous Batching, Saturation, Tail Latency
- **Learn it:** [vLLM Serving Internals](../phases/17-infrastructure-and-production/04-vllm-serving-internals/)
- **English (source):** A runtime policy that forms inference batches from queued requests according to compatible shapes, maximum size, priority, and allowed queue delay. Grouping requests can improve hardware utilization, but waiting for a batch can make latency worse when traffic is sparse or requests differ sharply.

### Expert Parallelism

**မြန်မာ:** expert များကို device များအကြား ခွဲဝေခြင်း (expert parallelism)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** mixture-of-experts subnetwork များကို device များအကြား ဖြန့်ဝေပြီး၊ token တစ်ခုချင်း ရွေးချယ်ထားသည့် expert များကို လက်ခံဆောင်ရွက်သည့် device များဆီသို့ ၎င်း token ၏ activation များကို route လုပ်ပေးခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ကျဲပါးသည့် (sparse) expert များသည် token တိုင်းအတွက် expert တိုင်းကို လည်ပတ်စေခြင်း မပြုဘဲ model စွမ်းရည်ကို တိုးမြှင့်ပေးသည်။ သို့သော် routing သည် communication၊ load-balance နှင့် placement ကန့်သတ်ချက်များကို ဖြစ်ပေါ်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** expert parallelism သည် router က ရွေးချယ်သည့် expert များကို ခွဲဝေသည်။ tensor parallelism သည် layer များအတွင်းရှိ tensor operation များကို ခွဲဝေသည်။
- **လက်တွေ့:** expert အလိုက် token ဖြန့်ဝေမှုကို တိုင်းတာရမည်၊ communication bandwidth ကို စီစဉ်ပေးရမည်၊ overflow ကို တမင်တကာ ကန့်သတ်ရမည် သို့မဟုတ် route လုပ်ရမည်၊ traffic သည် expert လိုအပ်ချက်ကို မညီမျှစွာ ဖြစ်ပေါ်စေသည့်အခါ အရည်အသွေးကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** MoE (Mixture of Experts), Tensor Parallelism, Pipeline Parallelism, Model Serving
- **Learn it:** [Mixture of Experts](../phases/07-transformers-deep-dive/11-mixture-of-experts/)
- **English (source):** Distributing mixture-of-experts subnetworks across devices and routing each token's activations to the devices that host its selected experts. Sparse experts increase model capacity without executing every expert for every token, but routing introduces communication, load-balance, and placement constraints.

### FlashAttention

**မြန်မာ:** မြန်မာလို တိုက်ရိုက် ခေါ်ဝေါ်မှု မရှိ — attention တွက်ချက်မှုကို tile ခွဲ၍ memory လွှဲပြောင်းမှု လျှော့ချသည့် kernel

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** accelerator memory အလွှာများအကြား လွှဲပြောင်းမှုများကို လျှော့ချရန် တွက်ချက်မှုကို tile များအဖြစ် ခွဲ၍ လုပ်ဆောင်သည့် တိကျသည့် (exact) attention algorithm ဖြစ်သည်။ attention matrix အပြည့်ကို high-bandwidth memory တွင် အမှန်တကယ် ဖန်တီးထားရန် (materialization) မလိုအပ်စေပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** အထူးသဖြင့် ရှည်လျားသည့် sequence များတွင် attention သည် ဂဏန်း တွက်ချက်မှုထက် memory လှုပ်ရှားမှုကြောင့် ကန့်သတ်ခံရနိုင်သည်။ ထို့ကြောင့် IO ကို သိသည့် kernel သည် အသုံးဝင်သည့် အမြန်နှုန်းနှင့် memory စွမ်းရည်ကို တိုးတက်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** FlashAttention သည် attention တွက်ချက်သည့် နည်းလမ်းကို ပြောင်းလဲသည်။ ၎င်း ရည်မှန်းသည့် သင်္ချာ attention ရလဒ်ကို မပြောင်းလဲပါ။ KV caching နှင့် quantization တို့နှင့် သီးခြား ဖြစ်သည်။
- **လက်တွေ့:** model ၏ shape၊ mask၊ dtype နှင့် hardware တို့ ထောက်ပံ့သည့် kernel ကို အသုံးပြုရမည်၊ ဂဏန်း ခံနိုင်မှု အတိုင်းအတာ (numerical tolerance) ကို စစ်ဆေးရမည်၊ paper ရလဒ်ကို ပုံသေ multiplier အဖြစ် ကိုးကားမည့်အစား end-to-end latency ကို benchmark လုပ်ရမည်။
- **ဆက်စပ် term များ:** Attention, Self-Attention, KV Cache, Mixed Precision
- **Learn it:** [KV Cache and Flash Attention](../phases/07-transformers-deep-dive/12-kv-cache-flash-attention/)
- **English (source):** An exact attention algorithm that tiles the computation to reduce transfers between accelerator memory levels while avoiding materialization of the full attention matrix in high-bandwidth memory. Attention can be limited by memory movement rather than arithmetic, especially for long sequences, so an IO-aware kernel can improve usable speed and memory efficiency.

### Goodput

**မြန်မာ:** ဝန်ဆောင်မှု သတ်မှတ်ချက် ပြည့်မီသည့် throughput (goodput)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် workload တစ်ခုအောက်တွင် သတ်မှတ်ထားသည့် ဝန်ဆောင်မှု ကန့်သတ်ချက်များ — ဥပမာ time-to-first-token နှင့် per-token latency ပန်းတိုင် နှစ်ခုလုံး — ပြည့်မီသည့် ပြီးစီးသွားသည့် request များ၏ နှုန်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ကုန်ကြမ်း throughput မြင့်တက်နေစဉ် အသုံးပြုသူများသည် နှေးကွေးသည့် request များကို ပိုမို ကြုံတွေ့နိုင်သည်။ goodput သည် ဝန်ဆောင်မှု သဘောတူညီချက် ပြည့်မီသည့် အလုပ်ကိုသာ ရေတွက်သည်။
- **မကြာခဏ ရောထွေးမှု:** goodput သည် ပြီးစီးသည့် throughput အားလုံး မဟုတ်သလို၊ model တစ်ခု၏ အားလုံးအတွက် တူညီသည့် ဂုဏ်သတ္တိလည်း မဟုတ်ပါ။ ၎င်းသည် workload နှင့် အောင်မြင်မှု သတ်မှတ်ချက်များအပေါ် မူတည်သည်။
- **လက်တွေ့:** request ဖြန့်ဝေမှု ပုံစံနှင့် latency သတ်မှတ်ချက်များကို ကြေညာရမည်၊ ကိုက်ညီသည့် ပြီးစီးမှုများကိုသာ ရေတွက်ရမည်၊ စုစုပေါင်း နှုန်းဘေးတွင် percentile များကို ဖော်ပြရမည်၊ မတူညီသည့် ပန်းတိုင်များအောက်ရှိ စနစ်များကို နှိုင်းယှဉ်ခြင်းကို ရှောင်ရမည်။
- **ဆက်စပ် term များ:** Service Level Objective (SLO), Time to First Token (TTFT), Time per Output Token (TPOT), Cost per Successful Task
- **Learn it:** [Inference Metrics and Goodput](../phases/17-infrastructure-and-production/08-inference-metrics-goodput/)
- **English (source):** The rate of completed requests that satisfy defined service constraints, such as both time-to-first-token and per-token latency objectives, under a stated workload. Raw throughput can rise while users experience more slow requests. Goodput counts only work that meets the service contract.

### Inter-Token Latency (ITL)

**မြန်မာ:** token များအကြား latency (inter-token latency)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** request တစ်ခုအတွက် output token နှစ်ခု ဆက်တိုက် ရောက်ရှိသည့် အချိန် အစီအစဉ် နှစ်ခုအကြား ကြာချိန် ဖြစ်သည်။ ပထမမဟုတ်သည့် output token တစ်ခုအတွက် `t_i - t_(i-1)` ဟု တွက်ချက်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** token ကြား ကွာဟမှု တစ်ခုချင်းသည် decode ရပ်တန့်မှုများနှင့် streaming တုန်ခါမှုကို ဖော်ထုတ်ပေးသည်။ request တစ်ခုချင်း ပျှမ်းမျှက ထို အချက်များကို ဖုံးကွယ်နိုင်သည် — အထူးသဖြင့် batching၊ preemption သို့မဟုတ် ရောနှော workload များအောက်တွင် ဖြစ်သည်။
- **မကြာခဏ ရောထွေးမှု:** ITL သည် ဆက်တိုက် token များအကြား ကြားကာလ တစ်ခု ဖြစ်သည်။ time per output token သည် ထို ကြားကာလများ၏ request တစ်ခုချင်း ပျှမ်းမျှ ဖြစ်ပြီး၊ time to first token သည် streaming မစမီ စောင့်ချိန်ကို ဖုံးလွှမ်းသည်။
- **လက်တွေ့:** ပထမ token နောက်ပိုင်း ကြားကာလ တစ်ခုချင်းကို ၎င်း၏ request နှင့် token နေရာ (position) နှင့်အတူ မှတ်တမ်းတင်ရမည်၊ ထို့နောက် request နယ်နိမိတ်များကို ရောစပ်ပစ်ခြင်း မပြုဘဲ workload၊ output အရှည်နှင့် concurrency အလိုက် ဖြန့်ဝေမှု ပုံစံများကို ဖော်ပြရမည်။
- **ဆက်စပ် term များ:** Time per Output Token (TPOT), Time to First Token (TTFT), Decode Phase, Tail Latency
- **Learn it:** [Inference Metrics and Goodput](../phases/17-infrastructure-and-production/08-inference-metrics-goodput/)
- **English (source):** The elapsed time between two consecutive output-token arrival events for one request, calculated as `t_i - t_(i-1)` for an output token after the first. Individual gaps expose decode stalls and streaming jitter that a per-request average can hide, especially under batching, preemption, or mixed workloads.

### Model Serving

**မြန်မာ:** model ဝန်ဆောင်မှု (model serving)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** version သတ်မှတ်ထားသည့် model artifact များကို ဖွင့်တင်ပေးပြီး၊ inference request များကို လက်ခံကာ၊ လည်ပတ်မှုကို schedule လုပ်ပြီး၊ အရင်းအမြစ်များကို စီမံကာ၊ လုပ်ငန်း သဘောတူညီချက် (operational contract) အောက်တွင် ရလဒ်များကို ပြန်ပေးသည့် runtime နှင့် API အလွှာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** စွမ်းရည်ကောင်းသည့် model တစ်ခုသည် queueing၊ batching၊ placement၊ versioning၊ cancellation နှင့် ဖြေကြားမှု နယ်နိမိတ်များကို အင်ဂျင်နီယာ နည်းဖြင့် ရှင်းလင်းစွာ မလုပ်ဆောင်ပါက ယုံကြည်မရသည့် ထုတ်ကုန် ဖြစ်စေနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** model serving သည် inference တစ်ခါ ခေါ်ခြင်းထက် ပိုကျယ်ပြန့်သည်။ retrieval၊ tool၊ policy နှင့် အသုံးပြုသူ အခြေအနေ (user state) ပါဝင်သည့် အပလီကေးရှင်း တစ်ခုလုံးထက် ကျဉ်းမြောင်းသည်။
- **လက်တွေ့:** model နှင့် tokenizer version များကို pin လုပ်ရမည်၊ request ကန့်သတ်ချက်များကို စစ်ဆေးရမည်၊ readiness နှင့် latency signal များကို ဖော်ထုတ်ရမည်၊ concurrency ကို ထိန်းချုပ်ရမည်၊ production traffic မလွှဲမီ rollback ကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Inference, Model Router, Autoscaling, Observability
- **Learn it:** [Self-Hosted Serving Selection](../phases/17-infrastructure-and-production/28-self-hosted-serving-selection/)
- **English (source):** The runtime and API layer that loads versioned model artifacts, accepts inference requests, schedules execution, manages resources, and returns results under an operational contract. A capable model can still produce an unreliable product when queueing, batching, placement, versioning, cancellation, and response boundaries are not engineered explicitly.

### Paged KV Cache

**မြန်မာ:** page ခွဲ KV cache (paged KV cache)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** attention state ကို ပုံသေ အရွယ်အစား block များတွင် သိမ်းဆည်းပြီး၊ logical sequence နေရာများကို physical block များသို့ map လုပ်ပေးသည့် KV-cache memory manager ဖြစ်သည်။ sequence တစ်ခုချင်းအတွက် ဆက်တိုက် (contiguous) allocation တစ်ခုတည်း လိုအပ်ခြင်း မရှိပါ။
- **အရေးပါသည့် အကြောင်းရင်း:** sequence အရှည် မတူညီမှုသည် fragmentation နှင့် ခန့်မှန်းမရသည့် ကြီးထွားမှုကို ဖြစ်ပေါ်စေသည်။ ထို့ကြောင့် block အခြေခံ allocation သည် အသုံးဝင်သည့် memory ကို တိုးတက်စေပြီး ပြောင်းလွယ်သည့် sharing ကို ဖြစ်နိုင်စေသည်။
- **မကြာခဏ ရောထွေးမှု:** paged KV cache သည် runtime ရှိ attention-state memory ကို စီမံသည်။ model parameter များကို disk သို့ ရွှေ့သည် မဟုတ်သလို၊ model ၏ သင်တန်းပေးထားသည့် context limit ကို တိုးချဲ့သည် လည်း မဟုတ်ပါ။
- **လက်တွေ့:** workload တိုင်းတာမှုများမှ block size ကို ရွေးရမည်၊ allocation နှင့် eviction ကို ခြေရာခံရမည်၊ request များအကြား state ကို သီးခြားထားရမည်၊ memory ဖိအားအောက်တွင် cancellation နှင့် prefix sharing ကို စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** KV Cache, Prefix Caching, Context Window, Model Serving
- **Learn it:** [vLLM Serving Internals](../phases/17-infrastructure-and-production/04-vllm-serving-internals/)
- **English (source):** A KV-cache memory manager that stores attention state in fixed-size blocks and maps logical sequence positions to physical blocks instead of requiring one contiguous allocation per sequence. Variable sequence lengths create fragmentation and unpredictable growth, so block-based allocation can improve usable memory and enable flexible sharing.

### Pipeline Parallelism

**မြန်မာ:** pipeline အလိုက် ခွဲဝေခြင်း (pipeline parallelism)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ဆက်တိုက် လိုက်နာရသည့် (sequential) model layer အုပ်စုများကို device များအကြား ပိုင်းခြားပြီး၊ microbatch များ သို့မဟုတ် request များကို ထို အဆင့်များမှတစ်ဆင့် pipeline တစ်ခုကဲ့သို့ ရွှေ့ပေးခြင်း ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** device တစ်ခု၏ memory ထက် ကြီးသည့် model များကို ထည့်သွင်းနိုင်စေသည်။ သို့သော် အဆင့်များ မညီမျှမှု (stage imbalance)၊ pipeline bubble၊ activation လွှဲပြောင်းမှုများနှင့် failure ညှိနှိုင်းမှုတို့သည် အသုံးဝင်သည့် စွမ်းဆောင်ရည်ကို သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** pipeline parallelism သည် layer များကို အတိမ်အနက် (depth) အလိုက် ခွဲသည်။ tensor parallelism သည် layer တစ်ခုအတွင်းရှိ tensor operation များကို ခွဲသည်။
- **လက်တွေ့:** အဆင့် တစ်ခုချင်း၏ ကုန်ကျစရိတ်ကို ညီမျှစေရမည်၊ microbatch schedule ကို ရွေးရမည်၊ အားလပ်ချိန် (idle time) နှင့် interconnect traffic ကို တိုင်းတာရမည်၊ model နှင့် checkpoint partition metadata ကို version စနစ်ဖြင့် ထိန်းသိမ်းရမည်။
- **ဆက်စပ် term များ:** Tensor Parallelism, Expert Parallelism, Batch Size, Model Serving
- **Learn it:** [Scaling and Distributed Training](../phases/10-llms-from-scratch/05-scaling-distributed/)
- **English (source):** Partitioning sequential groups of model layers across devices and moving microbatches or requests through those stages as a pipeline. It lets models exceed one device's memory, but stage imbalance, pipeline bubbles, activation transfers, and failure coordination affect usable performance.

### Prefill

**မြန်မာ:** prefill (prompt ကို စီမံသည့် အစပိုင်း အဆင့်) — အခြား အမည် Prefill Phase

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** ပေးထားသည့် input token အားလုံးကို စီမံ၍ ၎င်းတို့၏ representation များနှင့် နောက်ဆက်တွဲ autoregressive generation အတွက် လိုအပ်သည့် attention state ကို ထုတ်လုပ်သည့် ကနဦး inference အဆင့် ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** prompt ပုံစံ (shape)၊ queueing နှင့် cache ပြန်သုံးမှုတို့သည် prefill ကုန်ကျစရိတ်ကို သက်ရောက်သည်။ prefill သည် decode နှင့် compute အတွက် ယှဉ်ပြိုင်ပုံ ကွာခြားသည်။ ထို့ကြောင့် ၎င်းသည် စတင်ချိန် latency နှင့် serving schedule များအပေါ် ပြင်းထန်စွာ သက်ရောက်သည်။
- **မကြာခဏ ရောထွေးမှု:** prefill သည် runtime ရှိ prompt-processing အဆင့် ဖြစ်သည်။ ပထမ ထုတ်လုပ်သည့် token ကိုယ်တိုင် မဟုတ်ပါ။ ပထမ token သည် prefill နှင့် queueing ပြီးဆုံးပြီးမှသာ ပေါ်လာသည်။
- **လက်တွေ့:** prompt token များနှင့် prefill latency ကို မှတ်တမ်းတင်ရမည်၊ queue ကြာချိန်နှင့် လည်ပတ်ချိန်ကို ခွဲထားရမည်၊ cache ရှိသည့် prefix နှင့် မရှိသည့် prefix ကို နှိုင်းယှဉ်ရမည်၊ ရှည်လျားသည့် prompt များကို တက်ကြွသည့် decode traffic ဘေးတွင် စမ်းသပ်ရမည်။
- **ဆက်စပ် term များ:** Decode Phase, KV Cache, Time to First Token (TTFT), Chunked Prefill
- **Learn it:** [Disaggregated Prefill and Decode](../phases/17-infrastructure-and-production/17-disaggregated-prefill-decode/)
- **English (source):** The initial inference stage that processes all supplied input tokens to produce their representations and the attention state required for subsequent autoregressive generation. Prompt shape, queueing, and cache reuse affect prefill cost, and prefill competes differently for compute than decode, so it strongly influences startup latency and serving schedules.

### Prefix Caching

**မြန်မာ:** prefix cache ပြန်သုံးခြင်း (prefix caching)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** တူညီပြီး သတ်မှတ်ချက် ပြည့်မီသည့် token prefix တစ်ခုအတွက် ထုတ်လုပ်ထားသည့် KV-cache block များကို request များအကြား ပြန်လည် အသုံးပြုခြင်း ဖြစ်သည်။ ထိုသို့ဖြင့် serving runtime သည် ထပ်ခါတလဲလဲ prefix တွက်ချက်မှုကို ကျော်လွှားနိုင်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** မျှဝေသည့် system instruction၊ template သို့မဟုတ် document များသည် prefill အလုပ်ကို အတော်အသင့် စားသုံးနိုင်သည်။ သို့သော် ပြန်သုံးမှုသည် token sequence များနှင့် cache သတ်မှတ်ချက် (eligibility) ကိုက်ညီသည့်အခါမှသာ အကျိုးရှိသည်။
- **မကြာခဏ ရောထွေးမှု:** prefix caching သည် တိကျသည့် token prefix များအတွက် runtime attention state ကို ပြန်သုံးသည်။ prompt caching သည် ပိုမို ကျယ်ပြန့်သည့် provider သို့မဟုတ် အပလီကေးရှင်း သဘောတူညီချက် ဖြစ်ပြီး၊ semantic caching သည် ဆင်တူသည့် request တစ်ခုအတွက် ယခင် ရလဒ်ကို ပြန်သုံးသည်။
- **လက်တွေ့:** တည်ငြိမ်သည့် token များကို request သီးသန့် အကြောင်းအရာ မတိုင်မီ ထားရမည်၊ cache အမှတ်အသားတွင် model နှင့် tokenizer version များ ထည့်ရမည်၊ tenant ဆိုင်ရာ state ကို သီးခြားထားရမည်၊ hit rate ကို စောင့်ကြည့်ရမည်၊ eviction ကို ပုံမှန် ဖြစ်ရိုးဖြစ်စဉ်အဖြစ် သတ်မှတ်ရမည်။
- **ဆက်စပ် term များ:** Prompt Cache, Semantic Cache, KV Cache, Paged KV Cache
- **Learn it:** [Inference Optimization](../phases/10-llms-from-scratch/12-inference-optimization/)
- **English (source):** Reusing KV-cache blocks produced for an identical eligible token prefix across requests so the serving runtime can skip repeated prefix computation. Shared system instructions, templates, or documents can consume substantial prefill work, but reuse only helps when token sequences and cache eligibility match.

### Tensor Parallelism

**မြန်မာ:** tensor တွက်ချက်မှုကို device များအကြား ခွဲဝေခြင်း (tensor parallelism)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** model layer တစ်ခုအတွင်းရှိ tensor operation များကို device များအကြား ပိုင်းခြားခြင်း ဖြစ်သည်။ layer တွက်ချက်မှုအတွင်း ကျသွားသည့် ရလဒ် အစိတ်အပိုင်းများကို collective communication ဖြင့် ပေါင်းစပ်ပေးသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** layer တစ်ခုသည် device အတော်များများ၏ memory နှင့် compute ကို အသုံးပြုနိုင်စေသည်။ သို့သော် interconnect သို့မဟုတ် partition မသင့်လျော်သည့်အခါ အကြိမ်များစွာ communication လုပ်ရခြင်းက လွှမ်းမိုးနိုင်သည်။
- **မကြာခဏ ရောထွေးမှု:** tensor parallelism သည် layer များအတွင်းရှိ အလုပ်ကို ခွဲသည်။ pipeline parallelism သည် layer အုပ်စု မတူညီသည့်အရာများကို device မတူညီသည့် နေရာများတွင် ထားသည်။
- **လက်တွေ့:** partition dimension များကို model shape များနှင့် ကိုက်ညီစေရမည်၊ collective traffic ကို benchmark လုပ်ရမည်၊ rank များကို အမြန်သည့် interconnect တွင် ထားရမည်၊ sharding layout ကို checkpoint နှင့် serving configuration များနှင့်အတူ မှတ်တမ်းတင်ရမည်။
- **ဆက်စပ် term များ:** Tensor, Pipeline Parallelism, Expert Parallelism, Parameter
- **Learn it:** [Scaling and Distributed Training](../phases/10-llms-from-scratch/05-scaling-distributed/)
- **English (source):** Partitioning tensor operations within a model layer across devices, with collective communication combining partial results during the layer computation. It lets one layer use memory and compute from several devices, but frequent communication can dominate when the interconnect or partition is unsuitable.

### Time per Output Token (TPOT)

**မြန်မာ:** output token တစ်ခုချင်း ကြာချိန် (TPOT)

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** `N > 1` output token ရှိသည့် request တစ်ခုအတွက် ပထမ token နောက်ပိုင်း ကြားကာလများ၏ ပျှမ်းမျှ — `(t_N - t_1) / (N - 1)` ဖြစ်သည်။ ထို့နောက် စနစ် ဖြန့်ဝေမှု ပုံစံများသည် ထို request တစ်ခုချင်း ပျှမ်းမျှများကို စုစည်းသည်။
- **အရေးပါသည့် အကြောင်းရင်း:** အသုံးပြုသူသည် ပထမ token ကို လျင်မြန်စွာ ရရှိသော်လည်း ကျန် အဖြေသည် နှေးကွေးစွာ စီးဆင်းနိုင်သည်။ ထို့ကြောင့် စတင်ချိန် latency တစ်ခုတည်းက generation တုံ့ပြန်မှုကို ဖော်ပြပေးနိုင်သည် မဟုတ်ပါ။
- **မကြာခဏ ရောထွေးမှု:** TPOT သည် request တစ်ခုချင်း ပျှမ်းမျှ ဖြစ်သည်။ inter-token latency တစ်ခုချင်းသည် ဆက်တိုက် token နှစ်ခုအကြား ကွာဟချက် တစ်ခု ဖြစ်ပြီး၊ time to first token သည် output မစမီ စောင့်ချိန်ကို ပါဝင်သည်။
- **လက်တွေ့:** TPOT ကို request တစ်ခုချင်းအတွက် သီးခြား တွက်ရမည်၊ output အရှည်နှင့် concurrency အလိုက် request များအကြား percentile များကို ဖော်ပြရမည်၊ token ကြားကာလ အားလုံးကို ရောစပ်ပစ်ခြင်း သို့မဟုတ် tokenizer နှင့် တိုင်းတာမှု နယ်နိမိတ် မတူညီသည့် စနစ်များကို နှိုင်းယှဉ်ခြင်းကို ရှောင်ရမည်။
- **ဆက်စပ် term များ:** Decode Phase, Time to First Token (TTFT), Streaming, Goodput
- **Learn it:** [Inference Metrics and Goodput](../phases/17-infrastructure-and-production/08-inference-metrics-goodput/)
- **English (source):** For one request with `N > 1` output tokens, the average post-first-token interval: `(t_N - t_1) / (N - 1)`. System distributions then aggregate those per-request averages. Users can receive the first token quickly while the rest of the answer streams slowly, so startup latency alone does not describe generation responsiveness.

### Tokens per Second (TPS)

**မြန်မာ:** တစ်စက္ကန့် ထုတ်လုပ်သည့် token အရေအတွက် (TPS) — အခြား အမည် output token throughput

- **ဆိုလိုသည့် အဓိပ္ပာယ်:** သတ်မှတ်ထားသည့် နယ်ပယ် (scope) နှင့် workload တစ်ခုအောက်တွင် serving စနစ် တစ်ခုသည် အချိန် တစ်ယူနစ်အတွင်း output token မည်မျှ ထုတ်လုပ်သည်ကို ဖော်ပြသည့် throughput အတိုင်းအတာ ဖြစ်သည်။
- **အရေးပါသည့် အကြောင်းရင်း:** ၎င်းသည် စတင်ချိန် latency ကို ဖြည့်စွက်ပေးသည် — output စပြီးနောက် generation မည်မျှ မြန်သည်ကို ပြသပြီး၊ ဝန်အောက်တွင် serving မည်သို့ ပြုမူသည်ကို ဖော်ပြသည်။
- **မကြာခဏ ရောထွေးမှု:** TPS ကို tokenizer၊ workload၊ အရည်အသွေး သတ်မှတ်ချက် သို့မဟုတ် တိုင်းတာမှု နယ်နိမိတ် မတူညီသည့် စနစ်များအကြား တိုက်ရိုက် နှိုင်းယှဉ်၍ မရပါ။
- **လက်တွေ့:** TPS သည် request တစ်ခုချင်းအတွက် ဟုတ်သည် သို့မဟုတ် စုစုပေါင်း ဟုတ်သည်ကို ဖော်ပြရမည်၊ prefill ကို ဖယ်ထားသည် သို့မဟုတ် သီးခြား ဖော်ပြရမည်၊ batch၊ concurrency၊ sequence အရှည်များ၊ hardware နှင့် percentile latency ကို ဖော်ပြရမည်။
- **ဆက်စပ် term များ:** Time to First Token (TTFT), Streaming, Prefill, Observability
- **English (source):** A throughput measure reporting how many output tokens a serving system produces per unit time under a stated scope and workload. It complements startup latency by showing how quickly generation proceeds after output begins and how serving behaves under load.

## Self-check

1. Autoscaling သည် စွမ်းရည် ထပ်တိုးခြင်းသာ ဖြစ်သလား၊ မည်သည့် အချက်များကို ထည့်သွင်း စဉ်းစားရမည်နည်း။
2. Continuous Batching နှင့် Dynamic Batching ကွာခြားချက်သည် အဘယ်နည်း။
3. Chunked Prefill သည် model ၏ context window ကို ပြောင်းလဲသလား။
4. Time to First Token (TTFT)၊ Inter-Token Latency (ITL) နှင့် Time per Output Token (TPOT) တို့ မည်သို့ ကွာခြားသနည်း။
5. Goodput နှင့် throughput ကွာခြားချက်ကား အဘယ်နည်း။

<details>
<summary>အဖြေများ</summary>

1. Autoscaling သည် စွမ်းရည်ကို ထပ်တိုး သို့မဟုတ် လျှော့ချခြင်းသာ ဖြစ်သည်။ overload ဖြစ်နေသည့် dependency ကို ပိုမြန်စေသည် မဟုတ်သလို၊ hardware ကို အချိန်မီ ရရှိမည်ဟု အာမခံသည် မဟုတ်ပါ။ scaling ဆုံးဖြတ်ချက်များတွင် model ဖွင့်တင်ရန် ကြာချိန်၊ accelerator ရရှိနိုင်မှု၊ queueing နှင့် request ကုန်ကျစရိတ်တို့ကို ထည့်သွင်းရမည်။
2. Dynamic Batching သည် queue တွင် စောင့်နေသည့် request များမှ batch များကို ဖွဲ့စည်းသည် — လည်ပတ်မှု မစမီ အဆင့် ဖြစ်သည်။ Continuous Batching သည် autoregressive generation လည်ပတ်နေစဉ်အတွင်း iteration နယ်နိမိတ်များတွင် batch ၏ အဖွဲ့ဝင်များကို ထည့်/ဖယ် ပြောင်းလဲသည်။
3. မပြောင်းလဲပါ။ Chunked Prefill သည် prompt တွက်ချက်မှုကို schedule လုပ်သည့် ပုံစံကို ပြောင်းလဲခြင်း ဖြစ်သည်။ အသုံးပြုသူ၏ context ကို အဓိပ္ပာယ် သီးသန့်သည့် chunk များအဖြစ် ခွဲသည် မဟုတ်သလို၊ model ၏ context window ကို တိုးချဲ့သည် လည်း မဟုတ်ပါ။
4. TTFT သည် output မစမီ စောင့်ချိန်ကို ဖုံးလွှမ်းသည်။ ITL သည် ဆက်တိုက် output token နှစ်ခုအကြား ကြားကာလ တစ်ခု ဖြစ်သည်။ TPOT သည် request တစ်ခုချင်းအတွက် ထို ကြားကာလများ၏ ပျှမ်းမျှ ဖြစ်သည်။
5. Throughput သည် ပြီးစီးသည့် အလုပ် အားလုံးကို ရေတွက်နိုင်သည်။ Goodput သည် သတ်မှတ်ထားသည့် ဝန်ဆောင်မှု ကန့်သတ်ချက်များ — ဥပမာ TTFT နှင့် per-token latency ပန်းတိုင် — ပြည့်မီသည့် ပြီးစီးမှုများကိုသာ ရေတွက်သည်။ ထို့ကြောင့် goodput သည် workload နှင့် အောင်မြင်မှု သတ်မှတ်ချက်များအပေါ် မူတည်သည်။

</details>

## References

- Source glossary — https://aiengineeringfromscratch.com/glossary
- Source repository — https://github.com/rohitg00/ai-engineering-from-scratch (MIT)
- Lessons — [GPU Autoscaling on Kubernetes](../phases/17-infrastructure-and-production/03-gpu-autoscaling-kubernetes/), [vLLM Serving Internals](../phases/17-infrastructure-and-production/04-vllm-serving-internals/), [Disaggregated Prefill and Decode](../phases/17-infrastructure-and-production/17-disaggregated-prefill-decode/), [Inference Metrics and Goodput](../phases/17-infrastructure-and-production/08-inference-metrics-goodput/), [Self-Hosted Serving Selection](../phases/17-infrastructure-and-production/28-self-hosted-serving-selection/), [Mixture of Experts](../phases/07-transformers-deep-dive/11-mixture-of-experts/), [KV Cache and Flash Attention](../phases/07-transformers-deep-dive/12-kv-cache-flash-attention/), [Scaling and Distributed Training](../phases/10-llms-from-scratch/05-scaling-distributed/), [Inference Optimization](../phases/10-llms-from-scratch/12-inference-optimization/)
- Papers — [Orca](https://www.usenix.org/conference/osdi22/presentation/yu), [Sarathi-Serve](https://arxiv.org/abs/2403.02310), [DistServe](https://arxiv.org/abs/2401.09670), [PagedAttention](https://arxiv.org/abs/2309.06180), [FlashAttention](https://arxiv.org/abs/2205.14135), [Megatron-LM](https://arxiv.org/abs/1909.08053), [GPipe](https://arxiv.org/abs/1811.06965), [GShard](https://arxiv.org/abs/2006.16668), [SGLang](https://arxiv.org/abs/2312.07104)

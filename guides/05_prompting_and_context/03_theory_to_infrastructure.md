# 03 — သီအိုရီမှ ထုတ်လုပ်မှု အခြေခံအဆောက်အအုံသို့ (Theory to Infrastructure)

ဤစာတမ်းသည် နယ်ပယ် ၀၅ ၏ term ၁၅ ခုလုံးကို အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ပြန်လည် ဖတ်သည်။ prompting နှင့် context term တစ်ခုသည် စာတမ်းအတွင်း သီအိုရီ အဖြစ်သာ မကျန်ရပါ။ ၎င်းသည် GPU memory (prompt နှင့် cache)၊ compute (prefill)၊ latency (အထူးသဖြင့် TTFT)၊ throughput၊ တောင်းဆိုမှု တစ်ခုစီ၏ cost (cost per call) သို့မဟုတ် ထုတ်လုပ်မှု အခြေအနေတွင် ကျိုးပျက်သည့် အရာ အနက် တစ်ခုခုကို ရွေ့လျားစေသည်။ ရွေ့လျားသည့် ကိန်းဂဏန်း တစ်ခုစီသည် serving engineer နှင့် prompt author တို့ တုံ့ပြန်ရမည့် ဆုံးဖြတ်ချက် တစ်ခုစီနှင့် တွဲလျက် ရှိသည်။

နယ်ပယ် ၀၂ တွင် မော်ဒယ်၏ ဖွဲ့စည်းပုံသည် memory နှင့် compute ကို ဆုံးဖြတ်သည်ကို တွေ့ခဲ့ပြီး ဖြစ်သည်။ ဤနယ်ပယ်တွင် ထို မော်ဒယ်အား ပေးအပ်သည့် စာသားကိုယ်တိုင် ကုန်ကျစရိတ်၏ အရင်းအမြစ် ဖြစ်လာသည်။ prompt token တိုင်းသည် prefill compute ကို တိုးစေသည်၊ KV cache တွင် နေရာယူသည်၊ TTFT ကို ရွေ့စေသည်၊ ထို့ကြောင့် တောင်းဆိုမှု တစ်ခုစီ၏ စျေးနှုန်းကို တိုးစေသည်။ context window ကြီးမားခြင်းသည် ထို ကုန်ကျစရိတ်ကို ဖယ်ရှားပေးခြင်း မဟုတ်ပါ၊ ပိုမို သိမ်းဆည်းနိုင်စေခြင်းသာ ဖြစ်သည်။

ဤစာတမ်းရှိ ကိန်းဂဏန်း အားလုံးသည် `guides/05_prompting_and_context/scripts/` အောက်ရှိ Python script သုံးခုမှ ရရှိသည့် တန်ဖိုးများ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။ token အားလုံးသည် ဖော်ပြထားသည့် estimator `tokens = ceil(characters / 4)` မှ ရရှိသည့် ခန့်မှန်းတန်ဖိုး ဖြစ်သည်။ စျေးနှုန်း၊ prefill rate နှင့် overhead အားလုံးကို assumption အဖြစ် တိကျစွာ မှတ်သားထားသည်၊ ၎င်းတို့သည် vendor၊ GPU နှင့် region အလိုက် ကွာခြားသည့်အတွက် `တန်ဖိုးသည် အခြေအနေအလိုက် ကွာခြားသည်`။ ဤစာတမ်းသည် benchmark ရလဒ် များကို ဖော်ပြခြင်း မပြုပါ၊ ဖော်ပြသည့် တန်ဖိုး အားလုံးသည် ဖော်မြူလာ နှင့် ယူဆချက် (assumption) မှ တွက်ချက်ထားသည့် တန်ဖိုးများ ဖြစ်သည်။

## ၁။ ဝင်ရိုး ခြောက်ခု၏ ဝေါဟာရ သတ်မှတ်ချက်

နောက်ပိုင်း အပိုင်းများတွင် ဤဝေါဟာရ ခြောက်ခုကို တူညီသည့် အဓိပ္ပာယ်ဖြင့်သာ အသုံးပြုမည် ဖြစ်သည်။

**GPU memory (VRAM) — prompt နှင့် cache** — accelerator တစ်လုံး၏ memory ပေါ်တွင် တစ်ပြိုင်နက် နေရာယူသည့် byte ပမာဏ ဖြစ်သည်။ prompt token တိုင်းသည် prefill အဆင့်တွင် activation အဖြစ် နေရာယူပြီး ထိုနောက် key နှင့် value tensor အဖြစ် KV cache တွင် ဆက်လက် တည်ရှိသည်။ ပမာဏသည် prompt token၊ layer အရေအတွက်၊ head အရေအတွက်၊ head dimension နှင့် numerical format အပေါ် မှီခိုသည်။ ဥပမာ (ခ) တွင် ထို reference model သည် token တစ်လုံးလျှင် 0.500 MiB ဖြစ်သည်။

**compute (prefill FLOPs)** — prompt ကို ဖတ်သည့် prefill အဆင့်သည် sequence အတွင်း position အားလုံးကို တစ်ပြိုင်နက် တွက်ချက်နိုင်သည့် အဆင့် ဖြစ်သည်။ prompt token တိုးလျှင် prefill FLOPs အချိုးအစား တိုးသည်၊ ထို့ကြောင့် cache မမိသည့် prompt ရှည်တိုင်းသည် compute အရင်းအမြစ်ကို ဖိသည်။

**latency (TTFT)** — generation တောင်းဆိုမှု တင်သည့် အချိန်မှ ပထမဆုံး output token client ထံ ရောက်သည့် အချိန်အထိ ကာလ ဖြစ်သည်။ TTFT တွင် queueing၊ prefill (prompt processing)၊ cache အခြေအနေနှင့် network ဆိုင်ရာ နှောင့်နှေးမှု အားလုံး ပါဝင်သည်။ ဤတန်ဖိုးသည် အလုပ်ပမာဏ၏ linear function အဖြစ် တွက်နိုင်သည်၊ ဥပမာ (ဂ) တွင် ထို ဖော်မြူလာကို ပြထားသည်။

**throughput** — ယူနစ်အချိန်တစ်ခုအတွင်း ဆောင်ရွက်ပြီးစီးသည့် output token သို့မဟုတ် တောင်းဆိုမှု အရေအတွက် ဖြစ်သည်။ prompt တိုခြင်းနှင့် cache hit မြင့်ခြင်းသည် accelerator အချိန်ကို လျော့စေသည့်အတွက် တူညီသည့် hardware အောက်တွင် throughput ကို တိုးစေသည်။

**cost per call (input နှင့် output ခွဲခြား)** — တောင်းဆိုမှု တစ်ခုစီ၏ ကုန်ကျစရိတ် ဖြစ်သည်။ input token နှင့် output token တို့သည် စျေးနှုန်း မတူညီသည့်အတွက် နှစ်ခုကို ခွဲခြား တွက်ရမည်။ prompt token အပိုင်း သည်သာ prompt engineering နှင့် context engineering က ထိန်းချုပ်နိုင်သည့် အပိုင်း ဖြစ်သည်။

**production consequence** — ထို concept ကို လျစ်လျူရှုလျှင် deployment တွင် မည်သည့် အရာ ကျိုးပျက်မည်ကို ဆိုလိုသည်။ ဥပမာ context window ကို ကြော်ငြာ အရေအတွက်အတိုင်း အသုံးပြုလျှင် window ကျော်သည့် တောင်းဆိုမှုသည် quality ကျခြင်းဖြင့် မဟုတ်ဘဲ အလုံးအရင်း ကျရှုံးခြင်းဖြင့် ကျိုးပျက်သည်။

## ၂။ Master table — term ၁၅ ခုလုံး

| Term | primary axis | ကုန်ကျခြင်း / ချွေတာခြင်း | ရွေ့လျားသည့် ကိန်း | ထုတ်လုပ်မှု အကျိုးဆက် |
|---|---|---|---|---|
| Chain of Thought (CoT) | latency | output token အရေအတွက်ကို တိုးစေသည် | output tokens per call | reasoning transcript ရှည်လျှင် စုစုပေါင်း cost နှင့် ပြီးဆုံးချိန် တိုးသည် |
| Context Compression | GPU memory (prompt) | prompt token ကို လျှော့သည်၊ ဆုံးရှုံးမှု အန္တရာယ် ယူသည် | prompt tokens (24,000 ကို 8,000 သို့ ချုံ့လျှင် 16,000 လွတ်သည်) | ချုံ့လွန်းလျှင် အထောက်အထား ဆုံးရှုံး၍ အဖြေ မှား |
| Context Engineering | compute (prefill) | သက်ဆိုင်သည့် အထောက်အထားကိုသာ ထည့်သည် | prefill tokens | မလိုအပ်သည့် context သည် noise ဖြစ်၍ တိကျမှု ကျ |
| Context Window | GPU memory (prompt) | capacity အထက်ကန့်သတ်ချက် သတ်မှတ်သည် | maximum tokens (128,000) | window ကျော်လျှင် တောင်းဆိုမှု လုံးဝ ကျရှုံး |
| Few-Shot | GPU memory (prompt) | ဥပမာ တစ်ခုစီသည် prompt ကို တိုးစေသည် | example tokens (46 token/ဥပမာ in ဥပမာ (က)) | ဥပမာ များလျှင် cost နှင့် KV cache နှစ်ခုလုံး တိုး |
| In-Context Learning | compute (prefill) | parameter update မလိုဘဲ အပြုအမူ ရွေ့သည် | prompt tokens | demonstration ညံ့လျှင် ယုံကြည်စိတ်ချရမှု ကျ |
| Instruction Following | production consequence | format လိုက်နာလျှင် retry လျော့သည် | retry rate | format ချိုးဖောက်လျှင် downstream parse ကျိုးပျက် |
| Instruction Hierarchy | production consequence | ပဋိပက္ခ ဖြေရှင်းမှုကို သတ်မှတ်သည် | conflict resolution rate | hierarchy မရှိလျှင် prompt injection အန္တရာယ် တိုး |
| Lost in the Middle | compute | အထောက်အထား တည်နေရာကို ရွေးသည် | position of the key evidence | အလယ်ပိုင်း အထောက်အထား လျစ်လျူရှုခံရလျှင် အဖြေ မှား |
| Prompt Cache | latency (TTFT) | တည်ငြိမ်သည့် shared prefix ကို ပြန်သုံးသည် | cache hit rate (92.81% prefill saving in ဥပမာ (ခ)) | prefix မတည်ငြိမ်လျှင် cache မမိဘဲ cost တိုး |
| Prompt Engineering | throughput | output format ကို တည်ငြိမ်စေသည် | parse success rate | wording သည် ပျောက်နေသည့် အထောက်အထားကို ဖြည့်မပေး |
| Prompt Sensitivity | production consequence | မူကွဲများအကြား ကွဲပြားမှုကို ဖော်ထုတ်သည် | variance across prompt variants | wording ပြောင်းလျှင် regression ဖြစ် |
| System Prompt | GPU memory (prompt) | prefix ကို တည်ငြိမ်စွာ ထားရန် နေရာ ယူသည် | prefix tokens (69 မှ 195 in ဥပမာ (က)) | system prompt သည် လျှို့ဝှက် နယ်နိမိတ် မဟုတ် |
| Token Budget | compute (prefill) | အစိတ်အပိုင်း အလိုက် token ကို ခွဲဝေသည် | used ÷ window (59,356 ÷ 128,000) | budget မရှိလျှင် window ပြည့်ချိန် တောင်းဆိုမှု ကျရှုံး |
| Zero-Shot | GPU memory (prompt) | ဥပမာ token ကို လုံးဝ မကုန်သည် | prompt tokens (99 in ဥပမာ (က)) | ရှုပ်ထွေးသည့် task တွင် ဥပမာ မရှိလျှင် format လွဲနိုင် |

## ၃။ term အလိုက် ရှင်းလင်းချက်

term များကို မိသားစု လေးခုဖြင့် စုစည်းထားသည် — (က) တောင်းဆိုမှု နည်းလမ်းများ၊ (ခ) context နေရာ နှင့် ရွေးချယ်မှု၊ (ဂ) ညွှန်ကြားချက် အခွင့်အာဏာ နှင့် လိုက်နာမှု၊ (ဃ) လက်တွေ့ အပြုအမူ နှင့် ကန့်သတ်ချက်။ ဤအုပ်စုခွဲမှုသည် အပိုင်း ၂ ၏ ဇယားနှင့် တိုက်ရိုက် ကိုက်ညီသည်။

### မိသားစု (က) — တောင်းဆိုမှု နည်းလမ်းများ (prompting technique)

#### Prompt Engineering

Prompt Engineering သည် မော်ဒယ်အား ပေးအပ်သည့် ညွှန်ကြားချက်၊ ဥပမာ၊ ကန့်သတ်ချက်နှင့် output လိုအပ်ချက်ကို စီစဉ် တည်ဆောက်ခြင်း ဖြစ်သည်။ ၎င်း၏ ပထမဆုံး တိုင်းတာနိုင်သည့် အကျိုးဆက်သည် output format တည်ငြိမ်မှု ဖြစ်သည်၊ format ချိုးဖောက်မှု တိုင်းသည် retry ဖြစ်စေပြီး accelerator အချိန် ထပ်ကုန်စေသည့်အတွက် parse success rate သည် throughput အပေါ် တိုက်ရိုက် သက်ရောက်သည်။ ဥပမာ (က) တွင် task instruction ၁၃ token နှင့် output format ပါဝင်သည့် system prompt ၆၉ token ဖြစ်ပြီး base တောင်းဆိုမှုသည် USD 0.002097 per call ဖြစ်သည်။ prompt ကို ရေးသည့် အလုပ်သည် output token ကို ထိန်းချုပ်ခြင်းဖြင့် output စျေးနှုန်း (USD 15.00 per 1e6) အပေါ်လည်း သက်ရောက်သည်။ သို့သော် prompt ၏ စကားလုံး ရွေးချယ်မှုသည် ပျောက်ဆုံးနေသည့် အထောက်အထား၊ မလုံခြုံသည့် permission၊ ညံ့ဖျင်းသည့် tool contract သို့မဟုတ် မရှိသည့် evaluation တို့ကို ဖြည့်ဆည်းပေးနိုင်ခြင်း မရှိပါ။ ထို့ကြောင့် Prompt Engineering ကို Context Engineering နှင့် တွဲဖက်၍သာ အားကိုးရမည်။

#### Zero-Shot

Zero-Shot သည် လက်ရှိ input တွင် task-specific demonstration များ မထည့်ဘဲ ညွှန်ကြားချက်များ သို့မဟုတ် task ဖွဲ့စည်းမှုဖြင့် task တစ်ခုကို လုပ်ဆောင်ခြင်း ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ၎င်းသည် အကုန်အကျ အနည်းဆုံး ရွေးချယ်မှု ဖြစ်သည် — ဥပမာ token အားလုံး လွတ်သည့်အတွက် prompt တိုသည်၊ KV cache နည်းသည်၊ TTFT တိုသည်။ ဥပမာ (က) တွင် base (system + task + question) တောင်းဆိုမှုသည် ၉၉ input token ဖြစ်ပြီး ဥပမာ တစ်ခုမျှ မပါဝင်ပါ။ သို့သော် ၎င်းသည် မော်ဒယ်တွင် သက်ဆိုင်သည့် pretraining၊ instruction tuning၊ tool သို့မဟုတ် ရယူထားသည့် context မရှိခဲ့သည်ဟု မဆိုလိုပါ၊ zero-shot သည် context အတွင်း demonstration မပါခြင်းကိုသာ ဖော်ပြသည်။ ရှုပ်ထွေးသည့် format လိုအပ်သည့် task များတွင် ဥပမာ မရှိခြင်းသည် output format လွဲမှားမှုကို ဖြစ်စေနိုင်သည့်အတွက် instruction following ကို သီးခြား တိုင်းတာရမည်။

#### Few-Shot

Few-Shot သည် ပစ်မှတ် input မတိုင်မီ ဥပမာ အနည်းငယ်ကို ထည့်သွင်း၍ မော်ဒယ်က လိုလားသည့် task၊ format သို့မဟုတ် ဆုံးဖြတ်ချက် နယ်နိမိတ်ကို ကောက်ချက်ချစေသည့် in-context learning ဖြစ်သည်။ ဤနည်းလမ်းသည် ဖွဲ့စည်းပုံ အရ အရိုးရှင်းဆုံး ကုန်ကျစရိတ် ကိန်းစား တစ်ခုကို မိတ်ဆက်ပေးသည် — ဥပမာ တိုင်းသည် တောင်းဆိုမှု တိုင်း၏ prompt တွင် ပြန်လည် ပါဝင်သည်။ ဥပမာ (က) တွင် ဥပမာ တစ်ခုလျှင် ၄၆ input token ဖြစ်ပြီး ဥပမာ တစ်ခုသည် USD 0.000138 per call တိုးစေသည်၊ ဥပမာ သုံးခုသည် USD 0.000414 per call တိုးစေသည်။ ထို token အားလုံးသည် KV cache တွင်လည်း နေရာယူသည့်အတွက် ဥပမာ အရေအတွက်သည် memory၊ TTFT နှင့် cost သုံးခုလုံးကို တစ်ပြိုင်နက် ရွေ့စေသည်။ ဥပမာ အရေအတွက် တစ်သမတ်တည်း ထက် ဥပမာ၏ အရည်အသွေးနှင့် လွှမ်းခြုံမှုက ပို၍ အရေးပါသည်၊ ညံ့ဖျင်းသည့် သို့မဟုတ် ဆန့်ကျင်နေသည့် demonstration များသည် ယုံကြည်စိတ်ချရမှုကို လျှော့ချနိုင်သည်။

#### Chain of Thought (CoT)

Chain of Thought သည် ဖြေဆိုချက် မထုတ်လုပ်မီ task တစ်ခုကို အစိတ်အပိုင်းများ ခွဲခြမ်းရန် အသုံးပြုသည့် ကြားခံ ကျိုးကြောင်းဆင်ခြင်မှု ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ၎င်းသည် output token အရေအတွက်ကို တိုးစေသည့် တောင်းဆိုမှု ဖြစ်သည့်အတွက် output စျေးနှုန်း အရ စုစုပေါင်း cost ကို တိုးစေပြီး generation ပြီးဆုံးချိန်ကို ရွေ့စေသည်။ reasoning request ကိုယ်တိုင်သည် prompt ကို အနည်းငယ်သာ တိုးစေသည် — lab_shape_prompt ၏ sweep တွင် cot on သည် prompt ကို ၁၆ token တိုးစေသည်ဟု ပြသည် — သို့သော် အဓိက ကုန်ကျစရိတ်သည် စာသားအဖြစ် ထွက်လာသည့် rationale တွင် ရှိသည်။ ထို့ကြောင့် prompting ဆုံးဖြတ်ချက် တိုင်းတွင် output token ခန့်မှန်းချက်ကို ထည့်တွက်ရမည်။ ချောမွေ့သည့် rationale တစ်ခုသည် ဖြေဆိုချက် မှန်ကန်ကြောင်း သို့မဟုတ် ထို စာသားသည် မော်ဒယ်၏ အတွင်းပိုင်း တွက်ချက်မှုကို သစ္စာရှိစွာ ကိုယ်စားပြုကြောင်း သက်သေ မဟုတ်ပါ၊ ထို့ကြောင့် ရလဒ်ကို သီးခြားစီ စစ်ဆေးရမည်။

#### In-Context Learning

In-Context Learning သည် သာမန် parameter update မပြုဘဲ လက်ရှိ input တွင် ပေးအပ်ထားသည့် ညွှန်ကြားချက်များ၊ ဥပမာများ သို့မဟုတ် ပုံစံများမှ မော်ဒယ်တစ်ခု မိမိ၏ အပြုအမူကို လိုက်လျောညီထွေ ပြောင်းလဲခြင်း ဖြစ်သည်။ ၎င်းသည် prefill compute အပေါ် အခြေခံသည့် လိုက်လျောညီထွေမှု ဖြစ်သည် — weight မပြောင်းလဲသောကြောင့် ကုန်ကျစရိတ် တိုင်းသည် တောင်းဆိုမှု တိုင်း၏ prompt token အပေါ် ပြန်လည် ကျရောက်သည်။ ဤအချက်က few-shot နှင့် zero-shot နှစ်ခုလုံးကို ရှင်းလင်းစေသည်၊ မော်ဒယ် တစ်ခုတည်းသည် demonstration ပါသည့် context နှင့် မပါသည့် context တွင် task အသစ် တစ်ခုကို မတူညီစွာ လုပ်ဆောင်နိုင်သည်။ သို့သော် ၎င်းသည် ယာယီ conditioning သာ ဖြစ်ပြီး fine-tuning၊ ခံတည်သည့် memory သို့မဟုတ် မော်ဒယ်သည် ရည်ရွယ်သည့် စည်းမျဉ်းကို ကောက်ချက်ချခဲ့သည့် သက်သေ မဟုတ်ပါ။ လက်တွေ့တွင် ကိုယ်စားပြုသည့် demonstration များကို ပစ်မှတ် input မတိုင်မီ ထားရမည်၊ အစဉ်နှင့် format မူကွဲများကို စမ်းသပ်ရမည်၊ အကဲဖြတ်သည့် ဥပမာများကို demonstration များနှင့် သီးခြားခွဲထားရမည်။

### မိသားစု (ခ) — context နေရာ နှင့် ရွေးချယ်မှု (context capacity)

#### Context Window

Context Window သည် တိကျသည့် မော်ဒယ်နှင့် API contract တစ်ခုအောက်တွင် မော်ဒယ် inference တစ်ခုအတွက် ရရှိနိုင်သည့် အများဆုံး token ပမာဏ ဖြစ်သည်။ ထို ပမာဏတွင် system ညွှန်ကြားချက်များ၊ message များ၊ ရယူထားသည့် အကြောင်းအရာ၊ tool ဖလှယ်မှုများနှင့် ထုတ်လုပ်သည့် output တို့ ပါဝင်နိုင်သည်။ ဤစာတမ်း၏ ဥပမာများတွင် window 128,000 token ကို အသုံးပြုသည်၊ lab_token_budget ၏ default run သည် ထို window ၏ 46.37% ကို အသုံးပြုသည်ဟု ပြသည်။ window သည် GPU memory ဝင်ရိုးအပေါ် ကျရောက်သည် — ဥပမာ (ခ) တွင် 32,000 token ၏ KV cache သည် reference model အောက်တွင် batch 1 တွင် 15.625 GiB ဖြစ်ပြီး batch 32 တွင် 500 GiB ဖြစ်သည်ဟု တွက်သည်။ window ကျော်လွန်သည့် တောင်းဆိုမှုသည် quality ကျခြင်းဖြင့် မဟုတ်ဘဲ အလုံးအရင်း ကျရှုံးခြင်းဖြင့် ကျိုးပျက်သည်၊ ထို့ကြောင့် window ကို ကြော်ငြာ အရေအတွက်အတိုင်း မသတ်မှတ်ရပါ။ window ကြီးသည့်တိုင် ထည့်သွင်းထားသည့် အသေးစိတ် တိုင်းကို ယုံကြည်စိတ်ချစွာ အသုံးပြုမည်ဟု အာမခံခြင်း မပြုပါ။

#### Token Budget

Token Budget သည် ညွှန်ကြားချက်များ၊ အထောက်အထား၊ မှတ်တမ်း၊ tool ရလဒ်များ၊ reasoning သို့မဟုတ် working space နှင့် output တို့အကြား token ပမာဏကို တိကျစွာ ခွဲဝေ သတ်မှတ်ခြင်း ဖြစ်သည်။ ၎င်းသည် အစီအစဉ် ဆွဲသည့် ကန့်သတ်ချက် ဖြစ်ပြီး မော်ဒယ်၏ အများဆုံး context window နှင့် တူညီသည် မဟုတ်ပါ။ ဥပမာ (ခ) ၏ ဇယားတွင် ထို ကွာခြားချက် ပေါ်လာသည် — အစိတ်အပိုင်း အားလုံး ပေါင်းလျှင် 59,356 token ဖြစ်ပြီး window 128,000 ၏ 46.37% သာ ဖြစ်သည်၊ ထို့ကြောင့် budget ချိန်ညှိရန် နေရာ ရှိသည်။ ထည့်သွင်းသည့် token တိုင်းသည် context ပမာဏ၊ latency နှင့် ကုန်ကျစရိတ် အတွက် ယှဉ်ပြိုင်သည့်အတွက် budget သတ်မှတ်ခြင်းသည် တန်ဖိုးမြင့်သည့် အထောက်အထားကို ဦးစွာ ထိန်းသိမ်းရန် တွန်းအားပေးသည်။ လက်တွေ့တွင် output ပမာဏကို ဖယ်ထားရမည်၊ ရယူထားသည့် chunk များကို ကန့်သတ်ရမည်၊ ဟောင်းသည့် tool ရလဒ်များကို state အဖြစ် အနှစ်ချုပ်ရမည်၊ မော်ဒယ်၏ ကန့်သတ်ချက် မရောက်မီ ရပ်တန့်ရမည် သို့မဟုတ် ချုံ့ရမည်။

#### Context Engineering

Context Engineering သည် ညွှန်ကြားချက်များ၊ ရွေးချယ်ထားသည့် file များ၊ ရယူထားသည့် အထောက်အထားများ၊ tool ရလဒ်များ၊ ဥပမာများ၊ state နှင့် output ကန့်သတ်ချက်များ အပါအဝင် အဆင့်တိုင်းတွင် မော်ဒယ်အား ပေးအပ်သည့် အချက်အလက် ပတ်ဝန်းကျင် အပြည့်အစုံကို စီစဉ် ဖွဲ့စည်းခြင်း ဖြစ်သည်။ မော်ဒယ် စွမ်းဆောင်ရည် ကျရှုံးမှု အများစုသည် သက်ဆိုင်သည့် အထောက်အထားများ ပျောက်ဆုံးခြင်း၊ ခေတ်မမီတော့ခြင်း၊ အစဉ်လွဲနေခြင်း သို့မဟုတ် ဆူညံသံများဖြင့် ဖုံးလွှမ်းခံရခြင်းတို့ကြောင့် ဖြစ်သည်။ Prompt Engineering သည် ညွှန်ကြားချက်၏ စကားလုံး ရွေးချယ်မှုကို အာရုံစိုက်သည်၊ Context Engineering သည် မည်သည့် အထောက်အထားနှင့် state များ မော်ဒယ်၏ working context ထဲသို့ ဝင်ရောက်မည်ကိုလည်း ဆုံးဖြတ်သည်။ ထို့ကြောင့် ၎င်းသည် prompt token ကို တိုက်ရိုက် ထိန်းချုပ်သည့် အလုပ် ဖြစ်ပြီး prefill compute၊ KV cache၊ TTFT နှင့် cost per call လေးခုလုံးအပေါ် တစ်ပြိုင်နက် သက်ရောက်သည်။ လက်တွေ့တွင် ပန်းတိုင်၊ repository စည်းမျဉ်းများ၊ သက်ဆိုင်သည့် interface များ၊ လတ်တလော tool output နှင့် မဖြေရှင်းရသေးသည့် ဆုံးဖြတ်ချက်များ ပါဝင်သည့် ကျစ်လျစ်သည့် task packet တစ်ခုကို တည်ဆောက်ရမည်၊ ထို့နောက် state ပြောင်းလဲသည့်အခါ ၎င်းကို update လုပ်ရမည်။

#### Context Compression

Context Compression သည် နောက်ပိုင်း မော်ဒယ် ဆုံးဖြတ်ချက် တစ်ခုအတွက် လိုအပ်သည့် အချက်အလက်ကို ထိန်းသိမ်းရန် ကြိုးစားရင်း ရင်းမြစ် အကြောင်းအရာ၏ token ပမာဏကို လျှော့ချခြင်း ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ၎င်းသည် prompt token ကို ပြန်ပေးသည့် လုပ်ဆောင်ချက် ဖြစ်သည် — lab_token_budget တွင် ရယူထားသည့် context ကို 24,000 မှ 8,000 သို့ ချုံ့လျှင် 16,000 token လွတ်ပြီး မှတ်တမ်းကို ၎င်း၏ ၂၅% အထိ အနှစ်ချုပ်လျှင် 22,500 token လွတ်သည်ဟု တွက်သည်။ ထို လွတ်သည့် token တိုင်းသည် prefill compute၊ KV cache နေရာ၊ TTFT နှင့် input cost လေးခုလုံးမှ တစ်ပြိုင်နက် လျော့သည်။ သို့သော် ချုံ့ခြင်းသည် lossy ဖြစ်သည်၊ ချန်လှပ်လိုက်သည့် အသေးစိတ် တိုင်းသည် မော်ဒယ်တွင် အထောက်အထား၊ ကန့်သတ်ချက် သို့မဟုတ် မဖြေရှင်းရသေးသည့် state များ ဆုံးရှုံးနိုင်သည့် အန္တရာယ်ကို ဖန်တီးသည်။ မူရင်း အပြည့်အစုံကို ထိန်းသိမ်းထားခြင်း မရှိပါက ပိုတိုသည့် summary တစ်ခုသည် အလိုအလျောက် ညီမျှသည့် context မဟုတ်ပါ။ ထို့ကြောင့် အတည်ပြုပြီး အချက်အလက်များနှင့် identifier များကို စာလုံးတိုင်း ထိန်းသိမ်းရမည်၊ ထပ်နေသည့် မှတ်တမ်းကို အနှစ်ချုပ်ရမည်၊ source ညွှန်းချက်များကို တွဲဖက်ရမည်၊ ချုံ့ထားသည့် context ကို ကိုယ်စားပြုသည့် task များတွင် စမ်းသပ်ရမည်။

### မိသားစု (ဂ) — ညွှန်ကြားချက် အခွင့်အာဏာ နှင့် လိုက်နာမှု (instruction authority)

#### System Prompt

System Prompt သည် ထို provider ၏ instruction hierarchy အတွင်း အပြုအမူနှင့် ကန့်သတ်ချက်များကို တည်ထောင်ရန် application မှ ပေးအပ်သည့် provider မှ သတ်မှတ်ထားသည့် ညွှန်ကြားချက် message တစ်ခု သို့မဟုတ် configuration တစ်ခု ဖြစ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့် system prompt သည် prompt ၏ အစတွင် တည်ငြိမ်စွာ တည်ရှိသည့် prefix token အပိုင်း ဖြစ်သည်၊ ထို့ကြောင့် ၎င်းသည် prefix caching အတွက် အသင့်တော်ဆုံး အပိုင်း ဖြစ်သည်။ ဥပမာ (က) တွင် system prompt သည် ၆၉ token ဖြစ်ပြီး ရှည်သည့် version သည် ၁၉၅ token ဖြစ်သည်၊ ထို့ကြောင့် ရှည်သည့် system prompt သည် အတိုထက် ၂.၈၃ ဆ ကုန်သည်။ ဤကွာခြားချက်သည် တောင်းဆိုမှု တိုင်း၏ prefix တွင် ရှိသည်ဖြစ်၍ တောင်းဆိုမှု အရေအတွက်နှင့် အချိုးကျ တိုးသည်။ system ညွှန်ကြားချက်များသည် အပြုအမူကို လမ်းညွှန်နိုင်သော်လည်း ၎င်းတို့သည် လျှို့ဝှက်နေမည်ဟု အာမခံခြင်း မပြုပါ၊ လုံခြုံရေး နယ်နိမိတ် အနေဖြင့် သဘောထားရမည် မဟုတ်ပါ။ ဦးစားပေး စည်းမျဉ်းများ၊ message role များ၊ ဆက်လက် တည်ရှိမှုနှင့် မြင်နိုင်မှုတို့သည် API အလိုက် ကွာခြားသည့်အတွက် လက်ရှိ provider စာချုပ်ကို စစ်ဆေးရမည်။

#### Instruction Hierarchy

Instruction Hierarchy သည် application policy၊ အသုံးပြုသူများနှင့် မယုံကြည်ရသည့် ရယူထားသည့် အကြောင်းအရာ ကဲ့သို့ အခွင့်အာဏာ မတူညီသည့် ရင်းမြစ်များမှ ညွှန်ကြားချက်များကြား ပဋိပက္ခများကို ဖြေရှင်းသည့် စည်းမျဉ်း အစု တစ်ခု ဖြစ်သည်။ agent စနစ်များသည် ယုံကြည်ရသည့် ပန်းတိုင်များနှင့် ပြင်ပ စာသားများကို ရောနှောထားသောကြောင့် အခွင့်အာဏာ နည်းသည့် အကြောင်းအရာသည် အခွင့်အာဏာ မြင့်သည့် ကန့်သတ်ချက်များနှင့် ပဋိပက္ခဖြစ်သည့်အခါ မော်ဒယ်နှင့် harness သည် တိကျသည့် တုံ့ပြန်မှု တစ်ခုကို လိုအပ်သည်။ ကုန်ကျစရိတ် အမြင်ဖြင့် ၎င်းသည် ပဋိပက္ခ တိုင်းကို ကိုင်တွယ်ရန် ထပ်ဆောင်း prompt token (ဥပမာ escalation စည်းမျဉ်း) ကို တောင်းနိုင်သည်၊ သို့သော် မရှိလျှင် ဖြစ်ပေါ်သည့် ထိခိုက်မှုသည် များစွာ ကြီးမားသည်။ hierarchy သည် အပြုအမူကို တိုးတက်စေနိုင်သော်လည်း လုံခြုံရေး နယ်နိမိတ် တစ်ခု မဟုတ်ပါ၊ least privilege နှင့် အတည်ပြုချက် ထိန်းချုပ်မှုများက အကျိုးဆက်များကို ကန့်သတ်ဆဲ ဖြစ်သည်။ လက်တွေ့တွင် မယုံကြည်ရသည့် tool output ကို data အနေဖြင့် အမှတ်အသားပြုရမည်၊ ထို အကြောင်းအရာ၏ အပြင်ဘက်တွင် ဦးစားပေး မြင့်သည့် ကန့်သတ်ချက်များကို ထိန်းသိမ်းရမည်၊ တိုက်ရိုက်နှင့် သွယ်ဝိုက်သည့် ပဋိပက္ခ အမှုများကို စမ်းသပ်ရမည်။

#### Instruction Following

Instruction Following သည် ဖော်ပြထားသည့် task နှင့် ကန့်သတ်ချက်များကို ပြည့်မီသည့် အပြုအမူသို့ သဘာဝဘာသာ ညွှန်ကြားချက်များနှင့် ပေးအပ်ထားသည့် context ကို ချိတ်ဆက်ပေးသည့် မော်ဒယ် စွမ်းရည် ဖြစ်သည်။ ဘာသာစကား ထုတ်လုပ်ခြင်းသည် အသုံးပြုသူ တောင်းဆိုသည့် လုပ်ဆောင်ချက်၊ format၊ နယ်နိမိတ် သို့မဟုတ် ဦးစားပေး အစဉ်ကို မလိုက်နာဘဲ ချောမွေ့နိုင်သည့်အတွက် ၎င်း၏ ကျရှုံးမှုသည် ထင်ရှားသည့် error မဟုတ်ဘဲ format ချိုးဖောက်မှု၊ မလိုအပ်သည့် ထပ်ဆောင်း စာသား သို့မဟုတ် schema မကိုက်ညီမှု အဖြစ် ထွက်လာတတ်သည်။ အခြေခံအဆောက်အအုံ အမြင်ဖြင့် ထို ကျရှုံးမှု တိုင်းသည် retry သို့မဟုတ် လူဖြင့် ပြန်လည် ပြင်ဆင်မှု အဖြစ် ပြောင်းလဲပြီး accelerator အချိန်ကို ထပ်ဆောင်း ကုန်စေသည့်အတွက် တောင်းဆိုမှု တစ်ခုစီ၏ အမှန်တကယ် ကုန်ကျစရိတ်ကို တိုးစေသည်။ ထို့ကြောင့် instruction adherence ကို ဖြေဆိုချက် အရည်အသွေးနှင့် သီးခြားစီ အကဲဖြတ်ရမည် — ဆန့်ကျင်နေသည့် ကန့်သတ်ချက်များ၊ format လိုအပ်ချက်များ၊ မသက်ဆိုင်သည့် context နှင့် ငြင်းပယ်သည့် အမှုများကို အသုံးပြုရမည်။

### မိသားစု (ဃ) — လက်တွေ့ အပြုအမူ နှင့် ကန့်သတ်ချက် (operational behaviour)

#### Prompt Cache

Prompt Cache သည် တူညီသည့် သို့မဟုတ် အရည်အချင်း ပြည့်မီသည့် prompt prefix တစ်ခုအတွက် provider-side သို့မဟုတ် application-side တွက်ချက်မှုကို ပြန်လည် အသုံးပြုခြင်းဖြင့် ထပ်တလဲလဲ inference သည် preprocessing လုပ်ငန်း အချို့ကို ရှောင်ရှားစေသည်။ ၎င်းသည် ဤနယ်ပယ်တွင် prefill compute ကို တိုက်ရိုက် ချွေတာသည့် တစ်ခုတည်းသော term ဖြစ်ပြီး ထို ချွေတာမှုသည် TTFT နှင့် input cost နှစ်ခုလုံးအပေါ် ကျရောက်သည်။ ဥပမာ (ခ) တွင် 3,000 token ရှိသည့် shared prefix တစ်ခုကို ခေါ်ဆိုမှု ၁၀၀ က မျှဝေသုံးစွဲသည့်အခါ prefill token သည် 320,000 မှ 23,000 သို့ ကျဆင်းသည် (92.81% ချွေတာသည်)၊ TTFT သည် 40,000 ms မှ 2,915 ms သို့ ကျဆင်းပြီး cost သည် USD 0.96 မှ USD 0.069 သို့ ကျဆင်းသည်ဟု တွက်သည်။ ဤအကျိုးအမြတ်ကို VRAM ဖြင့် ဝယ်ရသည်၊ shared prefix ၏ KV ကို တစ်ကြိမ်သာ သိမ်းဆည်းလျှင် 1,500 MiB ဖြစ်ပြီး မျှဝေခြင်း မရှိဘဲ မိတ္တူ ၁၀၀ သိမ်းဆည်းလျှင် 146.48 GiB ဖြစ်သည်။ Prompt cache သည် provider သို့မဟုတ် application ၏ ပြန်လည် အသုံးပြုမှု စာချုပ် တစ်ခု ဖြစ်ပြီး အတွင်းပိုင်းတွင် prefix caching ကို အသုံးပြုနိုင်သည်၊ prefix caching သည် အရည်အချင်း ပြည့်မီသည့် တိကျသည့် token တူညီသည့် KV state ကို အထူး အသုံးပြုပြီး semantic caching သည် လုံလောက်စွာ ဆင်တူသည့် တောင်းဆိုမှု တစ်ခုအတွက် ယခင် ရလဒ်ကို ပြန်လည် အသုံးပြုသည်။ လက်တွေ့တွင် တည်ငြိမ်သည့် policy စာသားကို တောင်းဆိုမှုနှင့် သီးခြားဖြစ်သည့် အကြောင်းအရာ မတိုင်မီ ထားရမည်၊ cache-hit metadata ကို စောင့်ကြည့်ရမည်၊ အရည်အချင်းနှင့် သက်တမ်းသည် provider အလိုက် ကွာခြားသည့်အတွက် miss များကို ပုံမှန် အဖြစ် သဘောထားရမည်။

#### Prompt Sensitivity

Prompt Sensitivity သည် ရည်ရွယ်သည့် task ကို မပြောင်းလဲဘဲ prompt ၏ စကားလုံး၊ အစဉ်၊ format သို့မဟုတ် ဥပမာများကို ပြောင်းလဲခြင်းကြောင့် ဖြစ်ပေါ်သည့် မော်ဒယ် output သို့မဟုတ် တိုင်းတာသည့် စွမ်းဆောင်ရည်၏ ကွဲပြားမှု ဖြစ်သည်။ အဆင်ပြေသည့် စကားလုံး ဖွဲ့စည်းမှု တစ်ခုအောက်တွင် အောင်မြင်သည့် စနစ် တစ်ခုသည် အမှန်တကယ် အသုံးပြုသူများအတွက် ယုံကြည်စိတ်ချရနိုင် မရှိနိုင် သို့မဟုတ် အကဲဖြတ်မှုတွင် လွဲမှားစေနိုင်သည်။ ထို့ကြောင့် prompt မူကွဲ တစ်ခုတည်းပေါ်တွင် ရရှိသည့် အောင်မြင်မှုသည် capacity ခန့်မှန်းမှုအတွက် လုံလောက်သည့် သက်သေ မဟုတ်ပါ — မူကွဲများအကြား ကွဲပြားမှုကို ပုံမှန် တိုင်းတာရမည်။ sensitivity သည် prompt ချို့ယွင်းမှု တိုင်း မဟုတ်ပါ၊ ၎င်းသည် မရှင်းလင်းမှု၊ မော်ဒယ်၏ ခိုင်မာမှု အားနည်းမှု၊ မတည်ငြိမ်သည့် decoding သို့မဟုတ် မလုံလောက်သည့် scoring စည်းမျဉ်းတို့ကို ဖော်ထုတ်နိုင်သည်။ လက်တွေ့တွင် အဓိပ္ပာယ် တူညီသည့် prompt မူကွဲများ ဖန်တီးရမည်၊ အမှု အလိုက် ကွဲပြားမှုကို တိုင်းတာရမည်၊ eval set တစ်ခုပေါ်တွင် prompt တစ်ခုကို အကောင်းဆုံး ဖြစ်အောင် ပြုပြင်ခြင်းအစား မူကွဲများကို regression test များတွင် ထိန်းသိမ်းရမည်။

#### Lost in the Middle

Lost in the Middle သည် အထောက်အထား၏ တည်နေရာအလိုက် မော်ဒယ် စွမ်းဆောင်ရည် ပြောင်းလဲပြီး သက်ဆိုင်သည့် အချက်အလက်သည် အစနှင့် အဆုံးကြား တွင် ရှိသည့်အခါ ကျဆင်းနိုင်သည့် long-context ကျရှုံးမှု ပုံစံ တစ်ခု ဖြစ်သည်။ အထောက်အထားကို context window အတွင်း ထည့်သွင်းနိုင်ခြင်းသည် မော်ဒယ်က တည်နေရာ တိုင်းကို ညီမျှသည့် ယုံကြည်စိတ်ချရမှုဖြင့် အသုံးပြုမည်ဟု အာမခံခြင်း မပြုပါ။ ထို့ကြောင့် context window ကို ဖြည့်သည့် မူဝါဒသည် compute နှင့် memory သာ ကုန်ခြင်း မဟုတ်ဘဲ အထောက်အထား၏ တည်နေရာ ကြောင့် တိကျမှုကိုလည်း ရွေ့စေနိုင်သည်။ ၎င်းသည် လေ့လာ တွေ့ရှိထားသည့် အပြုအမူ ပုံစံ တစ်ခု ဖြစ်ပြီး မော်ဒယ်၊ task သို့မဟုတ် တည်နေရာ တိုင်းကို တူညီစွာ သက်ရောက်သည့် ပုံသေ နိယာမ တစ်ခု မဟုတ်ပါ။ လက်တွေ့တွင် အထောက်အထား တည်နေရာ များစွာကို စမ်းသပ်ရမည်၊ အာရုံလွဲစေသည့် အရာများကို လျှော့ချရမည်၊ ဆုံးဖြတ်ချက်အတွက် အရေးပါသည့် ကန့်သတ်ချက်များကို ထင်ရှားနေဆဲ နေရာတွင် ထားရှိရမည်၊ ဖြေဆိုချက်များကို ရင်းမြစ်နှင့် ကိုက်ညီမှု စစ်ဆေးရမည်။

## ၄။ လက်တွေ့ တွက်ချက်မှု သုံးခု

ဤအပိုင်းရှိ output အားလုံးသည် အောက်တွင် ဖော်ပြသည့် command များကို တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ script များသည် standard library သာ အသုံးပြုပြီး deterministic ဖြစ်သည်။ token အားလုံးသည် script ထဲတွင် ဖော်ပြထားသည့် estimator `tokens = ceil(characters / 4)` မှ ရရှိသည့် ခန့်မှန်းတန်ဖိုး ဖြစ်သည်။

### (က) ဖော်ပြထားသည့် prompt တစ်ခု၏ cost — ဥပမာ ၁၊ ၂၊ ၃ ခုနှင့် ရှည်သည့် system prompt

ဖော်မြူလာ — `input_cost = input_tokens × input_price ÷ 10⁶`၊ `output_cost = output_tokens × output_price ÷ 10⁶`။ ယူဆချက် — input price USD 3.00 per 1e6 token၊ output price USD 15.00 per 1e6 token၊ ဖြေဆိုချက် အရှည် ၁၂၀ token။ ဥပမာ တစ်ခုသည် ၄၆ token၊ instruction ၁၃ token၊ မေးခွန်း ၁၇ token ဖြစ်သည်။

```text
$ python3 guides/05_prompting_and_context/scripts/ex_a_prompt_cost.py
estimator: tokens = ceil(characters / 4) ; input USD 3.00/1e6 tok ; output USD 15.00/1e6 tok ; answer 120 tok
fixed parts, in tokens: system=69  instructions=13  example=46  question=17

prompt variant                     input tok      input USD       USD/call
base (system + task + question)           99       0.000297       0.002097
base + 1 example(s)                      145       0.000435       0.002235
base + 2 example(s)                      191       0.000573       0.002373
base + 3 example(s)                      237       0.000711       0.002511
base with longer system prompt           225       0.000675       0.002475
longer system + 1 example(s)             271       0.000813       0.002613
longer system + 2 example(s)             317       0.000951       0.002751
longer system + 3 example(s)             363       0.001089       0.002889

what one example adds      : 46 input tok = USD 0.000138 per call
what the longer system adds: 126 input tok = USD 0.000378 per call
three examples add         : 138 input tok = USD 0.000414 per call
the longer system prompt costs 2.83x the short one, before any example
```

ဤဇယားက ပြသည့် အဓိက အချက်မှာ ဥပမာ တစ်ခုစီသည် တောင်းဆိုမှု တိုင်း၏ cost ကို တူညီစွာ တိုးစေပြီး system prompt ကို ရှည်စေခြင်းသည် ဥပမာ တစ်ခုကို ထည့်ခြင်းထက် ပို၍ ကုန်ကျခြင်း ဖြစ်သည်။

### (ခ) ရှည်သည့် prompt တစ်ခု၏ KV cache memory နှင့် prefix caching ၏ ချွေတာမှု

ဖော်မြူလာ — `kv_bytes = 2 × layers × tokens × heads × head_dim × bytes_per_element`။ ယူဆချက် — reference model layers 32၊ heads 32၊ head_dim 128၊ fp16 (0.500 MiB per token)၊ accelerator 80 GB တွင် 16 GiB သီးသန့်ထား၍ KV အတွက် 64 GiB အသုံးပြုနိုင်သည်၊ prefill rate 8000 tokens/s၊ input price USD 3.00 per 1e6 token။

```text
$ python3 guides/05_prompting_and_context/scripts/ex_b_prefix_cache.py
estimator of KV memory: kv_bytes = 2 * layers * tokens * heads * head_dim * bytes
reference model: layers=32 heads=32 head_dim=128 fp16 -> 0.500 MiB per token
usable KV on one 80 GB accelerator with 16 GiB reserved = 64 GiB

part 1 - what a longer prompt costs in KV cache
prompt tok      batch 1 MiB    batch 1 GiB   batch 32 GiB  batch 32 fits
1000                 500.00         0.4883        15.6250              1
3000                1500.00         1.4648        46.8750              1
8000                4000.00         3.9062       125.0000              0
32000              16000.00        15.6250       500.0000              0

part 2 - prefix caching: 3000 shared prefix tokens, 100 calls, 200 suffix tokens each
prefill tokens without cache           320000
prefill tokens with prefix cache        23000
prefill tokens saved                   297000
saved, percent of the uncached prefill     92.81%
token saving per added call (calls>1)       2970

latency at 8000 tokens/s prefill
without cache                         40000.0 ms
with prefix cache                      2875.0 ms
saved                                 37125.0 ms

cost at USD 3.00 per 1e6 prefill tokens
without cache                        0.960000 USD
with prefix cache                    0.069000 USD

memory side: the shared prefix KV is stored once = 1500.00 MiB (1.4648 GiB); without sharing, 100 copies would take 146.48 GiB
the cache contract (eligibility, lifetime, minimum block) is provider-specific, so misses are normal.
```

part 1 သည် memory အပိုင်းကို ပြသည် — prompt ရှည်လာသည့်အလိုက် KV cache သည် အချိုးကျ တိုးပြီး 32,000 token တွင် batch 32 သည် 64 GiB အထဲ မဆံ့တော့ပါ။ part 2 သည် ထပ်တလဲလဲ ခေါ်ဆိုမှု များစွာ တူညီသည့် prefix ကို မျှဝေသည့်အခါ ချွေတာမှုကို ပြသည်။

### (ဂ) prompt အရှည်သည် TTFT ကို မည်သို့ ရွေ့စေသည် — cache hit ရှိ/မရှိ

ဖော်မြူလာ — `ttft_ms = overhead_ms + (prompt_tokens − cached_tokens) ÷ prefill_rate × 1000`။ ယူဆချက် — prefill rate 8000 tokens/s၊ overhead 40 ms (queueing၊ scheduling နှင့် network အတွက် cache နှင့် မသက်ဆိုင်သည့် ကိန်းသေ)၊ ဤအပိုင်းတွင် generation အချိန်ကို မတွက်ပါ။

```text
$ python3 guides/05_prompting_and_context/scripts/ex_c_ttft.py
model: ttft_ms = 40 + (prompt_tokens - cached_tokens) / 8000 * 1000
assumption: prefill rate 8000 tokens/s, overhead 40 ms

prompt         ttft cache=0  ttft cache=3000  ttft cache=8000 saving 3000 vs 0
500                102.5 ms          40.0 ms          40.0 ms          61.0 %
1000               165.0 ms          40.0 ms          40.0 ms          75.8 %
2000               290.0 ms          40.0 ms          40.0 ms          86.2 %
4000               540.0 ms         165.0 ms          40.0 ms          69.4 %
8000              1040.0 ms         665.0 ms          40.0 ms          36.1 %
16000             2040.0 ms        1665.0 ms        1040.0 ms          18.4 %
32000             4040.0 ms        3665.0 ms        3040.0 ms           9.3 %

a 3000-token cache hit removes 375.0 ms of prefill at every prompt length
a full 8000-token cache hit removes 1000.0 ms of prefill at every prompt length
doubling the prompt doubles the uncached prefill term and leaves the 40 ms overhead untouched
prefill latency = (prompt_tokens - cached_tokens) / prefill_rate, linear in prompt length and linear in cache hits
```

ဇယားက ပြသည့် အဓိက အချက်မှာ TTFT သည် prompt အရှည်အပေါ် linear တိုးခြင်း ဖြစ်သည်၊ cache hit သည် အရှည် တိုင်းတွင် တူညီသည့် ကိန်းသေ ပမာဏကို ဖြတ်တောက်ပေးခြင်း ဖြစ်သည်။ ထို့ကြောင့် prompt အလွန်ရှည်သည့် အသုံးမှုတွင် cache hit rate သည် TTFT SLO ၏ အဓိက ကိန်း ဖြစ်လာသည်။

## ၅။ ဤနယ်ပယ်မှ ဆင်းသက်လာသည့် prompt-engineering ဆုံးဖြတ်ချက် ခြောက်ခု

**၁။ Prompt အရှည် သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Token Budget၊ Context Window၊ Few-Shot၊ System Prompt။ သက်သေပြသည့် မက်ထရစ် — input token နှင့် cost per call။ ဥပမာ (က) က ဥပမာ သုံးခုနှင့် ရှည်သည့် system prompt ပေါင်းလျှင် USD 0.002889 ဖြစ်သည်ဟု ပြသည်၊ ထို့ကြောင့် ဥပမာ အရေအတွက်နှင့် system အရှည်ကို အတူတကွ ဆုံးဖြတ်ရမည်။

**၂။ Prefix ကို တည်ငြိမ်စွာ ထားခြင်း** — မှီခိုသည့် term များ — Prompt Cache၊ System Prompt၊ Context Engineering။ သက်သေပြသည့် မက်ထရစ် — cache hit rate နှင့် prefill token saving ရာခိုင်နှုန်း။ ဥပမာ (ခ) အရ တည်ငြိမ်သည့် prefix 3,000 token ကို ခေါ်ဆိုမှု ၁၀၀ က မျှဝေလျှင် prefill ၏ 92.81% ကို ချွေတာသည်၊ ထို့ကြောင့် တောင်းဆိုမှု အလိုက် ပြောင်းသည့် အကြောင်းအရာကို အမြဲ နောက်ဆုံးတွင် ထားရမည်။

**၃။ TTFT ရည်မှန်းချက် သတ်မှတ်ခြင်း** — မှီခိုသည့် term များ — Time to First Token (TTFT)၊ Prompt Cache၊ Context Window၊ Token Budget။ သက်သေပြသည့် မက်ထရစ် — client-side TTFT (cache အခြေအနေ အလိုက် ခွဲခြား)။ ဥပမာ (ဂ) အရ 8,000 token prompt သည် cache မရှိလျှင် 1,040 ms ဖြစ်ပြီး 3,000 token cache hit ဖြင့် 665 ms ဖြစ်သည်၊ ထို့ကြောင့် TTFT SLO ကို prompt အရှည်နှင့် cache policy နှင့် တွဲဖက် သတ်မှတ်ရမည်။

**၄။ ဥပမာ အရေအတွက် ရွေးချယ်ခြင်း** — မှီခိုသည့် term များ — Few-Shot၊ Zero-Shot၊ In-Context Learning၊ Prompt Sensitivity။ သက်သေပြသည့် မက်ထရစ် — ဥပမာ token တစ်ခုစီလျှင် ရရှိသည့် တိကျမှု တိုးတက်မှု (accuracy per example token)။ ဥပမာ (က) အရ ဥပမာ တစ်ခုစီသည် ၄၆ input token ကုန်သည့်အတွက် တိကျမှု မတိုးသည့် ဥပမာ များကို ဖယ်ရှားရမည်။

**၅။ Context ချုံ့မှု မူဝါဒ** — မှီခိုသည့် term များ — Context Compression၊ Token Budget၊ Lost in the Middle။ သက်သေပြသည့် မက်ထရစ် — ချုံ့ထားသည့် context ပေါ်တွင် တိကျမှု နှင့် လွတ်သွားသည့် token။ lab_token_budget အရ မှတ်တမ်းကို ၂၅% အထိ အနှစ်ချုပ်လျှင် 22,500 token လွတ်သည်၊ သို့သော် ထို ချုံ့မှုကို ကိုယ်စားပြုသည့် task များတွင် စမ်းသပ်မှသာ လက်ခံရမည်။

**၆။ ညွှန်ကြားချက် လိုက်နာမှုနှင့် မူကွဲ စမ်းသပ်ခြင်း** — မှီခိုသည့် term များ — Instruction Hierarchy၊ System Prompt၊ Instruction Following၊ Prompt Sensitivity၊ Chain of Thought (CoT)။ သက်သေပြသည့် မက်ထရစ် — instruction adherence နှင့် မူကွဲများအကြား variance။ lab_shape_prompt အရ လိုအပ်သည့် အပိုင်း (ဥပမာ examples) မပါလျှင် စစ်ဆေးမှုက ဖော်ထုတ်သည်၊ ထို စစ်ဆေးမှုကို eval set နှင့် regression test များတွင် ထည့်ထားရမည်။

## လေ့ကျင့်ခန်း ဆက်စပ်မှု

ဤစာတမ်းရှိ ဖော်မြူလာများကို `guides/05_prompting_and_context/labs/lab_token_budget.py`၊ `lab_prefix_cache.py`၊ `lab_shape_prompt.py` တို့ဖြင့် လက်တွေ့ စမ်းသပ်နိုင်သည်။ ထို lab များ၏ လမ်းညွှန်ချက်နှင့် ကူးထားသည့် output များသည် `guides/05_prompting_and_context/labs/README.md` တွင် ရှိသည်။

## References

- Source glossary: [AI Engineering from Scratch — Glossary](https://aiengineeringfromscratch.com/glossary) — MIT licensed၊ `rohitg00/ai-engineering-from-scratch`။
- ဤနယ်ပယ်၏ term ရှင်းလင်းချက် — `terms/05_prompting_and_context.md`။
- ဤနယ်ပယ်၏ term အစဉ် အခြေခံ — `glossary/by_area/05_prompting_and_context.json`။
- ဖော်မြူလာ အခြေခံ — `guides/02_models_and_inference/03_theory_to_infrastructure.md` (KV cache နှင့် cost model)။
- [Prompt Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/01-prompt-engineering/)၊ [Few-Shot and Chain of Thought](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/02-few-shot-cot/)၊ [Context Engineering](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/05-context-engineering/)၊ [Prompt Caching](https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/phases/11-llm-engineering/15-prompt-caching/)။

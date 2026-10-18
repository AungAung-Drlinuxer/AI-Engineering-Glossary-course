# Labs - Area 09: Infrastructure & Serving

ဤ lab suite သည် area 09 ၏ term များ (Model Serving, Prefill, Decode Phase, Continuous
Batching, KV-cache memory, roofline throughput, Autoscaling) ကို လက်တွေ့ တွက်ကြည့်ရန်
ဖြစ်သည်။ Python standard library သာ အသုံးပြုသည်၊ network နှင့် GPU မလိုအပ်ပါ၊ run တိုင်း
ရလဒ် တူညီသည် (deterministic)။ bandwidth၊ efficiency၊ စျေးနှုန်းနှင့် KV geometry အားလုံးကို
assumption အဖြစ် ဖော်ပြထားသည်။

## Run the whole suite (မဖြစ်မနေ)

```bash
cd guides/09_infrastructure_and_serving/labs
python3 run_labs.py
```
Lab သုံးခုလုံးကို `--self-test` ဖြင့် run ပြီး တစ်လိုင်း စီ ပြသည်။ အားလုံး အောင်မြင်ပါက
`[PASS] All 3/3 labs passed successfully.` ဖြင့် ပြီး exit 0 ဖြစ်သည်။

```
==========================================================================
run_labs - area 09 Infrastructure & Serving (offline, deterministic)
==========================================================================
[PASS] lab_serving_memory.py: [PASS] lab_serving_memory self-test passed.
[PASS] lab_roofline.py: [PASS] lab_roofline self-test passed.
[PASS] lab_autoscale.py: [PASS] lab_autoscale self-test passed.
==========================================================================
[PASS] All 3/3 labs passed successfully.
```

## lab_serving_memory.py - weights, KV cache, activations နှင့် batch headroom

weight GiB၊ KV cache per sequence နှင့် total၊ activation workspace၊ total VRAM နှင့်
stated budget အောက်တွင် တင်နိုင်သည့် အကြီးဆုံး batch ကို ပြသည်။

```bash
python3 lab_serving_memory.py                       # default: 8.0B, 32L/32H/128D, context 8192, batch 32, fp16, budget 72 GiB
python3 lab_serving_memory.py --context 32768 --dtype int8 --batch 8
python3 lab_serving_memory.py --params-b 70 --dtype int4 --budget-gib 40
python3 lab_serving_memory.py --sweep
python3 lab_serving_memory.py --self-test
python3 lab_serving_memory.py --help
```
Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_serving_memory - weights, KV cache, activations and batch headroom
params=8.0B  layers=32  heads=32  head_dim=128  d_model=4096  context=8192  batch=32  dtype=fp16
budget=72.000 GiB (assumption)   activation factor=4.00 (assumption)
--------------------------------------------------------------------------
weights                     :      14.901 GiB  (16000000000 B)
KV cache per sequence       :       4.000 GiB  (4294967296 B)
KV cache total ( 32)        :     128.000 GiB
activations per sequence    :       0.250 GiB
activations total ( 32)     :       8.000 GiB
total VRAM (weights+KV+act) :     150.901 GiB
fits budget 72.000 GiB    : no  (over by 78.901 GiB)
largest batch that fits     : 13
--------------------------------------------------------------------------
batch sweep (KV cache and activations scale with batch, weights do not):
batch     KV total GiB    act GiB   total GiB   headroom GiB
1                4.000      0.250      19.151         52.849
8               32.000      2.000      48.901         23.099
16              64.000      4.000      82.901        -10.901
32             128.000      8.000     150.901        -78.901
--------------------------------------------------------------------------
မှတ်ချက် - KV cache သည် context နှင့် batch အပေါ် မှီခို၍ ကြီးထွားသည်၊ weight သည် batch အပေါ် မမှီခိုပါ။
==========================================================================
```
context နှင့် dtype ကို ပြောင်းလိုက်သည့် run -
```bash
python3 lab_serving_memory.py --context 32768 --dtype int8 --batch 8
```
ထို run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_serving_memory - weights, KV cache, activations and batch headroom
params=8.0B  layers=32  heads=32  head_dim=128  d_model=4096  context=32768  batch=8  dtype=int8
budget=72.000 GiB (assumption)   activation factor=4.00 (assumption)
--------------------------------------------------------------------------
weights                     :       7.451 GiB  (8000000000 B)
KV cache per sequence       :       8.000 GiB  (8589934592 B)
KV cache total (  8)        :      64.000 GiB
activations per sequence    :       0.500 GiB
activations total (  8)     :       4.000 GiB
total VRAM (weights+KV+act) :      75.451 GiB
fits budget 72.000 GiB    : no  (over by 3.451 GiB)
largest batch that fits     : 7
--------------------------------------------------------------------------
batch sweep (KV cache and activations scale with batch, weights do not):
batch     KV total GiB    act GiB   total GiB   headroom GiB
1                8.000      0.500      15.951         56.049
8               64.000      4.000      75.451         -3.451
16             128.000      8.000     143.451        -71.451
32             256.000     16.000     279.451       -207.451
--------------------------------------------------------------------------
မှတ်ချက် - KV cache သည် context နှင့် batch အပေါ် မှီခို၍ ကြီးထွားသည်၊ weight သည် batch အပေါ် မမှီခိုပါ။
==========================================================================
```

## lab_roofline.py - decode အတွက် roofline ခန့်မှန်းချက်

bytes per decode step၊ tokens/s ceiling၊ stated efficiency ဖြင့် ရရှိသည့် tokens/s နှင့်
cost per million tokens ကို ပြသည်။ decode သည် memory bandwidth ဖြင့် ကန့်သတ်ခံရသည်ဟု
ယူဆသည်။

```bash
python3 lab_roofline.py                            # default: bandwidth 3350 GB/s, 8.0B fp16, batch 32, 0.75 efficiency, USD 2.50/GPU-hour
python3 lab_roofline.py --params-b 70 --dtype int4 --batch 64 --gpu-hour-cost 1.20
python3 lab_roofline.py --bandwidth-gbps 2000 --efficiency 0.6 --batch 8
python3 lab_roofline.py --sweep
python3 lab_roofline.py --self-test
python3 lab_roofline.py --help
```
Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_roofline - memory-bandwidth roofline for decode (offline, deterministic)
bandwidth=3350.0 GB/s (assumption)  params=8.0B fp16  batch=32
KV=512.0 KiB per token per sequence (32L/32H/128D, assumption)  efficiency=75.0% (assumption)
GPU-hour price=USD 2.50 (assumption, varies by vendor)
--------------------------------------------------------------------------
weight bytes per step        :    16000000000 B  (16.000 GB)
KV bytes per token per seq   :         524288 B  (512.000 KiB)
bytes per decode step        :    16016777216 B  (weights + batch * KV)
tokens/s ceiling             :         6693.0
tokens/s at 75.0% efficiency  :         5019.7
time per decode step (ms)    :          0.149
cost per million tokens      :         0.1383 USD
--------------------------------------------------------------------------
batch sweep (weights are read once per step, KV cache once per sequence):
batch        bytes/step   tok/s ceiling  tok/s achieved  USD/1e6 tokens
1            1.6001e+10           209.4           157.0          4.4225
2            1.6001e+10           418.7           314.0          2.2113
4            1.6002e+10           837.4           628.0          1.1057
8            1.6004e+10          1674.6          1255.9          0.5529
16           1.6008e+10          3348.2          2511.2          0.2765
32           1.6017e+10          6693.0          5019.7          0.1383
64           1.6034e+10         13372.0         10029.0          0.0692
128          1.6067e+10         26688.1         20016.0          0.0347
256          1.6134e+10         53154.1         39865.6          0.0174
--------------------------------------------------------------------------
မှတ်ချက် - batch တိုးလျှင် weight byte သည် sequence အရေအတွက်ဖြင့် ပြန်လည် အသုံးပြုခံရသည်၊ ထို့ကြောင့် cost per million tokens ကျဆင်းသည်။
==========================================================================
```
params၊ dtype၊ batch နှင့် စျေးနှုန်းကို ပြောင်းလိုက်သည့် run -
```bash
python3 lab_roofline.py --params-b 70 --dtype int4 --batch 64 --gpu-hour-cost 1.20
```
ထို run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_roofline - memory-bandwidth roofline for decode (offline, deterministic)
bandwidth=3350.0 GB/s (assumption)  params=70.0B int4  batch=64
KV=128.0 KiB per token per sequence (32L/32H/128D, assumption)  efficiency=75.0% (assumption)
GPU-hour price=USD 1.20 (assumption, varies by vendor)
--------------------------------------------------------------------------
weight bytes per step        :    35000000000 B  (35.000 GB)
KV bytes per token per seq   :         131072 B  (128.000 KiB)
bytes per decode step        :    35008388608 B  (weights + batch * KV)
tokens/s ceiling             :         6124.2
tokens/s at 75.0% efficiency  :         4593.2
time per decode step (ms)    :          0.163
cost per million tokens      :         0.0726 USD
--------------------------------------------------------------------------
batch sweep (weights are read once per step, KV cache once per sequence):
batch        bytes/step   tok/s ceiling  tok/s achieved  USD/1e6 tokens
1            3.5000e+10            95.7            71.8          4.6435
2            3.5000e+10           191.4           143.6          2.3217
4            3.5001e+10           382.9           287.1          1.1609
8            3.5001e+10           765.7           574.3          0.5804
16           3.5002e+10          1531.3          1148.5          0.2902
32           3.5004e+10          3062.5          2296.9          0.1451
64           3.5008e+10          6124.2          4593.2          0.0726
128          3.5017e+10         12245.6          9184.2          0.0363
256          3.5034e+10         24479.4         18359.5          0.0182
--------------------------------------------------------------------------
မှတ်ချက် - batch တိုးလျှင် weight byte သည် sequence အရေအတွက်ဖြင့် ပြန်လည် အသုံးပြုခံရသည်၊ ထို့ကြောင့် cost per million tokens ကျဆင်းသည်။
==========================================================================
```

## lab_autoscale.py - replica အရေအတွက်၊ queue ကြီးထွားမှုနှင့် ကုန်ကျစရိတ်

offered load၊ replica တစ်လုံးချင်း၏ load နှင့် utilisation၊ queue growth၊ target
utilisation အတွက် required replicas၊ scale-up time နှင့် over- နှင့် under-provisioning
ကုန်ကျစရိတ်ကို ပြသည်။

```bash
python3 lab_autoscale.py                           # default: rps 12.0, output 220, replica-tps 900, replicas 2, target 0.75, cold-start 45 s
python3 lab_autoscale.py --rps 40 --output-tokens 300 --replicas 3
python3 lab_autoscale.py --rps 8 --target-utilisation 0.6 --replicas 1 --cold-start-s 90
python3 lab_autoscale.py --sweep
python3 lab_autoscale.py --self-test
python3 lab_autoscale.py --help
```
Default run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_autoscale - replica count, queue growth, scale-up time and cost
rps=12.0  output-tokens=220  replica-tps=900  replicas=2  target-utilisation=0.75  cold-start-s=45.0
GPU-hour price=USD 2.50 (assumption, varies by vendor)
--------------------------------------------------------------------------
offered load                :       2640.0 output tokens/s
effective per replica       :        675.0 tokens/s at the target
load per replica            :       1320.0 tokens/s  (utilisation 1.467)
queue growth                :        3.818 requests/s  (backlog 229 requests in 60 s)
required replicas (target)  :            4
scale-up needed             :            2 replica(s)
scale-up time               :         90.0 s
served throughput           :       1800.0 tokens/s
cost at 2 replica(s)           :         5.00 USD/hour
cost per million tokens     :       0.7716 USD
over-provisioning cost      :         0.00 USD/hour  (0 idle replica(s))
under-provisioning shortfall:        840.0 tokens/s unscheduled
--------------------------------------------------------------------------
replica sweep:
replicas   utilisation  served tok/s  queue req/s   USD/hour  USD/1e6 tokens
1                2.933         900.0        7.909       2.50          0.7716
2                1.467        1800.0        3.818       5.00          0.7716
3                0.978        2640.0        0.000       7.50          0.7891
4                0.733        2640.0        0.000      10.00          1.0522
6                0.489        2640.0        0.000      15.00          1.5783
8                0.367        2640.0        0.000      20.00          2.1044
--------------------------------------------------------------------------
မှတ်ချက် - utilisation သည် 1.0 ကျော်လျှင် queue ကြီးထွားသည်၊ target utilisation အောက် ထားလျှင် latency headroom ရရှိသည်။
==========================================================================
```
arrival rate နှင့် output အရှည်ကို ပြောင်းလိုက်သည့် run -
```bash
python3 lab_autoscale.py --rps 40 --output-tokens 300 --replicas 3
```
ထို run ၏ အမှန်တကယ် output -
```
==========================================================================
lab_autoscale - replica count, queue growth, scale-up time and cost
rps=40.0  output-tokens=300  replica-tps=900  replicas=3  target-utilisation=0.75  cold-start-s=45.0
GPU-hour price=USD 2.50 (assumption, varies by vendor)
--------------------------------------------------------------------------
offered load                :      12000.0 output tokens/s
effective per replica       :        675.0 tokens/s at the target
load per replica            :       4000.0 tokens/s  (utilisation 4.444)
queue growth                :       31.000 requests/s  (backlog 1860 requests in 60 s)
required replicas (target)  :           18
scale-up needed             :           15 replica(s)
scale-up time               :        675.0 s
served throughput           :       2700.0 tokens/s
cost at 3 replica(s)           :         7.50 USD/hour
cost per million tokens     :       0.7716 USD
over-provisioning cost      :         0.00 USD/hour  (0 idle replica(s))
under-provisioning shortfall:       9300.0 tokens/s unscheduled
--------------------------------------------------------------------------
replica sweep:
replicas   utilisation  served tok/s  queue req/s   USD/hour  USD/1e6 tokens
1               13.333         900.0       37.000       2.50          0.7716
2                6.667        1800.0       34.000       5.00          0.7716
3                4.444        2700.0       31.000       7.50          0.7716
4                3.333        3600.0       28.000      10.00          0.7716
6                2.222        5400.0       22.000      15.00          0.7716
8                1.667        7200.0       16.000      20.00          0.7716
--------------------------------------------------------------------------
မှတ်ချက် - utilisation သည် 1.0 ကျော်လျှင် queue ကြီးထွားသည်၊ target utilisation အောက် ထားလျှင် latency headroom ရရှိသည်။
==========================================================================
```

## မှတ်ချက်

- Output အားလုံးကို `python3 verify_guide.py --guide 09 --labs --verbose` ဖြင့် စစ်ဆေးနိုင်သည်။
- `--self-test` သည် တိကျသည့် ဂုဏ်သတ္တိများကို assert လုပ်သည် (context နှစ်ဆ ဖြစ်ပါက
  KV နှစ်ဆ၊ int8 သည် fp16 ၏ တစ်ဝက်၊ batch တိုးလျှင် throughput sublinear တိုး၊ throughput
  နှစ်ဆ ဖြစ်ပါက cost per million ထက်ဝက်၊ utilisation သည် 1.0 ကျော်လျှင် queue ကြီးထွားသည်)။
- Flag တိုင်း၏ အဓိပ္ပာယ်ကို `python3 <lab> --help` ဖြင့် ကြည့်နိုင်သည်။
- bandwidth၊ efficiency၊ GPU-hour စျေးနှုန်းနှင့် activation factor အားလုံးသည်
  stated assumption ဖြစ်သည်၊ accelerator၊ vendor နှင့် region အလိုက် ကွာခြားသည်။

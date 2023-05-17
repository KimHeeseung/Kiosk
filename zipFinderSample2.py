from kozip import KoZIP
import datetime

kozip = KoZIP()

#HANS # depth: 1(시도), 2(시군구 단위까지), 3(도로명 단위까지), 4(=full, 추가정보 모두)
#HANS addrL = kozip.ZIPtoAddr("05656", depth=1)
#HANS for l in addrL:
#HANS     print(l)
#HANS print('#'*80)
#HANS addrL = kozip.ZIPtoAddr("05656", depth=2)
#HANS for l in addrL:
#HANS     print(l)
#HANS print('#'*80)
#HANS addrL = kozip.ZIPtoAddr("05656", depth=3)
#HANS for l in addrL:
#HANS     print(l)
#HANS print('#'*80)
#HANS addrL = kozip.ZIPtoAddr("05656", depth="full")
#HANS for l in addrL:
#HANS     print(l)
#HANS print('#'*80)
#HANS 

#HANS addrL = kozip.maskedZIPtoAddr("05***")  # ['서울특별시']
#HANS addrL = kozip.maskedZIPtoAddr("056??", masking_letter="?", depth=2, format="list")  # ['서울특별시', '송파구']
addrL = kozip.maskedZIPtoAddr("0565?", masking_letter="?", depth=4, format="list")  # ['서울특별시', '송파구']
for l in addrL:
    print(l)

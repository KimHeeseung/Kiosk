import requests
import xml.etree.ElementTree as ET
import time, datetime

uri = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
service_key = 'GZzJcb9olEnt8Q15pRWntpSnUZV0S%2BxQ14qJbZ3tUFsEOF4MyliI%2F3KIDxekDb%2Bt6l%2B3DVexcO2zRiIODa4mSg%3D%3D'
service_key_decoding = requests.utils.unquote(service_key)
print('=============== 도로명 주소 & 지번 주소 & 우편번호 =======================')
print('1. 지번으로 검색\n2. 도로명으로 검색\n3. 우편번호\n')

select = input('검색 방법 선택 : ')

if select == '1':
    seach_se = 'dong'
    srchwrd = input('지번 입력(예: 주월동 408-1) : ')
elif select == '2':
    seach_se = 'road'
    srchwrd = input('도로명 입력(예: 서문대로 745) : ')
else:
    seach_se = 'post'
    srchwrd = input('우편번호 입력(예: 61725) : ')
    
cnt = 0
interval = 1200
while True:
    payload = {'ServiceKey': service_key_decoding, 'searchSe': seach_se,
            'srchwrd': srchwrd, 'countPerPage': '10', 'currentPage': '1'}
    resp = requests.get(uri, params=payload)
    if "SERVICE KEY IS NOT REGISTERED ERROR" in resp.text:
        print(f"SERVICE KEY {service_key_decoding} IS NOT REGISTERED ERROR")
    else:
        break
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{cnt*interval/60:.2f}분 경과: {timestamp}")
    cnt += 1
    time.sleep(interval)

print(resp.text)
root = ET.fromstring(resp.text)

newAddressListAreaCd = root.findall("newAddressListAreaCd")

print('=============== 결과 출력 =======================')
    
for r in newAddressListAreaCd:
    print(f'우편번호 : {r.findtext("zipNo")}')
    print(f'도로명 주소 : {r.findtext("lnmAdres")}')
    print(f'지번 주소 : {r.findtext("rnAdres")}')
    print('--------------------------------------------------------------------')


import requests
import xml.etree.ElementTree as ET
import time, datetime
import mysql.connector
import re
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#
# 우편번호 검색기(23년 4월 5일)
#
# 1. 결색 결과는 foundAddr.txt 파일에 저장하고, 검색에 실패한 주소는
#       notFoundAddr.txt 파일에 저장한다.
# 2. plastichero1.g5_kiosk 테이블에서 키오스크(plastichero)의 도로명 주소를 읽어온다.
#       kc_add1, kc_addr2, kc_addr3
# 3.  공공데이터포털(www.data.go.kr)에서 "과학기술정보부 우정사업본부_도로명주소조회서비스"
#       API용 서비스 키를 받고(신청에서 승인까지 하루 정도 소요), 이를 이용해서
#       위에서 읽어온 키오스크 도로명 주소 중 kc_addr1을 검색키로 (복수의) 우편번호와 주소,
#       그리고 지번주소를 받아온다. --> 1:n 매핑이 된다.
# 4. 키오스트 전체 주소(kc_addr1 ~ kc_addr3)와 가장 일치하는 우편번호를 찾는다.
#  

# 1. 결색 결과는 foundAddr.txt 파일에 저장하고, 검색에 실패한 주소는
#       notFoundAddr.txt 파일에 저장한다.
# 우편번호 검색 결과를 저장한다.
sFile = './foundAddr.txt'
with open(sFile, 'w') as f:
    f.truncate(0)
# 우편번호 검색에 실패한 주소를 적는다.
fFile = './notFoundAddr.txt'
with open(fFile, 'w') as f:
    f.truncate(0)

def find_most_similar_string(addr: str, tempAddr: dict) -> str:
    global fFile
    ss = addr.replace(" ", "")
    for l in tempAddr.keys():
        ll = l.replace(" ", "")
        if ss in ll:
            return l
    with open(fFile, 'a') as f:
        f.write(addr + '\n')
    return None


# 2. plastichero1.g5_kiosk 테이블에서 키오스크(plastichero)의 도로명 주소를 읽어온다.
#       kc_add1, kc_addr2, kc_addr3
plastichero1 = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'm-road_0415',
        database = 'plastichero1'
        )
mycursor = plastichero1.cursor()

query = 'SELECT kc_addr1, CONCAT(kc_addr1, " ", kc_addr2, " ", kc_addr3) FROM g5_kiosk ORDER BY kc_no;'
mycursor.execute(query)
resL = mycursor.fetchall()
kAddrs = []
for l in resL:
    # print(l[0])       # tuple data from query above
    kAddrs.append(l)    # ('서울특별시 강남구 선릉로116길 8', '서울특별시 강남구 선릉로116길 8 1층 (삼성동)')

mycursor.close()

# 3.  공공데이터포털(www.data.go.kr)에서 "과학기술정보부 우정사업본부_도로명주소조회서비스"
#       API용 서비스 키를 받고(신청에서 승인까지 하루 정도 소요), 이를 이용해서
#       위에서 읽어온 키오스크 도로명 주소 중 kc_addr1을 검색키로 (복수의) 우편번호와 주소,
#       그리고 지번주소를 받아온다. --> 1:n 매핑이 된다.
uri = 'http://openapi.epost.go.kr/postal/retrieveNewAdressAreaCdService/retrieveNewAdressAreaCdService/getNewAddressListAreaCd'
service_key = 'GZzJcb9olEnt8Q15pRWntpSnUZV0S%2BxQ14qJbZ3tUFsEOF4MyliI%2F3KIDxekDb%2Bt6l%2B3DVexcO2zRiIODa4mSg%3D%3D'
service_key_decoding = requests.utils.unquote(service_key)

seach_se = 'road'   # 우편번호 검색 옵션: 도로명 주소
#pattern = r"\b[가-힣]+로\s*\d+(?:[가-힣]?길)?\s*(?:\d+\S*)?"

file = open(sFile, 'a')
for idx, addrTuple in enumerate(kAddrs):

    addr = addrTuple[0]
    #srchwrd = re.findall(pattern, addr)
    # 주소는 반드시 '서울특별시 양천구 신정이펜2러 55' 식으로 띄어쓰기가 되어야 한다.
    #   (최소한 ..구와 도로명 사이는 띄어쓰기가 되어 있어야 한다.)
    try:
        srchwrd = ' '.join(addr.split()[2:])
    except Exception as e:
        print(type(e), e)
        import pdb; pdb.set_trace()
    
    # 도로명 주소를 가지고 주소를 검색한다.
    payload = {'ServiceKey': service_key_decoding, 'searchSe': seach_se,
            'srchwrd': srchwrd, 'countPerPage': '999', 'currentPage': '1'}
    resp = requests.get(uri, params=payload)
    # API 키가 활성화(등록)되기 전까지는 사용할 수 없다.
    if "SERVICE KEY IS NOT REGISTERED ERROR" in resp.text:
        sys.exit(f"SERVICE KEY {service_key_decoding} IS NOT REGISTERED ERROR")

    root = ET.fromstring(resp.text)
    
    newAddressListAreaCd = root.findall("newAddressListAreaCd")
    
    tempAddr = {}
    for r in newAddressListAreaCd:
        zipNo = r.findtext("zipNo")
        roadAdr = r.findtext("lnmAdres")
        jibAdr = r.findtext("rnAdres")
        tempAddr[roadAdr] = zipNo
        #print(zipNo, roadAdr, jibAdr)

    # 4. 키오스트 전체 주소(kc_addr1 ~ kc_addr3)와 가장 일치하는 우편번호를 찾는다.
    aa = find_most_similar_string(addr, tempAddr)
    if aa != None:
        print(f"우편번호: {tempAddr[aa]}\n검색주소: {addr}, 검색어: {srchwrd}\n결과: {aa}\n")
        print('*'*80)
        file.write(f"우편번호: {tempAddr[aa]}\n검색주소: {addr}, 검색어: {srchwrd}\n결과: {aa}\n\n")
    else:
        # 일치하는 우편번호가 없다면?
        #   1) 서울시의 경우 '성동구아파산로...' 식으로 행정구와 도로명 사이에 띄어쓰기가 안되었거나,
        #   2) 실제로 주소를 잘못 적었을 수도 있다.
        #   3) 확인을 위해서 ./notFoundAddr.txt 파일에 기록한다.
        print(f"{addr}, {srchwrd}  --> {newAddressListAreaCd}")

file.close()


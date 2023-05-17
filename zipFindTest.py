import requests
import xml.etree.ElementTree as ET
import time, datetime
import mysql.connector
import re
import sys
import warnings
from zipFinder import zipFind
warnings.simplefilter(action='ignore', category=FutureWarning)

# plastichero1.g5_kiosk 테이블에서 키오스크(plastichero)의 도로명 주소를 읽어온다.
#       kc_add1, kc_addr2, kc_addr3
plastichero1 = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'm-road_0415',
        database = 'plastichero1'
        )
mycursor = plastichero1.cursor()

#query = 'SELECT kc_addr1, CONCAT(kc_addr1, " ", kc_addr2, " ", kc_addr3) FROM g5_kiosk ORDER BY kc_no;'
query = 'SELECT kc_addr1, CONCAT(kc_addr1, " ", kc_addr2, " ", kc_addr3) FROM g5_kiosk ORDER BY RAND() LIMIT 1;'
mycursor.execute(query)
resL = mycursor.fetchall()
kAddrs = []
for l in resL:
    # print(l[0])       # tuple data from query above
    kAddrs.append(l)    # ('서울특별시 강남구 선릉로116길 8', '서울특별시 강남구 선릉로116길 8 1층 (삼성동)')

mycursor.close()

zipFind(kAddrs)

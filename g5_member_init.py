import pandas as pd
from pyproj import Proj, transform
from idGenerate import generate_unique_id as id_generate
import names, genUsernames
import random, string, re
import datetime
import traceback
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#
# 이 프로그램은 plastichero 사용 회원 2000명의 DB를 생성합니다.
#   ('서울시 휴게음식점 인허가 정보.xlsx' 파일에서 거피숍(업태구분명)만 발췌하여
#    '서울시 회원 정보.xlsx' 파일을 만들었다.) --> 사용할 필요가 없다!!
#
#   1. g5_member에서 필요한 컬럼은 mb_id, mb_name, mb_nick_date(가입날짜), mb_sex, mb_birth, mb_point
#   2. mb_name, mb_sex, mb_birth는 name 및 jumin 모듈로 생성한다.
#   3. mb_id는 mb_name을 해쉬하거나 해서 영문숫자를 조합하여 중복되지 않도록 8~15자로 만든다.
#   4. mb_nick_date는 kiosk 설치일 이후의 날짜를 무작위로 설정하면 된다.
#   5. mb_point는 일단 mb_nick_date에 비례하도록 적당히 설정한다.
#   5.1.    1인당 한 주에 5~10개 정도를 투입하는 것으로 한다.
#   6. 출력 파일은 'g5_member_init.sql'
#

#   2. mb_name, mb_sex, mb_birth는 name 모듈로 생성한다(주민등록번호가 필요하면 jumin 모듈 사용하면 됨)
male_nameBirths, female_nameBirths, nS = names.make_names(2000)
nameBirthSex = []
for k, v in male_nameBirths.items():
    nameBirthSex.append([k, v, 'M'])
for k, v in female_nameBirths.items():
    nameBirthSex.append([k, v, 'F'])
#   nameBirthSex[0]     ['박유준', '19980222', 'M']
#   nameBirthSex[-1]    ['오유림', '20030910', 'F']
#   nameBirthSex[999]   ['홍정우', '19860306', 'M']
#   nameBirthSex[1000]  ['송윤아', '19451117', 'F']

#   4. 출력 파일은 'f5_kiosk_test.sql' (먼저 기존 g5_member 테이블의 모든 레코드를 삭제한다.)
sqlFile = open('g5_member_init.sql', 'w')
sql_query='DELETE FROM g5_member;'
sqlFile.write(sql_query + '\n')

#   3. mb_id는 mb_name을 해쉬하거나 해서 영문숫자를 조합하여 중복되지 않도록 8~15자로 만든다.
#       call genUsernames()
for i in range(len(nameBirthSex)):
    print(nameBirthSex[i], genUsernames.generate_username(nameBirthSex[i][0]))
    mb_id = genUsernames.generate_username(nameBirthSex[i][0])
    mb_name = nameBirthSex[i][0]
    mb_birth = nameBirthSex[i][1]
    mb_sex = nameBirthSex[i][2]
   
    #   4. mb_nick_date는 kiosk 설치일 이후의 날짜를 무작위로 설정하면 된다.
    #       단 키오스크는 2022년 3월 17일부터 2023년 3월 16일까지 설치된 것으로 가정한다.
    #   5. mb_point는 일단 mb_nick_date에 비례하도록 적당히 설정한다.
    #   5.1.    1인당 한 주에 5~10개 정도를 투입하는 것으로 한다.
    start_date = datetime.date(2022,3,17)
    end_date = datetime.date(2023,3,16)
    
    # 임의의 날짜 생성
    random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
    # 임의의 시간 생성 (01:00 ~ 05:00 제외)
    random_hour = random.choice([j for j in range(0, 24) if j not in range(1, 6)])
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    
    # 출력 형식 지정
    mb_nick_date = random_date.strftime('%Y-%m-%d')
    mb_point = int( (random_date - start_date).days * random.randint(5, 10) * 10 / 7 )
    
    sql_query='INSERT INTO g5_member (mb_id, mb_name, mb_nick_date, mb_sex, mb_birth, mb_point, mb_signature, ' + \
            f'mb_memo, mb_lost_certify, mb_profile) VALUES (\'{mb_id}\', \'{mb_name}\', \'{mb_nick_date}\', ' + \
            f'\'{mb_sex}\', \'{mb_birth}\', {mb_point}, \'\', \'\', \'\', \'\');'
    print(sql_query)
    sqlFile.write(sql_query + '\n')
    print(f'{i=}')

sqlFile.close()

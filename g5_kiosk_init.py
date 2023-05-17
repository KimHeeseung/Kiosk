import pandas as pd
from pyproj import Proj, transform
from idGenerate import generate_unique_id as id_generate
import random, string, re
import datetime
import traceback
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#
# 이 프로그램은 5명의 현장 기사가 200대의 kiosk를 관리한다는 가정하에 kiosk 머신 DB를 생성합니다.
#   ('서울시 휴게음식점 인허가 정보.xlsx' 파일에서 편의점(업태구분명)만 발췌하여
#    '서울시 편의점 인허가 정보.xlsx' 파일을 만들었다.)
#
#   1. 파일 '서울시 편의점 인허가 정보.xlsx'의 '서울시 휴게음식점 인허가 정보' 시트로부터
#   2. g5_kiosk (테이블명) 시뮬레이션에 필요한 8개 컬럼 데이터를 가져오되,
#       8개 컬럼 데이터가 모두 채워져 있는 것으로만 가져온다.
#   2.1 중부원점 좌표계를 일반 GIS 좌표계로 변환한다.
#   3. kiosk 설치 일자는 2022년 3월 17일 ~ 2023년 3월 16일로 한다.
#   4. 출력 파일은 'g5_kiosk_test.sql'\으로 하고,
#   4.1 출력 시 g5_kiosk 테이블의 모든 컬럼을 채워준다.
#   4.2 kiosk당 하루 평균 20.00~30.00g 페트병 200개(150~250)개가 투입되고,
#   4.3 수거통의 용량은 450개로 정한다.
#   4.4 따라서 kiosk 설치일로부터 환산해서 평균 200개씩 투입되는 것으로 계산한다.
#   4.5 단, 비회원 투입 비율은 최대 30%까지로 한다.
#

#   1. 파일 '서울시 편의점 인허가 정보.xlsx'의 '서울시 휴게음식점 인허가 정보' 시트로부터
df = pd.read_excel('서울시 편의점 인허가 정보.xlsx', sheet_name='서울시 휴게음식점 인허가 정보',
        usecols = ['인허가일자', '소재지우편번호', '지번주소', '도로명주소', '도로명우편번호',
            '업태구분명', '좌표정보(X)', '좌표정보(Y)'])

#   2. g5_kiosk 시뮬레이션에 필요한 8개 컬럼 데이터를 가져오되,
#       8개 컬럼 데이터가 모두 채워져 있는 것으로만 가져온다.
df = df.dropna(subset=['인허가일자', '소재지우편번호', '지번주소', '도로명주소', '도로명우편번호',
                '업태구분명', '좌표정보(X)', '좌표정보(Y)'], how='any')
df_200 = df.sample(n=200, random_state=random.seed())

# 열 선택
col1 = df_200['인허가일자']
col2 = df_200['소재지우편번호']
col3 = df_200['지번주소']
col4 = df_200['도로명주소']
col5 = df_200['도로명우편번호']
col6 = df_200['업태구분명']
col7 = df_200['좌표정보(X)']        # kc_lat
col8 = df_200['좌표정보(Y)']        # kc_lng

engineer = ['홍길동', '로빈훗', '배트맨', '맥아더', '에바페론']     # 현장기사 5명
engineer_tel = ['010-1234-1234', '010-1324-1324', '010-1243-1243', '010-4321-4321', '010-2134-2134']
#   2.1 중부원점 좌표계를 일반 GIS 좌표계로 변환한다.
proj1, proj2 = Proj(init='epsg:2097'), Proj(init='epsg:4326')

# 주소 예:
#   다음 예에서 (..) 부분은 항상 있는 것으로 간주한다(없으면 해당 레코드 무시)
#   (..) 이전 부분은 코머(,)가 있을 수도 있고 없을 수도 있다.
#   코머가 2개 있으면 최초로 나온 코머를 기준으로 나눈다.
#
#   서울특별시 구로구 남부순환로95길 54, 상가동 1층 111,112호 (개봉동, 삼환아파트)
#   서울특별시 강서구 화곡로20길 42, 1층 (화곡동, 1동)
#   서울특별시 강서구 송정로 37 (공항동)
#
#   --> 정규표현식보다는 split() 메서드가 효율적이다.
#
#HANS p_comma = re.compile(r'(.*?),')
#HANS p_bracket = re.compile(r'\((.*?)\)')

#   3. kiosk 설치 일자는 2022년 3월 17일 ~ 2023년 3월 16일로 한다.
start_date = datetime.date(2022,3,17)
end_date = datetime.date(2023,3,16)

#   4. 출력 파일은 'f5_kiosk_init.sql'(먼저 초기화, 즉, 모든 데이터를 삭제한다.)
sqlFile = open('g5_kiosk_init.sql', 'w')
sql_query='DELETE FROM g5_kiosk;'
sqlFile.write(sql_query + '\n')

# 행 단위 데이터 읽기
idx = 0
for index, row in df_200.iterrows():
    try:
        col1, col2, kc_addr_jibeon, col4, col5, col6 = row['인허가일자'], row['소재지우편번호'], row['지번주소'], row['도로명주소'], row['도로명우편번호'], row['업태구분명']

        e_indx = random.randint(0, 4)
        idx += 1
        kc_kiosk_id = id_generate(str(col1) + str(idx))
        kc_engineer = engineer[e_indx]
        kc_engineer_tel=engineer_tel[e_indx]
        print(f'{kc_kiosk_id=}\n{kc_engineer=}\n{kc_engineer_tel=}')
        
        eng_pass = ''.join(random.choices(string.digits, k=random.randint(4, 10)))
        kio_pass = ''.join(random.choices(string.digits, k=random.randint(4, 10)))
        kc_engineer_password=eng_pass
        kc_door_password=kio_pass
        print(f'{kc_engineer_password=}\n{kc_door_password=}')
        
        kc_zip1, kc_zip2 = str(col2)[:3], str(col2)[-3:]
        print(f'{kc_zip1=}')
        print(f'{kc_zip2=}')
        try:
            chk_zip = int(kc_zip1) - int(kc_zip2)
        except Exception as e:
            print(e, type(e))
            idx -= 1
            import pdb; pdb.set_trace()

        try:
            tmpAddr = col4.split('(')
            kc_addr3 = '(' + tmpAddr[1].strip()
            tmpAddr = tmpAddr[0].split(',')
            if len(tmpAddr) == 1:
                kc_addr1 = tmpAddr[0].strip()
                kc_addr2 = ''
            else:
                kc_addr1 = tmpAddr[0].strip()
                kc_addr2 = tmpAddr[1].strip()
        except Exception as e:
            print(e, type(e))
            idx -= 1
            import pdb; pdb.set_trace()
        print(f'{kc_addr1=}')
        print(f'{kc_addr2=}')
        print(f'{kc_addr3=}')
        
        print(f'{kc_addr_jibeon=}')
        
        kc_lng, kc_lat = transform(proj1, proj2, row['좌표정보(X)'], row['좌표정보(Y)'])
        try:
            chk_lat = float(kc_lng) - float(kc_lat)
        except Exception as e:
            print(e, type(e))
            idx -= 1
            import pdb; pdb.set_trace()
        print(f'{kc_lat=}\n{kc_lng=}')

        # 임의의 날짜 생성
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        # 임의의 시간 생성 (01:00 ~ 05:00 제외)
        random_hour = random.choice([i for i in range(0, 24) if i not in range(1, 6)])
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        d_now = datetime.datetime.now()
        s_days = (d_now.date() - random_date).days
        s_hours = d_now.strftime('%H')
        
        # 출력 형식 지정
        formatted_datetime1 = random_date.strftime('%Y-%m-%d')
        formatted_datetime2 = random_date.strftime('%Y-%m-%d') + f' {random_hour:02d}:{random_minute:02d}:{random_second:02d}'
        
        kc_start=formatted_datetime1
        kc_end='9999-12-31'
        kc_datetime=formatted_datetime2
        print(f'{kc_start=}\n{kc_end=}\n{kc_datetime=}')

#   4.2 kiosk당 하루 평균 20.00~30.00g 페트병 200개(150~250)개가 투입되고,
#   4.3 수거통의 용량은 450개로 정한다.
#   4.4 따라서 kiosk 설치일로부터 환산해서 평균 200개씩 투입되는 것으로 계산한다.
#   4.5 단, 비회원 투입 비율은 최대 30%까지로 한다.
        kc_current_weight = random.uniform(20.00, 30.00) * random.uniform(150, 250) * int(s_hours) / 24
        t_num = random.uniform(150, 250)
        kc_accumulated_weight =  random.uniform(20.00, 30.00) * t_num * s_days
        kc_accumulated_save_point = int(t_num * s_days * 10 * 0.7)
        kc_accumulated_donation_point = int(kc_accumulated_save_point * 0.1)
        print(kc_current_weight, t_num, kc_accumulated_weight, kc_accumulated_save_point, kc_accumulated_donation_point)
        
#   4. 출력 파일은 'f5_kiosk_init.sql'\으로 하고,
#   4.1 출력 시 g5_kiosk 테이블의 모든 컬럼을 채워준다.
        sql_query='INSERT INTO g5_kiosk (kc_kiosk_id, kc_engineer, kc_engineer_tel, kc_engineer_password, ' + \
                'kc_door_password, kc_zip1, kc_zip2, kc_addr1, kc_addr2, kc_addr3, kc_addr_jibeon, kc_lat, kc_lng, ' + \
                'kc_current_weight, kc_accumulated_weight, kc_accumulated_save_point, kc_accumulated_donation_point, ' + \
                f'kc_start, kc_end, kc_datetime) VALUES (\'{kc_kiosk_id}\', \'{kc_engineer}\', \'{kc_engineer_tel}\', ' + \
                f'\'{kc_engineer_password}\', \'{kc_door_password}\', \'{kc_zip1}\', \'{kc_zip2}\', \'{kc_addr1}\', \'{kc_addr2}\', ' + \
                f'\'{kc_addr3}\', \'{kc_addr_jibeon}\', {kc_lat}, {kc_lng}, {kc_current_weight}, {kc_accumulated_weight}, ' + \
                f'{kc_accumulated_save_point}, {kc_accumulated_donation_point}, \'{kc_start}\', \'{kc_end}\', \'{kc_datetime}\');'

        print(sql_query)
        sqlFile.write(sql_query + '\n')
        print()
    except Exception as e:
        print(e, type(e))
        print(traceback.format_exc())
        idx -= 1
        import pdb; pdb.set_trace()
    print(f'{idx+1} 레코그 생성')
    if idx >= 200:
        break

sqlFile.close()

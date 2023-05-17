import mysql.connector
import datetime, random, sys
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


#
# 이 프로그램은 200대의 키오스크 현재 상태를 20분 간격으로 업데이트 한다.
# 시뮬레이션에서는 2%(4대)에서 고장(E001~E012)이 발생하고, 3시간 후 복구된다고 가정한다.
# 고장 이력이 있어야 하므로 INSERT 방식으로 레코드를 삽입한다.
# 여기서는 최초 상태만 기록한다.
#
# 1. g5_kiosk_status 테이블의 모든 레코드를 삭제한다.
# 2. g5_kiosk 테이블에서 키오스크 명단을 받아서 모든 키오스크를 초기화한다.

alarm_tmp = '알람 없음,상부 DOOR OPEN,하부 DOOR OPEN,투입부 DOOR OPEN ERROR,투입부 DOOR CLOSE ERROR,' + \
        '파쇄부 DOOR OPEN ERROR,파쇄부 DOOR CLOSE ERROR,파쇄모터 과부하 ERROR,컨베이어 구동 ERROR,' + \
        '카메라 동작 ERROR,INPUT 통신 ERROR,OUTPUT 통신 ERROR,CAS 저울 통신 ERROR'
alarm_msg = alarm_tmp.split(',')

alarm_tmp = '알람이 초기화되어 정상 가동한 상태,상부(판넬부) DOOR가 열려있는지 점검,' + \
        '하부(판넬부) DOOR가 열려있는지 점검,투입부 DOOR OPEN 감지센서 및 모터 구동 상태 점검,' + \
        '투입부 DOOR CLOSE 감지센서 및 모터 구동 상태 점검,파쇄부 DOOR OPEN 감지센서 및 모터 구동 상태 점검,' + \
        '파쇄부 DOOR CLOSE 감지센서 및 모터 구동 상태 점검,파쇄모터 과부하 발생으로 이물질 끼임 상태 점검,' + \
        '컨베이어 물체 감지 센서 및 모터 구동 상태 점검,카메라 동작 상태 점검,' + \
        'INPUT 모듈 통신 배선 및 통신 연결 상태 점검,OUTPUT 모듈 통신 배선 및 통신 연결 상태 점검,' + \
        'CAS 저울 통신 배선 및 통신 연결 상태 점검'
alarm_content = alarm_tmp.split(',')

plastichero1 = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'm-road_0415',
        database = 'plastichero1'
        )
mycursor = plastichero1.cursor()

# 1. g5_kiosk_status 테이블의 모든 레코드를 삭제한다.
query = "DELETE FROM g5_kiosk_status;"
mycursor.execute(query)

# 2. g5_kiosk 테이블에서 키오스크 명단을 받아서 모든 키오스크를 초기화한다.
query = 'SELECT kc_kiosk_id from g5_kiosk;'
mycursor.execute(query)
kiosks = mycursor.fetchall()

tNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

query = ''
for ks in kiosks:
    print(ks[0])
    query += 'INSERT INTO g5_kiosk_status (kc_kiosk_id, kc_alarm_code, kc_alarm_msg, kc_check_msg, kc_alarm_datetime) ' + \
            f'VALUES (\'{ks[0]}\', \'E000\', \'{alarm_msg[0]}\', \'{alarm_content[0]}\', \'{tNow}\');'

mycursor.execute(query)

mycursor.close()

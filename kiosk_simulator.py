import mysql.connector
import datetime, random, sys
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#
# 이 프로그램은 plastichero를 사용하는 회원을 시뮬레이션한다.
#
# 1. plastichero(키오스크)가 g5_member에 속한 회원(g5_member.mb_id)임을 확인한다.
#       즉, 특정 g5_member.mb_id 값을 갖는 회원이 g5_member.mb_point의 포인트를
#       가지고 있다(무작위로 회원 한 명을 고른다.).
#       --> select mb_id, mb_point from g5_member order by rand() limit 1; --> g5member(변수)
#       --> (2000명의 회원은 한 주 평균 n개의 페트병을 투입한다고 가정한다.
#           따라서 회원은 하루 n/7개 꼴로 투입하고, 키오스크는 2000n/1400개가 투입된다.
#           시뮬레이션 목적 상 n 값을 49개라고 가정한다.
# 2. 회원은 자신이 속한 소재지 근처에 있는 plastichero(g5_kiosk.kc_kiosk_id)를
#       사용하며(시뮬레이션에서 제외), 하루 평균 7병의 페트병을 투입한다고 가정한다
#       (50% 확률로 0개, 나머지 50%의 확률로 1~27개를 투입한다.). 페트병 투입 시마다(투입 행위가 완료된 후)
#       수거통 무게가 증가하고, 총 수거 실적과 기부금 발생 포인트가 증가한다
#       ************************************************************************************
#       키오스크 중 무작위로 1% 정도(2대)를 골라 3시간 동안 고장(E001~E012) 상태로 둔다.
#       ************************************************************************************
#       (g5_kiosk.kc_current_weight, g5_kiosk.kc_accumulated_save_point,
#        g5_kiosk.kc_accumulated_donation_point, g5_kiosk.kc_datetime).
#       tNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') // Python
#       select kc_kiosk_id from g5_kiosk order by rand() limit 1; -- g5kiosk(변수)
#       update g5_kiosk set kc_current_weight = .(계산한다).., kc_accumulated_weight = ...,
#           ..., kc_datetime = tNow where g5_kiosk.kc_kiosk_id = g5kiosk;
#       def pet_insertion():  // 파이썬
#           rand_num = random.random()
#           if rand_num < 0.5:
#               return 0
#           else:
#               return random.randint(1, 27)
# 3. 이때 g5_kiosk_collection 테이블의 g5_kiosk_collection.mb_id,
#       g5_kiosk_collection.kc_bottle_weight, g5_kiosk_collection.kc_save_point,
#       g5_kiosk_collection.kc_donation_point, g5_kiosk_collection.datetime,
#       g5_kiosk_collection.kc_rel_action 값이 수정된다.
#       update g5_kiosk_collection set kc_bottle_weight = ..., kc_save_point = ...
#           .... kc_rel_action = g5relAction     -- 이 값을 g5relAction이라고 하자.
#           where mb_id = g5member;
# 4. 위의  g5_kiosk_collection.kc_rel_action 값을 가지고 g5_point 테이블을 업데이트한다.
#       g5_point.mb_id가 같은 회원의 g5_point.po_datetime, g5_point.point 등등의 값을
#       업데이트하고 g5_kiosk_collection.kc_rel_action 값을 g5_point.po_rel-action
#       값으로 적어준다.
# 5. 마지막으로 g5_member.mb_id의 g5_member.mb_point 값을 업데이트하고 종료한다.
# 6. 임의의 회원에 대해서 상기 과정을 되풀이 한다.
#

def pet_insertion():
    rand_num = random.random()
    if rand_num < 0.5:
        return 0
    else:
        return random.randint(1, 27)

while True:
    tNow = datetime.datetime.now().replace(microsecond=0)
    print('\n' + '*' * 80)
    print(f'현재 시각: {tNow}\n\n')

    nBottle = pet_insertion()
    if nBottle == 0:
        print('페트병 투입하지 않았습니다~')
        time.sleep(10)
    else:
        print(f'페트병 {nBottle}개 투입~\n')
    
    plastichero1 = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'm-road_0415',
            database = 'plastichero1'
            )
    mycursor = plastichero1.cursor()
    
    # 1. plastichero(키오스크)가 g5_member에 속한 회원(g5_member.mb_id)임을 확인한다.
    #       즉, 특정 g5_member.mb_id 값을 갖는 회원이 g5_member.mb_point의 포인트를
    #       가지고 있다(무작위로 회원 한 명을 고른다.).
    #       --> select mb_id, mb_point from g5_member order by rand() limit 1; --> g5member(변수)
    #       --> (2000명의 회원은 한 주 평균 n개의 페트병을 투입한다고 가정한다.
    #           따라서 회원은 하루 n/7개 꼴로 투입하고, 키오스크는 2000n/1400개가 투입된다.
    #           시뮬레이션 목적 상 n 값을 50개라고 가정한다.
    #
    query = 'SELECT mb_id, mb_point FROM g5_member ORDER BY rand() LIMIT 1;'
    mycursor.execute(query)
    g5_member_mb_id, g5_member_mb_point = mycursor.fetchall()[0]
    print(f'{g5_member_mb_id=}, {g5_member_mb_point=}')
    
    # 2. 회원은 자신이 속한 소재지 근처에 있는 plastichero(g5_kiosk.kc_kiosk_id)를
    #       사용하며(시뮬레이션에서 제외), 하루 평균 7병의 페트병을 투입한다고 가정한다
    #       (50% 확률로 0개, 나머지 50%의 확률로 1~27개를 투입한다.). 페트병 투입 시마다(투입 행위가 완료된 후)
    #       수거통 무게가 증가하고, 총 수거 실적과 기부금 발생 포인트가 증가한다
    #       ************************************************************************************
    #       키오스크 중 무작위로 1% 정도(2대)를 골라 3시간 동안 고장(E001~E012) 상태로 둔다.
    #       (먼저 kiosk_status_init.py 코드를 실행시켜 키오스크를 초기화한다.... 한슈)
    #       ************************************************************************************
    #       (g5_kiosk.kc_current_weight, g5_kiosk.kc_accumulated_save_point,
    #        g5_kiosk.kc_accumulated_donation_point, g5_kiosk.kc_datetime).
    #       tNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') // Python
    #       select kc_kiosk_id from g5_kiosk order by rand() limit 1; -- g5kiosk(변수)
    #       update g5_kiosk set kc_current_weight = .(계산한다).., kc_accumulated_weight = ...,
    #           ..., kc_datetime = tNow where g5_kiosk.kc_kiosk_id = g5kiosk;
    #       def pet_insertion():  // 파이썬
    #           rand_num = random.random()
    #           if rand_num < 0.5:
    #               return 0
    #           else:
    #               return random.randint(1, 27)
    query = 'SELECT kc_kiosk_id, kc_current_weight, kc_accumulated_weight, kc_accumulated_save_point, ' + \
            'kc_accumulated_donation_point, kc_datetime FROM g5_kiosk ORDER BY rand() LIMIT 1;'
    mycursor.execute(query)

    g5_kiosk_kc_kiosk_id, g5_kiosk_kc_current_weight, g5_kiosk_kc_accumulated_weight, \
    g5_kiosk_kc_accumulated_save_point, g5_kiosk_kc_accumulated_donation_point, \
    g5_kiosk_kc_datetime  = mycursor.fetchall()[0]
    print(f'{g5_kiosk_kc_kiosk_id=}, {g5_kiosk_kc_current_weight=}, {g5_kiosk_kc_accumulated_weight=}, ' + \
            f'{g5_kiosk_kc_accumulated_save_point=}, {g5_kiosk_kc_accumulated_donation_point=}, ' + \
            f'{g5_kiosk_kc_datetime=}')
    
    
    pet_weight = random.uniform(20.00, 30.00) * nBottle
    g5_kiosk_kc_current_weight += pet_weight
    g5_kiosk_kc_accumulated_weight += pet_weight
    g5_kiosk_kc_accumulated_save_point += nBottle * 10
    g5_kiosk_kc_accumulated_donation_point += nBottle
    g5_kiosk_kc_datetime = tNow.strftime('%Y-%m-%d %H:%M:%S')
    rel_action_id = g5_kiosk_kc_kiosk_id + '-' + tNow.strftime('%Y%m%d%H%M%S') + str(random.randint(11, 99))
    print(f'{nBottle=}, {pet_weight=}')
    print(f'{g5_kiosk_kc_kiosk_id=}, {g5_kiosk_kc_current_weight=}, {g5_kiosk_kc_accumulated_weight=}, ' + \
            f'{g5_kiosk_kc_accumulated_save_point=}, {g5_kiosk_kc_accumulated_donation_point=}, ' + \
            f'{g5_kiosk_kc_datetime=}')
    query = f'UPDATE g5_kiosk SET kc_current_weight = {g5_kiosk_kc_current_weight}, ' + \
            f'kc_accumulated_weight = {g5_kiosk_kc_accumulated_weight}, ' + \
            f'kc_accumulated_save_point = {g5_kiosk_kc_accumulated_save_point}, ' + \
            f'kc_accumulated_donation_point = {g5_kiosk_kc_accumulated_donation_point}, ' + \
            f'kc_datetime = \'{g5_kiosk_kc_datetime}\' WHERE kc_kiosk_id = \'{g5_kiosk_kc_kiosk_id}\';'
    mycursor.execute(query)
    #HANS mycursor.execute(f'select * from g5_kiosk where kc_kiosk_id = \'{g5_kiosk_kc_kiosk_id}\';')
    #HANS print('*'*80)
    #HANS print(mycursor.fetchall())
    
    
    # 3. 이때 g5_kiosk_collection 테이블의 g5_kiosk_collection.mb_id,
    #       g5_kiosk_collection.kc_bottle_weight, g5_kiosk_collection.kc_save_point,
    #       g5_kiosk_collection.kc_donation_point, g5_kiosk_collection.datetime,
    #       g5_kiosk_collection.kc_rel_action 값이 수정된다.
    #       update g5_kiosk_collection set kc_bottle_weight = ..., kc_save_point = ...
    #           .... kc_rel_action = g5relAction     -- 이 값을 g5relAction이라고 하자.
    #           where mb_id = g5member;
    #HANS query = f'UPDATE g5_kiosk_collection SET kc_bottle_weight = {pet_weight}, ' + \
    #HANS        f'kc_save_point = {nBottle * 10}, kc_donation_point = {nBottle}, ' + \
    #HANS        f'kc_datetime = \'{g5_kiosk_kc_datetime}\' WHERE mb_id = \'{g5_member_mb_id}\' and ' + \
    #HANS        f'kc_kiosk_id = \'{g5_kiosk_kc_kiosk_id}\';'
    kc_rel_action = po_rel_action = rel_action_id
    try:
        query = 'INSERT INTO g5_kiosk_collection (mb_id, kc_kiosk_id, kc_bottle_weight, kc_save_point, kc_donation_point, ' + \
                f'kc_datetime, kc_rel_action) VALUES (\'{g5_member_mb_id}\', \'{g5_kiosk_kc_kiosk_id}\', {pet_weight}, ' + \
                f'{nBottle * 10}, {nBottle}, \'{g5_kiosk_kc_datetime}\', \'{kc_rel_action}\');'
        print(query)
        print(f'{kc_rel_action=}')
        mycursor.execute(query)
        mycursor.execute(f'SELECT * FROM g5_kiosk_collection WHERE mb_id = \'{g5_member_mb_id}\' and kc_kiosk_id = \'{g5_kiosk_kc_kiosk_id}\';')
        print('*'*80)
        print(mycursor.fetchall())
    except Exception as e:
        print(e, type(e))
        import pdb; pdb.set_trace()
    
    
    
    # 4. 위의  g5_kiosk_collection.kc_rel_action 값을 가지고 g5_point 테이블을 업데이트한다.
    #       g5_point.mb_id가 같은 회원의 g5_point.po_datetime, g5_point.point 등등의 값을
    #       업데이트하고 g5_kiosk_collection.kc_rel_action 값을 g5_point.po_rel-action
    #       값으로 적어준다.
    try:
        query = f'SELECT po_use_point, po_mb_point FROM g5_point WHERE mb_id = \'{g5_member_mb_id}\';'
        mycursor.execute(query)
    except Exception as e:
        print(e, type(e))
        import pdb; pdb.set_trace()
    g5_point_po_use_point, g5_point_po_mb_point = mycursor.fetchall()[0]
    
    g5_point_po_use_point += nBottle * 10
    g5_point_po_mb_point += nBottle * 10
    query = f'INSERT INTO g5_point (mb_id, po_datetime, po_content, po_point, po_use_point, po_expired, po_mb_point, po_rel_action) ' + \
            f'VALUES (\'{g5_member_mb_id}\', \'{g5_kiosk_kc_datetime}\', \'페트병 수거 포인트 적립\', {nBottle * 10}, ' + \
            f'{g5_point_po_use_point}, 0, {g5_point_po_mb_point}, \'{po_rel_action}\');'
    mycursor.execute(query)
    mycursor.execute(f'select * from g5_point where mb_id = \'{g5_member_mb_id}\';')
    print('*'*80)
    print(mycursor.fetchall())
    
    # 5. 마지막으로 g5_member.mb_id의 g5_member.mb_point 값을 업데이트하고 종료한다.
    query = f'UPDATE g5_member SET mb_point = {g5_point_po_mb_point}, mb_datetime = \'{g5_kiosk_kc_datetime}\' ' + \
            f'WHERE mb_id = \'{g5_member_mb_id}\';'
    mycursor.execute(query)
    
    mycursor.close()
    
    time.sleep(10)

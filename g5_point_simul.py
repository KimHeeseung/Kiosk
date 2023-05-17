import mysql.connector
import datetime, random

plastichero1 = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'm-road_0415',
        database = 'plastichero1'
        )
mycursor = plastichero1.cursor()

query = 'select mb_id, mb_point from g5_member'
mycursor.execute(query)
members = mycursor.fetchall()

def generate_zero():
    '''
    0(포인트 발생)을 70%, 1(포인트 지급/사용)을 30% 발생시킨다.
    '''
    rand = random.random()
    if rand <= 0.7:
        return 0
    else:
        return 1

#
# 현재 시각을 기준으로 point를 발생시킨다.
#
#   1. 회원은 무작위로 5개까지 페트병을 집어넣되,
#   2. 30% 정도는 이미 발생한 포인트를 사용하는 경우를 고려한다.
#
for row in members:
    mb_id = row[0]
    po_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    po_point = random.randint(0, 5) * 10
    po_expired = generate_zero()
    print(f'{row=}, {po_expired=}')
    if po_expired == 0:
        po_expire_date = po_datetime.split()[0]
        po_sign = 1
        po_use_point = row[1] + po_point
    else:
        po_expire_date = '9999-12-31'
        po_sign = -1
        po_use_point = row[1]
    po_mb_point = po_use_point + po_sign * po_point
    
    print(f'{mb_id=}, {po_datetime=}, {po_point=}, {po_use_point=}, {po_expired=}, {po_expire_date=}, {po_mb_point=}')
    point_query=f'UPDATE g5_point set po_datetime=\'{po_datetime}\', po_point={po_point}, ' + \
            f'po_use_point={po_use_point}, po_expired={po_expired}, po_expire_date=\'{po_expire_date}\', ' + \
            f'po_mb_point={po_mb_point} where mb_id=\'{mb_id}\';'
    mycursor.execute(point_query)
    mem_query=f'UPDATE g5_member set mb_point={po_mb_point} where mb_id=\'{mb_id}\';'
    mycursor.execute(mem_query)


# 검증
ver_query='select a.mb_id, a.mb_point, b.po_mb_point from g5_member as a inner join g5_point as b on a.mb_id = b.mb_id;'
mycursor.execute(ver_query)
members = mycursor.fetchall()
for l in members:
    if l[1] != l[2]:
        print(l)

mycursor.close()

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

for row in members:
    mb_id = row[0]
    po_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    po_point = random.randint(0, 5) * 10
    po_expired = generate_zero()
    print(f'{row=}, {po_expired=}')
    if po_expired == 0:
        po_expire_date = po_datetime
        po_sign = 1
        po_use_point = row[1] + po_point
    else:
        po_expire_date = '9999-12-31'
        po_sign = -1
        po_use_point = row[1]
    po_mb_point = po_use_point + po_sign * po_point
    
    print(f'{mb_id=}, {po_datetime=}, {po_point=}, {po_use_point=}, {po_expired=}, {po_expire_date=}, {po_mb_point=}')
    sql_query='UPDATE g5_point (mb_id, po_datetime, po_point, po_use_point, po_expired, po_expired_date, ' + \
            f'po_mb_point) VALUES (\'{mb_id}\', \'{po_datetime}\', {po_point}, {po_use_point}, {po_expired}, ' + \
            f'\'{po_expire_date}\', {po_mb_point});'
    print(sql_query)
    input()


import mysql.connector
import datetime, random

#
#   g5_member 테이블을 가지고 g5_point 테이블을 초기화는 프로그렘이다.
#   2023년 3월 1일 05시 기준으로 모든 데이터를 g5_member 테이블의 mb_id, mb_point를
#   g5_point 테이블의 mb_id, po_use_point와 일치시킨다.
#
# 1. g5_point 테이블의 모든 데이터를 삭제한다.
# 2. g5_member 테이블에서 필요한 데이터를 가져온다.

plastichero1 = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'm-road_0415',
        database = 'plastichero1'
        )
mycursor = plastichero1.cursor()

# 1. g5_point 테이블의 모든 데이터를 삭제한다.
query = 'delete from g5_point'
mycursor.execute(query)

# 2. g5_member 테이블에서 필요한 데이터를 가져온다.
query = 'select mb_id, mb_point from g5_member'
mycursor.execute(query)
members = mycursor.fetchall()

for row in members:
    mb_id = row[0]
    po_datetime = '2023-03-01 05:00:00'
    po_point = 0
    po_expired = 0
    print(f'{row=}, {po_expired=}')
    po_expire_date = '2023-03-01'
    po_use_point = row[1]
    po_mb_point = po_use_point
    
    print(f'{mb_id=}, {po_datetime=}, {po_point=}, {po_use_point=}, {po_expired=}, {po_expire_date=}, {po_mb_point=}')
    sql_query='INSERT INTO  g5_point (mb_id, po_datetime, po_point, po_use_point, po_expired, po_expire_date, ' + \
            f'po_mb_point) VALUES (\'{mb_id}\', \'{po_datetime}\', {po_point}, {po_use_point}, {po_expired}, ' + \
            f'\'{po_expire_date}\', {po_mb_point});'
    print(sql_query)
    mycursor.execute(sql_query)

mycursor.close()

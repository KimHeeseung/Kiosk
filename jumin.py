import datetime, calendar
import random


def last(*args):
    # 각 자릿수에 2,3,4,5,6,7,8,9,2,3,4,5를 곱한 값을 합한 다음 11로 나눈다.
    # 그 값을 11에서 빼준다.
    lm = 11 - sum(int(args[i]) * (i % 8 + 2) for i in range(12)) % 11
    return lm if lm <= 9 else lm % 10


def back(year, month, day, gender):
    #ju = [int(d) for d in str(year % 100)[::-1]]
    ju = [int(d) for d in '{:02d}'.format(year % 100)]
    ju += [int(d) for d in '{:02d}{:02d}'.format(month, day)]
    ju += [int(d) for d in str(gender)]
    ju += [random.randint(0, 9) for i in range(5)]
    try:
        ju += [last(*ju)]
    except Exception as e:
        print(e, type(e))
        import pdb; pdb.set_trace()
    return ''.join(str(d) for d in ju)


def jumin():
    '''
    주민등록번호 생성기: 1940년 이후 출생자로
    '''
    result = []
    year = random.randint(1940, datetime.datetime.now().year)
    month = random.randint(1, 12)
    if calendar.isleap(year):
        max_days_per_month = [31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        max_days_per_month = [31,28,31,30,31,30,31,31,30,31,30,31]
    day = random.randint(1, max_days_per_month[month-1])
    date = datetime.date(year, month, day)
    if year >= 2000:
        gender = random.randint(3, 4)
    else:
        gender = random.randint(1, 2)
    # 2000년 이후 출생자는 남성 3, 여성 4로 바뀐다.
    ju = back(year, month, day, gender)
    return ju
    
def verify(ap, di=None):
    if not ap:
        print('no arguments.')
        return False
    if di:
        ap = ap.replace('-', '')
    if len(ap) != 13:
        print('not valid length.')
        return False
    ju = list(ap)
    year = int(('20' if ju[6] > '2' else '19') + ap[:2])
    month = int(ap[2:4])
    day = int(ap[4:6])
    try:
        dt = datetime.date(year, month, day)
    except ValueError:
        print('not valid date (yyMMdd).')
        return False
    if ap[:6] != '{:02d}{:02d}{:02d}'.format(year % 100, month, day):
        print('not valid date (yyMMdd).')
        return False
    if int(ju[12]) != last(*ju):
        print('not valid ssn (last number not match).')
        return False
    return True
    
if __name__ == '__main__':
    ap = '591023-1023811'
    res = verify(ap, di='-')
    print(res)
    ap = '5910231023811'
    res = verify(ap)
    print(res)
    for i in range(10000):
        res = jumin()
        print(res[:6]+'-'+res[6:], end='\t')


import random
import datetime
import pandas as pd

def make_names(n):
    """
    이 프로그램은 len(last_name_keys) * len(first_names) 개의 이름을 만들 수 있다.
    KOSIS 자료(https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1IN15SD)에서
    '성씨, 본관별 인구(5인 이상) - 전국' 자료를 이용했다.
    1. 자료로부터 제목과 첫 데이터 라인을 제외하고 읽어들인다.
    2. 성씨 한자명이 같으면 같은 성(한글로)으로 간주하되,
    3. 상위 50개를 발췌한다.
    4. 남녀 각각 n/2 명씩 이름과 생년월일을 생성한다.
    5. 만일 생성된 명단이 각각 n/2개에 미달하면 n(Male), n(Female), n/2 중
        가장 작은 수만큼 남녀 명단을 작성한다.
    """
    # 1. 자료로부터 제목과 첫 데이터 라인을 제외하고 읽어들인다.
    df = pd.read_excel('성씨ㆍ본관별_인구_5인_이상___전국_20230321112257.xlsx', sheet_name='데이터',
                    usecols = ['성씨, 본관별', '인구 비율'], skiprows=range(1, 2))
    last_names_dic = {}
    for idx, row in df.iterrows():
        k, v = row['성씨, 본관별'], row['인구 비율']
        key = k.split('(')[0]
        # 2. 성씨 한자명이 같으면 같은 성(한글로)으로 간주하되,
        if key not in last_names_dic.keys():
            last_names_dic[key] = v * 100.0
        else:
            last_names_dic[key] += v * 100.0
    # last_names_dic.items()는 dict_items 자료형이다.
    sorted_names = sorted(last_names_dic.items(), key = lambda x: x[1], reverse=True)
    # sorted_names는 list 자료형이다.
    # 3. 상위 50개를 발췌한다.
    last_names_dic = dict(sorted_names[:50])

    male_names = ["서준", "하준", "예준", "도윤", "시우", "주원", "유준", "준서", "민준", "지호", "지후",
            "준혁", "재윤", "준우", "현우", "지훈", "우진", "성민", "예성", "시후", "승현", "승우", "시현",
            "정우", "태윤", "재원", "현준", "하율", "윤우", "승민", "현성", "은찬", "도현", "은우", "영준",
            "성준", "동현", "진우", "준성", "예찬", "재민", "성우", "윤호", "민재", "정현", "재훈", "태민",
            "승재", "준영", "건우", "시온", "정민", "주영", "윤성", "태현", "영재", "영호", "재현", "우빈",
            "태준", "승훈", "한결", "민성", "준희", "도혁", "민건", "수현", "재원", "시헌", "지안", "윤재",
            "성진", "현승", "재우", "준영", "건우", "민준", "상민", "지섭", "동하", "민호", "현빈", "현수",
            "은성", "현서", "주현", "준수", "시혁", "효준", "승호", "우주", "영민", "상윤", "시훈", "상호",
            "준민", "주원", "도원", "원준", "태호"]
    
    female_names = ["서연", "지우", "서윤", "지민", "하은", "민서", "예은", "채원", "지유", "수아", "수빈",
            "예린", "지아", "소율", "예나", "유진", "하윤", "지원", "윤서", "다은", "채은", "예나", "은서",
            "예지", "소윤", "지안", "소민", "수현", "유나", "은영", "서현", "수민", "은지", "수진", "은서",
            "지현", "가은", "현서", "하진", "혜원", "현주", "아름", "예서", "예빈", "승아", "하늘", "지은",
            "다인", "지연", "채영", "민지", "예슬", "서아", "하랑", "혜인", "민아", "아현", "채린", "은영",
            "지우", "시은", "예은", "혜원", "은채", "소연", "현지", "승희", "하경", "현진", "윤아", "가희",
            "민주", "시연", "시아", "은주", "주아", "다현", "수연", "예지", "수현", "하랑", "미소", "윤지",
            "예림", "가온", "하율", "서은", "채아", "유경", "채민", "서영", "예솔", "한별", "아린", "승연",
            "주하", "가람", "유림", "은경", "은정"]
    
    last_name_keys = list(last_names_dic.keys())
    last_name_values = list(last_names_dic.values())
    maxName = len(last_name_keys) * (len(male_names) + len(female_names))
    
    full_mnames = {}
    full_fnames = {}
    
    # 1940년 1월 1일 이후 출생자 ~ 현재 기준 10세 이상자
    start_date = datetime.datetime(1940, 1, 1)
    end_date = datetime.datetime.now() - datetime.timedelta(days=365*10)
    
    flag_male = 1
    n_dupl = n_mdupl = n_fdupl = 0
    for idx in range(maxName):
        sel_last_name = random.choices(last_name_keys, weights=last_name_values)[0]
        if flag_male == 1:
            name = sel_last_name + random.choice(male_names)
            if name not in full_mnames.keys():
                random_days = random.randint(0, (end_date - start_date).days)
                random_date = start_date + datetime.timedelta(days = random_days)
                full_mnames[name] = random_date.strftime('%Y%m%d')
                #print(f'{idx + 1}: {name}, {full_mnames[name]}')
            else:
                n_mdupl += 1
                n_dupl += 1
            flag_male = 1 - flag_male
        else:
            name = sel_last_name + random.choice(female_names)
            if name not in full_fnames.keys():
                random_days = random.randint(0, (end_date - start_date).days)
                random_date = start_date + datetime.timedelta(days = random_days)
                full_fnames[name] = random_date.strftime('%Y%m%d')
                #print(f'{idx + 1}: {name}, {full_fnames[name]}')
            else:
                n_fdupl += 1
                n_dupl += 1
            flag_male = 1 - flag_male

    # 4. 남녀 각각 n/2 명씩 이름과 생년월일을 생성한다.
    # 5. 만일 생성된 명단이 각각 n/2개에 미달하면 n(Male), n(Female), n/2 중
    #       가장 작은 수만큼 남녀 명단을 작성한다.
    #print(f'before: {len(full_mnames.keys())} cf. {maxName=} / {n_mdupl=}')
    nM = len(full_mnames); nF = len(full_fnames)
    nS = min(nM, nF, int(n/2))
    keys = random.sample(list(full_mnames.keys()), k=nS)
    selected_mnames = {k: full_mnames[k] for k in keys}
    #print(f'after: {len(selected_mnames.keys())}')
    print(f'we selected {n} male names from {len(full_mnames.keys())} names generated from maximum {maxName} potential names')

    #print(f'before: {len(full_fnames.keys())} cf. {maxName=} / {n_fdupl=}')
    keys = random.sample(list(full_fnames.keys()), k=nS)
    selected_fnames = {k: full_fnames[k] for k in keys}
    #print(f'after: {len(selected_fnames.keys())}')
    print(f'we selected {n} female names from {len(full_fnames.keys())} names generated from maximum {maxName} potential names')

    return selected_mnames, selected_fnames, nS

if __name__ == "__main__":

    full_mnames, full_fnames, nS = make_names(2000)
    # 첫 글자로 시작하는 원소의 개수 계산하기
    # 남성 이름 명단과 생년월일
    for k, v in full_mnames.items():
        print(f'{k} : {v} (M)', end=", ")
    print()
    print(f'total {nS}')
    # 여성 이름 명단과 생년월일
    for k, v in full_fnames.items():
        print(f'{k} : {v} (M)', end=", ")
    print(f'total {nS}')

    count_by_first_letter = {}
    for word in full_fnames.keys():
        first_letter = word[0]
        if first_letter not in count_by_first_letter:
            count_by_first_letter[first_letter] = 0
        count_by_first_letter[first_letter] += 1
    # 결과 출력하기
    total_count = len(full_fnames)
    for first_letter, count in count_by_first_letter.items():
        ratio = count / total_count
        print(f"{first_letter}: {ratio:.2%}", end=", ")
    

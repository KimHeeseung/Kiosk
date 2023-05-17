import hashlib
import random
import string

def generate_username(string_to_hash):
    # 주어진 문자열을 해싱하여 16진수 형태로 변환합니다.
    hashed_string = hashlib.sha256(string_to_hash.encode()).hexdigest()
    
    # 8~12자의 영문 소문자와 숫자로 구성된 무작위 문자열을 생성합니다.
    username_length = random.randint(8, 12)
    username_chars = string.ascii_lowercase + string.digits
    username = ''.join(random.choices(username_chars, k=username_length))
    
    return username

if __name__ == "__main__":
    for i in range(100):
        print(generate_username('gkst한슈' + str(i)))


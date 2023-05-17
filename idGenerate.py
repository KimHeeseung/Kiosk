import hashlib
import random
import string

def generate_unique_id(data):
    # data를 bytes 형태로 변환하여 SHA-256 해시 함수를 적용합니다.
    hash_obj = hashlib.sha256(str(data).encode())
    hash_str = hash_obj.hexdigest()
    
    # 20자리의 alphanumeric으로 변환합니다.
    random.seed(int(hash_str, 16))  # 해시값을 시드로 사용합니다.
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
    
    return unique_id

if __name__ == '__main__':
    data = '아버지'
    k_id = generate_unique_id(data)
    print(k_id)

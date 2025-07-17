import os
from hashlib import sha256
from dotenv import load_dotenv


load_dotenv()
HASH_NUM = int(os.getenv('HASHNUM'))

def hash_password(password):
    for _ in range(HASH_NUM):
        password = sha256(password.encode()).hexdigest()
    return password

def check_user(email, password, db):
    user = db.users.find_one({'email': email})
    if user and user['password'] == hash_password(password):
        return True
    return False

def register_new_user(email, password, db):
    user = db.users.find_one({'email': email})
    if user:
        return False
    db.users.insert_one({'email': email, 'password': hash_password(password), 'chat_history': []})
    return True 
from Application import db
from Application.Models import User

import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#verifies the login and returns the user object
#if unsuccessful, it returns none
def verify_login(username, password) -> User:
    try:   
        user = db.session.query(User).filter_by(username = username).first()
    except Exception as e:
        print(e)
        return False

    if (user == None):
        return None
    elif (compare_passwords(password, encrypted_password=user.password)):
        return user
    else:
        return None
        
#creates a user and return None if it fails
def create_user(username, password, email=None) -> User:
    token = encrypt_password(password)
    new_user = User(username, token, email)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as error:
        print(error)
        return None
    
#returns an encrypted password
def encrypt_password(password) -> str:
    type = PBKDF2HMAC(hashes.SHA256(), 32, bytes(os.environ["SALT_KEY"], "utf-8"), 500000)
    key = urlsafe_b64encode(type.derive(bytes(os.environ["ENCRYPT_KEY"], "utf-8")))
    algor = Fernet(key)
    token = algor.encrypt(bytes(password, "utf-8"))

    return token

#returns a decrypted password
def decrypt_password(encrypted_password) -> str:
    type = PBKDF2HMAC(hashes.SHA256(), 32, bytes(os.environ["SALT_KEY"], "utf-8"), 500000)
    key = urlsafe_b64encode(type.derive(bytes(os.environ["ENCRYPT_KEY"], "utf-8")))
    algor = Fernet(key)
    password = algor.decrypt(encrypted_password)

    return password

#compares a password with a encrypted password
#returns true if it's the same
def compare_passwords(password, encrypted_password):
    if (bytes(password, "utf-8") == decrypt_password(encrypted_password)):
        return True
    else:
        return False
from cryptography.fernet import Fernet

key = b'lJUX4ph1i6eKbOmnJdziRSPbwmZ7MSO0J9Ch-NoTUjM='
cipher  = Fernet(key)

def encrypt(data):
    return cipher.encrypt(data)

def decrypt(data):
    return cipher.decrypt(data)

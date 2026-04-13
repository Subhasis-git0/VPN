import socket
from encryption import encrypt, decrypt
from cryptography.fernet import Fernet
from rsa_utils import load_public_key, encrypt_with_public_key

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',8080))

public_key_data = client.recv(2048)
public_key = load_public_key(public_key_data)

session_key = Fernet.generate_key()

encrypted_key = encrypt_with_public_key(public_key, session_key)

client.send(encrypted_key)

cipher = Fernet(session_key)


http_request = b"""GET / HTTP/1.1\r
Host: example.com\r
User-Agent: Mozilla/5.0\r
Accept: text/html\r
Connection: close\r
\r
"""

client.send(cipher.encrypt(http_request))

response = client.recv(4096)

data = cipher.decrypt(response)

print("response from internet:\n")
print(data.decode(errors='ignore'))
client.close()

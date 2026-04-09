import socket
from encryption import encrypt, decrypt

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',8080))

message = encrypt(b"hello server")
client.send(message)

response = client.recv(1024)

print("server says:", decrypt(response).decode())

client.send(b"hello server")

response = client.recv(1024)
print("server says:", response.decode())
client.close()

import socket
from encryption import encrypt, decrypt

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',8080))

http_request = http_request = b"""GET / HTTP/1.1\r
Host: example.com\r
User-Agent: Mozilla/5.0\r
Accept: text/html\r
Connection: close\r
\r
"""
message = encrypt(http_request)
client.send(message)

response = client.recv(4096)

data = decrypt(response)

print("response from internet:\n")
print(data.decode(errors='ignore'))
client.close()

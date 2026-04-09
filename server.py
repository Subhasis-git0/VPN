import socket 
from encryption import encrypt, decrypt

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind(('0.0.0.0', 8080)) 
server.listen(5) 

print('Server is listening on port 8080...') 

while True: 
    client_socket, addr = server.accept() 
    print('connection:', addr)

    encrypted_data = client_socket.recv(1024)

    data = decrypt(encrypted_data)
    print("decrypted data:", data.decode())

    response = encrypt(b"hello from vpn server") 
    client_socket.send(response)

    data = client_socket.recv(1024) 
    if not data: 
        break
    print("Received:", data.decode()) 
    client_socket.send(b"hello from vpn server")
 
    client_socket.close()

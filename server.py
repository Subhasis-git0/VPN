import socket 
import threading
from encryption import encrypt, decrypt

def handle_client(client_socket, addr):
    print('connected:', addr)

    try: 
        encrypted_data = client_socket.recv(4096)
        if not encrypted_data:
            client_socket.close()
            return
        
        request = decrypt(encrypted_data)

        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect(('example.com', 80))
        remote.send(request)

        response = remote.recv(4096)
        client_socket.send(encrypt(response))
        remote.close()
        client_socket.close()

    except Exception as e:
        print("Error:", e)
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8080))
server.listen(5)

print('VPN server running...')

while True:
    client_socket, addr = server.accept()
    
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()


 
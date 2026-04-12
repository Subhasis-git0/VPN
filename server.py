import socket 
import threading
from encryption import encrypt, decrypt
from rsa_utils import decrypt_with_private_key, generate_keys, serialize_private_key, load_private_key

private_key, public_key = generate_keys()


def handle_client(client_socket, addr):
    print('connected:', addr)

    try: 
        client_socket.send(serialize_private_key(public_key))

        encrypted_key = client_socket.recv(1024)
        session_key = decrypt_with_private_key(private_key, encrypted_key)

        cipher = Fernet(session_key)

        encrypted_data = client_socket.recv(4096)
        request = cipher.decrypt(encrypted_data)


        remote = socket.socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        remote.connect(('example.com', 80))
        remote.send(request)

        response = b""
        while True:
            chuck = remote.recv(4096)
            if not chuck:
                break
            response += chuck

        client_socket.send(cipher.encrypt(response))
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


 
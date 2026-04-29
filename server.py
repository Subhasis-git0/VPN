import socket 
import threading
from encryption import encrypt, decrypt
from cryptography.fernet import Fernet
from rsa_utils import decrypt_with_private_key, generate_keys, serialize_public_key, load_private_key

private_key, public_key = generate_keys()

stats = {
    "connections": 0,
    "data": 0
}

def handle_client(client_socket, addr):
    print("Client connected:", addr)

    try:
        # Send the server's public key first, then receive the encrypted session key.
        client_socket.sendall(serialize_public_key(public_key))
        print("Sent public key to client")

        encrypted_key = client_socket.recv(1024)
        session_key = decrypt_with_private_key(private_key, encrypted_key)
        print("Received encrypted session key")

        cipher = Fernet(session_key)

        encrypted_data = client_socket.recv(4096)
        request = cipher.decrypt(encrypted_data)
        print("Received and decrypted client request")


        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect(('example.com', 80))
        remote.sendall(request)

        response = b""
        while True:
            chuck = remote.recv(4096)
            if not chuck:
                break
            response += chuck

        client_socket.sendall(cipher.encrypt(response))
        remote.close()
        client_socket.close()

    except Exception as e:
        print("Error:", e)
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9191))
server.listen(5)

print('VPN server running on port 9191...')

while True:
    client_socket, addr = server.accept()
    
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()


 
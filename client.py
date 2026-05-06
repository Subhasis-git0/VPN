import requests
from cryptography.fernet import Fernet
from rsa_utils import load_public_key, encrypt_with_public_key

BASE_URL = "https://cut-spider-tightwad.ngrok-free.dev"

print("Step 1: Getting public key...")
public_key_data = requests.get(BASE_URL + "/get_key").content
public_key = load_public_key(public_key_data)

print("Step 2: Generating session key...")
session_key = Fernet.generate_key()
cipher = Fernet(session_key)

print("Step 3: Sending encrypted session key...")
client_id = requests.post(
    BASE_URL + "/connect",
    data=encrypt_with_public_key(public_key, session_key),
    timeout=5
).text

print("Client ID:", client_id)

print("Step 4: Sending encrypted request...")
http_request = b"""GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"""

encrypted_request = cipher.encrypt(http_request)

response = requests.post(
    BASE_URL + f"/request/{client_id}",
    data=encrypted_request,
    timeout=10
).content

print("Step 5: Decrypting response...")
decrypted = cipher.decrypt(response)

print("\n===== RESPONSE =====\n")
print(decrypted.decode(errors="ignore"))
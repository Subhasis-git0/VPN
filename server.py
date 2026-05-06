from flask import Flask, request
from cryptography.fernet import Fernet
from rsa_utils import decrypt_with_private_key, generate_keys, serialize_public_key

import socket
from datetime import datetime

app = Flask(__name__)

private_key, public_key = generate_keys()

session_keys = {}

# 📊 Stats for dashboard
stats = {
    "total_requests": 0,
    "total_data": 0,
    "clients": 0,
    "logs": []
}

# 🔑 Send public key
@app.route("/get_key", methods=["GET"])
def get_key():
    return serialize_public_key(public_key)

# 🔐 Client connects (key exchange)
@app.route("/connect", methods=["POST"])
def connect():
    print("➡️ Received /connect request")

    encrypted_key = request.data
    print("Encrypted key received")

    session_key = decrypt_with_private_key(private_key, encrypted_key)
    print("Session key decrypted")

    client_id = str(len(session_keys))
    session_keys[client_id] = Fernet(session_key)

    stats["clients"] += 1

    print("Client registered:", client_id)

    return client_id

# 🌐 Handle request
@app.route("/request/<client_id>", methods=["POST"])
def handle_request(client_id):
    cipher = session_keys[client_id]

    encrypted_data = request.data
    request_data = cipher.decrypt(encrypted_data)

    # 📊 Update stats
    stats["total_requests"] += 1
    stats["total_data"] += len(request_data)

    stats["logs"].append({
        "client": client_id,
        "size": len(request_data),
        "time": datetime.now().strftime("%H:%M:%S")
    })

    # 🌍 Connect to website
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote.connect(('example.com', 80))
    remote.sendall(request_data)

    response = b""
    while True:
        chunk = remote.recv(4096)
        if not chunk:
            break
        response += chunk

    remote.close()

    encrypted_response = cipher.encrypt(response)
    return encrypted_response

# 📊 DASHBOARD ROUTE (🔥 MAIN FEATURE)
@app.route("/dashboard")
def dashboard():
    logs_html = "".join([
        f"<li>Client {log['client']} | {log['size']} bytes | {log['time']}</li>"
        for log in stats["logs"][-10:]
    ])

    return f"""
    <html>
    <head>
        <title>VPN Dashboard</title>
    </head>
    <body>
        <h1>🔐 VPN Dashboard</h1>
        <p><b>Total Requests:</b> {stats['total_requests']}</p>
        <p><b>Total Data:</b> {stats['total_data']} bytes</p>
        <p><b>Connected Clients:</b> {stats['clients']}</p>

        <h3>Recent Activity:</h3>
        <ul>
            {logs_html}
        </ul>
    </body>
    </html>
    """

app.run(host="0.0.0.0", port=8080)

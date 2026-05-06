------------Secure Proxy-Based VPN System----------------
A secure proxy-based VPN system built using Python that demonstrates core VPN concepts such as encrypted tunneling, hybrid cryptography, proxy-based traffic routing, and cross-network communication.

This project uses a hybrid encryption model:

RSA for secure key exchange
AES (Fernet) for encrypted communication

The server acts as an intermediary proxy between the client and the internet, securely forwarding requests and responses through an encrypted tunnel.

Global accessibility is achieved using ngrok, allowing clients from different networks and devices to connect to the locally hosted VPN server.

------------------Features------------------------------
Hybrid Encryption (RSA + AES)
Proxy-Based Secure Communication
Client-Server Architecture
Global Connectivity using ngrok
Real-Time Monitoring Dashboard
Encrypted Request-Response Handling
Multi-Client Support
Secure Key Exchange Mechanism

------------------How It Works-------------------------
The client requests the server's RSA public key.
The client generates an AES session key.
The AES key is encrypted using the server’s RSA public key.
The encrypted session key is sent to the server.
The server decrypts the AES key using its private RSA key.
The client sends encrypted HTTP requests.
The server decrypts the request, forwards it to the target website, receives the response, encrypts it again, and sends it back to the client.
The client decrypts and displays the response securely.

--------------------Architecture------------------------
Client Device
      ↓
Encrypted HTTP Request
      ↓
Ngrok Public Tunnel
      ↓
VPN Server (Kali Linux)
      ↓
Target Website (example.com)
      ↓
Encrypted Response Back
      ↓
Client Device

------------------Project Structure-----------------------
VPN/
│
├── server.py          # VPN server
├── client.py          # VPN client
├── rsa_utils.py       # RSA encryption utilities
├── encryption.py      # AES encryption functions
├── requirements.txt   # Dependencies
└── README.md

-------------------Installation-----------------------------
Clone Repository
  git clone https://github.com/your-username/secure-vpn.git
  cd secure-vpn

Create Virtual Environment
  python3 -m venv vpn_env
  source vpn_env/bin/activate

Install Dependencies
  pip install -r requirements.txt

Run Server
  python server.py

Expose Server Globally using ngrok
  ngrok http 8080

Run Client
  python client.py

Dashboard
  https://your-ngrok-url.ngrok-free.dev/dashboard

---------------------Limitations-----------------------
This project is a proxy-based VPN demonstration and not a full system-level VPN like:

OpenVPN
WireGuard

Current limitations:

HTTP request-based communication
No full packet routing
No UDP support
No system-wide traffic tunneling






import socket
import json

def send_message(message, host="169.254.45.67", port=8002):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(message).encode())

import socket
import json


def send_message(message, host="192.168.1.2", port=8002):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(json.dumps(message).encode())


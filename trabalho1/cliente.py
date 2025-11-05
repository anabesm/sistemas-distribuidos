import socket

def connect_tcp_client(host, port, handler):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    try:
        handler(sock)
    finally:
        sock.close()
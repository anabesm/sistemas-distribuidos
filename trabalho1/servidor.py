import socket
import threading
import time

def start_tcp_server(handler, host="127.0.0.1", port=5059):
    def _server():
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(1)
        print(f"[SERVIDOR] ouvindo em {host}:{port}")
        conn, addr = srv.accept()
        print(f"[SERVIDOR] conexão de {addr}")
        try:
            handler(conn)
        finally:
            conn.close()
            srv.close()
            print("[SERVIDOR] encerrado")
    t = threading.Thread(target=_server, daemon=True)
    t.start()
    time.sleep(0.2)
import socket
import threading
import time
from livro_output_stream import LivroOutputStream
from socket_writer import _SocketWriter
from helpers.objetos import _objetos_demo

def _servidor_tcp(host="127.0.0.1", port=5059, stop_after_one=True):
    def _hexdump(b: bytes) -> str:
        return " ".join(f"{x:02X}" for x in b)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(1)
    print(f"Servidor TCP ouvindo em {host}:{port} ...")
    conn, addr = srv.accept()
    print(f"Conexão de {addr}")
    with conn:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(f"[TCP] {len(data)} bytes : { _hexdump(data) }")
    if stop_after_one:
        srv.close()
        print("Servidor TCP encerrado.")

def teste_tcp():
    print("\n=== Teste iii) Servidor remoto (TCP) ===")
    host, port = "127.0.0.1", 5059
    t = threading.Thread(target=_servidor_tcp, args=(host, port), daemon=True)
    t.start()
    time.sleep(0.2) 

    # cliente TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    dest = _SocketWriter(sock)
    stream = LivroOutputStream(_objetos_demo(), n_objetos=3, destino=dest, close_destino=True)
    stream.send_all()
    time.sleep(0.2) 
import json
from testes.objetos import _objetos_demo
from streams.livro_output_stream import LivroOutputStream
from streams.livro_input_stream import LivroInputStream
from servidor import start_tcp_server
from cliente import connect_tcp_client
from streams.socket_writer import _SocketWriter 
from streams.socket_reader import _SocketReader

def teste_tcp_envia():
    print("\n=== Teste iii) Envio via TCP ===")
    def server_handler(conn):
        data = conn.recv(4096)
        print(f"[SERVIDOR] recebeu {len(data)} bytes")

    start_tcp_server(server_handler, port=5059)

    def client_handler(sock):
        dest = _SocketWriter(sock)
        out = LivroOutputStream(_objetos_demo(), 3, dest, close_destino=True)
        out.send_all()

    connect_tcp_client("127.0.0.1", 5059, client_handler)

def teste_tcp_recebe():
    print("\n=== Teste vi) Recebimento via TCP ===")
    def server_handler(conn):
        dest = _SocketWriter(conn)
        out = LivroOutputStream(_objetos_demo(), 3, dest, close_destino=True)
        out.send_all()

    start_tcp_server(server_handler, port=5060)

    def client_handler(sock):
        src = _SocketReader(sock)
        ins = LivroInputStream(src, close_origem=True)
        objs = ins.read_all()
        print(f"[TCP] Lidos {len(objs)} objetos:")
        print(json.dumps(objs, ensure_ascii=False, indent=2))

    connect_tcp_client("127.0.0.1", 5060, client_handler)
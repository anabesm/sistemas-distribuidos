import json
import struct
from typing import Tuple, Dict

VERSION = 1
TYPE_REQUEST = 0x01
TYPE_REPLY   = 0x02
TYPE_ERROR   = 0x03

_HEADER_FMT = "!BBI"
_HEADER_SIZE = struct.calcsize(_HEADER_FMT)

class ProtocolError(Exception):
    pass

def pack_message(msg_type: int, payload: Dict) -> bytes:
    if msg_type not in (TYPE_REQUEST, TYPE_REPLY, TYPE_ERROR):
        raise ProtocolError(f"msg_type inválido: {msg_type}")
    try:
        body = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    except Exception as e:
        raise ProtocolError(f"Falha ao serializar JSON: {e}") from e
    header = struct.pack(_HEADER_FMT, VERSION, msg_type, len(body))
    return header + body

def unpack_header(header_bytes: bytes) -> Tuple[int, int, int]:
    if len(header_bytes) != _HEADER_SIZE:
        raise ProtocolError("Tamanho de header inválido.")
    version, msg_type, payload_len = struct.unpack(_HEADER_FMT, header_bytes)
    if version != VERSION:
        raise ProtocolError(f"Versão não suportada: {version}")
    return version, msg_type, payload_len

def recv_exact(sock, n: int) -> bytes:
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ProtocolError("Conexão encerrada durante leitura.")
        data.extend(chunk)
    return bytes(data)

def recv_message(sock) -> Tuple[int, Dict]:
    header = recv_exact(sock, _HEADER_SIZE)
    _, msg_type, payload_len = unpack_header(header)
    body = recv_exact(sock, payload_len)
    try:
        payload = json.loads(body.decode('utf-8'))
    except Exception as e:
        raise ProtocolError(f"Falha ao decodificar JSON: {e}") from e
    return msg_type, payload

def send_message(sock, msg_type: int, payload: Dict) -> None:
    data = pack_message(msg_type, payload)
    sock.sendall(data)

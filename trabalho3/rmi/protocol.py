from __future__ import annotations
import json, base64, itertools
from dataclasses import dataclass
from typing import Any, Dict

REQUEST, REPLY = 0, 1
_request_counter = itertools.count(1)

# representação de referência a objeto remoto
@dataclass
class RemoteObjectRef:
    host: str
    port: int
    object_name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"host": self.host, "port": self.port, "object_name": self.object_name}

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RemoteObjectRef":
        return RemoteObjectRef(d["host"], int(d["port"]), d["object_name"])

# conversão entre bytes e representação externa (dicionários JSON compatíveis)
def to_bytes(data: Any) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf-8")

def from_bytes(b: bytes) -> Any:
    return json.loads(b.decode("utf-8"))

# empacotamento/desempacotamento de argumentos em base64
def pack_args(payload: Any) -> str:
    by = to_bytes(payload)
    return base64.b64encode(by).decode("ascii")

def unpack_args(s: str) -> Any:
    by = base64.b64decode(s.encode("ascii"))
    return from_bytes(by)

# criação de mensagens de requisição e resposta RMI
def make_request(ror: RemoteObjectRef, method: str, args_external: Any) -> Dict[str, Any]:
    return {
        "messageType": REQUEST,
        "requestId": next(_request_counter),
        "objectReference": ror.object_name,
        "methodId": method,
        "arguments": pack_args(args_external),
    }

def make_reply(req_id: int, result_external: Any, is_exception: bool=False) -> Dict[str, Any]:
    return {
        "messageType": REPLY,
        "requestId": req_id,
        "arguments": pack_args(result_external),
        "isException": is_exception,
    }

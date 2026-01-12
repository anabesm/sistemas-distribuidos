from dataclasses import dataclass
from typing import Dict, Any
from .protocol import RemoteObjectRef

# representa o registro de objetos remotos
@dataclass
class Registry:
    host: str
    port: int
    def ror(self, name: str) -> RemoteObjectRef:
        return RemoteObjectRef(self.host, self.port, name)

# repositório de objetos remotos
class Repository:
    def __init__(self):
        self._objs: Dict[str, Any] = {}

    def bind(self, name: str, obj: Any):
        self._objs[name] = obj

    def resolve(self, name: str) -> Any:
        if name not in self._objs:
            raise KeyError(f"Objeto remoto '{name}' não encontrado")
        return self._objs[name]

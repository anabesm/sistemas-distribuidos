from typing import Iterable, List, Optional, Sequence, Any
import io
import struct

class LivroOutputStream(io.BufferedIOBase):
    def __init__(
        self,
        array_objs: Iterable[Any],
        n_objetos: int,
        destino: Any,
        campos: Optional[Sequence[str]] = None,
        close_destino: bool = False,
    ) -> None:
        super().__init__()
        self._objetos: List[Any] = list(array_objs)[: max(0, n_objetos)]
        self._dest = destino
        self._campos = list(campos) if campos else None
        self._close_destino = close_destino
        if self._campos is not None and len(self._campos) < 3:
            raise ValueError("Informe pelo menos 3 campos ou deixe None para seleção automática.")

    @staticmethod
    def _to_bytes(texto: str) -> bytes:
        return texto.encode("utf-8")

    @staticmethod
    def _pick_3_campos(obj: Any) -> List[str]:
        preferencia = ["id", "titulo", "preco", "estado", "autor"]
        disponiveis = [c for c in preferencia if hasattr(obj, c)]

        if len(disponiveis) < 3:
            extras = [k for k in obj.__dict__.keys() if k not in disponiveis]
            disponiveis.extend(extras)
        return disponiveis[:3]

    def _encode_obj(self, obj: Any) -> bytes:
        campos = self._campos or self._pick_3_campos(obj)

        payload = bytearray()
        payload.append(len(campos) & 0xFF)

        for nome in campos:
            valor = getattr(obj, nome)
            valor_str = str(valor)
            nome_b = self._to_bytes(nome)
            val_b = self._to_bytes(valor_str)
            if len(nome_b) > 255:
                raise ValueError("Nome do campo ficou grande demais para 1 byte de tamanho.")

            payload.append(len(nome_b))
            payload.extend(nome_b)
            payload.extend(struct.pack(">I", len(val_b)))  
            payload.extend(val_b)

        return bytes(payload)

    def write(self, b: bytes) -> int:
        return self._dest.write(b)

    def flush(self) -> None:
        if hasattr(self._dest, "flush"):
            self._dest.flush()

    def close(self) -> None:
        try:
            self.flush()
        finally:
            if self._close_destino and hasattr(self._dest, "close"):
                self._dest.close()
        return super().close()

    def send_all(self) -> None:
        self.write(struct.pack(">I", len(self._objetos)))
        for obj in self._objetos:
            payload = self._encode_obj(obj)
            self.write(struct.pack(">I", len(payload))) 
            self.write(payload)
        self.flush()
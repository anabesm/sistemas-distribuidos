from typing import Any, Dict, List
import io
import struct

class LivroInputStream(io.BufferedIOBase):
    def __init__(self, origem: Any, close_origem: bool = False) -> None:
        super().__init__()
        self._src = origem
        self._close = close_origem

    def _read_exact(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self._src.read(n - len(data))
            if not chunk:
                raise EOFError("Dados insuficientes (EOF).")
            data += chunk
        return data

    def _decode_obj(self) -> Dict[str, str]:
        (length,) = struct.unpack(">I", self._read_exact(4))
        payload = io.BytesIO(self._read_exact(length))

        campos_qtd_raw = payload.read(1)
        if not campos_qtd_raw:
            raise EOFError("Payload truncado.")
        campos_qtd = campos_qtd_raw[0]

        obj: Dict[str, str] = {}
        for _ in range(campos_qtd):
            name_len_raw = payload.read(1)
            if not name_len_raw:
                raise EOFError("Payload truncado (name_len).")
            name_len = name_len_raw[0]
        
            name = payload.read(name_len).decode("utf-8")
            (val_len,) = struct.unpack(">I", payload.read(4))

            value = payload.read(val_len).decode("utf-8")
            obj[name] = value
        return obj

    def read_all(self) -> List[Dict[str, str]]:
        (n_objs,) = struct.unpack(">I", self._read_exact(4))
        objs = []
        for _ in range(n_objs):
            objs.append(self._decode_obj())
        return objs

    def close(self) -> None:
        if self._close and hasattr(self._src, "close"):
            try:
                self._src.close()
            except Exception:
                pass
        return super().close()
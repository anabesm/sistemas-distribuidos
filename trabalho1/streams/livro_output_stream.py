from typing import Iterable, List, Optional, Sequence, Any
import io
import struct

class LivroOutputStream(io.BufferedIOBase):
    def __init__(
        self,
        array_objs: Iterable[Any],
        n_objetos: int,
        destino: Any,
        campos: Optional[Sequence[str]] = ["id", "titulo", "preco"],
        close_destino: bool = False,
    ) -> None:
        super().__init__()
        self._objetos: List[Any] = list(array_objs)[: max(0, n_objetos)]
        self._dest = destino
        self._campos = list(campos) if campos else None
        self._close_destino = close_destino
        if self._campos is not None and len(self._campos) < 3:
            raise ValueError("Informe pelo menos 3 campos ou deixe None para seleção automática.")

    # helper para converter texto em bytes UTF-8
    @staticmethod
    def _to_bytes(texto: str) -> bytes:
        return texto.encode("utf-8")

    # codifica um objeto em bytes conforme o formato especificado
    def _encode_obj(self, obj: Any) -> bytes:
        payload = bytearray()
        payload.append(len(self._campos) & 0xFF)

        for nome in self._campos:
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

    # escreve bytes no destino
    def write(self, b: bytes) -> int:
        return self._dest.write(b)

    # garante que todos os dados foram escritos
    def flush(self) -> None:
        if hasattr(self._dest, "flush"):
            self._dest.flush()

    # fecha o stream e o destino se necessário
    def close(self) -> None:
        try:
            self.flush()
        finally:
            if self._close_destino and hasattr(self._dest, "close"):
                self._dest.close()
        return super().close()

    # envia todos os objetos no stream
    def send_all(self) -> None:
        self.write(struct.pack(">I", len(self._objetos)))
        for obj in self._objetos:
            payload = self._encode_obj(obj)
            self.write(struct.pack(">I", len(payload))) 
            self.write(payload)
        self.flush()
from dataclasses import dataclass
from models.base import Produto, Trocavel

@dataclass
class EBook(Produto, Trocavel):
    autor: str
    isbn: str
    formato: str
    tamanho_mb: float
    drm: bool

    # e-books só podem ser trocados com eBooks sem DRM
    def pode_trocar_por(self, outro: "Produto") -> bool:
        return (
            isinstance(outro, EBook)
            and not self.drm
            and isinstance(getattr(outro, "drm", False), bool)
            and not outro.drm
            and self.disponivel
            and outro.disponivel
        )
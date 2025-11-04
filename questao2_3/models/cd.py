from dataclasses import dataclass
from models.base import Produto

@dataclass
class CD(Produto):
    artista: str
    genero: str
    faixas: int
    # CD não é trocável

from dataclasses import dataclass
from models.base import Produto, Trocavel

@dataclass
class Apostila(Produto, Trocavel):
    materia: str
    instituicao: str

    # apostilas usadas podem ser trocadas entre si
    def pode_trocar_por(self, outro: "Produto") -> bool:
        return (
            isinstance(outro, Apostila)
            and self.estado == "usado"
            and outro.estado == "usado"
            and self.disponivel
            and outro.disponivel
        )
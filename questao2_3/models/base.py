from dataclasses import dataclass, field
from typing import Literal
from abc import ABC, abstractmethod

class Trocavel(ABC):
    @abstractmethod
    # define a política de troca entre produtos
    def pode_trocar_por(self, outro: "Produto") -> bool:
        pass


@dataclass
class Produto(ABC):
    id: str
    titulo: str
    preco: float
    estado: Literal["novo", "usado"]
    disponivel: bool = field(default=True, init=False)

    # marca o produto como vendido
    def marcar_vendido(self) -> None:
        if not self.disponivel:
            raise ValueError("Produto indisponível.")
        self.disponivel = False

from dataclasses import dataclass, field, asdict
from typing import Literal
from abc import ABC, abstractmethod

class Trocavel(ABC):
    @abstractmethod
    def pode_trocar_por(self, outro: "Produto") -> bool:
        pass

@dataclass
class Produto(ABC):
    id: str
    titulo: str
    preco: float
    estado: Literal["novo", "usado"]
    disponivel: bool = field(default=True, init=False)

    def marcar_vendido(self) -> None:
        if not self.disponivel:
            raise ValueError("Produto indisponível.")
        self.disponivel = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["__type__"] = self.__class__.__name__
        return d

    @staticmethod
    def from_dict(d: dict) -> "Produto":
        from .livro import Livro
        from .ebook import EBook
        from .apostila import Apostila
        from .cd import CD
        map_cls = {"Livro": Livro, "EBook": EBook, "Apostila": Apostila, "CD": CD}
        cls = map_cls.get(d.get("__type__"))
        if not cls:
            raise ValueError("Tipo de produto desconhecido")
        d = dict(d)
        d.pop("__type__", None)
        obj = cls(**{k: v for k, v in d.items() if k not in ("disponivel",)})
        obj.disponivel = d.get("disponivel", True)
        return obj

    def __str__(self):
        status = "disponível" if self.disponivel else "vendido"
        return f"{self.__class__.__name__}({self.id}) – {self.titulo} – R${self.preco:.2f} – {status}"
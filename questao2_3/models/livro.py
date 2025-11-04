from dataclasses import dataclass
from models.base import Produto, Trocavel
from models.ebook import EBook

@dataclass
class Livro(Produto, Trocavel):
    autor: str
    isbn: str
    paginas: int

    # livros podem ser trocados com livros ou eBooks
    def pode_trocar_por(self, outro: "Produto") -> bool:
        return (
            isinstance(outro, (Livro, EBook))
            and self.disponivel
            and outro.disponivel
            and abs(self.preco - outro.preco) <= 10
        )
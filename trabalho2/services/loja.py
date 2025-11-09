from dataclasses import dataclass, field
from typing import List, Dict
from models.base import Produto

@dataclass
class Loja:
    nome: str
    estoque: Dict[str, Produto] = field(default_factory=dict)

    # adiciona um produto ao estoque
    def add_produto(self, produto: Produto) -> None:
        self.estoque[produto.id] = produto

    # obtém um produto pelo ID
    def get(self, produto_id: str) -> Produto:
        if produto_id not in self.estoque:
            raise KeyError("Produto não encontrado.")
        return self.estoque[produto_id]

    # lista todos os produtos
    def listar(self) -> List[Produto]:
        return list(self.estoque.values())

    # busca produtos pelo termo
    def buscar(self, termo: str) -> List[Produto]:
        termo = termo.lower()
        return [
            p
            for p in self.estoque.values()
            if termo in p.titulo.lower()
            or ("autor" in p.__dict__ and termo in str(p.__dict__["autor"]).lower())
        ]

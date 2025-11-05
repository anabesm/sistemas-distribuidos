from typing import List, Optional
from models.base import Produto
from services.loja import Loja

# serviço de catálogo: cadastro, listagem e busca
class CatalogoService:
    def __init__(self, loja: Loja):
        self.loja = loja

    def cadastrar(self, produto: Produto) -> Produto:
        self.loja.add_produto(produto)
        return produto

    def listar(self, tipo: Optional[str] = None) -> List[Produto]:
        itens = self.loja.listar()
        if tipo:
            tipo = tipo.lower()
            itens = [p for p in itens if p.__class__.__name__.lower() == tipo]
        return itens

    def buscar(self, termo: str) -> List[Produto]:
        return self.loja.buscar(termo)
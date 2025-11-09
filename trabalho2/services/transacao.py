from models.base import Produto, Trocavel
from services.loja import Loja

# serviço de transações (venda e troca de produtos)
class TransacaoService:
    def __init__(self, loja: Loja):
        self.loja = loja

    # vende um produto pelo ID
    def vender(self, produto_id: str) -> Produto:
        produto = self.loja.get(produto_id)
        produto.marcar_vendido()
        return produto

    # troca dois produtos pelo ID
    def trocar(self, produto_a_id: str, produto_b_id: str) -> dict:
        a = self.loja.get(produto_a_id)
        b = self.loja.get(produto_b_id)

        if not isinstance(a, Trocavel) or not isinstance(b, Trocavel):
            raise ValueError("Pelo menos um dos itens não é trocável.")

        if not (a.pode_trocar_por(b) and b.pode_trocar_por(a)):
            raise ValueError("Condições de troca não atendidas.")

        return {"ok": True, "mensagem": f"Troca autorizada entre '{a.titulo}' e '{b.titulo}'."}
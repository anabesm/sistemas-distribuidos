from rmi.naming import Registry
from rmi.transport import Requestor
from rmi.marshalling import marshal
from rmi.protocol import RemoteObjectRef

class CatalogoProxy:
    def __init__(self, ror: RemoteObjectRef, requestor: Requestor):
        self.ror = ror
        self.req = requestor

    def cadastrar(self, produto):
        args = {"args": [marshal(produto)]}
        return self.req.doOperation(self.ror, "cadastrar", args)

    def listar(self, tipo=None):
        if tipo is None:
            args = {"args": []}
        else:
            args = {"args": [tipo]}
        return self.req.doOperation(self.ror, "listar", args)

    def buscar(self, termo: str):
        args = {"args": [termo]}
        return self.req.doOperation(self.ror, "buscar", args)

class TransacaoProxy:
    def __init__(self, ror: RemoteObjectRef, requestor: Requestor):
        self.ror = ror
        self.req = requestor

    def vender(self, produto_id: str):
        args = {"args": [produto_id]}
        return self.req.doOperation(self.ror, "vender", args)

    def trocar(self, a_id: str, b_id: str):
        args = {"args": [a_id, b_id]}
        return self.req.doOperation(self.ror, "trocar", args)

def demo():
    reg = Registry(host="127.0.0.1", port=9000)
    requestor = Requestor()
    catalogo = CatalogoProxy(reg.ror("CatalogoService"), requestor)
    transacao = TransacaoProxy(reg.ror("TransacaoService"), requestor)

    print("== LISTA INICIAL ==")
    for p in catalogo.listar():
        print(p)

    print("\n== BUSCA por 'python' ==")
    for p in catalogo.buscar("python"):
        print(p)

    print("\n== VENDA L2 ==")
    vendido = transacao.vender("L2")
    print(vendido)

    print("\n== TROCA E1 por L1 (deve falhar regras) ==")
    try:
        print(transacao.trocar("E1","L1"))
    except Exception as e:
        print("Erro esperado:", e)

if __name__ == "__main__":
    demo()

# app/demo_in_process.py
from rmi.naming import Registry, Repository
from rmi.skeleton import Dispatcher
from rmi.transport import ServerRequestHandler, Requestor
from services.loja import Loja
from services.catalogo import CatalogoService
from services.transacao import TransacaoService
from models.livro import Livro
from models.ebook import EBook
from models.apostila import Apostila
from models.cd import CD

from app.client import CatalogoProxy, TransacaoProxy

def start_server(host="127.0.0.1", port=9999):
    repo = Repository()
    loja = Loja("Loja de Mídias")

    # seed com exemplos que permitem trocas válidas e inválidas
    loja.add_produto(Livro(id="L1", titulo="Clean Code", preco=120.0, estado="novo",
                           autor="Robert C. Martin", isbn="978", paginas=464, genero="Engenharia"))
    loja.add_produto(Livro(id="L2", titulo="O Senhor dos Anéis", preco=90.0, estado="usado",
                           autor="J.R.R. Tolkien", isbn="978", paginas=1200, genero="Fantasia"))
    loja.add_produto(EBook(id="E1", titulo="Python Fluente", preco=60.0, estado="novo",
                           autor="Luciano", isbn="978", formato="PDF", tamanho_mb=12.5, drm=False))
    loja.add_produto(EBook(id="E2", titulo="Python Cookbook", preco=62.0, estado="novo",
                           autor="Beazley", isbn="978", formato="PDF", tamanho_mb=15.0, drm=False))  # permite troca com E1
    loja.add_produto(Apostila(id="A1", titulo="Cálculo I", preco=30.0, estado="usado",
                              materia="Cálculo", instituicao="UF"))
    loja.add_produto(Apostila(id="A2", titulo="Cálculo II", preco=28.0, estado="usado",
                              materia="Cálculo", instituicao="UF"))  # permite troca com A1
    loja.add_produto(CD(id="C1", titulo="Kind of Blue", preco=40.0, estado="novo",
                        artista="Miles", genero="Jazz", faixas=5))

    catalogo = CatalogoService(loja)
    transacao = TransacaoService(loja)
    repo.bind("CatalogoService", catalogo)
    repo.bind("TransacaoService", transacao)

    handler = ServerRequestHandler(host, port, Dispatcher(repo))

    # inicia servidor em background
    import threading, time
    threading.Thread(target=handler.serve_forever, daemon=True).start()
    time.sleep(0.2)
    return handler

def main():
    host, port = "127.0.0.1", 9999
    start_server(host, port)

    reg = Registry(host=host, port=port)
    req = Requestor()
    catalogo = CatalogoProxy(reg.ror("CatalogoService"), req)
    transacao = TransacaoProxy(reg.ror("TransacaoService"), req)

    print("== LISTANDO ==")
    for p in catalogo.listar():
        print(p)

    print("\n== TROCA VÁLIDA: E1 <-> E2 ==")
    ok = transacao.trocar("E1", "E2")
    print(ok)

    print("\n== TROCA VÁLIDA: A1 <-> A2 ==")
    ok = transacao.trocar("A1", "A2")
    print(ok)

    print("\n== VENDA L2 ==")
    vendido = transacao.vender("L2")
    print(vendido)

    print("\n== VENDA REPETIDA L2 (ERRO ESPERADO) ==")
    try:
        transacao.vender("L2")
    except Exception as e:
        print("Erro esperado:", e)

    print("\n== TROCA INVÁLIDA: E1 <-> L1 (ERRO ESPERADO) ==")
    try:
        transacao.trocar("E1", "L1")
    except Exception as e:
        print("Erro esperado:", e)

if __name__ == "__main__":
    main()

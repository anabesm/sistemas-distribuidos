from rmi.naming import Registry, Repository
from rmi.skeleton import Dispatcher
from rmi.transport import ServerRequestHandler
from services.loja import Loja
from services.catalogo import CatalogoService
from services.transacao import TransacaoService
from models.livro import Livro
from models.ebook import EBook
from models.apostila import Apostila
from models.cd import CD

def seed(loja: Loja):
    loja.add_produto(Livro(id="L1", titulo="Clean Code", preco=120.0, estado="novo",
                           autor="Robert C. Martin", isbn="978-0132350884",
                           paginas=464, genero="Engenharia"))
    loja.add_produto(Livro(id="L2", titulo="O Senhor dos Anéis", preco=90.0, estado="usado",
                           autor="J.R.R. Tolkien", isbn="978-8595084757",
                           paginas=1200, genero="Fantasia"))
    loja.add_produto(EBook(id="E1", titulo="Python Fluente", preco=60.0, estado="novo",
                           autor="Luciano Ramalho", isbn="978-8575224625",
                           formato="PDF", tamanho_mb=12.5, drm=False))
    loja.add_produto(Apostila(id="A1", titulo="Cálculo I - Exercícios", preco=30.0,
                              estado="usado", materia="Cálculo", instituicao="UF"))
    loja.add_produto(CD(id="C1", titulo="Kind of Blue", preco=40.0, estado="novo",
                        artista="Miles Davis", genero="Jazz", faixas=5))

def main(host: str="127.0.0.1", port: int=9000):
    repo = Repository()
    loja = Loja("Loja de Mídias")
    seed(loja)

    catalogo = CatalogoService(loja)
    transacao = TransacaoService(loja)
    repo.bind("CatalogoService", catalogo)
    repo.bind("TransacaoService", transacao)

    disp = Dispatcher(repo)
    handler = ServerRequestHandler(host, port, disp)
    print(f"Servidor RMI em {host}:{port} - objetos: CatalogoService, TransacaoService")
    handler.serve_forever()

if __name__ == "__main__":
    main()

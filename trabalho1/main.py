from models.livro import Livro
from services.loja import Loja
from services.catalogo import CatalogoService
from services.transacao import TransacaoService

if __name__ == "__main__":
    loja = Loja("Sebo Central")
    catalogo = CatalogoService(loja)
    transacao = TransacaoService(loja)

    livro1 = Livro(id="1", titulo="Dom Casmurro", preco=30, estado="usado", autor="Machado", isbn="123", paginas=200, genero="Romance")
    livro2 = Livro(id="2", titulo="Memórias Póstumas", preco=28, estado="usado", autor="Machado", isbn="456", paginas=250, genero="Romance")

    catalogo.cadastrar(livro1)
    catalogo.cadastrar(livro2)

    print("Catálogo:")
    for p in catalogo.listar():
        print(p.titulo)

    resultado = transacao.trocar("1", "2")
    print(resultado)

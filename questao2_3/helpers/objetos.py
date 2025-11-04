from typing import List
from models.livro import Livro
from models.ebook import EBook
from models.apostila import Apostila
from models.base import Produto

def _objetos_demo() -> List[Produto]:
    return [
        Livro(id="1", titulo="Padrões de Projeto", preco=80.0, estado="usado",
              autor="GoF", isbn="978857522", paginas=395),
        EBook(id="2", titulo="Clean Code", preco=85.0, estado="novo",
              autor="Robert C. Martin", isbn="9780132350884", formato="epub", tamanho_mb=3.2, drm=False),
        Apostila(id="3", titulo="Estruturas de Dados", preco=25.0, estado="usado",
                 materia="ED", instituicao="UFXX"),
    ]
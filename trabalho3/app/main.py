from typing import List, Optional, Union, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from services.loja import Loja
from services.catalogo import CatalogoService
from services.transacao import TransacaoService

from models.livro import Livro
from models.ebook import EBook
from models.apostila import Apostila
from models.cd import CD

app = FastAPI(title="Sebo API RESTful")

loja = Loja("Sebo")

def seed(loja: Loja):
    loja.add_produto(Livro(
        id="L1", titulo="Clean Code", preco=120.0, estado="novo",
        autor="Robert C. Martin", isbn="978-0132350884",
        paginas=464, genero="Engenharia"
    ))
    loja.add_produto(Livro(
        id="L2", titulo="O Senhor dos Anéis", preco=90.0, estado="usado",
        autor="J.R.R. Tolkien", isbn="978-8595084757",
        paginas=1200, genero="Fantasia"
    ))
    loja.add_produto(EBook(
        id="E1", titulo="Python Fluente", preco=60.0, estado="novo",
        autor="Luciano Ramalho", isbn="978-8575224625",
        formato="PDF", tamanho_mb=12.5, drm=False
    ))
    loja.add_produto(EBook(
        id="E2", titulo="Python Cookbook", preco=62.0, estado="novo",
        autor="Beazley", isbn="978",
        formato="PDF", tamanho_mb=15.0, drm=False
    ))
    loja.add_produto(Apostila(
        id="A1", titulo="Cálculo I - Exercícios", preco=30.0, estado="usado",
        materia="Cálculo", instituicao="UF"
    ))
    loja.add_produto(Apostila(
        id="A2", titulo="Cálculo II", preco=28.0, estado="usado",
        materia="Cálculo", instituicao="UF"
    ))
    loja.add_produto(CD(
        id="C1", titulo="Kind of Blue", preco=40.0, estado="novo",
        artista="Miles Davis", genero="Jazz", faixas=5
    ))

seed(loja)

catalogo_service = CatalogoService(loja)
transacao_service = TransacaoService(loja)


class ProdutoCreate(BaseModel):
    id: str
    tipo_produto: str 
    titulo: str
    preco: float
    estado: str
    extras: Dict[str, Any] 

class TrocaRequest(BaseModel):
    produto_a_id: str
    produto_b_id: str


@app.get("/produtos")
def listar_produtos(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (livro, cd, etc)"),
    termo: Optional[str] = Query(None, description="Buscar por termo no título ou autor")
):
    """
    Lista produtos. Pode filtrar por tipo ou buscar por termo.
    """
    if termo:
        resultados = catalogo_service.buscar(termo)
    else:
        resultados = catalogo_service.listar(tipo)
    
    return [p.to_dict() for p in resultados]


@app.get("/produtos/{produto_id}")
def obter_produto(produto_id: str):
    """
    Busca um único produto pelo ID.
    """
    try:
        produto = loja.get(produto_id)
        return produto.to_dict()
    except KeyError:
        raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.post("/produtos", status_code=201)
def cadastrar_produto(item: ProdutoCreate):
    """
    Cria um novo produto no catálogo.
    """
    try:
        tipo = item.tipo_produto.lower()
        dados = item.extras
        
        common_args = {
            "id": item.id,
            "titulo": item.titulo,
            "preco": item.preco,
            "estado": item.estado
        }
        
        novo_produto = None

        if tipo == "livro":
            novo_produto = Livro(**common_args, **dados)
        elif tipo == "ebook":
            novo_produto = EBook(**common_args, **dados)
        elif tipo == "apostila":
            novo_produto = Apostila(**common_args, **dados)
        elif tipo == "cd":
            novo_produto = CD(**common_args, **dados)
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de produto '{tipo}' inválido.")

        catalogo_service.cadastrar(novo_produto)
        return novo_produto.to_dict()

    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Argumentos inválidos para o tipo {tipo}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/produtos/{produto_id}/venda")
def vender_produto(produto_id: str):
    """
    Realiza a venda de um produto específico.
    """
    try:
        produto = transacao_service.vender(produto_id)
        return {
            "mensagem": "Venda realizada com sucesso", 
            "produto": produto.to_dict()
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transacoes/troca")
def realizar_troca(dados: TrocaRequest):
    """
    Realiza a troca entre dois produtos.
    """
    try:
        resultado = transacao_service.trocar(dados.produto_a_id, dados.produto_b_id)
        return resultado
    except KeyError:
        raise HTTPException(status_code=404, detail="Um dos produtos não foi encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/produtos/{produto_id}")
def atualizar_produto(produto_id: str, item: ProdutoCreate):
    """
    Atualiza (substitui) um produto existente.
    """
    if produto_id not in loja.estoque:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if item.id != produto_id:
        raise HTTPException(status_code=400, detail="O ID da URL difere do ID do corpo da requisição.")

    try:
        tipo = item.tipo_produto.lower()
        dados = item.extras
        
        common_args = {
            "id": produto_id,
            "titulo": item.titulo,
            "preco": item.preco,
            "estado": item.estado
        }
        
        novo_produto = None

        if tipo == "livro":
            novo_produto = Livro(**common_args, **dados)
        elif tipo == "ebook":
            novo_produto = EBook(**common_args, **dados)
        elif tipo == "apostila":
            novo_produto = Apostila(**common_args, **dados)
        elif tipo == "cd":
            novo_produto = CD(**common_args, **dados)
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de produto '{tipo}' inválido.")

        loja.estoque[produto_id] = novo_produto
        
        return novo_produto.to_dict()

    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Argumentos inválidos para atualizar {tipo}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/produtos/{produto_id}", status_code=204)
def remover_produto(produto_id: str):
    """
    Remove um produto do catálogo.
    """
    if produto_id not in loja.estoque:
         raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    del loja.estoque[produto_id]
    return
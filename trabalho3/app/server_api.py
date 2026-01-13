from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.loja import Loja
from services.catalogo import CatalogoService
from services.transacao import TransacaoService

from models.base import Produto
from models.livro import Livro
from models.ebook import EBook
from models.apostila import Apostila
from models.cd import CD

app = FastAPI(title="Loja Midias API (sem RMI, protocolo request/response)")

loja = Loja("Loja de Mídias")


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

SERVICES: Dict[str, Any] = {
    "CatalogoService": catalogo_service,
    "TransacaoService": transacao_service,
}


class InvokeArguments(BaseModel):
    args: list = Field(default_factory=list)
    kwargs: Dict[str, Any] = Field(default_factory=dict)


class InvokeRequest(BaseModel):
    requestId: Optional[int] = None
    objectReference: str
    methodId: str
    arguments: InvokeArguments = Field(default_factory=InvokeArguments)


class InvokeReply(BaseModel):
    requestId: Optional[int] = None
    isException: bool
    result: Optional[Any] = None
    error: Optional[str] = None


def _deserialize_value(v: Any) -> Any:
    # converte produto serializado pra objeto
    if isinstance(v, dict) and "__type__" in v:
        return Produto.from_dict(v)
    if isinstance(v, list):
        return [_deserialize_value(x) for x in v]
    if isinstance(v, dict):
        return {k: _deserialize_value(val) for k, val in v.items()}
    return v


def _serialize_value(v: Any) -> Any:
    # converte objetos Produto para dict JSON
    if isinstance(v, Produto):
        return v.to_dict()
    if isinstance(v, list):
        return [_serialize_value(x) for x in v]
    if isinstance(v, dict):
        return {k: _serialize_value(val) for k, val in v.items()}
    return v


@app.post("/invoke", response_model=InvokeReply)
def invoke(req: InvokeRequest):
    try:
        service = SERVICES.get(req.objectReference)
        if service is None:
            raise ValueError(f"Serviço '{req.objectReference}' não encontrado.")

        if not hasattr(service, req.methodId):
            raise ValueError(
                f"Método '{req.methodId}' não existe em '{req.objectReference}'."
            )

        method = getattr(service, req.methodId)

        # desserializa args/kwargs
        args = [_deserialize_value(a) for a in (req.arguments.args or [])]
        kwargs = _deserialize_value(req.arguments.kwargs or {})

        result = method(*args, **kwargs)

        # serializa retorno
        result_external = _serialize_value(result)

        return InvokeReply(
            requestId=req.requestId,
            isException=False,
            result=result_external,
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=InvokeReply(
                requestId=req.requestId,
                isException=True,
                error=str(e),
            ).model_dump(),
        )
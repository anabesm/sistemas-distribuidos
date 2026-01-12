from typing import Any
from models.base import Produto

# representação externa: JSON compatível
def marshal(obj: Any) -> Any:
    # produto por valor
    if isinstance(obj, Produto):
        return {"__kind__": "Produto", "value": obj.to_dict()}
    # lista de produtos
    if isinstance(obj, list) and obj and isinstance(obj[0], Produto):
        return {"__kind__": "ListaProduto", "value": [p.to_dict() for p in obj]}
    # tipos simples
    return obj

def unmarshal(data: Any) -> Any:
    if isinstance(data, dict) and data.get("__kind__") == "Produto":
        return Produto.from_dict(data["value"])
    if isinstance(data, dict) and data.get("__kind__") == "ListaProduto":
        return [Produto.from_dict(d) for d in data["value"]]
    return data

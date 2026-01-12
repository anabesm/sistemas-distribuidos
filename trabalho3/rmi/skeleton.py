from typing import Any
from .marshalling import marshal, unmarshal

# localiza objeto e invoca método, retornando representação externa
class Dispatcher:
    def __init__(self, repository):
        self.repo = repository

    def dispatch(self, object_name: str, method_id: str, args_external: Any) -> Any:
        obj = self.repo.resolve(object_name)
        if isinstance(args_external, dict) and "args" in args_external:
            args = [unmarshal(a) for a in args_external["args"]]
            kwargs = {k: unmarshal(v) for k, v in args_external.get("kwargs", {}).items()}
        else:
            args, kwargs = [], {}
        method = getattr(obj, method_id)
        result = method(*args, **kwargs)
        return marshal(result)

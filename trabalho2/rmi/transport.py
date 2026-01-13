from __future__ import annotations
from .protocol import unpack_args, pack_args, RemoteObjectRef, make_request
from .marshalling import unmarshal
from typing import Any, Dict
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

# cliente RMI
class Requestor:
    def doOperation(self, o: RemoteObjectRef, methodId: str, arguments: Any) -> Any:
        req = make_request(o, methodId, arguments)
        proxy = ServerProxy(f"http://{o.host}:{o.port}", allow_none=True)
        reply_dict = proxy.invoke(req)
        if reply_dict.get("isException"):
            raise RuntimeError(unmarshal(unpack_args(reply_dict["arguments"])))
        result_external = unpack_args(reply_dict["arguments"])
        return unmarshal(result_external)

# servidor RMI
class ServerRequestHandler:
    def __init__(self, host: str, port: int, dispatcher):
        self._server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
        self.dispatcher = dispatcher
        self._server.register_function(self.getRequest, "invoke")

    def getRequest(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        req_id = int(request_dict["requestId"])
        try:
            r = self.dispatcher.dispatch(
                object_name=request_dict["objectReference"],
                method_id=request_dict["methodId"],
                args_external=unpack_args(request_dict["arguments"]),
            )
            return {
                "messageType": 1,
                "requestId": req_id,
                "isException": False,
                "arguments": pack_args(r),
            }
        except Exception as e:
            return {
                "messageType": 1,
                "requestId": req_id,
                "isException": True,
                "arguments": pack_args(str(e)),
            }

    def sendReply(self, *args, **kwargs):
        pass

    def serve_forever(self):
        self._server.serve_forever()

    def start_in_background(self):
        import threading
        t = threading.Thread(target=self.serve_forever, daemon=True)
        t.start()
        return t
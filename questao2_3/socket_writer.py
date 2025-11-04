from __future__ import annotations
import socket

# classe auxiliar para adaptar socket a stream binário
class _SocketWriter:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
    def write(self, b: bytes) -> int:
        self.sock.sendall(b)
        return len(b)
    def flush(self) -> None:
        pass
    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_WR)
        except Exception:
            pass
        self.sock.close()


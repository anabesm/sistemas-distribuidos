import socket

class _SocketReader:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            chunks = []
            while True:
                c = self.sock.recv(4096)
                if not c:
                    break
                chunks.append(c)
            return b"".join(chunks)
        buf = bytearray()
        while len(buf) < n:
            c = self.sock.recv(n - len(buf))
            if not c:
                break
            buf.extend(c)
        return bytes(buf)
    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RD)
        except Exception:
            pass
        self.sock.close()

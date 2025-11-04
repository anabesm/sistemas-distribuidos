import argparse
import socket
import threading
import time
from typing import Dict, Set
from protocol import (
    TYPE_REQUEST, TYPE_REPLY, TYPE_ERROR,
    recv_message, send_message, ProtocolError
)

class VotingState:
    def __init__(self, candidates=None, duration=120):
        self.lock = threading.Lock()
        self.candidates: Dict[str, int] = {c:0 for c in (candidates or ["A","B"])}
        self.voted_users: Set[str] = set()
        self.start_time = time.time()
        self.end_time = self.start_time + duration
        self.closed = False

    def time_left(self) -> int:
        return max(0, int(self.end_time - time.time()))

    def is_open(self) -> bool:
        if self.closed:
            return False
        if time.time() >= self.end_time:
            self.closed = True
            return False
        return True

    def add_candidate(self, name: str):
        with self.lock:
            if name in self.candidates:
                return False, "Candidato já existe."
            self.candidates[name] = 0
            return True, None

    def remove_candidate(self, name: str):
        with self.lock:
            if name not in self.candidates:
                return False, "Candidato inexistente."
            del self.candidates[name]
            return True, None

    def stats(self):
        with self.lock:
            totals = dict(self.candidates)
        total_votes = sum(totals.values())
        percent = {k: (100.0 * v / total_votes) if total_votes>0 else 0.0 for k,v in totals.items()}
        winner = None
        if totals:
            max_votes = max(totals.values())
            winners = [k for k,v in totals.items() if v == max_votes]
            winner = sorted(winners)[0] if winners else None
        return totals, percent, winner, total_votes

def handle_request(payload: dict, state: VotingState, admin_password: str):
    if not isinstance(payload, dict):
        return False, {"error": "Payload inválido."}

    op = payload.get("op")

    if op == "login":
        user = payload.get("user") or "anon"
        role = payload.get("role", "voter")
        with state.lock:
            candidates = list(state.candidates.keys())
        return True, {"ok": True, "user": user, "role": role, "candidates": candidates, "time_left": state.time_left()}

    if op == "get_candidates":
        with state.lock:
            return True, {"candidates": list(state.candidates.keys()), "time_left": state.time_left()}

    if op == "vote":
        user = payload.get("user")
        cand = payload.get("candidate")
        if not user or not cand:
            return False, {"error": "Campos 'user' e 'candidate' são obrigatórios."}
        if not state.is_open():
            return False, {"error": "Votação encerrada."}
        with state.lock:
            if user in state.voted_users:
                return False, {"error": "Usuário já votou."}
            if cand not in state.candidates:
                return False, {"error": "Candidato inexistente."}
            state.candidates[cand] += 1
            state.voted_users.add(user)
            return True, {"ok": True, "time_left": state.time_left()}

    if op in ("add_candidate", "remove_candidate"):
        if payload.get("admin_password") != admin_password:
            return False, {"error": "Admin não autorizado."}
        name = payload.get("candidate")
        if not name:
            return False, {"error": "Campo 'candidate' é obrigatório."}
        if op == "add_candidate":
            ok, err = state.add_candidate(name)
        else:
            ok, err = state.remove_candidate(name)
        if ok:
            with state.lock:
                return True, {"ok": True, "candidates": list(state.candidates.keys())}
        return False, {"error": err or "Falha na operação."}

    if op == "results":
        totals, percent, winner, total_votes = state.stats()
        closed = not state.is_open()
        return True, {"closed": closed, "totals": totals, "percent": percent, "winner": winner, "total_votes": total_votes}

    return False, {"error": f"Operação desconhecida: {op}"}

def client_thread(conn: socket.socket, addr, state: VotingState, admin_password: str):
    with conn:
        try:
            while True:
                msg_type, payload = recv_message(conn)
                if msg_type != TYPE_REQUEST:
                    send_message(conn, TYPE_ERROR, {"error": "Mensagem não é REQUEST."})
                    continue
                ok, reply = handle_request(payload, state, admin_password)
                send_message(conn, TYPE_REPLY if ok else TYPE_ERROR, reply)
        except ProtocolError as e:
            print(f"[{addr}] Encerrando conexão: {e}")
        except Exception as e:
            print(f"[{addr}] Erro inesperado: {e}")

def main():
    parser = argparse.ArgumentParser(description="Servidor de Votação - TCP (unicast)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--duration", type=int, default=120, help="Janela de votação em segundos (default: 120)")
    parser.add_argument("--candidates", nargs="*", default=["A", "B"], help="Lista inicial de candidatos")
    parser.add_argument("--admin-password", default="secret", help="Senha do administrador para operações TCP")
    args = parser.parse_args()

    state = VotingState(candidates=args.candidates, duration=args.duration)
    print(f"Iniciando servidor em {args.host}:{args.port} (deadline em {args.duration}s). Candidatos: {args.candidates}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((args.host, args.port))
        server_sock.listen(16)
        print(f"Servidor escutando em {args.host}:{args.port} ...")

        while True:
            conn, addr = server_sock.accept()
            print(f"[+] Conexão de {addr}")
            t = threading.Thread(target=client_thread, args=(conn, addr, state, args.admin_password), daemon=True)
            t.start()

if __name__ == "__main__":
    main()

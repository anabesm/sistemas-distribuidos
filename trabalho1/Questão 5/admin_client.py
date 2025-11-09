import argparse
import json
import socket
import time
from protocol import recv_message, send_message
from multicast import make_sender, send_note, DEFAULT_GROUP, DEFAULT_PORT

def send_tcp(host, port, payload):
    with socket.create_connection((host, port)) as sock:
        send_message(sock, 0x01, payload)
        msg_type, payload = recv_message(sock)
        return msg_type, payload

def main():
    parser = argparse.ArgumentParser(description="Cliente Administrador - TCP (gerência) + UDP Multicast (notas)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--mgroup", default=DEFAULT_GROUP)
    parser.add_argument("--mport", type=int, default=DEFAULT_PORT)
    parser.add_argument("--miface", default="127.0.0.1", help="Interface local para multicast (ex.: 127.0.0.1 ou IP da rede)")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--admin-password", default="secret")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="Listar candidatos")
    p_add = sub.add_parser("add", help="Adicionar candidato")
    p_add.add_argument("candidate")
    p_rem = sub.add_parser("remove", help="Remover candidato")
    p_rem.add_argument("candidate")
    p_note = sub.add_parser("note", help="Enviar nota (multicast)")
    p_note.add_argument("text", nargs="+")

    sub.add_parser("results", help="Ver resultados")

    args = parser.parse_args()

    if args.cmd == "list":
        _, r = send_tcp(args.host, args.port, {"op":"get_candidates"})
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.cmd == "add":
        _, r = send_tcp(args.host, args.port, {"op":"add_candidate","user":args.user,"admin_password":args.admin_password,"candidate":args.candidate})
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.cmd == "remove":
        _, r = send_tcp(args.host, args.port, {"op":"remove_candidate","user":args.user,"admin_password":args.admin_password,"candidate":args.candidate})
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.cmd == "results":
        _, r = send_tcp(args.host, args.port, {"op":"results"})
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif args.cmd == "note":
        sock, dst = make_sender(group=args.mgroup, port=args.mport, ttl=1, iface_ip=args.miface, loopback=True)
        payload = {"from": args.user, "ts": int(time.time()), "note": " ".join(args.text)}
        send_note(sock, dst, payload)
        print("Nota enviada ao grupo multicast.")
    else:
        print("Comando inválido.")

if __name__ == "__main__":
    main()

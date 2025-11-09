import argparse
import json
import socket
import threading
import time
from protocol import TYPE_REQUEST, recv_message, send_message
from multicast import make_receiver, recv_loop, DEFAULT_GROUP, DEFAULT_PORT

def send_tcp(host, port, payload):
    with socket.create_connection((host, port)) as sock:
        send_message(sock, 0x01, payload)
        msg_type, payload = recv_message(sock)
        return msg_type, payload

def print_note(note):
    ts = time.strftime("%H:%M:%S", time.localtime(note.get("ts", time.time())))
    src = note.get("_from_addr", "?")
    who = note.get("from", "admin")
    text = note.get("note", "")
    print(f"[MULTICAST {ts} {src}] {who}: {text}")

def start_multicast_listener(group, port, iface):
    sock = make_receiver(group=group, port=port, iface_ip=iface)
    t = threading.Thread(target=recv_loop, args=(sock, print_note), daemon=True)
    t.start()
    return t

def main():
    parser = argparse.ArgumentParser(description="Cliente Eleitor - TCP + Multicast")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--mgroup", default=DEFAULT_GROUP)
    parser.add_argument("--mport", type=int, default=DEFAULT_PORT)
    parser.add_argument("--miface", default="127.0.0.1", help="Interface local para multicast (ex.: 127.0.0.1 ou IP da rede)")
    parser.add_argument("--user", default="anon")
    parser.add_argument("--follow", action="store_true", help="Mantém o processo ouvindo notas após o comando")
    parser.add_argument("--keep-seconds", type=int, default=0, help="Mantém ouvindo por N segundos após o comando")
    parser.add_argument("command", choices=["login", "vote", "candidates", "results", "listen"], help="Ação do eleitor")
    parser.add_argument("extra", nargs="*")
    args = parser.parse_args()

    start_multicast_listener(args.mgroup, args.mport, args.miface)

    if args.command == "login":
        payload = {"op":"login", "user": args.user, "role":"voter"}
        _, r = send_tcp(args.host, args.port, payload)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.command == "candidates":
        _, r = send_tcp(args.host, args.port, {"op":"get_candidates"})
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.command == "vote":
        if not args.extra:
            print("Uso: vote <CANDIDATO>")
            return
        cand = args.extra[0]
        _, r = send_tcp(args.host, args.port, {"op":"vote","user":args.user,"candidate":cand})
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.command == "results":
        _, r = send_tcp(args.host, args.port, {"op":"results"})
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.command == "listen":
        print("Ouvindo notas multicast... (Ctrl+C para sair)")
        args.follow = True

    if args.follow:
        print("Aguardando notas... (Ctrl+C para sair)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    elif args.keep_seconds > 0:
        time.sleep(args.keep_seconds)

if __name__ == "__main__":
    main()

import socket
import struct
import json
from typing import Callable, Optional

DEFAULT_GROUP = "239.255.0.1"
DEFAULT_PORT = 6000

def make_sender(group: str = DEFAULT_GROUP, port: int = DEFAULT_PORT, ttl: int = 1, iface_ip: Optional[str] = None, loopback: bool = True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1 if loopback else 0)
    if iface_ip:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(iface_ip))
    return sock, (group, port)

def send_note(sender_sock, dst, payload: dict):
    data = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    sender_sock.sendto(data, dst)

def make_receiver(group: str = DEFAULT_GROUP, port: int = DEFAULT_PORT, iface_ip: str = "0.0.0.0"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((iface_ip, port))
    except OSError:
        sock.bind((group, port))
    try:
        mreq = struct.pack("=4s4s", socket.inet_aton(group), socket.inet_aton(iface_ip))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    except Exception:
        mreq = struct.pack("=4sl", socket.inet_aton(group), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock

def recv_loop(sock, on_message: Callable[[dict], None]):
    while True:
        data, addr = sock.recvfrom(65535)
        try:
            note = json.loads(data.decode('utf-8'))
        except Exception:
            continue
        note['_from_addr'] = f"{addr[0]}:{addr[1]}"
        on_message(note)

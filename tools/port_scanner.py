#!/usr/bin/env python3
"""
CyberShield Academy — Custom Port Scanner
A learning tool to understand how Nmap works under the hood.
For authorized use only.
"""

import socket
import sys
import threading
import argparse
from datetime import datetime
from queue import Queue

# Common ports and their services
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}

open_ports = []
lock = threading.Lock()

def scan_port(target: str, port: int, timeout: float = 1.0) -> bool:
    """Attempt a TCP connection to target:port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except (socket.error, OSError):
        return False

def get_banner(target: str, port: int) -> str:
    """Attempt to grab service banner"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner[:80] if banner else ""
    except Exception:
        return ""

def worker(target: str, queue: Queue, verbose: bool):
    """Thread worker — scan ports from queue"""
    while not queue.empty():
        port = queue.get()
        if scan_port(target, port):
            service = COMMON_PORTS.get(port, "Unknown")
            banner = get_banner(target, port) if verbose else ""
            with lock:
                open_ports.append((port, service, banner))
                print(f"  \033[92m[OPEN]\033[0m  {port:5d}/tcp  {service}")
                if banner and verbose:
                    print(f"         Banner: {banner[:60]}")
        queue.task_done()

def scan(target: str, start_port: int, end_port: int,
         threads: int = 100, verbose: bool = False):
    
    # Resolve hostname
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"\033[91m[ERROR]\033[0m Cannot resolve: {target}")
        sys.exit(1)
    
    print(f"""
\033[94m\033[1m
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
 ╚══════╝╚═╝   ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝
                              Port Scanner v1.0
\033[0m""")
    
    print(f"  Target  : {target} ({ip})")
    print(f"  Ports   : {start_port}–{end_port}")
    print(f"  Threads : {threads}")
    print(f"  Started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  {'─'*50}")
    
    queue = Queue()
    for port in range(start_port, end_port + 1):
        queue.put(port)
    
    thread_list = []
    for _ in range(min(threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(ip, queue, verbose), daemon=True)
        t.start()
        thread_list.append(t)
    
    queue.join()
    
    print(f"\n  {'─'*50}")
    print(f"  Scan complete: {len(open_ports)} open port(s) found")
    print(f"  Finished    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    if open_ports:
        print(f"  \033[1mOpen Ports Summary:\033[0m")
        for port, service, _ in sorted(open_ports):
            risk = ""
            if port in [23, 21]:
                risk = "  \033[91m⚠ INSECURE PROTOCOL\033[0m"
            elif port == 3306 and target not in ("127.0.0.1", "localhost"):
                risk = "  \033[91m⚠ DATABASE EXPOSED\033[0m"
            print(f"  {port:5d}/tcp  {service}{risk}")
    print()

def main():
    parser = argparse.ArgumentParser(
        description="CyberShield Academy — Educational Port Scanner",
        epilog="⚠ For authorized use only. Never scan systems without permission."
    )
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end",   type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show banner grabbing")
    parser.add_argument("--top", action="store_true", help="Scan only common ports")
    
    args = parser.parse_args()
    
    if args.top:
        print(f"\033[93m[*] Scanning common ports only\033[0m")
        queue = Queue()
        for port in COMMON_PORTS.keys():
            queue.put(port)
        ip = socket.gethostbyname(args.target)
        print(f"  Target: {args.target} ({ip})\n")
        for port in COMMON_PORTS.keys():
            if scan_port(ip, port):
                service = COMMON_PORTS[port]
                print(f"  \033[92m[OPEN]\033[0m  {port:5d}/tcp  {service}")
    else:
        scan(args.target, args.start, args.end, args.threads, args.verbose)

if __name__ == "__main__":
    print("\033[93m⚠  Educational tool — only use on systems you own or have permission to scan.\033[0m\n")
    main()

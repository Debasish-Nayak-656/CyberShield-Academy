#!/usr/bin/env python3
"""
CyberShield Academy — Hash Identifier & Cracker
Educational tool for understanding password hashing weaknesses.
"""

import hashlib
import sys
import argparse
import re
from pathlib import Path

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

HASH_PATTERNS = {
    "MD5":        (r"^[a-f0-9]{32}$",   "hashlib.md5"),
    "SHA-1":      (r"^[a-f0-9]{40}$",   "hashlib.sha1"),
    "SHA-256":    (r"^[a-f0-9]{64}$",   "hashlib.sha256"),
    "SHA-512":    (r"^[a-f0-9]{128}$",  "hashlib.sha512"),
    "NTLM":       (r"^[a-f0-9]{32}$",   "ntlm"),
    "bcrypt":     (r"^\$2[ab]?\$",      "bcrypt"),
    "SHA-512crypt":(r"^\$6\$",          "linux_sha512"),
}

HASH_SECURITY = {
    "MD5":         f"{RED}BROKEN — collisions found, GPU cracks in seconds{RESET}",
    "SHA-1":       f"{RED}WEAK — collisions demonstrated, avoid for passwords{RESET}",
    "SHA-256":     f"{YELLOW}FAIR — fast hash, use PBKDF2/bcrypt/argon2 for passwords{RESET}",
    "SHA-512":     f"{YELLOW}FAIR — same issue as SHA-256 for passwords{RESET}",
    "NTLM":        f"{RED}BROKEN — equivalent to MD5, rainbowtable databases exist{RESET}",
    "bcrypt":      f"{GREEN}GOOD — slow by design, salt built-in{RESET}",
    "SHA-512crypt": f"{GREEN}GOOD — used in Linux /etc/shadow, salted+iterated{RESET}",
}

def identify_hash(hash_str: str) -> list:
    """Try to identify the hash type by length and pattern"""
    candidates = []
    h = hash_str.strip().lower()
    for name, (pattern, _) in HASH_PATTERNS.items():
        if re.match(pattern, h, re.IGNORECASE):
            candidates.append(name)
    return candidates

def crack_hash(target_hash: str, wordlist_path: str, algorithm: str) -> str | None:
    """Attempt to crack hash using a wordlist"""
    target = target_hash.strip().lower()
    
    algo_map = {
        "md5":    hashlib.md5,
        "sha1":   hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    
    if algorithm.lower() not in algo_map:
        print(f"{RED}Unsupported algorithm: {algorithm}{RESET}")
        return None
    
    hash_func = algo_map[algorithm.lower()]
    
    try:
        wordlist = Path(wordlist_path)
        if not wordlist.exists():
            print(f"{RED}Wordlist not found: {wordlist_path}{RESET}")
            return None
        
        total = sum(1 for _ in open(wordlist_path, 'r', errors='ignore'))
        print(f"  Wordlist: {wordlist_path} ({total:,} words)")
        print(f"  Algorithm: {algorithm.upper()}")
        print(f"  Target: {target_hash}\n")
        
        count = 0
        with open(wordlist_path, 'r', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue
                
                count += 1
                candidate = hash_func(word.encode()).hexdigest()
                
                if count % 100000 == 0:
                    pct = (count / total) * 100
                    print(f"\r  Progress: {count:,}/{total:,} ({pct:.1f}%) — trying: {word[:20]:20s}", end="")
                
                if candidate == target:
                    print(f"\n\n  {GREEN}{BOLD}✓ CRACKED!{RESET}")
                    print(f"  Hash   : {target_hash}")
                    print(f"  Plain  : {GREEN}{BOLD}{word}{RESET}")
                    print(f"  Tries  : {count:,}\n")
                    return word
        
        print(f"\n\n  {RED}Not found in wordlist after {count:,} attempts.{RESET}")
        print(f"  Try: hashcat -m 0 {target_hash} rockyou.txt\n")
        return None
        
    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}Interrupted after {count:,} attempts.{RESET}\n")
        return None

def generate_hashes(plaintext: str):
    """Show hash of given plaintext using multiple algorithms"""
    data = plaintext.encode()
    print(f"\n  {BOLD}Hashes for: \"{plaintext}\"{RESET}\n")
    algos = [
        ("MD5",    hashlib.md5(data).hexdigest(),    "BROKEN"),
        ("SHA-1",  hashlib.sha1(data).hexdigest(),   "WEAK"),
        ("SHA-256",hashlib.sha256(data).hexdigest(), "BETTER"),
        ("SHA-512",hashlib.sha512(data).hexdigest(), "BEST"),
    ]
    for name, digest, rating in algos:
        color = RED if rating in ("BROKEN","WEAK") else (YELLOW if rating == "BETTER" else GREEN)
        print(f"  {name:8s} [{color}{rating:6s}{RESET}]  {digest}")
    print()

def main():
    print(f"\n{BLUE}{BOLD}  CyberShield Academy — Hash Tool{RESET}\n")
    
    parser = argparse.ArgumentParser(description="Hash identifier, generator, and cracker (educational)")
    subparsers = parser.add_subparsers(dest="command")
    
    # identify
    id_parser = subparsers.add_parser("identify", help="Identify hash type")
    id_parser.add_argument("hash", help="Hash string to identify")
    
    # crack
    crack_parser = subparsers.add_parser("crack", help="Dictionary attack on a hash")
    crack_parser.add_argument("hash", help="Hash to crack")
    crack_parser.add_argument("-w", "--wordlist", default="/usr/share/wordlists/rockyou.txt")
    crack_parser.add_argument("-a", "--algorithm", default="md5",
                              choices=["md5","sha1","sha256","sha512"])
    
    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate hashes for a string")
    gen_parser.add_argument("plaintext", help="String to hash")
    
    args = parser.parse_args()
    
    if args.command == "identify":
        candidates = identify_hash(args.hash)
        if candidates:
            print(f"  Hash: {args.hash}")
            print(f"  Possible types:")
            for c in candidates:
                sec = HASH_SECURITY.get(c, "")
                print(f"    → {BOLD}{c}{RESET}")
                if sec:
                    print(f"      Security: {sec}")
        else:
            print(f"  {YELLOW}Unknown hash type.{RESET}")
    
    elif args.command == "crack":
        crack_hash(args.hash, args.wordlist, args.algorithm)
    
    elif args.command == "generate":
        generate_hashes(args.plaintext)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

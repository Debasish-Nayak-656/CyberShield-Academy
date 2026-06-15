#!/usr/bin/env python3
"""
CyberShield Academy — Environment Checker
Verifies all required tools are installed and accessible.
"""

import subprocess
import sys
import shutil
from dataclasses import dataclass
from typing import List

@dataclass
class Tool:
    name: str
    command: str
    module: str
    required: bool = True

TOOLS: List[Tool] = [
    Tool("Python 3",        "python3 --version",    "All Modules"),
    Tool("pip",             "pip --version",         "All Modules"),
    Tool("Nmap",            "nmap --version",        "Networking / Pentesting"),
    Tool("Wireshark",       "wireshark --version",   "Networking"),
    Tool("Metasploit",      "msfconsole --version",  "Pentesting",     required=False),
    Tool("sqlmap",          "sqlmap --version",      "Web Security",   required=False),
    Tool("hashcat",         "hashcat --version",     "Cryptography",   required=False),
    Tool("John the Ripper", "john --version",        "Cryptography",   required=False),
    Tool("Gobuster",        "gobuster version",      "Recon",          required=False),
    Tool("Nikto",           "nikto --version",       "Web Security",   required=False),
    Tool("theHarvester",    "theHarvester --help",   "OSINT",          required=False),
    Tool("Git",             "git --version",         "General"),
    Tool("Docker",          "docker --version",      "Labs",           required=False),
]

PYTHON_PACKAGES = [
    "pycryptodome",
    "requests",
    "scapy",
    "colorama",
    "beautifulsoup4",
]

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def check_tool(tool: Tool) -> bool:
    try:
        result = subprocess.run(
            tool.command.split(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_python_package(package: str) -> bool:
    try:
        __import__(package.replace("-", "_").split("=")[0])
        return True
    except ImportError:
        return False

def print_banner():
    print(f"""
{BLUE}{BOLD}
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ 
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗███████║██║█████╗  ██║     ██║  ██║
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝
                            A C A D E M Y  —  Environment Checker
{RESET}""")

def main():
    print_banner()
    
    print(f"{BOLD}[ Checking Required Tools ]{RESET}\n")
    
    passed = 0
    failed = 0
    optional_missing = 0
    
    for tool in TOOLS:
        ok = check_tool(tool)
        if ok:
            status = f"{GREEN}✓ FOUND{RESET}"
            passed += 1
        else:
            if tool.required:
                status = f"{RED}✗ MISSING{RESET}"
                failed += 1
            else:
                status = f"{YELLOW}○ NOT INSTALLED (optional){RESET}"
                optional_missing += 1
        
        req_marker = "" if tool.required else f" {YELLOW}[optional]{RESET}"
        print(f"  {status:30s} {tool.name:20s} → {tool.module}{req_marker}")
    
    print(f"\n{BOLD}[ Checking Python Packages ]{RESET}\n")
    
    pkg_ok = 0
    pkg_fail = 0
    for pkg in PYTHON_PACKAGES:
        installed = check_python_package(pkg)
        if installed:
            print(f"  {GREEN}✓ {pkg}{RESET}")
            pkg_ok += 1
        else:
            print(f"  {RED}✗ {pkg}  →  pip install {pkg}{RESET}")
            pkg_fail += 1
    
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}Summary:{RESET}")
    print(f"  Tools:    {GREEN}{passed} found{RESET}, {RED}{failed} missing{RESET}, {YELLOW}{optional_missing} optional not installed{RESET}")
    print(f"  Packages: {GREEN}{pkg_ok} installed{RESET}, {RED}{pkg_fail} missing{RESET}")
    
    if failed == 0 and pkg_fail == 0:
        print(f"\n  {GREEN}{BOLD}✓ You're all set! Start with: modules/01-networking/README.md{RESET}")
    elif failed == 0:
        print(f"\n  {YELLOW}{BOLD}⚠ Run: pip install -r requirements.txt to install missing packages{RESET}")
    else:
        print(f"\n  {RED}{BOLD}✗ Install missing required tools before proceeding.{RESET}")
        print(f"  {BLUE}  Recommended: Use Kali Linux — all tools pre-installed{RESET}")
        print(f"  {BLUE}  Download: https://www.kali.org/get-kali/{RESET}")
    
    print()
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

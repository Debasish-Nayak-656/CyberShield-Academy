# Module 04 — OSINT & Reconnaissance

**Duration:** Week 7 | **Difficulty:** 🟢 Beginner | **Status:** ✅ Completed

---

## Learning Objectives

- Gather intelligence on a target using only public sources
- Use professional OSINT tools effectively
- Understand the attacker's information-gathering process
- Know how to defend against OSINT attacks

---

## What is OSINT?

**Open Source Intelligence (OSINT)** is the collection and analysis of information from publicly available sources. Attackers use OSINT to map the attack surface *before* touching a target.

Sources include: websites, social media, DNS records, WHOIS, job postings, GitHub, Shodan, and more.

---

## Passive Reconnaissance (No Direct Contact)

### DNS Enumeration

```bash
# Basic DNS lookup
dig target.com ANY
dig target.com MX      # mail servers
dig target.com NS      # name servers
dig target.com TXT     # SPF, DKIM, verification records

# Reverse DNS lookup
dig -x 93.184.216.34

# Zone transfer attempt (misconfiguration check)
dig axfr @ns1.target.com target.com

# dnsrecon — comprehensive DNS enumeration
dnsrecon -d target.com -t std
dnsrecon -d target.com -t brt   # brute force subdomains
```

### WHOIS & Registration Data

```bash
# WHOIS lookup
whois target.com
whois 93.184.216.34   # reverse WHOIS by IP

# Look for:
# - Registrant name / email (sometimes hidden by privacy)
# - Registration / expiry dates
# - Name servers
# - Registrar abuse contact
```

### Google Dorks

```
# Find subdomains
site:target.com

# Find specific file types (may expose sensitive docs)
site:target.com filetype:pdf
site:target.com filetype:xlsx
site:target.com filetype:sql

# Find admin/login pages
site:target.com inurl:admin
site:target.com inurl:login
site:target.com inurl:dashboard

# Find exposed directories
site:target.com intitle:"index of"

# Find configuration files
site:target.com ext:conf OR ext:config OR ext:cfg

# Find cached login pages
cache:target.com/login

# Combine operators
site:target.com filetype:pdf intext:"confidential"
```

### Shodan — The Hacker's Search Engine

Shodan indexes internet-connected devices and their open ports/services.

```bash
# Install CLI
pip install shodan
shodan init YOUR_API_KEY

# Search for target
shodan search hostname:target.com

# Get info on an IP
shodan host 93.184.216.34

# Common search filters
hostname:target.com
org:"Target Corporation"
port:3389 country:IN          # RDP in India
product:nginx version:1.14    # specific server version
vuln:CVE-2021-44228           # Log4Shell vulnerable systems
```

**Shodan reveals:**
- Open ports and services
- Software versions (find unpatched systems)
- SSL certificate info
- Geographic location of servers
- Whether default credentials are in use

---

## Active Reconnaissance

### Subdomain Enumeration

```bash
# Gobuster DNS brute force
gobuster dns -d target.com \
             -w /usr/share/wordlists/dns/subdomains-top1mil-5000.txt \
             -t 50

# Subfinder — passive + active
subfinder -d target.com -all -o subdomains.txt

# amass — comprehensive
amass enum -d target.com
amass enum -passive -d target.com

# Certificate transparency (passive, powerful)
# curl https://crt.sh/?q=%25.target.com&output=json | python3 -m json.tool
curl "https://crt.sh/?q=%.target.com&output=json" | \
  python3 -c "import json,sys; data=json.load(sys.stdin); \
  [print(d['name_value']) for d in data]" | sort -u
```

### Email Harvesting

```bash
# theHarvester
theHarvester -d target.com -b google,bing,linkedin,twitter -l 500

# Finds: emails, employee names, subdomains, IPs

# Hunter.io — web-based email finder
# https://hunter.io

# LinkedIn recon (manual)
# Search: site:linkedin.com "target company" "security engineer"
```

### Web Technology Fingerprinting

```bash
# Wappalyzer (browser extension — easiest)
# Shows: CMS, frameworks, server, CDN, analytics

# Whatweb — CLI fingerprinting
whatweb target.com
whatweb -a 3 target.com   # aggressive mode

# BuiltWith — online tool
# https://builtwith.com

# Check HTTP headers (often reveal server info)
curl -I https://target.com
# Look for: Server, X-Powered-By, X-Generator
```

---

## OSINT Python Script

```python
#!/usr/bin/env python3
# osint_recon.py — Quick OSINT gathering script

import socket
import subprocess
import requests
import json
from datetime import datetime

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "Could not resolve"

def get_headers(domain):
    try:
        r = requests.get(f"https://{domain}", timeout=5, verify=False)
        interesting = ["Server", "X-Powered-By", "X-Generator", "Via", "CF-Ray"]
        return {h: r.headers.get(h) for h in interesting if r.headers.get(h)}
    except Exception:
        return {}

def check_robots(domain):
    try:
        r = requests.get(f"https://{domain}/robots.txt", timeout=5)
        if r.status_code == 200:
            return r.text[:500]
    except Exception:
        pass
    return "Not found"

def recon(domain):
    print(f"\n{'='*60}")
    print(f"  OSINT Recon: {domain}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    print(f"[*] IP Address: {get_ip(domain)}")
    
    print(f"\n[*] HTTP Headers:")
    for k, v in get_headers(domain).items():
        print(f"    {k}: {v}")
    
    print(f"\n[*] robots.txt:\n{check_robots(domain)}")
    
    print(f"\n[*] DNS Records:")
    for rtype in ["A", "MX", "NS", "TXT"]:
        result = run(f"dig {domain} {rtype} +short")
        if result:
            print(f"    {rtype}: {result[:100]}")
    
    print(f"\n[*] Certificate transparency (subdomains):")
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        r = requests.get(url, timeout=10)
        subs = set()
        for entry in r.json():
            for name in entry["name_value"].split("\n"):
                subs.add(name.strip())
        for s in sorted(subs)[:20]:
            print(f"    {s}")
        if len(subs) > 20:
            print(f"    ... and {len(subs)-20} more")
    except Exception as e:
        print(f"    Error: {e}")

if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    recon(domain)
```

---

## Defending Against OSINT

| Attack Vector | Defense |
|---------------|---------|
| WHOIS exposes registrant data | Use WHOIS privacy / proxy registration |
| Google dorks find exposed files | robots.txt, remove sensitive files, WAF |
| LinkedIn exposes employees | Security awareness training on oversharing |
| Shodan finds open ports | Firewall rules, only expose necessary ports |
| Certificate transparency | Expected — can't hide; monitor for unauthorized certs |
| Job postings reveal tech stack | Redact specific versions/tools from postings |

---

## Practice Questions

1. What is the difference between active and passive reconnaissance?
2. How can you find subdomains without directly querying the target?
3. Why do attackers look at job postings during OSINT?
4. What does Shodan index and why is it useful for attackers?

---

## Next Module → [05 — Cryptography](../05-cryptography/README.md)

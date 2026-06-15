# Lab 01 — Network Scanning with Nmap

**Module:** Networking Fundamentals | **Duration:** 90 minutes | **Difficulty:** 🟢 Beginner

---

## Objective

By the end of this lab you will:
- Discover live hosts on a network
- Identify open ports and running services
- Detect operating systems of remote hosts
- Export scan results in multiple formats
- Understand the difference between scan types

---

## Lab Setup

```bash
# Option A: Use Metasploitable 2 VM (recommended)
# Download: https://sourceforge.net/projects/metasploitable/
# Boot the VM — note its IP address with:  ifconfig
# Your Kali IP and Metasploitable must be on the same network (Host-Only adapter)

# Option B: Scan your local network (use with caution — only scan your own network)
# Find your subnet:
ip addr show        # look for your IP, e.g. 192.168.1.5/24

# Option C: Use a safe online target
# scanme.nmap.org  (Nmap's official scan-me server — authorized)
```

---

## Task 1 — Host Discovery

```bash
# Ping sweep — find all live hosts
nmap -sn 192.168.1.0/24

# Expected output:
# Host: 192.168.1.1 (router.local)  Latency: 0.00s
# Host: 192.168.1.5 (kali)          Latency: 0.00s
# Host: 192.168.1.10 (metasploitable) Latency: 0.00s

# Save to file
nmap -sn 192.168.1.0/24 -oN lab01_hosts.txt
```

**Record your findings:**
- How many hosts did you find?
- What is the target's IP address?

---

## Task 2 — Basic Port Scan

```bash
# Scan the top 1000 most common ports
nmap 192.168.1.10

# Scan specific port range
nmap -p 1-100 192.168.1.10

# Scan all 65535 ports (slower but thorough)
nmap -p- 192.168.1.10
```

**Record open ports found:**
| Port | Protocol | State |
|------|----------|-------|
| | | |

---

## Task 3 — Service & Version Detection

```bash
# Detect service versions
nmap -sV 192.168.1.10

# Increase intensity for better detection (0-9, default 7)
nmap -sV --version-intensity 9 192.168.1.10
```

**Record service versions:**
| Port | Service | Version |
|------|---------|---------|
| 21 | FTP | |
| 22 | SSH | |
| 80 | HTTP | |

**Question:** Why is knowing the exact version important for an attacker?

---

## Task 4 — OS Detection

```bash
# OS detection (requires root/sudo)
sudo nmap -O 192.168.1.10

# Aggressive detection
sudo nmap -O --osscan-guess 192.168.1.10
```

**Record:** What OS did Nmap identify? How confident was it?

---

## Task 5 — NSE Scripts (Nmap Scripting Engine)

```bash
# Default scripts (safe, commonly used)
nmap -sC 192.168.1.10

# Specific script categories
nmap --script=banner 192.168.1.10            # grab banners
nmap --script=http-title 192.168.1.10        # web page titles
nmap --script=ftp-anon 192.168.1.10          # anonymous FTP check
nmap --script=ssh-auth-methods 192.168.1.10  # SSH auth methods

# Vulnerability scripts (be careful — can be noisy)
nmap --script=vuln 192.168.1.10

# List all available scripts
ls /usr/share/nmap/scripts/ | grep "http-"
```

---

## Task 6 — Full Aggressive Scan

```bash
# Combines -sV, -O, -sC and traceroute
sudo nmap -A 192.168.1.10 -oA lab01_full_scan

# This creates 3 files:
# lab01_full_scan.nmap  — human readable
# lab01_full_scan.xml   — machine readable
# lab01_full_scan.gnmap — grep-friendly
```

---

## Task 7 — Stealth Techniques

```bash
# SYN scan (half-open, less likely to be logged)
sudo nmap -sS 192.168.1.10

# UDP scan (slower, finds different services)
sudo nmap -sU --top-ports 20 192.168.1.10

# Decoy scan (disguise source)
sudo nmap -D RND:5 192.168.1.10

# Slow scan (evade IDS rate thresholds)
nmap -T1 192.168.1.10    # T0=paranoid, T1=sneaky, T5=insane
```

---

## Task 8 — Analyze Results for Vulnerabilities

Look at your scan results and answer:

1. **FTP (port 21):** Is anonymous login enabled? (`ftp-anon` script)
2. **SSH (port 22):** What version? Is it outdated?
3. **HTTP (port 80):** What web server/version? Known CVEs?
4. **MySQL (port 3306):** Is it accessible from outside? Should it be?

```bash
# Check for anonymous FTP
nmap --script ftp-anon -p 21 192.168.1.10

# Try connecting manually
ftp 192.168.1.10
# Username: anonymous
# Password: (press enter or use any email)
```

---

## Lab Report Template

Fill in after completing all tasks:

```
Lab 01 Report — Network Scanning
Student: _______________
Date: _______________
Target IP: _______________

1. Live hosts discovered: ___
2. Open ports on target: _______________
3. Operating system: _______________
4. Most interesting service found: _______________
5. Potential vulnerability identified: _______________
6. What would you do next as a pentester?

Notes:
_______________________________________________
```

---

## Cheat Sheet

```bash
nmap -sn   192.168.1.0/24    # ping sweep
nmap -sS   target             # stealth SYN scan
nmap -sV   target             # version detection
nmap -O    target             # OS detection
nmap -sC   target             # default scripts
nmap -A    target             # all of the above
nmap -p-   target             # all ports
nmap -T4   target             # faster timing
nmap -oN   out.txt target     # normal output
nmap -oX   out.xml target     # XML output
nmap -oA   out target         # all formats
```

---

## Next Lab → [Lab 02 — Wireshark Traffic Analysis](../lab-02-wireshark/README.md)

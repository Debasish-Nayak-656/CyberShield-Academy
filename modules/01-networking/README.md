# Module 01 — Networking Fundamentals

**Duration:** Week 1–2 | **Difficulty:** 🟢 Beginner | **Status:** ✅ Completed

---

## Learning Objectives

By the end of this module you will be able to:
- Explain the OSI and TCP/IP models and identify which layer each protocol operates on
- Capture and analyze live network traffic with Wireshark
- Use Nmap to discover hosts and open ports on a network
- Understand how DNS, ARP, DHCP, and ICMP work at a packet level

---

## Topics Covered

### 1. The OSI Model

```
Layer 7 — Application   → HTTP, FTP, SMTP, DNS
Layer 6 — Presentation  → SSL/TLS, JPEG, ASCII
Layer 5 — Session       → NetBIOS, RPC
Layer 4 — Transport     → TCP, UDP
Layer 3 — Network       → IP, ICMP, ARP
Layer 2 — Data Link     → Ethernet, MAC, Switch
Layer 1 — Physical      → Cables, Hubs, Wi-Fi signals
```

**Security relevance:** Knowing which layer an attack targets helps you choose the right defense.
- ARP spoofing = Layer 2
- IP spoofing = Layer 3
- SYN flood = Layer 4
- SQL injection = Layer 7

### 2. TCP Three-Way Handshake

```
Client                    Server
  |--- SYN (seq=100) ------→|
  |←-- SYN-ACK (seq=200) ---|
  |--- ACK (seq=201) ------→|
  |  [Connection Established] |
```

A **SYN flood attack** sends thousands of SYN packets without completing the handshake, exhausting server resources.

### 3. Key Protocols

| Protocol | Port | Transport | Purpose |
|----------|------|-----------|---------|
| HTTP | 80 | TCP | Web traffic (unencrypted) |
| HTTPS | 443 | TCP | Encrypted web traffic |
| SSH | 22 | TCP | Secure remote shell |
| FTP | 21 | TCP | File transfer |
| DNS | 53 | UDP/TCP | Domain name resolution |
| DHCP | 67/68 | UDP | IP address assignment |
| SMTP | 25 | TCP | Email sending |
| RDP | 3389 | TCP | Remote desktop |

---

## Practical Labs

### Lab 1.1 — Wireshark Basics

```bash
# Capture traffic on your network interface
sudo wireshark &

# Or use tcpdump from the command line
sudo tcpdump -i eth0 -w capture.pcap

# Filter HTTP traffic
sudo tcpdump -i eth0 port 80

# Filter by IP
sudo tcpdump -i eth0 host 192.168.1.1
```

**Wireshark filters to know:**
```
http                    — show only HTTP
tcp.port == 443         — HTTPS traffic
ip.addr == 192.168.1.5  — traffic to/from this IP
dns                     — DNS queries only
arp                     — ARP packets
tcp.flags.syn == 1      — SYN packets (port scans)
```

### Lab 1.2 — Nmap Network Scanning

```bash
# Ping sweep — discover live hosts
nmap -sn 192.168.1.0/24

# Basic port scan
nmap 192.168.1.10

# Service/version detection
nmap -sV 192.168.1.10

# OS detection
nmap -O 192.168.1.10

# Aggressive scan (combines -sV, -O, scripts)
nmap -A 192.168.1.10

# Scan all 65535 ports
nmap -p- 192.168.1.10

# Stealth SYN scan (requires root)
sudo nmap -sS 192.168.1.0/24

# Save output to file
nmap -oN scan_results.txt 192.168.1.0/24
```

### Lab 1.3 — ARP Analysis

```bash
# View your ARP table
arp -a

# Watch ARP packets in real time
sudo tcpdump -i eth0 arp -n

# Detect ARP spoofing: if same IP maps to two different MACs — alert!
```

---

## Practice Questions

1. Which OSI layer does a router operate at?
2. What is the difference between TCP and UDP?
3. Why is port 22 important in security?
4. How does ARP poisoning work, and how can it be detected?
5. What does the `-sV` flag do in Nmap?

---

## Key Takeaways

- The OSI model is your mental map for understanding where attacks happen
- Wireshark is the most important tool for understanding what's actually on the wire
- Nmap is the go-to tool for reconnaissance — understanding it is fundamental to both attack and defense
- Unencrypted protocols (HTTP, FTP, Telnet) send credentials in plaintext — always visible in Wireshark

---

## Next Module → [02 — Linux for Security](../02-linux/README.md)

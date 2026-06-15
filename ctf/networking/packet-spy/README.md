# CTF Challenge #2 — Packet Spy

**Category:** Networking | **Points:** 100 | **Difficulty:** 🟢 Easy

---

## Challenge Description

A PCAP file was captured on a coffee shop Wi-Fi network. The attacker intercepted someone logging in over an unencrypted connection. Find the stolen credentials.

**File:** `capture.pcap` (in this folder)

---

## Learning Goal

Understand why unencrypted protocols (HTTP, FTP, Telnet) are dangerous on untrusted networks, and why HTTPS is mandatory.

---

## Solution Steps

```bash
# Open in Wireshark
wireshark capture.pcap

# Filter for HTTP POST requests (login forms send POST)
# Wireshark filter: http.request.method == "POST"

# Look for credentials in the packet details
# Right-click → Follow → TCP Stream

# From command line with tshark
tshark -r capture.pcap -Y "http.request.method==POST" -T fields \
       -e http.host \
       -e http.request.uri \
       -e urlencoded-form.value

# Search for credentials
strings capture.pcap | grep -i "username\|password\|user=\|pass="

# Follow TCP stream for session #N
tshark -r capture.pcap -z follow,tcp,ascii,0
```

---

## What You'll Find

The PCAP contains an HTTP POST to `http://login.example.com/auth`:

```
POST /auth HTTP/1.1
Host: login.example.com
Content-Type: application/x-www-form-urlencoded

username=admin&password=hunter2
```

**Flag:** `FLAG{w1r3sh4rk_m4st3r}`

---

## Why This Matters

```
HTTP  (port 80)  → plaintext → ANYONE on the network can read it
HTTPS (port 443) → encrypted → only endpoints can read it

On public Wi-Fi, an attacker can:
1. Set up an evil twin access point
2. Intercept ALL unencrypted traffic
3. Steal credentials, session cookies, personal data
```

**Defense:**
- Always use HTTPS
- Use a VPN on public Wi-Fi
- Enable HSTS (HTTP Strict Transport Security) on your servers
- Never send credentials over HTTP

---

## Create Your Own PCAP Challenge

```bash
# Capture traffic
sudo tcpdump -i eth0 -w my_capture.pcap

# Or capture specific traffic
sudo tcpdump -i eth0 port 80 -w http_capture.pcap

# Replay a capture
tcpreplay -i eth0 capture.pcap
```

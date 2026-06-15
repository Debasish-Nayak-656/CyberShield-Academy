# Lab Environment Setup Guide

## Recommended Setup: Kali Linux VM

### Step 1 — Install VirtualBox
Download from https://www.virtualbox.org/

### Step 2 — Download Kali Linux
Get the VM image from https://www.kali.org/get-kali/#kali-virtual-machines

### Step 3 — Import into VirtualBox
- File → Import Appliance → select .ova file
- Recommended: 4GB RAM, 2 CPUs, 50GB disk

### Step 4 — Network Configuration
```
Adapter 1: NAT (for internet access)
Adapter 2: Host-Only (for lab communication)
```

### Step 5 — Clone this repository
```bash
git clone https://github.com/YOUR-USERNAME/CyberShield-Academy.git
cd CyberShield-Academy
pip install -r requirements.txt
python tools/env_check.py
```

---

## Vulnerable VMs for Practice

| VM | Download | Used In |
|----|----------|---------|
| Metasploitable 2 | https://sourceforge.net/projects/metasploitable/ | Module 6 |
| DVWA | https://github.com/digininja/DVWA | Module 3 |
| VulnHub | https://vulnhub.com | General |
| OWASP WebGoat | https://owasp.org/www-project-webgoat/ | Module 3 |

---

## Online Platforms (No Setup Required)

| Platform | Best For | Cost |
|----------|---------|------|
| TryHackMe | Beginners, guided | Free tier |
| HackTheBox | Intermediate+ | Free tier |
| PicoCTF | CTF challenges | Free |
| PortSwigger Web Academy | Web security | Free |
| Cybrary | Video courses | Free tier |

---

## Docker Lab Setup

Many labs in this project use Docker for easy setup:

```bash
# Install Docker (Kali)
sudo apt update && sudo apt install -y docker.io docker-compose
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# Start a specific lab
cd labs/lab-03-burpsuite
docker-compose up -d

# Stop lab
docker-compose down
```

---

## Troubleshooting

**Nmap requires root:**
```bash
sudo nmap -sS target
```

**Permission denied on Python scripts:**
```bash
chmod +x tools/port_scanner.py
```

**Wireshark interface not showing:**
```bash
sudo wireshark
# Or add your user to wireshark group:
sudo usermod -aG wireshark $USER
```

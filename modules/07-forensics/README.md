# Module 07 — Digital Forensics & Incident Response

**Duration:** Week 12–13 | **Difficulty:** 🔴 Advanced | **Status:** 🔒 Upcoming

---

## Learning Objectives

- Perform memory forensics using Volatility
- Analyze disk images with Autopsy
- Parse and correlate security logs
- Follow a structured incident response process
- Identify indicators of compromise (IOCs)

---

## Incident Response Phases (NIST SP 800-61)

```
1. PREPARATION      → Policies, playbooks, tools ready
2. DETECTION        → Identify the incident
3. CONTAINMENT      → Stop the spread
4. ERADICATION      → Remove the threat
5. RECOVERY         → Restore to normal ops
6. LESSONS LEARNED  → Post-incident review
```

---

## Memory Forensics with Volatility

```bash
# Install Volatility 3
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3 && pip install -r requirements.txt

# Identify OS profile from memory dump
python3 vol.py -f memory.dmp windows.info

# List running processes
python3 vol.py -f memory.dmp windows.pslist

# Process tree (spot injected/hidden processes)
python3 vol.py -f memory.dmp windows.pstree

# Network connections at time of dump
python3 vol.py -f memory.dmp windows.netstat

# Find injected code (malware indicator)
python3 vol.py -f memory.dmp windows.malfind

# Dump a suspicious process
python3 vol.py -f memory.dmp windows.dumpfiles --pid 1234

# Command history
python3 vol.py -f memory.dmp windows.cmdline

# Registry hives
python3 vol.py -f memory.dmp windows.registry.hivelist
```

---

## Disk Forensics with Autopsy

```bash
# Install Autopsy
sudo apt install autopsy

# Launch
autopsy
# Open browser: http://localhost:9999/autopsy

# Key analysis steps:
# 1. Create new case
# 2. Add disk image (.dd, .E01, .vmdk)
# 3. Run ingest modules:
#    - File Type Identification
#    - Hash Lookup (NSRL, known malware hashes)
#    - Keyword Search
#    - Recent Activity
#    - Email Parser
# 4. Review Timeline
# 5. Export findings
```

### Acquiring a Disk Image

```bash
# Create forensic image with dd
sudo dd if=/dev/sda of=/evidence/disk.dd bs=4M status=progress

# Verify integrity with hash
md5sum /evidence/disk.dd > disk.dd.md5
sha256sum /evidence/disk.dd > disk.dd.sha256

# Mount read-only for analysis
sudo mount -o ro,noexec /evidence/disk.dd /mnt/evidence
```

---

## Log Analysis & SIEM

### Important Log Locations

```bash
# Linux
/var/log/auth.log       # authentication events
/var/log/syslog         # system events
/var/log/kern.log       # kernel events
/var/log/nginx/         # web server logs
/var/log/apache2/       # apache logs

# Windows Event Log IDs
4624  — Successful login
4625  — Failed login
4648  — Explicit credential use (pass-the-hash indicator)
4688  — Process creation
4698  — Scheduled task created
4720  — User account created
7045  — Service installed (persistence indicator)
```

### Practical Log Analysis

```bash
# Find brute force attacks
grep "Failed password" /var/log/auth.log | \
  awk '{print $11}' | sort | uniq -c | sort -rn | head -20

# Detect web scanning (many 404s from one IP)
awk '$9 == 404 {print $1}' /var/log/nginx/access.log | \
  sort | uniq -c | sort -rn | head

# Find unusual outbound connections
netstat -an | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | \
  sort | uniq -c | sort -rn
```

---

## Indicators of Compromise (IOCs)

| Type | Examples |
|------|---------|
| File hashes | MD5/SHA256 of malware samples |
| IP addresses | C2 server IPs |
| Domain names | malicious-domain.com |
| URLs | http://evil.com/payload.exe |
| Registry keys | HKLM\Software\Malware |
| Mutex names | Unique malware mutex |
| File paths | C:\Windows\Temp\evil.exe |

```bash
# Check file hash against VirusTotal
# https://virustotal.com/gui/home/upload
sha256sum suspicious_file.exe

# Check IP reputation
# https://www.abuseipdb.com

# Yara rule matching
yara malware_rules.yar suspicious_file.exe
```

---

## Practice Questions

1. What is chain of custody and why does it matter in forensics?
2. How does Volatility's `malfind` plugin detect malware?
3. What Windows Event ID indicates a failed login?
4. What is the difference between volatile and non-volatile evidence?

---

## Next Module → [08 — Red vs Blue Team](../08-red-blue-team/README.md)

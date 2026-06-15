# Module 02 — Linux for Security

**Duration:** Week 3–4 | **Difficulty:** 🟢 Beginner | **Status:** ✅ Completed

---

## Learning Objectives

- Navigate the Linux filesystem and use essential CLI tools
- Write Bash scripts to automate security tasks
- Manage users, groups, permissions, and processes
- Analyze log files to detect suspicious activity

---

## Essential Commands

```bash
# Navigation
ls -la          # list files with permissions
pwd             # print working directory
cd /etc         # change directory
find / -name "*.conf" 2>/dev/null   # find files

# File operations
cat /etc/passwd         # view file
grep "root" /etc/passwd # search in file
tail -f /var/log/auth.log  # follow log in real time
less /var/log/syslog    # paginated view

# Permissions
chmod 755 script.sh     # rwxr-xr-x
chmod 600 private.key   # rw-------
chown root:root file    # change owner
ls -la /etc/shadow      # check shadow file permissions

# Processes
ps aux | grep nginx     # find process
kill -9 PID             # force kill
top / htop              # live process monitor
netstat -tulpn          # listening ports (install net-tools)
ss -tulpn               # modern alternative to netstat

# Users & Groups
id                      # current user info
whoami                  # username
cat /etc/passwd         # all users
sudo -l                 # what can I run as sudo?
last                    # login history
```

---

## Bash Scripting for Security

```bash
#!/bin/bash
# scan_users.sh — List users with login shells (potential accounts)

echo "[*] Users with login shells:"
grep -v "nologin\|false" /etc/passwd | cut -d: -f1,3,6,7

echo ""
echo "[*] Users with empty passwords:"
sudo awk -F: '($2 == "") {print $1}' /etc/shadow 2>/dev/null

echo ""
echo "[*] Recently modified files in /etc:"
find /etc -newer /etc/passwd -type f 2>/dev/null | head -20
```

---

## Log Analysis

```bash
# Failed SSH logins
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# Successful logins
grep "Accepted" /var/log/auth.log

# Web server access log
cat /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head

# Find large files (useful in forensics)
find / -size +100M -type f 2>/dev/null

# SUID binaries (privilege escalation vectors)
find / -perm -4000 -type f 2>/dev/null
```

---

## Practice Questions

1. What does `chmod 777` do and why is it dangerous?
2. How do you check what ports are listening on a Linux machine?
3. What is the difference between `/etc/passwd` and `/etc/shadow`?
4. How would you find all files modified in the last 24 hours?

---

## Next Module → [03 — Web Security](../03-web-security/README.md)

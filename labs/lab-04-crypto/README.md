# Lab 04 — Cryptography in Practice

**Module:** Cryptography & PKI | **Duration:** 2 hours | **Difficulty:** 🟡 Intermediate

---

## Objective

Implement and break cryptographic systems to understand their strengths and weaknesses.

---

## Task 1 — AES Encryption Lab

```bash
cd labs/lab-04-crypto
python3 solutions/aes_lab.py
```

```python
# aes_lab.py — complete this file
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# CHALLENGE 1: Encrypt the secret message using AES-256-CBC
secret_message = "The flag is FLAG{aes_m4st3r_0ps}"
key = get_random_bytes(32)  # 256-bit key

# TODO: Encrypt the message
# cipher = ???
# ciphertext = ???

# CHALLENGE 2: Decrypt the following (key is given)
known_key = bytes.fromhex("4f7c8a2b1e9d3f6c5a0b8e4d2c7f1a9b3e6d0c4f8a2b5e1d7c9f3a0b4e8c2d6")
known_iv  = bytes.fromhex("1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d")
known_ct  = bytes.fromhex("8f3a2c1e9b4d7f0a5c8e3b6d1f4a7c2e9b5d8f0a3c6e1b4d7f2a5c8e0b3d6f1a")

# TODO: Decrypt known_ct using known_key and known_iv
# cipher = ???
# plaintext = ???
# print(plaintext)
```

---

## Task 2 — Hash Cracking

```bash
# The following MD5 hashes are from a leaked database
# Crack them using the wordlist at /usr/share/wordlists/rockyou.txt

python3 ../../tools/hash_tool.py crack \
  5f4dcc3b5aa765d61d8327deb882cf99 \
  -a md5 \
  -w /usr/share/wordlists/rockyou.txt

# Hashes to crack:
# 5f4dcc3b5aa765d61d8327deb882cf99  → what is this password?
# 098f6bcd4621d373cade4e832627b4f6  → ?
# d8578edf8458ce06fbc5bb76a58c5ca4  → ?

# OR use hashcat (GPU accelerated):
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

**Reflection:** How long did it take to crack them? What does this tell you about MD5?

---

## Task 3 — RSA Math by Hand

```python
# rsa_manual.py — understand RSA from scratch with small numbers

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    return gcd, y1 - (b // a) * x1, x1

def mod_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    return x % phi

def rsa_keygen_small():
    # Small primes for demonstration ONLY
    p = 61
    q = 53
    n = p * q           # 3233
    phi = (p-1) * (q-1) # 3120
    e = 17              # public exponent (must be coprime with phi)
    d = mod_inverse(e, phi)  # private exponent
    
    print(f"p = {p}, q = {q}")
    print(f"n = {n} (public modulus)")
    print(f"phi(n) = {phi}")
    print(f"e = {e} (public exponent)")
    print(f"d = {d} (private exponent — KEEP SECRET)")
    print(f"\nPublic key:  (e={e}, n={n})")
    print(f"Private key: (d={d}, n={n})")
    
    # Encrypt message m=65
    m = 65
    c = pow(m, e, n)
    print(f"\nEncrypt m={m}: c = {m}^{e} mod {n} = {c}")
    
    # Decrypt
    m2 = pow(c, d, n)
    print(f"Decrypt c={c}: m = {c}^{d} mod {n} = {m2}")
    assert m == m2, "Decryption failed!"
    print("✓ Encryption/decryption successful!")
    return e, d, n

if __name__ == "__main__":
    rsa_keygen_small()
```

---

## Task 4 — TLS Certificate Analysis

```bash
# Examine the certificate of any HTTPS website
echo | openssl s_client -connect github.com:443 2>/dev/null | \
  openssl x509 -noout -text | head -60

# Check expiry
echo | openssl s_client -connect github.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# View full certificate chain
openssl s_client -connect github.com:443 -showcerts 2>/dev/null | \
  grep -E "(subject|issuer|notAfter)"

# Generate your own self-signed certificate
openssl req -x509 -newkey rsa:2048 -keyout my_key.pem \
            -out my_cert.pem -days 365 -nodes \
            -subj "/C=IN/ST=TN/L=Chennai/O=CyberShield/CN=localhost"

# View your certificate
openssl x509 -in my_cert.pem -text -noout
```

**Questions:**
1. Who issued GitHub's certificate?
2. When does it expire?
3. What cipher suite was negotiated in the TLS handshake?

---

## Task 5 — CTF Cryptography Challenge

Solve all 3 cipher challenges. Scripts are in `ctf/crypto/`.

```
Challenge A (20 pts):
Decode: aGVsbG8gY3liZXJzaGllbGQ=

Challenge B (30 pts):  
Decode: 68 65 6c 6c 6f 20 77 6f 72 6c 64

Challenge C (50 pts):
Decode: Khoor FlebhuVklhog (hint: Caesar)
```

---

## Solutions (complete after attempting)

```python
# solutions/lab04_solutions.py
import base64

# A: Base64
print(base64.b64decode("aGVsbG8gY3liZXJzaGllbGQ=").decode())

# B: Hex
print(bytes.fromhex("68 65 6c 6c 6f 20 77 6f 72 6c 64".replace(" ","")).decode())

# C: Caesar shift 3
cipher = "Khoor FlebhuVklhog"
print(''.join(chr((ord(c)-65-3)%26+65) if c.isupper()
              else chr((ord(c)-97-3)%26+97) if c.islower()
              else c for c in cipher))
```

---

## Lab Report

```
Lab 04 Report — Cryptography
Student: _______________
Date: _______________

1. AES encryption: did you successfully encrypt/decrypt? Y/N
2. Hash cracking: what were the plaintext passwords?
   5f4dcc3b... = _______________
   098f6bcd... = _______________
   d8578edf... = _______________
3. How long did hash cracking take? _______________
4. RSA: what was the private key d? _______________
5. GitHub cert: who issued it? Expiry date?
6. CTF answers:
   A: _______________
   B: _______________
   C: _______________
7. Key takeaway: what surprised you most in this lab?
```

---

## Next Lab → [Lab 05 — Metasploit](../lab-05-metasploit/README.md)

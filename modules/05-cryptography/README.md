# Module 05 — Cryptography & PKI

**Duration:** Week 8–9 | **Difficulty:** 🟡 Intermediate | **Status:** 🔄 In Progress

---

## Learning Objectives

- Understand symmetric vs asymmetric encryption
- Implement AES-256 and RSA in Python
- Explain how TLS/SSL works and identify certificate chain issues
- Perform basic cryptanalysis on weak ciphers
- Understand hashing and its role in security

---

## Symmetric Encryption

One key for both encryption and decryption.

### AES (Advanced Encryption Standard)

```python
# aes_demo.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def encrypt_aes(plaintext: str, key: bytes) -> str:
    """Encrypt plaintext using AES-256-CBC"""
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode()
    ct = base64.b64encode(ct_bytes).decode()
    return f"{iv}:{ct}"

def decrypt_aes(ciphertext: str, key: bytes) -> str:
    """Decrypt AES-256-CBC ciphertext"""
    iv_b64, ct_b64 = ciphertext.split(":")
    iv = base64.b64decode(iv_b64)
    ct = base64.b64decode(ct_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), AES.block_size).decode()

if __name__ == "__main__":
    key = get_random_bytes(32)  # 256-bit key
    message = "CyberShield secret message!"
    
    encrypted = encrypt_aes(message, key)
    print(f"Encrypted: {encrypted}")
    
    decrypted = decrypt_aes(encrypted, key)
    print(f"Decrypted: {decrypted}")
```

---

## Asymmetric Encryption

Two mathematically linked keys: public (share freely) + private (keep secret).

### RSA Implementation

```python
# rsa_demo.py
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_rsa_keypair(bits=2048):
    """Generate RSA key pair"""
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt(message: str, public_key: bytes) -> str:
    """Encrypt with recipient's public key"""
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted).decode()

def rsa_decrypt(ciphertext: str, private_key: bytes) -> str:
    """Decrypt with your private key"""
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    return decrypted.decode()

if __name__ == "__main__":
    print("Generating 2048-bit RSA key pair...")
    priv, pub = generate_rsa_keypair(2048)
    
    msg = "Hello from CyberShield!"
    enc = rsa_encrypt(msg, pub)
    print(f"Encrypted: {enc[:60]}...")
    
    dec = rsa_decrypt(enc, priv)
    print(f"Decrypted: {dec}")
```

---

## Hashing

One-way functions — you can't reverse them.

```python
# hashing_demo.py
import hashlib
import hmac
import secrets

def hash_password(password: str) -> tuple:
    """Properly hash a password with salt"""
    salt = secrets.token_hex(32)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100_000  # iterations
    )
    return salt, hashed.hex()

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify a password against stored hash"""
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        100_000
    )
    return hashed.hex() == stored_hash

# Common hashing algorithms
data = b"CyberShield"
print("MD5    :", hashlib.md5(data).hexdigest())       # BROKEN — don't use
print("SHA-1  :", hashlib.sha1(data).hexdigest())     # WEAK — don't use
print("SHA-256:", hashlib.sha256(data).hexdigest())   # GOOD
print("SHA-512:", hashlib.sha512(data).hexdigest())   # BETTER
```

---

## TLS/SSL Handshake

```
Client                              Server
  |                                   |
  |--- ClientHello (TLS 1.3) ------->|
  |    (supported ciphers, random)    |
  |                                   |
  |<-- ServerHello ------------------|
  |    (chosen cipher, certificate)   |
  |                                   |
  |--- Verify cert (CA chain) ------->|  ← this is PKI
  |                                   |
  |--- Key Exchange (ECDH) ---------->|
  |<-- Key Exchange ------------------|
  |                                   |
  |=== Encrypted Application Data ===|
```

**Check a certificate from CLI:**
```bash
# View certificate details
openssl s_client -connect google.com:443 -showcerts

# Check expiry date
echo | openssl s_client -connect google.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Generate self-signed cert
openssl req -x509 -newkey rsa:4096 -keyout key.pem \
            -out cert.pem -days 365 -nodes
```

---

## Classic Cipher Attacks (CTF)

```python
# caesar_crack.py
def caesar_decrypt(ciphertext: str, shift: int) -> str:
    result = ""
    for char in ciphertext:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                result += chr((shifted - ord('a')) % 26 + ord('a'))
            else:
                result += chr((shifted - ord('A')) % 26 + ord('A'))
        else:
            result += char
    return result

def brute_force_caesar(ciphertext: str):
    """Try all 26 shifts"""
    print("Brute forcing Caesar cipher...")
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        print(f"Shift {shift:2d}: {decrypted}")

# Frequency analysis
def frequency_analysis(ciphertext: str) -> dict:
    freq = {}
    for char in ciphertext.lower():
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
```

---

## Hands-On Exercises

1. **AES Lab** — Encrypt a secret message with AES-256, send the ciphertext to a teammate, have them decrypt it using the shared key
2. **RSA Lab** — Exchange public keys with a teammate and send encrypted messages back and forth
3. **Hash Cracking** — Use hashcat to crack MD5 hashes from the wordlist: `hashcat -m 0 hashes.txt rockyou.txt`
4. **Caesar CTF** — Solve the CTF challenge in `ctf/crypto/caesars-secret/`
5. **TLS Analysis** — Capture TLS handshake in Wireshark and identify each step

---

## Tools

```bash
# hashcat — password cracking
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt   # MD5
hashcat -m 1000 hash.txt rockyou.txt                      # NTLM
hashcat -m 1800 hash.txt rockyou.txt                      # sha512crypt

# john the ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt

# CyberChef (browser-based) — https://gchq.github.io/CyberChef/
# Excellent for CTF encoding/decoding challenges
```

---

## Practice Questions

1. Why is MD5 considered broken for password storage?
2. What is the difference between encryption and hashing?
3. How does a Certificate Authority (CA) establish trust?
4. What is a rainbow table attack and how does salting prevent it?
5. Why is RSA-512 considered insecure today?

---

## Next Module → [06 — Penetration Testing](../06-pentesting/README.md)

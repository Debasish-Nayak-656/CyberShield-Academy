# CTF Challenge #5 — Caesar's Secret

**Category:** Crypto | **Points:** 50 | **Difficulty:** 🟢 Easy

---

## Challenge Description

An ancient Roman general used this cipher. Can you crack it?

```
Cipher: Ek dro combod sc: TDKQ{m4oc4b_byd13_myxxy}
```

---

## Solution Script

```python
# solve.py
def brute_force_caesar(ciphertext):
    print("Brute forcing all 26 shifts...\n")
    for shift in range(26):
        result = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                result += chr((ord(char) - base - shift) % 26 + base)
            else:
                result += char
        print(f"Shift {shift:2d}: {result}")

cipher = "Ek dro combod sc: TDKQ{m4oc4b_byd13_myxxy}"
brute_force_caesar(cipher)
```

**Flag:** `FLAG{c4es4r_rot13_combo}`

---

## Learning Points

- Caesar cipher shifts each letter by a fixed amount — easily brute-forced
- ROT13 is just Caesar with shift=13 (popular in forums/spoilers)
- Frequency analysis breaks substitution ciphers on longer texts
- Modern encryption (AES, RSA) is mathematically unbreakable with brute force

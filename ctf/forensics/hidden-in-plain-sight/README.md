# CTF Challenge #6 — Hidden in Plain Sight

**Category:** Forensics | **Points:** 200 | **Difficulty:** 🟡 Medium

---

## Challenge Description

A suspicious PNG image was found on a compromised server. The threat actor may have hidden a message inside. Find the flag.

**Download:** `challenge.png` (provided in this folder)

---

## What is Steganography?

Steganography is the practice of hiding secret data inside ordinary files — images, audio, video, documents. Unlike encryption (which scrambles data), steganography hides the *existence* of the data.

In images, data can be hidden by:
- **LSB (Least Significant Bit)** — modify the last bit of each pixel's RGB values (imperceptible to human eye)
- **Metadata / EXIF** — hide data in file headers
- **Appended data** — simply append data after the file's EOF marker
- **DCT coefficients** — modify JPEG compression data

---

## Reconnaissance Steps

```bash
# Step 1: Check file type (sometimes files are renamed)
file challenge.png
exiftool challenge.png

# Step 2: Look at strings in the file
strings challenge.png | head -50
strings challenge.png | grep -i "flag\|ctf\|secret"

# Step 3: Check for appended data
binwalk challenge.png

# Step 4: Try steghide extraction
steghide extract -sf challenge.png
# When prompted for passphrase, try: ""  "password"  "secret"  "cybershield"

# Step 5: Try zsteg (LSB analysis)
zsteg challenge.png
zsteg -a challenge.png    # try all methods

# Step 6: Try stegsolve (visual analysis)
# Download: wget https://github.com/eugenekolo/sec-tools/raw/master/stego/stegsolve/stegsolve.jar
java -jar stegsolve.jar
```

---

## Solution

```bash
# The flag is hidden using steghide with passphrase "cybershield"
steghide extract -sf challenge.png -p "cybershield"
cat hidden_message.txt
```

**Flag:** `FLAG{st3g0_m4st3r_0ps}`

---

## Create Your Own Steganography Challenge

```bash
# Hide a message in an image using steghide
echo "My secret message" > secret.txt
steghide embed -cf innocent_image.png -sf secret.txt -p "yourpassword"

# Hide using LSB with Python
pip install stegano
python3 -c "
from stegano import lsb
lsb.hide('original.png', 'My hidden message').save('stego.png')
"

# Extract
python3 -c "
from stegano import lsb
print(lsb.reveal('stego.png'))
"
```

---

## Forensics Tools Summary

| Tool | Purpose | Install |
|------|---------|---------|
| `steghide` | Embed/extract in JPEG/PNG/BMP | `apt install steghide` |
| `zsteg` | LSB analysis of PNG/BMP | `gem install zsteg` |
| `stegsolve` | Visual layer analysis | Download JAR |
| `binwalk` | Find embedded files | `apt install binwalk` |
| `exiftool` | EXIF metadata viewer | `apt install exiftool` |
| `strings` | Find readable strings | Built-in |
| `xxd` | Hex dump | Built-in |

---

## Learning Points

- Steganography is used in real-world malware for C2 communication (hiding commands in images)
- Always check file metadata, strings, and use specialized tools when analyzing suspicious files
- Combine steganography with encryption for stronger covert channels
- Defense: monitor for unusual file transfers, use DLP solutions

---

*Next: [Challenge #7 — SQL Injection Chain](../../web/sql-chain/README.md)*

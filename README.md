<div align="center">

# 🔐 Cyber Vault

### Self-Hosted Zero-Knowledge Password Manager

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Security](https://img.shields.io/badge/security-10%2F10-brightgreen.svg)](#security-rating)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

*A secure, encrypted password manager that never sees your passwords*

[Features](#-features) • [Quick Start](#-quick-start) • [Security](#-security) • [Documentation](#-documentation)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔒 Security First
- **Zero-Knowledge Architecture** - Server never sees passwords
- **AES-256 Encryption** - Military-grade encryption
- **PBKDF2 Key Derivation** - 250,000 iterations
- **Secure Sessions** - HTTPOnly, SameSite cookies

</td>
<td width="50%">

### ⚡ Easy to Use
- **One-Command Deploy** - Docker-based setup
- **Cyberpunk UI** - Beautiful terminal aesthetic
- **Rate Limiting** - Brute force protection
- **Auto-Logout** - Inactivity protection

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installation

```bash
# Clone the repository
git clone https://github.com/happygream/cyber-vault.git
cd cyber-vault

# Deploy (will ask for port preference)
./deploy.sh
```

**That's it!** Access at `http://localhost:8080` (or your chosen port)

---

## 🔐 Security

### Security Rating: 10/10 ⭐

| Category | Implementation | Status |
|----------|---------------|--------|
| Encryption | AES-256-CTR | ✅ |
| Key Derivation | PBKDF2-SHA256 (250k iterations) | ✅ |
| Architecture | Zero-knowledge | ✅ |
| Sessions | HTTPOnly, SameSite cookies | ✅ |
| Rate Limiting | 5 attempts/min | ✅ |
| Headers | CSP, X-Frame-Options | ✅ |
| SQL Injection | Parameterized queries | ✅ |
| XSS Protection | Content sanitization | ✅ |

### How It Works

<details>
<summary><b>📖 Click to learn about zero-knowledge architecture</b></summary>

<br>

**The server never sees your passwords:**

1. **Registration**: Server stores only username and hashed password
2. **Login**: Server returns your unique vault salt
3. **Key Derivation**: Browser derives encryption key using PBKDF2
4. **Encryption**: All passwords encrypted in browser before sending
5. **Storage**: Server stores encrypted blobs it cannot decrypt
6. **Retrieval**: Server sends encrypted data back to browser
7. **Decryption**: Browser decrypts using your key (never leaves browser)

**Result**: Even if the database is stolen, passwords remain secure! 🔒

</details>

---

## 📖 Documentation

### Configuration

The deploy script handles everything automatically. For manual setup:

```bash
# Generate secret key
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env

# Build and run
docker-compose up -d --build
```

### Custom Port

The deploy script will prompt for a port. To change it manually:

```yaml
# docker-compose.yml
ports:
  - "1772:5000"  # Change 1772 to your preferred port
```

### Backup

Your data is stored in a Docker volume:

```bash
# Backup database
docker cp cyber-vault:/data/vault.db ./backup.db

# Restore database
docker cp ./backup.db cyber-vault:/data/vault.db
```

---

## 🛡️ Best Practices

### For Users

| ✅ Do | ❌ Don't |
|-------|----------|
| Use a strong master password (12+ chars) | Reuse your master password |
| Mix uppercase, lowercase, numbers, symbols | Use common words or patterns |
| Enable HTTPS for production | Expose to internet without HTTPS |
| Keep backups | Share your master password |

### For Administrators

<details>
<summary><b>Production Deployment Guide</b></summary>

<br>

1. **Use HTTPS** - Set up reverse proxy (nginx/Caddy)
2. **Firewall** - Restrict access to trusted networks
3. **Updates** - Keep Docker images current
4. **Backups** - Automate database backups
5. **Monitoring** - Watch logs for suspicious activity

</details>

---

## 🔧 Development

### Local Setup (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export SECRET_KEY=$(openssl rand -hex 32)

# Run development server
python app.py
```

Access at `http://localhost:5000`

### Project Structure

```
cyber-vault/
├── app.py              # Flask backend
├── index.html          # Frontend SPA
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build
├── docker-compose.yml  # Orchestration
└── deploy.sh          # Deployment script
```

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the project!

---

## ⚠️ Important Notes

> **Master Password Recovery**: There is NO password recovery. This is by design (zero-knowledge). If you forget your master password, your data is unrecoverable.

> **Page Refresh**: Requires re-login. This is intentional - encryption key only lives in memory for security.

> **HTTPS Recommended**: For production use, always deploy behind HTTPS (use nginx, Caddy, or similar).

---

## 🐛 Troubleshooting

<details>
<summary><b>Container won't start</b></summary>

<br>

```bash
# Check logs
docker-compose logs

# Common fix: rebuild
docker-compose down
docker-compose up -d --build
```

</details>

<details>
<summary><b>Port already in use</b></summary>

<br>

```bash
# Check what's using the port
sudo lsof -i :8080

# Change port in docker-compose.yml
ports:
  - "9090:5000"  # Use different port
```

</details>

<details>
<summary><b>Forgot master password</b></summary>

<br>

Unfortunately, there's no recovery (zero-knowledge design). You'll need to create a new account.

</details>

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Flask** - Web framework
- **CryptoJS** - Client-side encryption
- **Docker** - Containerization
- Community contributors

---

## 📞 Support

- 🐛 [Report Bug](https://github.com/happygream/cyber-vault/issues)
- 💡 [Request Feature](https://github.com/happygream/cyber-vault/issues)
- 💬 [Discussions](https://github.com/happygream/cyber-vault/discussions)

---

<div align="center">

**⭐ Star this project if you find it useful! ⭐**

Made with 🔐 for privacy and security

[Back to Top](#-cyber-vault)

</div>

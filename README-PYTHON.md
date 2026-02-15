# ⚡ Cyber Vault - Python Edition ⚡

A secure, self-hosted password manager built with Python Flask backend and SQLite database. Features a cyberpunk/hacker-themed interface with AES-256 encryption.

## 🚀 Features

- 🔐 **Strong Encryption** - AES-256 with PBKDF2 key derivation
- 🐍 **Python Backend** - Flask REST API with SQLite database
- 👥 **Multi-User Support** - Each user has their own encrypted vault
- 🔑 **Password Generator** - Create strong, random passwords
- 🎨 **Hacker Theme** - Cyberpunk/terminal aesthetic with neon effects
- 🐳 **Docker Ready** - One-command deployment with Docker Compose
- 💾 **Persistent Storage** - Data stored in Docker volume
- 🔒 **Secure by Design** - Client-side encryption, server-side storage

## 📦 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- That's it!

### Deployment (3 Commands)

```bash
# 1. Clone or download the files
cd cyber-vault

# 2. Start the container
docker-compose -f docker-compose-python.yml up -d

# 3. Access at http://localhost:8080
```

Done! Your password manager is now running.

## 📁 File Structure

```
cyber-vault/
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── Dockerfile.python           # Docker image definition
├── docker-compose-python.yml   # Docker Compose configuration
├── .env.example               # Environment variables template
├── templates/
│   └── index.html             # Frontend application
└── README-PYTHON.md           # This file
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Generate a secure secret key:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Add it to your `.env` file:

```
SECRET_KEY=your-generated-secret-key-here
```

### Changing Port

Edit `docker-compose-python.yml`:

```yaml
ports:
  - "3000:5000"  # Change 3000 to your desired port
```

Then restart:

```bash
docker-compose -f docker-compose-python.yml restart
```

## 🛠️ Managing the Application

### View Logs

```bash
docker-compose -f docker-compose-python.yml logs -f
```

### Stop Container

```bash
docker-compose -f docker-compose-python.yml down
```

### Restart Container

```bash
docker-compose -f docker-compose-python.yml restart
```

### Rebuild After Code Changes

```bash
docker-compose -f docker-compose-python.yml up -d --build
```

### Access Container Shell

```bash
docker exec -it cyber-vault-python sh
```

## 🔐 Security Features

### Encryption

- **Master Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Password Encryption**: Fernet (AES-128-CBC with HMAC)
- **Salting**: Unique salt per user
- **Client-Side Protection**: Additional encryption layer in browser

### Best Practices

1. **Use Strong Master Password**
   - Minimum 16 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Don't reuse from other services

2. **Keep Secret Key Secure**
   - Generate a random SECRET_KEY
   - Never commit .env file to version control
   - Change it if compromised

3. **Regular Backups**
   - Database is in Docker volume `vault-data`
   - Export volume regularly for backups

4. **Network Security**
   - Only expose on localhost by default
   - Use reverse proxy with SSL for remote access
   - Consider VPN for additional security

## 💾 Backup & Restore

### Backup Database

```bash
# Backup the vault data
docker run --rm -v cyber-vault-python_vault-data:/data -v $(pwd):/backup alpine tar czf /backup/vault-backup-$(date +%Y%m%d).tar.gz /data
```

### Restore Database

```bash
# Restore from backup
docker run --rm -v cyber-vault-python_vault-data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/vault-backup-YYYYMMDD.tar.gz --strip 1"
```

## 🌐 API Endpoints

The Flask backend provides a REST API:

### Authentication

- `POST /api/register` - Register new user
- `POST /api/login` - Authenticate user

### Password Management

- `GET /api/passwords` - Get all passwords
- `POST /api/passwords` - Create new password
- `GET /api/passwords/<id>` - Get specific password
- `PUT /api/passwords/<id>` - Update password
- `DELETE /api/passwords/<id>` - Delete password

### Health Check

- `GET /health` - Check API health

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8080
lsof -i :8080

# Change port in docker-compose-python.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose-python.yml logs

# Check container status
docker ps -a
```

### Database Issues

```bash
# Reset database (WARNING: Deletes all data)
docker-compose -f docker-compose-python.yml down -v
docker-compose -f docker-compose-python.yml up -d
```

### Permission Errors

```bash
# Fix volume permissions
docker-compose -f docker-compose-python.yml down
docker volume rm cyber-vault-python_vault-data
docker-compose -f docker-compose-python.yml up -d
```

## 🚀 Advanced Usage

### Running with Custom Database Location

```yaml
services:
  cyber-vault:
    volumes:
      - /path/to/your/data:/data
```

### Using with Reverse Proxy (Nginx)

```nginx
server {
    listen 443 ssl;
    server_name vault.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Development Mode

Edit `docker-compose-python.yml`:

```yaml
environment:
  - FLASK_ENV=development
```

This enables:
- Auto-reload on code changes
- Detailed error pages
- Debug logging

## 📊 Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Passwords Table

```sql
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    username TEXT,
    encrypted_password TEXT NOT NULL,
    url TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔮 Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Password strength analyzer
- [ ] Breach detection integration
- [ ] Export/import functionality
- [ ] Browser extension
- [ ] Mobile app
- [ ] Biometric authentication
- [ ] Secure password sharing

## ⚠️ Disclaimer

This password manager is provided as-is for self-hosting purposes. While it implements industry-standard encryption:

- Conduct your own security audit before production use
- Keep regular backups of your vault
- Use strong, unique master passwords
- Consider using established solutions like Bitwarden for critical enterprise use

## 📝 License

MIT License - Use freely, modify as needed.

## 🤝 Contributing

Feel free to fork and customize for your needs!

## 💡 Tips

1. **First Time Setup**
   - Create a strong master password
   - Write it down in a secure physical location
   - Never forget it - there's no recovery option

2. **Regular Maintenance**
   - Update passwords periodically
   - Remove unused entries
   - Backup your vault monthly

3. **Using the Generator**
   - Always use generated passwords for new accounts
   - Customize length and character types as needed
   - Copy directly from generator to avoid typos

4. **Search Feature**
   - Search by name, username, or URL
   - Case-insensitive matching
   - Real-time filtering

---

**Enjoy your cyberpunk password vault! Stay secure! ⚡🔐**

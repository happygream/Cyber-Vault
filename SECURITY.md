# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow responsible disclosure:

### Do NOT

- Create a public GitHub issue
- Discuss publicly before a fix is available
- Exploit the vulnerability

### Do

1. **Email**: Send details to [your-email@example.com]
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix**: Depends on severity
  - Critical: 1-3 days
  - High: 1 week
  - Medium: 2 weeks
  - Low: 1 month

### Disclosure Timeline

1. Vulnerability reported
2. Fix developed and tested
3. Update released
4. Public disclosure (coordinated with reporter)

## Security Best Practices

### For Users

1. **Strong Master Password**
   - Minimum 12 characters
   - Mix: uppercase, lowercase, numbers, symbols
   - Unique (never reused)

2. **HTTPS in Production**
   - Use reverse proxy (nginx, Caddy)
   - Valid SSL/TLS certificate

3. **Keep Updated**
   - Regular updates
   - Monitor security releases

4. **Secure Hosting**
   - Don't expose to public internet without HTTPS
   - Use firewall rules
   - Limit access to trusted networks

### For Administrators

1. **Environment Security**
   - Generate strong `SECRET_KEY`
   - Never commit `.env` file
   - Protect database file
   - Regular backups

2. **Network Security**
   - Use firewall
   - Disable unnecessary ports
   - Consider VPN for remote access

3. **Container Security**
   - Keep Docker updated
   - Use official base images
   - Scan for vulnerabilities

## Known Limitations

1. **HTTP on Local Network**
   - Web Crypto API not available
   - Falls back to CryptoJS
   - Still secure, but use HTTPS for production

2. **No Password Recovery**
   - Zero-knowledge = no password reset
   - This is by design for security

3. **Session Management**
   - Sessions expire on browser close
   - This is intentional for security

## Security Features

### Implemented

✅ AES-256 encryption  
✅ PBKDF2 (250,000 iterations)  
✅ Zero-knowledge architecture  
✅ Session cookies (HTTPOnly, SameSite)  
✅ Rate limiting  
✅ Security headers (CSP, X-Frame-Options)  
✅ SQL injection protection  
✅ XSS protection  

### Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Hardware key support (YubiKey)
- [ ] Encrypted database file
- [ ] Audit logging
- [ ] Account sharing (encrypted)

## Responsible Disclosure Hall of Fame

We recognize security researchers who help make Cyber Vault more secure:

<!-- List will be updated as vulnerabilities are reported and fixed -->

---

**Thank you for helping keep Cyber Vault secure!**

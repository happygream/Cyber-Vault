# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-15

### Added
- Zero-knowledge password manager
- AES-256 encryption with CryptoJS
- PBKDF2 key derivation (250,000 iterations)
- Flask session-based authentication
- Rate limiting (5 login attempts/min)
- Security headers (CSP, X-Frame-Options, etc.)
- Docker deployment with one-command setup
- Cyberpunk-themed UI
- Password generator
- Auto-logout on inactivity
- Session timeout display
- Audit logging capability
- Database auto-migration

### Security
- Client-side encryption (zero-knowledge)
- HTTPOnly, SameSite session cookies
- SQL injection protection
- XSS protection
- CSRF protection via SameSite cookies
- No CORS vulnerabilities

### Documentation
- Comprehensive README
- Security policy
- Contributing guidelines
- MIT License

## [Unreleased]

### Planned
- Two-factor authentication (2FA)
- Import/export functionality
- Browser extension
- Mobile app
- Encrypted database file
- Password sharing
- Hardware key support (YubiKey)

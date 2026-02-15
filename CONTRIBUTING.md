# Contributing to Cyber Vault

Thank you for considering contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment (OS, Docker version, etc.)
   - Logs (if applicable)

### Suggesting Features

1. Check if the feature has been requested
2. Explain the use case
3. Describe the proposed solution
4. Consider alternatives

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/happygream/cyber-vault.git
   cd cyber-vault
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes

5. Test thoroughly:
   ```bash
   # Deploy and test
   ./deploy.sh
   
   # Test all features:
   # - Registration
   # - Login
   # - Add password
   # - View password
   # - Edit password
   # - Delete password
   # - Logout
   ```

6. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description"
   ```

7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

8. Create a Pull Request

#### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions small and focused

**JavaScript (Frontend)**
- Use `const` and `let` (no `var`)
- Async/await for promises
- Clear variable names
- Add comments for complex logic

**HTML/CSS**
- Maintain cyberpunk aesthetic
- Keep UI responsive
- Test on different screen sizes

#### Commit Messages

Good commit messages:
```
✅ Add two-factor authentication support
✅ Fix session timeout not working
✅ Update README with HTTPS setup guide
✅ Refactor password encryption module
```

Bad commit messages:
```
❌ fix bug
❌ update stuff
❌ changes
❌ asdf
```

### Documentation

- Update README.md for new features
- Add inline code comments
- Update SECURITY.md for security changes

### Testing Checklist

Before submitting a PR, ensure:

- [ ] Code runs without errors
- [ ] All features still work
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No sensitive data in commits

## Security Contributions

For security-related contributions:

1. **Do NOT** create public issues for vulnerabilities
2. Follow the [Security Policy](SECURITY.md)
3. Email security concerns privately
4. Coordinate disclosure timeline

## Development Setup

### Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export SECRET_KEY=$(openssl rand -hex 32)

# Run
python app.py
```

### Docker Development

```bash
# Build
docker-compose build

# Run
docker-compose up

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

## Areas for Contribution

### High Priority

- [ ] Two-factor authentication (2FA)
- [ ] Import/export functionality
- [ ] Password strength meter improvements
- [ ] Mobile app (React Native?)
- [ ] Browser extension

### Medium Priority

- [ ] Encrypted backups
- [ ] Account sharing
- [ ] Password history
- [ ] Auto-fill suggestions
- [ ] Dark/light theme toggle

### Low Priority

- [ ] Additional UI themes
- [ ] Multi-language support
- [ ] Password generator improvements
- [ ] Audit log viewer

## Questions?

- 💬 Start a [Discussion](https://github.com/happygream/cyber-vault/discussions)
- 🐛 File an [Issue](https://github.com/happygream/cyber-vault/issues)

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Assume good intentions
- No harassment or discrimination
- Keep discussions professional

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Cyber Vault better!** 🔐

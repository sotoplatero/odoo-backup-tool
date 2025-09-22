# Contributing to Odoo Backup Tool

Thank you for your interest in contributing to the Odoo Backup Tool! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the issue template** if available
3. **Provide detailed information**:
   - Operating system and version
   - Python version
   - PostgreSQL version
   - Odoo version (if applicable)
   - Full error messages or logs
   - Steps to reproduce

### Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** for similar requests
2. **Describe the use case** and why it would be valuable
3. **Provide examples** of how the feature would work
4. **Consider implementation complexity** and backwards compatibility

### Pull Requests

#### Before You Start

1. **Fork the repository** and create a new branch
2. **Check the issue tracker** for existing work
3. **Discuss major changes** in an issue first

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/odoo-backup-tool.git
cd odoo-backup-tool

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt  # If available
```

#### Coding Standards

- **Python Style**: Follow [PEP 8](https://pep8.org/)
- **Line Length**: Max 88 characters (Black formatter default)
- **Imports**: Use [isort](https://pycqa.github.io/isort/) for import sorting
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Use Google-style docstrings

#### Code Quality Tools

We use several tools to maintain code quality:

```bash
# Code formatting
black odoo_backup/

# Import sorting
isort odoo_backup/

# Linting
flake8 odoo_backup/

# Type checking
mypy odoo_backup/
```

#### Testing

- **Write tests** for new features and bug fixes
- **Ensure all tests pass** before submitting
- **Test on multiple Python versions** (3.8+)
- **Test with different PostgreSQL versions** if relevant

```bash
# Run tests (when available)
pytest

# Run with coverage
pytest --cov=odoo_backup
```

#### Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Write or update tests** as needed

4. **Update documentation** if necessary

5. **Ensure all checks pass**:
   - Code formatting (black, isort)
   - Linting (flake8)
   - Type checking (mypy)
   - Tests (pytest)

6. **Commit with clear messages**:
   ```bash
   git commit -m "feat: add support for remote filestore backup"
   ```

7. **Push to your fork** and create a pull request

8. **Fill out the PR template** with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Breaking changes (if any)

#### Commit Message Format

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add support for compressed backup encryption
fix: handle missing filestore directory gracefully
docs: update installation instructions
style: format code with black
refactor: extract backup logic into separate module
test: add tests for database connection handling
chore: update dependencies
```

## 🔧 Development Guidelines

### Architecture

The project follows a simple, modular structure:

```
odoo_backup/
├── __init__.py     # Package initialization
├── cli.py          # Main CLI implementation
├── backup.py       # Core backup logic (future)
├── database.py     # Database operations (future)
└── utils.py        # Utility functions (future)
```

### Code Organization

- **Keep functions focused** and single-purpose
- **Use descriptive variable names** and function names
- **Add docstrings** to all public functions and classes
- **Handle errors gracefully** with user-friendly messages
- **Log important operations** for debugging

### Adding New Features

When adding new features:

1. **Consider backwards compatibility**
2. **Update CLI help text** and documentation
3. **Add configuration options** if needed
4. **Test edge cases** and error conditions
5. **Update the changelog**

### Dependencies

- **Minimize new dependencies** - justify each addition
- **Pin dependency versions** in pyproject.toml
- **Check for security vulnerabilities** in dependencies
- **Consider cross-platform compatibility**

## 📚 Documentation

### Updating Documentation

- **README.md**: Keep examples current and comprehensive
- **CHANGELOG.md**: Document all user-facing changes
- **Docstrings**: Document all public APIs
- **CLI help**: Ensure `--help` output is clear and complete

### Documentation Style

- **Use clear, simple language**
- **Provide practical examples**
- **Include troubleshooting information**
- **Keep formatting consistent**

## 🐛 Debugging

### Common Issues

- **PostgreSQL connection problems**: Check host, port, credentials
- **Missing pg_dump**: Ensure PostgreSQL client tools are installed
- **File permissions**: Verify access to filestore directories
- **Path issues**: Use absolute paths when possible

### Debug Mode

Add debug logging when needed:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security

### Security Considerations

- **Never log passwords** or sensitive information
- **Validate all user inputs**
- **Use parameterized queries** for database operations
- **Handle file paths securely** to prevent path traversal
- **Consider backup file permissions**

### Reporting Security Issues

For security-related issues, please email soto.platero@gmail.com directly instead of creating a public issue.

## 📝 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md` with release notes
3. Create release tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. GitHub Actions will automatically publish to PyPI

## 💬 Communication

### Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussion
- **Email**: soto.platero@gmail.com for direct contact

### Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming environment for all contributors.

## 🙏 Recognition

Contributors will be recognized in:

- **GitHub contributors list**
- **Release notes** for significant contributions
- **README.md** acknowledgments section

Thank you for contributing to the Odoo Backup Tool! 🚀
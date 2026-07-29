# Contributing to Blue Team Portal

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/blue-team-portal.git
   cd blue-team-portal
   ```
3. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Run migrations and seed data**:
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```
5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Branch Naming

Use descriptive branch names following this convention:

| Type | Format | Example |
|---|---|---|
| Feature | `feature/short-description` | `feature/add-export-csv` |
| Bug Fix | `fix/short-description` | `fix/serializer-field-mapping` |
| Documentation | `docs/short-description` | `docs/update-readme` |
| Tests | `test/short-description` | `test/add-api-coverage` |

## Coding Standards

- Follow **PEP 8** for Python code.
- Use **Django conventions** for views, models, and templates.
- Write **docstrings** for all public classes and functions.
- Keep imports organized: standard library → third-party → local.

## Testing Requirements

- All new features **must** include tests.
- Run the full test suite before submitting a PR:
  ```bash
  python manage.py test
  ```
- Ensure `python manage.py check` produces zero warnings.

## Pull Request Guidelines

1. Create a feature branch from `main`.
2. Make your changes with clear, atomic commits.
3. Write or update tests as needed.
4. Ensure all tests pass locally.
5. Open a Pull Request with a clear description of the changes.
6. Reference any related issues.

## Issue Reporting

When reporting a bug, please include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Python and Django versions
- Operating system

## Important Notes

- **Do NOT** modify the intended CTF vulnerability or challenge flag.
- **Do NOT** introduce additional security vulnerabilities.
- **Do NOT** commit secrets, API keys, or credentials.

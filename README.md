# 🛡️ Blue Team Portal — SOC CTF Challenge

[![Django CI](https://github.com/your-org/blue-team-portal/actions/workflows/django.yml/badge.svg)](https://github.com/your-org/blue-team-portal/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A realistic, investigation-driven **Capture The Flag** challenge built as a fully functional enterprise Security Operations Center (SOC) portal for the fictional company **Apex Global Solutions**.

Players must investigate incidents, examine audit trails, and discover a hidden legacy API left behind during an incomplete infrastructure migration — all to uncover a single Broken Access Control vulnerability.

---

## ✨ Features

- **Full SOC Dashboard** — Real-time metrics, incident analytics, and migration status tracking
- **Incident Management** — Complete CRUD with filtering, search, timeline tracking, and assignment
- **Asset Inventory** — Infrastructure tracking with criticality ratings and owner management
- **Investigation Reports** — Linked to incidents with draft/approval workflow
- **Notification Center** — Read/unread management with per-user isolation
- **Activity Logs** — Comprehensive audit trail with date, user, and action filtering
- **Role-Based Access Control** — Administrator, SOC Manager, SOC Analyst, Read Only Analyst
- **Secure REST API (v2)** — Full CRUD with OpenAPI/Swagger documentation
- **Hidden Legacy API (v1)** — Realistic abandoned infrastructure with investigation clues
- **CTF Challenge** — One intended vulnerability, one flag, one investigation path

---

## 🏗️ Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Django 6.0 |
| API | Django REST Framework, drf-spectacular |
| Frontend | Django Templates, Bootstrap 5, Chart.js |
| Database | SQLite (development), PostgreSQL-ready |
| Deployment | Docker, Docker Compose, Gunicorn |
| CI/CD | GitHub Actions |
| Testing | Django TestCase, 25+ automated tests |

---

## 📐 Architecture

For detailed architecture diagrams (system overview, database ERD, API structure, auth flow, and CTF attack path), see the [Architecture Documentation](docs/architecture.md).

```
blue-team-portal/
├── accounts/          # User profiles, auth, notifications
├── activity_logs/     # Audit trail
├── api/
│   ├── v1/            # Hidden Legacy API (CTF target)
│   └── v2/            # Secure Production API
├── assets/            # Infrastructure inventory
├── dashboard/         # SOC dashboard
├── incidents/         # Incident management
├── reports/           # Investigation reports
├── templates/         # Django HTML templates
├── static/            # CSS, JS, images
├── docs/              # Architecture diagrams
├── tests.py           # Comprehensive test suite
├── Dockerfile         # Container build
├── docker-compose.yml # Orchestration
└── manage.py          # Django CLI
```

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/your-org/blue-team-portal.git
cd blue-team-portal
docker-compose up -d --build
```

Navigate to `http://localhost:8000` — the database is automatically initialized and seeded.

### Local Development

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Demo Credentials

| Username | Role | Password |
|---|---|---|
| `mchen` | SOC Manager | `Password123!` |
| `jsmith` | Senior Analyst | `Password123!` |
| `tnguyen` | Junior Analyst | `Password123!` |

---

## 🧪 Running Tests

```bash
python manage.py test --verbosity=2
```

The test suite includes 25+ tests covering authentication, RBAC, CRUD operations, API endpoints, and challenge validation.

---

## 📖 API Documentation

The Secure API (v2) includes interactive Swagger documentation:

```
http://localhost:8000/api/v2/docs/
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` to customize:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | (insecure dev key) | Django secret key |
| `DEBUG` | `True` | Enable/disable debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,*` | Comma-separated allowed hosts |

---

## 🎯 Challenge Instructions

Flag format:
flag{...}

---

## 🔒 Security Disclaimer

> **⚠️ This application contains one intentional security vulnerability for educational purposes.** Do not deploy on a public-facing server without understanding the risks. See [SECURITY.md](SECURITY.md) for details.

---

## 📚 Learning Objectives

This project demonstrates proficiency in:

- **Django Full-Stack Development** — Models, Views, Templates, Forms, Signals, Context Processors
- **REST API Design** — DRF ViewSets, Serializers, Permissions, Filtering, Pagination
- **Security Engineering** — RBAC, CSRF protection, input validation, IDOR prevention
- **DevOps** — Docker containerization, CI/CD with GitHub Actions, environment configuration
- **CTF Design** — Narrative-driven challenges, realistic vulnerability implementation
- **Software Engineering** — Clean architecture, automated testing, comprehensive documentation

---

## 🔮 Future Improvements

- PostgreSQL production database support
- Redis caching for dashboard analytics
- WebSocket-based real-time notifications
- Expanded test coverage with API integration tests
- Kubernetes deployment manifests
- Additional CTF challenge layers

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

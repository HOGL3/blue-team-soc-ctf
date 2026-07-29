# Changelog

All notable changes to the Blue Team Portal CTF project are documented here.

## [1.0.0] — 2026-07-29

### 🚀 Initial Release

#### Blue Team Portal
- Full-featured SOC dashboard with real-time metrics and analytics
- Incident management with CRUD, filtering, search, and timeline tracking
- Asset inventory management with owner tracking and criticality ratings
- Investigation report system linked to incidents
- Notification center with read/unread management
- User profile management with image upload
- Activity log viewer with date, user, and action filtering
- Role-based access control (Administrator, SOC Manager, SOC Analyst, Read Only Analyst)
- Professional Bootstrap dark-theme UI

#### Secure Production API (v2)
- RESTful API using Django REST Framework
- Full CRUD for Incidents, Assets, Reports, Profiles, and Notifications
- Read-only Activity Logs endpoint
- Dashboard aggregation API
- Cross-entity Search API
- Public Health check endpoint
- OpenAPI 3.0 schema with Swagger UI (`/api/v2/docs/`)
- Comprehensive RBAC permission enforcement

#### Hidden Legacy API (v1)
- 13 legacy endpoints simulating abandoned infrastructure
- Historical data, migration records, and archived configurations
- Completely hidden from Swagger documentation and frontend UI

#### CTF Challenge
- Single intentional Broken Access Control vulnerability (OWASP A01:2021)
- Investigation-driven storyline with realistic SOC clues
- One challenge flag retrievable only through the intended attack path

#### Deployment
- Docker and Docker Compose support
- Automated setup via `entrypoint.sh` (migrate, collectstatic, seed)
- Environment variable configuration via `.env`
- Gunicorn production server

#### Documentation
- Comprehensive README with installation and deployment guides
- Architecture diagrams (Mermaid)
- Security policy (SECURITY.md)
- Contribution guide (CONTRIBUTING.md)
- GitHub Actions CI pipeline

#### Testing
- 25+ automated tests covering authentication, CRUD, APIs, and challenge validation
- Django system checks passing with zero issues

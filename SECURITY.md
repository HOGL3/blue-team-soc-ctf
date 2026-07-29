# Security Policy

## Purpose

The Blue Team Portal is an **educational Capture The Flag (CTF) challenge** designed for learning about web application security, SOC operations, and API security testing.

## Intentional Vulnerability

This project contains **exactly one intentional security vulnerability**:

- **Type**: Broken Access Control (OWASP Top 10 — A01:2021)
- **Location**: Hidden Legacy API (`/api/v1/`)
- **Scope**: A single endpoint within the Legacy API fails to enforce proper role-based authorization

This vulnerability is the core of the CTF challenge and exists by design.

## Security Scope

The following components are **intentionally secure** and should not contain vulnerabilities:

- Django Authentication System
- Secure Production API (`/api/v2/`)
- Web Portal (Dashboard, Incidents, Assets, Reports, Notifications, Profile, Activity Logs)
- Django Admin Panel
- CSRF Protection
- Session Management

## Reporting Unintended Vulnerabilities

If you discover an **unintended** security vulnerability (one that is NOT the designed CTF challenge), please report it responsibly:

1. **Do NOT** open a public GitHub issue.
2. Email the maintainer directly with details of the vulnerability.
3. Include steps to reproduce, potential impact, and suggested fix if possible.

## Educational Disclaimer

> **⚠️ WARNING**: This application is designed for **educational purposes only**. Do not deploy this application on a public-facing server without understanding the intentional vulnerability it contains. The maintainers are not responsible for any misuse of this software.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

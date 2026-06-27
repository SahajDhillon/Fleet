# Security

FleetIQ follows DevSecOps "shift-left" practices.

## Practices
- **Containers** run as a non-root user; images are minimal (`python:3.12-slim`).
- **Secrets** are never committed. Configure via environment variables / `.env`
  (see `.env.example`). In production, use your platform's secret manager
  (AWS Secrets Manager, Azure Key Vault, or Kubernetes Secrets).
- **Image scanning** with Trivy on every build.
- **Static analysis** with Bandit; **dependency CVE audits** with pip-audit.
- **Secret scanning** with gitleaks.
- All scans run automatically in CI (see the pipeline).

## Reporting a vulnerability
Please open a private security advisory or email the maintainers; do not file
a public issue for undisclosed vulnerabilities.
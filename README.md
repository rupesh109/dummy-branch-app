# **Branch Loan API - Production-Ready Microfinance Platform 🚀**
https://github.com/rupesh109/dummy-branch-app/actions
https://img.shields.io/badge/docker-ready-blue.svg
https://img.shields.io/badge/postgresql-16-blue.svg
https://img.shields.io/badge/python-3.11-blue.svg
A containerized microfinance API with full CI/CD automation, monitoring, and multi-environment support.
Built for Branch International’s DevOps internship assessment.

# **📋 Table of Contents**


1. Architecture Overview
2. Quick Start (5 Minutes)
3. Running Locally (Step-by-Step)
4. Environment Management
5. Environment Variables Reference
6. CI/CD Pipeline
7. API Endpoints
8. Monitoring & Observability
9. Troubleshooting
10. Design Decisions

# **🏗️ Architecture Overview**
Key Components:
| Component         | Technology       | Purpose                   | Port    |
| ----------------- | ---------------- | ------------------------- | ------- |
| **API**           | Flask + Gunicorn | REST API & Business Logic | 8000    |
| **Database**      | PostgreSQL 16    | Data Persistence          | 5432    |
| **Reverse Proxy** | Nginx            | SSL Termination & Routing | 80, 443 |
| **Monitoring**    | Prometheus       | Metrics Collection        | 9090    |
| **Visualization** | Grafana          | Dashboard & Alerts        | 3000    |

# **🚀 Quick Start:**

Prerequisites
• Docker 20.10+
• Docker Compose v2+
• OpenSSL
• 4GB+ RAM
• Linux/macOS or Windows WSL2

Instant Setup
### *1. git clone https://github.com/rupesh109/dummy-branch-app.git*
cd dummy-branch-app
### *2. Generate SSL certificates*
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/branchloans.key \
  -out certs/branchloans.crt \
  -subj "/C=IN/ST=Haryana/L=Gurugram/O=Branch/CN=branchloans.com"
### 3. Add domain to hosts
echo "127.0.0.1 branchloans.com" | sudo tee -a /etc/hosts
# 4. Copy environment file
cp .env.dev .env
# 5. Start all services
docker compose up -d --build
# 6. Initialize database
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed.py
# 7. Verify it's working
curl -k https://branchloans.com/health

# Expected Output:
{"status": "ok"}

# **Branch Loan API - Production-Ready Microfinance Platform 🚀**
[GitHub Actions Status](https://github.com/rupesh109/dummy-branch-app/actions)

![Docker Ready](https://img.shields.io/badge/docker-ready-blue.svg)
![PostgreSQL 16](https://img.shields.io/badge/postgresql-16-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)


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
### *3. Add domain to hosts*
echo "127.0.0.1 branchloans.com" | sudo tee -a /etc/hosts
### *4. Copy environment file*
cp .env.dev .env
### *5. Start all services*
docker compose up -d --build
### *6. Initialize database*
docker compose exec api alembic upgrade head
docker compose exec api python scripts/seed.py
### *7. Verify it's working*
curl -k https://branchloans.com/health

### *Expected Output:*
{"status": "ok"}

### *Access Points:*

API: https://branchloans.com
Prometheus: http://localhost:9090 (if monitoring enabled)
Grafana: http://localhost:3000 (if monitoring enabled)

# **📚 Running Locally (Step-by-Step)**
#### Step 1: Clone and Navigate
git clone https://github.com/rupesh109/dummy-branch-app.git
cd dummy-branch-app

#### Step 2: Generate SSL Certificates
### *Create certificates directory*
mkdir -p certs

### *Generate self-signed certificate (valid for 1 year)*
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/branchloans.key \
  -out certs/branchloans.crt \
  -subj "/C=IN/ST=Haryana/L=Gurugram/O=Branch/OU=DevOps/CN=branchloans.com" \
  -addext "subjectAltName=DNS:branchloans.com,DNS:*.branchloans.com"

#### Step 3: Configure Local DNS
 Add branchloans.com to /etc/hosts
echo "127.0.0.1 branchloans.com" | sudo tee -a /etc/hosts

 Verify it was added
cat /etc/hosts | grep branchloans

Output:
127.0.0.1 branchloans.com

#### Step 4: Set Up Environment ####
cp .env.dev .env
cat .env

#### Step 5: Start Services
docker compose up -d --build

watch docker compose ps

NAME              STATUS
loan-api-dev      Up (healthy)
loan-db-dev       Up (healthy)
loan-nginx-dev    Up (healthy)

#### Step 6: Initialize Database
docker compose exec api alembic upgrade head

docker compose exec api python scripts/seed.py

#### Step 7: Verify Everything Works
curl -k https://branchloans.com/health

curl -k https://branchloans.com/api/loans | jq .

curl -k https://branchloans.com/api/stats | jq .

curl -k https://branchloans.com/metrics

## ⚙️ **Environment Management**

The application supports three environments with different configurations optimized for their use case:

| **Environment** | **Use Case** | **Resource Limits** | **Features** |
|-----------------|-------------|---------------------|--------------|
| **Development** | Local coding & debugging | 0.5 CPU, 512MB RAM | Hot reload, debug logs, exposed ports |
| **Staging** | Pre-production testing | 1 CPU, 1GB RAM | Production-like behavior, standard logs, SSL |
| **Production** | Live deployment | 2 CPU, 2GB RAM | Optimized performance, structured logs, security hardened |

**Switching Between Environments**

Development Environment

Purpose: Local development with hot code reload and detailed debugging.

cp .env.dev .env
docker compose down
docker compose up -d --build


docker compose exec api env | grep ENV_NAME

**Features:**

✅ Hot Reload: Code changes reflect immediately

✅ Debug Logging: Verbose LOG_LEVEL=debug

✅ Exposed DB: Direct access on port 5432

✅ Minimal Resources: 0.5 CPU, 512MB RAM

✅ Fast Restart: No persistent data cleanup

**Staging Environment**
Purpose: Test production configuration before deploying to prod.

cp .env.staging .env
docker compose down
docker compose up -d --build

docker compose exec api env | grep ENV_NAME
 Output: ENV_NAME=staging

**Features:**

✅ Production-Like: Mimics prod settings

✅ Standard Logging: LOG_LEVEL=info

✅ No Hot Reload: Static code deployment

✅ Medium Resources: 1 CPU, 1GB RAM

✅ SSL Enabled: Full HTTPS setup

✅ Separate DB: Different credentials from dev

**Production Environment**
Purpose: Live deployment with maximum performance and security.

cp .env.prod .env

nano .env

docker compose down
docker compose up -d --build

docker compose exec api env | grep ENV_NAME
 Output: ENV_NAME=prod
 
**Features:**

✅ Optimized: Maximum performance settings

✅ Warning Logs Only: LOG_LEVEL=warning

✅ Structured Logging: JSON formatted logs

✅ Maximum Resources: 2 CPU, 2GB RAM

✅ Data Persistence: Guaranteed volume persistence

✅ Security Hardened: Non-root users, secure headers

✅ Separate Network: Isolated from other environments

# **📊 Environment Variables Reference**

#### Core Configuration

| Variable    | Description            | Dev           | Staging      | Prod         | Required |
| ----------- | ---------------------- | ------------- | ------------ | ------------ | -------- |
| `ENV_NAME`  | Environment identifier | `dev`         | `staging`    | `prod`       | ✅       |
| `FLASK_ENV` | Flask runtime mode     | `development` | `production` | `production` | ✅       |
| `LOG_LEVEL` | Logging verbosity      | `debug`       | `info`       | `warning`    | ✅       |


 **Test all three environments**
for env in dev staging prod; do
  echo "Testing $env environment..."
  cp .env.$env .env
  docker compose down -v
  docker compose up -d --build
  sleep 30
  docker compose exec api alembic upgrade head
  curl -k https://branchloans.com/health
  echo "✓ $env environment working"
done

 **Return to development**
cp .env.dev .env
docker compose up -d

#### Database Configuration
| Variable            | Description      | Dev           | Staging              | Prod                      | Required |
| ------------------- | ---------------- | ------------- | -------------------- | ------------------------- | -------- |
| `POSTGRES_USER`     | DB username      | `postgres`    | `branch`             | `branch_prod`             | ✅        |
| `POSTGRES_PASSWORD` | DB password      | `postgres`    | `staging-secret`     | **⚠ MUST CHANGE IN PROD** | ✅        |
| `POSTGRES_DB`       | Database name    | `microloans`  | `microloans_staging` | `microloans_prod`         | ✅        |
| `DB_PORT`           | External DB port | `5432`        | `5433`               | `5434`                    | ✅        |
| `DB_VOLUME`         | Volume name      | `db-data-dev` | `db-data-staging`    | `db-data-prod`            | ✅        |


# **🔄 CI/CD Pipeline*


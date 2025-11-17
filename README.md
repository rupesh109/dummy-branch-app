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


## **🔄 CI/CD Pipeline**

The project uses **GitHub Actions** to build, test, scan, and publish the Docker image to **GitHub Container Registry (GHCR)**.

---

### 🔔 Pipeline Triggers

The workflow runs automatically on:

- **Push** to:
  - `main`
  - `develop`
- **Pull Requests** targeting `main` or `develop`
- **Manual trigger** from the **Actions** tab

---

### 🧱 High-Level Flow

1. **Stage 1 – TEST**  
   ✅ Run tests and verify code quality

2. **Stage 2 – BUILD**  
   ✅ Build and tag the Docker image

3. **Stage 3 – SCAN**  
   ✅ Run security scan (Trivy) and fail on critical CVEs

4. **Stage 4 – PUSH**  
   ✅ Push the verified image to **GHCR**

> **Final Image:**  
> `ghcr.io/rupesh109/dummy-branch-app:latest`

---

### 🧪 Stage 1: TEST

**Purpose:** Verify code quality and functionality before building.

**Key Actions:**

- Checkout repository  
- Setup **Python 3.11** (with pip caching)  
- Install dependencies from `requirements.txt`  
- Start PostgreSQL service container  
- Run **Alembic migrations**  
- Execute **pytest** with coverage  
- Upload coverage report (e.g. to Codecov, if configured)

**Fails if:**

- Tests fail  
- Coverage threshold is not met  
- There are syntax/import errors  

**Typical duration:** ~2–3 minutes

---

### 🏗️ Stage 2: BUILD

**Purpose:** Build the Docker image with proper tagging and caching.

**Key Actions:**

- Setup **Docker Buildx** (multi-platform capable)  
- Extract metadata (branch, SHA, tags)  
- Build Docker image using the project `Dockerfile`  
- Tag image with:
  - `latest`
  - `main-<short-sha>`  
  - `develop` (for develop branch)  
  - `vX.Y.Z` (for release tags, if any)
- Cache image layers via GitHub Actions cache  
- Export the built image as an artifact for the next stage

**Fails if:**

- Dockerfile is invalid  
- Build step fails  
- Runner runs out of disk space  

**Typical duration:** ~3–5 minutes

---

### 🛡️ Stage 3: SCAN

**Purpose:** Catch vulnerabilities **before** the image is published.

**Key Actions:**

- Download the image artifact from the **Build** stage  
- Load the Docker image  
- Run **Trivy** vulnerability scanner  
- Generate **SARIF** report  
- Upload the report to GitHub → **Security → Code scanning alerts**  
- **Fail the pipeline if any CRITICAL CVEs are found**

**Coverage:**

- OS packages (Debian/Alpine)  
- Python dependencies (pip)  
- Known CVEs  
- Potential exposed secrets (depending on Trivy config)

**Fails if:**

- Trivy encounters critical vulnerabilities  
- Trivy itself errors out

**Typical duration:** ~1–2 minutes

---

### 📦 Stage 4: PUSH

**Purpose:** Publish the verified image to **GitHub Container Registry**.

**Key Actions:**

- Login to `ghcr.io` using `GITHUB_TOKEN`  
- Push all relevant tags, for example:
  - `ghcr.io/rupesh109/dummy-branch-app:latest`
  - `ghcr.io/rupesh109/dummy-branch-app:main-<short-sha>`
  - `ghcr.io/rupesh109/dummy-branch-app:develop`
- Update GitHub **Packages** metadata  
- Generate a short summary in the workflow output

**Runs only when:**

- Branch is `main` or `develop`  
- All previous stages have passed  
- The event is **not** just a PR from a fork (to avoid pushing untrusted images)

**Typical duration:** ~30–60 seconds

---

### ⚙️ Workflow Configuration

- **Workflow file:** `.github/workflows/ci-cd.yml`  
- **Core environment variables:**
  - `REGISTRY=ghcr.io`
  - `IMAGE_NAME=${{ github.repository }}`

- **Secrets used:**
  - `GITHUB_TOKEN` (provided automatically by GitHub)

> No extra secrets are needed for pushing to **GHCR**. Authentication is handled via `GITHUB_TOKEN`.

---

### 🚀 Using the Published Images

Once the pipeline completes successfully, you can use the built images locally or in any environment.

**Login to GHCR:**

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u rupesh109 --password-stdin


# **📡 API Endpoints**
**Base URL**

Local: https://branchloans.com
Docker Network: http://api:8000

**Authentication**
Current: No authentication required (prototype)
Production: Would require API keys or OAuth2

**Endpoints**
**1. Health Check**
Purpose: Verify service and database connectivity
GET /health

{
  "status": "ok",
  "db": "up",
  "timestamp": 1704638400.123
}

**Status Codes:**

200 OK - Service healthy
503 Service Unavailable - Database down

**2. List All Loans**
Purpose: Retrieve all loan records

GET /api/loans

[
  {
    "id": 1,
    "borrower_id": "usr_india_123",
    "amount": 5000.0,
    "currency": "INR",
    "term_months": 6,
    "interest_rate_apr": 24.0,
    "status": "approved",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "borrower_id": "usr_india_456",
    "amount": 12000.5,
    "currency": "INR",
    "term_months": 12,
    "interest_rate_apr": 22.0,
    "status": "pending",
    "created_at": "2024-01-16T14:20:00Z",
    "updated_at": "2024-01-16T14:20:00Z"
  }
]

**3. Get Loan by ID**
Purpose: Retrieve specific loan details

GET /api/loans/:id

Response:

{
  "id": 1,
  "borrower_id": "usr_india_123",
  "amount": 5000.0,
  "currency": "INR",
  "term_months": 6,
  "interest_rate_apr": 24.0,
  "status": "approved",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}

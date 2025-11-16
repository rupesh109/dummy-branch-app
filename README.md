## Running the Loan API locally

### 1. Prerequisites

- Docker & docker-compose
- Git
- OpenSSL (for local TLS)

### 2. Clone the repo

```bash
git clone https://github.com/rupesh109/dummy-branch-app.git
cd dummy-branch-app

###3. Generate local TLS certificates
mkdir certs
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout certs/branchloans.key \
  -out certs/branchloans.crt \
  -subj "/CN=branchloans.com"
###4. Map local domain

Edit /etc/hosts and add:

127.0.0.1   branchloans.com

###5. Start the dev environment
docker-compose --env-file .env.dev up -d --build
docker-compose --env-file .env.dev exec api alembic upgrade head
docker-compose --env-file .env.dev exec api python -m scripts.seed

###6. Test the API
curl -k https://branchloans.com/health
curl -k https://branchloans.com/api/loans



### Environments section (dev / staging / prod)

## Environments

This repo uses a single `docker-compose.yml` with three environment files:

- `.env.dev`
- `.env.staging`
- `.env.prod`

Each file configures:

- Database name & credentials
- Log level
- Resource limits
- Volume name for persistent data

Examples:

```bash
# Development
docker-compose --env-file .env.dev up -d --build

# Staging
docker-compose --env-file .env.staging up -d --build

# Production (local simulation)
docker-compose --env-file .env.prod up -d --build

##### CI/CD Pipeline

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and runs on GitHub Actions.

**Triggers**

- `push` to `main`
- `pull_request` targeting `main`

**Stages**

1. **Test**
   - Install Python dependencies from `requirements.txt`
   - Run tests with `pytest` (if a `tests/` directory exists)

2. **Build**
   - Build Docker image for the API using the repo `Dockerfile`
   - Tag image with `ghcr.io/rupesh109/dummy-branch-app:<git-sha>` and `<branch-name>`

3. **Security Scan**
   - Build a local image `local/loan-api:scan`
   - Scan the image with Trivy
   - Fail the pipeline on HIGH or CRITICAL vulnerabilities

4. **Push**
   - Only on `push` to `main` (not PRs)
   - Build & push image to GitHub Container Registry (`ghcr.io/rupesh109/dummy-branch-app:latest` and `:sha`)

**Secrets**

- `REGISTRY_USERNAME` – registry username
- `REGISTRY_PASSWORD` – access token/password with permission to push images

These are stored as GitHub Actions secrets and never committed to the repo.


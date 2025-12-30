# Cloud Computing Semester Project — CI/CD Pipeline (Beginner-Friendly)

This repo is a minimal **Student Management System REST API** (Flask + PostgreSQL) with a complete **CI/CD pipeline** using:
- GitHub Actions (CI/CD)
- Docker + Docker Compose
- Docker Hub (image registry)
- AWS EC2 Ubuntu (deployment host)

## 1) What you get
- `/health` endpoint for deployment verification
- `/students` GET and POST endpoints
- Unit test with pytest
- Docker image build + push to Docker Hub
- Automated deploy to EC2 with Docker Compose over SSH

---

## 2) Local run (quick test)
### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine + Compose (Linux)

### Run
```bash
docker compose up -d --build
curl http://localhost/health
```

Test API:
```bash
curl http://localhost/students
curl -X POST http://localhost/students -H "Content-Type: application/json" -d '{"name":"Alice"}'
curl http://localhost/students
```

Stop:
```bash
docker compose down
```

---

## 3) Cloud deployment (AWS EC2)
### A) Create an Ubuntu EC2 instance
Security Group inbound rules:
- SSH 22 (your IP only)
- HTTP 80 (0.0.0.0/0)

### B) Install Docker on EC2
```bash
sudo apt update -y
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

### C) Prepare deployment directory
```bash
sudo mkdir -p /opt/student-app
sudo chown -R $USER:$USER /opt/student-app
cd /opt/student-app
```

Copy `docker-compose.yml` from this repo to `/opt/student-app/` on EC2.

Create `.env` on EC2 (first time):
```bash
echo "DB_PASSWORD=postgres" > .env
echo "TAG=latest" >> .env
echo "DOCKER_IMAGE=yourdockerhubusername/student-app" >> .env
```

Run first time (optional):
```bash
docker compose up -d
curl http://localhost/health
```

---

## 4) GitHub Actions setup (CI/CD)
### A) Create Docker Hub repo
Create a Docker Hub repo, for example:
`yourdockerhubusername/student-app`

### B) Edit workflow image name
Update this in `.github/workflows/ci-cd.yml`:
```yaml
env:
  IMAGE_NAME: yourdockerhubusername/student-app
```

### C) Add GitHub secrets
Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Required:
- `DOCKERHUB_USERNAME` = your Docker Hub username
- `DOCKERHUB_TOKEN` = Docker Hub access token
- `EC2_HOST` = EC2 public IP/DNS
- `EC2_USER` = ubuntu
- `EC2_SSH_KEY` = private key content (PEM)
- `DB_PASSWORD` = database password (e.g., postgres)

### D) Push to main
Push code to `main` and check:
- GitHub Actions CI passes
- Docker image tags appear in Docker Hub (latest + SHA)
- EC2 deploy completes and `/health` returns ok

---

## 5) Rollback (if needed)
Because images are tagged with commit SHA, you can roll back on EC2:
```bash
cd /opt/student-app
echo "TAG=<previous_commit_sha>" > .env
echo "DB_PASSWORD=postgres" >> .env
echo "DOCKER_IMAGE=yourdockerhubusername/student-app" >> .env
docker compose pull
docker compose up -d
```

---

## 6) Files you should screenshot for your report
- GitHub repo structure
- GitHub Actions run (CI passing)
- Docker Hub tags (latest + SHA)
- EC2 terminal: `docker ps` / `docker compose ps`
- Browser or curl: `http://<EC2-IP>/health`

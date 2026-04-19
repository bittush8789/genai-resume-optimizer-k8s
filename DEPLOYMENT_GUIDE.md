# 🚀 Step-by-Step Deployment Guide: AI Resume Analyzer

This guide provides a comprehensive, command-by-command walkthrough to take the AI Resume Analyzer from your local machine to a full production environment.

---

## Phase 1: Local Setup & Testing

Before deploying, ensure the app runs flawlessly locally.

**1. Create and Activate Virtual Environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**2. Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**3. Configure Environment Variables**
```bash
# Copy the example env file
cp .env.example .env

# Open .env and add your GEMINI_API_KEY and generate a SECRET_KEY
# To generate a strong SECRET_KEY, run:
python -c "import secrets; print(secrets.token_hex(32))"
```

**4. Run Tests**
```bash
# Install testing dependencies if not already installed
pip install pytest pytest-cov

# Run the test suite
pytest tests/ -v
```

**5. Start the App Locally**
```bash
streamlit run app.py
# The app should now be accessible at http://localhost:8501
```

---

## Phase 2: Docker Containerization

Containerizing ensures the app runs identically in production as it does on your laptop.

**1. Build the Docker Image**
```bash
docker build -t resume-analyzer:latest .
```

**2. Run the Docker Container Locally (Testing)**
```bash
# This maps port 8501 and passes your local .env file
docker run -p 8501:8501 --env-file .env resume-analyzer:latest
```

**3. Test with Docker Compose (App + PostgreSQL)**
This mimics the production database setup.
```bash
# Start both the app and PostgreSQL database
docker-compose up -d --build

# View logs to ensure both started correctly
docker-compose logs -f

# To stop the containers
docker-compose down
```

---

## Phase 3: Push to GitHub & Configure CI/CD

Set up GitHub Actions to automate testing and image building.

**1. Initialize Git (if not done)**
```bash
git init
git add .
git commit -m "Initial commit for production deployment"
git branch -M main
git remote add origin https://github.com/your-username/resume-analyzer.git
git push -u origin main
```

**2. Configure GitHub Secrets**
Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

Add the following secrets:
- `GEMINI_API_KEY`: Your Google AI API key
- `SECRET_KEY`: Your generated session secret
- `DATABASE_URL`: `sqlite:///./test_resume_analyzer.db` (for CI testing)
- `DOCKERHUB_USERNAME`: Your DockerHub username
- `DOCKERHUB_TOKEN`: Generate this in DockerHub (Account Settings -> Security -> New Access Token)
- `KUBECONFIG_BASE64`: (We will generate this in Phase 4)
- `POSTGRES_PASSWORD`: A strong password for your production database

*Note: Once these secrets are added, every push to `main` will trigger the tests and build the Docker image automatically.*

---

## Phase 4: Kubernetes Deployment (Production)

Deploying to a K8s cluster (like AWS EKS, Google GKE, or a local Minikube).

**1. Connect to your Cluster**
Ensure your `kubectl` is connected to your cluster.
```bash
# Verify connection
kubectl cluster-info
kubectl get nodes
```

**2. Generate KUBECONFIG_BASE64 for GitHub Actions**
```bash
# Run this locally to get the base64 encoded config
cat ~/.kube/config | base64

# Copy the entire output and add it as the `KUBECONFIG_BASE64` secret in GitHub.
# (If on macOS/Linux, use `cat ~/.kube/config | base64 | tr -d '\n'`)
```

**3. Apply Kubernetes Manifests Manually (Optional Initial Setup)**
While GitHub Actions handles this, doing it manually the first time helps verify the configuration.

```bash
# Create the namespace
kubectl apply -f k8s/namespace.yaml

# Create the secrets (IMPORTANT: Edit k8s/secret.yaml to include your REAL base64 encoded keys first, or use the command below)
kubectl create secret generic resume-analyzer-secrets \
  --from-literal=GEMINI_API_KEY="your_actual_api_key_here" \
  --from-literal=SECRET_KEY="your_actual_secret_key_here" \
  --from-literal=DATABASE_URL="postgresql://resumeuser:YOUR_SECURE_PASSWORD@postgres-service:5432/resume_analyzer" \
  --from-literal=POSTGRES_PASSWORD="YOUR_SECURE_PASSWORD" \
  -n resume-analyzer

# Deploy the PostgreSQL Database
kubectl apply -f k8s/postgres.yaml

# Wait for DB to be ready
kubectl get pods -n resume-analyzer -w

# Deploy the Application
kubectl apply -f k8s/deployment.yaml

# Deploy Networking (Service & Ingress)
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Deploy Autoscaler
kubectl apply -f k8s/hpa.yaml
```

**4. Monitor the Deployment**
```bash
# Check Pods
kubectl get pods -n resume-analyzer

# Check Services
kubectl get svc -n resume-analyzer

# Check Ingress (Wait for an IP address to be assigned)
kubectl get ingress -n resume-analyzer

# View App Logs
kubectl logs -f deployment/resume-analyzer -n resume-analyzer
```

---

## Phase 5: Domain & SSL Setup (Final Polish)

If using the NGINX ingress controller on a public cloud:

**1. Point your Domain**
Get the external IP of your Ingress Controller:
```bash
kubectl get ingress -n resume-analyzer
```
*Create an `A Record` in your DNS provider pointing `resume-analyzer.yourdomain.com` to this IP.*

**2. Update `k8s/ingress.yaml`**
Change `resume-analyzer.yourdomain.com` to your actual domain name.

**3. Setup SSL with Cert-Manager (Optional but Recommended)**
If you have cert-manager installed, uncomment the TLS sections in `k8s/ingress.yaml` and apply:
```bash
kubectl apply -f k8s/ingress.yaml
```

---

## Common Maintenance Commands

**Scale the application manually:**
```bash
kubectl scale deployment resume-analyzer --replicas=3 -n resume-analyzer
```

**Restart the application pods:**
```bash
kubectl rollout restart deployment resume-analyzer -n resume-analyzer
```

**Access the PostgreSQL database directly:**
```bash
kubectl exec -it statefulset/postgres -n resume-analyzer -- psql -U resumeuser -d resume_analyzer
```

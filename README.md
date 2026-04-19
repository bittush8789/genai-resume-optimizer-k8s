# 🤖 AI Resume Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![Google Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google)
![LangChain](https://img.shields.io/badge/LangChain-1.x-green?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-K8s-326CE5?style=for-the-badge&logo=kubernetes)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions)

**An AI-powered resume analysis SaaS platform that helps job seekers optimize their resumes, improve ATS scores, generate cover letters, and prepare for interviews — powered by Google Gemini.**

[Live Demo](#) · [Report Bug](https://github.com/your-username/resume-analyzer/issues) · [Request Feature](https://github.com/your-username/resume-analyzer/issues)

</div>

---

## 📸 Screenshots

> *(Add screenshots of your running app here)*

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     NGINX INGRESS (K8s)                              │
│                  resume-analyzer.yourdomain.com                      │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│              KUBERNETES CLUSTER (resume-analyzer namespace)          │
│                                                                      │
│  ┌─────────────────────────────────────────────────┐                │
│  │         Streamlit App (Deployment)               │                │
│  │  ┌──────────────┐   ┌──────────────┐            │                │
│  │  │   Pod 1      │   │   Pod 2      │  ← HPA     │                │
│  │  │  (replica)   │   │  (replica)   │  (2-10)    │                │
│  │  └──────┬───────┘   └──────┬───────┘            │                │
│  │         └──────────┬───────┘                     │                │
│  └──────────────────  │ ──────────────────────────── │                │
│                        │                             │                │
│           ┌────────────┼──────────────┐             │                │
│           ▼            ▼              ▼             │                │
│  ┌──────────────┐  ┌────────┐  ┌──────────────┐   │                │
│  │ PostgreSQL   │  │Gemini  │  │  K8s Secret  │   │                │
│  │ StatefulSet  │  │  API   │  │  (API Keys)  │   │                │
│  │  + PVC 5Gi  │  │(Google)│  └──────────────┘   │                │
│  └──────────────┘  └────────┘                     │                │
│                                                    │                │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 CI/CD Pipeline Architecture

```
 Developer
    │
    │  git push main
    ▼
┌──────────────────────────────────────────────────────┐
│              GitHub Actions Pipeline                  │
│                                                       │
│  ┌──────────────┐   ┌───────────────┐   ┌─────────┐ │
│  │  JOB 1       │   │  JOB 2        │   │  JOB 3  │ │
│  │  🧪 Test     │──▶│  🐳 Build     │──▶│  🚀 Deploy│ │
│  │              │   │  & Push Image │   │  to K8s │ │
│  │ • flake8     │   │               │   │         │ │
│  │ • pytest     │   │ Docker Hub    │   │ kubectl │ │
│  │ • coverage   │   │ (sha tag)     │   │ rollout │ │
│  └──────────────┘   └───────────────┘   └─────────┘ │
└──────────────────────────────────────────────────────┘
```

## 🧩 Application Architecture (Internal)

```
resume-analyzer/
│
├── app.py                  ← Streamlit UI (router + pages)
│   ├── render_landing_page()
│   ├── render_home()
│   ├── render_analyzer()   ← ATS analysis core
│   ├── render_tools()      ← Cover Letter, Interview Prep, Rewrite
│   └── render_history()    ← User history from DB
│
├── auth.py                 ← Authentication (PBKDF2 hashing)
├── database.py             ← SQLAlchemy ORM models + session
│
├── utils/
│   ├── ai_chains.py        ← LangChain LCEL chains (Gemini)
│   └── parser.py           ← PDF/DOCX resume text extraction
│
├── k8s/                    ← Kubernetes manifests
├── tests/                  ← Pytest test suite
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/      ← GitHub Actions CI/CD
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Upload** | Upload PDF or DOCX resumes |
| 🎯 **ATS Scoring** | AI-powered ATS compatibility score (0-100) |
| 🔍 **Keyword Analysis** | Identify missing keywords vs job description |
| 💡 **Smart Suggestions** | Actionable improvement recommendations |
| ✍️ **Bullet Rewriter** | Rewrite weak resume bullets with AI |
| 📝 **Cover Letter** | Generate tailored cover letters instantly |
| 🎙️ **Interview Prep** | Role-specific interview Q&A generation |
| 🕒 **History** | Track all past resume analyses |
| 🔐 **Auth** | Secure signup/login with session management |

---

## 🛠️ Tech Stack

### Application
| Layer | Technology |
|---|---|
| **Frontend/Backend** | Streamlit |
| **AI/LLM** | Google Gemini (via LangChain LCEL) |
| **LLM Orchestration** | LangChain Core 1.x |
| **Database ORM** | SQLAlchemy |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Auth** | PBKDF2-SHA256 (passlib) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **DOCX Parsing** | python-docx |

### DevOps
| Tool | Purpose |
|---|---|
| **Docker** | Containerization |
| **Kubernetes** | Orchestration & scaling |
| **GitHub Actions** | CI/CD pipeline |
| **NGINX Ingress** | Traffic routing |
| **HPA** | Auto-scaling (2-10 pods) |
| **PostgreSQL StatefulSet** | Production database |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A Google Gemini API Key → [Get one here](https://aistudio.google.com/app/apikey)

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Create your .env file
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///./resume_analyzer.db
SECRET_KEY=your-random-secret-key-here
```

### 3. Run the App
```bash
streamlit run app.py
```
Visit → **http://localhost:8501**

---

## 🐳 Docker Deployment

### Run with Docker
```bash
# Build the image
docker build -t resume-analyzer .

# Run the container
docker run -p 8501:8501 --env-file .env resume-analyzer
```

### Run with Docker Compose (with PostgreSQL)
```bash
docker-compose up --build
```

---

## ☸️ Kubernetes Deployment

### Prerequisites
- A running Kubernetes cluster (EKS, GKE, AKS, or Minikube)
- `kubectl` configured
- Docker image pushed to a registry

### Step-by-Step Deploy

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Create secrets (replace with real values)
kubectl create secret generic resume-analyzer-secrets \
  --from-literal=GEMINI_API_KEY="your_key" \
  --from-literal=SECRET_KEY="your_secret" \
  --from-literal=DATABASE_URL="postgresql://resumeuser:password@postgres-service:5432/resume_analyzer" \
  --from-literal=POSTGRES_PASSWORD="your_db_password" \
  -n resume-analyzer

# 3. Deploy PostgreSQL
kubectl apply -f k8s/postgres.yaml

# 4. Deploy the application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# 5. Check status
kubectl get pods -n resume-analyzer
kubectl rollout status deployment/resume-analyzer -n resume-analyzer
```

### Verify Deployment
```bash
kubectl get all -n resume-analyzer
```

---

## 🔄 CI/CD Setup (GitHub Actions)

Add these secrets to your GitHub repository (`Settings → Secrets → Actions`):

| Secret | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `SECRET_KEY` | App session secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `KUBECONFIG_BASE64` | Base64-encoded kubeconfig (`cat ~/.kube/config \| base64`) |

On every `git push` to `main`:
1. ✅ Tests run automatically
2. 🐳 Docker image is built & pushed
3. ☸️ Kubernetes rolling update is triggered

---

## 🧪 Running Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=. --cov-report=html
```

---

## 📁 Project Structure

```
resume-analyzer/
├── 📄 app.py                  # Main Streamlit application
├── 🔐 auth.py                 # User authentication
├── 🗄️  database.py             # DB models & session
├── 📋 requirements.txt        # Python dependencies
├── 🐳 Dockerfile              # Container definition
├── 🐳 docker-compose.yml      # Local dev with PostgreSQL
├── 🚫 .dockerignore           # Docker build exclusions
├── 🚫 .gitignore              # Git exclusions
├── 🚂 railway.toml            # Railway deployment config
│
├── utils/
│   ├── 🤖 ai_chains.py        # LangChain + Gemini chains
│   └── 📑 parser.py           # Resume file parser
│
├── k8s/                       # Kubernetes manifests
│   ├── namespace.yaml
│   ├── secret.yaml
│   ├── deployment.yaml        # App pods (2 replicas)
│   ├── service.yaml           # ClusterIP service
│   ├── ingress.yaml           # NGINX ingress + TLS
│   ├── hpa.yaml               # Auto-scaling (2-10 pods)
│   └── postgres.yaml          # PostgreSQL StatefulSet
│
├── tests/
│   ├── conftest.py            # Test configuration
│   ├── test_auth.py           # Auth unit tests
│   ├── test_database.py       # DB integration tests
│   └── test_parser.py         # Parser unit tests
│
├── .streamlit/
│   └── config.toml            # Streamlit theme config
│
└── .github/
    └── workflows/
        └── deploy.yml         # GitHub Actions CI/CD
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `DATABASE_URL` | ✅ | SQLAlchemy DB connection string |
| `SECRET_KEY` | ✅ | Session secret key |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Bittu Sharma**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)

---

<div align="center">

⭐ **Star this repo if it helped you!** ⭐

*Built with ❤️ using Python, Streamlit, Google Gemini & LangChain*

</div>

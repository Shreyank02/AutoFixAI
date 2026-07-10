# 🚀 AutoFix AI — Autonomous GitHub Issue Resolver

> An AI-powered software engineer that automatically analyzes GitHub issues, understands the repository, generates a code fix, commits the changes to a new branch, and creates a Pull Request for human review.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-orange)
![Qdrant](https://img.shields.io/badge/Qdrant-VectorDB-red)
![GitHub App](https://img.shields.io/badge/GitHub-App-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

# 📖 Overview

AutoFix AI is an autonomous AI Software Engineer built as a GitHub App.

Whenever an issue is opened in a connected GitHub repository, AutoFix AI automatically:

- Receives the GitHub webhook
- Clones the repository
- Understands the project structure
- Retrieves the most relevant source code using semantic search
- Uses multiple AI agents to analyze the issue and generate a fix
- Applies the patch safely
- Creates a new Git branch
- Commits the generated changes
- Pushes the branch
- Opens a Pull Request for developer review

The developer only needs to review and merge the PR.

---

# ✨ Features

- GitHub App Integration
- Automatic Issue Detection
- Repository Cloning
- Repository Scanner
- Semantic Code Search using Qdrant
- AI-powered Repository Analysis
- Multi-Agent Workflow using LangGraph
- Automatic Patch Generation
- Safe Patch Application
- Automatic Git Commit
- Automatic Branch Creation
- Automatic Push to GitHub
- Automatic Pull Request Creation
- Human-in-the-loop Approval

---

# 🏗️ Architecture

```
GitHub Issue
      │
      ▼
GitHub Webhook
      │
      ▼
FastAPI Backend
      │
      ▼
Supabase Job Queue
      │
      ▼
Worker
      │
      ▼
Clone Repository
      │
      ▼
Repository Scanner
      │
      ▼
Qdrant Retriever
      │
      ▼
Analyzer Agent
      │
      ▼
Developer Agent
      │
      ▼
Patch Service
      │
      ▼
Git Service
      │
      ▼
Push Branch
      │
      ▼
Create Pull Request
```

---

# 🤖 AI Workflow

## 1. Repository Scanner

Scans the cloned repository and extracts

- Functions
- Classes
- Imports
- Dependencies
- Framework
- Language
- Symbols

---

## 2. Repository Retriever

Uses embeddings stored in **Qdrant** to retrieve the most relevant code snippets related to the GitHub issue.

---

## 3. Analyzer Agent

Responsibilities

- Understand the GitHub issue
- Identify root cause
- Determine affected files
- Generate implementation plan
- Produce structured JSON output

---

## 4. Developer Agent

Responsibilities

- Read implementation plan
- Generate exact code patch
- Produce structured patch JSON

---

## 5. Patch Service

Safely applies generated code changes.

Includes rollback support if patching fails.

---

## 6. Git Service

Handles

- Branch creation
- Git commit
- Push to GitHub

---

## 7. GitHub API Service

Automatically creates a Pull Request using GitHub REST API.

---

# 🛠 Tech Stack

### Backend

- Python
- FastAPI

### AI

- LangGraph
- LangChain
- OpenRouter
- NVIDIA Nemotron 120B

### Vector Database

- Qdrant

### Queue

- Supabase

### Git

- GitPython

### Deployment

- Render

### Version Control

- GitHub App
- GitHub Webhooks

---

# 📂 Project Structure

```
AutoFixAI/
│
├── agents/
│   ├── analyzer.py
│   ├── developer.py
│   ├── supervisor.py
│   ├── workflow.py
│   └── schemas.py
│
├── api/
│   └── webhook.py
│
├── app_rag/
│   ├── scanner.py
│   ├── embeddings.py
│   ├── indexer.py
│   └── retriever.py
│
├── core/
│   ├── config.py
│   └── security.py
│
├── prompts/
│   ├── analyzer.txt
│   ├── developer.txt
│   └── supervisor.txt
│
├── services/
│   ├── auth_service.py
│   ├── github_service.py
│   ├── github_api_service.py
│   ├── git_service.py
│   ├── job_service.py
│   ├── patch_service.py
│   ├── repository_service.py
│   └── installation_service.py
│
├── utils/
│
├── worker.py
├── main.py
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/AutoFixAI.git

cd AutoFixAI
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file

```env
APP_NAME=AutoFixAI

HOST=0.0.0.0
PORT=8000

GITHUB_APP_ID=

GITHUB_PRIVATE_KEY=

GITHUB_WEBHOOK_SECRET=

OPENROUTER_API_KEY=

OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b-20230311:free

QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=

SUPABASE_URL=
SUPABASE_KEY=
```

---

## 5. Create GitHub App

Create a GitHub App and configure

- Webhook URL

```
https://your-domain.com/webhooks/github
```

Permissions

- Issues (Read)
- Pull Requests (Write)
- Contents (Read & Write)
- Metadata (Read)

Events

- Issues
- Installation
- Installation Repositories

Download the private key and update

```
GITHUB_PRIVATE_KEY
```

---

## 6. Start FastAPI Server

```bash
uvicorn main:app --reload
```

---

## 7. Start Worker

```bash
python worker.py
```

---

# 🔄 Workflow

```
User opens GitHub Issue
          │
          ▼
Webhook Received
          │
          ▼
Issue added to Queue
          │
          ▼
Worker starts processing
          │
          ▼
Repository cloned
          │
          ▼
Repository scanned
          │
          ▼
Relevant code retrieved
          │
          ▼
Analyzer Agent
          │
          ▼
Developer Agent
          │
          ▼
Patch Applied
          │
          ▼
Branch Created
          │
          ▼
Commit Created
          │
          ▼
Push Branch
          │
          ▼
Create Pull Request
          │
          ▼
Developer Reviews PR
```

---

# 🧠 AI Agents

| Agent | Responsibility |
|---------|----------------|
| Analyzer | Understand issue and generate implementation plan |
| Developer | Generate code patch |
| Supervisor | Validate workflow state and coordinate execution |

---

# 📌 Current Capabilities

✅ GitHub App Integration

✅ GitHub Webhooks

✅ Repository Cloning

✅ Repository Scanner

✅ Semantic Code Retrieval

✅ AI Issue Analysis

✅ AI Code Generation

✅ Patch Application

✅ Git Automation

✅ Automatic Pull Request Creation

---

# 🚀 Future Improvements

- Automatic Test Execution
- AI Code Reviewer
- Docker Support
- Parallel Repository Indexing
- Incremental Repository Updates
- Multi-language Support
- Automatic PR Review Comments
- CI/CD Integration
- Slack & Discord Notifications
- Web Dashboard
- Repository Memory Cache

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Shreyank Choudhary**

AI Engineer | Machine Learning | Generative AI | Autonomous Systems

If you found this project useful, consider giving it a ⭐ on GitHub!

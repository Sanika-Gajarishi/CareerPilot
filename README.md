# 🚀 CareerPilot AI

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge" />
<img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge" />
<img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge" />
<img src="https://img.shields.io/badge/JWT-Authentication-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

</p>

<p align="center">

### An AI-Powered Career Development Platform

**Resume Analysis • ATS Optimization • Job Matching • Mock Interviews • Career Roadmaps • Application Tracking**

</p>

---

# 📖 Overview

CareerPilot AI is a AI-powered career assistant designed to help students and job seekers prepare for their dream careers.

Instead of using multiple platforms for resume optimization, ATS checking, interview preparation, job matching, and career planning, CareerPilot AI brings everything together into one intelligent platform.

The project uses **FastAPI** for the backend, **Streamlit** for the frontend, **PostgreSQL** for data storage, and modular AI agents for each career-related feature.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login
- JWT Authentication
- Protected APIs
- User Profile Management

---

## 📄 Resume Management

- Upload Resume (PDF)
- Resume Parsing
- Contact Information Extraction
- Education Extraction
- Skills Extraction
- Projects Extraction
- Resume History

---

## 🤖 ATS Resume Analyzer

Analyze resumes like modern Applicant Tracking Systems.

### Includes

- ATS Score
- Resume Completeness
- Keyword Matching
- Formatting Analysis
- Grammar Analysis
- Resume Impact Analysis
- Missing Keywords
- Strengths & Weaknesses
- AI Recommendations

---

## ✨ AI Resume Optimizer

Improve resumes using AI.

Features

- Better Resume Summary
- Improved Bullet Points
- ATS Friendly Suggestions
- Action Verb Improvements
- Resume Enhancement

---

## 💼 AI Job Matching

Match resumes against jobs.

Features

- Resume vs Job Comparison
- Match Percentage
- Missing Skills
- Matching Skills
- Job Recommendations

---

## 🎤 AI Mock Interview

Practice interviews with AI.

Supports

- Technical Interviews
- HR Interviews
- Behavioral Interviews

Features

- Role Based Questions
- Difficulty Levels
- Previous / Next Question Navigation
- Personalized AI Feedback
- Ideal Answers
- Interview History

---

## 🗺 Career Roadmap Generator

Generate personalized learning plans.

Includes

- Monthly Learning Plan
- Weekly Tasks
- Learning Resources
- Recommended Projects
- Timeline Planning
- Progress Tracking

---

## 📊 Dashboard

Personal dashboard showing

- Resume Statistics
- ATS Results
- Interview History
- Job Matches
- Career Progress

---

## 📁 Job Application Tracker

Track your job applications.

- Applied Jobs
- Interview Status
- Offer Tracking
- Rejection Tracking
- Application History

---

# 🏗 Project Structure

```text
CareerPilot-AI
│
├── backend
│   ├── app
│   │
│   ├── agents
│   │   ├── ats_agent
│   │   ├── interview_agent
│   │   ├── roadmap_agent
│   │   ├── job_agent
│   │   └── resume_optimizer
│   │
│   ├── api
│   ├── auth
│   ├── database
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── parsers
│   └── main.py
│
├── frontend
│   ├── components
│   ├── services
│   ├── views
│   ├── assets
│   └── app.py
│
├── README.md
└── .gitignore
```

---

# ⚙️ Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Pydantic

## Frontend

- Streamlit

## AI Modules

- Resume Parser
- ATS Analyzer
- Resume Optimizer
- Job Matching Engine
- Interview Agent
- Career Roadmap Generator

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/Sanika-Gajarishi/CareerPilot.git

cd CareerPilot-AI
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Frontend Setup

Open a second terminal.

```bash
cd frontend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a file named **backend/.env**

```env
APP_NAME=CareerPilot AI
APP_VERSION=1.0.0

DEBUG=true

HOST=127.0.0.1
PORT=8000

DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=careerpilot
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

UPLOAD_DIR=uploads/resumes

MAX_FILE_SIZE_MB=10

GEMINI_API_KEY=your_gemini_api_key
```

---

# ▶ Running the Project

## Start Backend

```bash
cd backend

uvicorn app.main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

Swagger Docs

```
http://127.0.0.1:8000/docs
```

---

## Start Frontend

```bash
cd frontend

streamlit run app.py
```

Frontend

```
http://localhost:8501
```

---

# 📡 API Modules

| Module | Description |
|---------|-------------|
| Authentication | Register, Login, JWT |
| Resume | Resume Upload & Parsing |
| ATS | ATS Resume Analysis |
| Resume Optimizer | AI Resume Improvement |
| Job Matching | AI Job Matching |
| Interview | AI Mock Interview |
| Roadmap | Career Roadmap |
| Dashboard | User Dashboard |
| Job Tracker | Track Applications |
| Profile | User Profile |


---

# 📈 Project Workflow

```
User Login
      │
      ▼
Upload Resume
      │
      ▼
Resume Parsing
      │
      ├─────────────► ATS Analysis
      │
      ├─────────────► Resume Optimization
      │
      ├─────────────► Job Matching
      │
      ├─────────────► Mock Interview
      │
      └─────────────► Career Roadmap
                    │
                    ▼
              Dashboard
```

# 👩‍💻 Author

**Sanika Gajarishi**

GitHub

https://github.com/Sanika-Gajarishi

LinkedIn

*(https://www.linkedin.com/in/sanika-gajarishi-7a0583255/)*

---

# ⭐ Support

If you found this project helpful, consider giving it a **⭐ Star** on GitHub.

It helps others discover the project and motivates future development.

---

## 📄 License

This project is licensed under the MIT License.
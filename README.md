# 🤖 AI Resume Screener

An AI-powered Resume Screening System built with **Python**, **Flask**, **HTML**, **CSS**, and **JavaScript** that helps recruiters and hiring managers analyze resumes, calculate ATS scores, rank candidates, detect resume issues, and generate interview questions.

---

## 📌 Overview

The AI Resume Screener automates the resume screening process by extracting important information from resumes, comparing it with a given job description, and providing detailed analytics.

The application includes an interactive dashboard, candidate ranking, interview question generation, ATS score calculation, report generation, and resume history management.

---

# ✨ Features

- 📄 Resume Upload (PDF)
- 🤖 AI Resume Analysis
- 📊 ATS Score Calculation
- 🎯 Resume & Job Description Matching
- 🧠 Skill Extraction
- 📈 Candidate Ranking
- 📝 Interview Question Generator
- 📋 Resume Analysis Report
- 📉 Bias Detection
- 🔍 Fake Resume Detection
- 📊 Interactive Dashboard
- 📜 Resume History
- 📥 PDF Report Download
- 📱 Responsive UI
- 🌙 Modern Dashboard Design

---

# 🛠 Tech Stack

## Backend

- Python
- Flask
- SQLite
- Werkzeug
- Python-dotenv

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)
- Chart.js

---

# 📂 Project Structure

```
AI_Resume_Screener/
│
├── app.py
├── requirements.txt
├── README.md
│
├── uploads/
│
├── utils/
│   ├── __init__.py
│   ├── ats_checker.py
│   ├── bias_detector.py
│   ├── fake_resume_detector.py
│   ├── interview_generator.py
│   ├── matcher.py
│   ├── pdf_reader.py
│   ├── pdf_report.py
│   ├── skill_confidence.py
│   └── skill_extractor.py
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   ├── animations.css
│   │   ├── responsive.css
│   │   └── themes.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   ├── dashboard.js
│   │   ├── upload.js
│   │   ├── charts.js
│   │   ├── animations.js
│   │   ├── interview.js
│   │   ├── report.js
│   │   └── ranking.js
│   │
│   ├── images/
│   ├── icons/
│   └── audio/
│
├── templates/
│   ├── index.html
│   ├── analyze.html
│   ├── dashboard.html
│   ├── history.html
│   ├── interview.html
│   ├── ranking.html
│   ├── report.html
│   │
│   └── components/
│       ├── navbar.html
│       ├── sidebar.html
│       ├── footer.html
│       └── loader.html
│
└── resume_screener.db
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/jeevanabadveli/AI-Resume-Screener.git
```

```bash
cd AI-Resume-Screener
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python app.py
```

---

## Open Browser

```
http://127.0.0.1:5000/
```

---

# 📊 Modules

### 📄 Resume Analyzer

- Extract Resume Text
- ATS Score
- Resume Parsing
- Experience Detection
- Education Detection
- Skill Detection

---

### 🎯 Resume Matcher

- Compare Resume
- Compare Job Description
- Match Percentage
- Missing Skills
- Recommendations

---

### 📈 Dashboard

- Total Candidates
- Average ATS Score
- Resume Statistics
- Charts
- Analytics

---

### 🏆 Resume Ranking

- Rank Multiple Candidates
- Best Candidate Selection
- Score Comparison
- Progress Visualization

---

### 🧠 Interview Generator

Automatically generates interview questions based on

- Skills
- Experience
- Technologies
- Job Description

---

### 📋 Report Generation

Generates complete analysis report including

- ATS Score
- Match Score
- Skills
- Recommendations
- Candidate Details

---

### 📜 Resume History

Stores previous analyses

- Candidate Name
- ATS Score
- Match Score
- Analysis Date

---

# 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home Page |
| `/dashboard` | GET | Dashboard |
| `/analyze` | GET | Analyze Page |
| `/ranking` | GET | Ranking Page |
| `/history` | GET | History |
| `/interview` | GET | Interview Page |
| `/report` | GET | Report |
| `/api/analyze` | POST | Analyze Resume |
| `/api/rank` | POST | Rank Resumes |
| `/api/dashboard` | GET | Dashboard Data |
| `/api/history` | GET | Resume History |
| `/api/result` | GET | Latest Result |
| `/api/interview` | POST | Generate Interview Questions |
| `/api/download-report` | POST | Download PDF Report |

---

# 🚀 Future Improvements

- OpenAI GPT Integration
- AI Resume Suggestions
- LinkedIn Profile Analysis
- Resume Keyword Optimization
- Email Notification
- User Authentication
- Recruiter Dashboard
- Candidate Login
- Cloud Deployment
- Docker Support
- REST API Documentation

---



## 💡 Project Highlights

- AI-Based Resume Screening
- ATS Score Calculator
- Candidate Ranking
- Interview Question Generator
- Resume Analysis Dashboard
- PDF Report Generation
- Flask Backend
- Modern Responsive UI
- Recruiter-Friendly Workflow

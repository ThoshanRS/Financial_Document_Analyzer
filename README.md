# 📊 AI Financial Document Analyzer  
*CrewAI Debug & Optimization Project*

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.3-009688.svg)
![CrewAI](https://img.shields.io/badge/CrewAI-0.130.0-orange.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)

---

## 📌 Overview

This project is an **AI-powered Financial Document Analysis System** built using **CrewAI** and **FastAPI**.

Originally provided as a **buggy codebase**, this repository has been:

- ✅ Debugged (deterministic issues fixed)
- ✅ Refactored (clean architecture)
- ✅ Prompt-optimized (hallucination removal)
- ✅ Upgraded with asynchronous queue execution
- ✅ Integrated with a persistent SQLite database

The system processes corporate financial reports and generates:

- Financial insights  
- Risk assessments  
- Investment recommendations  
- Regulatory-aware summaries  

---

## 🚀 Key Features

### 🤖 Multi-Agent AI Workflow
Built with CrewAI orchestrating:

- 🔎 Financial Document Verifier  
- 📈 Senior Financial Analyst  
- ⚠️ Risk Assessment Expert  
- 💼 Investment Advisor  

Agents collaborate sequentially to produce structured, data-grounded outputs.

---

### ⚡ Asynchronous Queue Worker Model
- Implemented using **FastAPI BackgroundTasks**
- Non-blocking API execution
- Supports concurrent analysis requests
- Immediate task ID returned to client

---

### 🗄️ Database Integration
- Integrated **SQLite + SQLAlchemy ORM**
- Persistent storage of:
  - Task ID
  - File metadata
  - User query
  - Analysis result
  - Error logs
  - Processing status

Database file:

```
analysis.db
```

---

### 📄 Robust PDF Extraction
- Implemented using **PyPDF**
- Efficient O(N) text normalization
- Safe extraction with error handling

---

### 🔍 Web Search Integration
- Serper API integrated for external financial fact-checking

---

## 🏗️ System Architecture

```
Client Request
     ↓
FastAPI API
     ↓
Background Task Queue (Worker Simulation)
     ↓
CrewAI Multi-Agent Workflow
     ↓
SQLite Database (Persistent Storage)
```

---

## 🐛 Bugs Identified & Fixed

### 1️⃣ Dependency Conflicts

**Issues**
- Invalid CrewAI version pin
- Conflicting `onnxruntime`, `click`, `pypdf`, `langchain` versions

**Fix**
- Updated compatible versions
- Removed hard dependency locks
- Rebuilt virtual environment

---

### 2️⃣ Tool Registration Errors

**Issues**
- Incorrect `tool=[...]` argument
- Missing `@tool` decorators
- Async tools incompatible with CrewAI execution

**Fix**
- Standardized to `tools=[...]`
- Converted tools to synchronous CrewAI-compatible functions

---

### 3️⃣ LLM Configuration Errors

**Issues**
- Incorrect provider routing in LiteLLM
- Default fallback to OpenAI without explicit config

**Fix**
- Explicit provider-based model configuration
- Environment-based API key loading
- Clean LLM abstraction

---

### 4️⃣ Prompt Engineering Flaws

**Issues**
- Prompts allowed hallucinations
- No compliance guardrails

**Fix**
- Removed unsafe instructions
- Rewrote system prompts to:
  - Anchor strictly to provided document
  - Enforce regulatory awareness
  - Maintain professional tone

---

### 5️⃣ Blocking API Execution

**Issue**
- Crew execution blocked FastAPI thread

**Fix**
- Refactored to asynchronous background execution

---

## 🤖 AI Crew

| Agent | Responsibility |
|--------|----------------|
| Financial Document Verifier | Validates report authenticity |
| Senior Financial Analyst | Extracts financial KPIs |
| Risk Assessment Expert | Identifies operational & financial risks |
| Investment Advisor | Generates risk-adjusted recommendations |

---

## 📂 Project Structure

```
financial-document-analyzer/
│
├── main.py              # FastAPI application
├── agents.py            # CrewAI agents
├── tools.py             # Custom tools
├── task.py              # Agent tasks
├── database.py          # SQLite database models
├── requirements.txt
├── .env
└── README.md
```

---

## 🛠️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd financial-document-analyzer
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create `.env` file in root:

```
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
```

*(Any LiteLLM-supported provider can be configured.)*

---

### 5️⃣ Run Application

```bash
uvicorn main:app --reload
```

Access API docs at:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Documentation

### POST `/analyze`

Upload financial document for analysis.

**Form Data**
- `file` → PDF file
- `query` → Optional analysis instruction

**Response**

```json
{
  "status": "success",
  "task_id": "uuid"
}
```

---

### GET `/status/{task_id}`

Check analysis progress.

#### While Processing

```json
{
  "status": "processing"
}
```

#### When Completed

```json
{
  "status": "completed",
  "analysis": "Full AI-generated report..."
}
```

---

## 🔄 Workflow

1. User uploads financial report  
2. File stored locally  
3. Background worker triggers CrewAI  
4. Agents collaborate sequentially  
5. Results stored in SQLite  
6. User polls for completion  

---

## 🧪 Technologies Used

- CrewAI  
- FastAPI  
- LiteLLM  
- SQLAlchemy  
- SQLite  
- PyPDF  
- LangChain  

---

## ✅ Submission Checklist

- [x] Deterministic bugs fixed  
- [x] Inefficient prompts optimized  
- [x] Working CrewAI multi-agent system  
- [x] Asynchronous queue worker implemented  
- [x] Database integration added  
- [x] API documentation included  

---

## 👨‍💻 Author

**Thoshan Naik R S**  
SAP Certified Developer | Data Analyst | AI Application Builder  

---

## 🎯 Final Result

This project demonstrates:

- Multi-agent orchestration  
- Backend engineering  
- Async API design  
- LLM integration  
- Production-oriented debugging  
- Database-backed AI workflows  "# Financial_Document_Analyzer" 

☁️ CloudOps Copilot

**Explainable Multi-Agent Incident and Cost Triage for AWS Teams**

CloudOps Copilot is an AI-powered, multi-agent assistant designed for small engineering teams. When AWS costs spike, deployments fail, or permissions break, teams waste hours jumping between CloudWatch logs, IAM policies, and billing dashboards. 

Instead of giving teams another dashboard, CloudOps Copilot acts as an agentic SRE teammate. It analyzes operational evidence and internal runbooks to produce an explainable incident report with root causes, cost impacts, blast radius, and step-by-step remediation plans.

## 🚀 Features

* **Multi-Agent Architecture**: Uses a supervisor agent to route tasks to specialized sub-agents.
* **Cost Agent**: Detects cost anomalies and billing spikes from CSV data.
* **Infrastructure Agent**: Parses CloudWatch JSON logs to find deployment failure root causes.
* **Security Agent**: Analyzes IAM policies for missing permissions or security vulnerabilities.
* **RAG Knowledge Agent**: Uses ChromaDB to ground AI answers in local markdown runbooks.
* **Action Plan Agent**: Synthesizes all findings into a clean, human-readable UI report.

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Backend**: FastAPI (Python)
* **AI/LLM**: OpenAI API (GPT-4o-mini) / Groq API 
* **Vector Database**: ChromaDB (Local)

---

## 💻 Local Setup Instructions

Follow these steps to run CloudOps Copilot from scratch on your local Windows machine.

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/cloudops-copilot.git](https://github.com/YOUR_GITHUB_USERNAME/cloudops-copilot.git)
cd cloudops-copilot
2. Set up a Python Virtual Environment
PowerShell
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies
PowerShell
pip install -r requirements.txt
4. Set up your API Key
Create a file named .env in the root directory of the project and add your OpenAI or Groq API key:

Plaintext
OPENAI_API_KEY=sk-proj-your-api-key-here
(Note: .env is included in .gitignore and will not be uploaded to GitHub).

▶️ Running the Application
Because this is a full-stack application, you need to run the backend and the frontend in two separate terminals.

Terminal 1: Start the FastAPI Backend
Ensure your virtual environment is active, then run:

PowerShell
uvicorn app.main:app --reload
The backend will start on http://127.0.0.1:8000.

Terminal 2: Start the Streamlit Frontend
Open a second terminal, activate the virtual environment (.\venv\Scripts\activate), and run:

PowerShell
streamlit run app/frontend.py
Your browser will automatically open the UI at http://localhost:8501.

📁 Project Structure
/app - Contains the FastAPI backend, Agent logic, RAG setup, and Streamlit frontend.

/sample-data - Mock AWS JSON logs, IAM policies, billing CSVs, and markdown runbooks used for the MVP.
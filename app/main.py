from dotenv import load_dotenv
load_dotenv() # This loads the .env file
from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
import json
import csv
import os
from app.agents import run_all_agents

app = FastAPI(title="CloudOps Copilot API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "CloudOps Copilot is running."}

@app.post("/analyze")
def analyze_incident():
    # Define paths to the mock data we created in Step 2
    base_dir = os.path.dirname(os.path.dirname(__file__))
    logs_path = os.path.join(base_dir, "sample-data", "cloudwatch_logs.json")
    iam_path = os.path.join(base_dir, "sample-data", "iam_policy.json")
    billing_path = os.path.join(base_dir, "sample-data", "billing_anomaly.csv")

    # Read the mock data
    with open(logs_path, "r") as f:
        logs = json.load(f)

    with open(iam_path, "r") as f:
        iam_policy = json.load(f)

    with open(billing_path, "r") as f:
        reader = csv.DictReader(f)
        billing_data = list(reader)

    # Pass the data to the orchestrator in agents.py
    report = run_all_agents(logs, billing_data, iam_policy)
    return {"status": "success", "report": report}

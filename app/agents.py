import os
import json
from openai import OpenAI
from app.rag import setup_rag, query_rag
from app.rag import setup_rag, query_rag

# Initialize the vector database when the app starts
print("Initializing RAG Database... (This might take a few seconds the first time to download the embedding model)")
rag_collection = setup_rag()

def supervisor_agent(question="Why did my deployment fail and costs spike?"):
    return {
        "call_cost_agent": True,
        "call_infra_agent": True,
        "call_security_agent": True,
        "call_rag_agent": True # NEW: Supervisor now calls RAG
    }

def cost_agent(billing_data):
    # NOTE: If you are using Groq, remember to add your api_key and base_url here 
    # just like you did in the action_plan_agent!
    client = OpenAI()
    
    billing_str = json.dumps(billing_data, indent=2)
    
    prompt = f"""
    You are an AWS FinOps AI. Review this billing data:
    {billing_str}
    
    Identify if there is a sudden cost spike.
    Output EXACTLY a JSON object with these keys:
    - "finding": A short sentence explaining the cost anomaly.
    - "evidence": The exact dates and dollar amounts involved.
    - "confidence": A float between 0.0 and 1.0.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Change to "llama3-8b-8192" if using Groq
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a CloudOps AI. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)

def infra_agent(logs):
    client = OpenAI()
    
    # We convert the raw log dictionary into a string so the AI can read it
    logs_str = json.dumps(logs, indent=2)
    
    prompt = f"""
    You are an AWS Infrastructure Expert AI. Review the following CloudWatch logs:
    {logs_str}
    
    Find the primary reason the deployment failed. 
    Output EXACTLY a JSON object with these keys:
    - "finding": A short sentence explaining the failure.
    - "evidence": The specific error code or timestamp from the logs.
    - "confidence": A float between 0.0 and 1.0 representing your certainty.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a CloudOps AI. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)

def security_agent(iam_policy):
    client = OpenAI()
    
    policy_str = json.dumps(iam_policy, indent=2)
    
    prompt = f"""
    You are an AWS Cloud Security Expert AI. Review this IAM Role Policy:
    {policy_str}
    
    Identify if any permissions are missing that would prevent an EC2 instance from downloading a config file from S3.
    Output EXACTLY a JSON object with these keys:
    - "finding": A short sentence explaining the missing permission.
    - "security_risk": "High", "Medium", or "Low".
    - "confidence": A float between 0.0 and 1.0.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a CloudOps AI. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)

# NEW: The Knowledge Agent
def rag_agent(question):
    context = query_rag(rag_collection, question)
    return {
        "finding": "Retrieved AWS runbook guidelines for incident.",
        "retrieved_context": context
    }

def action_plan_agent(all_findings):
    # 1. Initialize the OpenAI client (it automatically finds your key in the .env file)
    client = OpenAI()

    # 2. Convert all the evidence we gathered into a text string
    evidence_str = json.dumps(all_findings, indent=2)

    # 3. Write the prompt instructing the AI what to do
    prompt = f"""
    You are the CloudOps Copilot Action Agent. 
    Review the following evidence from the specialist agents:
    {evidence_str}

    Generate a final incident report based ONLY on the evidence provided.
    Output a JSON object with EXACTLY these 4 keys:
    - "executive_summary": A 1-sentence plain English summary.
    - "most_likely_root_cause": The root cause based on infra findings.
    - "cost_impact": Explain the cost spike based on cost findings.
    - "immediate_actions": A list of 2-3 specific step-by-step strings to fix the issue. Include the RAG guidance.
    """

    # 4. Call the LLM and force it to return valid JSON
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Fast and cost-effective
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a DevOps AI. Always return valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # 5. Parse the AI's text response back into a Python dictionary
    ai_generated_json = json.loads(response.choices[0].message.content)

    # Safely inject our RAG runbook guidance so the UI can display it
    ai_generated_json["runbook_guidance"] = all_findings.get("rag_analysis", {}).get("retrieved_context", "No runbook found.")

    return ai_generated_json

def run_all_agents(logs, billing_data, iam_policy):
    plan = supervisor_agent()
    findings = {}

    if plan["call_cost_agent"]:
        findings["cost_analysis"] = cost_agent(billing_data)

    if plan["call_infra_agent"]:
        findings["infra_analysis"] = infra_agent(logs)

    if plan["call_security_agent"]:
        findings["security_analysis"] = security_agent(iam_policy)

    # NEW: Execute RAG Agent
    if plan["call_rag_agent"]:
        findings["rag_analysis"] = rag_agent("Why did EC2 costs spike?")

    final_report = action_plan_agent(findings)
    return final_report
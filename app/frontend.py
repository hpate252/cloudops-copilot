import streamlit as st
import requests

# Configure the page
st.set_page_config(page_title="CloudOps Copilot", page_icon="☁️", layout="wide")

st.title("☁️ CloudOps Copilot")
st.subheader("Explainable Multi-Agent Incident & Cost Triage")

# Sidebar for "File Uploads"
with st.sidebar:
    st.header("1. Upload Evidence")
    st.info("For MVP demo, these files are pre-loaded from /sample-data")
    st.checkbox("cloudwatch_logs.json", value=True, disabled=True)
    st.checkbox("billing_anomaly.csv", value=True, disabled=True)
    st.checkbox("iam_policy.json", value=True, disabled=True)

    st.divider()
    st.header("Agent Status")
    st.success("✅ Supervisor Agent Ready")
    st.success("✅ Cost Agent Ready")
    st.success("✅ Infra Agent Ready")
    st.success("✅ Security Agent Ready")
    st.success("✅ RAG Knowledge Base Ready")

# Main interaction area
st.markdown("### 2. Ask Copilot")
question = st.text_input("Describe the issue:", value="Why did my deployment fail and why did costs spike?")

if st.button("Analyze Incident", type="primary"):
    with st.spinner("Agents are investigating logs, billing, and IAM policies..."):
        try:
            # Call our FastAPI backend
            response = requests.post("http://127.0.0.1:8000/analyze")
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "success":
                report = data["report"]

                # Display the formatted report
                st.divider()
                st.markdown("## 🚨 Incident Triage Report")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Executive Summary")
                    st.info(report.get("executive_summary"))

                    st.markdown("### Most Likely Root Cause")
                    st.error(report.get("most_likely_root_cause"))

                with col2:
                    st.markdown("### Cost Impact")
                    st.warning(report.get("cost_impact"))

                    st.markdown("### Retrieved Runbook Guidance")
                    st.markdown(f"> {report.get('runbook_guidance')}")

                st.markdown("### 🛠️ Immediate Actions")
                for action in report.get("immediate_actions", []):
                    st.markdown(f"- **{action}**")

        except Exception as e:
            st.error(f"Failed to connect to backend. Is the FastAPI server running? Error: {e}")
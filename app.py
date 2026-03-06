import streamlit as st
import json
from log_parser import read_log_file, extract_relevant_sections
from prompt_builder import build_prompt
from bedrock_client import BedrockClient
from rag.vector_store import SimpleIncidentMemory


st.set_page_config(
    page_title="OpsInsight AI",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 OpsInsight AI")
st.subheader("AI-Powered DevOps Incident Analyzer")

# Author
st.markdown("Built by **Genevio – DevOps Engineer**")

st.write(
    "Upload DevOps or infrastructure logs and let AI analyze incidents, "
    "identify the root cause, and recommend remediation steps."
)

# Upload file
uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])


if uploaded_file:

    log_content = uploaded_file.read().decode("utf-8")

    st.markdown("### Log Preview")
    st.code(log_content[:1000], language="text")

    if st.button("Analyze Incident 🚀"):

        with st.spinner("AI is analyzing the logs..."):

            log_lines = log_content.split("\n")
            filtered_log = extract_relevant_sections(log_lines)

            memory = SimpleIncidentMemory()
            retrieved_incident = memory.retrieve_similar_incident(filtered_log)

            prompt = build_prompt(filtered_log, retrieved_incident)

            bedrock = BedrockClient()
            model_output = bedrock.invoke_model(prompt)

            result = json.loads(model_output)

        st.success("Analysis Complete")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🚨 Incident Type")
            st.write(result["incident_type"])

            st.markdown("### 🔍 Root Cause")
            st.write(result["root_cause"])

        with col2:
            st.markdown("### 📊 Confidence Score")
            st.write(result["confidence_score"])

        st.markdown("### 🛠 Recommended Fix")

        for step in result["remediation_steps"]:
            st.write("•", step)

# Footer
st.markdown("---")
st.caption("© 2026 Genevio | OpsInsight AI")
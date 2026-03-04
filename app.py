import streamlit as st
import json
from log_parser import read_log_file, extract_relevant_sections
from prompt_builder import build_prompt
from bedrock_client import BedrockClient
from rag.vector_store import SimpleIncidentMemory

st.title("OpsInsight AI - DevOps Incident Analyzer")

uploaded_file = st.file_uploader("Upload Log File", type=["log", "txt"])

if uploaded_file is not None:

    log_text = uploaded_file.read().decode("utf-8")

    st.subheader("Log Preview")
    st.code(log_text[:500])

    if st.button("Analyze Incident"):

        log_lines = log_text.splitlines()
        filtered_log = extract_relevant_sections(log_lines)

        memory = SimpleIncidentMemory()
        retrieved_incident = memory.retrieve_similar_incident(filtered_log)

        prompt = build_prompt(filtered_log, retrieved_incident)

        bedrock = BedrockClient()

        model_output = bedrock.invoke_model(prompt)

        try:
            result = json.loads(model_output)

            st.subheader("Incident Analysis")

            st.write("**Incident Type:**", result["incident_type"])
            st.write("**Root Cause:**", result["root_cause"])
            st.write("**Confidence:**", result["confidence_score"])

            st.write("**Remediation Steps:**")

            for step in result["remediation_steps"]:
                st.write("•", step)

        except:
            st.error("Model output parsing failed")
            st.text(model_output)
import streamlit as st
import json
from log_parser import extract_relevant_sections
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

    log_content = uploaded_file.read().decode("utf-8", errors="ignore")

    # Split lines
    log_lines = log_content.split("\n")

    # Show preview
    st.markdown("### Log Preview")
    preview_text = "\n".join(log_lines[:40])
    st.code(preview_text, language="text")

    st.info(f"Total log lines: {len(log_lines)}")

    if st.button("Analyze Incident 🚀"):

        with st.spinner("AI is analyzing the logs..."):

            try:

                # STEP 1: Extract relevant sections
                filtered_log = extract_relevant_sections(log_lines)

                # STEP 2: Additional filtering for large logs
                important_lines = [
                    line for line in filtered_log.split("\n")
                    if "ERROR" in line or "WARN" in line or "CRITICAL" in line
                ]

                # If important lines exist, use them
                if important_lines:
                    filtered_log = "\n".join(important_lines[-60:])  # last 60 important lines

                # STEP 3: Hard limit to avoid Bedrock overflow
                filtered_log = filtered_log[:8000]

                # STEP 4: Retrieve similar past incident (RAG)
                memory = SimpleIncidentMemory()
                retrieved_incident = memory.retrieve_similar_incident(filtered_log)

                # STEP 5: Build prompt
                prompt = build_prompt(filtered_log, retrieved_incident)

                # STEP 6: Invoke Bedrock
                bedrock = BedrockClient()
                model_output = bedrock.invoke_model(prompt)

                # Parse response
                result = json.loads(model_output)

                st.success("Analysis Complete")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 🚨 Incident Type")
                    st.write(result.get("incident_type", "Unknown"))

                    st.markdown("### 🔍 Root Cause")
                    st.write(result.get("root_cause", "Not detected"))

                with col2:
                    st.markdown("### 📊 Confidence Score")
                    st.write(result.get("confidence_score", "N/A"))

                st.markdown("### 🛠 Recommended Fix")

                for step in result.get("remediation_steps", []):
                    st.write("•", step)

            except Exception as e:

                st.error("Incident analysis failed.")
                st.code(str(e))

# Footer
st.markdown("---")
st.caption("© 2026 Genevio | OpsInsight AI")
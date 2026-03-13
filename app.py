import streamlit as st
import json
from log_parser import extract_relevant_sections
from prompt_builder import build_prompt, build_summary_prompt, build_timeline_prompt
from bedrock_client import BedrockClient
from rag.vector_store import SimpleIncidentMemory


st.set_page_config(
    page_title="OpsInsight AI",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 OpsInsight AI")
st.caption("AI-driven incident analysis using RAG + AWS Bedrock")

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
    log_lines = log_content.split("\n")

    # Log Preview
    st.markdown("### Log Preview")
    preview_text = "\n".join(log_lines[:40])
    st.code(preview_text, language="text")

    st.info(f"Total log lines: {len(log_lines)}")

    if st.button("Analyze Incident 🚀"):

        with st.spinner("AI is analyzing the logs..."):

            try:

                # STEP 1: Extract relevant sections
                filtered_log = extract_relevant_sections(log_lines)

                # STEP 2: Filter important lines
                important_lines = [
                    line for line in filtered_log.split("\n")
                    if "ERROR" in line or "WARN" in line or "CRITICAL" in line
                ]

                if important_lines:
                    filtered_log = "\n".join(important_lines[-60:])

                # STEP 3: Limit log size for LLM
                filtered_log = filtered_log[:8000]

                # Initialize Bedrock client
                bedrock = BedrockClient()

                # STEP 4: AI LOG SUMMARY
                summary_prompt = build_summary_prompt(filtered_log)
                summary_output = bedrock.invoke_model(summary_prompt)
                summary_result = json.loads(summary_output)

                st.success("Log Summary Generated")

                colA, colB = st.columns(2)

                with colA:
                    st.markdown("### 📜 Log Summary")
                    st.write(summary_result.get("summary", "No summary generated"))

                with colB:
                    st.markdown("### ⚠ Possible Issue")
                    st.write(summary_result.get("possible_issue", "Unknown"))

                    st.markdown("### 🚦 Severity")
                    st.write(summary_result.get("severity", "Unknown"))

                st.markdown("---")

                # STEP 5: INCIDENT TIMELINE
                timeline_prompt = build_timeline_prompt(filtered_log)
                timeline_output = bedrock.invoke_model(timeline_prompt)
                timeline_result = json.loads(timeline_output)

                st.markdown("### ⏱ Incident Timeline")

                for event in timeline_result.get("timeline", []):
                    st.write("•", event)

                st.markdown("---")

                # STEP 6: Retrieve similar past incident (RAG)
                memory = SimpleIncidentMemory()
                retrieved_incident = memory.retrieve_similar_incident(filtered_log)

                # STEP 7: Root Cause Analysis
                prompt = build_prompt(filtered_log, retrieved_incident)
                model_output = bedrock.invoke_model(prompt)
                result = json.loads(model_output)

                st.success("Incident Analysis Complete")

                # INCIDENT DASHBOARD METRICS
                st.markdown("### 📊 Incident Overview")

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric(
                    label="🚨 Incident Type",
                    value=result.get("incident_type", "Unknown")
                )

                metric2.metric(
                    label="📊 Confidence Score",
                    value=result.get("confidence_score", "N/A")
                )

                metric3.metric(
                    label="⚠ Severity",
                    value=summary_result.get("severity", "Unknown")
                )

                st.markdown("---")

                # Root Cause
                st.markdown("### 🔍 Root Cause")
                st.write(result.get("root_cause", "Not detected"))

                # Recommended Fix
                st.markdown("### 🛠 Recommended Fix")

                for step in result.get("remediation_steps", []):
                    st.write("•", step)

            except Exception as e:

                st.error("Incident analysis failed.")
                st.code(str(e))


# Footer
st.markdown("---")
st.caption("© 2026 Genevio | OpsInsight AI")
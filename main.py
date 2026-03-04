# main.py

import argparse
import json
from log_parser import read_log_file, extract_relevant_sections
from prompt_builder import build_prompt
from bedrock_client import BedrockClient
from rag.vector_store import SimpleIncidentMemory

CONFIDENCE_THRESHOLD = 0.75


def run_analysis(log_content, retrieved_incident):

    prompt = build_prompt(log_content, retrieved_incident)

    bedrock = BedrockClient()

    model_output = bedrock.invoke_model(prompt)

    try:
        parsed_output = json.loads(model_output)
        return parsed_output
    except json.JSONDecodeError:
        print("\nModel did not return valid JSON.")
        print(model_output)
        return None


def main():

    parser = argparse.ArgumentParser(
        description="OpsInsight AI - DevOps Incident Analyzer"
    )

    parser.add_argument("--log", required=True, help="Path to log file")

    args = parser.parse_args()

    # STEP 1 — Read Log
    log_lines = read_log_file(args.log)
    filtered_log_content = extract_relevant_sections(log_lines)

    print("\nFiltered Log Length:", len(filtered_log_content), "characters")

    # STEP 2 — Load Incident Memory
    memory = SimpleIncidentMemory()

    retrieved_incident = memory.retrieve_similar_incident(filtered_log_content)

    if retrieved_incident:
        print("\n=== Retrieved Similar Past Incident ===")
        print(json.dumps(retrieved_incident, indent=4))
    else:
        print("\nNo similar past incident found.")

    # STEP 3 — Initial Analysis
    print("\nRunning initial analysis (filtered logs)...")

    initial_result = run_analysis(filtered_log_content, retrieved_incident)

    if not initial_result:
        print("Initial analysis failed.")
        return

    initial_confidence = initial_result.get("confidence_score", 0)

    print("\n=== Initial Analysis ===")
    print(json.dumps(initial_result, indent=4))

    # STEP 4 — Confidence Agent Loop
    if initial_confidence < CONFIDENCE_THRESHOLD:

        print("\n⚠ Low confidence detected. Running deeper analysis...")

        full_log = "".join(log_lines)

        refined_result = run_analysis(full_log, retrieved_incident)

        if refined_result:
            refined_confidence = refined_result.get("confidence_score", 0)

            print("\n=== Refined Analysis ===")
            print(json.dumps(refined_result, indent=4))

            if refined_confidence > initial_confidence:
                final_result = refined_result
                print("\n✅ Refined analysis selected.")
            else:
                final_result = initial_result
                print("\nℹ Initial analysis retained.")
        else:
            final_result = initial_result

    else:
        print("\n✅ High confidence. No re-analysis required.")
        final_result = initial_result

    # STEP 5 — Self Learning Memory
    if retrieved_incident is None:

        new_incident = {
            "incident_type": final_result.get("incident_type"),
            "description": final_result.get("root_cause"),
            "recommended_fix": ", ".join(final_result.get("remediation_steps", []))
        }

        memory.add_new_incident(new_incident)

    # STEP 6 — Final Output
    print("\n=== Final Selected Analysis ===")
    print(json.dumps(final_result, indent=4))


if __name__ == "__main__":
    main()
# prompt_builder.py

import json


def build_prompt(log_content: str, retrieved_context: dict = None) -> str:

    memory_section = ""

    if retrieved_context:
        memory_section = f"""
Previous Similar Incident:
{json.dumps(retrieved_context, indent=2)}

Use this past incident as reference while analyzing the current issue.
"""

    prompt = f"""
You are a senior DevOps SRE AI assistant.

Analyze the following Kubernetes log and return STRICT JSON only.

Log Data:
{log_content}

{memory_section}

Return output in this JSON format only:

{{
    "incident_type": "",
    "root_cause": "",
    "confidence_score": 0.0,
    "remediation_steps": []
}}

Rules:
- Do NOT add explanations.
- Do NOT add markdown.
- Return valid JSON only.
"""

    return prompt
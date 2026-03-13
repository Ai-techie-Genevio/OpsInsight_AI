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


def build_summary_prompt(log_content: str) -> str:
    """
    Build prompt for AI log summarization.
    Used before root cause analysis.
    """

    prompt = f"""
You are a DevOps AI observability assistant.

Analyze the following infrastructure logs and summarize what is happening.

Logs:
{log_content}

Return STRICT JSON only in this format:

{{
    "summary": "",
    "possible_issue": "",
    "severity": "Low | Medium | High"
}}

Rules:
- Do NOT include explanations outside JSON.
- Return valid JSON only.
"""

    return prompt


def build_timeline_prompt(log_content: str) -> str:
    """
    Build prompt for incident timeline extraction.
    """

    prompt = f"""
You are a DevOps incident investigation AI.

From the following infrastructure logs extract the key incident timeline.

Logs:
{log_content}

Return STRICT JSON only in this format:

{{
    "timeline": [
        "timestamp event",
        "timestamp event",
        "timestamp event"
    ]
}}

Rules:
- Extract only important events
- Focus on ERROR, WARN, CRITICAL logs
- Keep the timeline short and meaningful
- Do NOT include explanations outside JSON
"""

    return prompt
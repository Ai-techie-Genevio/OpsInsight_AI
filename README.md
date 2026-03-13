OpsInsight AI — DevOps Incident Analyzer

OpsInsight AI is an intelligent DevOps log analysis system that uses **Generative AI, RAG, and Vector Search** to automatically detect infrastructure incidents and suggest remediation steps.

The system analyzes logs from CI/CD pipelines, Kubernetes clusters, and microservices, identifies the root cause, and recommends solutions using AI reasoning.

# OpsInsight AI

![Python](https://img.shields.io/badge/Python-3.11-blue)
![AI](https://img.shields.io/badge/AI-LLM-green)
![VectorDB](https://img.shields.io/badge/VectorDB-FAISS-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
---

# Architecture

```
Log File / CI-CD / Kubernetes Logs
            ↓
        Log Parser
            ↓
     Log Filtering Engine
            ↓
   AI Log Summary (Bedrock Claude)
            ↓
   Incident Timeline Extraction
            ↓
 Embedding Model (SentenceTransformer)
            ↓
      Vector Database (FAISS)
            ↓
 Retrieve Similar Incidents (RAG)
            ↓
      LLM Root Cause Analysis
            ↓
  Confidence-Based Evaluation
            ↓
   Self-Learning Incident Memory
            ↓
      DevOps Incident Report

---

# Features

• AI-powered DevOps incident detection
• Retrieval-Augmented Generation (RAG) for contextual analysis
• FAISS vector database for semantic log similarity search
• Self-learning incident memory system
• Confidence-based AI re-analysis agent
• Web-based UI for uploading and analyzing logs
• Supports large log files (1MB+)

---

# Technologies Used

Python
Streamlit
AWS Bedrock (Claude Model)
FAISS Vector Database
Sentence Transformers
Retrieval-Augmented Generation (RAG)

---

# Project Structure

```
opsinsight/
│
├── app.py
├── main.py
├── log_parser.py
├── prompt_builder.py
├── bedrock_client.py
│
├── rag/
│   ├── vector_store.py
│   └── incident_memory.json
│
├── sample_logs/
│   ├── memory_issue.log
│   ├── cpu_issue.log
│   ├── database_outage.log
│   └── kubernetes_cluster_disk_failure_1MB.txt
│
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```
git clone https://github.com/YOUR_USERNAME/opsinsight-ai.git
cd opsinsight-ai
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Running the Web UI

Start the application:

```
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

Upload any log file and click **Analyze Incident**.

---

# Example Incidents Detected

Memory Exhaustion
CPU Throttling
Database Outage
Kubernetes Disk Pressure
CI/CD Deployment Failure

---

# Example Output

```
Incident Type: Memory Exhaustion

Root Cause:
Container terminated due to OOMKilled and CrashLoopBackOff.

Confidence Score: 0.9

Remediation Steps:
• Increase container memory limits
• Investigate application memory leaks
• Enable memory monitoring alerts
```

---

# Future Improvements

• Multi-incident retrieval (Top-3 RAG search)
• Real-time log streaming analysis
• Slack / PagerDuty alert integration
• Kubernetes cluster monitoring agent
• Bedrock Agent integration

---
## Architecture

See [architecture.md](architecture.md)

## Demo

### Upload Log File

The user uploads a DevOps log file through the Streamlit UI.

### AI Analysis

OpsInsight AI analyzes the log using RAG + LLM.

### Output

```
Incident Type: Kubernetes Disk Pressure

Root Cause:
Node filesystem exhaustion causing pod eviction and cluster instability.

Confidence Score: 0.91

Remediation Steps:
- Free disk space on affected nodes
- Clean unused container images
- Enable log rotation
- Add disk monitoring alerts
```

## Why This Project Matters

Modern DevOps environments generate massive volumes of logs from CI/CD pipelines, microservices, and Kubernetes clusters.
Manually analyzing these logs during incidents is slow and error-prone.

OpsInsight AI automates incident analysis by combining:

* Vector search (FAISS)
* Retrieval-Augmented Generation (RAG)
* Large Language Models (AWS Bedrock)
* Self-learning incident memory

The system enables faster root cause detection and intelligent remediation suggestions.



# Author

Genevio R
DevOps Engineer | AI & Cloud Enthusiast


## Contribution

If you would like to contribute or improve this project,
please create a Pull Request.

For collaboration or questions, feel free to contact me.


# OpsInsight AI Architecture

```
            DevOps Logs
        (CI/CD / Kubernetes)
                │
                ▼
           Log Parser
     (Filters critical errors)
                │
                ▼
       Embedding Generator
     (Sentence Transformers)
                │
                ▼
        Vector Database
              FAISS
                │
                ▼
      Similar Incident Retrieval
            (RAG Layer)
                │
                ▼
        LLM Root Cause Analysis
          (AWS Bedrock)
                │
                ▼
        Confidence Agent Loop
     (Re-analyze if confidence low)
                │
                ▼
        Self-Learning Memory
       (Add new incidents)
                │
                ▼
          Incident Report
```

This pipeline enables automated DevOps incident detection and remediation using AI.

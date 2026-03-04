# rag/semantic_vector_store.py

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticIncidentMemory:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Example memory database
        self.incident_db = [
            {
                "incident_type": "Memory Exhaustion",
                "description": "Container terminated with OOMKilled and CrashLoopBackOff due to high memory usage.",
                "recommended_fix": "Increase container memory limits and investigate memory leaks."
            },
            {
                "incident_type": "CPU Throttling",
                "description": "Application experiencing CPU throttling and high CPU usage.",
                "recommended_fix": "Increase CPU limits and optimize CPU-heavy processes."
            },
        ]

        # Precompute embeddings
        self.embeddings = self.model.encode(
            [incident["description"] for incident in self.incident_db]
        )

    def retrieve_similar_incident(self, log_text, threshold=0.5):

        log_embedding = self.model.encode([log_text])

        similarities = cosine_similarity(log_embedding, self.embeddings)[0]

        best_index = np.argmax(similarities)
        best_score = similarities[best_index]

        print(f"\nSemantic Similarity Score: {best_score:.4f}")

        if best_score >= threshold:
            return self.incident_db[best_index]

        return None
#vectorstore
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class SimpleIncidentMemory:

    def __init__(self, memory_file="rag/incident_memory.json"):

        self.memory_file = memory_file

        # Load incident memory
        with open(memory_file, "r", encoding="utf-8") as f:
            self.memory = json.load(f)

        # Load embedding model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Convert descriptions → embeddings
        descriptions = [incident["description"] for incident in self.memory]
        embeddings = self.model.encode(descriptions)

        self.embeddings = np.array(embeddings).astype("float32")

        # Build FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(self.embeddings)

    def retrieve_similar_incident(self, log_text: str):

        log_vector = self.model.encode([log_text]).astype("float32")

        distances, indices = self.index.search(log_vector, k=1)

        best_index = indices[0][0]
        best_distance = distances[0][0]

        similarity_score = 1 / (1 + best_distance)

        print(f"\nFAISS Similarity Score: {similarity_score:.4f}")

        if similarity_score < 0.45:
            return None

        return self.memory[best_index]

    def add_new_incident(self, incident_data):

        """
        Add new incident to memory + FAISS index
        """

        print("\n⚡ New incident detected. Adding to memory...")

        # Append to memory
        self.memory.append(incident_data)

        # Save to JSON
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

        # Create embedding for new incident
        new_vector = self.model.encode([incident_data["description"]]).astype("float32")

        # Add to FAISS index
        self.index.add(new_vector)

        print("✅ Incident added to vector memory.")
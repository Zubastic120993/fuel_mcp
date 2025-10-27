# fuel_mcp/rag/retriever.py
"""
Semantic retriever for ASTM/ISO tables.
Searches vector_store.json for the most relevant table by meaning.
"""

import json
import numpy as np
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


MODEL = "text-embedding-3-small"
RAG_DIR = Path(__file__).parent
VECTOR_FILE = RAG_DIR / "vector_store.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# =====================================================
# 🔹 Utility: cosine similarity
# =====================================================
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# =====================================================
# 🔹 Load vector store
# =====================================================
with open(VECTOR_FILE, "r") as f:
    VECTOR_STORE = json.load(f)

# =====================================================
# 🔹 Core search
# =====================================================
def search_table(query: str, top_k: int = 3):
    """Return top-k most relevant tables for a natural-language query."""
    # 1️⃣ Embed the query
    resp = client.embeddings.create(model=MODEL, input=query)
    query_vec = resp.data[0].embedding

    # 2️⃣ Compute similarities
    results = []
    for key, entry in VECTOR_STORE.items():
        sim = cosine_similarity(query_vec, entry["embedding"])
        results.append({
            "table": key,
            "similarity": round(float(sim), 4),
            "description": entry["description"],
            "category": entry["category"]
        })

    # 3️⃣ Sort and return
    results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]

# =====================================================
# 🔹 CLI demo
# =====================================================
if __name__ == "__main__":
    print("🔎 ASTM/ISO Table Retriever\n")
    while True:
        query = input("Enter query (or 'exit'): ").strip()
        if query.lower() == "exit":
            break

        hits = search_table(query)
        for h in hits:
            print(f"\n📄 {h['table']} — {h['description']}")
            print(f"   🔹 Similarity: {h['similarity']}")
        print("-" * 60)

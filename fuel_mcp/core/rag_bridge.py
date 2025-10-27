
# fuel_mcp/core/rag_bridge.py
"""
Bridge between MCP Core and the RAG semantic layer.
Lets MCP auto-discover the right ASTM/ISO table by meaning.
"""

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json
import numpy as np
import os

load_dotenv()

MODEL = "text-embedding-3-small"
RAG_DIR = Path(__file__).parent.parent / "rag"
VECTOR_FILE = RAG_DIR / "vector_store.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =====================================================
# 🔹 Cosine similarity helper
# =====================================================
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# =====================================================
# 🔹 Load the vector store once
# =====================================================
with open(VECTOR_FILE, "r") as f:
    VECTOR_STORE = json.load(f)

# =====================================================
# 🔹 Semantic table resolver
# =====================================================
def find_table_for_query(query: str, top_k: int = 1):
    """Return the most relevant ASTM/ISO table(s) for a conversion query."""
    resp = client.embeddings.create(model=MODEL, input=query)
    qvec = resp.data[0].embedding

    scored = []
    for key, entry in VECTOR_STORE.items():
        score = cosine_similarity(qvec, entry["embedding"])
        scored.append({
            "table": key,
            "similarity": round(float(score), 4),
            "description": entry.get("description", ""),
            "category": entry.get("category", "")
        })

    scored = sorted(scored, key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]

# =====================================================
# 🔹 Demo
# =====================================================
if __name__ == "__main__":
    print("🔍 RAG-powered Table Resolver\n")
    while True:
        q = input("Enter a query (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        for hit in find_table_for_query(q, top_k=3):
            print(f"\n📘 {hit['table']}")
            print(f"   🔹 Similarity: {hit['similarity']}")
            if hit['description']:
                print(f"   📝 {hit['description']}")
        print("-" * 60)

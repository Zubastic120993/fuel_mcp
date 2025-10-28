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
import requests
import logging
from datetime import datetime, UTC
from sentence_transformers import SentenceTransformer

# =====================================================
# 🌐 Environment & Constants
# =====================================================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-3-small"

RAG_DIR = Path(__file__).parent.parent / "rag"
VECTOR_FILE = RAG_DIR / "vector_store.json"
VECTOR_STORE_PATH = VECTOR_FILE  # for reuse

# =====================================================
# 🌐 Online / Offline Detection
# =====================================================
def is_internet_available(url="https://api.openai.com/v1/embeddings", timeout=3) -> bool:
    """
    Quick check to confirm online API accessibility.
    Returns False if no internet or invalid API key.
    """
    try:
        if not OPENAI_API_KEY:
            return False
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            timeout=timeout,
        )
        # 401 = bad key, 200/404 = reachable endpoint
        return response.status_code in (200, 401, 404)
    except Exception:
        return False


ONLINE_MODE = is_internet_available()

if ONLINE_MODE:
    print("🌐 Online mode detected — using OpenAI embeddings.")
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("🛰️ Offline mode active — using local vector_store.json.")
    client = None

# =====================================================
# 🧠 Dynamic RAG Fallback Logic with Structured Logging
# =====================================================
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
RAG_LOG = LOG_DIR / "rag_activity.json"

def log_rag_event(event_type: str, detail: str):
    """Append structured RAG event to JSON log."""
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "event": event_type,
        "detail": detail,
        "mode": "online" if ONLINE_MODE else "offline"
    }
    try:
        existing = json.load(open(RAG_LOG)) if RAG_LOG.exists() else []
    except Exception:
        existing = []
    existing.append(entry)
    with open(RAG_LOG, "w") as f:
        json.dump(existing[-100:], f, indent=2)  # keep last 100 entries

# =====================================================
# 💾 Offline Vector Search (NumPy-based)
# =====================================================
def load_local_vector_store():
    """
    Load local vector store and normalize its format.
    Supports both dict-based and list-based structures.
    """
    if not VECTOR_STORE_PATH.exists():
        print("⚠️  No local vector_store.json found.")
        return []

    try:
        with open(VECTOR_STORE_PATH, "r") as f:
            data = json.load(f)

        # If data is a dict → convert to list[dict]
        if isinstance(data, dict):
            data = [
                {
                    "table": key,
                    **val,
                }
                for key, val in data.items()
            ]
        return data

    except Exception as e:
        print(f"❌ Failed to load local vector store: {e}")
        return []

# =====================================================
# 🧠 Local Semantic Embedder
# =====================================================
try:
    LOCAL_EMBEDDER = SentenceTransformer(
        "nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True,  # ✅ Required for Nomic models
    )
    print("✅ Loaded local semantic model: nomic-ai/nomic-embed-text-v1.5")
except Exception as e:
    LOCAL_EMBEDDER = None
    print(f"⚠️ Could not load local embedding model: {e}")

def embed_query_offline(query: str) -> np.ndarray:
    """
    Generate a true semantic embedding using a local model.
    Returns 1536-D vector comparable to OpenAI embeddings.
    """
    if LOCAL_EMBEDDER is None:
        # Fallback deterministic pseudo-embedding (if model missing)
        print("⚠️ Using fallback pseudo-embedding.")
        vector = np.zeros(1536)
        for i, c in enumerate(query.lower()):
            vector[i % 1536] += ord(c)
        norm = np.linalg.norm(vector)
        return vector / norm if norm != 0 else vector

    emb = LOCAL_EMBEDDER.encode(query, normalize_embeddings=True)
    return np.array(emb, dtype=np.float32)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def find_table_offline(query: str, top_k: int = 3) -> list[dict]:
    """Offline semantic search using precomputed embeddings in vector_store.json."""
    store = load_local_vector_store()
    if not store:
        print("⚠️ Empty or missing local vector store.")
        return []

    q_vec = embed_query_offline(query)
    scored = []
    for entry in store:
        emb = np.array(entry.get("embedding", []))
        if len(emb) == 0:
            continue
        score = cosine_similarity(q_vec, emb)
        scored.append(
            {
                "table": entry.get("table", "unknown"),
                "similarity": round(score, 4),
                "description": entry.get("description", ""),
                "category": entry.get("category", ""),
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]

# =====================================================
# 🌐 Online Table Finder
# =====================================================
def find_table_online(query: str, top_k: int = 3) -> list[dict]:
    """Online embedding-based search using OpenAI."""
    with open(VECTOR_FILE, "r") as f:
        vector_store = json.load(f)

    resp = client.embeddings.create(model=MODEL, input=query)
    qvec = resp.data[0].embedding

    scored = []
    for key, entry in vector_store.items():
        score = cosine_similarity(qvec, entry["embedding"])
        scored.append(
            {
                "table": key,
                "similarity": round(float(score), 4),
                "description": entry.get("description", ""),
                "category": entry.get("category", ""),
            }
        )

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]

# =====================================================
# 🧠 Unified Entry Point (Auto-fallback)
# =====================================================
def find_table_for_query(query: str, top_k: int = 3) -> list[dict]:
    """
    Unified table resolver with automatic online/offline switching.
    Tries OpenAI first; falls back to offline NumPy RAG on failure.
    """
    global ONLINE_MODE
    if ONLINE_MODE:
        try:
            results = find_table_online(query, top_k)
            log_rag_event("query_success", f"Online RAG resolved: {query}")
            return results
        except Exception as e:
            log_rag_event("query_fail", f"Online RAG failed: {type(e).__name__}")
            print("⚠️ Online RAG failed — switching to offline mode.")
            ONLINE_MODE = False
            return find_table_offline(query, top_k)
    else:
        results = find_table_offline(query, top_k)
        log_rag_event("query_offline", f"Offline RAG handled: {query}")
        return results

# =====================================================
# 🧪 CLI Demo
# =====================================================
if __name__ == "__main__":
    print("🔍 RAG-powered Table Resolver\n")
    while True:
        q = input("Enter a query (or 'exit'): ").strip()
        if q.lower() == "exit":
            break
        results = find_table_for_query(q, top_k=3)
        for hit in results:
            print(f"\n📘 {hit['table']}")
            print(f"   🔹 Similarity: {hit['similarity']}")
            if hit.get("description"):
                print(f"   📝 {hit['description']}")
        print("-" * 60)

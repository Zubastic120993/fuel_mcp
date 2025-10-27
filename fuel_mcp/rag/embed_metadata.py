# fuel_mcp/rag/embed_metadata.py
import json
import os
from pathlib import Path
from openai import OpenAI
from time import sleep
from dotenv import load_dotenv

# 🔹 Load environment variables from .env
load_dotenv()

# =====================================================
# ⚙️ Configuration
# =====================================================
MODEL = "text-embedding-3-small"
RAG_DIR = Path(__file__).parent
METADATA_FILE = RAG_DIR / "metadata.json"
VECTOR_FILE = RAG_DIR / "vector_store.json"
MAX_RETRIES = 3
TIMEOUT = 30.0

# 🔹 Initialize OpenAI client with timeout
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=TIMEOUT
)

# =====================================================
# 🧩 Load metadata
# =====================================================
with open(METADATA_FILE, "r") as f:
    metadata = json.load(f)

# Resume support: load existing embeddings if file exists
vector_store = {}
if VECTOR_FILE.exists():
    try:
        with open(VECTOR_FILE, "r") as f:
            vector_store = json.load(f)
        print(f"🔁 Resuming from {len(vector_store)} existing embeddings...")
    except Exception:
        print("⚠️ Could not read existing vector_store.json — starting fresh.")

# =====================================================
# 🚀 Embedding builder with retry logic
# =====================================================
def get_embedding_with_retry(text, key, max_retries=MAX_RETRIES):
    """Get embedding with exponential backoff retry"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"🔄 Requesting embedding for: {key} (attempt {attempt}/{max_retries})...")
            response = client.embeddings.create(model=MODEL, input=text)
            print(f"📥 Received response for: {key}")
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for {key}: {e}")
            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                print(f"⏳ Retrying in {wait_time} seconds...")
                sleep(wait_time)
            else:
                print(f"❌ All retries exhausted for {key}")
                raise

def embed_metadata():
    total = len(metadata)
    count = 0

    print(f"\n🚀 Embedding {total} metadata entries...\n")

    for key, content in metadata.items():
        if key in vector_store:
            print(f"⏩ Skipped (already embedded): {key}")
            continue

        desc = content.get("description") or content.get("purpose") or "No description available."
        category = content.get("category", "uncategorized")
        text = f"{key}: {desc}"
        
        try:
            embedding = get_embedding_with_retry(text, key)

            vector_store[key] = {
                "embedding": embedding,
                "description": desc,
                "category": category,
            }

            count += 1
            print(f"✅ ({len(vector_store)}/{total}) Embedded: {key}\n")

            # Auto-save every 5 items
            if count % 5 == 0:
                with open(VECTOR_FILE, "w") as f:
                    json.dump(vector_store, f, indent=2)
                print(f"💾 Progress saved ({len(vector_store)}/{total})\n")
            
            # Rate limit protection
            sleep(0.5)

        except Exception as e:
            print(f"❌ Skipping {key} after all retries failed: {e}\n")
            # Save progress even on failure
            with open(VECTOR_FILE, "w") as f:
                json.dump(vector_store, f, indent=2)
            continue

    # Final save
    with open(VECTOR_FILE, "w") as f:
        json.dump(vector_store, f, indent=2)
    print(f"\n✅ Done — embedded {len(vector_store)} total → {VECTOR_FILE}")

# =====================================================
if __name__ == "__main__":
    embed_metadata()
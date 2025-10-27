# fuel_mcp/core/mcp_core.py
"""
MCP Core Integration with RAG and Conversion Engine
---------------------------------------------------
This connects the semantic retriever (RAG) with the conversion engine.
MCP can now interpret natural language queries, find the right table,
and execute the appropriate conversion.
"""

from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import json
import os
from datetime import datetime, UTC
timestamp = datetime.now(UTC).isoformat()

from fuel_mcp.core.conversion_dispatcher import convert
from fuel_mcp.core.rag_bridge import find_table_for_query

load_dotenv()

# -----------------------------------------------------
# 🗂️ Storage for conversation / query history
# -----------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "conversion_history.json"

# -----------------------------------------------------
# 🧠 Main dispatcher
# -----------------------------------------------------
def query_mcp(query: str) -> dict:
    """
    Accepts a natural-language conversion query, automatically
    finds the right table via RAG, performs the calculation,
    and logs the result.
    """

    print(f"\n🧩 MCP query received → {query}")

    # 1️⃣ Ask RAG which table is most relevant
    candidates = find_table_for_query(query, top_k=3)
    top = candidates[0]
    print(f"🔍 Selected table: {top['table']} (similarity={top['similarity']})")

    # 2️⃣ Infer operation type based on the query
    ctype = None
    if "density" in query and "ton" in query:
        ctype = "density_to_mass"
    elif "density" in query and "volume" in query:
        ctype = "density_to_volume"
    elif "vacuo" in query or "air" in query or "correction" in query:
        ctype = "air_correction"

    if not ctype:
        raise ValueError("❌ Could not infer conversion type from query")

    # 3️⃣ Extract numeric value (basic)
    import re
    match = re.search(r"(\d+(?:\.\d+)?)", query)
    if not match:
        raise ValueError("❌ No numeric value found in query")
    value = float(match.group(1))

    # 4️⃣ Perform conversion
    result = convert(ctype, value)
    result["_meta"] = {
        "query": query,
        "selected_table": top["table"],
        "similarity": top["similarity"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # 5️⃣ Log history
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.load(open(HISTORY_FILE))
        except Exception:
            history = []
    history.append(result)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print("✅ Conversion complete.\n")
    return result

# -----------------------------------------------------
# 🧪 Manual test
# -----------------------------------------------------
if __name__ == "__main__":
    tests = [
        "convert density 15C 980 to long tons",
        "get correction factor for 850 kg/m³ fuel",
    ]
    for q in tests:
        print(query_mcp(q))

"""
MCP Core Integration with RAG and Conversion Engine
---------------------------------------------------
This connects the semantic retriever (RAG) with the conversion engine.
MCP interprets natural language queries, finds the relevant table,
and performs the proper conversion (density, mass, volume, etc.).
"""

import json
import os
import re
import logging
from datetime import datetime, UTC
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from fuel_mcp.core.conversion_dispatcher import convert
from fuel_mcp.core.rag_bridge import find_table_for_query

# =====================================================
# 🔧 Environment setup
# =====================================================
load_dotenv()

# =====================================================
# 🧭 Logging configuration
# =====================================================
Path("logs").mkdir(exist_ok=True)

rotating_handler = RotatingFileHandler(
    "logs/mcp_queries.log", maxBytes=1_000_000, backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[rotating_handler, logging.StreamHandler()],
)

# -----------------------------------------------------
# 🗂️ Storage for conversion history
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
    logging.info(f"🧩 MCP query started: {query}")

    # 1️⃣ Ask RAG which table is most relevant
    candidates = find_table_for_query(query, top_k=3)
    top = candidates[0]
    logging.info(f"🔍 Selected table: {top['table']} (similarity={top['similarity']})")

    # 2️⃣ Infer operation type based on the query
    ctype = None
    q_lower = query.lower()
    if "density" in q_lower and "ton" in q_lower:
        ctype = "density_to_mass"
    elif "density" in q_lower and "volume" in q_lower:
        ctype = "density_to_volume"
    elif "vacuo" in q_lower or "air" in q_lower or "correction" in q_lower:
        ctype = "air_correction"

    if not ctype:
        raise ValueError("❌ Could not infer conversion type from query")

    # 3️⃣ Extract numeric value (basic)
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
        "timestamp": datetime.now(UTC).isoformat(),
    }

    # 5️⃣ Save history
    try:
        history = json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else []
    except Exception:
        history = []

    history.append(result)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    logging.info(f"✅ Conversion complete: {result}")
    return result


# -----------------------------------------------------
# 🧪 Manual test
# -----------------------------------------------------
if __name__ == "__main__":
    tests = [
        "convert density 850 to ton at 25C",
        "get correction factor for 980 kg/m³ fuel",
    ]
    for q in tests:
        print(query_mcp(q))

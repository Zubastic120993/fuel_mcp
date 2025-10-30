"""
fuel_mcp/core/mcp_core.py
=========================

MCP Core Integration with RAG, Conversion, and VCF Engines
----------------------------------------------------------
Connects the semantic retriever (RAG) with the conversion and VCF engines.
Interprets natural-language queries, determines the appropriate ASTM/ISO
table, performs conversions or analytical corrections, and logs results
directly to SQLite (mcp_history.db).
"""

import re
import logging
from datetime import datetime, UTC
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

from fuel_mcp.core.conversion_dispatcher import convert
from fuel_mcp.core.rag_bridge import find_table_for_query
from fuel_mcp.core.vcf_official_full import vcf_iso_official
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.core.db_logger import init_db, log_query, log_error as log_error_db

# =====================================================
# 🔧 Environment setup
# =====================================================
load_dotenv()
init_db()  # ensure DB tables exist before logging anything

# =====================================================
# 🧭 Logging configuration
# =====================================================
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
rotating_handler = RotatingFileHandler(LOG_DIR / "mcp_queries.log", maxBytes=1_000_000, backupCount=5)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[rotating_handler, logging.StreamHandler()],
)

# -----------------------------------------------------
# 📦 Default densities by product name
# -----------------------------------------------------
PRODUCT_DEFAULT_DENSITY = [
    (["hfo", "heavy fuel oil", "ifo180", "ifo380", "marine fuel oil"], 980.0),
    (["diesel", "gasoil", "ago"], 840.0),
    (["gasoline", "petrol"], 740.0),
    (["jet a", "jet a1", "kerosene"], 800.0),
    (["lpg"], 540.0),
]


def try_infer_density_from_product(q_lower: str) -> float | None:
    """Infer default density when none provided."""
    for synonyms, rho in PRODUCT_DEFAULT_DENSITY:
        for name in synonyms:
            if name in q_lower:
                logging.info(f"ℹ️ Using default density {rho} kg/m³ inferred from '{name}'")
                return rho
    return None


# -----------------------------------------------------
# 🧠 Main Dispatcher
# -----------------------------------------------------
def query_mcp(query: str) -> dict:
    """
    Unified MCP query processor.
    Detects operation type (VCF, density_to_mass, etc.),
    extracts temperature/density, runs analytical logic,
    and logs results directly to SQLite (no JSON history).
    """
    logging.info(f"🧩 MCP query started: {query}")
    q_lower = query.lower().replace("℃", "°c").replace("kg/m3", "kg/m³")

    try:
        # 1️⃣ Detect operation type
        if any(k in q_lower for k in ["vcf", "volume correction", "correction factor", "temperature correction"]):
            op_type = "vcf"
        elif "density" in q_lower and "ton" in q_lower:
            op_type = "density_to_mass"
        elif "density" in q_lower and "volume" in q_lower:
            op_type = "density_to_volume"
        else:
            raise ValueError("❌ Could not infer conversion type from query")

        # 2️⃣ Extract numeric values
        temp_match = re.search(r"(-?\d+(?:\.\d+)?)\s*°?\s*c", q_lower)
        tempC = float(temp_match.group(1)) if temp_match else 15.0

        dens_match = re.search(r"(\d+(?:\.\d+)?)\s*kg\s*/\s*m(?:³|3)", q_lower)
        rho15 = float(dens_match.group(1)) if dens_match else try_infer_density_from_product(q_lower)
        if rho15 is None:
            raise ValueError("❌ No density found or inferable from query")

        # 3️⃣ Determine relevant ASTM/ISO table (RAG)
        candidates = find_table_for_query(query, top_k=1)
        selected_table = candidates[0]["table"] if candidates else "unknown"

        # 4️⃣ Perform analytical or conversion operation
        if op_type == "vcf":
            result = vcf_iso_official(rho15, tempC)
        else:
            result = convert(op_type, rho15)

        # 5️⃣ Attach metadata
        result["_meta"] = {
            "mode": op_type,
            "selected_table": selected_table,
            "query": query,
            "rho15": rho15,
            "tempC": tempC,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        # 6️⃣ Log success → SQLite only
        log_query(query, result, mode=op_type, success=True)
        logging.info(f"✅ Operation '{op_type}' completed successfully.")

        return result

    except Exception as e:
        # Structured + DB error logging
        log_error(e, query=query, module="mcp_core")
        log_error_db("mcp_core", str(e))
        logging.error(f"❌ MCP query failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "mode": "error",
            "timestamp": datetime.now(UTC).isoformat(),
        }


# -----------------------------------------------------
# 🧪 Manual Test
# -----------------------------------------------------
if __name__ == "__main__":
    tests = [
        "calculate VCF for diesel at 25°C",
        "get correction factor for heavy fuel oil at 30 °C",
        "convert density 850 kg/m³ to ton",
    ]
    for q in tests:
        print("\n🧠 Query:", q)
        print(query_mcp(q))
"""
MCP Core Integration with RAG, Conversion, and VCF Engines
----------------------------------------------------------
Connects the semantic retriever (RAG) with the conversion and VCF engines.
MCP interprets natural-language queries, finds the relevant ASTM/ISO table,
and performs either a density/mass/volume conversion or an analytical
temperature correction (VCF).
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
from fuel_mcp.core.vcf_official_full import vcf_iso_official
from fuel_mcp.core.error_handler import log_error

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
# 📦 Product default densities
# -----------------------------------------------------
PRODUCT_DEFAULT_DENSITY = [
    (["hfo", "heavy fuel oil", "ifo180", "ifo380", "marine fuel oil"], 980.0),
    (["diesel", "gasoil", "ago"], 840.0),
    (["gasoline", "petrol"], 740.0),
    (["jet a", "jet a1", "kerosene"], 800.0),
    (["lpg"], 540.0),
]

def try_infer_density_from_product(q_lower: str) -> float | None:
    """Infer default density from product name when not explicitly given."""
    for names, rho in PRODUCT_DEFAULT_DENSITY:
        for name in names:
            if name in q_lower:
                logging.info(f"ℹ️ Using default density {rho} kg/m³ inferred from product name '{name}'")
                return rho
    return None

# -----------------------------------------------------
# 🧠 Main dispatcher
# -----------------------------------------------------
def query_mcp(query: str) -> dict:
    """
    Unified MCP query processor.
    Automatically detects VCF, density, or volume operations,
    executes the correct analytical or semantic workflow,
    and logs structured results.
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
            op_type = "unknown"

        if op_type == "unknown":
            raise ValueError("❌ Could not infer conversion type from query")

        # 2️⃣ Extract numbers
        temp_match = re.search(r"(-?\d+(?:\.\d+)?)\s*°?\s*c", q_lower)
        tempC = float(temp_match.group(1)) if temp_match else 15.0

        dens_match = re.search(r"(\d+(?:\.\d+)?)\s*kg\s*/\s*m(?:³|3)", q_lower)
        rho15 = float(dens_match.group(1)) if dens_match else try_infer_density_from_product(q_lower)

        if rho15 is None:
            raise ValueError("❌ No density found or inferable from query")

        # 3️⃣ Perform operation
        if op_type == "vcf":
            result = vcf_iso_official(rho15, tempC)
            result["_meta"] = {
                "mode": "vcf_analytical",
                "query": query,
                "rho15": rho15,
                "tempC": tempC,
                "timestamp": datetime.now(UTC).isoformat(),
            }
            logging.info(f"✅ VCF computed successfully: {result.get('VCF', '?')}")
        else:
            result = convert(op_type, rho15)
            result["_meta"] = {
                "mode": op_type,
                "query": query,
                "rho15": rho15,
                "timestamp": datetime.now(UTC).isoformat(),
            }

        # 4️⃣ Save history
        try:
            history = json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else []
        except Exception:
            history = []
        history.append(result)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

        return result

    except Exception as e:
        log_error(e, query=query, module="mcp_core")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "mode": "error",
        }

# -----------------------------------------------------
# 🧪 Manual test
# -----------------------------------------------------
if __name__ == "__main__":
    tests = [
        "calculate VCF for diesel at 25°C",
        "get correction factor for heavy fuel oil at 30 °C",
        "convert density 850 kg/m³ to ton",
    ]
    for q in tests:
        print("\n🧠 Query:", q)
        print(json.dumps(query_mcp(q), indent=2))
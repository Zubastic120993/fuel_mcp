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
# 📦 Product default densities (opt-in heuristic)
# -----------------------------------------------------
# These defaults are typical values and may vary by spec/blend.
# They are used only when VCF is requested and no explicit density is provided.
PRODUCT_DEFAULT_DENSITY = [
    # (list of synonyms, default density kg/m³)
    (["heavy oil", "heavy fuel oil", "hfo", "ifo 180", "ifo180", "ifo 380", "ifo380", "marine fuel oil"], 980.0),
    (["diesel", "diesel fuel", "ago", "gasoil"], 840.0),
    (["gasoline", "petrol", "mogas"], 740.0),
    (["jet", "jet a", "jet a1", "jet-a", "jet-a1", "kerosene"], 800.0),
    (["marine fuel", "mfo", "residual fuel"], 990.0),
]

def try_infer_density_from_product(q_lower: str) -> float | None:
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
    Accepts a natural-language conversion query, automatically
    finds the right table via RAG, performs the calculation,
    and logs the result.
    """
    logging.info(f"🧩 MCP query started: {query}")

    # Normalize some unicode and unit variants early
    q_norm = (
        query.replace("°", " °")
             .replace("℃", " °C")
             .replace("kg/m3", "kg/m³")
    )
    q_lower = q_norm.lower()

    # 1️⃣ Ask RAG which table is most relevant
    candidates = find_table_for_query(query, top_k=3)
    top = candidates[0] if candidates else {"table": "unknown", "similarity": 0.0}
    logging.info(f"🔍 Selected table: {top['table']} (similarity={top['similarity']})")

    # 2️⃣ Infer operation type based on the query
    ctype = None
    # 🔍 Detect VCF or correction queries (case-insensitive)
    if any(keyword in q_lower for keyword in [
        "vcf", "volume correction", "temperature correction",
        "correction factor", "factor for", "get correction", "calculate vcf"
    ]):
        ctype = "vcf"
    elif "density" in q_lower and "ton" in q_lower:
        ctype = "density_to_mass"
    elif "density" in q_lower and "volume" in q_lower:
        ctype = "density_to_volume"
    elif any(word in q_lower for word in ["vacuo", "air", "correction factor"]):
        ctype = "air_correction"

    if not ctype:
        raise ValueError("❌ Could not infer conversion type from query")

    # 3️⃣ Extract parameters from the query (density and temperature)
    #    - Identify temperature by proximity to °C/C keywords
    #    - Identify density by proximity to density keywords or units
    density = None
    temp = None

    # Temperature extraction
    # Patterns: "25 °c", "25 c", "at 25 c", "temp 25", "25c", "25 degrees celsius"
    temp_match = re.search(r"(?:(?:at|temp(?:erature)?|t)\s*)?(-?\d+(?:\.\d+)?)\s*°?\s*c\b", q_lower)
    if temp_match:
        try:
            temp = float(temp_match.group(1))
        except ValueError:
            temp = None
    else:
        # Fallback: any number followed by "deg/degree(s) celsius"
        temp_match2 = re.search(r"(-?\d+(?:\.\d+)?)\s*(?:deg(?:rees?)?|degree(?:s)?)\s*celsius\b", q_lower)
        if temp_match2:
            try:
                temp = float(temp_match2.group(1))
            except ValueError:
                temp = None

    # Density extraction
    # Prioritize explicit units or "density" context
    # Examples: "density 850", "rho 980", "980 kg/m³", "980 kg/m3"
    dens_unit_match = re.search(r"(\d+(?:\.\d+)?)\s*kg\s*/\s*m(?:\u00B3|3)\b", q_lower)  # kg/m³ or kg/m3
    dens_word_match = re.search(r"(?:density|rho)\s*[:=]?\s*(\d+(?:\.\d+)?)\b", q_lower)

    if dens_unit_match:
        try:
            density = float(dens_unit_match.group(1))
        except ValueError:
            density = None
    elif dens_word_match:
        try:
            density = float(dens_word_match.group(1))
        except ValueError:
            density = None
    else:
        # As a last resort, inspect all numbers and disambiguate
        nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", q_lower)]
        if nums:
            if temp is not None:
                # Exclude identified temp; fuels typically 610–1164 kg/m³ (ASTM range)
                cand = [x for x in nums if x != temp]
                likely = [x for x in cand if 610.5 <= x <= 1164.0]
                density = likely[0] if likely else (cand[0] if cand else None)
            else:
                likely = [x for x in nums if 610.5 <= x <= 1164.0]
                density = likely[0] if likely else None

    # 4️⃣ Perform conversion or analytical VCF calculation
    if ctype == "vcf":
        if density is None:
            # Try to infer from product name as a last resort
            density = try_infer_density_from_product(q_lower)
            if density is None:
                raise ValueError(
                    "❌ No density found in the query for VCF calculation. "
                    "Please include density, e.g., 'calculate VCF for heavy oil with density 980 kg/m³ at 25°C'."
                )
        tempC = temp if temp is not None else 15.0
        result = vcf_iso_official(density, tempC)
        result["_meta"] = {
            "query": query,
            "selected_table": top["table"],
            "similarity": round(top["similarity"], 4),
            "timestamp": datetime.now(UTC).isoformat(),
            "mode": "vcf_analytical",
        }
        logging.info(f"✅ VCF computed: Table {result['table']} | VCF={result['VCF']:.6f}")

    else:
        if density is None:
            raise ValueError("❌ No density value found in query")
        result = convert(ctype, density)
        result["_meta"] = {
            "query": query,
            "selected_table": top["table"],
            "similarity": round(top["similarity"], 4),
            "timestamp": datetime.now(UTC).isoformat(),
            "mode": ctype,
        }
        logging.info(f"✅ Conversion complete ({ctype}): {result}")

    # 5️⃣ Save history
    try:
        history = json.load(open(HISTORY_FILE)) if HISTORY_FILE.exists() else []
    except Exception:
        history = []

    history.append(result)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return result


# -----------------------------------------------------
# 🧪 Manual test
# -----------------------------------------------------
if __name__ == "__main__":
    tests = [
        "convert density 850 to ton at 25C",
        "get correction factor for 980 kg/m³ fuel",
        "calculate VCF for heavy oil at 25°C",  # now uses default 980 unless explicit density provided
        # Try also: "calculate VCF for HFO at 25°C", "calculate VCF for diesel at 28 C"
        # Or explicit: "calculate VCF for heavy oil with density 980 kg/m³ at 25°C"
    ]
    for q in tests:
        print("\n🧠 Query:", q)
        print(query_mcp(q))
"""
fuel_mcp/core/regex_parser.py
=============================

Enhanced regex parser — integrates with dynamic fuel density loader,
supports reverse (mass→volume) conversion, alias normalization,
and robust temperature + free-text parsing.
"""

import re
from fuel_mcp.core.vcf_official_full import vcf_iso_official, auto_correct
from fuel_mcp.core.fuel_density_loader import get_fuel_density


# =====================================================
# 🛢️ Alias Normalization
# =====================================================
def normalize_fuel_name(raw: str | None) -> str | None:
    """Normalize common aliases like 'mgo', 'heavy oil', etc."""
    if not raw:
        return None
    raw = raw.lower().strip()

    aliases = {
        "mgo": "diesel",
        "mdo": "diesel",
        "marine gas oil": "diesel",
        "marine diesel": "diesel",
        "light oil": "diesel",
        "gas oil": "diesel",
        "ifo": "hfo",
        "ifo380": "hfo",
        "intermediate fuel oil": "hfo",
        "heavy oil": "hfo",
        "heavy fuel": "hfo",
        "heavy fuel oil": "hfo",
        "residual fuel": "hfo",
    }
    return aliases.get(raw, raw)


# =====================================================
# 🔍 Query Parsing
# =====================================================
def parse_query(text: str):
    """Extract fuel, volume, mass, and temperature data from natural query text."""
    text_lower = text.lower().strip()
    result = {
        "fuel": None,
        "volume_l": None,
        "volume_m3": None,
        "mass_ton": None,
        "tempC": None,
        "mode": "unknown",
    }

    # --- detect fuel (multi-word safe, longest first) ---
    fuels = [
        "heavy fuel oil", "heavy fuel", "heavy oil",
        "intermediate fuel oil", "marine gas oil", "marine diesel", "light oil",
        "diesel", "gasoline", "hfo", "jet", "lube", "methanol",
        "mgo", "mdo", "ifo"
    ]
    for fuel in fuels:
        if re.search(rf"\b{re.escape(fuel)}\b", text_lower):
            result["fuel"] = normalize_fuel_name(fuel)
            break

    # --- detect temperature (robust for "25C", "25 C", "@25°C", "at 25 degrees", etc.) ---
    t_match = re.search(
        r"(?:@|at)?\s*(\d+(?:\.\d+)?)\s*(?:°\s*)?(?:c|deg(?:rees)?)\b",
        text_lower,
        re.IGNORECASE
    )
    if not t_match:
        # Fallback: just digits followed by optional ° and c
        t_match = re.search(r"(\d+(?:\.\d+)?)\s*°?\s*c\b", text_lower, re.IGNORECASE)

    if t_match:
        try:
            t_val = float(t_match.group(1))
            if -30 <= t_val <= 120:
                result["tempC"] = t_val
        except (ValueError, IndexError):
            pass

    # --- detect volume ---
    v_match = re.search(r"(\d+(?:\.\d+)?)\s*(l|litre|liter|m3|m³)", text_lower)
    if v_match:
        val = float(v_match.group(1))
        unit = v_match.group(2)
        if unit.startswith("l"):
            result["volume_l"] = val
            result["volume_m3"] = round(val / 1000, 3)
        else:
            result["volume_m3"] = val
            result["volume_l"] = round(val * 1000, 1)

    # --- detect mass ---
    m_match = re.search(r"(\d+(?:\.\d+)?)\s*(t|ton|tons|tonne|tonnes|kg)", text_lower)
    if m_match:
        val = float(m_match.group(1))
        unit = m_match.group(2)
        result["mass_ton"] = round(val / 1000, 3) if unit.startswith("k") else val
        result["mode"] = "reverse"

    # --- detect mode ---
    if "vcf" in text_lower or "correction" in text_lower:
        result["mode"] = "vcf"
    elif "convert" in text_lower or "mass" in text_lower:
        if result["mode"] != "reverse":
            result["mode"] = "convert"
    elif result["volume_m3"] and result["tempC"]:
        result["mode"] = "convert"

    return result


# =====================================================
# ⚙️ Query Processing
# =====================================================
def process_query(text: str):
    """Interpret and execute the parsed query."""
    parsed = parse_query(text)
    fuel = parsed["fuel"]
    tempC = parsed["tempC"]
    volume_m3 = parsed["volume_m3"]
    mass_ton = parsed["mass_ton"]

    if not fuel or tempC is None:
        return {"error": "Could not parse fuel or temperature from query."}

    try:
        rho15 = get_fuel_density(fuel)
    except ValueError as e:
        return {"error": str(e)}

    if parsed["mode"] == "vcf":
        result = vcf_iso_official(rho15, tempC)
        result.update({"fuel": fuel, "rho15": rho15, "mode": "vcf"})
        return result

    if parsed["mode"] == "convert" and volume_m3 is not None:
        result = auto_correct(fuel=fuel, volume_m3=volume_m3, tempC=tempC)
        result.update({"fuel": fuel, "rho15": rho15, "mode": "convert"})
        return result

    if parsed["mode"] == "reverse" and mass_ton is not None:
        result = auto_correct(fuel=fuel, mass_ton=mass_ton, tempC=tempC)
        result.update({"fuel": fuel, "rho15": rho15, "mode": "reverse"})
        return result

    return {"error": "Unsupported or unrecognized query type."}


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    samples = [
        "calculate VCF for heavy oil at 25C",
        "calculate VCF for heavy fuel at 25C",
        "calculate VCF for heavy fuel oil at 25C",
        "calculate VCF for marine gas oil at 25C",
        "calculate VCF for light oil at 25C",
        "convert 500 L diesel @ 30°C",
        "mass of 100 m3 methanol at 20°C",
        "convert 2 tons of diesel to m3 @ 25°C",
    ]
    for s in samples:
        print(f"{s} → {process_query(s)}")
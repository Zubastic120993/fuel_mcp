"""
fuel_mcp/core/regex_parser.py
=============================

Enhanced regex parser — integrates with dynamic fuel density loader
and auto_correct / vcf_iso_official depending on query intent.
"""

import re
from fuel_mcp.core.vcf_official_full import vcf_iso_official, auto_correct
from fuel_mcp.core.fuel_density_loader import get_fuel_density


def parse_query(text: str):
    """Extract fuel, volume, and temperature data from natural query text."""
    text = text.lower().strip()
    result = {
        "fuel": None,
        "volume_l": None,
        "volume_m3": None,
        "tempC": None,
        "mode": "unknown",
    }

    # --- detect fuel ---
    fuels = ["diesel", "gasoline", "hfo", "jet", "lube", "methanol"]
    for fuel in fuels:
        if fuel in text:
            result["fuel"] = fuel
            break

    # --- detect temperature (@ or at 25°C, etc.) ---
    t_match = re.search(r"(?:@|at)?\s*(\d+(\.\d+)?)\s*(°c|deg|degrees|c)", text)
    if t_match:
        result["tempC"] = float(t_match.group(1))

    # --- detect volume (L or m3) ---
    v_match = re.search(r"(\d+(\.\d+)?)\s*(l|litre|liter|m3|m³)", text)
    if v_match:
        val = float(v_match.group(1))
        unit = v_match.group(3)
        if unit.startswith("l"):
            result["volume_l"] = val
            result["volume_m3"] = round(val / 1000, 3)
        else:
            result["volume_m3"] = val
            result["volume_l"] = round(val * 1000, 1)

    # --- determine query mode ---
    if "vcf" in text or "correction" in text or "calculate vcf" in text:
        result["mode"] = "vcf"
    elif "convert" in text or "mass" in text:
        result["mode"] = "convert"

    return result


def process_query(text: str):
    """Interpret and execute the parsed query."""
    parsed = parse_query(text)
    fuel = parsed["fuel"]
    tempC = parsed["tempC"]
    volume_m3 = parsed["volume_m3"]

    if not fuel or not tempC:
        return {"error": "Could not parse fuel or temperature from query."}

    rho15 = get_fuel_density(fuel)

    if parsed["mode"] == "vcf":
        result = vcf_iso_official(rho15, tempC)
        result["fuel"] = fuel
        result["rho15"] = rho15
        result["mode"] = "vcf"
        return result

    if parsed["mode"] == "convert":
        if volume_m3 is None:
            return {"error": "Missing volume for conversion mode."}
        result = auto_correct(fuel=fuel, volume_m3=volume_m3, tempC=tempC)
        result["fuel"] = fuel
        result["rho15"] = rho15
        result["mode"] = "convert"
        return result

    return {"error": "Unsupported or unrecognized query type."}


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    samples = [
        "convert 500 L diesel @ 30°C",
        "calculate VCF for HFO at 25 degrees",
        "mass of 100 m3 methanol at 20°C",
    ]
    for s in samples:
        print(f"{s} → {process_query(s)}")
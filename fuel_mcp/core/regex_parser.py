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


def normalize_fuel_name(raw: str | None) -> str | None:
    """Normalize fuel aliases like 'mgo', 'mdo', 'ifo' → standard."""
    if not raw:
        return None
    raw = raw.lower()
    aliases = {
        "mgo": "diesel",
        "mdo": "diesel",
        "marine gas oil": "diesel",
        "ifo": "hfo",
        "intermediate fuel oil": "hfo",
        "gas oil": "diesel",
    }
    return aliases.get(raw, raw)


def parse_query(text: str):
    """Extract fuel, volume, mass, and temperature data from natural query text."""
    text = text.lower().strip()
    result = {
        "fuel": None,
        "volume_l": None,
        "volume_m3": None,
        "mass_ton": None,
        "tempC": None,
        "mode": "unknown",
    }

    # --- detect fuel ---
    fuels = ["diesel", "gasoline", "hfo", "jet", "lube", "methanol", "mgo", "mdo", "ifo"]
    for fuel in fuels:
        if fuel in text:
            result["fuel"] = normalize_fuel_name(fuel)
            break

    # --- detect temperature ---
    t_match = re.search(
        r"(?:@|at)?\s*(\d+(?:\.\d+)?)\s*(?:°?\s*c|deg(?:rees)?|degrees|c)\b",
        text,
    )
    if not t_match:
        t_match = re.search(r"(\d+(?:\.\d+)?)(?:\s*°?\s*c|deg(?:rees)?)", text)

    if t_match:
        try:
            t_val = float(t_match.group(1))
            if -30 <= t_val <= 120:
                result["tempC"] = t_val
        except ValueError:
            pass

    # --- detect volume ---
    v_match = re.search(r"(\d+(?:\.\d+)?)\s*(l|litre|liter|m3|m³)", text)
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
    m_match = re.search(r"(\d+(?:\.\d+)?)\s*(t|ton|tons|tonne|tonnes|kg)", text)
    if m_match:
        val = float(m_match.group(1))
        unit = m_match.group(2)
        if unit.startswith("k"):
            result["mass_ton"] = round(val / 1000, 3)
        else:
            result["mass_ton"] = val
        result["mode"] = "reverse"

    # --- detect mode ---
    if "vcf" in text or "correction" in text or "calculate vcf" in text:
        result["mode"] = "vcf"
    elif "convert" in text or "mass" in text:
        if result["mode"] != "reverse":
            result["mode"] = "convert"
    elif result["volume_m3"] and result["tempC"]:
        # fallback: no explicit keyword but both values known
        result["mode"] = "convert"

    return result


def process_query(text: str):
    """Interpret and execute the parsed query."""
    parsed = parse_query(text)
    fuel = parsed["fuel"]
    tempC = parsed["tempC"]
    volume_m3 = parsed["volume_m3"]
    mass_ton = parsed["mass_ton"]

    if not fuel or tempC is None:
        return {"error": "Could not parse fuel or temperature from query."}

    rho15 = get_fuel_density(fuel)

    # --- Case 1: VCF ---
    if parsed["mode"] == "vcf":
        result = vcf_iso_official(rho15, tempC)
        result.update({"fuel": fuel, "rho15": rho15, "mode": "vcf"})
        return result

    # --- Case 2: Volume → Mass ---
    if parsed["mode"] == "convert" and volume_m3 is not None:
        result = auto_correct(fuel=fuel, volume_m3=volume_m3, tempC=tempC)
        result.update({"fuel": fuel, "rho15": rho15, "mode": "convert"})
        return result

    # --- Case 3: Mass → Volume ---
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
        "convert 500 L diesel @ 30°C",
        "calculate VCF for HFO at 25 degrees",
        "mass of 100 m3 methanol at 20°C",
        "convert 2 tons of diesel to m3 @ 25°C",
        "mass of diesel 50°C 10m³",
        "diesel 20c 500l",
        "10 m³ hfo at 30 degrees",
        "convert 2 ton diesel 25C",
        "mgo 35deg 200l",
    ]
    for s in samples:
        print(f"{s} → {process_query(s)}")
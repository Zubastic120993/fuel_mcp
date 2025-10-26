
"""
vcf_official_full.py
=====================
Exact ISO 91-1 / ASTM D1250 / API 2540 computational method for
Tables 54A–54D (metric, °C system).

Implements:
    a = (K0 + K1 * ρ15) / ρ15²
    b = −a * ΔT * (1 + 0.8 * a * ΔT)
    VCF = exp(b)

Special case (770 ≤ ρ < 778):
    c = −0.00336312 + 2680.32 / ρ15²
    d = −c * ΔT * (1 + 0.8 * c * ΔT)
    VCF = exp(d)
"""

import math
import json
from pathlib import Path

# =====================================================
# 🔹  OFFICIAL COEFFICIENTS (ISO 91-1 Annex B)
# =====================================================
VCF_TABLES = {
    "54A": {"K0": 613.9723, "K1": 0.0, "range": (610.5, 1075.0)},          # Distillates
    "54B": [
        {"range": (653.0, 770.0), "K0": 346.4228, "K1": 0.4388},           # Gasoline
        {"range": (770.5, 787.5), "A": -0.00336312, "B": 2680.3206},       # Transition
        {"range": (788.0, 838.5), "K0": 594.5418, "K1": 0.0},              # Jet fuels
        {"range": (839.0, 1075.0), "K0": 186.9696, "K1": 0.48618},         # Residual fuels
    ],
    "54D": {"K0": 0.0, "K1": 0.6278, "range": (800.0, 1164.0)},            # Lubricating oils
}


# =====================================================
# 🔹  CORE FUNCTION
# =====================================================
def vcf_iso_official(rho15: float, tempC: float) -> dict:
    """
    Compute Volume Correction Factor (VCF) for a given density and temperature.
    Reproduces official printed ISO 91-1 / ASTM D1250 tables.
    :param rho15: density at 15 °C [kg/m³]
    :param tempC: observed temperature [°C]
    :return: dict with VCF and calculation details
    """

    dT = tempC - 15.0

    # ---- Determine applicable table ----
    if 800 <= rho15 <= 1164:
        table = "54D"
    elif 653 <= rho15 <= 1075:
        table = "54B"
    else:
        table = "54A"

    # ---- Perform calculation ----
    if table == "54A":
        k0, k1 = VCF_TABLES["54A"]["K0"], VCF_TABLES["54A"]["K1"]
        a = (k0 + k1 * rho15) / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)

    elif table == "54D":
        k0, k1 = VCF_TABLES["54D"]["K0"], VCF_TABLES["54D"]["K1"]
        a = (k0 + k1 * rho15) / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)

    elif table == "54B":
        # find sub-range
        selected = None
        for seg in VCF_TABLES["54B"]:
            lo, hi = seg["range"]
            if lo <= rho15 < hi:
                selected = seg
                break
        if selected is None:
            raise ValueError(f"Density {rho15} kg/m³ not in any 54B range")

        if "K0" in selected:
            k0, k1 = selected["K0"], selected["K1"]
            a = (k0 + k1 * rho15) / (rho15 ** 2)
            b = -a * dT * (1 + 0.8 * a * dT)
            vcf = math.exp(b)
        else:
            # transition band (770 – 778 kg/m³)
            A, B = selected["A"], selected["B"]
            c = A + B / (rho15 ** 2)
            d = -c * dT * (1 + 0.8 * c * dT)
            vcf = math.exp(d)
            a, b = c, d  # for reference output

    else:
        raise ValueError("Unsupported table")

    return {
        "table": table,
        "rho15": round(rho15, 3),
        "tempC": round(tempC, 2),
        "deltaT": round(dT, 2),
        "a_or_c": round(a, 9),
        "b_or_d": round(b, 8),
        "VCF": round(vcf, 6),
    }


# =====================================================
# 🔹  VOLUME-CORRECTION WRAPPER
# =====================================================
def correct_volume(fuel: str, observed_m3: float, tempC: float,
                   db_path: str | None = None) -> dict:
    """
    Correct observed fuel volume to 15 °C using the official algorithm.
    Automatically loads density database from package tables.
    """
    # 🔹 If path not given, use the internal MCP data file
    if db_path is None:
        db_path = Path(__file__).parent / "tables" / "fuel_data.json"

    # Read densities at 15 °C
    with open(db_path) as f:
        fuels = json.load(f)

    rho15 = fuels[fuel]["density_15C"]
    result = vcf_iso_official(rho15, tempC)
    result["fuel"] = fuel
    result["observed_m3"] = observed_m3
    result["V15_m3"] = round(observed_m3 * result["VCF"], 3)
    return result

# =====================================================
# 🔹  MASS → VOLUME CALCULATION
# =====================================================
def correct_mass(fuel: str, mass_ton: float, tempC: float,
                 db_path: str | None = None) -> dict:
    """
    Given mass (t), fuel type, and observed temperature (°C),
    compute:
      - Volume at observed temperature (m³)
      - Volume at 15 °C (m³, reference)
    """
    from pathlib import Path

    if db_path is None:
        db_path = Path(__file__).parent / "tables" / "fuel_data.json"

    # Load density data
    with open(db_path) as f:
        fuels = json.load(f)

    rho15 = fuels[fuel]["density_15C"]  # kg/m³ @15°C
    rho15_ton_m3 = rho15 / 1000          # ton/m³

    # 1️⃣ Get the correction factor
    result = vcf_iso_official(rho15, tempC)
    vcf = result["VCF"]

    # 2️⃣ Density at observed temperature
    rhoT_ton_m3 = rho15_ton_m3 * vcf

    # 3️⃣ Compute volumes
    volume_obs_m3 = mass_ton / rhoT_ton_m3
    volume_15_m3 = volume_obs_m3 * vcf

    # 4️⃣ Return all results
    result.update({
        "fuel": fuel,
        "mass_ton": mass_ton,
        "rhoT_ton_m3": round(rhoT_ton_m3, 6),
        "volume_obs_m3": round(volume_obs_m3, 3),
        "V15_m3": round(volume_15_m3, 3),
    })
    return result

# =====================================================
# 🔹  UNIVERSAL AUTO-DETECT FUNCTION
# =====================================================
def auto_correct(
    fuel: str,
    volume_m3: float | None = None,
    mass_ton: float | None = None,
    tempC: float | None = None,
    db_path: str | None = None
) -> dict:
    """
    Automatically detects whether to perform:
      - Volume → Mass (if volume given)
      - Mass → Volume (if mass given)
    Returns detailed results dictionary.
    """
    if tempC is None:
        raise ValueError("Temperature (°C) must be provided.")

    # Volume → Mass path
    if volume_m3 is not None and mass_ton is None:
        result = correct_volume(fuel, volume_m3, tempC, db_path)
        result["mode"] = "volume_to_mass"
        return result

    # Mass → Volume path
    elif mass_ton is not None and volume_m3 is None:
        result = correct_mass(fuel, mass_ton, tempC, db_path)
        result["mode"] = "mass_to_volume"
        return result

    else:
        raise ValueError("Provide either volume_m3 or mass_ton, not both.")


# =====================================================
# 🔹  DEMONSTRATION
# =====================================================
if __name__ == "__main__":
    # Example density database
    FUEL_DATA = {
        "diesel": {"density_15C": 850.0},
        "hfo": {"density_15C": 980.0},
        "jet": {"density_15C": 800.0},
        "lube": {"density_15C": 910.0},
        "gasoline": {"density_15C": 740.0},
    }
    with open("fuel_data.json", "w") as f:
        json.dump(FUEL_DATA, f, indent=2)

    # Example test run
    print("ISO 91-1 / ASTM D1250 VCF CALCULATOR\n")
    for fuel in FUEL_DATA:
        res = correct_volume(fuel, 1000, 56)
        print(f"{res['fuel'].upper():10s} | Table {res['table']} | "
              f"ρ₁₅={res['rho15']} kg/m³ | ΔT={res['deltaT']}°C | "
              f"VCF={res['VCF']} | V15={res['V15_m3']} m³")

"""
vcf_official_full.py
=====================
Exact ISO 91-1 / ASTM D1250 / API 2540 computational method for
Tables 54A–54D (metric, °C system).
"""

import math
import json
from pathlib import Path
from .unit_converter import convert


# =====================================================
# 🔹 OFFICIAL COEFFICIENTS (ISO 91-1:2019 Annex B)
# =====================================================
VCF_TABLES = {
    "54A": {"K0": 613.9723, "K1": 0.0, "range": (610.5, 770.0),
            "label": "Light distillates (gasoline / naphtha)"},
    "54B": [
        {"range": (770.5, 787.5), "A": -0.00336312, "B": 2680.3206, "label": "Transition band"},
        {"range": (787.5, 838.5), "K0": 594.5418, "K1": 0.0, "label": "Jet / Kerosene"},
        {"range": (838.5, 1075.0), "K0": 186.9696, "K1": 0.48618, "label": "Residual / Marine fuels"},
    ],
    "54D": {"K0": 0.0, "K1": 0.6278, "range": (1075.0, 1164.0),
            "label": "Lubricating oils"},
}


# =====================================================
# 🔹 CORE FUNCTION
# =====================================================
def vcf_iso_official(rho15: float, tempC: float) -> dict:
    """Compute Volume Correction Factor (VCF) for given density and temperature."""
    dT = tempC - 15.0

    # --- Determine applicable table ---
    if 610.5 <= rho15 <= 770.0:
        table = "54A"
    elif 770.0 < rho15 <= 1075.0:
        table = "54B"
    elif 1075.0 < rho15 <= 1164.0:
        table = "54D"
    else:
        raise ValueError(f"Density {rho15} kg/m³ outside ASTM range 610.5–1164.0")

    # --- Calculate VCF ---
    if table in ("54A", "54D"):
        coeff = VCF_TABLES[table]
        k0, k1 = coeff["K0"], coeff["K1"]
        a = (k0 + k1 * rho15) / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)
        label = coeff["label"]

    elif table == "54B":
        seg = next((s for s in VCF_TABLES["54B"]
                    if s["range"][0] < rho15 <= s["range"][1]), None)
        if seg is None:
            raise ValueError(f"Density {rho15} kg/m³ not in any 54B sub-range")

        label = seg.get("label", "Unknown 54B sub-range")
        if "K0" in seg:
            a = (seg["K0"] + seg["K1"] * rho15) / (rho15 ** 2)
        else:
            a = seg["A"] + seg["B"] / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)

    return {
        "table": f"{table} ({label})",
        "rho15": round(rho15, 3),
        "tempC": round(tempC, 2),
        "deltaT": round(dT, 2),
        "coefficient_a": round(a, 9),
        "exponent_b": round(b, 8),
        "VCF": round(vcf, 6),
    }


# =====================================================
# 🔹 VOLUME CORRECTION
# =====================================================
def correct_volume(fuel: str, observed_m3: float, tempC: float,
                   rho15: float | None = None, db_path: str | None = None) -> dict:
    """Correct observed volume → standard 15 °C volume."""
    db = Path(db_path or Path(__file__).parent / "tables" / "fuel_data.json")
    with open(db) as f:
        fuels = json.load(f)

    # ✅ Use user-input rho15 if provided, otherwise from DB
    rho15 = rho15 or fuels.get(fuel, {}).get("density_15C", 850.0)

    result = vcf_iso_official(rho15, tempC)
    vcf = result["VCF"]

    result.update({
        "fuel": fuel,
        "observed_m3": observed_m3,
        "V15_m3": round(observed_m3 * vcf, 3),
        "rho15": round(rho15, 3),
    })
    return result


# =====================================================
# 🔹 MASS CORRECTION
# =====================================================
def correct_mass(fuel: str, mass_ton: float, tempC: float,
                 rho15: float | None = None, db_path: str | None = None) -> dict:
    """Compute observed volume & 15 °C volume from mass."""
    db = Path(db_path or Path(__file__).parent / "tables" / "fuel_data.json")
    with open(db) as f:
        fuels = json.load(f)

    rho15 = rho15 or fuels.get(fuel, {}).get("density_15C", 850.0)
    rho15_ton_m3 = rho15 / 1000
    result = vcf_iso_official(rho15, tempC)
    vcf = result["VCF"]

    rhoT_ton_m3 = rho15_ton_m3 / vcf
    vol_obs = mass_ton / rhoT_ton_m3
    vol15 = vol_obs * vcf

    result.update({
        "fuel": fuel,
        "mass_ton": mass_ton,
        "rho15": round(rho15, 3),
        "rhoT_ton_m3": round(rhoT_ton_m3, 6),
        "volume_obs_m3": round(vol_obs, 3),
        "V15_m3": round(vol15, 3),
    })
    return result


# =====================================================
# 🔹 AUTO-DETECT CORRECTION
# =====================================================
def auto_correct(fuel: str, volume_m3=None, mass_ton=None,
                 tempC=None, rho15=None, db_path=None) -> dict:
    """Auto-detect input type and perform correction."""
    if tempC is None:
        raise ValueError("Temperature (°C) is required.")

    if volume_m3 is not None and mass_ton is None:
        result = correct_volume(fuel, volume_m3, tempC, rho15=rho15, db_path=db_path)
        result["mode"] = "volume_input"
        rho15_ton_m3 = result["rho15"] / 1000
        result["mass_ton"] = round(result["V15_m3"] * rho15_ton_m3, 3)
        base_volume = result["V15_m3"]

    elif mass_ton is not None and volume_m3 is None:
        result = correct_mass(fuel, mass_ton, tempC, rho15=rho15, db_path=db_path)
        result["mode"] = "mass_input"
        base_volume = result["V15_m3"]

    else:
        raise ValueError("Provide either volume_m3 or mass_ton (not both).")

    result["equivalents"] = {
        "m3_15C": round(base_volume, 3),
        "barrels_15C": round(convert(base_volume, "cum", "barrel"), 3),
        "litres_15C": round(convert(base_volume, "cum", "litre"), 1),
        "usg_15C": round(convert(base_volume, "cum", "usg"), 1),
    }
    return result
    
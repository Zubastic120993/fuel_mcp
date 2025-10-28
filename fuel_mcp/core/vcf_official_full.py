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
    "54A": {"K0": 613.9723, "K1": 0.0, "range": (610.5, 770.0), "label": "Light distillates (gasoline / naphtha)"},
    "54B": [
        {"range": (770.5, 787.5), "A": -0.00336312, "B": 2680.3206, "label": "Transition band"},
        {"range": (787.5, 838.5), "K0": 594.5418, "K1": 0.0, "label": "Jet / Kerosene"},
        {"range": (838.5, 1075.0), "K0": 186.9696, "K1": 0.48618, "label": "Residual / Marine fuels"},
    ],
    "54D": {"K0": 0.0, "K1": 0.6278, "range": (1075.0, 1164.0), "label": "Lubricating oils"},
}


# =====================================================
# 🔹 CORE FUNCTION
# =====================================================
def vcf_iso_official(rho15: float, tempC: float) -> dict:
    """
    Compute Volume Correction Factor (VCF) for a given density and temperature.
    Matches official ISO 91-1 / ASTM D1250 printed tables.
    
    Args:
        rho15: Density at 15°C in kg/m³
        tempC: Observed temperature in °C
        
    Returns:
        Dictionary with VCF calculation details
    """
    dT = tempC - 15.0

    # ---- Determine applicable table ----
    if 610.5 <= rho15 <= 770.0:
        table = "54A"
    elif 770.0 < rho15 <= 1075.0:
        table = "54B"
    elif 1075.0 < rho15 <= 1164.0:
        table = "54D"
    else:
        raise ValueError(
            f"Density {rho15} kg/m³ outside ASTM range (610.5–1164.0 kg/m³). "
            f"Valid ranges: 54A (610.5–770.0), 54B (770.0–1075.0), 54D (1075.0–1164.0)"
        )

    # ---- Perform calculation ----
    if table == "54A":
        k0, k1 = VCF_TABLES["54A"]["K0"], VCF_TABLES["54A"]["K1"]
        a = (k0 + k1 * rho15) / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)
        label = VCF_TABLES["54A"]["label"]

    elif table == "54D":
        k0, k1 = VCF_TABLES["54D"]["K0"], VCF_TABLES["54D"]["K1"]
        a = (k0 + k1 * rho15) / (rho15 ** 2)
        b = -a * dT * (1 + 0.8 * a * dT)
        vcf = math.exp(b)
        label = VCF_TABLES["54D"]["label"]

    elif table == "54B":
        selected = None
        for seg in VCF_TABLES["54B"]:
            lo, hi = seg["range"]
            if lo < rho15 <= hi:
                selected = seg
                break
        if not selected:
            raise ValueError(
                f"Density {rho15} kg/m³ not in any 54B sub-range. "
                f"Valid sub-ranges: (770.5–787.5), (787.5–838.5), (838.5–1075.0)"
            )

        label = selected.get("label", "Unknown 54B sub-range")

        if "K0" in selected:
            k0, k1 = selected["K0"], selected["K1"]
            a = (k0 + k1 * rho15) / (rho15 ** 2)
            b = -a * dT * (1 + 0.8 * a * dT)
            vcf = math.exp(b)
        else:
            A, B = selected["A"], selected["B"]
            a = A + B / (rho15 ** 2)
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
# 🔹 VOLUME-CORRECTION WRAPPER
# =====================================================
def correct_volume(fuel: str, observed_m3: float, tempC: float, db_path: str | None = None) -> dict:
    """
    Correct observed volume to standard conditions (15°C).
    
    Args:
        fuel: Fuel type identifier
        observed_m3: Observed volume in m³
        tempC: Observed temperature in °C
        db_path: Optional path to fuel database JSON
        
    Returns:
        Dictionary with correction details and corrected volume
    """
    if db_path is None:
        db_path = Path(__file__).parent / "tables" / "fuel_data.json"
    with open(db_path) as f:
        fuels = json.load(f)

    if fuel not in fuels:
        raise ValueError(f"Fuel '{fuel}' not found in database. Available fuels: {list(fuels.keys())}")

    rho15 = fuels[fuel]["density_15C"]
    result = vcf_iso_official(rho15, tempC)
    result["fuel"] = fuel
    result["observed_m3"] = observed_m3
    result["V15_m3"] = round(observed_m3 * result["VCF"], 3)
    return result


# =====================================================
# 🔹 MASS → VOLUME CALCULATION
# =====================================================
def correct_mass(fuel: str, mass_ton: float, tempC: float, db_path: str | None = None) -> dict:
    """
    Calculate volume from mass at observed temperature and correct to 15°C.
    
    Args:
        fuel: Fuel type identifier
        mass_ton: Mass in metric tons
        tempC: Observed temperature in °C
        db_path: Optional path to fuel database JSON
        
    Returns:
        Dictionary with correction details and volumes
    """
    if db_path is None:
        db_path = Path(__file__).parent / "tables" / "fuel_data.json"
    with open(db_path) as f:
        fuels = json.load(f)

    if fuel not in fuels:
        raise ValueError(f"Fuel '{fuel}' not found in database. Available fuels: {list(fuels.keys())}")

    rho15 = fuels[fuel]["density_15C"]
    rho15_ton_m3 = rho15 / 1000
    result = vcf_iso_official(rho15, tempC)
    vcf = result["VCF"]

    # Calculate density at observed temperature
    rhoT_ton_m3 = rho15_ton_m3 / vcf
    
    # Calculate observed volume from mass
    volume_obs_m3 = mass_ton / rhoT_ton_m3
    
    # Calculate volume at 15°C
    volume_15_m3 = volume_obs_m3 * vcf

    result.update({
        "fuel": fuel,
        "mass_ton": mass_ton,
        "rhoT_ton_m3": round(rhoT_ton_m3, 6),
        "volume_obs_m3": round(volume_obs_m3, 3),
        "V15_m3": round(volume_15_m3, 3),
    })
    return result


# =====================================================
# 🔹 UNIVERSAL AUTO-DETECT FUNCTION
# =====================================================
def auto_correct(fuel: str, volume_m3=None, mass_ton=None, tempC=None, db_path=None) -> dict:
    """
    Automatically detect input type and perform appropriate correction.
    
    Args:
        fuel: Fuel type identifier
        volume_m3: Observed volume in m³ (provide this OR mass_ton)
        mass_ton: Mass in metric tons (provide this OR volume_m3)
        tempC: Observed temperature in °C (required)
        db_path: Optional path to fuel database JSON
        
    Returns:
        Dictionary with correction details and equivalent volumes
    """
    if tempC is None:
        raise ValueError("Temperature (°C) must be provided.")
    if volume_m3 is not None and mass_ton is None:
        result = correct_volume(fuel, volume_m3, tempC, db_path)
        result["mode"] = "volume_input"
        rho15 = result["rho15"] / 1000
        result["mass_ton"] = round(result["V15_m3"] * rho15, 3)
        base_volume = result["V15_m3"]
    elif mass_ton is not None and volume_m3 is None:
        result = correct_mass(fuel, mass_ton, tempC, db_path)
        result["mode"] = "mass_input"
        base_volume = result["V15_m3"]
    else:
        raise ValueError("Provide either volume_m3 or mass_ton, not both.")

    result["equivalents"] = {
        "m3_15C": round(base_volume, 3),
        "barrels_15C": round(convert(base_volume, "cum", "barrel"), 3),
        "litres_15C": round(convert(base_volume, "cum", "litre"), 1),
        "usg_15C": round(convert(base_volume, "cum", "usg"), 1),
    }
    return result


# =====================================================
# 🔹 DEMONSTRATION
# =====================================================
if __name__ == "__main__":
    FUEL_DATA = {
        "diesel": {"density_15C": 850.0},
        "hfo": {"density_15C": 980.0},
        "jet": {"density_15C": 800.0},
        "lube": {"density_15C": 910.0},
        "gasoline": {"density_15C": 740.0},
    }
    
    # Create tables directory and write fuel data
    tables_dir = Path(__file__).parent / "tables"
    tables_dir.mkdir(exist_ok=True)
    db_path = tables_dir / "fuel_data.json"
    
    with open(db_path, "w") as f:
        json.dump(FUEL_DATA, f, indent=2)

    print("ISO 91-1 / ASTM D1250 VCF CALCULATOR\n")
    print(f"{'FUEL':<10} | {'TABLE':<40} | {'ρ₁₅ (kg/m³)':<12} | {'ΔT (°C)':<8} | {'VCF':<8} | {'V15 (m³)':<10}")
    print("-" * 110)
    
    for fuel in FUEL_DATA:
        res = correct_volume(fuel, 1000, 56, db_path=str(db_path))
        print(f"{res['fuel'].upper():<10} | {res['table']:<40} | "
              f"{res['rho15']:<12} | {res['deltaT']:<8} | "
              f"{res['VCF']:<8} | {res['V15_m3']:<10}")
    
    print("\n" + "="*110)
    print("\nExample with mass input:")
    res_mass = correct_mass("diesel", 100, 30, db_path=str(db_path))
    print(f"Fuel: {res_mass['fuel']}")
    print(f"Mass: {res_mass['mass_ton']} tons")
    print(f"Temperature: {res_mass['tempC']}°C")
    print(f"Density at T: {res_mass['rhoT_ton_m3']} ton/m³")
    print(f"Observed volume: {res_mass['volume_obs_m3']} m³")
    print(f"Volume at 15°C: {res_mass['V15_m3']} m³")
    print(f"VCF: {res_mass['VCF']}")
"""
conversion_engine.py
====================
Handles loading and simple interpolation from ASTM/ISO normalized tables.
Used internally by the dispatcher and MCP core for conversions.
"""

import pandas as pd
from pathlib import Path
import json


# =====================================================
# 🔧 Load registry (safe with fallback)
# =====================================================
REGISTRY_PATH = Path(__file__).parents[1] / "tables" / "registry.json"

try:
    with open(REGISTRY_PATH, "r") as f:
        REGISTRY = json.load(f)
except FileNotFoundError:
    REGISTRY = {}
    print(f"⚠️ Warning: registry.json not found at {REGISTRY_PATH}")


# =====================================================
# 📘 Core Table Loader
# =====================================================
def load_table_from_registry(table_name: str) -> pd.DataFrame:
    """
    Load table by its name from the registry (official/normalized folder).

    Parameters:
        table_name (str): CSV filename (e.g. ASTM_Table54B_...csv)

    Returns:
        pd.DataFrame: Loaded and parsed table.
    """
    base = Path(__file__).parents[1] / "tables" / "official" / "normalized"
    path = base / table_name

    if not path.exists():
        raise FileNotFoundError(f"❌ Table not found: {path}")

    return pd.read_csv(path)


# =====================================================
# 🔢 Core Conversion Functions (simple lookup/interpolation)
# =====================================================
def convert_density_to_mass(density_15C: float) -> dict:
    """
    Convert density at 15°C to mass (Short/Long tons per m³)
    using ASTM Table 54B (Density ↔ Tons/m³).

    Args:
        density_15C (float): Density at 15°C (kg/m³)

    Returns:
        dict: {
            "density_15C": float,
            "short_tons_per_m3": float,
            "long_tons_per_m3": float
        }
    """
    table_name = "ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter_norm.csv"
    df = load_table_from_registry(table_name)

    x = df["density_15c_kg_per_m3"]
    y1 = df["short_tons_per_cubicmeter"]
    y2 = df["long_tons_per_cubicmeter"]

    # Linear interpolation to approximate closest match
    idx = (x - density_15C).abs().idxmin()
    short_tons = float(pd.Series(y1).interpolate().iloc[idx])
    long_tons = float(pd.Series(y2).interpolate().iloc[idx])

    return {
        "density_15C": density_15C,
        "short_tons_per_m3": short_tons,
        "long_tons_per_m3": long_tons,
    }


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    result = convert_density_to_mass(980)
    print("✅ Conversion Result:", result)

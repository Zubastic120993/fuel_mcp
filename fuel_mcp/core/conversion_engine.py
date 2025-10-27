
# fuel_mcp/core/conversion_engine.py
import pandas as pd
from pathlib import Path
import json

# =====================================================
# 🔧 Load registry
# =====================================================
REGISTRY_PATH = Path(__file__).parents[1] / "tables" / "registry.json"

with open(REGISTRY_PATH, "r") as f:
    REGISTRY = json.load(f)


# =====================================================
# 📘 Core Table Loader
# =====================================================
def load_table_from_registry(table_name: str) -> pd.DataFrame:
    """Load table by its name from registry (normalized folder)."""
    base = Path(__file__).parents[1] / "tables" / "official" / "normalized"
    path = base / table_name

    if not path.exists():
        raise FileNotFoundError(f"❌ Table not found: {path}")

    return pd.read_csv(path)


# =====================================================
# 🔢 Core Conversion Functions (simple lookup or interpolation)
# =====================================================
def convert_density_to_mass(density_15C: float) -> dict:
    """
    Example: Use ASTM Table 54B (Density ↔ Tons/m³).
    Returns interpolated Short_Tons_per_CubicMeter and Long_Tons_per_CubicMeter.
    """
    table_name = "ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter_norm.csv"
    df = load_table_from_registry(table_name)

    x = df["density_15c_kg_per_m3"]
    y1 = df["short_tons_per_cubicmeter"]
    y2 = df["long_tons_per_cubicmeter"]

    # linear interpolation
    short_tons = float(pd.Series(y1).interpolate().iloc[(x - density_15C).abs().idxmin()])
    long_tons = float(pd.Series(y2).interpolate().iloc[(x - density_15C).abs().idxmin()])

    return {
        "density_15C": density_15C,
        "short_tons_per_m3": short_tons,
        "long_tons_per_m3": long_tons,
    }


# =====================================================
# 🧪 Quick Test
# =====================================================
if __name__ == "__main__":
    result = convert_density_to_mass(980)
    print("✅ Conversion Result:", result)

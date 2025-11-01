"""
fuel_mcp/core/fuel_density_loader.py
====================================

Dynamic loader for product densities used in Fuel MCP.
Reads from /fuel_mcp/core/tables/fuel_data.json (and merges it with built‑in defaults).
"""

import json
from pathlib import Path

# =====================================================
# 🧭 Default fallback densities (kg/m³ @15 °C)
# =====================================================
FUEL_DEFAULTS = {
    "diesel": 850.0,
    "hfo": 980.0,
    "gasoline": 740.0,
    "jet": 800.0,
    "lube": 910.0,
    "methanol": 791.0,
    "lpg": 540.0,
    "lng": 450.0,
}


# =====================================================
# 📂 Load densities from optional JSON source
# =====================================================
def load_fuel_densities() -> dict:
    """
    Load fuel density data from JSON file and merge with defaults.
    JSON can omit fuels — missing entries fall back to FUEL_DEFAULTS.
    """
    densities = dict(FUEL_DEFAULTS)
    json_path = Path(__file__).parent / "tables" / "fuel_data.json"

    if json_path.exists():
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            # Merge: JSON values override defaults
            for k, v in data.items():
                if isinstance(v, dict) and "density_15C" in v:
                    densities[k.lower()] = float(v["density_15C"])
        except Exception as e:
            print(f"⚠️ Failed to read fuel_data.json: {e} — using defaults.")

    return densities


# =====================================================
# ⚙️ Density accessor
# =====================================================
def get_fuel_density(fuel_name: str) -> float:
    """Return density (kg/m³ @15 °C) for the given fuel name."""
    fuel_name = fuel_name.lower().strip()
    densities = load_fuel_densities()

    if fuel_name not in densities:
        available = ", ".join(sorted(densities.keys()))
        raise ValueError(
            f"Unknown fuel '{fuel_name}'. Available fuels: {available}"
        )

    return float(densities[fuel_name])


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    data = load_fuel_densities()
    print("Available fuels:", sorted(data.keys()))
    for name, dens in sorted(data.items()):
        print(f"{name:<12} {dens} kg/m³")
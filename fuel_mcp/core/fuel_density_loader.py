"""
fuel_mcp/core/fuel_density_loader.py
====================================

Dynamic loader for product densities used in Fuel MCP.
Reads from /fuel_mcp/core/tables/fuel_data.json (or fallback default dict).
"""

import json
from pathlib import Path

# Default densities (fallback)
DEFAULT_DENSITIES = {
    "diesel": 850.0,
    "hfo": 980.0,
    "gasoline": 740.0,
    "jet": 800.0,
    "lube": 910.0,
    "methanol": 791.0,
    "lpg": 540.0,
    "lng": 450.0,
}


def load_fuel_densities() -> dict:
    """Load fuel density data from JSON file or fallback to defaults."""
    json_path = Path(__file__).parent / "tables" / "fuel_data.json"
    if json_path.exists():
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            return {k.lower(): v.get("density_15C", DEFAULT_DENSITIES.get(k, 850.0)) for k, v in data.items()}
        except Exception:
            return DEFAULT_DENSITIES
    return DEFAULT_DENSITIES


def get_fuel_density(fuel_name: str) -> float:
    """Return density for a given fuel (case-insensitive)."""
    densities = load_fuel_densities()
    return densities.get(fuel_name.lower(), 850.0)


if __name__ == "__main__":
    data = load_fuel_densities()
    print("Available fuels:", list(data.keys()))
    for name, dens in data.items():
        print(f"{name}: {dens} kg/m³")
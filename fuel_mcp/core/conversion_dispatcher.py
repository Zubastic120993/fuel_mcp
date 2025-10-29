
# fuel_mcp/core/conversion_dispatcher.py
import json
from pathlib import Path

from fuel_mcp.core.conversion_engine import load_table_from_registry


# =====================================================
# ⚙️ Load registry for all available tables
# =====================================================
REGISTRY_PATH = Path(__file__).parents[1] / "tables" / "registry.json"
with open(REGISTRY_PATH, "r") as f:
    REGISTRY = json.load(f)


# =====================================================
# 🧩 Helper to find tables by category
# =====================================================
def find_tables_by_category(category: str) -> list[str]:
    """Return all table names that match a given category."""
    return [
        name for name, meta in REGISTRY.items()
        if meta.get("category", "").lower().startswith(category.lower())
    ]


# =====================================================
# 🚀 General conversion dispatcher
# =====================================================
def convert(conversion_type: str, value: float) -> dict:
    """
    Dispatch conversion based on type.
    Example:
        convert("density_to_mass", 980)
        convert("density_to_volume", 850)
        convert("air_correction", 0.84)
    """
    conversion_type = conversion_type.lower()

    if conversion_type == "density_to_mass":
        # Table 54B
        table_name = "ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter_norm.csv"
        table = load_table_from_registry(table_name)
        idx, row = table.find_closest_row(
            "density_15c_kg_per_m3",
            value,
            required=["short_tons_per_cubicmeter", "long_tons_per_cubicmeter"],
        )
        short_ton = float(row["short_tons_per_cubicmeter"])  # type: ignore[arg-type]
        long_ton = float(row["long_tons_per_cubicmeter"])    # type: ignore[arg-type]
        return {
            "input_density_15C": value,
            "short_tons_per_m3": short_ton,
            "long_tons_per_m3": long_ton,
            "source_table": table_name,
            "_row_index": idx,
        }

    elif conversion_type == "density_to_volume":
        # Table 53B
        table_name = "ASTM_Table53B_Density15C_to_CubicMeters_per_MetricTon_norm.csv"
        table = load_table_from_registry(table_name)
        idx, row = table.find_closest_row(
            "density_15c_kg_per_m3",
            value,
            required=["cubic_meters_per_tonne"],
        )
        result = float(row["cubic_meters_per_tonne"])  # type: ignore[arg-type]
        return {
            "input_density_15C": value,
            "cubic_meters_per_tonne": result,
            "source_table": table_name,
            "_row_index": idx,
        }

    elif conversion_type == "air_correction":
        # Table 56
        table_name = "ASTM_Table56_Density15C_to_VacuoAirFactor_norm.csv"
        table = load_table_from_registry(table_name)
        idx, row = table.find_closest_row(
            "density_15c_kg_per_l",
            value,
            required=["weight_in_vacuo_to_air_factor"],
        )
        result = float(row["weight_in_vacuo_to_air_factor"])  # type: ignore[arg-type]
        return {
            "input_density_15C": value,
            "weight_in_vacuo_to_air_factor": result,
            "source_table": table_name,
            "_row_index": idx,
        }

    else:
        raise ValueError(f"❌ Unknown conversion type: {conversion_type}")


# =====================================================
# 🧪 Quick tests
# =====================================================
if __name__ == "__main__":
    print("🔹 Density → Mass:", convert("density_to_mass", 980))
    print("🔹 Density → Volume:", convert("density_to_volume", 850))
    print("🔹 Air Correction:", convert("air_correction", 0.84))

"""
conversion_engine.py
====================
Handles loading and simple interpolation from ASTM/ISO normalized tables.
Used internally by the dispatcher and MCP core for conversions.

The original implementation relied on :mod:`pandas`, but the execution
environment for the kata does not have that dependency available.  To keep the
behaviour accessible without external packages we provide a very small helper
layer that loads CSV files into plain Python data structures and exposes a few
utility helpers for querying rows.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable


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
# 📦 Lightweight table container
# =====================================================
@dataclass(frozen=True)
class TableData:
    """Container representing a CSV table loaded as rows of dictionaries."""

    rows: tuple[dict[str, float | str | None], ...]

    def column(self, name: str) -> list[float | str | None]:
        """Return a column as a list preserving ``None`` entries."""

        return [row.get(name) for row in self.rows]

    def get(self, index: int, name: str) -> float | str | None:
        return self.rows[index].get(name)

    def find_closest_row(
        self,
        column: str,
        target: float,
        *,
        required: Iterable[str] | None = None,
    ) -> tuple[int, dict[str, float | str | None]]:
        """Return the index and row with the closest value in ``column``.

        ``required`` can be supplied to ensure that the selected row has valid
        (non-``None``) entries for the listed columns.
        """

        required = tuple(required or ())
        best_idx: int | None = None
        best_diff: float | None = None

        for idx, row in enumerate(self.rows):
            value = row.get(column)
            if value is None:
                continue
            if not isinstance(value, (int, float)):
                continue
            if any(row.get(field) is None for field in required):
                continue

            diff = abs(float(value) - target)
            if best_diff is None or diff < best_diff:
                best_idx = idx
                best_diff = diff

        if best_idx is None:
            raise ValueError(
                f"No valid row found in column '{column}' for target {target}."
            )

        return best_idx, self.rows[best_idx]


# =====================================================
# 📘 Core Table Loader
# =====================================================
@lru_cache(maxsize=None)
def load_table_from_registry(table_name: str) -> TableData:
    """
    Load a table from the registry and return it as :class:`TableData`.

    ``pandas`` used to power this functionality, but the implementation now
    relies solely on the standard library so that it works in restricted
    environments.
    """

    base = Path(__file__).parents[1] / "tables" / "official" / "normalized"
    path = base / table_name

    if not path.exists():
        raise FileNotFoundError(f"❌ Table not found: {path}")

    def parse_value(value: str | None) -> float | str | None:
        if value is None:
            return None
        value = value.strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            return value

    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows: list[dict[str, float | str | None]] = []
        for raw_row in reader:
            parsed = {key: parse_value(val) for key, val in raw_row.items()}
            rows.append(parsed)

    if not rows:
        raise ValueError(f"Table '{table_name}' is empty or could not be parsed.")

    return TableData(tuple(rows))


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
    table = load_table_from_registry(table_name)

    idx, row = table.find_closest_row(
        "density_15c_kg_per_m3",
        density_15C,
        required=["short_tons_per_cubicmeter", "long_tons_per_cubicmeter"],
    )

    short_tons = float(row["short_tons_per_cubicmeter"])  # type: ignore[arg-type]
    long_tons = float(row["long_tons_per_cubicmeter"])    # type: ignore[arg-type]

    return {
        "density_15C": density_15C,
        "short_tons_per_m3": short_tons,
        "long_tons_per_m3": long_tons,
        "_row_index": idx,
    }


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    result = convert_density_to_mass(980)
    print("✅ Conversion Result:", result)

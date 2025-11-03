"""
api_correlate.py
================
ASTM / ISO correlation lookup API.
Uses normalized CSV tables under fuel_mcp/tables/official/normalized/.
Performs linear interpolation for values between table points.
Supports bidirectional (reverse) lookups with case-insensitive columns.
"""

from fastapi import APIRouter, Query
import pandas as pd
import numpy as np
from pathlib import Path

router = APIRouter(prefix="/correlate", tags=["ASTM correlations"])

DATA_DIR = Path(__file__).parent.parent / "tables" / "official" / "normalized"


@router.get("/")
def correlate(
    table: str = Query(..., description="CSV table filename (without .csv extension)"),
    column: str = Query(..., description="Input column name (any column name, case-insensitive)"),
    value: float = Query(..., description="Value to interpolate (x-value)"),
):
    """
    Lookup and interpolate ASTM/ISO correlation tables.
    - Works bidirectionally (any column as input).
    - Interpolates all numeric outputs.
    - Handles unsorted data safely.
    """
    file = DATA_DIR / f"{table}.csv"
    if not file.exists():
        return {"error": f"❌ Table '{table}.csv' not found in {DATA_DIR}"}

    try:
        df = pd.read_csv(file)
        df.columns = [c.lower().strip() for c in df.columns]
        column = column.lower().strip()

        if column not in df.columns:
            return {"error": f"❌ Column '{column}' not found. Available: {list(df.columns)}"}

        # Convert to numeric safely
        df = df.apply(pd.to_numeric, errors="coerce")
        df = df.dropna(subset=[column])

        if df.empty:
            return {"error": f"⚠️ No valid numeric data for column '{column}' in table '{table}'."}

        # Prepare and sort x-values
        x = df[column].astype(float).values
        sort_idx = np.argsort(x)
        x_sorted = x[sort_idx]

        # Clamp input value within range to prevent extrapolation
        value_clamped = max(min(value, np.max(x_sorted)), np.min(x_sorted))

        results = {}
        for col in df.columns:
            if col == column:
                continue
            y = df[col].astype(float).values
            y_sorted = y[sort_idx]
            results[col] = round(float(np.interp(value_clamped, x_sorted, y_sorted)), 4)

        return {
            "result": {
                "table": table,
                "input": {column: value},
                "outputs": results,
                "_meta": {
                    "rows": len(df),
                    "source": file.name,
                    "interpolation": "linear",
                    "reverse_supported": True,
                    "clamped": value != value_clamped,
                },
            },
            "mode": "correlate",
            "version": "1.5.1",
            "timestamp": pd.Timestamp.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "error": f"⚠️ Exception while correlating '{table}' column '{column}': {str(e)}"
        }
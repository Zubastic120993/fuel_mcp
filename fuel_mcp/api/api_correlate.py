"""
api_correlate.py
================
ASTM / ISO correlation lookup API.
Uses normalized CSV tables under fuel_mcp/tables/official/normalized/.
Performs linear interpolation for values between table points.
Now supports bidirectional (reverse) lookups with case-insensitive columns.
"""

from fastapi import APIRouter, Query
import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------------------------
# 🔹 Router definition
# -------------------------------------------------------------
router = APIRouter(prefix="/correlate", tags=["ASTM correlations"])

# Base directory for normalized ASTM tables
DATA_DIR = Path(__file__).parent.parent / "tables" / "official" / "normalized"

# -------------------------------------------------------------
# 🔹 Endpoint
# -------------------------------------------------------------
@router.get("/")
def correlate(
    table: str = Query(..., description="CSV table filename (without .csv extension)"),
    column: str = Query(..., description="Input column name (any column name, case-insensitive)"),
    value: float = Query(..., description="Value to interpolate (x-value)")
):
    """
    Lookup and interpolate ASTM/ISO correlation tables.
    - Automatically detects reverse lookup direction.
    - Interpolates across all other numeric columns.
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

        # Ensure all numeric
        numeric_df = df.apply(pd.to_numeric, errors="coerce").dropna()
        if column not in numeric_df.columns:
            return {"error": f"⚠️ Column '{column}' has non-numeric data."}

        # Prepare x-axis
        x = numeric_df[column].astype(float)

        results = {}
        for col in numeric_df.columns:
            if col == column:
                continue
            y = numeric_df[col].astype(float)
            result = float(np.interp(value, x, y))
            results[col] = round(result, 5)

        return {
            "result": {
                "table": table,
                "input": {column: value},
                "outputs": results,
                "_meta": {
                    "rows": len(numeric_df),
                    "source": file.name,
                    "interpolation": "linear",
                    "reverse_supported": True,
                },
            },
            "mode": "correlate",
            "version": "1.5.0",
            "timestamp": pd.Timestamp.utcnow().isoformat(),
        }

    except Exception as e:
        return {"error": f"⚠️ Exception: {str(e)}"}
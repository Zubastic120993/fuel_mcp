# fuel_mcp/core/mcp_core.py
"""
MCP Core Interface
==================
Unified API for all conversions inside fuel_mcp.
Now includes automatic logging to data/conversion_history.json.
"""

import json
from datetime import datetime
from pathlib import Path

from fuel_mcp.core.conversion_dispatcher import convert as table_convert
from fuel_mcp.vcf_official_full import auto_correct


# =====================================================
# 🔹 Logging helper
# =====================================================
def log_conversion(entry: dict):
    """Append each conversion result to a JSON log."""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    log_file = data_dir / "conversion_history.json"

    # Read existing log (if exists)
    if log_file.exists():
        try:
            with open(log_file, "r") as f:
                log = json.load(f)
        except json.JSONDecodeError:
            log = []
    else:
        log = []

    entry["timestamp"] = datetime.utcnow().isoformat() + "Z"
    log.append(entry)

    with open(log_file, "w") as f:
        json.dump(log, f, indent=2)


# =====================================================
# 🔹 Unified MCP Conversion API
# =====================================================
def mcp_convert(conversion_type: str, **kwargs) -> dict:
    """
    Central dispatcher for all conversion requests.
    Supports:
      - "density_to_mass"
      - "density_to_volume"
      - "air_correction"
      - "vcf" (analytical ISO 91-1 correction)
    """
    try:
        if conversion_type in ["density_to_mass", "density_to_volume", "air_correction"]:
            value = kwargs.get("value")
            if value is None:
                raise ValueError("Missing required argument: 'value'")
            result = table_convert(conversion_type, value)

        elif conversion_type == "vcf":
            fuel = kwargs.get("fuel")
            tempC = kwargs.get("tempC")
            vol = kwargs.get("volume_m3")
            mass = kwargs.get("mass_ton")
            if fuel is None or tempC is None:
                raise ValueError("Missing required arguments: 'fuel' and 'tempC'")
            result = auto_correct(fuel, vol, mass, tempC)

        else:
            raise ValueError(f"Unsupported conversion type: {conversion_type}")

        # Add metadata + log it
        result["_meta"] = {"conversion_type": conversion_type, "input": kwargs}
        log_conversion(result)

        return result

    except Exception as e:
        return {"error": str(e), "conversion_type": conversion_type}


# =====================================================
# 🔹 Demonstration
# =====================================================
if __name__ == "__main__":
    print("🔹 Test: Density → Mass")
    print(mcp_convert("density_to_mass", value=980))

    print("\n🔹 Test: VCF Analytical Correction")
    print(mcp_convert("vcf", fuel="diesel", tempC=56, volume_m3=1000))

    print("\n📁 Log file saved at: fuel_mcp/data/conversion_history.json")

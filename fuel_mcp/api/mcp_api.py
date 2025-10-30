"""
MCP Local API Service
=====================
Provides REST endpoints for MCP operations.

Endpoints:
- /status              → check online/offline mode
- /query?text=...      → run semantic MCP query (conversion / VCF)
- /convert?...         → perform unit conversion (ASTM Table 1)
- /vcf?...             → perform official ISO 91-1 VCF computation
- /auto_correct?...    → automatic mass/volume correction
- /units?...           → generic unit conversion
- /history             → show recent API calls
- /logs                → show recent log entries
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import json

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.core.unit_converter import convert as unit_convert
from fuel_mcp.core.vcf_official_full import (
    vcf_iso_official,
    correct_volume,
    correct_mass,
    auto_correct,
)

# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(title="MCP Local API", version="1.3")

LOG_FILE = Path("logs/mcp_queries.log")
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# =====================================================
# 📡 /status endpoint
# =====================================================
@app.get("/status")
def get_status():
    """Return online/offline mode."""
    try:
        mode = "online" if ONLINE_MODE else "offline"
        return {"status": "ok", "mode": mode}
    except Exception as e:
        log_error(e, module="mcp_api")
        return {"status": "error", "message": str(e)}


# =====================================================
# 🧠 /query endpoint
# =====================================================
@app.get("/query")
def run_query(text: str = Query(..., description="MCP natural-language query")):
    """Perform a semantic MCP query (conversion / correction)."""
    try:
        result = query_mcp(text)
        return JSONResponse(content=result)
    except Exception as e:
        log_error(e, query=text, module="mcp_api")
        logging.error(f"❌ MCP query failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# =====================================================
# ⚙️ /convert endpoint — ASTM D1250 Table 1 unit conversion
# =====================================================
@app.get("/convert")
def convert_units(
    value: float = Query(..., description="Numeric value to convert"),
    from_unit: str = Query(..., description="Unit to convert from"),
    to_unit: str = Query(..., description="Unit to convert to"),
):
    """Perform simple ASTM D1250 Table 1 unit conversion."""
    try:
        result = unit_convert(value, from_unit, to_unit)
        logging.info(f"🔄 Unit conversion: {value} {from_unit} → {result:.6f} {to_unit}")
        return {
            "input": {"value": value, "from": from_unit, "to": to_unit},
            "result": result,
        }
    except Exception as e:
        log_error(e, query=f"convert {value} {from_unit}->{to_unit}", module="unit_converter")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧮 /vcf endpoint — official ISO 91-1 / ASTM D1250 computation
# =====================================================
@app.get("/vcf")
def get_vcf(
    rho15: float = Query(..., description="Density at 15 °C (kg/m³)"),
    tempC: float = Query(..., description="Observed temperature °C"),
):
    """Compute exact Volume Correction Factor (VCF) using ISO 91-1 / ASTM D1250."""
    try:
        result = vcf_iso_official(rho15=rho15, tempC=tempC)
        logging.info(f"📊 VCF {rho15} kg/m³ @ {tempC} °C = {result['VCF']}")
        return result
    except Exception as e:
        log_error(e, query=f"vcf {rho15}@{tempC}", module="vcf_iso_official")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧠 /auto_correct endpoint — automatic volume/mass correction
# =====================================================
@app.get("/auto_correct")
def auto_correction(
    fuel: str = Query(...),
    volume_m3: float | None = Query(None),
    mass_ton: float | None = Query(None),
    tempC: float = Query(...),
    rho15: float | None = Query(None),
    db_path: str | None = None,
):
    """
    Auto correction for mass/volume — supports user-specified ρ15 (density at 15°C).
    If rho15 is not given, uses default from fuel_data.json.
    """
    try:
        # Load database if needed
        if db_path is None:
            db_path = Path(__file__).parent.parent / "core" / "tables" / "fuel_data.json"

        with open(db_path) as f:
            fuels = json.load(f)

        # ✅ Use user-specified density if provided
        if rho15 is None:
            rho15 = fuels.get(fuel, {}).get("density_15C", 850.0)
            logging.info(f"📘 Using database default density ρ15={rho15} kg/m³ for {fuel}")
        else:
            logging.info(f"⚙️ Using user-specified density ρ15={rho15} kg/m³ for {fuel}")

        # Pass to calculation core
        result = auto_correct(
            fuel=fuel,
            volume_m3=volume_m3,
            mass_ton=mass_ton,
            tempC=tempC,
            db_path=db_path,
        )

        # Add metadata
        result["fuel"] = fuel
        result["rho15"] = round(rho15, 3)

        logging.info(f"🧮 Auto-correct {fuel}: {tempC} °C @ {rho15} kg/m³ → VCF {result['VCF']}")
        return result

    except Exception as e:
        log_error(e, query=f"auto_correct {fuel}", module="vcf_iso_official")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧮 /units endpoint — alternative converter
# =====================================================
@app.get("/units")
def units_convert(
    value: float = Query(...),
    from_unit: str = Query(...),
    to_unit: str = Query(...),
):
    """Generic converter endpoint."""
    try:
        result = unit_convert(value, from_unit, to_unit)
        return {"input": {"value": value, "from": from_unit, "to": to_unit}, "result": result}
    except Exception as e:
        log_error(e, query=f"units {value} {from_unit}->{to_unit}", module="unit_converter")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧾 /history endpoint
# =====================================================
_HISTORY = []

@app.middleware("http")
async def track_requests(request, call_next):
    response = await call_next(request)
    try:
        if request.url.path in ("/vcf", "/auto_correct", "/convert", "/units"):
            entry = f"{request.url.path} | params={dict(request.query_params)}"
            _HISTORY.append(entry)
            if len(_HISTORY) > 200:
                _HISTORY.pop(0)
    except Exception:
        pass
    return response

@app.get("/history")
def get_history(limit: int = 20):
    """Return recent API calls."""
    return {"entries": _HISTORY[-limit:]}


# =====================================================
# 📜 /logs endpoint
# =====================================================
@app.get("/logs")
def get_logs(limit: int = 20):
    """Return last N log lines."""
    if not LOG_FILE.exists():
        return {"message": "No log file yet."}
    lines = LOG_FILE.read_text().splitlines()[-limit:]
    return {"entries": lines}


# =====================================================
# 🧪 Run standalone
# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fuel_mcp.api.mcp_api:app", host="0.0.0.0", port=8000, reload=True)

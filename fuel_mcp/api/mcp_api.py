"""
fuel_mcp/api/mcp_api.py
=======================

Fuel MCP Local API Service
--------------------------
Provides REST endpoints for MCP operations.

Endpoints:
- /                   → Welcome + route overview
- /status             → Check online/offline mode
- /query?text=...     → Run semantic MCP query (conversion / VCF)
- /convert?...        → Perform unit conversion (ASTM Table 1)
- /vcf?...            → Compute official ISO 91-1 / ASTM D1250 VCF
- /auto_correct?...   → Automatic mass/volume correction
- /tool               → Return OpenAI-compatible JSON schema
- /history            → Show recent API calls
- /logs               → Show recent log entries
"""

from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import json
from datetime import datetime, UTC

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.core.unit_converter import convert as unit_convert
from fuel_mcp.core.vcf_official_full import vcf_iso_official, auto_correct
from fuel_mcp.tool_integration import mcp_tool

# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(
    title="Fuel MCP Local API",
    version="1.4.0",
    description="ISO 91-1 / ASTM D1250 Marine Fuel Correction Processor",
)

LOG_FILE = Path("logs/mcp_queries.log")
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# =====================================================
# 🏠 Root endpoint — welcome and route overview
# =====================================================
@app.get("/")
def root():
    """Welcome message and route overview."""
    return {
        "service": "🧩 Fuel MCP Local API",
        "version": app.version,
        "docs_url": "http://127.0.0.1:8000/docs",
        "available_endpoints": {
            "/status": "Check online/offline mode",
            "/query?text=...": "Run semantic MCP query",
            "/convert?value=...&from_unit=...&to_unit=...": "Perform unit conversion",
            "/vcf?rho15=...&tempC=...": "Compute ISO 91-1 / ASTM D1250 VCF",
            "/auto_correct?fuel=...&tempC=...": "Auto mass/volume correction",
            "/history": "View recent API calls",
            "/logs": "View recent log entries",
            "/tool": "Get OpenAI-compatible function schema",
        },
    }


# =====================================================
# 📡 /status endpoint
# =====================================================
@app.get("/status")
def get_status():
    """Return current online/offline mode."""
    try:
        mode = "ONLINE" if ONLINE_MODE else "OFFLINE"
        return {
            "status": "ok",
            "mode": mode,
            "timestamp": datetime.now(UTC).isoformat(),
        }
    except Exception as e:
        log_error(e, module="mcp_api")
        return JSONResponse(status_code=500, content={"error": str(e)})


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
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# ⚙️ /convert endpoint — ASTM Table 1 unit conversion
# =====================================================
@app.get("/convert")
def convert_units(
    value: float = Query(..., description="Numeric value to convert"),
    from_unit: str = Query(..., description="Unit to convert from"),
    to_unit: str = Query(..., description="Unit to convert to"),
):
    """Perform ASTM D1250 Table 1 unit conversion."""
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
    tempC: float = Query(..., description="Observed temperature (°C)"),
):
    """Compute exact Volume Correction Factor (VCF)."""
    try:
        result = vcf_iso_official(rho15=rho15, tempC=tempC)
        logging.info(f"📊 VCF {rho15} kg/m³ @ {tempC} °C = {result['VCF']}")
        return result
    except Exception as e:
        log_error(e, query=f"vcf {rho15}@{tempC}", module="vcf_iso_official")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# ⚖️ /auto_correct endpoint — automatic volume/mass correction
# =====================================================
@app.get("/auto_correct")
def auto_correction(
    fuel: str = Query(...),
    volume_m3: float | None = Query(None),
    mass_ton: float | None = Query(None),
    tempC: float = Query(...),
    rho15: float | None = Query(None),
):
    """Auto-corrects mass/volume based on density and temperature."""
    try:
        db_path = Path(__file__).parent.parent / "core" / "tables" / "fuel_data.json"
        with open(db_path) as f:
            fuels = json.load(f)

        rho15 = rho15 or fuels.get(fuel, {}).get("density_15C", 850.0)
        result = auto_correct(
            fuel=fuel,
            volume_m3=volume_m3,
            mass_ton=mass_ton,
            tempC=tempC,
            db_path=db_path,
        )
        result["fuel"] = fuel
        result["rho15"] = round(rho15, 3)
        logging.info(f"🧮 Auto-correct {fuel}: {tempC} °C @ {rho15} kg/m³ → VCF {result['VCF']}")
        return result
    except Exception as e:
        log_error(e, query=f"auto_correct {fuel}", module="mcp_api")
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧰 /tool endpoint — OpenAI / LangChain tool schema
# =====================================================
@app.get("/tool")
def get_tool_schema():
    """Return OpenAI-compatible JSON schema for the Fuel MCP tool."""
    try:
        schema = {
            "type": "function",
            "function": {
                "name": mcp_tool.name,
                "description": "Marine Fuel Correction Processor Tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural-language query such as 'calculate VCF for diesel at 25°C'.",
                        }
                    },
                    "required": ["query"],
                },
            },
            "meta": {
                "version": app.version,
                "generated_at": datetime.now(UTC).isoformat(),
            },
        }
        return JSONResponse(content=schema)
    except Exception as e:
        log_error(e, module="mcp_api")
        return JSONResponse(status_code=500, content={"error": str(e)})


# =====================================================
# 🧾 /history endpoint
# =====================================================
_HISTORY: list[str] = []


@app.middleware("http")
async def track_requests(request: Request, call_next):
    response = await call_next(request)
    try:
        if request.url.path in ("/vcf", "/auto_correct", "/convert", "/query"):
            entry = f"{datetime.now().isoformat()} | {request.url.path} | {dict(request.query_params)}"
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
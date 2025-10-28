"""
MCP Local API Service
=====================
Provides REST endpoints for MCP operations.

Endpoints:
- /status              → check online/offline mode
- /query?text=...      → run semantic MCP query (conversion / VCF)
- /convert?...         → perform unit conversion (ASTM Table 1)
- /logs                → show recent log entries
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import logging

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.core.unit_converter import convert as unit_convert

# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(title="MCP Local API", version="1.1")

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
    """
    Perform an MCP query (conversion, correction, etc.).
    Example:
      /query?text=calculate VCF for heavy oil at 25C
    """
    try:
        result = query_mcp(text)
        return JSONResponse(content=result)

    except Exception as e:
        log_error(e, query=text, module="mcp_api")
        logging.error(f"❌ MCP query failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

# =====================================================
# ⚙️ /convert endpoint — simple ASTM D1250-80 converter
# =====================================================
@app.get("/convert")
def convert_units(
    value: float = Query(..., description="Numeric value to convert"),
    from_unit: str = Query(..., description="Unit to convert from"),
    to_unit: str = Query(..., description="Unit to convert to")
):
    """
    Perform a simple ASTM D1250-80 Table 1 unit conversion.
    Example:
      /convert?value=1&from_unit=barrel&to_unit=litre
    """
    try:
        result = unit_convert(value, from_unit, to_unit)
        logging.info(f"🔄 Unit conversion: {value} {from_unit} → {result:.6f} {to_unit}")
        return {
            "input": {"value": value, "from": from_unit, "to": to_unit},
            "result": result
        }

    except Exception as e:
        log_error(e, query=f"convert {value} {from_unit}->{to_unit}", module="unit_converter")
        return JSONResponse(status_code=400, content={"error": str(e)})

# =====================================================
# 📜 /logs endpoint
# =====================================================
@app.get("/logs")
def get_logs(limit: int = 20):
    """Return last N log lines for review."""
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

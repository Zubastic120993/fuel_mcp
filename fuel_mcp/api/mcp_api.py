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
- /history            → Show recent query history (SQLite)
- /errors             → Show recent application errors (SQLite)
- /metrics            → Show aggregated performance statistics
- /logs               → Show recent log entries
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import json
from datetime import datetime, UTC
from contextlib import asynccontextmanager
import sqlite3

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.core.unit_converter import convert as unit_convert
from fuel_mcp.core.vcf_official_full import vcf_iso_official, auto_correct
from fuel_mcp.tool_integration import mcp_tool
from fuel_mcp.core.db_logger import (
    get_recent_queries,
    init_db,
    DB_PATH,
)
from fuel_mcp.core.async_logger import log_query_async, log_error_async

# =====================================================
# 🧩 Lifespan handler
# =====================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize SQLite and log startup/shutdown events."""
    try:
        init_db()
        logging.info("🧩 SQLite initialized successfully (lifespan startup).")
        yield
    finally:
        logging.info("🧹 Fuel MCP API shutting down cleanly.")


# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(
    title="Fuel MCP Local API",
    version="1.4.3",
    description="ISO 91-1 / ASTM D1250 Marine Fuel Correction Processor",
    lifespan=lifespan,
)

LOG_FILE = Path("logs/mcp_queries.log")
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# =====================================================
# 🏠 Root endpoint
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
            "/tool": "Get OpenAI-compatible function schema",
            "/history": "View query history (SQLite)",
            "/errors": "View recent error logs (SQLite)",
            "/metrics": "View performance statistics (query counts, ratios, timestamps)",
            "/logs": "View log entries",
        },
    }


# =====================================================
# 📡 /status
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
# 🧠 /query
# =====================================================
@app.get("/query")
def run_query(text: str = Query(..., description="MCP natural-language query")):
    """Perform a semantic MCP query (conversion / correction)."""
    try:
        result = query_mcp(text)
        log_query_async(text, result, mode=result.get("_meta", {}).get("mode", "unknown"), success=True)
        return JSONResponse(content=result)
    except Exception as e:
        log_error(e, query=text, module="mcp_api")
        log_error_async("mcp_api", str(e))
        log_query_async(text, {"error": str(e)}, mode="error", success=False)
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# ⚙️ /convert — ASTM Table 1 conversion
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
        log_query_async(f"convert {value} {from_unit}->{to_unit}", result, "unit_convert", True)
        return {
            "input": {"value": value, "from": from_unit, "to": to_unit},
            "result": result,
        }
    except Exception as e:
        log_error(e, query=f"convert {value} {from_unit}->{to_unit}", module="unit_converter")
        log_error_async("unit_converter", str(e))
        log_query_async(f"convert {value} {from_unit}->{to_unit}", str(e), "error", False)
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# 🧮 /vcf — ISO/ASTM correction
# =====================================================
@app.get("/vcf")
def get_vcf(
    rho15: float = Query(..., description="Density at 15 °C (kg/m³)"),
    tempC: float = Query(..., description="Observed temperature (°C)"),
):
    """Compute exact Volume Correction Factor (VCF)."""
    try:
        result = vcf_iso_official(rho15=rho15, tempC=tempC)
        log_query_async(f"vcf {rho15}@{tempC}", result, "vcf", True)
        return result
    except Exception as e:
        log_error(e, query=f"vcf {rho15}@{tempC}", module="vcf_iso_official")
        log_error_async("vcf_iso_official", str(e))
        log_query_async(f"vcf {rho15}@{tempC}", str(e), "error", False)
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# ⚖️ /auto_correct — Mass/volume correction
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
        log_query_async(f"auto_correct {fuel}", result, "auto_correct", True)
        return result
    except Exception as e:
        log_error(e, query=f"auto_correct {fuel}", module="mcp_api")
        log_error_async("mcp_api", str(e))
        log_query_async(f"auto_correct {fuel}", str(e), "error", False)
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# ⚠️ /errors — View recent error entries
# =====================================================
@app.get("/errors")
def get_errors(limit: int = 20):
    """Return recent application errors from SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "SELECT timestamp, module, message, stacktrace FROM errors ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return {"entries": [], "message": "No errors recorded."}

        return {
            "count": len(rows),
            "entries": [
                {"timestamp": ts, "module": mod, "message": msg, "stacktrace": stack}
                for ts, mod, msg, stack in rows
            ],
        }
    except Exception as e:
        log_error(e, module="mcp_api")
        log_error_async("mcp_api", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


# =====================================================
# 📊 /metrics — System health and performance stats
# =====================================================
@app.get("/metrics")
def get_metrics():
    """Return live MCP engine metrics and database statistics."""
    metrics = {
        "total_queries": 0,
        "successful_queries": 0,
        "failed_queries": 0,
        "success_ratio": "0.0%",
        "last_query_time": None,
        "last_error_time": None,
        "db_path": str(DB_PATH.resolve()),
        "timestamp": datetime.now(UTC).isoformat(),
    }

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM queries")
        metrics["total_queries"] = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM queries WHERE success = 1")
        metrics["successful_queries"] = cur.fetchone()[0] or 0

        cur.execute("SELECT COUNT(*) FROM queries WHERE success = 0")
        metrics["failed_queries"] = cur.fetchone()[0] or 0

        cur.execute("SELECT timestamp FROM queries ORDER BY id DESC LIMIT 1")
        last_query = cur.fetchone()
        metrics["last_query_time"] = last_query[0] if last_query else None

        cur.execute("SELECT timestamp FROM errors ORDER BY id DESC LIMIT 1")
        last_error = cur.fetchone()
        metrics["last_error_time"] = last_error[0] if last_error else None

        total = metrics["total_queries"]
        success = metrics["successful_queries"]
        if total > 0:
            metrics["success_ratio"] = f"{(success / total) * 100:.1f}%"

        conn.close()
        return metrics

    except Exception as e:
        log_error(e, module="mcp_api")
        log_error_async("mcp_api", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


# =====================================================
# 🧾 /history — SQLite-backed
# =====================================================
@app.get("/history")
def get_history(limit: int = 20):
    """Return recent MCP query records from SQLite database."""
    try:
        rows = get_recent_queries(limit)
        entries = [
            {"timestamp": ts, "query": q, "mode": m, "success": bool(s)}
            for ts, q, m, s in rows
        ]
        return {"count": len(entries), "entries": entries}
    except Exception as e:
        log_error(e, module="mcp_api")
        log_error_async("mcp_api", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})


# =====================================================
# 📜 /logs — Plain log tail
# =====================================================
@app.get("/logs")
def get_logs(limit: int = 20):
    """Return last N log lines."""
    if not LOG_FILE.exists():
        return {"message": "No log file yet."}
    return {"entries": LOG_FILE.read_text().splitlines()[-limit:]}


# =====================================================
# 🧪 Run standalone
# =====================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fuel_mcp.api.mcp_api:app", host="0.0.0.0", port=8000, reload=True)
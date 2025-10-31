"""
fuel_mcp/api/mcp_api.py
=======================

Fuel MCP Local API Service — Unified Response Schema Edition (v1.0.3)
Includes regex-based natural language query parsing with reverse conversion support.
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
import json
import sqlite3
import platform
from datetime import datetime, UTC
from contextlib import asynccontextmanager

# -----------------------------------------------------
# ✅ Core imports
# -----------------------------------------------------
from fuel_mcp.core.regex_parser import process_query
from fuel_mcp.core.vcf_official_full import vcf_iso_official, auto_correct
from fuel_mcp.core.unit_converter import convert as unit_convert
from fuel_mcp.core.response_schema import success_response, error_response
from fuel_mcp.core.db_logger import get_recent_queries, init_db, DB_PATH
from fuel_mcp.core.async_logger import log_query_async, log_error_async
from fuel_mcp.core.error_handler import log_error
from fuel_mcp.tool_integration import mcp_tool
from fuel_mcp import __version__

# =====================================================
# 🧩 Lifespan handler
# =====================================================
START_TIME = datetime.now(UTC)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logging.info("🧩 SQLite initialized successfully (lifespan startup).")
        yield
    finally:
        logging.info("🧹 Fuel MCP API shutting down cleanly.")


# =====================================================
# ⚙️ FastAPI setup
# =====================================================
app = FastAPI(
    title="Fuel MCP Local API",
    version=__version__,
    description="ISO 91-1 / ASTM D1250 Marine Fuel Correction Processor",
    lifespan=lifespan,
)
init_db()

LOG_FILE = Path("logs/mcp_queries.log")
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# =====================================================
# 🧠 /query — Intelligent Parser + Unified Schema
# =====================================================
@app.get("/query")
def run_query(text: str = Query(...)):
    """
    Automatically interprets natural-language queries such as:
      - "convert 500 L diesel @ 30°C"
      - "calculate VCF for HFO at 25 degrees"
      - "convert 2 tons of diesel to m3 @ 25°C"
    """
    try:
        result = process_query(text)
        mode = result.get("mode", "unknown")

        if "error" in result:
            raise ValueError(result["error"])

        if mode not in ("vcf", "convert", "reverse", "volume_input"):
            raise ValueError(f"Unsupported query mode: {mode}")

        # Log + return schema
        log_query_async(text, result, mode, True)
        return JSONResponse(content=success_response(result, text, mode, app.version))

    except Exception as e:
        log_error(e, query=text, module="mcp_api")
        log_error_async("mcp_api", str(e))
        log_query_async(text, {"error": str(e)}, "error", False)
        return JSONResponse(
            status_code=400,
            content=error_response(str(e), text, "error", app.version, "/query"),
        )


# =====================================================
# ⚙️ /convert — Unified schema
# =====================================================
@app.get("/convert")
def convert_units(value: float = Query(...), from_unit: str = Query(...), to_unit: str = Query(...)):
    query_str = f"convert {value} {from_unit}->{to_unit}"
    try:
        result = unit_convert(value, from_unit, to_unit)
        log_query_async(query_str, result, "unit_convert", True)
        return JSONResponse(content=success_response(result, query_str, "unit_convert", app.version))
    except Exception as e:
        log_error(e, query=query_str, module="unit_converter")
        log_error_async("unit_converter", str(e))
        return JSONResponse(
            status_code=400,
            content=error_response(str(e), query_str, "error", app.version, "/convert"),
        )


# =====================================================
# 🧮 /vcf — Unified schema
# =====================================================
@app.get("/vcf")
def get_vcf(rho15: float = Query(...), tempC: float = Query(...)):
    query_str = f"vcf {rho15}@{tempC}"
    try:
        result = vcf_iso_official(rho15=rho15, tempC=tempC)
        log_query_async(query_str, result, "vcf", True)
        return JSONResponse(content=success_response(result, query_str, "vcf", app.version))
    except Exception as e:
        log_error(e, query=query_str, module="vcf_iso_official")
        log_error_async("vcf_iso_official", str(e))
        return JSONResponse(
            status_code=400,
            content=error_response(str(e), query_str, "error", app.version, "/vcf"),
        )


# =====================================================
# ⚖️ /auto_correct — Unified schema + dynamic density loader
# =====================================================
@app.get("/auto_correct")
def auto_correction(
    fuel: str = Query(...),
    volume_m3: float | None = None,
    mass_ton: float | None = None,
    tempC: float = Query(...),
    rho15: float | None = None,
):
    from fuel_mcp.core.fuel_density_loader import get_fuel_density

    query_str = f"auto_correct {fuel}@{tempC}"
    try:
        rho15 = rho15 or get_fuel_density(fuel)

        result = auto_correct(fuel=fuel, volume_m3=volume_m3, mass_ton=mass_ton, tempC=tempC)
        result["fuel"] = fuel
        result["rho15"] = round(rho15, 3)

        log_query_async(query_str, result, "auto_correct", True)
        return JSONResponse(content=success_response(result, query_str, "auto_correct", app.version))

    except Exception as e:
        log_error(e, query=query_str, module="mcp_api")
        log_error_async("mcp_api", str(e))
        return JSONResponse(
            status_code=400,
            content=error_response(str(e), query_str, "error", app.version, "/auto_correct"),
        )


# =====================================================
# 🧠 /debug — schema consistent
# =====================================================
@app.get("/debug")
def get_debug_info():
    try:
        log_size = LOG_FILE.stat().st_size / 1024 if LOG_FILE.exists() else 0
        db_size = Path(DB_PATH).stat().st_size / 1024 if Path(DB_PATH).exists() else 0
        result = {
            "service": "Fuel MCP Diagnostic Snapshot",
            "version": app.version,
            "python_version": platform.python_version(),
            "os": f"{platform.system()} {platform.release()}",
            "uptime_sec": round((datetime.now(UTC) - START_TIME).total_seconds(), 2),
            "db_path": str(DB_PATH.resolve()),
            "db_size_kb": round(db_size, 2),
            "log_file": str(LOG_FILE.resolve()),
            "log_size_kb": round(log_size, 2),
        }
        return JSONResponse(content=success_response(result, "debug info", "debug", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "debug", "error", app.version, "/debug"),
        )


# =====================================================
# 📡 /status — Unified schema
# =====================================================
@app.get("/status")
def get_status():
    try:
        from fuel_mcp.core.rag_bridge import ONLINE_MODE
        mode = "ONLINE" if ONLINE_MODE else "OFFLINE"
        result = {"status": "ok", "mode": mode}
        return JSONResponse(content=success_response(result, "status check", "status", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "status check", "error", app.version, "/status"),
        )


# =====================================================
# ⚠️ /errors — Unified schema
# =====================================================
@app.get("/errors")
def get_errors(limit: int = 20, module: str | None = None):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if module:
            cur.execute(
                "SELECT timestamp, module, message, stacktrace FROM errors WHERE module = ? ORDER BY id DESC LIMIT ?",
                (module, limit),
            )
        else:
            cur.execute("SELECT timestamp, module, message, stacktrace FROM errors ORDER BY id DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        conn.close()
        result = [{"timestamp": ts, "module": mod, "message": msg, "stacktrace": stack} for ts, mod, msg, stack in rows]
        return JSONResponse(content=success_response(result, f"errors (module={module})", "errors", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "errors", "error", app.version, "/errors"),
        )


# =====================================================
# 📊 /metrics — Unified schema
# =====================================================
@app.get("/metrics")
def get_metrics():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM queries")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM queries WHERE success = 1")
        success = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM queries WHERE success = 0")
        failed = cur.fetchone()[0]
        conn.close()
        result = {
            "total_queries": total,
            "successful_queries": success,
            "failed_queries": failed,
            "uptime_seconds": round((datetime.now(UTC) - START_TIME).total_seconds(), 2),
        }
        return JSONResponse(content=success_response(result, "metrics", "metrics", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "metrics", "error", app.version, "/metrics"),
        )


# =====================================================
# 🧾 /history — Unified schema
# =====================================================
@app.get("/history")
def get_history(limit: int = 20):
    try:
        rows = get_recent_queries(limit)
        result = [{"timestamp": ts, "query": q, "mode": m, "success": bool(s)} for ts, q, m, s in rows]
        return JSONResponse(content=success_response(result, "history", "history", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "history", "error", app.version, "/history"),
        )


# =====================================================
# 📜 /logs — Unified schema
# =====================================================
@app.get("/logs")
def get_logs(limit: int = 20):
    try:
        if not LOG_FILE.exists():
            result = {"message": "No log file yet."}
        else:
            result = {"entries": LOG_FILE.read_text().splitlines()[-limit:]}
        return JSONResponse(content=success_response(result, "logs", "logs", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "logs", "error", app.version, "/logs"),
        )


# =====================================================
# 🧰 /tool — Unified schema
# =====================================================
@app.get("/tool")
def get_tool_schema():
    try:
        schema = {
            "type": "function",
            "function": {
                "name": mcp_tool.name,
                "description": "Marine Fuel Correction Processor Tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Example: 'calculate VCF for diesel at 25°C'."},
                    },
                    "required": ["query"],
                },
            },
        }
        return JSONResponse(content=success_response(schema, "tool schema", "tool", app.version))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=error_response(str(e), "tool", "error", app.version, "/tool"),
        )
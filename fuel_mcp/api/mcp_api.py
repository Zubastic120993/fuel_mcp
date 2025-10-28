
"""
MCP Local API Service
=====================
Provides REST endpoints for MCP operations.
- /query?text=... : run conversion or VCF calculation
- /status         : return online/offline mode
- /logs           : show recent activity
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import json
import traceback
import logging
from datetime import datetime, UTC

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE

# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(title="MCP Local API", version="1.0")

LOG_FILE = Path("logs/mcp_queries.log")
ERROR_FILE = Path("logs/errors.json")
ERROR_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# =====================================================
# 📡 /status endpoint
# =====================================================
@app.get("/status")
def get_status():
    """Return online/offline mode and recent log summary."""
    try:
        mode = "online" if ONLINE_MODE else "offline"
        return {"status": "ok", "mode": mode}
    except Exception as e:
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
        err_info = {
            "timestamp": datetime.now(UTC).isoformat(),
            "query": text,
            "error_type": type(e).__name__,
            "message": str(e),
            "stacktrace": traceback.format_exc(),
        }

        # append to structured error log
        try:
            errors = json.load(open(ERROR_FILE)) if ERROR_FILE.exists() else []
        except Exception:
            errors = []
        errors.append(err_info)
        with open(ERROR_FILE, "w") as f:
            json.dump(errors, f, indent=2)

        logging.error(f"❌ MCP query failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

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

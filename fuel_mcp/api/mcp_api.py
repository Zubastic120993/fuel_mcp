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
import logging
from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.rag_bridge import ONLINE_MODE
from fuel_mcp.core.error_handler import log_error

# =====================================================
# 🔧 FastAPI setup
# =====================================================
app = FastAPI(title="MCP Local API", version="1.0")

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
    """Return online/offline mode and recent log summary."""
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
        # Unified structured error capture
        log_error(e, query=text, module="mcp_api")
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

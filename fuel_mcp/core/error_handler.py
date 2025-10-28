"""
Structured Error Handler
========================
Captures and logs MCP exceptions in a unified JSON format.
Used by both mcp_core.py and mcp_api.py.
"""

import json
import traceback
from datetime import datetime, UTC
from pathlib import Path
import logging

# =====================================================
# 📂 Paths
# =====================================================
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_FILE = LOG_DIR / "errors.json"

# =====================================================
# 🧠 Main Function
# =====================================================
def log_error(exception: Exception, query: str = None, module: str = None):
    """Append structured error details to logs/errors.json."""
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "module": module or "unknown",
        "query": query or "N/A",
        "error_type": type(exception).__name__,
        "message": str(exception),
        "stacktrace": traceback.format_exc(),
    }

    try:
        existing = json.load(open(ERROR_FILE)) if ERROR_FILE.exists() else []
    except Exception:
        existing = []

    existing.append(entry)
    with open(ERROR_FILE, "w") as f:
        json.dump(existing, f, indent=2)

    logging.error(f"❌ {entry['module']} failed: {entry['message']}")

# =====================================================
# 🧪 Quick test
# =====================================================
if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        log_error(e, query="test failure", module="demo")

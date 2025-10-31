"""
fuel_mcp/core/error_handler.py
==============================

Structured Error Handler
------------------------
Captures and logs MCP exceptions in a unified format.
All errors are written to both:
 - logs/mcp_errors.log (text file)
 - SQLite database (errors table in mcp_history.db)
"""

import traceback
import logging
from datetime import datetime, UTC
from pathlib import Path

from fuel_mcp.core.db_logger import init_db, log_error as log_error_db

# =====================================================
# 🔧 Setup
# =====================================================
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
ERROR_LOG_FILE = LOG_DIR / "mcp_errors.log"

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(ERROR_LOG_FILE),
        logging.StreamHandler(),
    ],
)

init_db()  # ensure database exists before logging


# =====================================================
# 🧠 Unified Error Logging
# =====================================================
def log_error(exception: Exception, query: str = None, module: str = None):
    """
    Log structured error information to SQLite + text log file.
    """
    timestamp = datetime.now(UTC).isoformat()
    entry = {
        "timestamp": timestamp,
        "module": module or "unknown",
        "query": query or "N/A",
        "error_type": type(exception).__name__,
        "message": str(exception),
        "stacktrace": traceback.format_exc(),
    }

    # 1️⃣ Log to SQLite
    try:
        log_error_db(
            module=entry["module"],
            message=entry["message"],
            stacktrace=entry["stacktrace"],
        )
    except Exception as db_exc:
        logging.error(f"⚠️ Failed to log error to SQLite: {db_exc}")

    # 2️⃣ Log to file
    logging.error(
        f"❌ {entry['module']} failed: {entry['message']}\n"
        f"→ {entry['error_type']}: {entry['stacktrace'].strip()}"
    )


# =====================================================
# 🧪 Manual Test
# =====================================================
if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        log_error(e, query="test failure", module="demo")
        print("✅ Error logged to SQLite and log file.")
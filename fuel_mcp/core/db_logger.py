"""
fuel_mcp/core/db_logger.py
==========================

SQLite logging and history storage for Fuel MCP.
Keeps structured logs of every query, result, error, and metrics snapshot.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, UTC

# =====================================================
# 📂 Database path (always root-level /data folder)
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "mcp_history.db"
DB_PATH.parent.mkdir(exist_ok=True)


# =====================================================
# 🏗️ Initialization
# =====================================================
def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Table: queries
    cur.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            mode TEXT,
            result TEXT,
            success INTEGER
        )
    """)

    # Table: errors
    cur.execute("""
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            module TEXT,
            message TEXT,
            stacktrace TEXT
        )
    """)

    # ✅ Table: metrics_log
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            uptime_seconds REAL,
            total_queries INTEGER,
            successful_queries INTEGER,
            failed_queries INTEGER,
            success_ratio TEXT,
            db_size_kb REAL
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# 🧠 Logging Functions
# =====================================================
def log_query(query: str, result: dict | str, mode: str = "unknown", success: bool = True):
    """Insert a query record into the database (auto-initialize if missing)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO queries (timestamp, query, mode, result, success) VALUES (?, ?, ?, ?, ?)",
        (datetime.now(UTC).isoformat(), query, mode, str(result), int(success)),
    )
    conn.commit()
    conn.close()


def log_error(module: str, message: str, stacktrace: str = ""):
    """Insert an error record into the database (auto-initialize if missing)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO errors (timestamp, module, message, stacktrace) VALUES (?, ?, ?, ?)",
        (datetime.now(UTC).isoformat(), module, message, stacktrace),
    )
    conn.commit()
    conn.close()


def log_metrics_snapshot(uptime_seconds, total, success, fail, ratio, db_size_kb):
    """Record periodic metrics snapshot into SQLite."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO metrics_log
        (timestamp, uptime_seconds, total_queries, successful_queries, failed_queries, success_ratio, db_size_kb)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(UTC).isoformat(),
            float(uptime_seconds),
            int(total),
            int(success),
            int(fail),
            str(ratio),
            float(db_size_kb),
        ),
    )
    conn.commit()
    conn.close()


def get_recent_queries(limit: int = 20) -> list[tuple]:
    """Return recent N query entries (auto-initialize if missing)."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT timestamp, query, mode, success FROM queries ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# =====================================================
# 🧪 Manual test
# =====================================================
if __name__ == "__main__":
    init_db()
    log_query("test query", {"VCF": 0.9915}, "vcf", True)
    log_metrics_snapshot(120.5, 5, 4, 1, "80.0%", 14.3)
    print(get_recent_queries(5))
    print("✅ DB initialized and metrics snapshot recorded.")
"""
fuel_mcp/core/cli.py
====================

Command-line interface for Fuel MCP.

Usage examples:
    mcp-cli status
    mcp-cli log
    mcp-cli vcf diesel 25
    mcp-cli convert "1000 liters of diesel at 25°C to mass in tons"
    mcp-cli history
    mcp-cli db stats
    mcp-cli db clean --days 30
    mcp-cli db vacuum
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from fuel_mcp.tool_interface import mcp_query
from fuel_mcp.core.setup_env import initialize_environment, LOG_FILE
from fuel_mcp.core.db_logger import get_recent_queries, log_query, DB_PATH

# =====================================================
# 📊 DB Maintenance Utilities
# =====================================================

def db_stats():
    """Show summary statistics from SQLite database."""
    initialize_environment(verbose=False)
    if not os.path.exists(DB_PATH):
        print("⚠️ Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM queries")
    total = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM queries WHERE success = 1")
    success = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM queries WHERE success = 0")
    failed = cur.fetchone()[0] or 0

    cur.execute("SELECT timestamp FROM queries ORDER BY id DESC LIMIT 1")
    last_query = cur.fetchone()

    cur.execute("SELECT timestamp FROM errors ORDER BY id DESC LIMIT 1")
    last_error = cur.fetchone()

    conn.close()

    ratio = (success / total * 100) if total > 0 else 0
    print("📊 Fuel MCP — Database Statistics")
    print(f"  • Total queries: {total}")
    print(f"  • Successful:   {success}")
    print(f"  • Failed:       {failed}")
    print(f"  • Success rate: {ratio:.1f}%")
    print(f"  • Last query:   {last_query[0] if last_query else '—'}")
    print(f"  • Last error:   {last_error[0] if last_error else '—'}")
    print(f"  • DB Path:      {DB_PATH}")


def db_clean(days: int = 30):
    """Remove old log and query entries older than N days."""
    initialize_environment(verbose=False)
    if not os.path.exists(DB_PATH):
        print("⚠️ Database not found.")
        return

    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM queries WHERE timestamp < ?", (cutoff,))
    cur.execute("DELETE FROM errors WHERE timestamp < ?", (cutoff,))
    deleted = conn.total_changes
    conn.commit()
    conn.close()

    print(f"🧹 Removed {deleted} old records (older than {days} days).")


def db_vacuum():
    """Compact and optimize SQLite database."""
    initialize_environment(verbose=False)
    if not os.path.exists(DB_PATH):
        print("⚠️ Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    before = DB_PATH.stat().st_size / 1024
    conn.execute("VACUUM")
    conn.close()
    after = DB_PATH.stat().st_size / 1024

    print("🧩 SQLite Database Optimization")
    print(f"  • Path: {DB_PATH}")
    print(f"  • Size reduced: {before:.1f} KB → {after:.1f} KB")


# =====================================================
# 🔍 Status and Logs
# =====================================================

def show_status():
    """Display current environment and log info."""
    initialize_environment(verbose=False)
    print("🧠 Fuel MCP Status:")
    print(f"  • Log file: {LOG_FILE}")
    if os.path.exists(LOG_FILE):
        size = os.path.getsize(LOG_FILE)
        print(f"  • Exists: ✅ ({size} bytes)")
        with open(LOG_FILE, "r") as log:
            lines = log.readlines()[-5:]
            print("🪵 Last log entries:")
            for line in lines:
                print(" ", line.strip())
    else:
        print("  • Exists: ❌ (no log yet)")


def show_log():
    """Print full application log."""
    initialize_environment(verbose=False)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            print(f.read())
    else:
        print("⚠️ No log file found.")


def show_history():
    """Show recent CLI query history from SQLite."""
    initialize_environment(verbose=False)
    rows = get_recent_queries(10)
    if not rows:
        print("⚠️ No recent queries found.")
        return
    print("🕒 Recent MCP Queries:")
    for ts, query, mode, success in rows:
        status = "✅" if success else "❌"
        print(f"  {ts} | {mode.upper():<10} | {status} | {query}")


# =====================================================
# 🔢 Query Handlers
# =====================================================

def handle_vcf(args):
    """Handle quick VCF calculation."""
    initialize_environment(verbose=False)
    if len(args) < 3:
        print("Usage: mcp-cli vcf <fuel> <tempC>")
        return
    fuel = args[1].lower()
    try:
        temp = float(args[2])
    except ValueError:
        print("❌ Temperature must be a number.")
        return
    query = f"calculate VCF for {fuel} at {temp}°C"
    result = mcp_query(query)
    log_query(query, result, mode="vcf", success=True)
    print(json.dumps(result, indent=2))


def handle_convert(args):
    """Handle general conversion queries."""
    initialize_environment(verbose=False)
    if len(args) < 2:
        print('Usage: mcp-cli convert "your query"')
        return
    query = " ".join(args[1:])
    result = mcp_query(query)
    log_query(query, result, mode="convert", success=True)
    print(json.dumps(result, indent=2))


# =====================================================
# 🚀 Entry Point
# =====================================================

def main():
    """Main CLI entry."""
    args = sys.argv[1:]
    if not args:
        print("Usage: mcp-cli [status|log|vcf|convert|history|db]")
        return

    cmd = args[0].lower()

    if cmd == "status":
        show_status()
    elif cmd == "log":
        show_log()
    elif cmd == "vcf":
        handle_vcf(args)
    elif cmd == "convert":
        handle_convert(args)
    elif cmd == "history":
        show_history()
    elif cmd == "db":
        if len(args) < 2:
            print("Usage: mcp-cli db [stats|clean|vacuum] [--days N]")
            return
        sub = args[1].lower()
        if sub == "stats":
            db_stats()
        elif sub == "clean":
            days = 30
            if len(args) > 3 and args[2] == "--days":
                try:
                    days = int(args[3])
                except ValueError:
                    print("❌ Invalid number for days.")
            db_clean(days)
        elif sub == "vacuum":
            db_vacuum()
        else:
            print("Available db commands: stats, clean, vacuum")
    else:
        print(f"❌ Unknown command: {cmd}")
        print("Available: status, log, vcf, convert, history, db")


if __name__ == "__main__":
    main()
"""
fuel_mcp/cli/mcp_cli.py
========================

Fuel MCP Command Line Interface.
Provides developer tools for quick system checks, tests, and maintenance.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
import platform
from pathlib import Path
import sqlite3

from fuel_mcp import __version__
from fuel_mcp.core.db_logger import DB_PATH


# =====================================================
# 🧩 STATUS COMMAND
# =====================================================
def cli_status():
    """Display basic environment and DB information."""
    db_size = round(DB_PATH.stat().st_size / 1024, 2) if DB_PATH.exists() else 0
    print("\n🧩 Fuel MCP — STATUS REPORT")
    print("=" * 40)
    print(f"🧠 Version:      {__version__}")
    print(f"🐍 Python:       {platform.python_version()}")
    print(f"📦 DB Path:      {DB_PATH}")
    print(f"💾 DB Size:      {db_size} KB")
    print(f"🕒 Timestamp:    {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 40)


# =====================================================
# 🧪 TEST COMMAND
# =====================================================
def cli_test():
    """Run pytest suite and save results to /logs/test_results.json."""
    logs_path = Path("logs")
    logs_path.mkdir(exist_ok=True)
    json_report = logs_path / "test_results.json"

    print("\n🧩 Running pytest suite...\n")
    cmd = ["pytest", "-q", "--json-report", f"--json-report-file={json_report}"]

    process = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in process.stdout:
        print(line, end="")

    process.wait()
    exit_code = process.returncode

    if json_report.exists():
        print(f"\n📝 JSON summary saved to: {json_report.resolve()}")
        try:
            with open(json_report) as f:
                report = json.load(f)
            summary = report.get("summary", {})
            print(
                f"\n✅ Tests: {summary.get('passed', 0)} passed, "
                f"{summary.get('failed', 0)} failed, "
                f"{summary.get('skipped', 0)} skipped."
            )
        except Exception as e:
            print(f"⚠️ Failed to parse JSON summary: {e}")
    else:
        print("❌ JSON report was not generated!")

    if exit_code == 0:
        print("\n✅ All tests passed successfully.")
    else:
        print("\n⚠️ Some tests failed. Review the summary above.")


# =====================================================
# 🧹 DB-PURGE COMMAND
# =====================================================
def cli_db_purge():
    """Clear all data from 'queries' and 'errors' tables."""
    if not DB_PATH.exists():
        print("❌ Database file not found.")
        return

    confirm = input("⚠️  This will delete all entries in 'queries' and 'errors'. Continue? [y/N]: ").lower()
    if confirm != "y":
        print("❌ Operation cancelled.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*) FROM queries;")
        query_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM errors;")
        error_count = cur.fetchone()[0]

        cur.execute("DELETE FROM queries;")
        cur.execute("DELETE FROM errors;")
        conn.commit()

        db_size = round(DB_PATH.stat().st_size / 1024, 2)

        print("\n✅ Database purged successfully.")
        print(f"🗑️  Deleted: {query_count} queries, {error_count} errors")
        print(f"💾 New DB size: {db_size} KB")
        print(f"🕒 Timestamp: {datetime.now().isoformat(timespec='seconds')}")

    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
    finally:
        conn.close()


# =====================================================
# 🔍 VERIFY COMMAND
# =====================================================
def cli_verify(auto_fix: bool = False):
    """Verify integrity of folders, database, and tables."""
    from fuel_mcp.core.db_logger import init_db
    from fuel_mcp.core.setup_env import initialize_environment

    data_path = Path("fuel_mcp/data")
    logs_path = Path("logs")

    db_exists = DB_PATH.exists()
    logs_exist = logs_path.exists()
    data_exist = data_path.exists()

    table_queries = False
    table_errors = False
    if db_exists:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cur.fetchall()]
                table_queries = "queries" in tables
                table_errors = "errors" in tables
        except Exception:
            pass

    print("\n🧩 Fuel MCP — VERIFICATION REPORT")
    print("=" * 50)
    print(f"✅ DB Exists: {db_exists}")
    print(f"✅ Logs Folder Exists: {logs_exist}")
    print(f"✅ Data Folder Exists: {data_exist}")
    print(f"✅ Table: queries: {table_queries}")
    print(f"✅ Table: errors: {table_errors}")

    if all([db_exists, logs_exist, data_exist, table_queries, table_errors]):
        print("\n✅ Verification successful — all components present.")
        return

    if auto_fix:
        print("\n⚙️  Running auto-fix...")
        initialize_environment()
        init_db()
        print("✅ Missing folders or tables recreated successfully.")
    else:
        print("\n⚠️ Some components are missing.")
        print("   Run again with '--fix' to auto-repair.")


# =====================================================
# 🚀 MAIN ENTRYPOINT
# =====================================================
def main():
    """Main CLI entrypoint."""
    if len(sys.argv) < 2:
        print("Usage: python -m fuel_mcp.cli.mcp_cli [status|test|db-purge|verify [--fix]]")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "status":
        cli_status()
    elif command == "test":
        cli_test()
    elif command == "db-purge":
        cli_db_purge()
    elif command == "verify":
        auto_fix = len(sys.argv) > 2 and sys.argv[2] == "--fix"
        cli_verify(auto_fix)
    else:
        print(f"❌ Unknown command: {command}")
        print("Available: status, test, db-purge, verify [--fix]")


if __name__ == "__main__":
    main()
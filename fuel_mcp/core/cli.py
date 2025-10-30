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
"""

import sys
import os
import json
from fuel_mcp.tool_interface import mcp_query
from fuel_mcp.core.setup_env import initialize_environment, LOG_FILE
from fuel_mcp.core.db_logger import get_recent_queries, log_query


# =====================================================
# 🧭 Status Display
# =====================================================
def show_status():
    """Display environment and log status."""
    initialize_environment(verbose=False)
    print("🧠 Fuel MCP Status:")
    print(f"  • Log file: {LOG_FILE}")

    if os.path.exists(LOG_FILE):
        size = os.path.getsize(LOG_FILE)
        print(f"  • Exists: ✅")
        print(f"  • Size: {size} bytes")
        print("🪵 Last log entries:")
        with open(LOG_FILE, "r") as log:
            for line in log.readlines()[-5:]:
                print(" ", line.strip())
    else:
        print("  • Exists: ❌ (no log yet)")


# =====================================================
# 📜 Show Log
# =====================================================
def show_log():
    """Print full app log."""
    initialize_environment(verbose=False)
    if not os.path.exists(LOG_FILE):
        print("⚠️ No log file found.")
        return
    with open(LOG_FILE, "r") as f:
        print(f.read())


# =====================================================
# ⚙️ Handle VCF
# =====================================================
def handle_vcf(args):
    """Quick VCF calculation from CLI."""
    initialize_environment(verbose=False)
    if len(args) < 3:
        print("Usage: mcp-cli vcf <fuel> <tempC>")
        return

    fuel = args[1].lower()
    try:
        temp = float(args[2])
    except ValueError:
        print("❌ Temperature must be numeric.")
        return

    query = f"calculate VCF for {fuel} at {temp}°C"
    result = mcp_query(query)
    log_query(query, result, mode="vcf", success=True)
    print(json.dumps(result, indent=2))


# =====================================================
# 🔁 Handle Conversion
# =====================================================
def handle_convert(args):
    """Run a natural-language conversion query."""
    initialize_environment(verbose=False)
    if len(args) < 2:
        print('Usage: mcp-cli convert "your query"')
        return

    query = " ".join(args[1:])
    result = mcp_query(query)
    log_query(query, result, mode="convert", success=True)
    print(json.dumps(result, indent=2))


# =====================================================
# 🕒 Show Query History
# =====================================================
def show_history():
    """Show recent MCP queries (SQLite only)."""
    initialize_environment(verbose=False)
    rows = get_recent_queries(10)
    if not rows:
        print("⚠️ No recent queries found.")
        return

    print("🕒 Recent MCP Queries:")
    for ts, query, mode, success in rows:
        status = "✅" if success else "❌"
        print(f"  {ts} | {mode.upper():<12} | {status} | {query}")


# =====================================================
# 🚀 Main CLI Dispatcher
# =====================================================
def main():
    """Main entry point for MCP CLI."""
    args = sys.argv[1:]
    if not args:
        print("Usage: mcp-cli [status|log|vcf|convert|history]")
        return

    cmd = args[0].lower()

    match cmd:
        case "status":
            show_status()
        case "log":
            show_log()
        case "vcf":
            handle_vcf(args)
        case "convert":
            handle_convert(args)
        case "history":
            show_history()
        case _:
            print(f"❌ Unknown command: {cmd}")
            print("Available commands: status, log, vcf, convert, history")


if __name__ == "__main__":
    main()
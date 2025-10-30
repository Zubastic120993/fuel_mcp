
"""
fuel_mcp/core/cli.py
====================

Command-line interface for Fuel MCP.
Usage examples:
    mcp-cli status
    mcp-cli log
    mcp-cli vcf diesel 25
    mcp-cli convert "1000 liters of diesel at 25°C to mass in tons"
"""

import sys
import os
import json
from fuel_mcp.tool_interface import mcp_query
from fuel_mcp.core.setup_env import initialize_environment, LOG_FILE


def show_status():
    """Display current environment and log info."""
    initialize_environment()
    print("🧠 Fuel MCP Status:")
    print(f"  • Log file: {LOG_FILE}")
    if os.path.exists(LOG_FILE):
        size = os.path.getsize(LOG_FILE)
        print(f"  • Exists: ✅")
        print(f"  • Size: {size} bytes")
        print("🪵 Last log entries:")
        with open(LOG_FILE, "r") as log:
            lines = log.readlines()[-5:]
            for line in lines:
                print(" ", line.strip())
    else:
        print("  • Exists: ❌ (no log yet)")


def show_log():
    """Print full application log."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            print(f.read())
    else:
        print("⚠️ No log file found.")


def handle_vcf(args):
    """Handle quick VCF calculation."""
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
    print(json.dumps(result, indent=2))


def handle_convert(args):
    """Handle general conversion queries."""
    if len(args) < 2:
        print('Usage: mcp-cli convert "your query"')
        return
    query = " ".join(args[1:])
    result = mcp_query(query)
    print(json.dumps(result, indent=2))


def main():
    """Main CLI entry."""
    args = sys.argv[1:]
    if not args:
        print("Usage: mcp-cli [status|log|vcf|convert]")
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
    else:
        print(f"❌ Unknown command: {cmd}")


if __name__ == "__main__":
    main()
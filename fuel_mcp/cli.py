
"""
fuel_mcp/cli.py
================

Command-line interface for Fuel MCP.
Usage:
  mcp-cli              → initializes environment
  mcp-cli status       → shows system status
  mcp-cli log          → prints last log entries
"""

import os
import sys
from fuel_mcp.core.setup_env import initialize_environment, LOG_FILE


def show_status():
    print("🧠 Fuel MCP Status:")
    print(f"  • Log file: {LOG_FILE}")
    print(f"  • Exists: {'✅' if os.path.exists(LOG_FILE) else '❌'}")
    print(f"  • Size: {os.path.getsize(LOG_FILE)} bytes" if os.path.exists(LOG_FILE) else "")


def show_logs(lines: int = 5):
    if not os.path.exists(LOG_FILE):
        print("⚠️ No log file found.")
        return
    with open(LOG_FILE, "r") as f:
        data = f.readlines()
    print("🪵 Last log entries:")
    for line in data[-lines:]:
        print("  " + line.strip())


def main():
    """Main entry point for mcp-cli."""
    args = sys.argv[1:]
    if not args:
        initialize_environment()
        return
    elif args[0] == "status":
        show_status()
    elif args[0] == "log":
        show_logs()
    else:
        print(f"❌ Unknown command: {' '.join(args)}")
        print("Usage: mcp-cli [status|log]")


if __name__ == "__main__":
    main()
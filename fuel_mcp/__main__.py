"""
fuel_mcp/__main__.py
====================

Command-line entry point for the Fuel MCP system.
Usage:
    python -m fuel_mcp
"""

from fuel_mcp.core.setup_env import initialize_environment


def main():
    """Entry point when executed as a module."""
    initialize_environment(verbose=False)
    print("🧠 Fuel MCP — Marine Correction Processor")
    print("✅ Ready for operation.")


if __name__ == "__main__":
    main()
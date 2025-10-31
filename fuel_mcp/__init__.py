"""
fuel_mcp/__init__.py
====================

Main package initializer.
This file defines constants and exposes core setup utilities.
"""

from fuel_mcp.core.setup_env import initialize_environment

# 🔖 Package version (used by CLI and API responses)
__version__ = "1.5.0"

__all__ = ["initialize_environment", "__version__"]
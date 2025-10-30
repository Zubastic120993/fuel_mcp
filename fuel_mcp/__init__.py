"""
fuel_mcp/__init__.py
====================

Main package initializer.
This file should only define imports and constants — not run initialization.
"""

from fuel_mcp.core.setup_env import initialize_environment

__all__ = ["initialize_environment"]
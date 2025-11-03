"""
fuel_mcp/__init__.py
====================

Main package initializer.
Defines package metadata and optionally initializes environment settings.
"""

# --------------------------------------------------------------------
# Optional environment setup (safe for Docker builds)
# --------------------------------------------------------------------
try:
    from fuel_mcp.core.setup_env import initialize_environment
    initialize_environment()
except ModuleNotFoundError:
    # Safe fallback for Dockerized or minimal builds
    print("⚙️  Environment initialization skipped (no setup_env module found).")

# --------------------------------------------------------------------
# Package metadata
# --------------------------------------------------------------------
__version__ = "1.5.0"

__all__ = ["__version__"]
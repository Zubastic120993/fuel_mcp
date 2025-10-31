"""
fuel_mcp/core/setup_env.py
==========================

Initializes the required folder structure for the Fuel MCP project.
Also writes a startup log entry each time the app is launched.
All folders and files are created *inside the package*, not in the root.
"""

from datetime import datetime
from pathlib import Path


# =====================================================
# 📂 Base Paths
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
ENV_FILE = BASE_DIR / ".env"
LOG_FILE = LOG_DIR / "app.log"


def ensure_directories() -> None:
    """Create essential directories if missing."""
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)


def ensure_env_file() -> bool:
    """Create a default .env file if missing. Returns True if created."""
    if not ENV_FILE.exists():
        ENV_FILE.write_text("# Fuel MCP environment variables\nMODE=OFFLINE\n")
        print(f"🧩 Created new .env file at {ENV_FILE}")
        return True
    return False


def log_startup_message() -> None:
    """Append a timestamped startup message to logs/app.log."""
    ensure_directories()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{now} | STARTUP | Fuel MCP initialized successfully (mode=OFFLINE)"
    try:
        with open(LOG_FILE, "a") as log:
            log.write(message + "\n")
    except Exception as e:
        print(f"⚠️ Failed to write log: {e}")
    else:
        print("🪵 Startup log entry recorded.")


def initialize_environment(verbose: bool = True) -> bool:
    """
    Main entry point for environment setup.
    Returns True if successful.
    """
    ensure_directories()
    created = ensure_env_file()
    log_startup_message()

    if verbose:
        print("✅ Environment initialized inside package (fuel_mcp/)")
        print("🧠 Fuel MCP — Marine Correction Processor")
        print("✅ Ready for operation." if not created else "🆕 First-time setup complete!")

    return True


# =====================================================
# 🧪 Manual Run
# =====================================================
if __name__ == "__main__":
    initialize_environment()
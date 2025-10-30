"""
fuel_mcp/core/setup_env.py
==========================

Initializes the required folder structure for the Fuel MCP project.
Also writes a startup log entry each time the app is launched.
"""

import os
from datetime import datetime

# Base project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
ENV_FILE = os.path.join(BASE_DIR, ".env")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def ensure_directories():
    """Create essential directories if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


def ensure_env_file():
    """Create a default .env file if missing."""
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w") as f:
            f.write("# Fuel MCP environment variables\nMODE=OFFLINE\n")
        print(f"🧩 Created new .env file at {ENV_FILE}")
        return True
    return False


def log_startup_message():
    """Append a timestamped startup message to app.log."""
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
        if created:
            print("✅ Environment initialized for the first time.")
        else:
            print("✅ Environment already initialized.")

    return True


if __name__ == "__main__":
    # Run directly (for standalone test)
    initialize_environment()
    print("🧠 Fuel MCP — Marine Correction Processor")
    print("✅ Ready for operation.")

"""
fuel_mcp/tests/test_cli_maintenance.py
=====================================

Tests for new Maintenance CLI features:
- mcp-cli db stats
- mcp-cli db clean
"""

import subprocess
import sqlite3
from pathlib import Path
from fuel_mcp.core.db_logger import DB_PATH, init_db


def setup_module(module):
    """Ensure database exists before tests."""
    init_db()


def test_db_stats_command(tmp_path):
    """Check that 'mcp-cli db stats' prints valid statistics."""
    result = subprocess.run(
        ["python", "-m", "fuel_mcp.core.cli", "db", "stats"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    assert "Fuel MCP — Database Statistics" in output
    assert "Total queries" in output
    assert "DB Path" in output
    assert result.returncode == 0


def test_db_clean_command(tmp_path):
    """Check that 'mcp-cli db clean --days 1' runs successfully and modifies DB."""
    # Insert dummy old data
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO queries (timestamp, query, mode, success) VALUES (?, ?, ?, ?)",
        ("2000-01-01T00:00:00", "old query", "test", 1),
    )
    conn.commit()
    conn.close()

    result = subprocess.run(
        ["python", "-m", "fuel_mcp.core.cli", "db", "clean", "--days", "1"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    assert "Removed" in output
    assert "records" in output
    assert result.returncode == 0


def test_db_clean_default(tmp_path):
    """Run without --days argument (default 30 days)."""
    result = subprocess.run(
        ["python", "-m", "fuel_mcp.core.cli", "db", "clean"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    assert "Removed" in output or "records" in output
    assert result.returncode == 0
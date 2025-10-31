
"""
fuel_mcp/tests/test_cli_vacuum.py
=================================

Test suite for the Fuel MCP CLI database maintenance — `db_vacuum()`.
Ensures that the database compacts properly and remains valid.
"""

import os
import sqlite3
from io import StringIO
from contextlib import redirect_stdout
from fuel_mcp.core import cli
from fuel_mcp.core.db_logger import DB_PATH, init_db


def setup_module(module):
    """Prepare a clean SQLite DB with sample data."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for i in range(50):
        cur.execute(
            "INSERT INTO queries (timestamp, query, mode, success) VALUES (?, ?, ?, ?)",
            (f"2025-10-01T12:00:{i:02d}", f"test_query_{i}", "vcf", 1),
        )
    conn.commit()
    conn.close()


def test_db_vacuum_effectiveness():
    """Ensure db_vacuum runs and reports size reduction."""
    assert os.path.exists(DB_PATH)

    before = os.path.getsize(DB_PATH)
    f = StringIO()
    with redirect_stdout(f):
        cli.db_vacuum()
    output = f.getvalue()

    after = os.path.getsize(DB_PATH)

    # Ensure the vacuum function prints expected info
    assert "SQLite Database Optimization" in output
    assert "Path:" in output
    assert "Size reduced:" in output

    # DB should still exist and not grow
    assert os.path.exists(DB_PATH)
    assert after <= before


def teardown_module(module):
    """Cleanup DB after test."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
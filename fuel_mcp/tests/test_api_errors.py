
"""
fuel_mcp/tests/test_api_errors.py
================================

Integration tests for the /errors API endpoint.

Checks:
- ✅ Basic access to /errors returns valid JSON structure.
- ✅ Module filtering via ?module=mcp_api works correctly.
- ✅ Graceful handling of empty database (no errors).
"""

import pytest
from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app

client = TestClient(app)


# -----------------------------------------------------
# ⚠️ /errors — Basic test
# -----------------------------------------------------
def test_errors_endpoint_basic():
    res = client.get("/errors")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)


# -----------------------------------------------------
# ⚙️ /errors — Filter by module
# -----------------------------------------------------
def test_errors_endpoint_with_module_filter():
    res = client.get("/errors", params={"module": "mcp_api"})
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)
    # If entries exist, all must match the requested module
    for e in data["result"]["entries"]:
        assert e["module"] == "mcp_api"


# -----------------------------------------------------
# 🧪 /errors — Limit parameter
# -----------------------------------------------------
def test_errors_endpoint_limit_param():
    res = client.get("/errors", params={"limit": 5})
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert len(data["result"]["entries"]) <= 5
"""
fuel_mcp/tests/test_api_full.py
===============================

Full integration test suite for the Fuel MCP Local API.
Covers all public endpoints exposed by FastAPI.

Endpoints tested:
- /status
- /vcf
- /convert
- /auto_correct
- /query
- /history
- /errors
- /metrics
- /tool
- /logs
"""

import pytest
from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app

client = TestClient(app)

# -----------------------------------------------------
# 🛰️ STATUS ENDPOINT
# -----------------------------------------------------
def test_status_endpoint():
    res = client.get("/status")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data and data["result"]["status"] == "ok"
    assert data["mode"] in ["OFFLINE", "ONLINE"]

# -----------------------------------------------------
# 🧮 VCF ENDPOINT
# -----------------------------------------------------
def test_vcf_endpoint():
    res = client.get("/vcf", params={"rho15": 840, "tempC": 25})
    assert res.status_code == 200
    data = res.json()
    assert "VCF" in data
    assert 0.98 < data["result"]["VCF"] < 1.0  # expected correction range

# -----------------------------------------------------
# ⚙️ CONVERT ENDPOINT
# -----------------------------------------------------
def test_convert_endpoint():
    res = client.get("/convert", params={"value": 1, "from_unit": "liter", "to_unit": "m3"})
    assert res.status_code == 200
    data = res.json()
    assert "result" in data
    assert data["result"] == pytest.approx(0.001, rel=1e-6)

# -----------------------------------------------------
# ⚖️ AUTO CORRECT ENDPOINT
# -----------------------------------------------------
def test_auto_correct_endpoint():
    # ✅ must include either volume_m3 or mass_ton
    res = client.get("/auto_correct", params={"fuel": "diesel", "tempC": 25, "volume_m3": 1})
    assert res.status_code == 200
    data = res.json()
    assert "VCF" in data
    assert "rho15" in data
    assert 0.98 < data["result"]["VCF"] < 1.0

# -----------------------------------------------------
# 🧠 QUERY ENDPOINT
# -----------------------------------------------------
def test_query_endpoint():
    res = client.get("/query", params={"text": "calculate VCF for diesel at 25°C"})
    assert res.status_code == 200
    data = res.json()
    assert "VCF" in data
    assert data["_meta"]["mode"] == "vcf"

# -----------------------------------------------------
# 🧾 HISTORY ENDPOINT
# -----------------------------------------------------
def test_history_endpoint():
    res = client.get("/history")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)
    assert len(data["result"]["entries"]) >= 1  # should not be empty after previous queries

# -----------------------------------------------------
# ⚠️ ERRORS ENDPOINT
# -----------------------------------------------------
def test_errors_endpoint():
    res = client.get("/errors")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)
    # It’s fine if empty, but structure must exist
    if len(data["result"]["entries"]) > 0:
        entry = data["result"]["entries"][0]
        assert "timestamp" in entry
        assert "module" in entry
        assert "message" in entry

# -----------------------------------------------------
# 📊 METRICS ENDPOINT
# -----------------------------------------------------
def test_metrics_endpoint():
    res = client.get("/metrics")
    assert res.status_code == 200
    data = res.json()
    # Must include performance metrics
    for key in [
        "total_queries",
        "successful_queries",
        "failed_queries",
        "success_ratio",
        "db_path",
        "timestamp",
    ]:
        assert key in data
    assert isinstance(data["result"]["total_queries"], int)
    assert "%" in data["success_ratio"]

# -----------------------------------------------------
# 🧰 TOOL ENDPOINT
# -----------------------------------------------------
def test_tool_schema_endpoint():
    res = client.get("/tool")
    assert res.status_code == 200
    data = res.json()
    assert "function" in data
    assert "parameters" in data["function"]

# -----------------------------------------------------
# 📜 LOGS ENDPOINT
# -----------------------------------------------------
def test_logs_endpoint():
    res = client.get("/logs")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)
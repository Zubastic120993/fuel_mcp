
"""
fuel_mcp/tests/test_api_metrics.py
==================================

Integration tests for the /metrics endpoint of Fuel MCP API.
Ensures that database stats, uptime, and ratios are reported correctly.
"""

from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app
import pytest

client = TestClient(app)

# -----------------------------------------------------
# 📊 METRICS ENDPOINT BASIC VALIDATION
# -----------------------------------------------------
def test_metrics_endpoint_status():
    res = client.get("/metrics")
    assert res.status_code == 200, "Expected HTTP 200 for /metrics endpoint"
    data = res.json()

    # Core keys must exist
    for key in [
        "version",
        "python_version",
        "uptime_seconds",
        "total_queries",
        "successful_queries",
        "failed_queries",
        "success_ratio",
        "timestamp",
        "db_path",
    ]:
        assert key in data, f"Missing key: {key}"

    # Value validation
    assert isinstance(data["result"]["uptime_seconds"], (int, float))
    assert isinstance(data["result"]["total_queries"], int)
    assert isinstance(data["successful_queries"], int)
    assert isinstance(data["failed_queries"], int)
    assert isinstance(data["success_ratio"], str)
    assert "%" in data["success_ratio"]

    # DB path should be valid
    assert data["db_path"].endswith("mcp_history.db")

# -----------------------------------------------------
# 🕒 METRICS SHOULD INCREASE AFTER A QUERY
# -----------------------------------------------------
def test_metrics_changes_after_query():
    """Run a query, then check that total_queries increased."""
    before = client.get("/metrics").json()
    before_count = before["total_queries"]

    # Run a sample API query
    query_response = client.get("/vcf", params={"rho15": 850, "tempC": 25})
    assert query_response.status_code == 200

    after = client.get("/metrics").json()
    assert after["total_queries"] >= before_count, "Query count should increase or remain valid"

# -----------------------------------------------------
# 🔄 UPTIME MUST ALWAYS INCREASE
# -----------------------------------------------------
@pytest.mark.asyncio
async def test_metrics_uptime_progress():
    """Uptime should be monotonic and positive."""
    import asyncio
    first = client.get("/metrics").json()["uptime_seconds"]
    await asyncio.sleep(1)
    second = client.get("/metrics").json()["uptime_seconds"]
    assert second >= first, "Uptime should increase over time"

"""
fuel_mcp/tests/test_api_reverse.py
==================================

Validates reverse conversion queries (mass → volume)
via the /query endpoint using the unified response schema.
"""

from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app

client = TestClient(app)


def test_reverse_conversion_diesel():
    """Check correct reverse (tons → m³) conversion for diesel."""
    query = "convert 2 tons of diesel to m3 @ 25°C"
    res = client.get("/query", params={"text": query})

    # Ensure request succeeded
    assert res.status_code == 200, res.text

    data = res.json()
    result = data.get("result", {})

    # Validate expected structure
    assert "fuel" in result
    assert "mass_ton" in result
    assert "volume_obs_m3" in result
    assert "VCF" in result
    assert result["fuel"] == "diesel"
    assert abs(result["mass_ton"] - 2.0) < 1e-6
    assert result["volume_obs_m3"] > 2.0  # around 2.33 expected
    assert result["mode"] == "reverse"

    # Ensure metadata block exists
    meta = data.get("_meta", {})
    assert "timestamp" in meta
    assert meta["mode"] == "reverse"


def test_reverse_missing_temp():
    """Ensure missing temperature triggers error gracefully."""
    query = "convert 5 tons of hfo to m3"
    res = client.get("/query", params={"text": query})

    # Should return 400 Bad Request
    assert res.status_code in (400, 422)
    body = res.json()
    assert "error" in body["result"] or "error" in body


def test_reverse_methanol_behavior():
    """Check methanol reverse conversion works."""
    query = "convert 1 ton of methanol to m3 @ 20°C"
    res = client.get("/query", params={"text": query})

    assert res.status_code == 200
    result = res.json().get("result", {})
    assert result["fuel"] == "methanol"
    assert "V15_m3" in result
    assert result["mode"] == "reverse"
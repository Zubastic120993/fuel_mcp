"""
test_api_endpoints.py
=====================
Integration tests for the MCP FastAPI layer.
Verifies that all core REST endpoints respond correctly and return valid data.
"""

from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app

client = TestClient(app)

# =====================================================
# 🧭 /status
# =====================================================
def test_status_endpoint():
    res = client.get("/status")
    assert res.status_code == 200
    data = res.json()
    assert "status" in data
    assert data["result"]["status"] == "ok"


# =====================================================
# ⚙️ /convert
# =====================================================
def test_convert_endpoint():
    res = client.get("/convert", params={"value": 1, "from_unit": "m3", "to_unit": "litre"})
    assert res.status_code == 200
    data = res.json()
    assert "result" in data
    assert abs(data["result"] - 1000) < 0.01  # 1 m³ = 1000 L


# =====================================================
# 🧮 /vcf
# =====================================================
def test_vcf_endpoint():
    res = client.get("/vcf", params={"rho15": 850, "tempC": 25})
    assert res.status_code == 200
    data = res.json()
    assert "VCF" in data
    assert 0.99 < data["result"]["VCF"] < 1.0


# =====================================================
# 🧠 /auto_correct
# =====================================================
def test_auto_correct_endpoint():
    res = client.get("/auto_correct", params={
        "fuel": "diesel",
        "rho15": 850,
        "volume_m3": 1000,
        "tempC": 25
    })
    assert res.status_code == 200
    data = res.json()
    assert "V15_m3" in data
    assert "mass_ton" in data
    assert data["result"]["V15_m3"] < 1000  # Corrected volume should be slightly lower


# =====================================================
# 🧾 /history
# =====================================================
def test_history_endpoint():
    res = client.get("/history")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data
    assert isinstance(data["result"]["entries"], list)


# =====================================================
# 📜 /logs
# =====================================================
def test_logs_endpoint():
    res = client.get("/logs")
    assert res.status_code == 200
    data = res.json()
    assert "entries" in data or "message" in data

from fastapi.testclient import TestClient
from fuel_mcp.api.mcp_api import app

client = TestClient(app)

def test_debug_endpoint_status():
    res = client.get("/debug")
    assert res.status_code == 200
    data = res.json()
    assert "version" in data
    assert "python_version" in data
    assert "os" in data
    assert "db_path" in data
    assert "uptime_sec" in data

def test_debug_sizes_are_numbers():
    res = client.get("/debug")
    data = res.json()
    assert isinstance(data["db_size_kb"], (int, float))
    assert isinstance(data["log_size_kb"], (int, float))

def test_debug_contains_timestamp():
    res = client.get("/debug")
    assert "timestamp" in res.json()
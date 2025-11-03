
"""
Quick Terminal Test — ASTM Smart Converter (Grouped & Dynamic Edition)
----------------------------------------------------------------------
Runs core conversions across all groups and prints results for verification.
"""

from fuel_mcp.core.unit_converter import convert
import requests

API_BASE = "http://127.0.0.1:8000"

# =====================================================
# 🔹 Helper for API-based conversions
# =====================================================
def test_api_density():
    print("\n🧪 API & Density Correlations (via MCP API)")
    tests = [
        ("API", "Relative Density", 30),
        ("API", "Density", 30),
        ("Relative Density", "API", 0.8762),
        ("Density", "API", 875.7),
    ]

    for f, t, v in tests:
        if f == "API":
            col = "api_gravity_60f"
        elif f == "Relative Density":
            col = "relative_density_60f"
        else:
            col = "density_15c_kg_per_m3"

        r = requests.get(
            f"{API_BASE}/correlate",
            params={
                "table": "ASTM_Table1_APIGravity60F_to_RelativeDensity60F_and_Density15C_norm",
                "column": col,
                "value": v,
            },
        )
        if r.status_code == 200:
            data = r.json().get("result", {}).get("outputs") or r.json().get("result", {}).get("output")
            print(f"{f} → {t} @ {v} = {data}")
        else:
            print(f"❌ Error {r.status_code}: {r.text}")


# =====================================================
# ⚖️ Mass / Weight
# =====================================================
def test_mass():
    print("\n⚖️ MASS / WEIGHT")
    tests = [
        ("kg", "lb", 1),
        ("tonne", "short_ton", 1),
        ("long_ton", "kg", 1),
    ]
    for f, t, v in tests:
        print(f"{v} {f} → {t} = {convert(v, f, t)}")


# =====================================================
# 🧴 Volume / Capacity
# =====================================================
def test_volume():
    print("\n🧴 VOLUME / CAPACITY")
    tests = [
        ("litre", "usg", 1),
        ("usg", "litre", 1),
        ("barrel", "litre", 1),
        ("m3", "barrel", 1),
    ]
    for f, t, v in tests:
        print(f"{v} {f} → {t} = {convert(v, f, t)}")


# =====================================================
# 📏 Length
# =====================================================
def test_length():
    print("\n📏 LENGTH")
    tests = [
        ("metre", "foot", 1),
        ("foot", "metre", 1),
        ("inch", "cm", 1),
    ]
    for f, t, v in tests:
        print(f"{v} {f} → {t} = {convert(v, f, t)}")


# =====================================================
# 🔹 Run All
# =====================================================
if __name__ == "__main__":
    print("🚀 ASTM Smart Converter — Terminal Test Suite")
    test_mass()
    test_volume()
    test_length()
    test_api_density()
    print("\n✅ Tests complete.\n")
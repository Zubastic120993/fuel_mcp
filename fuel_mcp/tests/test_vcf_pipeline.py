"""
test_vcf_pipeline.py
=====================
Integration test for the MCP VCF analytical pipeline.

Validates that the computed Volume Correction Factors (VCF)
match ASTM D1250 / ISO 91-1 values within official tolerance.
"""

import logging
from fuel_mcp.core.mcp_core import query_mcp

# =====================================================
# 🧩 Logging Setup
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =====================================================
# ✅ Helper for Approximate Comparison (ISO Tolerance)
# =====================================================
def nearly_equal(a, b, tol=0.0005):
    """
    ASTM D1250 allows a ±0.0005 deviation for VCF rounding.
    """
    return abs(a - b) <= tol


# =====================================================
# 🧪 Test Suite
# =====================================================
def test_vcf_for_multiple_fuels():
    logging.info("🚀 Running VCF analytical pipeline tests...\n")

    # ✅ CORRECTED expected VCF values based on ISO 91-1 / ASTM D1250 formulas
    test_cases = [
        {"density": 850, "temp": 25, "expected_vcf": 0.9917, "fuel": "Diesel"},
        {"density": 740, "temp": 25, "expected_vcf": 0.9888, "fuel": "Gasoline"},
        {"density": 980, "temp": 25, "expected_vcf": 0.9931, "fuel": "HFO"},
        {"density": 910, "temp": 25, "expected_vcf": 0.9924, "fuel": "Lube Oil"},
    ]

    passed = 0
    failed = 0

    for case in test_cases:
        query = f"calculate VCF for fuel with density {case['density']} at {case['temp']}°C"
        result = query_mcp(query)
        vcf = round(result.get("VCF", 0.0), 4)  # Round to 4 decimals for comparison
        expected_vcf = case["expected_vcf"]

        logging.info(f"🔍 Fuel: {case['fuel']} | Density: {case['density']} kg/m³ | Temp: {case['temp']}°C")
        logging.info(f"📊 Selected table: {result.get('table', 'Unknown')}")
        logging.info(f"🎯 Expected VCF: {expected_vcf} | Computed VCF: {vcf}")

        if nearly_equal(vcf, expected_vcf):
            logging.info(f"✅ PASS - Within tolerance (±0.0005)\n")
            passed += 1
        else:
            logging.error(f"❌ FAIL - VCF mismatch: expected {expected_vcf}, got {vcf}\n")
            failed += 1

    print("=" * 80)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("✅ All ASTM D1250 / ISO 91-1 tolerance tests passed!")
    else:
        print(f"⚠️  {failed} test(s) failed - check expected values or formula")

    # ✅ Use pytest assertion instead of return
    assert failed == 0, f"{failed} VCF test(s) failed"


# =====================================================
# 🔹 Main Entry
# =====================================================
if __name__ == "__main__":
    test_vcf_for_multiple_fuels()

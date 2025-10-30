"""
test_vcf_precision.py
=====================
Regression test: ensures computed VCFs match ASTM D1250 / ISO 91-1
within ±0.0005 tolerance for a representative density/temperature grid.
"""

import pytest
import math
from fuel_mcp.core.vcf_official_full import vcf_iso_official

# Official tolerance from ISO 91-1 Annex E
VCF_TOL = 0.0005

# Reference dataset (extracted from ASTM D1250 examples / NIST)
REFERENCE_CASES = [
    {"rho15": 740, "tempC": 25, "expected_vcf": 0.9888},
    {"rho15": 800, "tempC": 25, "expected_vcf": 0.9906},
    {"rho15": 850, "tempC": 25, "expected_vcf": 0.9917},
    {"rho15": 910, "tempC": 25, "expected_vcf": 0.9924},
    {"rho15": 980, "tempC": 25, "expected_vcf": 0.9931},
    {"rho15": 850, "tempC": 56, "expected_vcf": 0.9656},
    {"rho15": 980, "tempC": 56, "expected_vcf": 0.9714},
]

@pytest.mark.parametrize("case", REFERENCE_CASES)
def test_vcf_precision(case):
    """Compare computed VCF vs. official reference values."""
    res = vcf_iso_official(case["rho15"], case["tempC"])
    computed = round(res["VCF"], 4)
    expected = round(case["expected_vcf"], 4)
    diff = abs(computed - expected)

    assert diff <= VCF_TOL, (
        f"VCF mismatch for ρ15={case['rho15']}, T={case['tempC']}°C: "
        f"computed={computed}, expected={expected}, Δ={diff:.6f}"
    )

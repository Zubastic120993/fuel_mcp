"""
fuel_mcp/tests/test_regex_parser_cases.py
=========================================

Regression tests for regex-based natural query parser (v1.0.3-final-b)
Ensures full coverage for:
- Volume ↔ Mass conversions
- Temperature normalization
- Free-order syntax
- Fuel alias normalization (MGO → diesel, etc.)
"""

from fuel_mcp.core.regex_parser import process_query


def test_standard_volume_to_mass():
    result = process_query("convert 500 L diesel @ 30°C")
    assert "mass_ton" in result
    assert abs(result["mass_ton"] - 0.42) < 0.01
    assert result["mode"] == "convert"


def test_mass_to_volume_reverse():
    result = process_query("convert 2 tons of diesel to m3 @ 25°C")
    assert "volume_obs_m3" in result
    assert result["mode"] == "reverse"
    assert abs(result["V15_m3"] - 2.314) < 0.01


def test_vcf_calculation():
    result = process_query("calculate VCF for HFO at 25 degrees")
    assert "VCF" in result
    assert result["mode"] == "vcf"
    assert 0.99 < result["VCF"] < 1.0


def test_free_order_parsing():
    result = process_query("mass of diesel 50°C 10m³")
    assert result["mode"] == "convert"
    assert "mass_ton" in result
    assert abs(result["mass_ton"] - 8.25) < 0.1


def test_compact_lowercase_case():
    result = process_query("diesel 20c 500l")
    assert "mass_ton" in result
    assert result["mode"] == "convert"
    assert result["fuel"] == "diesel"


def test_alias_handling_for_mgo():
    result = process_query("mgo 35deg 200l")
    assert "mass_ton" in result
    assert result["fuel"] == "diesel"
    assert result["mode"] == "convert"


def test_mixed_case_spacing():
    result = process_query("10 m³ hfo at 30 degrees")
    assert "mass_ton" in result
    assert result["fuel"] == "hfo"
    assert result["mode"] == "convert"
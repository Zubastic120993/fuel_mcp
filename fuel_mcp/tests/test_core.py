import pytest

from fuel_mcp.core import conversion_engine, conversion_dispatcher, mcp_core, vcf_official_full

def test_conversion_engine_basic():
    """Check convert_density_to_mass produces valid result."""
    try:
        result = conversion_engine.convert_density_to_mass(850)
        assert isinstance(result, dict)
        assert result is not None
    except Exception as e:
        pytest.fail(f"conversion_engine failed: {e}")

def test_dispatcher_convert():
    """Verify conversion_dispatcher.convert works with sample input."""
    try:
        result = conversion_dispatcher.convert("density_to_mass", 850)
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"conversion_dispatcher failed: {e}")

def test_mcp_core_query():
    """Ensure MCP core query function responds."""
    try:
        result = mcp_core.query_mcp("convert density 850 to ton")
        assert isinstance(result, dict)
    except Exception as e:
        pytest.fail(f"mcp_core query failed: {e}")


def test_vcf_official_full():
    """Confirm VCF calculation works correctly."""
    try:
        result = vcf_official_full.vcf_iso_official(850, 25)
        assert isinstance(result, dict)
        assert "VCF" in (result.keys() or [])
    except Exception as e:
        pytest.fail(f"vcf_official_full failed: {e}")

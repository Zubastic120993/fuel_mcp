import pytest
from fuel_mcp.core import mcp_core

def test_full_pipeline_density_to_mass():
    """
    ✅ Integration test: end-to-end MCP query pipeline.
    Covers:
      - query parsing
      - table retrieval (RAG)
      - conversion execution
      - structured output verification
    """
    try:
        query = "convert density 850 to ton at 25C"
        result = mcp_core.query_mcp(query)

                # Structure checks
        assert isinstance(result, dict), "Result must be a dictionary"
        assert "_meta" in result, "Missing _meta section"
        meta = result["_meta"]
        assert "selected_table" in meta, "No table reference in meta"
        assert "timestamp" in meta, "Missing timestamp"
        assert any("ton" in k or "mass" in k for k in result.keys()), "No mass-related output fields"


        # Logical checks (sanity)
        if "mass" in str(result).lower():
            assert any(str(v).replace(".", "", 1).isdigit() for v in result.values()), "No numeric output found"
    except Exception as e:
        pytest.fail(f"Pipeline integration test failed: {e}")

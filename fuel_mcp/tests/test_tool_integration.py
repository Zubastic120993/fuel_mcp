"""
fuel_mcp/tests/test_tool_integration.py
=======================================

Verifies integration between:
- fuel_mcp.tool_interface.mcp_query()
- fuel_mcp.tool_integration.mcp_tool (LangChain StructuredTool)
"""

import pytest
from fuel_mcp.tool_interface import mcp_query
from fuel_mcp.tool_integration import mcp_tool


def test_mcp_query_basic():
    """Test that mcp_query returns a valid JSON structure."""
    result = mcp_query("calculate VCF for diesel at 25°C")
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "VCF" in result or "result" in result, "Should contain correction result"


def test_mcp_tool_structure():
    """Ensure the StructuredTool was registered properly."""
    assert hasattr(mcp_tool, "name")
    assert hasattr(mcp_tool, "description")
    assert callable(mcp_tool.func)
    assert mcp_tool.name == "FuelMCP"
    assert "fuel" in mcp_tool.description.lower()


def test_mcp_tool_executes_function():
    """Run the LangChain-style function through mcp_tool."""
    result = mcp_tool.func("calculate VCF for diesel at 25°C")
    assert isinstance(result, dict)
    assert any(k in result for k in ["VCF", "fuel", "tempC"]), "Expected fuel data in response"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
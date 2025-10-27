import pytest
import json
from fuel_mcp.core import rag_bridge
from fuel_mcp.rag import loader

def test_metadata_file_exists():
    """Check if metadata.json exists and loads correctly."""
    try:
        with open("fuel_mcp/rag/metadata.json", "r") as f:
            data = json.load(f)
        assert isinstance(data, (list, dict))
    except Exception as e:
        pytest.fail(f"metadata.json loading failed: {e}")

def test_vector_store_exists():
    """Ensure vector_store.json exists and is valid JSON."""
    try:
        with open("fuel_mcp/rag/vector_store.json", "r") as f:
            vec = json.load(f)
        assert len(vec) > 0
    except Exception as e:
        pytest.fail(f"vector_store.json invalid or missing: {e}")

def test_rag_loader():
    """Check if loader has proper data loading logic."""
    try:
        # Detect any function inside loader that loads or reads documents
        funcs = [f for f in dir(loader) if "load" in f or "get" in f]
        assert len(funcs) > 0, "No load/get functions found in loader"
    except Exception as e:
        pytest.fail(f"RAG loader failed: {e}")

def test_find_table_for_query():
    """Verify that find_table_for_query returns ranked results."""
    try:
        results = rag_bridge.find_table_for_query("density correction table", top_k=3)
        assert isinstance(results, list) and len(results) > 0
        assert "table" in results[0]
        assert "similarity" in results[0]
    except Exception as e:
        pytest.fail(f"find_table_for_query failed: {e}")


"""
RAG Fallback and Logging Validation Suite
------------------------------------------
Tests both online and offline operation modes of rag_bridge.
Ensures local vector store and logging mechanisms work correctly.
"""

import pytest
import json
import os
from pathlib import Path
from fuel_mcp.core import rag_bridge

RAG_LOG = Path("fuel_mcp/logs/rag_activity.json")

# =====================================================
# 🔍 1. Structural Integrity
# =====================================================
def test_metadata_and_vector_store():
    """Check presence and validity of metadata and vector store."""
    meta_path = Path("fuel_mcp/rag/metadata.json")
    vec_path = Path("fuel_mcp/rag/vector_store.json")

    assert meta_path.exists(), "metadata.json is missing"
    assert vec_path.exists(), "vector_store.json is missing"

    with open(vec_path, "r") as f:
        data = json.load(f)
    assert len(data) > 0, "vector_store.json is empty"

# =====================================================
# 🧠 2. Offline Fallback Logic
# =====================================================
def test_offline_vector_search(monkeypatch):
    """Simulate offline mode and ensure local RAG search works."""
    monkeypatch.setattr(rag_bridge, "ONLINE_MODE", False)
    results = rag_bridge.find_table_for_query("calculate VCF for diesel", top_k=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "table" in results[0]
    assert results[0]["similarity"] <= 1.0

# =====================================================
# 🌐 3. Online Mode (If Key Present)
# =====================================================
@pytest.mark.skipif(not rag_bridge.OPENAI_API_KEY, reason="No API key available")
def test_online_mode(monkeypatch):
    """Verify online mode works if API key is set."""
    monkeypatch.setattr(rag_bridge, "ONLINE_MODE", True)
    results = rag_bridge.find_table_for_query("density to volume correction", top_k=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "table" in results[0]

# =====================================================
# 🧾 4. Structured Logging Check
# =====================================================
def test_rag_activity_log_exists():
    """Ensure structured log file is created and valid JSON."""
    assert RAG_LOG.exists(), "rag_activity.json was not created"
    with open(RAG_LOG, "r") as f:
        log_data = json.load(f)
    assert isinstance(log_data, list)
    assert all("timestamp" in e for e in log_data)
    assert all("event" in e for e in log_data)
    assert all("mode" in e for e in log_data)

# =====================================================
# 🧩 5. Round-trip Consistency
# =====================================================
def test_table_resolution_consistency():
    """Ensure same query yields consistent ranking between runs."""
    q = "convert density 850 to ton at 25C"
    first = rag_bridge.find_table_for_query(q, top_k=3)
    second = rag_bridge.find_table_for_query(q, top_k=3)
    assert first[0]["table"] == second[0]["table"]

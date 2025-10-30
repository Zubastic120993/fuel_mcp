
"""
fuel_mcp/tests/test_async_logger.py
===================================

Tests async and sync fallback behavior for async_logger.
"""

import asyncio
import pytest
from fuel_mcp.core import async_logger


# -----------------------------------------------------
# 🧠 TEST: Async query logging within event loop
# -----------------------------------------------------
@pytest.mark.asyncio
async def test_async_query_logging(monkeypatch):
    """Ensure async log_query_async schedules properly inside event loop."""
    called = {}

    def fake_log_query(query, result, mode, success):
        called["ok"] = (query, result, mode, success)

    monkeypatch.setattr(async_logger, "log_query", fake_log_query)

    async_logger.log_query_async("test_query", {"a": 1}, "test_mode", True)
    await asyncio.sleep(0.1)  # allow task to run

    assert "ok" in called
    assert called["ok"][0] == "test_query"
    assert called["ok"][2] == "test_mode"


# -----------------------------------------------------
# ⚡ TEST: Sync fallback when no event loop is active
# -----------------------------------------------------
def test_sync_fallback(monkeypatch):
    """Ensure log_query_async runs synchronously when no event loop is active."""
    called = {}

    def fake_log_query(query, result, mode, success):
        called["sync"] = True

    monkeypatch.setattr(async_logger, "log_query", fake_log_query)

    # Force RuntimeError to simulate missing event loop
    monkeypatch.setattr(async_logger, "asyncio", type("FakeAsyncio", (), {
        "create_task": staticmethod(lambda *_: (_ for _ in ()).throw(RuntimeError("no loop"))),
    }))

    async_logger.log_query_async("test_fallback", {}, "sync_test", True)
    assert "sync" in called


# -----------------------------------------------------
# 🧱 TEST: Async error logging (module + message)
# -----------------------------------------------------
@pytest.mark.asyncio
async def test_async_error_logging(monkeypatch):
    """Ensure async error log schedules properly."""
    called = {}

    def fake_log_error(module, message):
        called["err"] = (module, message)

    monkeypatch.setattr(async_logger, "log_error", fake_log_error)

    async_logger.log_error_async("core", "simulated failure")
    await asyncio.sleep(0.1)

    assert "err" in called
    assert called["err"][0] == "core"
    assert "failure" in called["err"][1]
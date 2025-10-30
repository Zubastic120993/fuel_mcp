"""
fuel_mcp/core/async_logger.py
=============================

Asynchronous wrapper for DB logging — ensures that inserts
to SQLite (queries/errors) never block FastAPI response time.
"""

import asyncio
import logging
from fuel_mcp.core.db_logger import log_query, log_error


async def _run_in_thread(func, *args, **kwargs):
    """Run blocking function inside a thread pool executor."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


def _has_event_loop() -> bool:
    """Check if an asyncio event loop is currently running."""
    try:
        asyncio.get_running_loop()
        return True
    except Exception:
        return False


def log_query_async(query: str, result: dict | str, mode: str, success: bool):
    """Schedule async non-blocking query log."""
    if _has_event_loop():
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_run_in_thread(log_query, query, result, mode, success))
            return
        except Exception as e:
            logging.warning(f"⚠️ Async log scheduling failed: {e}")

    # fallback if no event loop
    logging.warning("⚠️ Async log fallback → running synchronously.")
    try:
        log_query(query, result, mode, success)
    except Exception as e:
        logging.error(f"❌ Sync log_query fallback failed: {e}")


def log_error_async(module: str, message: str):
    """Schedule async non-blocking error log."""
    if _has_event_loop():
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(_run_in_thread(log_error, module, message))
            return
        except Exception as e:
            logging.warning(f"⚠️ Async error scheduling failed: {e}")

    # fallback if no event loop
    logging.warning("⚠️ Async error log fallback → running synchronously.")
    try:
        log_error(module, message)
    except Exception as e:
        logging.error(f"❌ Sync log_error fallback failed: {e}")
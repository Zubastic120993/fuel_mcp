"""
fuel_mcp/tool_interface.py
==========================

Agent-facing interface for the Fuel MCP engine.
Provides a unified callable entry point for external tools,
such as LangChain, Flowise, or OpenAI function calls.

Example:
---------
from fuel_mcp.tool_interface import mcp_query

result = mcp_query("calculate VCF for diesel at 25°C")
print(result)
"""

import json
import os
from typing import Dict, Any

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.error_handler import log_error


def mcp_query(prompt: str) -> Dict[str, Any]:
    """
    Handles user or agent query for the MCP engine.

    Automatically detects ONLINE or OFFLINE mode,
    delegates the query to MCP Core, and applies
    structured error handling.
    """
    mode = "ONLINE" if os.getenv("OPENAI_API_KEY") else "OFFLINE"

    try:
        response = query_mcp(prompt)

        # Standardize the result structure for external tools
        if isinstance(response, dict):
            response.update({
                "mode": mode,
                "success": True,
                "query": prompt
            })
            return response

        return {
            "mode": mode,
            "success": True,
            "query": prompt,
            "result": response
        }

    except Exception as e:
        # Log and return a consistent structured error
        log_error(e, query=prompt, module="tool_interface")
        return {
            "mode": mode,
            "success": False,
            "query": prompt,
            "error": str(e)
        }


if __name__ == "__main__":
    # Local CLI-style test
    test_prompt = "calculate VCF for diesel at 25°C"
    print(json.dumps(mcp_query(test_prompt), indent=2))
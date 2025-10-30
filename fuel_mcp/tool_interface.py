
"""
fuel_mcp/tool_interface.py
==========================

Agent-facing interface for the Fuel MCP engine.
Provides a unified callable entry point for external tools,
such as LangChain, Flowise, or OpenAI function calls.

Example:
---------
from fuel_mcp.tool_interface import mcp_query

result = mcp_query("calculate VCF for diesel at 25°C and 850 kg/m³")
print(result)
"""

import json
import os
from typing import Dict, Any

from fuel_mcp.core.mcp_core import query_mcp


def mcp_query(prompt: str) -> Dict[str, Any]:
    """
    Handle user or agent query for the MCP engine.

    Automatically detects whether the system is in ONLINE (API) or OFFLINE mode
    depending on the availability of OPENAI_API_KEY or internet access.

    Parameters
    ----------
    prompt : str
        Natural language or structured text query.

    Returns
    -------
    dict
        Structured response from MCP Core, including mode and result.
    """
    mode = "ONLINE" if os.getenv("OPENAI_API_KEY") else "OFFLINE"
    try:
        response = query_mcp(prompt)
        return {
            "mode": mode,
            "success": True,
            "query": prompt,
            "result": response,
        }
    except Exception as e:
        return {
            "mode": mode,
            "success": False,
            "query": prompt,
            "error": str(e),
        }


if __name__ == "__main__":
    # Local CLI-style test
    test_prompt = "convert 1000 liters of diesel at 25°C to mass in tons"
    print(json.dumps(mcp_query(test_prompt), indent=2))
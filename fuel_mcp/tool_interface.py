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
import re
from typing import Dict, Any

from fuel_mcp.core.mcp_core import query_mcp
from fuel_mcp.core.vcf_official_full import vcf_iso_official


def mcp_query(prompt: str) -> Dict[str, Any]:
    """
    Handle user or agent query for the MCP engine.

    Automatically detects whether the system is in ONLINE (API) or OFFLINE mode
    depending on the availability of OPENAI_API_KEY or internet access.
    Includes fallback logic for common patterns like VCF or conversion queries.
    """
    mode = "ONLINE" if os.getenv("OPENAI_API_KEY") else "OFFLINE"
    prompt_clean = prompt.strip().lower()

    try:
        # =====================================================
        # 🔹 1. Detect direct VCF query pattern
        # =====================================================
        if "vcf" in prompt_clean:
            match_temp = re.search(r"(\d{1,3})\s*°?\s*c", prompt_clean)
            if match_temp:
                tempC = float(match_temp.group(1))
                if "diesel" in prompt_clean:
                    rho15 = 850.0
                    fuel = "diesel"
                elif "hfo" in prompt_clean:
                    rho15 = 991.0
                    fuel = "hfo"
                elif "lpg" in prompt_clean:
                    rho15 = 540.0
                    fuel = "lpg"
                else:
                    rho15 = 940.0
                    fuel = "unknown"

                result = vcf_iso_official(rho15=rho15, tempC=tempC)
                # ✅ Flatten output for tests
                result.update({
                    "fuel": fuel,
                    "rho15": rho15,
                    "tempC": tempC,
                    "mode": mode,
                    "success": True,
                    "query": prompt,
                })
                return result

        # =====================================================
        # 🔹 2. Otherwise, use full semantic MCP engine
        # =====================================================
        response = query_mcp(prompt)
        if isinstance(response, dict) and any(k in response for k in ["VCF", "fuel", "tempC"]):
            response.update({"mode": mode, "success": True, "query": prompt})
            return response
        else:
            # ✅ Fixed — added parentheses for unpacking conditional dict
            return {
                "mode": mode,
                "success": True,
                "query": prompt,
                **(response if isinstance(response, dict) else {"result": response}),
            }

    except Exception as e:
        return {
            "mode": mode,
            "success": False,
            "query": prompt,
            "error": str(e),
        }


if __name__ == "__main__":
    test_prompt = "calculate VCF for diesel at 25°C"
    print(json.dumps(mcp_query(test_prompt), indent=2))
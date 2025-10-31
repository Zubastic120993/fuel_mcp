"""
fuel_mcp/tool_integration.py
============================

LangChain-compatible + OpenAI-compatible wrapper for the Fuel MCP engine.
Allows MCP to be registered as:
  • LangChain `StructuredTool`
  • Flowise custom node
  • OpenAI "function calling" tool schema

Example (LangChain):
--------------------
from fuel_mcp.tool_integration import mcp_tool
agent = initialize_agent([mcp_tool], llm=llm)
result = agent.run("calculate VCF for HFO at 30°C")

Example (OpenAI Tools):
-----------------------
from fuel_mcp.tool_integration import tool_schema
tools = [tool_schema()]
client.chat.completions.create(model="gpt-4.1", messages=[...], tools=tools)
"""

from langchain_core.tools import StructuredTool
from fuel_mcp.tool_interface import mcp_query


# ------------------------------------------------------------
# 🔧 Define MCP Tool (LangChain new API)
# ------------------------------------------------------------
mcp_tool = StructuredTool.from_function(
    func=mcp_query,
    name="FuelMCP",
    description=(
        "Performs marine fuel mass–volume–temperature corrections using "
        "ASTM D1250 / ISO 91-1 tables and analytical methods. "
        "Supports queries like 'calculate VCF for diesel at 25 °C'."
    ),
)


# ------------------------------------------------------------
# 🧩 Export OpenAI-compatible Tool Schema
# ------------------------------------------------------------
def tool_schema() -> dict:
    """
    Returns the OpenAI function-calling JSON schema for Fuel MCP.
    Useful for Flowise or OpenAI Agents.
    """
    try:
        return mcp_tool.to_openai_function()
    except Exception as e:
        return {
            "type": "function",
            "function": {
                "name": "FuelMCP",
                "description": "Marine fuel correction processor tool.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural-language query such as 'calculate VCF for diesel at 25 °C'.",
                        }
                    },
                    "required": ["query"],
                },
            },
            "error": str(e),
        }


# ------------------------------------------------------------
# 🧪 Local Test
# ------------------------------------------------------------
if __name__ == "__main__":
    print("🧩 LangChain Tool registered successfully:")
    print("   →", mcp_tool.name)
    print("   →", mcp_tool.description)
    print("\n🧱 OpenAI Tool Schema Preview:")
    import json
    print(json.dumps(tool_schema(), indent=2))
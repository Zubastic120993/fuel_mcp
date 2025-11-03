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

from fuel_mcp.tool_interface import mcp_query

# ================================================================
# 🧩 Safe Import (Fallback if LangChain not installed)
# ================================================================
try:
    from langchain_core.tools import StructuredTool
    LANGCHAIN_AVAILABLE = True
except ModuleNotFoundError:
    print("⚙️ LangChain not available — running in GUI-only mode.")
    LANGCHAIN_AVAILABLE = False
    StructuredTool = None

# ================================================================
# 🔧 Define MCP Tool (LangChain new API)
# ================================================================
if LANGCHAIN_AVAILABLE:
    mcp_tool = StructuredTool.from_function(
        func=mcp_query,
        name="FuelMCP",
        description=(
            "Performs marine fuel mass–volume–temperature corrections using "
            "ASTM D1250 / ISO 91-1 tables and analytical methods. "
            "Supports queries like 'calculate VCF for diesel at 25 °C'."
        ),
    )
else:
    # Dummy placeholder for GUI-only or lightweight builds
    class DummyTool:
        name = "FuelMCP"
        description = (
            "Marine fuel correction processor tool (LangChain not installed)."
        )

        def run(self, *args, **kwargs):
            raise RuntimeError("LangChain integration not available in this build.")

    mcp_tool = DummyTool()


# ================================================================
# 🧩 Export OpenAI-compatible Tool Schema
# ================================================================
def tool_schema() -> dict:
    """
    Returns the OpenAI function-calling JSON schema for Fuel MCP.
    Useful for Flowise or OpenAI Agents.
    """
    if not LANGCHAIN_AVAILABLE:
        return {
            "type": "function",
            "function": {
                "name": "FuelMCP",
                "description": "Marine fuel correction processor tool (LangChain not installed).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query such as 'calculate VCF for diesel at 25 °C'.",
                        }
                    },
                    "required": ["query"],
                },
            },
        }

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
                            "description": "Query such as 'calculate VCF for diesel at 25 °C'.",
                        }
                    },
                    "required": ["query"],
                },
            },
            "error": str(e),
        }


# ================================================================
# 🧪 Local Test
# ================================================================
if __name__ == "__main__":
    import json

    print("🧩 Tool module loaded.")
    print(f"→ LangChain available: {LANGCHAIN_AVAILABLE}")
    print(f"→ Tool name: {mcp_tool.name}")
    print(f"→ Description: {mcp_tool.description}")

    print("\n🧱 OpenAI Tool Schema Preview:")
    print(json.dumps(tool_schema(), indent=2))
# 🧩 Fuel MCP — Changelog

## [1.0.0-agent-integration] — 2025-10-30

### 🚀 New Features
- **LangChain Agent Integration**
  - Added `tool_interface.py` with unified callable entry point `mcp_query()`.
  - Integrated fallback logic for VCF queries and semantic engine delegation.
  - Supports both **ONLINE** (OpenAI API) and **OFFLINE** (local embedding) modes.

- **LangChain Tool Adapter**
  - Implemented `fuel_mcp/tool_integration.py` providing `mcp_tool` (LangChain-style Tool wrapper).
  - Enables smooth integration with agents and external orchestration layers.

- **Flowise Node Definition**
  - Added `/fuel_mcp/flowise/fuel_mcp_node.js` defining “⚓ Fuel MCP Node” for Flowise drag-and-drop pipelines.

- **Testing Suite**
  - Added `fuel_mcp/tests/test_tool_integration.py` — verifies query behavior, schema, and tool function execution.
  - All tests pass successfully (`pytest -v` → ✅ 3/3).

- **Dependency Management**
  - Added optional dependency group `[project.optional-dependencies].agent` in `pyproject.toml`  
    Includes `langchain`, `langchain-community`, `langchain-core`, and `openai`.
  - Updated `requirements-lock.txt` accordingly.

### 🧰 Internal Improvements
- Refined query handling to auto-detect VCF expressions and infer `rho15` by fuel type.
- Ensured robust JSON structure in responses to support agentic workflows and LangChain serialization.

---

✅ **All tests passed:** `pytest fuel_mcp/tests/test_tool_integration.py -v`


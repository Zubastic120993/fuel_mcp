# 🧩 Fuel MCP — Changelog

## [v1.0.0-agent-integration] — 2025-10-30
### 🚀 New Features

- **LangChain Agent Integration**
  - Introduced `tool_interface.py` with unified callable entry point `mcp_query()`.
  - Added intelligent fallback logic for both **VCF** and **semantic queries**.
  - Supports dual operation modes:
    - **ONLINE:** via OpenAI API (real-time inference)
    - **OFFLINE:** via local embedding model (`nomic-embed-text-v1.5`)

- **LangChain Tool Adapter**
  - Implemented `fuel_mcp/tool_integration.py`, providing `mcp_tool` — a LangChain-compatible `Tool` wrapper.
  - Enables seamless use of Fuel MCP inside **LangChain**, **Flowise**, or **custom LLM agents**.

- **Flowise Node Integration**
  - Added `/fuel_mcp/flowise/fuel_mcp_node.js` defining the “⚓ Fuel MCP Node” for Flowise’s drag-and-drop pipelines.
  - Includes schema metadata, description, and endpoint mapping for direct API execution.

- **Test Coverage for Agent Mode**
  - Added `fuel_mcp/tests/test_tool_integration.py` — validates:
    - Tool schema structure  
    - Query dispatch via `mcp_query()`  
    - Agent compatibility layer behavior
  - ✅ All tests pass successfully (`pytest -v` → 3/3).

- **Dependency Management**
  - Introduced optional dependency group `[project.optional-dependencies].agent` in `pyproject.toml`, including:
    - `langchain`, `langchain-community`, `langchain-core`, `openai`
  - Updated `requirements-lock.txt` for agent-ready installations.

---

### 🧰 Internal Improvements
- Refined query logic in `query_mcp()` to auto-detect expressions like  
  `"calculate VCF for diesel at 25°C"` or `"convert 500 L to tons"`.
- Implemented automatic `rho15` inference based on fuel type (via JSON density map).
- Standardized response schema for agent workflows:
  ```json
  {
    "success": true,
    "mode": "vcf",
    "query": "calculate VCF for diesel at 25°C",
    "result": { "VCF": 0.9915 },
    "_meta": { "engine": "offline", "source": "local model" }
  }
  ```
- Enhanced compatibility with **LangChain serialization** for structured logging and tool registration.

---

✅ **All Tests Passed**
```bash
pytest fuel_mcp/tests/test_tool_integration.py -v
```

---

### 📦 Summary
| Component | Status |
|------------|--------|
| Agent Integration | ✅ Complete |
| Flowise Node | ✅ Complete |
| LangChain Tool Wrapper | ✅ Complete |
| Offline/Online Mode | ✅ Complete |
| Density Mapping | ⚙️ In Progress (extended version planned for v1.0.3) |
| Unified Schema Standardization | ⚙️ In Progress |

---

**Maintainer:** Chief Engineer **Volodymyr Zub**  
📧 [your.email@example.com](mailto:your.email@example.com)  
🏷️ “Precision Engineering for Smarter Maritime Operations”

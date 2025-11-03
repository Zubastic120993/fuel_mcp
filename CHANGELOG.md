# 🧩 Fuel MCP — Changelog

All notable changes to the Fuel MCP project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.5.0] — 2025-11-03
### Current Release
- Project structure stabilized
- Modular GUI architecture in `fuel_mcp/gui_astm/`
- Docker deployment with compose configuration
- Full CLI tooling via `mcp-cli`
- Database maintenance and vacuum operations
- Comprehensive test coverage (56+ tests)

---

## [v1.0.3] — 2025-10-31
### 🚀 Major Features
- **Unified Response Schema**
  - Introduced `fuel_mcp/core/response_schema.py`
  - All API endpoints standardized (`/query`, `/vcf`, `/convert`, `/auto_correct`)
  - Consistent `result` + `_meta` structure across all responses

- **Regex Parser & NLP**
  - Natural language query parsing: `"convert 500 L diesel @ 30°C"`
  - Reverse conversion support: `"2 tons → m³"`
  - Flexible syntax and alias mapping (MGO→diesel, IFO380→HFO)

- **Enhanced CLI Toolkit**
  - `mcp-cli status` - System status and log info
  - `mcp-cli db stats` - Database statistics
  - `mcp-cli db clean --days 30` - Log cleanup
  - `mcp-cli db vacuum` - Database optimization
  - `mcp-cli vcf <fuel> <temp>` - Quick VCF calculations
  - `mcp-cli convert "<query>"` - Conversion queries

- **Dynamic Fuel Density Loader**
  - JSON-based density retrieval and validation
  - Support for all marine fuels (diesel, HFO, MGO, LNG, methanol)
  - Automatic density inference from fuel type

### 🧰 Internal Improvements
- Enhanced `/metrics` endpoint with uptime tracking and version info
- Improved `/errors` endpoint with module filtering
- Enhanced `/debug` endpoint with system diagnostics
- Auto-changelog generator
- Full database logging with async support
- Reverse conversion logic for mass↔volume transformations

### 📊 Testing
- ✅ 56 tests passed / 1 skipped (no API key)
- Full coverage for regex parser, API endpoints, metrics, and errors

**Detailed documentation:** See `docs/Fuel_MCP_v1.0.3_Consolidated_Report.md` and `docs/CHANGELOG_v1.0.3.md`

---

## [v1.0.0] — 2025-10-30
### 🚀 Agent Integration Release

- **LangChain Agent Integration**
  - Introduced `tool_interface.py` with unified callable entry point `mcp_query()`
  - Added intelligent fallback logic for both **VCF** and **semantic queries**
  - Supports dual operation modes:
    - **ONLINE:** via OpenAI API (real-time inference)
    - **OFFLINE:** via local embedding model (`nomic-embed-text-v1.5`)

- **LangChain Tool Adapter**
  - Implemented `fuel_mcp/tool_integration.py`, providing `mcp_tool` — a LangChain-compatible `Tool` wrapper
  - Enables seamless use of Fuel MCP inside **LangChain**, **Flowise**, or **custom LLM agents**

- **Flowise Node Integration**
  - Added `/fuel_mcp/flowise/fuel_mcp_node.js` defining the "⚓ Fuel MCP Node" for Flowise's drag-and-drop pipelines
  - Includes schema metadata, description, and endpoint mapping for direct API execution

- **Test Coverage for Agent Mode**
  - Added `fuel_mcp/tests/test_tool_integration.py`
  - Validates tool schema structure, query dispatch, and agent compatibility
  - ✅ All tests pass successfully

- **Dependency Management**
  - Introduced optional dependency group `[project.optional-dependencies].agent` in `pyproject.toml`
  - Includes: `langchain`, `langchain-community`, `langchain-core`, `openai`

### 🧰 Internal Improvements
- Refined query logic to auto-detect expressions like `"calculate VCF for diesel at 25°C"`
- Implemented automatic `rho15` inference based on fuel type (via JSON density map)
- Standardized response schema for agent workflows
- Enhanced compatibility with **LangChain serialization** for structured logging and tool registration

---

## Version Roadmap

| Version | Focus | Status |
|---------|-------|--------|
| v1.5.0 | Current stable release | ✅ Released |
| v1.0.3 | Schema unification, CLI, NLP parser | ✅ Released |
| v1.0.0 | Agent integration | ✅ Released |
| v1.6.0 | GUI enhancements | 🔄 In Progress |
| v2.0.0 | Extended fuel blending, API v2 | 📋 Planned |

---

**Maintainer:** Chief Engineer **Volodymyr Zub**  
📧 Contact: [your.email@example.com](mailto:your.email@example.com)  
🏷️ "Precision Engineering for Smarter Maritime Operations"

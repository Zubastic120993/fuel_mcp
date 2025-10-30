# Fuel MCP TODO — Do not edit directly
# Central tracking file for all ongoing and planned development tasks.

# TODO — Fuel MCP Development Roadmap  
Version: 1.0.0-standalone  
Maintainer: Chief Engineer Volodymyr Zub  
Last Updated: 2025-10-30  

---

## TODO 1 — Agent Integration (feature/agent-integration)

- Create `fuel_mcp/tool_interface.py` with function `mcp_query(prompt: str)` calling `query_mcp()`.
- Add offline/online mode handling inside `mcp_query()`.
- Add LangChain Tool adapter in `tool_integration.py`.
- Create Flowise custom node definition JSON for MCP.
- Add `/tool` endpoint in FastAPI returning OpenAI tool schema.
- Add unit tests (`tests/test_tool_integration.py`).
- Add optional dependencies group `[project.optional-dependencies].agent` with `langchain`, `openai`.

---

## TODO 2 — Standalone App (feature/standalone-app)

- Expand FastAPI endpoints: `/convert`, `/vcf`, `/units`, unify dispatcher calls.
- Finalize GUI frontend (`app_ui.py`) using PySide6 or Gradio.
- Add local database logging (SQLite or TinyDB) for persistent history.
- Implement `/history` endpoint returning stored queries.
- Create `Dockerfile` and optional `docker-compose.yml` for deployment.

---

## TODO 3 — Common Core Enhancements

- Add CLI entry point `mcp-cli` to run from terminal.  
- Auto-create required folders (`/data`, `/logs`, `.env`) at first startup.  
- Integrate `vcf_official_full.py` analytical engine directly into `query_mcp()`.  
- Add structured error logger `logs/errors.json` for all exceptions.  

---

## TODO 4 — Developer Documentation

- Create `docs/README_Developer.md` explaining internal architecture (API, Core, RAG flow).  
- Add architecture diagram (User/API → Core → Dispatcher → Output).  
- Add `CHANGELOG.md` for version updates.  
- Add `CONTRIBUTING.md` for contribution guidelines.  
- Add license field (`license = "MIT"`) to `pyproject.toml`.  
- Add Python version / license badges to top of README.md.  

---

## TODO 5 — Optional Polish & Automation

- Update `.gitignore` to exclude `/dist`, `/build`, `.egg-info`, `.pytest_cache`.  
- Add GitHub Actions CI pipeline running `pytest` on push.  
- Add Docker Hub or GHCR publish workflow for container image deployment.  

---

## TODO 6 — Upcoming Features (Fuel Tool Expansion)

- Add advanced VCF and blending logic in `fuel_mcp/core/calculations.py`.  
- Add heating energy calculations (kWh/day ↔ MJ/kg).  
- Add viscosity–temperature correlation for HFO.  
- Add new API endpoint `/fuel_tool`.  
- Add new tests `test_fuel_tool_advanced.py`.  

---

## TODO 7 — Planned Version Sequence

- v1.0.1 — CLI entry point, folder auto setup, structured error logs  
- v1.1.0 — SQLite logging, `/history`, GUI frontend  
- v1.2.0 — Agent integration (LangChain + OpenAI tools)  
- v1.3.0 — Dockerized build, CI automation  
- v1.4.0 — Advanced fuel tool (blending, energy, viscosity)  

---

Generated: 2025-10-30  
Author: Chief Engineer Volodymyr Zub  
Project: Fuel MCP — Marine Fuel Correction Processor  
Motto: Precision Engineering for Smarter Maritime Operations  
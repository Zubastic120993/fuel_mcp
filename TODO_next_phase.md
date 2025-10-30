# ✅ Fuel MCP Development Roadmap — Updated 2025-10-30

**Version:** 1.0.1 (Stable)  
**Maintainer:** Chief Engineer Volodymyr Zub  
**Project:** *Fuel MCP — Marine Fuel Correction Processor*  
**Motto:** *Precision Engineering for Smarter Maritime Operations*

---

## ✅ TODO 1 — Agent Integration (`feature/agent-integration`)

| Task | Status |
|------|--------|
| Create `fuel_mcp/tool_interface.py` with `mcp_query()` calling `query_mcp()` | ✅ Done |
| Offline/Online mode handling inside `mcp_query()` | ✅ Done |
| LangChain Tool adapter in `tool_integration.py` | ✅ Done |
| Flowise custom node definition JSON for MCP | ✅ Done |
| `/tool` endpoint in FastAPI returning OpenAI tool schema | ✅ Done |
| Unit tests (`tests/test_tool_integration.py`) | ✅ Passed |
| Optional dependencies group `[project.optional-dependencies].agent` | ✅ Added |

---

## ⚙️ TODO 2 — Standalone App (`feature/standalone-app`)

| Task | Status |
|------|--------|
| Expand FastAPI endpoints (`/convert`, `/vcf`, `/units`) | ⚙️ In Progress |
| Implement `/history` endpoint | ✅ Done |
| GUI frontend (`app_ui.py`) using PySide6 / Gradio | ⏳ Pending |
| Local database logging (SQLite / TinyDB) | ⏳ Pending |
| `Dockerfile` and `docker-compose.yml` for deployment | ⏳ Pending |

---

## ✅ TODO 3 — Common Core Enhancements

| Task | Status |
|------|--------|
| CLI entry point `mcp-cli` to run from terminal | ✅ Done |
| Auto-create folders (`/data`, `/logs`, `.env`) at startup | ✅ Done |
| Integrate `vcf_official_full.py` into `query_mcp()` | ✅ Done |
| Structured error logger (`logs/errors.json`) | ✅ Done |

---

## ⚙️ TODO 4 — Developer Documentation

| Task | Status |
|------|--------|
| `docs/README_Developer.md` architecture overview | ⚙️ Next |
| Architecture diagram (User/API → Core → Dispatcher → Output) | ⏳ Pending |
| `CHANGELOG.md` for version updates | ⏳ Pending |
| `CONTRIBUTING.md` guidelines | ⏳ Pending |
| License field (`MIT`) in `pyproject.toml` | ✅ Done |
| Python version + license badges in `README.md` | ⏳ Pending |

---

## ⚙️ TODO 5 — Optional Polish & Automation

| Task | Status |
|------|--------|
| Update `.gitignore` to exclude build/test artifacts | ✅ Done |
| GitHub Actions CI pipeline running `pytest` | ⏳ Pending |
| Docker Hub / GHCR publish workflow | ⏳ Pending |

---

## ⚙️ TODO 6 — Upcoming Features (Fuel Tool Expansion)

| Task | Status |
|------|--------|
| Advanced VCF + blending logic in `core/calculations.py` | ⏳ Pending |
| Heating energy calculations (kWh/day ↔ MJ/kg) | ⏳ Pending |
| Viscosity–temperature correlation for HFO | ⏳ Pending |
| New API endpoint `/fuel_tool` | ⏳ Pending |
| New tests `test_fuel_tool_advanced.py` | ⏳ Pending |

---

## ✅ TODO 7 — Version Sequence

| Version | Features |
|----------|-----------|
| **v1.0.1** | CLI entry point, auto setup, structured logs ✅ |
| **v1.1.0** | SQLite logging, `/history`, GUI frontend |
| **v1.2.0** | Agent integration (LangChain + OpenAI) ✅ |
| **v1.3.0** | Dockerized build, CI automation |
| **v1.4.0** | Advanced fuel tool (blending, energy, viscosity) |

---

**Generated:** 2025-10-30  
**Author:** Chief Engineer Volodymyr Zub  
**Project:** Fuel MCP — Marine Fuel Correction Processor  
**Motto:** Precision Engineering for Smarter Maritime Operations

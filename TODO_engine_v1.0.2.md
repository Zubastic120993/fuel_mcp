# ✅ Fuel MCP v1.0.2 — Core Engine Improvement Roadmap

**Version Target:** v1.0.2  
**Maintainer:** Chief Engineer Volodymyr Zub  
**Project:** *Fuel MCP — Marine Fuel Correction Processor*  
**Motto:** *Precision Engineering for Smarter Maritime Operations*

---

## ⚙️ Phase Objective

> Strengthen the **analytical core** of Fuel MCP before GUI and Docker stages — ensuring rock-solid accuracy, structured data handling, and robust test coverage.

---

## 🔹 TODO 1 — Data Persistence & Logging Layer

| Task | Description | Status |
|------|--------------|--------|
| **SQLite integration** | Create /data/mcp_history.db with queries, results, and errors tables | ⏳ Pending |
| **Logging adapter** | Route FastAPI + CLI outputs into structured log (JSON or SQLite) | ⏳ Pending |
| **History API refactor** | /history to read directly from SQLite, not in-memory list | ⏳ Pending |
| **Add unit tests** | tests/test_db_logging.py validating inserts + retrieval | ⏳ Pending |

---

## 🔹 TODO 2 — Analytical Engine Improvements

| Task | Description | Status |
|------|--------------|--------|
| **Integrate vcf_iso_official() deeply in query_mcp()** | Already linked, refine fallback handling & parameter extraction | ⚙️ In Progress |
| **Improve regex parser** | Extend query parsing for multi-unit inputs (e.g., “convert 500 L diesel at 30°C”) | ⏳ Pending |
| **Add product density map** | Load densities dynamically from JSON instead of hardcoded | ⏳ Pending |
| **Extend blending support** | Add formula for weighted VCF and density blending | ⏳ Pending |
| **Add test coverage** | New tests/test_vcf_blending.py | ⏳ Pending |

---

## 🔹 TODO 3 — Structured Error & Result Format

| Task | Description | Status |
|------|--------------|--------|
| **Unify return schema** | All results from API/CLI must follow {success, mode, query, result, _meta} | ⚙️ In Progress |
| **Improve error categorization** | Add error_code field in logs/errors.json (e.g., VCF_MISSING_DENSITY, CONVERSION_FAIL) | ⏳ Pending |
| **Link error logger to SQLite** | Mirror critical logs to DB for easier debugging | ⏳ Pending |

---

## 🔹 TODO 4 — Test Infrastructure

| Task | Description | Status |
|------|--------------|--------|
| **Add full test suite for query_mcp()** | Cover both VCF and conversion branches | ⏳ Pending |
| **Simulate offline/online modes** | Unit tests for both scenarios with mock env | ⏳ Pending |
| **Add load test profile** | Stress-test 100 random queries (pytest parametrize) | ⏳ Pending |
| **Refactor test reports** | Generate summary test_results.json in /logs | ⏳ Pending |

---

## 🔹 TODO 5 — Internal Tools & Maintenance

| Task | Description | Status |
|------|--------------|--------|
| **Add mcp db-purge CLI command** | Clears local history and logs safely | ⏳ Pending |
| **Add mcp test CLI command** | Runs internal pytest suite and prints summary | ⏳ Pending |
| **Refactor folder auto-setup** | Ensure /data, /logs, /models auto-created in portable builds | ✅ Done |

---

## 🔹 Version Plan (Core Phase Only)

| Version | Focus | Notes |
|----------|--------|-------|
| **v1.0.2-engine** | Core stability, structured DB logging, extended parser | 🔜 Target now |
| **v1.0.3-qa** | Extended tests, load testing, JSON unification | Next |
| **v1.1.0-gui** | Begin GUI frontend (PySide6 / Gradio) | Later |

---

**Next Terminal Steps**
```bash
git add TODO_engine_v1.0.2.md
git commit -m '🧠 Added v1.0.2 engine improvement roadmap — preparing core for database and precision refactor'
```

---

**Generated:** 2025-10-30  
**Author:** Chief Engineer Volodymyr Zub  
**Project:** Fuel MCP — Marine Fuel Correction Processor  
**Motto:** Precision Engineering for Smarter Maritime Operations


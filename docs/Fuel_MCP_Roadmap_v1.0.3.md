# 🧭 Fuel MCP v1.0.3 — Core Polish & Metrics Extension

**Branch:** `feature/core-polish-v1.0.3`  
**Maintainer:** Chief Engineer *Volodymyr Zub*  
**Goal:** Stabilize and enrich API observability before Docker packaging & GUI integration.  

---

## 🔹 1. Enhanced `/metrics` Endpoint

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add uptime tracking | Include seconds since API start (`uptime_seconds`) | ✅ Done | Verified via `test_api_metrics.py` — uptime value increasing over time. |
| ✅ Add version info | Include `app.version` and `python_version` | ✅ Done | Confirmed in `/metrics` JSON output. |
| ✅ Include DB stats | Add DB file size, total queries, errors count | ✅ Done | Keys confirmed: `db_path`, `db_size_kb`, `total_queries`, `failed_queries`. |
| ✅ Add test coverage | Dedicated test coverage for metrics endpoint | ✅ Done | File `fuel_mcp/tests/test_api_metrics.py` — all tests passed. |

---

## 🔹 2. `/errors` Endpoint Improvements

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add filter by module | `/errors?module=mcp_core` | ✅ Done | SQL filter `WHERE module = ?` validated. |
| ✅ Add limit param | Restrict number of results | ✅ Done | `limit` param functional, default = 20. |
| ⚙️ Add pagination placeholder | Prepare for GUI integration (OFFSET support) | ⏳ Planned | To be implemented in v1.1.0-gui. |
| ✅ Add dedicated tests | Validate filtering, limits, and response structure | ✅ Done | Verified via `fuel_mcp/tests/test_api_errors.py`. |

---

## 🔹 3. `/debug` Endpoint Enhancements

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Return Python version, OS, uptime | Uses `platform` and `START_TIME` delta | ✅ Done | Output validated manually and via `/debug`. |
| ✅ Add DB + log size summary | Return both in KB for diagnostics | ✅ Done | Verified by JSON response in `/debug`. |
| ⚙️ Add unit tests | Validate key presence and uptime consistency | ⏳ Planned | To expand `tests/test_api_debug.py` coverage. |

---

## 🔹 4. Auto Changelog Generator v2

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add timestamp + Git hash tracking | Uses `git rev-parse HEAD` and timestamp injection | ✅ Done | Output visible in auto-generated changelogs. |
| ✅ Auto-create `CHANGELOG_v1.0.3.md` | Stored in `/logs` folder automatically | ✅ Done | Confirmed on v1.0.3 build. |
| ✅ Include modified files summary | via `git diff --name-only HEAD~1` | ✅ Done | Present in generated changelog content. |
| ⚙️ Add test coverage | Verify changelog creation and format integrity | ⏳ Planned | To be implemented as `tests/test_changelog_gen.py`. |

---

## 🔹 5. Preparation for GUI & Docker Integration

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ⚙️ Add `/info` endpoint | Return concise system and API overview | ⏳ Planned | Will include version, uptime, DB/log stats. |
| ✅ Verify all GET endpoints return 200 | `/`, `/status`, `/query`, `/convert`, `/vcf`, `/auto_correct`, `/tool`, `/errors`, `/metrics`, `/history`, `/logs`, `/debug` | ✅ Done | Confirmed in pytest suite (all endpoints tested). |
| ⚙️ Export OpenAPI schema | Save as `docs/api_schema_v1.0.3.json` | ⏳ Planned | Will implement via `app.openapi()` export or Makefile target. |

---

## 📊 **Verification Summary**

| Category | Tests | Result |
|-----------|--------|--------|
| Core Engine | 56 | ✅ Passed |
| RAG Fallback | 1 | ⚠️ Skipped (no API key) |
| CLI Tools | 4 | ✅ Verified manually |
| API Endpoints | 11 | ✅ Stable |
| JSON Schema | 1 | ✅ Unified |

---

## 📅 **Next Development Phase**

| Version | Focus | Deliverables |
|----------|--------|--------------|
| **v1.1.0-gui** | Flask / Gradio interface | Simple GUI for local engine interaction |
| **v1.1.1-docker** | Dockerfile + Compose setup | Build containerized Fuel MCP |
| **v1.2.0-agent** | Flowise / LangChain integration | Voice- and AI-driven query engine |

---

## 🧾 **Commit Recommendation**

```bash
git add docs/Fuel_MCP_Roadmap_v1.0.3.md
git commit -m "🧭 Added Fuel MCP v1.0.3 Roadmap — Core Polish & Metrics Extension (stable API)"
git push origin feature/core-polish-v1.0.3
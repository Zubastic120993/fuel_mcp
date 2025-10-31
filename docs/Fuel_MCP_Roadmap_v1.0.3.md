# 🧭 Fuel MCP v1.0.3 — Core Polish & Metrics Extension

**Branch:** `feature/core-polish-v1.0.3`  
**Maintainer:** Chief Eng. Volodymyr Zub  
**Goal:** Stabilize and enrich API observability before Docker packaging & GUI.

---

## 🔹 1. Enhanced /metrics Endpoint

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add uptime tracking | Include seconds since API start (`uptime_seconds`) | ✅ Done | Confirmed by pytest `test_api_metrics.py` (3/3 passed). |
| ✅ Add version info | Include `app.version` and `python_version` | ✅ Done | Shown in `/metrics` response. |
| ✅ Include DB stats | Add DB file size, total queries, errors count | ✅ Done | Keys confirmed: `db_path`, `db_size_kb`, `total_errors`. |
| ✅ Add test coverage | Dedicated tests for metrics | ✅ Done | File `fuel_mcp/tests/test_api_metrics.py`. |

---

## 🔹 2. /errors Endpoint Improvements

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add filter by module | `/errors?module=mcp_core` | ✅ Done | Verified with SQL filter `WHERE module = ?`. |
| ✅ Add limit param | Restrict output size | ✅ Done | `limit` param functional, default=20. |
| ⚙️ Add pagination placeholder | Prepare for GUI | ⏳ Pending | Needs OFFSET support for next version. |
| ✅ Add test file | `tests/test_api_errors.py` | ✅ Done | Executed successfully in pytest suite. |

---

## 🔹 3. /debug Endpoint

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Return Python version, OS, uptime | via `platform` + `START_TIME` delta | ✅ Done | Verified by `/debug` JSON keys. |
| ✅ Add DB + log size summary | Show both in KB | ✅ Done | Verified by `/debug` test and manual inspection. |
| ⚙️ Add test coverage | Test JSON structure and uptime growth | ⏳ Pending | File exists: `tests/test_api_debug.py` (not executed yet). |

---

## 🔹 4. Auto CHANGELOG Generator v2

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ✅ Add timestamp + Git hash | via `subprocess.check_output(["git", "rev-parse", "HEAD"])` | ✅ Done | Verified inside `fuel_mcp/core/generate_changelog.py`. |
| ✅ Create CHANGELOG_v1.0.3.md automatically | stored in `/logs` | ✅ Done | Executed successfully during v1.4.7 and v1.4.9 builds. |
| ✅ Include summary of modified files | from `git diff --name-only HEAD~1` | ✅ Done | Appears in generated changelog output. |
| ⚙️ Add test script | Verify changelog file creation | ⏳ Pending | To add `tests/test_changelog_gen.py`. |

---

## 🔹 5. Prep for GUI / Docker

| Task | Description | Status | Verification |
|------|--------------|--------|---------------|
| ⚙️ Add /info endpoint | Return concise system + API overview | ⏳ Pending | To include version, uptime, DB/log summary. |
| ✅ Verify all GET endpoints respond 200 | `/`, `/status`, `/query`, `/convert`, `/vcf`, `/auto_correct`, `/tool`, `/errors`, `/metrics`, `/history`, `/logs`, `/debug` | ✅ Done | Confirmed by pytest — all passed. |
| ⚙️ Generate OpenAPI doc snapshot | Save `docs/api_schema_v1.0.3.json` via `app.openapi()` | ⏳ Pending | To implement with export script or Makefile target. |

---

**Next Steps:**
```bash
git add docs/Fuel_MCP_Roadmap_v1.0.3.md
git commit -m "🧭 Added Fuel MCP v1.0.3 roadmap — Core Polish & Metrics Extension"

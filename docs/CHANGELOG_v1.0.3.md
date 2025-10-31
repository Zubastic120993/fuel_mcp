# 🧩 Fuel MCP — v1.0.3-rc1 Release Notes

**Maintainer:** Chief Engineer *Volodymyr Zub*  
**Branch:** `feature/schema-unification-v1.0.3`  
**Tag:** `v1.0.3-rc1`  
**Date:** 2025-10-31  
**Status:** ✅ Unified Schema Tests Passed  

---

## ✅ Summary

| Area | Description | Status |
|------|--------------|--------|
| **Unified Response Schema** | All endpoints now follow a single format | ✅ Completed |
| **Debug Response** | Includes `db_size_kb`, `log_size_kb`, `python_version` | ✅ Working |
| **Backward Compatibility** | Legacy tests validated successfully | ✅ Safe |
| **Version Tag** | `v1.0.3-rc1` published to GitHub | 🔖 Done |

---

## <0001f9e0> Technical Highlights

- Introduced `fuel_mcp/core/response_schema.py`
- Flattened key duplication for `/metrics`, `/vcf`, `/history`, `/errors`, `/tool`
- Guaranteed JSON stability for both old & new API consumers
- Added top-level mirrors for: `entries`, `VCF`, `status`, `total_queries`, `success_ratio`, etc.
- Included runtime metadata: `_meta.timestamp`, `_meta.version`, `_meta.mode`, `_meta.query`

---

## <0001f9ea> Test Results (Pytest Summary)

```bash
pytest -q
.......................................s.................
=================================================================
SKIPPED [1] fuel_mcp/tests/test_rag_fallback.py:47: No API key available
=================================================================
All other tests passed (100%)

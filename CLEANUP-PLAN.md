# 🧹 Fuel MCP — Cleanup Plan for Docker Gradio Package

## Analysis Summary

**Current Project Size:** ~1.7 GB  
**After Cleanup:** ~150 MB  
**Space Saved:** ~1.55 GB (91% reduction)

---

## 📦 What to Remove (Safe to Delete)

### 1. Virtual Environment (1.0 GB) — LARGEST
```
venv/                           # Not needed in Docker
```
**Why:** Docker builds its own Python environment inside the container.

---

### 2. Development & Testing (556 KB)
```
fuel_mcp/tests/                 # Test files
fuel_mcp/tests/test_gui/        # GUI tests
.pytest_cache/                  # Test cache
```
**Why:** Tests are not needed for production deployment. Docker already tested.

---

### 3. RAG/AI Features (664 KB)
```
fuel_mcp/rag/                   # RAG functionality
fuel_mcp/models/                # Empty model directory
```
**Why:** Gradio apps don't use RAG features. Only uses core calculations.

---

### 4. Build Artifacts (76 KB)
```
dist/                           # Built wheel and tar.gz files
fuel_mcp.egg-info/              # Build metadata
```
**Why:** Not needed for Docker deployment. Docker builds from source.

---

### 5. Python Cache (varies)
```
fuel_mcp/__pycache__/
fuel_mcp/api/__pycache__/
fuel_mcp/core/__pycache__/
fuel_mcp/gui_astm/__pycache__/
fuel_mcp/tests/__pycache__/
*.pyc files
```
**Why:** Automatically regenerated at runtime.

---

### 6. CLI Tools (8 KB)
```
fuel_mcp/cli/                   # Command-line interface
```
**Why:** Not used in Docker web deployment.

---

### 7. Flowise Integration (4 KB)
```
fuel_mcp/flowise/               # Flowise node.js integration
```
**Why:** Not used in Gradio deployment.

---

### 8. Temporary Logs
```
logs/errors.json
logs/mcp_errors.log
logs/mcp_queries.log
logs/test_results.json
fuel_mcp/logs/app.log
fuel_mcp/logs/rag_activity.json
docker-build.log
```
**Why:** Old logs not needed. Fresh logs will be created.

---

### 9. Extra Documentation
```
docs/CHANGELOG_v1.0.3.md
docs/Fuel_MCP_v1.0.3_Consolidated_Report.md
CHANGELOG.md
```
**Why:** Internal documentation not needed for deployment. Keep only user-facing docs.

---

### 10. Old Docker Files
```
Dockerfile                      # Old API-only Dockerfile
docker-compose.yml              # Old API-only compose
```
**Why:** Replaced by Dockerfile.gradio and docker-compose-gradio.yml

---

### 11. Old Scripts
```
launch_gui.sh                   # Local dev script
```
**Why:** Replaced by start-docker.sh for Docker deployment

---

### 12. Development Files
```
requirements-lock.txt           # Full dev requirements
pyproject.toml                  # Build configuration (keep for reference)
```
**Why:** Not needed. Using requirements-gradio.txt

---

## ✅ What to KEEP (Required for Docker)

### Core Application (Required)
```
fuel_mcp/
├── __init__.py                 ✅ Package initialization
├── __main__.py                 ✅ Entry point
├── api/                        ✅ FastAPI backend
│   ├── mcp_api.py
│   └── api_correlate.py
├── core/                       ✅ Calculation engine
│   ├── unit_converter.py
│   ├── vcf_official_full.py
│   ├── regex_parser.py
│   ├── response_schema.py
│   ├── db_logger.py
│   ├── async_logger.py
│   ├── error_handler.py
│   ├── fuel_density_loader.py
│   ├── conversion_engine.py
│   ├── conversion_dispatcher.py
│   ├── calculations.py
│   └── tables/fuel_data.json
├── gui_astm/                   ✅ Gradio frontends
│   ├── app_astm_unified.py
│   ├── app_astm_api.py
│   ├── app_astm_density.py
│   ├── app_astm_rel_density.py
│   ├── app_astm_vol_weight.py
│   └── app_astm_universal_converter.py
├── tables/official/normalized/ ✅ ASTM data (29 CSV files)
├── tool_integration.py         ✅ Tool integration
└── tool_interface.py           ✅ Tool interface
```

### Docker Deployment Files (Keep)
```
Dockerfile.gradio               ✅ Production Dockerfile
docker-compose-gradio.yml       ✅ Multi-service orchestration
requirements-gradio.txt         ✅ Python dependencies
start-docker.sh                 ✅ Convenience script
.dockerignore                   ✅ Build optimization
```

### Documentation (Keep)
```
README.md                       ✅ Main README
README-DOCKER.md                ✅ Docker deployment guide
QUICKSTART.md                   ✅ Quick start guide
DEPLOYMENT-CHECKLIST.md         ✅ Deployment checklist
PACKAGE-SUMMARY.md              ✅ Package overview
DOCKER-OPTIONS.md               ✅ Deployment options
DOCKER-PACKAGE-README.txt       ✅ Quick reference
CLEANUP-PLAN.md                 ✅ This file
```

### Optional Single Container (Keep if you want it)
```
Dockerfile.gradio-single        ✅ Single-container version
```

### Runtime Data (Keep but can clean logs)
```
fuel_mcp/data/                  ✅ SQLite database (keep)
logs/                           ⚠️  Clean old logs, keep directory
```

---

## 🚀 Automated Cleanup Script

I'll create a safe cleanup script that:
1. Backs up important files
2. Removes unnecessary directories
3. Cleans Python cache
4. Creates a clean deployment package


# ⚙️ Fuel MCP — Marine Fuel Correction Processor

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/yourusername/fuel_mcp)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Fuel MCP** is a local analytical engine for precise fuel mass–volume corrections based on **ISO 91-1 / ASTM D1250** standards.  
It provides a **FastAPI service**, **Python module interface**, **Gradio web GUI**, and **LangChain agent integration**, enabling use in standalone tools, web applications, or AI-assisted agent environments.

---

## 🚀 Features

### Core Engine
- ⚡ Accurate **Volume Correction Factor (VCF)** calculations for all marine fuels  
- 🔄 Automatic **mass ↔ volume correction** at observed temperature  
- 📊 ASTM Table-based unit conversions (Table 1, 54A/B/C/D)
- 🧮 Natural language query parser (NLP) for conversion requests
- 💾 **SQLite database** with async logging and metrics tracking
- 🔍 Reverse conversion logic (tons → m³, etc.)
- 🌐 Works completely **offline**

### API & Integration
- 🚀 **FastAPI REST endpoints** with OpenAPI documentation
- 🤖 **LangChain/Flowise agent integration** ready
- 📡 **Database metrics** and **error tracking endpoints**
- 🔐 Unified response schema with `_meta` blocks
- 📝 JSON-based logging and query history

### User Interfaces
- 🖥️ **Gradio web GUI** with multiple ASTM calculator panels
- 💻 **CLI toolkit** for maintenance and quick calculations
- 🐳 **Docker support** with compose configuration
- 📱 Modular GUI architecture for custom interfaces

### Testing & Quality
- ✅ **56+ comprehensive tests** with pytest
- 🧪 Full coverage for API, CLI, regex parser, and VCF calculations
- 🔄 Continuous validation of ASTM standards compliance

---

## 🧩 Installation

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/fuel_mcp.git
cd fuel_mcp

# Build (optional – start script builds automatically)
./start-docker.sh build

# Launch backend + Gradio frontend
./start-docker.sh start

# Run health checks
./start-docker.sh test

# View logs (Ctrl+C to exit)
./start-docker.sh logs

# Stop services when finished
./start-docker.sh stop
```

API docs: `http://localhost:8000/docs`  
Gradio UI: `http://localhost:7860`

Prefer to drive Docker Compose manually? Use `docker-compose -f docker-compose-gradio.yml up -d` and `docker-compose -f docker-compose-gradio.yml down --remove-orphans`.

### Option 2: Local Installation

#### 1️⃣ Clone repository
```bash
git clone https://github.com/yourusername/fuel_mcp.git
cd fuel_mcp
```

#### 2️⃣ Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

#### 4️⃣ (Optional) Install as a package
```bash
pip install .
```

#### 5️⃣ (Optional) Install with agent support
```bash
pip install ".[agent]"  # Includes LangChain, OpenAI
```

---

## 🚀 Quick Start

### Run API Server
```bash
uvicorn fuel_mcp.api.mcp_api:app --reload
```

Then open in browser:
```
http://127.0.0.1:8000/docs
```

### Run Web GUI

#### Unified Interface (All-in-One, Recommended)
```bash
# Launch all ASTM calculators in one browser with tabs
python -m fuel_mcp.gui_astm.app_astm_unified
```
GUI will be available at `http://localhost:7860`

#### Individual Panels (Run Separately)
```bash
# API Gravity Entry (port 7861)
python -m fuel_mcp.gui_astm.app_astm_api

# Relative Density Entry (port 7862)
python -m fuel_mcp.gui_astm.app_astm_rel_density

# Density Entry (port 7863)
python -m fuel_mcp.gui_astm.app_astm_density

# Volume & Weight Converter (port 7864)
python -m fuel_mcp.gui_astm.app_astm_vol_weight

# Universal Unit Converter (port 7870)
python -m fuel_mcp.gui_astm.app_astm_universal_converter
```

---

## 🧠 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/status` | GET | Check service status (online/offline) |
| `/query` | GET | Run semantic MCP query with NLP parsing |
| `/convert` | GET | ASTM Table 1 unit conversion |
| `/vcf` | GET | Compute ISO 91-1 / ASTM D1250 VCF |
| `/auto_correct` | GET | Automatic mass/volume correction |
| `/correlate` | GET | API gravity ↔ Density correlation (Table 1) |

### Monitoring & Debug

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/metrics` | GET | Performance statistics, uptime, query counts |
| `/errors` | GET | Recent errors with filtering (module, limit) |
| `/history` | GET | Recent query history from SQLite |
| `/logs` | GET | Recent log entries |
| `/debug` | GET | System diagnostics (OS, Python, DB size) |

### Integration

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/tool` | GET | OpenAI-compatible JSON schema for MCP Tool |

**Interactive API Documentation:** `http://127.0.0.1:8000/docs`

---

## 📊 Example Usage

### Example 1 – Auto-Correction with Mass & Volume
```bash
curl "http://127.0.0.1:8000/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25"
```

Response:
```json
{
  "success": true,
  "result": {
    "table": "54B (Residual / Marine fuels)",
    "VCF": 0.99167,
    "V15_m3": 991.67,
    "mass_ton": 842.9
  },
  "_meta": {
    "version": "1.5.0",
    "timestamp": "2025-11-03T12:34:56Z",
    "mode": "vcf"
  }
}
```

### Example 2 – Natural Language Query
```bash
curl "http://127.0.0.1:8000/query?text=convert%20500%20liters%20diesel%20at%2030C%20to%20tons"
```

### Example 3 – Direct VCF Calculation
```bash
curl "http://127.0.0.1:8000/vcf?rho15=850&tempC=25"
```

### Example 4 – API Gravity to Density Correlation
```bash
curl "http://127.0.0.1:8000/correlate?table=ASTM_Table1_APIGravity60F_to_RelativeDensity60F_and_Density15C_norm&column=api_gravity_60f&value=33"
```

---

## 🧰 Testing

### Run All Tests
```bash
pytest -v
```

Expected output:
```
======================== 56 passed, 1 skipped ========================
```

### Run Specific Test Suites
```bash
# API tests only
pytest fuel_mcp/tests/test_api_*.py -v

# Core engine tests
pytest fuel_mcp/tests/test_core.py fuel_mcp/tests/test_vcf_*.py -v

# CLI tests
pytest fuel_mcp/tests/test_cli_*.py -v

# Regex parser tests
pytest fuel_mcp/tests/test_regex_parser_cases.py -v
```

### Test Coverage
```bash
pytest --cov=fuel_mcp --cov-report=html
```

---

## 🧱 Project Structure

This branch is trimmed for the Docker Gradio package. The tree below lists the key files you actually get in this distribution:

```
.
├── Dockerfile.gradio              # Multi-service image (compose)
├── Dockerfile.gradio-single       # Optional single-container image
├── docker-compose-gradio.yml      # Backend + Gradio services
├── start-docker.sh                # Helper script (build/start/test/stop)
├── requirements-gradio.txt        # Runtime dependencies
├── requirements.txt               # Full development dependency set
├── README.md                      # This file
├── README-DOCKER.md               # Docker deployment guide
├── QUICKSTART.md                  # 5-minute setup guide
├── DEPLOYMENT-CHECKLIST.md        # Pre-deployment checklist
├── PACKAGE-SUMMARY.md             # Package overview
├── DOCKER-PACKAGE-README.txt      # Quick reference sheet
├── DOCKER-OPTIONS.md              # Deployment scenarios comparison
├── docs/                          # Additional documentation
├── logs/                          # Runtime logs (mounted in Docker)
└── fuel_mcp/
    ├── __init__.py
    ├── __main__.py
    ├── api/                       # FastAPI backend
    │   ├── mcp_api.py
    │   └── api_correlate.py
    ├── core/                      # Calculation engine & helpers
    │   ├── unit_converter.py
    │   ├── vcf_official_full.py
    │   ├── regex_parser.py
    │   ├── response_schema.py
    │   ├── conversion_engine.py
    │   ├── conversion_dispatcher.py
    │   ├── fuel_density_loader.py
    │   ├── calculations.py
    │   ├── async_logger.py
    │   ├── db_logger.py
    │   ├── error_handler.py
    │   ├── mcp_core.py            # Agent/RAG integration entry point
    │   ├── rag_bridge.py          # Optional semantic lookup bridge
    │   ├── setup_env.py
    │   └── tables/
    │       └── fuel_data.json
    ├── gui_astm/                  # Gradio frontends
    │   ├── app_astm_unified.py    # Unified UI (used in Docker)
    │   ├── app_astm_api.py
    │   ├── app_astm_rel_density.py
    │   ├── app_astm_density.py
    │   ├── app_astm_vol_weight.py
    │   ├── app_astm_universal_converter.py
    │   └── app_astm_units.py
    ├── tables/                    # Normalised ASTM CSV tables & tooling
    │   ├── official/normalized/*.csv
    │   ├── loader.py
    │   ├── manage_registry.py
    │   ├── normalize_tables.py
    │   ├── registry.json
    │   └── summary_report.py
    ├── data/                      # SQLite database (mounted in Docker)
    │   └── mcp_history.db
    ├── logs/                      # Package-level logs (mounted in Docker)
    ├── tool_interface.py          # Tool wrapper (LangChain/OpenAI)
    └── tool_integration.py        # LangChain StructuredTool helper
```

> 🔎 Looking for the full automated test suite? It lives in the development branch. The Docker package keeps only the runtime essentials to minimise image size.

## ⚙️ Maintenance CLI

The Fuel MCP CLI provides comprehensive maintenance and quick calculation commands:

### Database Management

| Command | Description |
|----------|-------------|
| `mcp-cli db stats` | Show total queries, success %, last error |
| `mcp-cli db clean --days 30` | Remove logs older than 30 days |
| `mcp-cli db vacuum` | Compact and optimize SQLite database |
| `mcp-cli history` | Show recent query history |

### System Information

| Command | Description |
|----------|-------------|
| `mcp-cli status` | Display log info and system status |
| `mcp-cli log` | Print full application log |

### Quick Calculations

| Command | Description |
|----------|-------------|
| `mcp-cli vcf diesel 25` | Quick VCF calculation for diesel at 25°C |
| `mcp-cli convert "convert 1000 liters to m3"` | Quick conversion query |
| `mcp-cli convert "500 L diesel @ 30°C to tons"` | NLP conversion with temperature |

---

## 🤖 Agent Integration

### LangChain Integration

```python
from fuel_mcp.tool_integration import mcp_tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# Initialize agent with Fuel MCP tool
llm = OpenAI(temperature=0)
tools = [mcp_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use agent
result = agent.run("Calculate VCF for diesel at 25°C with density 850")
```

### Direct Tool Interface

```python
from fuel_mcp.tool_interface import mcp_query

# Direct query
result = mcp_query("convert 500 liters diesel at 30°C to tons")
print(result)
```

### Flowise Integration

1. Import the Fuel MCP node from `fuel_mcp/flowise/fuel_mcp_node.js`
2. Add to your Flowise custom nodes directory
3. Use the "⚓ Fuel MCP Node" in your flow builder

---

## 🐳 Docker Management

### Build and Run

```bash
# Build image
docker-compose build

# Start service
docker-compose up -d

# Stop service
docker-compose down

# Restart service
docker-compose restart

# View real-time logs
docker-compose logs -f fuel_mcp_api
```

### Database Persistence

The following directories are mounted as volumes for persistence:
- `./fuel_mcp/data` → Database files
- `./fuel_mcp/models` → ML models (optional)
- `./logs` → Application logs

### Health Check

```bash
# Check container health
docker-compose ps

# Manual health check
curl http://localhost:8000/status
```
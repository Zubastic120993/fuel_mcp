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

# Run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f fuel_mcp_api
```

API will be available at `http://localhost:8000/docs`

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
```
fuel_mcp/
 ├── api/                         # FastAPI REST endpoints
 │   ├── mcp_api.py              # Main API routes
 │   └── api_correlate.py        # API/Density correlation endpoint
 ├── core/                       # Core calculation engine
 │   ├── vcf_official_full.py    # ISO 91-1 / ASTM D1250 VCF engine
 │   ├── calculations.py         # Mass/volume calculations
 │   ├── conversion_engine.py    # Unit conversion logic
 │   ├── unit_converter.py       # ASTM Table 1 conversions
 │   ├── regex_parser.py         # NLP query parser
 │   ├── fuel_density_loader.py  # Dynamic fuel density loader
 │   ├── response_schema.py      # Unified API response schema
 │   ├── async_logger.py         # Async non-blocking logging
 │   ├── db_logger.py            # SQLite logging utilities
 │   ├── error_handler.py        # Error handling & tracking
 │   └── cli.py                  # Maintenance CLI commands
 ├── gui_astm/                   # Gradio web interface modules
 │   ├── app_astm_unified.py     # 🎯 UNIFIED launcher (all-in-one)
 │   ├── app_astm_api.py         # API gravity calculator
 │   ├── app_astm_rel_density.py # Relative density calculator
 │   ├── app_astm_density.py     # Density calculator
 │   ├── app_astm_vol_weight.py  # Volume/weight converter
 │   └── app_astm_universal_converter.py  # Universal unit converter
 ├── rag/                        # RAG & vector store (optional)
 │   ├── retriever.py            # Semantic retrieval
 │   ├── loader.py               # Document loader
 │   └── metadata.json           # Metadata store
 ├── tables/                     # ASTM reference tables
 │   ├── fuel_data.json          # Fuel density database
 │   ├── registry.json           # Table registry
 │   └── official/normalized/    # Normalized ASTM CSV tables
 ├── tests/                      # Comprehensive test suite (56+ tests)
 │   ├── test_api_*.py           # API endpoint tests
 │   ├── test_core.py            # Core engine tests
 │   ├── test_vcf_*.py           # VCF calculation tests
 │   ├── test_regex_parser_cases.py  # NLP parser tests
 │   └── test_cli_*.py           # CLI tests
 ├── flowise/                    # Flowise integration
 │   └── fuel_mcp_node.js        # Flowise node definition
 ├── data/                       # Runtime data
 │   └── mcp_history.db          # SQLite database
 ├── logs/                       # Application logs
 │   ├── mcp_queries.log         # Query logs
 │   ├── mcp_errors.log          # Error logs
 │   └── test_results.json       # Test results
 ├── tool_interface.py           # LangChain tool interface
 ├── tool_integration.py         # LangChain tool wrapper
 ├── docker-compose.yml          # Docker orchestration
 ├── Dockerfile                  # Container definition
 ├── pyproject.toml              # Build & dependency config
 └── requirements.txt            # Python dependencies
```

---

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

---

## 🖥️ Web GUI Features

The Gradio-based GUI provides interactive ASTM D1250 calculators.

### 🎯 Unified Interface (`app_astm_unified.py`) — **Recommended**
**All calculators in one browser with tabs:**
- 🌡️ **API Gravity Entry** — Tables T.2–T.14
- 📊 **Relative Density Entry** — Volume IV/V/VI → XII
- 🧪 **Density Entry** — Tables 54A/B/C
- ⚖️ **Volume & Weight Converter** — ASTM D1250 conversions
- 🔄 **Universal Unit Converter** — Grouped conversions (Mass/Volume/Length)

**Usage:** `python -m fuel_mcp.gui_astm.app_astm_unified` → `http://localhost:7860`

### Individual Panels (Can run separately)

#### API Gravity Calculator (`app_astm_api.py`)
- API gravity → Density conversion
- Temperature-based VCF calculation
- Full ASTM Volume I–XI equivalents (T.2–T.14)

#### Relative Density Calculator (`app_astm_rel_density.py`)
- Relative Density (60/60°F) input
- Temperature correction
- Volume IV/V/VI → XII tables

#### Density Calculator (`app_astm_density.py`)
- Density @15°C input
- Temperature correction (Table 54A/B/C)
- Volume VII/VIII/IX → XII equivalents

#### Volume/Weight Converter (`app_astm_vol_weight.py`)
- Volume ↔ Mass conversions
- Temperature-corrected calculations
- Multiple fuel types support
- BBLS, M³, Tons, US Gallons

#### Universal Unit Converter (`app_astm_universal_converter.py`)
- Grouped unit conversions (Mass, Volume, Length)
- Dynamic unit selection based on category
- Real-time equivalent calculations
- Human-readable unit labels with internal ASTM mapping

---

## 📚 Documentation

- **CHANGELOG:** See [CHANGELOG.md](CHANGELOG.md) for version history
- **API Documentation:** `http://localhost:8000/docs` (when running)
- **Detailed Reports:** See `docs/` directory for comprehensive reports

---

## 🧩 License

© 2025 **Volodymyr Zub** — All rights reserved.

---

## 📬 Contact

**Chief Engineer Volodymyr Zub**  
📧 [your.email@example.com](mailto:your.email@example.com)  
🏷️ "Precision Engineering for Smarter Maritime Operations"

---

## 🌟 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🔖 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and release notes.

**Current Version:** v1.5.0 (2025-11-03)

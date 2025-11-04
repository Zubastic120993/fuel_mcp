# ⚙️ Fuel MCP — Marine Fuel Correction Processor

[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/Zubastic120993/fuel_mcp)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-56%20passed-green.svg)](https://github.com/Zubastic120993/fuel_mcp)

> **Precise fuel mass–volume corrections based on ISO 91-1 / ASTM D1250 standards**

**Fuel MCP** is a production-ready analytical engine for accurate marine fuel calculations. It provides a **FastAPI REST API**, **Python module interface**, **Gradio web GUI**, and **AI agent integration**, making it perfect for standalone tools, web applications, or AI-assisted workflows.

---

## 📑 Table of Contents

- [What Problem Does This Solve?](#-what-problem-does-this-solve)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Installation Options](#-installation-options)
- [Uninstallation](#-uninstallation)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Testing](#-testing)
- [Agent Integration](#-agent-integration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 What Problem Does This Solve?

In the petroleum and marine industries, accurate fuel quantity calculations are critical for:

- **Custody Transfer** — Precise measurements for billing and contracts
- **Bunker Fuel Management** — Temperature corrections for marine vessels
- **Quality Control** — Laboratory density corrections to standard temperatures
- **Financial Accuracy** — Correct volume-to-mass conversions at varying temperatures

**Fuel MCP** solves these challenges by providing:

✅ **Standards-Compliant Calculations** — Based on ISO 91-1 and ASTM D1250  
✅ **Temperature Corrections** — Accurate VCF calculations for all marine fuels  
✅ **Natural Language Processing** — Query like "convert 500 L diesel at 30°C to tons"  
✅ **Offline Operation** — No internet required, works completely offline  
✅ **Multiple Interfaces** — REST API, Python module, Web GUI, or AI agents  

---

## 🚀 Key Features

### Core Engine
- ⚡ **Volume Correction Factor (VCF)** calculations for all marine fuels (diesel, HFO, MGO, LNG, methanol)
- 🔄 **Automatic mass ↔ volume correction** at observed temperature
- 📊 **ASTM Table-based** unit conversions (Table 1, 54A/B/C/D)
- 🧮 **Natural language query parser** (NLP) for conversion requests
- 💾 **SQLite database** with async logging and metrics tracking
- 🔍 **Reverse conversion logic** (tons → m³, etc.)
- 🌐 **Completely offline** — no external dependencies

### API & Integration
- 🚀 **FastAPI REST endpoints** with interactive OpenAPI documentation
- 🤖 **LangChain/Flowise agent integration** ready
- 📡 **Database metrics** and **error tracking endpoints**
- 🔐 **Unified response schema** with `_meta` blocks
- 📝 **JSON-based logging** and query history

### User Interfaces
- 🖥️ **Gradio web GUI** with multiple ASTM calculator panels
- 💻 **CLI toolkit** for maintenance and quick calculations
- 🐳 **Docker support** with compose configuration
- 📱 **Modular GUI architecture** for custom interfaces

### Testing & Quality
- ✅ **56+ comprehensive tests** with pytest
- 🧪 **Full coverage** for API, CLI, regex parser, and VCF calculations
- 🔄 **Continuous validation** of ASTM standards compliance

---

## ⚡ Quick Start

### 🐳 Docker (Recommended - 2 minutes)

```bash
# Clone and start
git clone --branch feature/docker-gradio-package https://github.com/Zubastic120993/fuel_mcp.git fuel_mcp_gradio
cd fuel_mcp_gradio
./start-docker.sh start

# Access the application
# Web UI: http://localhost:7860
# API Docs: http://localhost:8000/docs
```

**That's it!** The application is now running. See [Docker Deployment Guide](docs/README-DOCKER.md) for details.

### 💻 Local Installation (5 minutes)

```bash
# Clone repository
git clone --branch feature/docker-gradio-package https://github.com/Zubastic120993/fuel_mcp.git fuel_mcp_gradio
cd fuel_mcp_gradio

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-gradio.txt

# Start backend (Terminal 1)
uvicorn fuel_mcp.api.mcp_api:app --reload

# Start frontend (Terminal 2)
python -m fuel_mcp.gui_astm.app_astm_unified
```

**Access:**
- Web UI: http://localhost:7860
- API Docs: http://localhost:8000/docs

For detailed instructions, see [Quick Start Guide](docs/QUICKSTART.md) or [Local Installation Guide](docs/INSTALL-LOCAL.md).

---

## 📦 Installation Options

### Option 1: Docker Deployment (Recommended)

**Best for:** Production, consistent environments, easy deployment

```bash
# Build and start
./start-docker.sh start

# Stop services
./start-docker.sh stop

# View logs
./start-docker.sh logs

# Run health tests
./start-docker.sh test
```

**Features:**
- ✅ Single-command deployment
- ✅ Automatic dependency management
- ✅ Isolated environment
- ✅ Persistent data storage
- ✅ Health monitoring

📖 **Full Guide:** [Docker Deployment Guide](docs/README-DOCKER.md)

### Option 2: Local Python Installation

**Best for:** Development, custom integrations, debugging

```bash
pip install -r requirements-gradio.txt

# Or install as package
pip install .

# Or with agent support
pip install ".[agent]"
```

📖 **Full Guide:** [Local Installation Guide](docs/INSTALL-LOCAL.md)

### Option 3: Package Installation

Install Fuel MCP as a Python package for use in your own projects:

```bash
pip install .
```

Then use it in your code:

```python
from fuel_mcp.core.vcf_official_full import compute_vcf
result = compute_vcf(rho15=850, tempC=25)
```

---

## 🗑️ Uninstallation

To completely remove Fuel MCP and all associated Docker resources:

### Docker Installation

```bash
# Full uninstall (removes everything including code)
./uninstall.sh

# Keep code, only remove Docker resources
KEEP_CODE=1 ./uninstall.sh
```

### Local Installation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # On Windows: rmdir /s venv

# Remove project (optional)
cd ..
rm -rf fuel_mcp_gradio
```

📖 **For detailed uninstall instructions and manual cleanup steps, see [Command Reference](docs/COMMANDS.md#-uninstall-complete-removal).**

---

## 💡 Usage Examples

### Example 1: Web GUI (Easiest)

1. Open http://localhost:7860
2. Navigate to **"API Gravity Entry"** tab
3. Enter:
   - API Gravity: `30.0`
   - Temperature: `60` °F
4. Click **"Compute ASTM Tables"**
5. View results: Density, VCF, corrected volumes

### Example 2: REST API

```bash
# Auto-correction with mass & volume
curl "http://localhost:8000/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25"
```

**Response:**
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

### Example 3: Natural Language Query

```bash
# Convert using natural language
curl "http://localhost:8000/query?text=convert%20500%20liters%20diesel%20at%2030C%20to%20tons"
```

### Example 4: Direct VCF Calculation

```bash
curl "http://localhost:8000/vcf?rho15=850&tempC=25"
```

### Example 5: Python Module

```python
from fuel_mcp.core.vcf_official_full import compute_vcf
from fuel_mcp.core.unit_converter import convert_units

# Calculate VCF
vcf = compute_vcf(rho15=850.0, tempC=25.0)
print(f"VCF: {vcf}")

# Unit conversion
result = convert_units(1000, "litre", "m3")
print(f"1000 L = {result} m³")
```

### Example 6: CLI Quick Calculations

```bash
# Quick VCF calculation
mcp-cli vcf diesel 25

# Natural language conversion
mcp-cli convert "convert 1000 liters to m3"
mcp-cli convert "500 L diesel @ 30°C to tons"
```

��📖 **More Examples:** See [Command Reference](docs/COMMANDS.md) for all available commands.

---

## 📚 API Reference

### Core Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/status` | GET | Service health check | `/status` |
| `/query` | GET | Natural language MCP query | `/query?text=convert 500L to tons` |
| `/convert` | GET | ASTM Table 1 unit conversion | `/convert?value=1&from_unit=barrel&to_unit=litre` |
| `/vcf` | GET | Compute VCF (ISO 91-1 / ASTM D1250) | `/vcf?rho15=850&tempC=25` |
| `/auto_correct` | GET | Automatic mass/volume correction | `/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25` |
| `/correlate` | GET | API gravity ↔ Density correlation | `/correlate?table=ASTM_Table1&column=api_gravity_60f&value=33` |

### Monitoring & Debug

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/metrics` | GET | Performance statistics, uptime, query counts |
| `/errors` | GET | Recent errors with filtering (module, limit) |
| `/history` | GET | Recent query history from SQLite |
| `/logs` | GET | Recent log entries |
| `/debug` | GET | System diagnostics (OS, Python, DB size) |

### Integration

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tool` | GET | OpenAI-compatible JSON schema for MCP Tool |

**Interactive API Documentation:** Visit http://localhost:8000/docs after starting the server.

---

## 📁 Project Structure

```
fuel_mcp/
├── 📄 README.md                    # This file
├── 📂 docs/                        # Comprehensive documentation
│   ├── QUICKSTART.md              # 5-minute setup guide
│   ├── README-DOCKER.md           # Docker deployment guide
│   ├── INSTALL-LOCAL.md           # Local installation guide
│   ├── COMMANDS.md                # Command reference
│   ├── PACKAGE-SUMMARY.md         # Package overview
│   ├── DEPLOYMENT-CHECKLIST.md    # Pre-deployment checklist
│   ├── DOCKER-OPTIONS.md          # Deployment scenarios
│   └── CHANGELOG.md               # Version history
│
├── 🐳 Docker files
│   ├── Dockerfile.gradio          # Production Dockerfile
│   ├── Dockerfile.gradio-single   # Single-container option
│   ├── docker-compose-gradio.yml  # Multi-service orchestration
│   └── start-docker.sh            # Convenience script
│
├── 📦 Package files
│   ├── requirements-gradio.txt    # Production dependencies
│   ├── requirements.txt           # Full dev dependencies
│   └── pyproject.toml             # Package configuration
│
└── 📂 fuel_mcp/                   # Main package
    ├── api/                       # FastAPI backend
    │   ├── mcp_api.py            # Main API routes
    │   └── api_correlate.py      # Correlation endpoints
    │
    ├── core/                      # Calculation engine
    │   ├── vcf_official_full.py  # VCF calculations
    │   ├── unit_converter.py     # ASTM conversions
    │   ├── regex_parser.py       # NLP query parser
    │   ├── conversion_engine.py  # Conversion dispatcher
    │   ├── db_logger.py          # SQLite logging
    │   └── tables/               # Fuel data & tables
    │
    ├── gui_astm/                  # Gradio web interfaces
    │   ├── app_astm_unified.py   # Unified UI (recommended)
    │   ├── app_astm_api.py       # API Gravity calculator
    │   ├── app_astm_density.py   # Density calculator
    │   └── ...                    # More calculators
    │
    └── tables/                    # ASTM CSV tables & tooling
        └── official/normalized/   # 29 normalized CSV files
```

---

## 📖 Documentation

Comprehensive documentation is available in the `docs/` folder:

| Document | Description | When to Use |
|----------|-------------|-------------|
| **[Quick Start Guide](docs/QUICKSTART.md)** | Get running in 5 minutes | First time setup |
| **[Docker Deployment](docs/README-DOCKER.md)** | Complete Docker guide | Docker deployment |
| **[Local Installation](docs/INSTALL-LOCAL.md)** | Install without Docker | Local development |
| **[Command Reference](docs/COMMANDS.md)** | All available commands | Daily operations |
| **[Package Summary](docs/PACKAGE-SUMMARY.md)** | Package overview | Understanding structure |
| **[Deployment Checklist](docs/DEPLOYMENT-CHECKLIST.md)** | Pre-deployment verification | Before going live |
| **[Docker Options](docs/DOCKER-OPTIONS.md)** | Deployment scenarios | Choosing deployment |
| **[Changelog](docs/CHANGELOG.md)** | Version history | Updates & changes |

---

## 🧪 Testing

### Run All Tests

```bash
pytest -v
```

**Expected output:**
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

Open `htmlcov/index.html` in your browser to view coverage report.

### Docker Testing

```bash
./start-docker.sh test
```

This runs automated health checks on the deployed services.

---

## 🤖 Agent Integration

Fuel MCP can be integrated into AI agent workflows using LangChain or Flowise.

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

For more details, see the agent integration examples in the codebase.

---

## 🛠️ Maintenance CLI

The Fuel MCP CLI provides maintenance and quick calculation commands:

### Database Management

```bash
# Show database statistics
mcp-cli db stats

# Clean old logs (older than 30 days)
mcp-cli db clean --days 30

# Optimize database
mcp-cli db vacuum

# View query history
mcp-cli history
```

### System Information

```bash
# Display system status
mcp-cli status

# View application logs
mcp-cli log
```

### Quick Calculations

```bash
# Quick VCF calculation
mcp-cli vcf diesel 25

# Natural language conversion
mcp-cli convert "convert 1000 liters to m3"
mcp-cli convert "500 L diesel @ 30°C to tons"
```

📖 **Full Command Reference:** See [COMMANDS.md](docs/COMMANDS.md)

---

## 🆘 Troubleshooting

### Port Already in Use

**Problem:** `Address already in use` error when starting services.

**Solution:**
```bash
# Find what's using the port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Change ports in docker-compose-gradio.yml or use different ports:
uvicorn fuel_mcp.api.mcp_api:app --port 8001
```

### Frontend Can't Connect to Backend

**Problem:** Gradio UI shows connection errors.

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/status`
2. Check that frontend is using correct backend URL (`http://127.0.0.1:8000`)
3. Check firewall settings
4. View backend logs: `./start-docker.sh logs` or check terminal output

### Module Not Found Error

**Problem:** `ModuleNotFoundError: No module named 'fuel_mcp'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements-gradio.txt

# Or install as package
pip install .
```

### Docker Container Won't Start

**Problem:** Container exits immediately or won't start.

**Solution:**
```bash
# Check logs
./start-docker.sh logs

# Restart from scratch
./start-docker.sh stop
./start-docker.sh clean
./start-docker.sh start

# Check Docker resources
docker system df
docker system prune -a  # If needed (removes unused resources)
```

### Database Locked Error

**Problem:** SQLite database is locked.

**Solution:**
```bash
# Stop all services
./start-docker.sh stop

# Check for stale processes
ps aux | grep fuel_mcp

# Restart services
./start-docker.sh start
```

### More Help

- Check [Docker Deployment Guide](docs/README-DOCKER.md) for Docker-specific issues
- Review [Local Installation Guide](docs/INSTALL-LOCAL.md) for setup problems
- View application logs in `logs/` directory or via `./start-docker.sh logs`

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Issues** — Found a bug? Open an issue on GitHub
2. **Suggest Features** — Have an idea? Share it in the issues
3. **Submit Pull Requests** — Fixed a bug or added a feature? Submit a PR

### Development Setup

```bash
# Clone repository
git clone https://github.com/Zubastic120993/fuel_mcp.git
cd fuel_mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest -v

# Run with coverage
pytest --cov=fuel_mcp --cov-report=html
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Based on **ISO 91-1** and **ASTM D1250** standards
- Built with [FastAPI](https://fastapi.tiangolo.com/), [Gradio](https://gradio.app/), and [LangChain](https://www.langchain.com/)
- Tested with comprehensive pytest suite

---

## 📞 Support

- **Documentation:** See `docs/` folder for detailed guides
- **Issues:** [GitHub Issues](https://github.com/Zubastic120993/fuel_mcp/issues)
- **Quick Help:** Check [Troubleshooting](#-troubleshooting) section above

---

## 🎯 Quick Links

- ⚡ **[Quick Start Guide](docs/QUICKSTART.md)** — Get running in 5 minutes
- 🐳 **[Docker Guide](docs/README-DOCKER.md)** — Complete Docker deployment
- 💻 **[Installation Guide](docs/INSTALL-LOCAL.md)** — Local setup instructions
- 📋 **[Command Reference](docs/COMMANDS.md)** — All available commands
- 📊 **[API Documentation](http://localhost:8000/docs)** — Interactive API docs (when running)
- 📝 **[Changelog](docs/CHANGELOG.md)** — Version history

---

**Made with ⚡ for the petroleum and marine industries**
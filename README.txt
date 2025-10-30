⚙️ Fuel MCP — Marine Fuel Correction Processor

Fuel MCP is a local analytical engine for precise fuel mass–volume corrections based on ISO 91-1 / ASTM D1250 standards.
It provides both a FastAPI service and a Python module interface, enabling use in standalone tools or AI-assisted agent environments.

------------------------------------------------------------
🚀 Features
------------------------------------------------------------
- Accurate Volume Correction Factor (VCF) calculations for all marine fuels
- Automatic mass ↔ volume correction at observed temperature
- ASTM Table-based unit conversions (Table 1 & 54B)
- FastAPI REST endpoints for integration
- JSON logs and automated tests
- Offline operation (no external API)

------------------------------------------------------------
🧩 Installation
------------------------------------------------------------
1️⃣ Clone repository:
    git clone https://github.com/yourusername/fuel_mcp.git
    cd fuel_mcp

2️⃣ Create virtual environment:
    python3 -m venv venv
    source venv/bin/activate

3️⃣ Install dependencies:
    pip install -r requirements.txt

   or install as a package:
    pip install .

------------------------------------------------------------
🧪 Run Local API
------------------------------------------------------------
    uvicorn fuel_mcp.api.mcp_api:app --reload

Then open in your browser:
    http://127.0.0.1:8000/docs

------------------------------------------------------------
🧠 API Endpoints
------------------------------------------------------------
Endpoint         | Method | Description
------------------------------------------------------------
/status          | GET    | Check service status
/query           | GET    | Run semantic fuel query
/convert         | GET    | ASTM Table 1 unit conversion
/vcf             | GET    | Compute VCF (ISO 91-1 / ASTM D1250)
/auto_correct    | GET    | Automatic mass/volume correction
/units           | GET    | General converter
/history         | GET    | View previous queries
/logs            | GET    | Access logs (JSON)

------------------------------------------------------------
📊 Example Usage
------------------------------------------------------------
Example 1 – VCF Auto-Correction:
    curl "http://127.0.0.1:8000/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25"

Response:
    {
      "table": "54B (Residual / Marine fuels)",
      "VCF": 0.99167,
      "V15_m3": 991.67,
      "mass_ton": 842.9
    }

Example 2 – Direct VCF:
    curl "http://127.0.0.1:8000/vcf?rho15=850&tempC=25"

------------------------------------------------------------
🧰 Run Tests
------------------------------------------------------------
    pytest -v

Expected:
    15 passed, 0 failed

------------------------------------------------------------
🧱 Project Structure
------------------------------------------------------------
fuel_mcp/
 ├── api/                # FastAPI endpoints
 ├── core/               # Core calculation engine
 ├── rag/                # RAG metadata & tables
 ├── tests/              # Pytest suites
 ├── logs/               # JSON logs
 └── pyproject.toml      # Build config

------------------------------------------------------------
🧩 License
------------------------------------------------------------
© 2025 Volodymyr Zub – All rights reserved.

------------------------------------------------------------
📬 Contact
------------------------------------------------------------
Chief Engineer Volodymyr Zub
your.email@example.com

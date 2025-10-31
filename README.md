# ⚙️ Fuel MCP — Marine Fuel Correction Processor

**Fuel MCP** is a local analytical engine for precise fuel mass–volume corrections based on **ISO 91-1 / ASTM D1250** standards.  
It provides both a **FastAPI service** and a **Python module interface**, enabling use in standalone tools or AI-assisted agent environments.

---

## 🚀 Features
- Accurate **Volume Correction Factor (VCF)** calculations for all marine fuels  
- Automatic **mass ↔ volume correction** at observed temperature  
- ASTM Table-based unit conversions (Table 1 & 54B)  
- **FastAPI REST endpoints** for integration  
- **Asynchronous (non-blocking) logging** via `async_logger`  
- Built-in **database metrics** and **error tracking endpoints**  
- **JSON logs** and full Pytest coverage  
- Works completely **offline**

---

## 🧩 Installation

### 1️⃣ Clone repository
```bash
git clone https://github.com/yourusername/fuel_mcp.git
cd fuel_mcp
```

### 2️⃣ Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ (Optional) Install as a package
```bash
pip install .
```

---

## 🧪 Run Local API
```bash
uvicorn fuel_mcp.api.mcp_api:app --reload
```

Then open in browser:
```
http://127.0.0.1:8000/docs
```

---

## 🧠 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/status` | GET | Check service status (online/offline) |
| `/query` | GET | Run semantic MCP query |
| `/convert` | GET | ASTM Table 1 unit conversion |
| `/vcf` | GET | Compute ISO 91-1 / ASTM D1250 VCF |
| `/auto_correct` | GET | Automatic mass/volume correction |
| `/errors` | GET | View recent recorded errors |
| `/metrics` | GET | View performance statistics (query counts, ratios) |
| `/history` | GET | View recent queries (SQLite) |
| `/logs` | GET | View recent log entries |
| `/tool` | GET | Get OpenAI-compatible JSON schema for MCP Tool |

---

## 📊 Example Usage

### Example 1 – Auto-Correction
```bash
curl "http://127.0.0.1:8000/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25"
```

Response:
```json
{
  "table": "54B (Residual / Marine fuels)",
  "VCF": 0.99167,
  "V15_m3": 991.67,
  "mass_ton": 842.9
}
```

### Example 2 – Direct VCF
```bash
curl "http://127.0.0.1:8000/vcf?rho15=850&tempC=25"
```

Response:
```json
{
  "table": "54B (Residual / Marine fuels)",
  "VCF": 0.99154
}
```

---

## 🧰 Run Tests
```bash
pytest -v
```
Expected output:
```
20 passed, 0 failed
```

---

## 🧱 Project Structure
```
fuel_mcp/
 ├── api/                 # FastAPI endpoints
 ├── core/                # Core calculation engine and database logic
 │   ├── async_logger.py  # Async non-blocking database logging
 │   ├── db_logger.py     # SQLite logging utilities
 │   ├── vcf_official_full.py  # ISO/ASTM correction engine
 │   └── cli.py           # Maintenance CLI commands
 ├── tests/               # Full pytest coverage (API + CLI + async)
 ├── logs/                # JSON logs
 └── pyproject.toml       # Build configuration
```

---

## ⚙️ Maintenance CLI

The Fuel MCP CLI provides simple maintenance commands:

| Command | Description |
|----------|-------------|
| `mcp-cli db stats` | Show total queries, success %, and last error |
| `mcp-cli db clean --days 30` | Remove logs older than 30 days |
| `mcp-cli status` | Display log info and system status |
| `mcp-cli history` | Show last queries |
| `mcp-cli vcf diesel 25` | Quick VCF calculation |
| `mcp-cli convert "convert 1 m3 to liters"` | Quick conversion query |

---

## 🧩 License
© 2025 **Volodymyr Zub** — All rights reserved.

---

## 📬 Contact
**Chief Engineer Volodymyr Zub**  
📧 [your.email@example.com](mailto:your.email@example.com)

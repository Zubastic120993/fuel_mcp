# ⚙️ Fuel MCP — Marine Fuel Correction Processor

**Fuel MCP** is a local analytical engine for precise fuel mass–volume corrections based on **ISO 91-1 / ASTM D1250** standards.  
It provides both a **FastAPI REST service** and a **Python module interface**, enabling use in standalone engineering tools or AI-powered agent environments.

---

## 🚀 Features

- ✅ Accurate **Volume Correction Factor (VCF)** calculations for all marine fuels  
- 🔁 Automatic **mass ↔ volume correction** at observed temperature  
- 📏 ASTM Table-based unit conversions (**Table 1**, **Table 54B**)  
- 🧠 **Semantic natural language queries** (“convert 850 kg/m³ to tons”)  
- ⚙️ **FastAPI REST endpoints** for local or remote integration  
- 🧩 **Asynchronous logging** (non-blocking DB writes via asyncio)  
- 🧾 **SQLite-backed history and error tracking**  
- 🧰 **Maintenance CLI** for DB cleanup, statistics, and optimization  
- 💾 Works completely **offline** (local vector store)  

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

### 4️⃣ (Optional) Install as editable package
```bash
pip install -e .
```

---

## 🧪 Run Local API
```bash
uvicorn fuel_mcp.api.mcp_api:app --reload
```

Then open in your browser:
```
http://127.0.0.1:8000/docs
```

---

## 🧠 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/status` | GET | Check service status and mode (ONLINE/OFFLINE) |
| `/query` | GET | Run semantic fuel query |
| `/convert` | GET | Perform ASTM Table 1 unit conversion |
| `/vcf` | GET | Compute ISO 91-1 / ASTM D1250 VCF |
| `/auto_correct` | GET | Automatic mass ↔ volume correction |
| `/errors` | GET | Retrieve recent internal error logs (SQLite) |
| `/metrics` | GET | Return system performance statistics |
| `/history` | GET | View query history from SQLite |
| `/logs` | GET | Read recent log file entries |
| `/tool` | GET | Get OpenAI-compatible JSON schema |

---

## 📊 Example Usage

### Example 1 – Automatic Correction
```bash
curl "http://127.0.0.1:8000/auto_correct?fuel=diesel&rho15=850&volume_m3=1000&tempC=25"
```
Response:
```json
{
  "table": "54B (Residual / Marine fuels)",
  "rho15": 850.0,
  "tempC": 25.0,
  "VCF": 0.99167,
  "V15_m3": 991.67,
  "mass_ton": 842.9
}
```

### Example 2 – Conversion Query
```bash
curl "http://127.0.0.1:8000/convert?value=1&from_unit=liter&to_unit=m3"
```
Response:
```json
{
  "input": {"value": 1, "from": "liter", "to": "m3"},
  "result": 0.001
}
```

### Example 3 – Engine Metrics
```bash
curl http://127.0.0.1:8000/metrics
```
Response:
```json
{
  "total_queries": 128,
  "successful_queries": 125,
  "failed_queries": 3,
  "success_ratio": "97.7%",
  "last_query_time": "2025-10-30T23:10:44.122Z",
  "db_path": "/fuel_mcp/data/mcp_history.db"
}
```

---

## 🧰 Maintenance CLI

### Check Database Statistics
```bash
mcp-cli db stats
```
Output:
```
📊 Fuel MCP — Database Statistics
  • Total queries: 120
  • Successful:   118
  • Failed:       2
  • Success rate: 98.3%
  • Last query:   2025-10-30 T23:16:12 Z
  • Last error:   2025-10-29 T22:45:00 Z
```

### Clean Old Records
```bash
mcp-cli db clean --days 60
🧹 Removed 42 old records (older than 60 days).
```

### Compact Database
```bash
mcp-cli db vacuum
```

---

## 🧪 Run Tests
```bash
pytest -v
```
Expected output:
```
✔ All tests passed (20 / 20)
```

All test suites validated:  
- API endpoints  
- Async logging  
- Metrics  
- CLI maintenance tools  

---

## 🧱 Project Structure
```
fuel_mcp/
 ├── api/                # FastAPI endpoints
 ├── core/               # Core engine & async logging
 ├── data/               # SQLite database (mcp_history.db)
 ├── logs/               # Log files
 ├── tests/              # Unit & integration tests
 └── pyproject.toml      # Build configuration
```

---

## 📦 Version
**Current Release:** v1.4.3  
**Branch:** `feature/agent-integration`  
**Author:** Chief Engineer **Volodymyr Zub**

---

## 🧩 License
© 2025 Volodymyr Zub — All rights reserved.

---

## 📬 Contact
**Chief Engineer Volodymyr Zub**  
📧 [your.email@example.com](mailto:your.email@example.com)
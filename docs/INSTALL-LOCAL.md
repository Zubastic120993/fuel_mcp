# 💻 Fuel MCP — Local Installation (Without Docker)

This guide shows you how to install and run Fuel MCP **without Docker**, using only Python.

---

## 📋 Prerequisites

- **Python 3.10+** (3.12 recommended)
- **pip** (Python package manager)
- **Git** (to clone the repository)

### Check Python Version
```bash
python3 --version
# Should show Python 3.10.0 or higher
```

---

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
git clone --branch feature/docker-gradio-package https://github.com/Zubastic120993/fuel_mcp.git fuel_mcp_gradio
cd fuel_mcp_gradio
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python3 -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements-gradio.txt
```

This installs:
- Gradio (web UI)
- FastAPI (API backend)
- Uvicorn (web server)
- NumPy, Pandas (data processing)
- Other dependencies

**Installation time:** ~2-5 minutes (depending on internet speed)

---

## ▶️ Running the Application

You need to run **two services**:
1. **Backend API** (FastAPI) - Port 8000
2. **Frontend UI** (Gradio) - Port 7860

### Option A: Run Both in Separate Terminals (Recommended)

#### Terminal 1: Start Backend API
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start backend
uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Terminal 2: Start Frontend UI
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start Gradio frontend
python -m fuel_mcp.gui_astm.app_astm_unified
```

You should see:
```
Running on local URL:  http://127.0.0.1:7860
```

### Option B: Run with Background Process (Advanced)

**On macOS/Linux:**
```bash
# Start backend in background
uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &

# Start frontend
python -m fuel_mcp.gui_astm.app_astm_unified
```

**Stop backend:**
```bash
pkill -f "uvicorn fuel_mcp.api.mcp_api"
```

**On Windows:**
Use PowerShell or create batch files for each service.

---

## 🌐 Access the Application

Once both services are running:

- **Gradio Web Interface**: http://localhost:7860
- **API Documentation**: http://localhost:8000/docs
- **API Status**: http://localhost:8000/status

The browser should open automatically, or you can manually navigate to the URLs above.

---

## 🧪 Test the Installation

### Test Backend API
```bash
curl http://localhost:8000/status
```

Should return:
```json
{"status":"ok","mode":"OFFLINE",...}
```

### Test VCF Calculation
```bash
curl "http://localhost:8000/vcf?rho15=850&tempC=25"
```

Should return VCF calculation results.

---

## ⏸️ Stop the Application

1. **Stop Frontend**: Press `Ctrl+C` in the Gradio terminal
2. **Stop Backend**: Press `Ctrl+C` in the backend terminal

---

## 🔧 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find what's using the port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change ports
# For backend, use: --port 8001
# For frontend, edit app_astm_unified.py port
```

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'fuel_mcp'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies again
pip install -r requirements-gradio.txt

# Or install as package
pip install .
```

### Frontend Can't Connect to Backend

**Error:** `HTTPConnectionPool: Max retries exceeded`

**Solution:**
1. Make sure backend is running on port 8000
2. Check that frontend is using `http://127.0.0.1:8000` (default for local)
3. Verify no firewall is blocking the connection

### Python Version Issues

**Error:** `Python version must be 3.10 or higher`

**Solution:**
```bash
# Install Python 3.12
# macOS: brew install python@3.12
# Linux: sudo apt install python3.12
# Windows: Download from python.org
```

---

## 📦 Uninstall (Optional)

To remove the local installation:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # On Windows: rmdir /s venv

# Remove project (optional)
cd ..
rm -rf fuel_mcp_gradio
```

---

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest code
git pull

# Update dependencies
pip install --upgrade -r requirements-gradio.txt
```

---

## 📊 Comparison: Docker vs Local

| Feature | Docker | Local |
|---------|--------|-------|
| **Setup Time** | 5 minutes | 5-10 minutes |
| **Dependencies** | Automatic | Manual |
| **Isolation** | Yes | No (uses system Python) |
| **Portability** | Excellent | Good |
| **Resource Usage** | Higher | Lower |
| **Best For** | Production, consistency | Development, simplicity |

---

## 💡 Tips

1. **Keep both terminals open** - You need both services running
2. **Check logs** - Backend logs appear in terminal, frontend shows errors in browser
3. **Use virtual environment** - Always activate `venv` before running
4. **API first** - Start backend before frontend for best results

---

## 🆘 Need Help?

- **Check logs**: Look at terminal output for errors
- **Verify ports**: Make sure 8000 and 7860 are available
- **Test API**: Try `curl http://localhost:8000/status`
- **Reinstall**: Delete `venv` and reinstall dependencies

---

## ✅ Quick Reference

**Install:**
```bash
git clone --branch feature/docker-gradio-package https://github.com/Zubastic120993/fuel_mcp.git fuel_mcp_gradio
cd fuel_mcp_gradio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-gradio.txt
```

**Run:**
```bash
# Terminal 1
uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000

# Terminal 2
python -m fuel_mcp.gui_astm.app_astm_unified
```

**Access:**
- UI: http://localhost:7860
- API: http://localhost:8000/docs


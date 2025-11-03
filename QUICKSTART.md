# 🚀 Fuel MCP — Quick Start Guide

Get up and running with Fuel MCP in **less than 5 minutes**!

---

## 🐳 Docker Installation (Recommended)

### Step 1: Prerequisites
- Install [Docker Desktop](https://docs.docker.com/get-docker/)
- Ensure Docker is running

### Step 2: Start Application

```bash
./start-docker.sh start
```

Or manually:

```bash
docker-compose -f docker-compose-gradio.yml up
```

### Step 3: Access Application

- **Gradio Interface**: http://localhost:7860
- **API Documentation**: http://localhost:8000/docs

### Step 4: Test It Out

Try this in the **API Gravity Entry** tab:
- API Gravity: `30.0`
- Temperature: `60` °F
- Click **"Compute ASTM Tables"**

---

## 💻 Local Installation (Alternative)

### Step 1: Install Python 3.12+

```bash
python3 --version  # Should be 3.12 or higher
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements-gradio.txt
```

### Step 4: Start Backend

```bash
uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000
```

### Step 5: Start Frontend (New Terminal)

```bash
source venv/bin/activate  # Activate venv again
python -m fuel_mcp.gui_astm.app_astm_unified
```

### Step 6: Access Application

- **Gradio Interface**: http://localhost:7860
- **API Documentation**: http://localhost:8000/docs

---

## 📊 Available Calculators

| Calculator | Description | Example |
|------------|-------------|---------|
| **API Gravity Entry** | Convert API gravity to density and related units | API=30°, Temp=60°F |
| **Relative Density** | Convert relative density to API and density | Rel.Density=0.8762 |
| **Density Entry** | Calculate VCF from density and temperature | Density=875.7 kg/m³ |
| **Volume & Weight** | Convert between volume and weight units | 100 m³ → US Gallons |
| **Universal Converter** | General unit conversions | 1 barrel → litres |

---

## 🧪 Quick Test

### Test Backend API

```bash
# Test VCF calculation
curl "http://localhost:8000/vcf?rho15=850&tempC=25"

# Test unit conversion
curl "http://localhost:8000/convert?value=1&from_unit=barrel&to_unit=litre"
```

**Expected Output:**
```json
{
  "status": "success",
  "result": {
    "value": 158.987,
    "unit": "litre"
  }
}
```

---

## 🛑 Stop Services

### Docker

```bash
./start-docker.sh stop
```

Or:

```bash
docker-compose -f docker-compose-gradio.yml down
```

### Local Installation

Press `Ctrl+C` in both terminal windows

---

## 📖 Next Steps

- Read [README-DOCKER.md](README-DOCKER.md) for detailed Docker configuration
- Explore the [API Documentation](http://localhost:8000/docs)
- Check [README.md](README.md) for development setup

---

## 🆘 Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Change ports in `docker-compose-gradio.yml`:

```yaml
ports:
  - "8080:8000"  # Change 8000 to 8080
  - "7870:7860"  # Change 7860 to 7870
```

### Backend Not Responding

**Check if backend is running:**

```bash
docker-compose -f docker-compose-gradio.yml ps
```

**View backend logs:**

```bash
docker-compose -f docker-compose-gradio.yml logs backend
```

### Frontend Cannot Connect

**Ensure backend is healthy:**

```bash
curl http://localhost:8000/status
```

**Expected response:**
```json
{
  "status": "success",
  "result": {
    "status": "operational"
  }
}
```

---

## 💡 Tips

- Use `./start-docker.sh logs` to view real-time logs
- Use `./start-docker.sh status` to check service health
- Use `./start-docker.sh test` to run automated tests
- Data is persisted in `fuel_mcp/data/` and `logs/` directories

---

**Need help?** Check [README-DOCKER.md](README-DOCKER.md) for detailed documentation.


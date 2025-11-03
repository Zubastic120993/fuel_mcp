# 🧩 Fuel MCP — Docker Deployment Guide

## Overview

This Docker package provides a production-ready deployment of **Fuel MCP Gradio Application** with:
- ✅ **FastAPI Backend** (Port 8000) — ISO 91-1 / ASTM D1250 computation engine
- ✅ **Gradio Frontend** (Port 7860) — Unified web interface for all calculators
- ✅ **Optimized Build** — Minimal dependencies, fast startup
- ✅ **Easy Installation** — One command to run everything

---

## 📋 Prerequisites

- **Docker** 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ (included with Docker Desktop)
- **4GB RAM minimum** (recommended: 8GB)
- **2GB disk space**

---

## 🚀 Quick Start

### 1. Build and Run (Single Command)

```bash
docker-compose -f docker-compose-gradio.yml up
```

This will:
1. Build the Docker image (first time only, ~2-5 minutes)
2. Start the FastAPI backend on `http://localhost:8000`
3. Start the Gradio frontend on `http://localhost:7860`

### 2. Run in Background (Detached Mode)

```bash
docker-compose -f docker-compose-gradio.yml up -d
```

### 3. Access the Application

- **Gradio Web Interface**: http://localhost:7860
- **FastAPI Backend (API Docs)**: http://localhost:8000/docs
- **API Status Check**: http://localhost:8000/status

### 4. Stop the Services

```bash
docker-compose -f docker-compose-gradio.yml down
```

---

## 📦 Available Calculators

The unified Gradio interface includes all ASTM D1250 calculators:

### 🌡️ API Gravity Entry (Tab 1)
Calculate ASTM tables from API gravity and temperature.

**Example Input:**
- API Gravity: 30.0 °API
- Temperature: 60°F

**Outputs:** Density @15°C, VCF, Relative Density, conversion factors

---

### 📊 Relative Density Entry (Tab 2)
Calculate ASTM tables from relative density (60/60°F).

**Example Input:**
- Relative Density: 0.8762
- Temperature: 100°F

**Outputs:** API Gravity, Density @15°C, VCF, conversion factors

---

### 🧪 Density Entry (Tab 3)
Calculate VCF and equivalents from density.

**Example Input:**
- Density @15°C: 875.7 kg/m³
- Temperature: 32.2°C

**Outputs:** API Gravity, Relative Density, VCF, ASTM table reference

---

### ⚖️ Volume & Weight Converter (Tab 4)
Convert between volume and weight units with temperature correction.

**Example Input:**
- Density @15°C: 796.7 kg/m³
- Observed Temperature: 22.6°C
- Convert: 100 M³ @15°C → US Gallons @60°F

**Outputs:** Temperature-corrected conversions

---

### 🔄 Universal Unit Converter (Tab 5)
Convert between standard petroleum measurement units.

**Unit Groups:**
- **Mass/Weight** ⚖️: kg, lb, tonne, short ton, long ton
- **Volume/Capacity** 🧴: litre, US gallon, imperial gallon, barrel, m³, ft³, in³
- **Length** 📏: metre, yard, foot, inch, cm

**Example:**
- Input: 1 barrel
- Output: 158.987 litres (ASTM D1250-80 Vol XI Table 1)

---

## 🔧 Advanced Configuration

### Custom Ports

Edit `docker-compose-gradio.yml` to change ports:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to your desired port
  
  frontend:
    ports:
      - "7870:7860"  # Change 7870 to your desired port
```

### Data Persistence

The following directories are mounted as volumes for data persistence:

- `./fuel_mcp/data` → SQLite database (query history, logs)
- `./logs` → Application logs

These directories will persist data even after container restarts.

---

## 🏗️ Manual Build

If you need to rebuild the image manually:

```bash
docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest .
```

---

## 🔍 Troubleshooting

### Backend Not Starting

**Check logs:**
```bash
docker-compose -f docker-compose-gradio.yml logs backend
```

**Common issues:**
- Port 8000 already in use → Change port in docker-compose-gradio.yml
- Insufficient memory → Increase Docker memory limit

### Frontend Cannot Connect to Backend

**Verify backend is healthy:**
```bash
curl http://localhost:8000/status
```

**Expected response:**
```json
{
  "status": "success",
  "result": {
    "service": "Fuel MCP Local API",
    "status": "operational",
    "version": "1.5.0"
  }
}
```

### Permission Errors

**Linux users:** Add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
(Logout and login again)

---

## 📊 API Endpoints

The FastAPI backend provides the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Health check and service status |
| `/vcf` | GET | Calculate VCF for density and temperature |
| `/query` | GET | Natural language query parser |
| `/convert` | GET | Unit conversion |
| `/correlate` | GET | ASTM table interpolation |
| `/auto_correct` | GET | Temperature correction for volume/mass |
| `/debug` | GET | System diagnostics |
| `/metrics` | GET | Query statistics |
| `/errors` | GET | Error log viewer |

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing the Deployment

### 1. Test Backend API

```bash
# Test VCF calculation
curl "http://localhost:8000/vcf?rho15=850&tempC=25"

# Test unit conversion
curl "http://localhost:8000/convert?value=1&from_unit=barrel&to_unit=litre"

# Test natural language query
curl "http://localhost:8000/query?text=convert+500+liters+diesel+at+30C"
```

### 2. Test Gradio Frontend

Open browser to http://localhost:7860 and try:
- API Gravity Entry: API=30, Temp=60°F → Click "Compute ASTM Tables"
- Universal Converter: 1 barrel → litres

---

## 📦 Production Deployment

### Using Docker Hub

1. **Tag the image:**
```bash
docker tag fuel-mcp-gradio:latest yourusername/fuel-mcp-gradio:latest
```

2. **Push to Docker Hub:**
```bash
docker push yourusername/fuel-mcp-gradio:latest
```

3. **Deploy on server:**
```bash
docker pull yourusername/fuel-mcp-gradio:latest
docker-compose -f docker-compose-gradio.yml up -d
```

### Environment Variables

Set these in `docker-compose-gradio.yml` for production:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=INFO
  - MAX_WORKERS=4
```

---

## 🔐 Security Considerations

### Network Security

- **Firewall**: Only expose necessary ports (8000, 7860)
- **Reverse Proxy**: Use nginx/traefik for HTTPS in production
- **API Keys**: Add authentication if exposing to internet

### Container Security

- ✅ Non-root user (UID 10001)
- ✅ Minimal base image (python:3.12-slim)
- ✅ No unnecessary dependencies
- ✅ Read-only filesystem where possible

---

## 📈 Resource Usage

Typical resource consumption:

| Service | CPU (idle) | CPU (load) | Memory | Disk |
|---------|------------|------------|--------|------|
| Backend | ~5% | ~30% | 150 MB | 50 MB |
| Frontend | ~3% | ~20% | 300 MB | 100 MB |
| **Total** | **~8%** | **~50%** | **450 MB** | **150 MB** |

---

## 🛠️ Development Mode

For development with hot-reload:

```yaml
# Add to backend service in docker-compose-gradio.yml
volumes:
  - ./fuel_mcp:/app/fuel_mcp
command: ["uvicorn", "fuel_mcp.api.mcp_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 📝 File Structure

```
fuel_mcp/
├── Dockerfile.gradio              # Optimized Dockerfile
├── docker-compose-gradio.yml      # Multi-service orchestration
├── requirements-gradio.txt        # Minimal dependencies
├── .dockerignore                  # Build optimization
├── fuel_mcp/
│   ├── api/                       # FastAPI backend
│   ├── gui_astm/                  # Gradio frontends
│   ├── core/                      # Computation engine
│   ├── tables/official/normalized/  # ASTM data tables
│   └── data/                      # SQLite database (persistent)
└── logs/                          # Application logs (persistent)
```

---

## 🆘 Support

### Logs and Diagnostics

View real-time logs:
```bash
# Backend logs
docker-compose -f docker-compose-gradio.yml logs -f backend

# Frontend logs
docker-compose -f docker-compose-gradio.yml logs -f frontend

# All logs
docker-compose -f docker-compose-gradio.yml logs -f
```

### Health Checks

```bash
# Check service health
docker-compose -f docker-compose-gradio.yml ps

# Backend diagnostics
curl http://localhost:8000/debug
```

---

## 📚 References

- **ASTM D1250-80**: Standard Guide for Petroleum Measurement Tables
- **ISO 91-1**: Petroleum measurement tables - Density
- **FastAPI**: https://fastapi.tiangolo.com/
- **Gradio**: https://gradio.app/
- **Docker**: https://docs.docker.com/

---

## 📄 License

Copyright © 2025 Fuel MCP Project

---

## ✨ Version

**Fuel MCP Gradio Docker Package v2.0.0**
- Date: 2025-11-03
- Python: 3.12
- FastAPI: 0.115.0
- Gradio: 5.7.1

---

*For issues, feature requests, or contributions, please contact the development team.*


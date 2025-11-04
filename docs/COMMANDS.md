# 🚀 Fuel MCP — Quick Command Reference

## 📦 Installation

### Option 1: Docker Installation (Recommended)

#### First-time Setup (from scratch)
```bash
# Clone and build the project
./install.sh
```

#### Manual Installation Steps
```bash
# 1. Clone repository (if not already done)
git clone https://github.com/Zubastic120993/fuel_mcp.git
cd fuel_mcp_gradio

# 2. Build Docker image
docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest .

# OR use docker-compose to build
docker-compose -f docker-compose-gradio.yml build
```

### Option 2: Local Installation (Without Docker)

**See detailed guide:** [INSTALL-LOCAL.md](INSTALL-LOCAL.md)

#### Quick Setup:
```bash
# 1. Clone repository
git clone https://github.com/Zubastic120993/fuel_mcp.git
cd fuel_mcp_gradio

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-gradio.txt

# 4. Start backend (Terminal 1)
uvicorn fuel_mcp.api.mcp_api:app --host 0.0.0.0 --port 8000

# 5. Start frontend (Terminal 2)
python -m fuel_mcp.gui_astm.app_astm_unified
```

**Access:**
- Gradio UI: http://localhost:7860
- API Docs: http://localhost:8000/docs

---

## ▶️ Start Services

### Using Helper Script (Recommended)
```bash
./start-docker.sh start
```

### Manual Docker Compose
```bash
docker-compose -f docker-compose-gradio.yml up -d --build
```

### What gets started:
- **Backend API** → http://localhost:8000
- **Gradio Frontend** → http://localhost:7860
- **API Docs** → http://localhost:8000/docs

---

## ⏸️ Stop Services

### Using Helper Script (Recommended)
```bash
./start-docker.sh stop
```

### Manual Docker Compose
```bash
docker-compose -f docker-compose-gradio.yml down
```

### Force Stop (removes containers)
```bash
docker-compose -f docker-compose-gradio.yml down --remove-orphans
```

---

## 🔁 Restart Services

```bash
./start-docker.sh restart
```

---

## 🧪 Test Services

```bash
./start-docker.sh test
```

Tests:
- Backend API health check
- VCF calculation endpoint
- Unit conversion endpoint

---

## 📜 View Logs

### Real-time Logs (Follow Mode)
```bash
./start-docker.sh logs
```

### Manual Logs
```bash
# All services
docker-compose -f docker-compose-gradio.yml logs -f

# Backend only
docker-compose -f docker-compose-gradio.yml logs -f backend

# Frontend only
docker-compose -f docker-compose-gradio.yml logs -f frontend
```

---

## 🧹 Clean Up (Stop + Remove Resources)

### Safe Cleanup (keeps images)
```bash
./start-docker.sh clean
```

### Manual Cleanup
```bash
# Stop and remove containers, networks, volumes
docker-compose -f docker-compose-gradio.yml down -v --remove-orphans

# Remove dangling images
docker image prune -af --filter "dangling=true"
```

---

## 🗑️ Uninstall (Complete Removal)

### Using Uninstall Script
```bash
# Full uninstall (removes everything including code)
./uninstall.sh

# Keep code, only remove Docker resources
KEEP_CODE=1 ./uninstall.sh
```

### Manual Uninstall Steps
```bash
# 1. Stop and remove containers
docker-compose -f docker-compose-gradio.yml down --remove-orphans

# 2. Remove containers by name
docker rm -f fuel_mcp_backend fuel_mcp_gradio 2>/dev/null || true

# 3. Remove images
docker rmi -f fuel-mcp-gradio:latest 2>/dev/null || true

# 4. Remove networks
docker network rm fuel_mcp_gradio_fuel_mcp_network 2>/dev/null || true

# 5. Remove project directory (optional)
rm -rf fuel_mcp_gradio/
```

---

## 🔍 Status & Monitoring

### Check Container Status
```bash
docker ps | grep fuel_mcp
```

### Check Health
```bash
# Backend health check
curl http://localhost:8000/status

# Frontend check
curl -I http://localhost:7860
```

### View Container Details
```bash
docker-compose -f docker-compose-gradio.yml ps
```

---

## 📋 All Available Commands Summary

| Command | Description |
|---------|-------------|
| `./install.sh` | Install and build project |
| `./start-docker.sh start` | Build and start services |
| `./start-docker.sh stop` | Stop services |
| `./start-docker.sh restart` | Restart services |
| `./start-docker.sh test` | Run health tests |
| `./start-docker.sh logs` | View logs |
| `./start-docker.sh clean` | Clean up resources |
| `./uninstall.sh` | Complete uninstall |

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :7860

# Stop conflicting services or change ports in docker-compose-gradio.yml
```

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh
```

### Container Won't Start
```bash
# Check logs
./start-docker.sh logs

# Restart from scratch
./start-docker.sh stop
./start-docker.sh clean
./start-docker.sh start
```

---

## 📍 Access Points (After Start)

- **Gradio UI**: http://localhost:7860
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/status


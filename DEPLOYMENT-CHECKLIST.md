# ✅ Fuel MCP — Deployment Package Checklist

## 📦 Package Contents

This deployment package includes everything needed to run Fuel MCP Gradio application in Docker.

---

## 🗂️ Core Files

### Docker Configuration
- ✅ `Dockerfile.gradio` — Optimized multi-stage Dockerfile
- ✅ `docker-compose-gradio.yml` — Multi-service orchestration
- ✅ `.dockerignore` — Build optimization (excludes unnecessary files)
- ✅ `requirements-gradio.txt` — Minimal Python dependencies

### Documentation
- ✅ `README-DOCKER.md` — Comprehensive Docker deployment guide
- ✅ `QUICKSTART.md` — 5-minute quick start guide
- ✅ `DEPLOYMENT-CHECKLIST.md` — This file

### Scripts
- ✅ `start-docker.sh` — Convenient startup script with commands:
  - `./start-docker.sh start` — Start services
  - `./start-docker.sh stop` — Stop services
  - `./start-docker.sh logs` — View logs
  - `./start-docker.sh status` — Check health
  - `./start-docker.sh test` — Run tests
  - `./start-docker.sh clean` — Remove all containers

---

## 📁 Required Application Files

### Core Modules (fuel_mcp/core/)
- ✅ `__init__.py`
- ✅ `unit_converter.py` — ASTM D1250-80 conversion factors
- ✅ `vcf_official_full.py` — VCF calculation engine
- ✅ `regex_parser.py` — Natural language query parser
- ✅ `response_schema.py` — Unified API response format
- ✅ `db_logger.py` — SQLite logging
- ✅ `async_logger.py` — Async logging utilities
- ✅ `error_handler.py` — Error management
- ✅ `fuel_density_loader.py` — Fuel data loader
- ✅ `conversion_engine.py` — Conversion engine
- ✅ `conversion_dispatcher.py` — Conversion dispatcher
- ✅ `calculations.py` — Calculation utilities

### API Backend (fuel_mcp/api/)
- ✅ `mcp_api.py` — FastAPI backend application
- ✅ `api_correlate.py` — ASTM table correlation router

### Gradio Frontend (fuel_mcp/gui_astm/)
- ✅ `app_astm_unified.py` — **Main unified interface** (all calculators)
- ✅ `app_astm_api.py` — API gravity calculator
- ✅ `app_astm_density.py` — Density calculator
- ✅ `app_astm_rel_density.py` — Relative density calculator
- ✅ `app_astm_vol_weight.py` — Volume/weight converter
- ✅ `app_astm_universal_converter.py` — Universal unit converter
- ✅ `app_astm_units.py` — Unit converter (alternative)

### Data Tables (fuel_mcp/tables/official/normalized/)
- ✅ 29 CSV files with ASTM correlation tables
- ✅ `ASTM_Table1_APIGravity60F_to_RelativeDensity60F_and_Density15C_norm.csv`
- ✅ Other ASTM tables for VCF calculations

### Additional Files
- ✅ `fuel_mcp/__init__.py` — Package initialization
- ✅ `fuel_mcp/__main__.py` — CLI entry point
- ✅ `fuel_mcp/tool_integration.py` — Tool integration layer
- ✅ `fuel_mcp/tool_interface.py` — Tool interface

---

## 🚀 Deployment Steps

### 1. Prerequisites Check
```bash
# Check Docker installation
docker --version  # Should be 20.10+
docker-compose --version  # Should be 2.0+

# Check available disk space
df -h  # Need at least 2GB free
```

### 2. Build Image
```bash
docker build -f Dockerfile.gradio -t fuel-mcp-gradio:latest .
```

**Expected result:**
- Build time: 2-5 minutes (first time)
- Image size: ~1.2 GB
- Status: Successfully built

### 3. Start Services
```bash
# Option A: Using convenience script
./start-docker.sh start

# Option B: Using docker-compose directly
docker-compose -f docker-compose-gradio.yml up -d
```

### 4. Verify Deployment
```bash
# Check container status
docker ps | grep fuel_mcp

# Test backend API
curl http://localhost:8000/status

# Test VCF calculation
curl "http://localhost:8000/vcf?rho15=850&tempC=25"

# Open browser
open http://localhost:7860  # macOS
xdg-open http://localhost:7860  # Linux
```

### 5. Access Application
- **Gradio Interface**: http://localhost:7860
- **API Documentation**: http://localhost:8000/docs
- **API Status**: http://localhost:8000/status

---

## 🧪 Testing Checklist

### Backend API Tests
- [ ] Health check: `GET /status` → Returns `"status": "operational"`
- [ ] VCF calculation: `GET /vcf?rho15=850&tempC=25` → Returns VCF value
- [ ] Unit conversion: `GET /convert?value=1&from_unit=barrel&to_unit=litre` → Returns 158.987
- [ ] Natural query: `GET /query?text=convert+500+liters+diesel+at+30C` → Returns result
- [ ] Correlation lookup: `GET /correlate?table=ASTM_Table1...&column=api_gravity_60f&value=30` → Returns interpolated data

### Gradio Frontend Tests
- [ ] API Gravity Entry: Input API=30, Temp=60°F → Shows ASTM tables
- [ ] Relative Density: Input Rel.Density=0.8762, Temp=100°F → Shows results
- [ ] Density Entry: Input Density=875.7, Temp=32.2°C → Shows VCF
- [ ] Volume/Weight Converter: Convert 100 M³ → US Gallons
- [ ] Universal Converter: Convert 1 barrel → litres (should show 158.987)

### System Tests
- [ ] Logs are accessible: `docker-compose -f docker-compose-gradio.yml logs`
- [ ] Data persistence: Stop/start containers, check if data persists
- [ ] Resource usage: Check CPU/Memory with `docker stats`
- [ ] Health checks: Backend responds within 10 seconds

---

## 📊 Expected Behavior

### Startup Sequence
1. Backend starts first (port 8000)
2. Backend health check passes
3. Frontend starts (port 7860)
4. All services operational within 30 seconds

### Resource Consumption
| Component | CPU (Idle) | CPU (Load) | Memory | Disk |
|-----------|------------|------------|--------|------|
| Backend   | 5-10%      | 20-40%     | 150 MB | 50 MB |
| Frontend  | 3-8%       | 15-30%     | 300 MB | 100 MB |

### Performance Benchmarks
- VCF calculation: < 50ms
- Unit conversion: < 10ms
- Natural query parsing: < 100ms
- Gradio page load: < 2 seconds

---

## 🔒 Security Checklist

- ✅ Non-root user (UID 10001) inside container
- ✅ Minimal base image (python:3.12-slim)
- ✅ No unnecessary system packages
- ✅ .dockerignore excludes sensitive files
- ✅ Read-only volumes where possible
- ✅ Health checks enabled
- ✅ Restart policy: unless-stopped

---

## 📝 Maintenance

### View Logs
```bash
# All logs
docker-compose -f docker-compose-gradio.yml logs -f

# Backend only
docker-compose -f docker-compose-gradio.yml logs -f backend

# Frontend only
docker-compose -f docker-compose-gradio.yml logs -f frontend
```

### Update Application
```bash
# Rebuild image
docker-compose -f docker-compose-gradio.yml build

# Restart services
docker-compose -f docker-compose-gradio.yml up -d
```

### Clean Up
```bash
# Stop and remove containers
docker-compose -f docker-compose-gradio.yml down

# Remove images
docker rmi fuel-mcp-gradio:latest

# Full cleanup (including volumes)
docker-compose -f docker-compose-gradio.yml down -v
```

---

## 🌐 Production Deployment

### Recommended Setup
1. **Reverse Proxy**: nginx or Traefik for HTTPS
2. **Domain**: Point domain to server IP
3. **SSL Certificate**: Let's Encrypt via certbot
4. **Firewall**: Only expose 80, 443
5. **Monitoring**: Prometheus + Grafana
6. **Backups**: Daily backup of `fuel_mcp/data/` directory

### Example nginx Configuration
```nginx
server {
    listen 80;
    server_name fuel-mcp.example.com;
    
    location / {
        proxy_pass http://localhost:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
    }
}
```

---

## 📋 Troubleshooting

### Build Failures
**Symptom:** Docker build fails
**Solutions:**
- Check disk space: `df -h`
- Clear Docker cache: `docker system prune -a`
- Verify file paths in Dockerfile.gradio

### Port Conflicts
**Symptom:** "Address already in use"
**Solutions:**
- Change ports in docker-compose-gradio.yml
- Stop conflicting services: `sudo lsof -i :8000`

### Permission Errors
**Symptom:** Cannot write to volumes
**Solutions:**
- Fix volume permissions: `sudo chown -R $(whoami) fuel_mcp/data logs`
- Check SELinux (Linux): `sudo setenforce 0`

### Backend Not Responding
**Symptom:** Frontend cannot connect to backend
**Solutions:**
- Check backend logs: `docker-compose -f docker-compose-gradio.yml logs backend`
- Verify backend health: `curl http://localhost:8000/status`
- Restart backend: `docker-compose -f docker-compose-gradio.yml restart backend`

---

## ✅ Pre-Deployment Final Check

Before deploying to production:

- [ ] Docker image builds successfully
- [ ] All backend endpoints respond correctly
- [ ] All Gradio tabs work properly
- [ ] Data persists across container restarts
- [ ] Logs are accessible and readable
- [ ] Health checks pass
- [ ] Resource usage is acceptable
- [ ] Documentation is complete
- [ ] Backup strategy is in place
- [ ] Monitoring is configured

---

## 📞 Support

For issues or questions:
1. Check logs: `./start-docker.sh logs`
2. Run diagnostics: `./start-docker.sh status`
3. Run tests: `./start-docker.sh test`
4. Review documentation: `README-DOCKER.md`

---

**Package Version:** 2.0.0  
**Last Updated:** 2025-11-03  
**Docker Image:** fuel-mcp-gradio:latest  
**Minimum Requirements:** Docker 20.10+, 4GB RAM, 2GB Disk


# 🐳 Fuel MCP — Docker Deployment Options

## Overview

You have **3 deployment options** for running Fuel MCP with Gradio. Here's a comparison:

---

## ⚠️ Your Simplified Dockerfile (WILL NOT WORK)

### Issues:
```dockerfile
# Your version only runs Gradio, but...
CMD ["python", "-m", "fuel_mcp.gui_astm.app_astm_unified"]
```

**Problems:**
1. ❌ **No backend API** — Gradio apps call `http://127.0.0.1:8000` which doesn't exist
2. ❌ **Missing files** — No `__main__.py`, `tool_integration.py`, `tool_interface.py`
3. ❌ **No security** — Runs as root user
4. ❌ **Missing directories** — No `fuel_mcp/data/`, `logs/`
5. ❌ **Will crash** — All VCF calculations will fail with connection errors

**Result:** Gradio starts but **all calculations fail** ❌

---

## ✅ Option 1: Multi-Service with Docker Compose (RECOMMENDED)

### What I Created:
```bash
./start-docker.sh start
```

**Architecture:**
```
┌─────────────────┐
│ Frontend (7860) │ ──HTTP─→ ┌─────────────────┐
│ Gradio UI       │           │ Backend (8000)  │
└─────────────────┘           │ FastAPI API     │
                              └─────────────────┘
```

**Pros:**
- ✅ **Works out of the box** — No modifications needed
- ✅ **Separate concerns** — Frontend/backend isolated
- ✅ **Easy scaling** — Scale frontend/backend independently
- ✅ **Health checks** — Automatic restarts
- ✅ **Production-ready** — Security hardened

**Cons:**
- Requires Docker Compose

**Usage:**
```bash
docker-compose -f docker-compose-gradio.yml up
# Access at http://localhost:7860
```

**Files:**
- `Dockerfile.gradio` — Multi-purpose image
- `docker-compose-gradio.yml` — Orchestration
- `start-docker.sh` — Convenience script

---

## ✅ Option 2: Single Container (Both Services)

### What I Created: `Dockerfile.gradio-single`

**Architecture:**
```
┌─────────────────────────────────┐
│  Container                      │
│  ├─ Backend (8000)              │
│  └─ Frontend (7860)             │
└─────────────────────────────────┘
```

**Pros:**
- ✅ **Single container** — Simpler deployment
- ✅ **Works correctly** — Backend included
- ✅ **No Docker Compose needed** — Just `docker run`

**Cons:**
- ⚠️ **Not recommended for production** — Mixing concerns
- ⚠️ **Harder to scale** — Must scale both together
- ⚠️ **If one crashes, both crash**

**Usage:**
```bash
docker build -f Dockerfile.gradio-single -t fuel-mcp:single .
docker run -p 7860:7860 -p 8000:8000 fuel-mcp:single
# Access at http://localhost:7860
```

---

## ✅ Option 3: Gradio Only (External Backend)

### Requires: Code modifications + separate backend

**Architecture:**
```
┌─────────────────┐          ┌─────────────────┐
│ Gradio (7860)   │ ──HTTP─→ │ External Backend│
│ (Container)     │          │ (Separate host) │
└─────────────────┘          └─────────────────┘
```

**Required Changes:**

1. **Modify all Gradio apps** to read API URL from environment:

```python
# app_astm_unified.py (and all others)
import os
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
```

2. **Simplified Dockerfile:**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements-gradio.txt .
RUN pip install -r requirements-gradio.txt
COPY fuel_mcp/__init__.py fuel_mcp/
COPY fuel_mcp/core/__init__.py fuel_mcp/core/
COPY fuel_mcp/core/unit_converter.py fuel_mcp/core/
COPY fuel_mcp/gui_astm/ fuel_mcp/gui_astm/
RUN useradd -m -u 10001 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 7860
CMD ["python", "-m", "fuel_mcp.gui_astm.app_astm_unified"]
```

3. **Run with environment variable:**
```bash
docker run -p 7860:7860 \
  -e API_URL=http://your-backend:8000 \
  fuel-mcp:frontend-only
```

**Pros:**
- ✅ **Minimal frontend container** — Smallest image
- ✅ **Backend can be anywhere** — Cloud API, other server, etc.

**Cons:**
- ⚠️ **Requires code changes** — All 6 Gradio apps need modification
- ⚠️ **Need separate backend** — Must deploy backend elsewhere
- ⚠️ **More complex setup** — Two deployments to manage

---

## 📊 Comparison Table

| Feature | Multi-Service (Option 1) | Single Container (Option 2) | Frontend-Only (Option 3) |
|---------|-------------------------|----------------------------|--------------------------|
| **Works immediately** | ✅ Yes | ✅ Yes | ⚠️ Needs modifications |
| **Code changes required** | ✅ None | ✅ None | ❌ Must modify 6 files |
| **Production ready** | ✅ Yes | ⚠️ Not ideal | ⚠️ Need external backend |
| **Easy to scale** | ✅ Yes | ❌ No | ✅ Yes (frontend only) |
| **Setup complexity** | 🟢 Simple | 🟢 Simple | 🟡 Moderate |
| **Image size** | 902 MB | 902 MB | ~600 MB |
| **Recommended for** | **Production** | Development | Microservices setup |

---

## 🎯 Recommendation

### For Your Use Case: **Option 1 (Multi-Service)** ✅

**Why:**
1. ✅ **Already built and tested** — Working right now
2. ✅ **No code changes** — Works with existing code
3. ✅ **Production-ready** — Security, health checks, restarts
4. ✅ **Easy to use** — `./start-docker.sh start`
5. ✅ **Complete documentation** — README-DOCKER.md, QUICKSTART.md

**How to use:**
```bash
# Start everything:
./start-docker.sh start

# Test:
./start-docker.sh test

# View logs:
./start-docker.sh logs

# Stop:
./start-docker.sh stop
```

---

## 🔧 If You Still Want Single Container

Use the file I created: `Dockerfile.gradio-single`

```bash
# Build
docker build -f Dockerfile.gradio-single -t fuel-mcp:single .

# Run
docker run -d \
  -p 7860:7860 \
  -p 8000:8000 \
  -v $(pwd)/fuel_mcp/data:/app/fuel_mcp/data \
  -v $(pwd)/logs:/app/logs \
  --name fuel-mcp \
  fuel-mcp:single

# Access
open http://localhost:7860
```

---

## ⚠️ Why Your Simplified Version Won't Work

```dockerfile
# Your version:
CMD ["python", "-m", "fuel_mcp.gui_astm.app_astm_unified"]
```

**What happens when it starts:**

1. ✅ Gradio starts on port 7860
2. 🌐 You open http://localhost:7860
3. 📝 You enter API=30, Temp=60
4. 🔘 You click "Compute"
5. ❌ **CRASH** — Connection refused to http://127.0.0.1:8000

**Error you'll see:**
```python
requests.exceptions.ConnectionError: 
  HTTPConnectionPool(host='127.0.0.1', port=8000): 
  Max retries exceeded with url: /vcf?rho15=875.7&tempC=32.2
  Caused by NewConnectionError: Failed to establish a new connection: 
  [Errno 61] Connection refused
```

**Why:** There's no backend API running in the container!

---

## 📝 Summary

| Your Goal | Best Option | Action |
|-----------|-------------|--------|
| **Production deployment** | Option 1: Multi-Service | Use existing setup ✅ |
| **Quick single container** | Option 2: Single Container | Use `Dockerfile.gradio-single` |
| **Microservices architecture** | Option 3: Frontend-Only | Modify code first |
| **Your simplified Dockerfile** | ❌ Won't work | Choose Option 1 or 2 |

---

## 🚀 Quick Decision Guide

**Choose Option 1 if:**
- ✅ You want it to work immediately
- ✅ You want production-ready deployment
- ✅ You're okay with Docker Compose

**Choose Option 2 if:**
- ✅ You need a single container
- ✅ You're okay with running both services together
- ✅ You don't need to scale independently

**Choose Option 3 if:**
- ✅ You have a separate backend already running
- ✅ You're willing to modify the code
- ✅ You want maximum flexibility

---

**My recommendation: Stick with Option 1 (what I built) — it's production-ready and works perfectly!** 🎉


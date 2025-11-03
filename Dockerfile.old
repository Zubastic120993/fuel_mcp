# 🧩 Fuel MCP — Lightweight Dockerfile v1.1.0-light
FROM python:3.12-slim

# =====================================================
# 🔧 Environment Configuration
# =====================================================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    MODE=OFFLINE

# Set workdir
WORKDIR /app

# =====================================================
# 📦 System Dependencies (minimal build essentials)
# =====================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# =====================================================
# 🧩 Dependency Installation
# =====================================================
# Copy only requirements first to leverage Docker caching
COPY requirements.txt ./

RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# =====================================================
# 📁 Application Code
# =====================================================
COPY . .

# Create non-root user
RUN useradd --create-home --uid 10001 appuser \
 && chown -R appuser:appuser /app
USER appuser

# =====================================================
# 🌐 Networking
# =====================================================
EXPOSE 8000

# =====================================================
# ✅ Optional Healthcheck (disabled here; handled in compose)
# =====================================================
# HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=5 \
#   CMD python - <<'PY'\nimport urllib.request,sys; \
#   sys.exit(0 if urllib.request.urlopen('http://localhost:8000/status',timeout=5).status==200 else 1)\nPY

# =====================================================
# 🚀 Default Startup Command
# =====================================================
CMD ["uvicorn", "fuel_mcp.api.mcp_api:app", "--host", "0.0.0.0", "--port", "8000"]

# 🧭 Fuel MCP — Git Roadmap

| Step | Phase | Branch Name | Focus | Expected Outcome |
|------|--------|--------------|--------|------------------|
| ✅ **1. Core Engine (Stable)** | `main` | Unified schema, CLI, regex parser, density loader | ✅ All tests passed *(v1.0.3-final)* |
| ✅ **2. Dockerization Phase** | `feature/docker-v1.1.0` | Created Dockerfile + Compose setup for MCP API with healthchecks and persistent volumes | 🐳 Fully operational portable API container |
| 🔹 **3. GUI Phase (Local App)** | `feature/gui-v1.1.1` | Develop Flask or Gradio-based front-end for interacting with `/query`, `/vcf`, and `/auto_correct` endpoints | 🧠 Interactive and user-friendly local interface |
| 🔹 **4. Agent Integration Phase** | `feature/agent-v1.2.0` | Integrate Flowise / LangChain for intelligent conversational MCP agent | 🤖 Autonomous AI assistant capable of contextual reasoning |
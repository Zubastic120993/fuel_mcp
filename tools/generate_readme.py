"""
tools/generate_readme.py
========================

Auto-generates a unified README.md for the Fuel MCP project.
Includes branch overview, phase roadmap, and usage examples.
"""

from datetime import datetime, UTC
from pathlib import Path


def generate_readme():
    # Use timezone-aware UTC timestamp
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

    readme = f"""# 🧩 Fuel MCP — Marine Fuel Correction Processor


**Maintainer:** Chief Engineer *Volodymyr Zub*  
**Last Updated:** {timestamp}  
**Status:** Stable core engine (v1.0.3-final) - Dockerized & Ready for GUI

---

## Project Overview

Fuel MCP is an intelligent marine fuel correction and conversion processor.  
It combines ISO 91-1 / ASTM D1250 Volume Correction Factor (VCF) calculations,  
dynamic density loading, and natural-language parsing for efficient use in  
shipboard or automated environments.

Core features:
- Unified API with `/query`, `/vcf`, `/auto_correct`
- Regex-based NLP parser ("convert 500L diesel @ 30C")
- Dynamic density loading from JSON
- CLI toolkit (`mcp status`, `mcp test`, `mcp verify`, `mcp db-purge`)
- SQLite-based query history and error logging
- Dockerized deployment with persistent logs and database

---

## Development Roadmap

| Step | Phase | Branch Name | Focus | Expected Outcome |
|------|--------|--------------|--------|------------------|
| 1 | Core Engine (Stable) | `main` | Unified schema, CLI, regex parser, density loader | All tests passed (v1.0.3-final) |
| 2 | Dockerization Phase | `feature/docker-v1.1.0` | Create Dockerfile + Compose setup for MCP API | Portable containerized API |
| 3 | GUI Phase (Local App) | `feature/gui-v1.1.1` | Build Flask/Gradio front-end for local use | Interactive interface |
| 4 | Agent Integration Phase | `feature/agent-v1.2.0` | Flowise / LangChain AI agent integration | Conversational AI MCP Assistant |

---

## Current Branches

- **`main`** - Stable production engine (v1.0.3-final)
- **`feature/docker-v1.1.0`** - Containerization (Docker + Compose)
- **`feature/gui-v1.1.1`** - Flask/Gradio GUI front-end
- **`feature/agent-v1.2.0`** - Flowise / LangChain AI integration

Legacy support branches:
- `feature/core-polish-v1.0.3`
- `feature/schema-unification-v1.0.3`
- `feature/regex-parser-v1.0.3`
- `feature/cli-tools-v1.0.3`
- `legacy/local-mcp` (archived pre-v1.0 engine)

---

## Quick Start - Docker

```bash
# Build image
docker build -t fuel_mcp:1.1.0-light .

# Run container
docker run -d -p 8000:8000 --name fuel_mcp_api fuel_mcp:1.1.0-light

# Test endpoints
curl http://127.0.0.1:8000/status
curl "http://127.0.0.1:8000/query?text=convert%20500L%20diesel%20@%2030C"
```

---

## CLI Tools

```bash
# Check engine and database
mcp status

# Run internal test suite
mcp test

# Recalculate stored records
mcp verify

# Purge old logs and DB records
mcp db-purge
```

---

## API Endpoints

### `/status`
Returns engine status and version info.

### `/query?text=<natural_language>`
Parse and process natural language fuel queries.

Example:
```bash
curl "http://127.0.0.1:8000/query?text=convert%20500L%20diesel%20@%2030C"
```

### `/vcf`
Calculate Volume Correction Factor (VCF) based on ASTM D1250.

Parameters:
- `density_15` - Density at 15C (kg/m3)
- `temp_obs` - Observed temperature (C)
- `volume_obs` - Observed volume (L or m3)

Example:
```bash
curl "http://127.0.0.1:8000/vcf?density_15=835&temp_obs=30&volume_obs=1000"
```

### `/auto_correct`
Automatically correct volume to 15C reference.

Parameters:
- `fuel_type` - Fuel type (e.g., diesel, jet_a, gasoline)
- `volume_obs` - Observed volume
- `temp_obs` - Observed temperature (C)

---

## ASTM D1250 / ISO 91-1 Implementation

Fuel MCP implements the official ASTM D1250 / API MPMS Chapter 11.1 standard for volume correction factors (VCF/CTL).

### Calculation Steps

1. **Identify Product Type (PT)**
   - Most transport fuels use PT 5 (generalized crude oils and refined products)
   - Lubricating oils use PT 6

2. **Select Correct VCF Table**
   - Table 54A: density < 790 kg/m3 (light products, gasoline)
   - Table 54B: 790-900 kg/m3 (kerosene, jet fuel, diesel)
   - Table 54D: > 900 kg/m3 (heavy fuel oils)

3. **Apply Volume Correction**
   ```
   V15 = V_obs × VCF(T_obs, density15)
   ```

4. **Calculate Mass**
   ```
   m = density15 × V15
   ```

### Supported Fuel Types

| Fuel Type | Typical Density (kg/m3) | VCF Table | Expansion Coeff |
|-----------|-------------------------|-----------|-----------------|
| Gasoline | 720-760 | 54A | ~0.00100/C |
| Jet A / Kerosene | 780-820 | 54B | ~0.00095/C |
| Diesel | 820-860 | 54B | ~0.00085/C |
| Heavy Fuel Oil | 930-990 | 54D | ~0.00070/C |

---

## License

(c) 2025 Volodymyr Zub.  
Released under the MIT License.
"""

    # Write the README to project root
    Path("README.md").write_text(readme, encoding="utf-8")
    print("README.md successfully generated at project root.")


if __name__ == "__main__":
    generate_readme()

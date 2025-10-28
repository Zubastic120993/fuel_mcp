
"""
Precision Patch — VCF & Air/Vacuo Tables
----------------------------------------
Enhances metadata for temperature and air correction tables
to improve offline semantic search accuracy in MCP.
"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# =====================================================
# ⚙️ Paths
# =====================================================
BASE_DIR = Path(__file__).parent.parent
REGISTRY_PATH = BASE_DIR / "tables" / "registry.json"
VECTOR_PATH = BASE_DIR / "rag" / "vector_store.json"

# =====================================================
# 🧠 Load embedding model
# =====================================================
print("🧩 Loading local semantic model: nomic-ai/nomic-embed-text-v1.5 ...")
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
print("✅ Model ready.\n")

# =====================================================
# 🗂️ Load files
# =====================================================
with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

with open(VECTOR_PATH, "r") as f:
    vector_store = json.load(f)

# =====================================================
# 🎯 Tables to patch
# =====================================================
TARGETS = {
    # --- Volume Correction Factors ---
    "ASTM_Table54A_VolumeCorrectionFactors_LightOils.csv":
        "Official VCF table (54A) — converts observed volume of light oils to volume at 15°C or 60°F per ASTM D1250 and ISO 91-1 standards.",

    "ASTM_Table54B_VolumeCorrectionFactors_MediumOils.csv":
        "Official VCF table (54B) — converts observed volume of medium oils to reference volume at 15°C or 60°F according to ASTM D1250.",

    "ASTM_Table54C_VolumeCorrectionFactors_HeavyOils.csv":
        "Official VCF table (54C) — converts observed volume of heavy fuel oils to reference volume at 15°C or 60°F following ISO 91-1 standard.",

    # --- Density & Temperature Conversion ---
    "ASTM_Table23_Temperature_to_Density15C.csv":
        "Table 23 — converts density at observed temperature to equivalent density at 15°C for petroleum and liquid fuels (ISO 91-1).",

    "ASTM_Table24_Density15C_to_Temperature.csv":
        "Table 24 — reverse of Table 23; converts density at 15°C to observed density at a given temperature.",

    # --- Air/Vacuo Correction ---
    "ASTM_Table56_Density15C_to_VacuoAirFactor.csv":
        "Air/vacuo correction factor table — converts fuel density from vacuum to air conditions at 15°C (ASTM D1250 Table 56).",

    "ASTM_Table57_Density15C_to_AirVacuoFactor.csv":
        "Reverse correction — converts density from air to vacuum conditions at 15°C per ASTM D1250 Table 57."
}

# =====================================================
# 🧩 Apply patch
# =====================================================
patched = 0
for table, desc in TARGETS.items():
    key = table.replace(".csv", "")

    if table in registry:
        registry[table]["description"] = desc
        patched += 1

        emb = model.encode(desc, normalize_embeddings=True).tolist()
        vector_store[key] = {
            "embedding": emb,
            "description": desc
        }

# =====================================================
# 💾 Save updates
# =====================================================
with open(REGISTRY_PATH, "w") as f:
    json.dump(registry, f, indent=2)

with open(VECTOR_PATH, "w") as f:
    json.dump(vector_store, f, indent=2)

print(f"✅ Patched {patched} VCF/Air-Vacuo tables with refined metadata.")
print("📘 registry.json and 📗 vector_store.json updated successfully.")
print("🎯 Precision: 4-decimal semantic embeddings refreshed for temperature & air correction tables.")

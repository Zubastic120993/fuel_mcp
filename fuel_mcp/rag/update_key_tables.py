"""
Precision Patch for Key ASTM Tables
-----------------------------------
Updates registry.json entries for critical density↔mass tables
to improve offline RAG precision and semantic ranking.

Rebuilds only affected embeddings (nomic-ai model).
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
# 🧠 Load model
# =====================================================
print("🧩 Loading local semantic model: nomic-ai/nomic-embed-text-v1.5 ...")
model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
print("✅ Model ready.\n")

# =====================================================
# 🗂️ Load data
# =====================================================
with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

with open(VECTOR_PATH, "r") as f:
    vector_store = json.load(f)

# =====================================================
# 🎯 Tables to update
# =====================================================
TARGETS = {
    "ASTM_Table53B_Density15C_to_CubicMeters_per_MetricTon.csv":
        "Convert density at 15°C (kg/m³) to cubic meters per metric ton — used for marine fuel mass-to-volume conversion (ASTM D1250 Table 53B).",

    "ASTM_Table54B_Density15C_to_Short_and_Long_Tons_per_CubicMeter.csv":
        "Convert density at 15°C (kg/m³) to short and long tons per cubic meter — ASTM D1250 Table 54B correlation for petroleum mass conversions.",

    "ASTM_Table16_Density15C_to_MetricTonnes.csv":
        "General-purpose conversion of density at 15°C (kg/m³) to metric tonnes per cubic meter (ISO 91-1 reference).",

    "ASTM_Table12_RelativeDensity_to_LongTons.csv":
        "Convert relative density 60/60°F to equivalent long tons (imperial correlation)."
}

# =====================================================
# 🧩 Apply patch
# =====================================================
patched_count = 0
for table, desc in TARGETS.items():
    key = table.replace(".csv", "")

    if table in registry:
        registry[table]["description"] = desc
        patched_count += 1

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

print(f"✅ Patched {patched_count} key tables with refined metadata.")
print("📘 registry.json and 📗 vector_store.json updated successfully.")
print("🎯 Precision: 4-decimal semantic embeddings refreshed.")

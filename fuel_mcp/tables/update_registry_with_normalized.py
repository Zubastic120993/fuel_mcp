# fuel_mcp/tables/update_registry_with_normalized.py
import json
from pathlib import Path

# Auto-locate project base even if script is run from nested folder
BASE_DIR = Path(__file__).resolve().parents[1]
TABLES_DIR = BASE_DIR / "tables"
OFFICIAL_DIR = TABLES_DIR / "official"
NORM_DIR = OFFICIAL_DIR / "normalized"
REGISTRY_PATH = TABLES_DIR / "registry.json"

def update_registry():
    if not REGISTRY_PATH.exists():
        print(f"❌ Registry not found: {REGISTRY_PATH}")
        return

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    updated_count = 0
    for table_name, info in registry.items():
        norm_file = NORM_DIR / f"{Path(table_name).stem}_norm.csv"
        if norm_file.exists():
            info["normalized_path"] = str(norm_file.relative_to(TABLES_DIR))
            updated_count += 1
        else:
            info["normalized_path"] = None

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated registry.json — {updated_count} tables now linked to normalized files.")
    print(f"📄 Saved to {REGISTRY_PATH}")

if __name__ == "__main__":
    update_registry()

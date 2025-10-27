
"""
manage_registry.py
==================
Unified tool for managing ASTM/ISO table metadata in fuel_mcp.

Usage:
    python fuel_mcp/tables/manage_registry.py --rebuild
    python fuel_mcp/tables/manage_registry.py --enrich
    python fuel_mcp/tables/manage_registry.py --summary
    python fuel_mcp/tables/manage_registry.py --all
"""

import json, os, glob, argparse
from pathlib import Path
import pandas as pd

BASE = Path("fuel_mcp/tables/official")
REGFILE = Path("fuel_mcp/tables/registry.json")
SUMMARY = Path("fuel_mcp/tables/registry_summary.md")


# ======================================================
# 🏗️ BUILD — scan official/ and create basic registry
# ======================================================
def build_registry():
    registry = {}
    for path in sorted(BASE.glob("*.csv")):
        name = os.path.basename(path)
        entry = {
            "purpose": "Table metadata placeholder — to be completed later.",
            "primary_column": "",
            "outputs": [],
            "ASTM_reference": "",
            "ISO_equivalent": "",
            "category": "",
            "conversion_path": "",
            "notes": "",
        }
        registry[name] = entry
    with open(REGFILE, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"✅ Registry built with {len(registry)} entries → {REGFILE}")


# ======================================================
# 🧠 ENRICH — fill known metadata mappings
# ======================================================
def enrich_registry():
    if not REGFILE.exists():
        print("⚠️ Registry not found — run with --rebuild first.")
        return

    with open(REGFILE) as f:
        registry = json.load(f)

    for name, entry in registry.items():
        if "54B" in name:
            entry.update({
                "purpose": "Density 15 °C–based conversion",
                "primary_column": "Density_15C_kg_per_m3",
                "outputs": ["Short_Tons_per_CubicMeter", "Long_Tons_per_CubicMeter"],
                "ASTM_reference": "ASTM D1250-80 Vol XI Table 54B",
                "ISO_equivalent": "ISO 91-1 Table 54B",
                "category": "density ↔ mass",
                "conversion_path": "ρ15 → tons/m³ → mass",
                "notes": "Used in bunker calculations; basis for VCF correction in Table 54D.",
            })
        elif "53B" in name:
            entry.update({
                "purpose": "Density 15 °C–based conversion",
                "primary_column": "Density_15C_kg_per_m3",
                "outputs": ["Cubic_Meters_per_Tonne"],
                "ASTM_reference": "ASTM D1250-80 Vol XI Table 53B",
                "ISO_equivalent": "ISO 91-1 Table 53B",
                "category": "density ↔ volume",
                "conversion_path": "ρ15 → m³/t → volume",
                "notes": "Common for cargo tank calculations and bunker reports.",
            })
        elif "56" in name or "57" in name:
            entry.update({
                "purpose": "Air/vacuo correction based on density 15 °C.",
                "primary_column": "Density_15C_kg_per_L",
                "outputs": ["Correction_Factor"],
                "ASTM_reference": f"ASTM D1250-80 Vol XI Table {name[10:12]}",
                "ISO_equivalent": f"ISO 91-1 Table {name[10:12]}",
                "category": "air correction",
                "conversion_path": "ρ15 → factor air↔vacuo",
                "notes": "Used when converting observed density to/from vacuo basis.",
            })
    with open(REGFILE, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"✅ Registry enriched with {len(registry)} entries → {REGFILE}")


# ======================================================
# 📊 SUMMARY — Markdown summary
# ======================================================
def summary_registry():
    if not REGFILE.exists():
        print("⚠️ Registry not found — run with --rebuild first.")
        return

    with open(REGFILE) as f:
        registry = json.load(f)

    rows = []
    for name, data in registry.items():
        rows.append({
            "Table Name": name,
            "Category": data.get("category", ""),
            "Primary Column": data.get("primary_column", ""),
            "Outputs": ", ".join(data.get("outputs", [])),
            "ASTM Ref": data.get("ASTM_reference", ""),
            "ISO Eq": data.get("ISO_equivalent", ""),
            "Purpose": data.get("purpose", ""),
        })

    df = pd.DataFrame(rows)
    df.sort_values(by=["Category", "Table Name"], inplace=True)
    md = "# 🧮 ASTM / ISO Table Registry Summary\n\n"
    md += df.to_markdown(index=False)
    SUMMARY.write_text(md)
    print(f"✅ Markdown summary created → {SUMMARY}")


# ======================================================
# 🎛️ MAIN — argument handler
# ======================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage ASTM/ISO table registry")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild registry from CSV files")
    parser.add_argument("--enrich", action="store_true", help="Enrich registry with known metadata")
    parser.add_argument("--summary", action="store_true", help="Generate Markdown summary")
    parser.add_argument("--all", action="store_true", help="Run all tasks sequentially")
    args = parser.parse_args()

    if args.all:
        build_registry()
        enrich_registry()
        summary_registry()
    else:
        if args.rebuild:
            build_registry()
        if args.enrich:
            enrich_registry()
        if args.summary:
            summary_registry()

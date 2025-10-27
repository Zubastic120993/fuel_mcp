#!/usr/bin/env python3
import json
from pathlib import Path
import re

REGISTRY = Path(__file__).resolve().parent / "registry.json"
OUTFILE = Path(__file__).resolve().parent / "registry_enriched_auto.json"

def infer_category(name):
    name_lower = name.lower()
    if "air" in name_lower or "vacuo" in name_lower:
        return "air correction"
    elif "api" in name_lower:
        return "API correlation"
    elif "density15" in name_lower:
        return "density correlation"
    elif "relativedensity" in name_lower:
        return "relative density correlation"
    else:
        return "miscellaneous"

def infer_purpose(name):
    if "api" in name.lower() and "ton" in name.lower():
        return "Convert API gravity at 60°F to corresponding tons per volume unit."
    elif "api" in name.lower() and "liter" in name.lower():
        return "Convert API gravity at 60°F to liters or cubic meters."
    elif "density15" in name.lower():
        return "Convert density at 15 °C to equivalent mass or volume."
    elif "relativedensity" in name.lower():
        return "Convert relative density 60/60°F to related volumetric or mass properties."
    elif "vacuo" in name.lower() or "air" in name.lower():
        return "Air/vacuo correction based on density or relative density."
    return "Table metadata placeholder — to be completed later."

def infer_reference(name):
    """Infer ASTM/ISO references when possible"""
    matches = re.findall(r"(\d+[A-Z]?)", name)
    if matches:
        table_number = matches[0]
        return {
            "ASTM_reference": f"ASTM D1250-80 Vol XI Table {table_number}",
            "ISO_equivalent": f"ISO 91-1 Table {table_number}",
        }
    return {"ASTM_reference": "", "ISO_equivalent": ""}

def main():
    with open(REGISTRY, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for fname, entry in data.items():
        if "placeholder" in entry.get("purpose", ""):
            cat = infer_category(fname)
            purp = infer_purpose(fname)
            refs = infer_reference(fname)
            entry.update({
                "category": cat,
                "purpose": purp,
                "ASTM_reference": refs["ASTM_reference"],
                "ISO_equivalent": refs["ISO_equivalent"],
                "conversion_path": entry.get("conversion_path", "")
            })
            updated += 1

    with open(OUTFILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Auto-enriched {updated} tables → {OUTFILE.name}")

if __name__ == "__main__":
    main()

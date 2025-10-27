
# fuel_mcp/rag/build_metadata.py
from pathlib import Path
import json
import re

REGISTRY_PATH = Path(__file__).parents[1] / "tables" / "registry.json"
SUMMARY_PATH = Path(__file__).parents[1] / "tables" / "registry_summary.md"
VCF_PATH = Path(__file__).parents[1] / "core" / "vcf_official_full.py"
OUTPUT_PATH = Path(__file__).parent / "metadata.json"

def extract_from_registry():
    data = json.loads(REGISTRY_PATH.read_text())
    meta = {}
    for name, entry in data.items():
        key = name.replace(".csv", "")
        meta[key] = {
            "category": entry.get("category", "unknown"),
            "inputs": [entry.get("primary_column")] if entry.get("primary_column") else [],
            "outputs": entry.get("outputs", []),
            "astm_ref": entry.get("ASTM_reference"),
            "iso_ref": entry.get("ISO_equivalent"),
            "summary": entry.get("purpose", ""),
            "source": "registry.json"
        }
    return meta

def extract_from_summary():
    text = SUMMARY_PATH.read_text()
    table_lines = re.findall(r"`(ASTM_[^`]+\.csv)`.*?\|\s*`([^`]*)`\s*\|\s*(.*?)\|", text)
    meta = {}
    for name, primary, outputs in table_lines:
        key = name.replace(".csv", "")
        meta[key] = {
            "primary_column": primary.strip(),
            "outputs_text": outputs.strip(),
            "source": "registry_summary.md"
        }
    return meta

def extract_vcf_doc():
    code = VCF_PATH.read_text()
    doc = re.search(r'"""(.*?)"""', code, re.S)
    return {
        "VCF_official_equations": {
            "category": "Analytical Equations",
            "summary": doc.group(1).strip() if doc else "VCF official formulae",
            "inputs": ["ρ15", "ΔT"],
            "outputs": ["VCF"],
            "source": "vcf_official_full.py"
        }
    }

def build_metadata():
    combined = extract_from_registry()
    for k, v in extract_from_summary().items():
        combined.setdefault(k, {}).update(v)
    combined.update(extract_vcf_doc())
    OUTPUT_PATH.write_text(json.dumps(combined, indent=2))
    print(f"✅ Built metadata for {len(combined)} items → {OUTPUT_PATH}")

if __name__ == "__main__":
    build_metadata()

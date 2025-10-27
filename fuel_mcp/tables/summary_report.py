"""
summary_report.py
=================
Generates a clean, categorized Markdown summary of all ASTM/ISO registry tables.
"""

import json
from pathlib import Path
import pandas as pd

REGFILE = Path("fuel_mcp/tables/registry.json")
OUTFILE = Path("fuel_mcp/tables/registry_summary.md")

# Load registry
with open(REGFILE) as f:
    registry = json.load(f)

# Categorize
categories = {}
for name, data in registry.items():
    cat = data.get("category", "Uncategorized") or "Uncategorized"
    categories.setdefault(cat, []).append((name, data))

# Markdown header
md = """# 🧮 ASTM / ISO Conversion Table Registry Summary

This registry summarizes all available ASTM D1250 / ISO 91-1 correlation tables used for
density, volume, and mass correction within **fuel_mcp**.

Each group below shows the relevant tables, reference links, and purpose notes.

---

"""

# Build sections
for cat, items in sorted(categories.items()):
    md += f"## 🗂️ {cat.upper()}\n\n"
    md += "| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |\n"
    md += "|:------|:----------------|:---------|:----------|:--------|:---------|\n"
    for name, d in sorted(items):
        outputs = ", ".join(d.get("outputs", []))
        md += (
            f"| `{name}` | `{d.get('primary_column', '')}` | {outputs or '-'} | "
            f"{d.get('ASTM_reference', '') or '-'} | {d.get('ISO_equivalent', '') or '-'} | "
            f"{d.get('purpose', '') or '-'} |\n"
        )
    md += "\n---\n\n"

# Save file
OUTFILE.write_text(md)

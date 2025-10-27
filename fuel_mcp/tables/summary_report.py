# fuel_mcp/tables/summary_report.py
import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
REGISTRY_FILE = BASE_DIR / "registry.json"
OUTPUT_FILE = BASE_DIR / "registry_summary.md"

def make_section(title: str, items: list[tuple[str, dict]]) -> str:
    """Generate Markdown table for a specific category."""
    if not items:
        return ""
    lines = [
        f"\n## 🗂️ {title}\n",
        "| Table | Primary Column | Outputs | ASTM Ref | ISO Eq | Purpose |",
        "|:------|:----------------|:---------|:----------|:--------|:---------|",
    ]
    for name, info in sorted(items):
        outputs = ", ".join(info.get("outputs", [])) or "-"
        lines.append(
            f"| `{name}` | `{info.get('primary_column', '') or '-'}` | {outputs} | "
            f"{info.get('ASTM_reference', '-') or '-'} | {info.get('ISO_equivalent', '-') or '-'} | "
            f"{info.get('purpose', '-') or '-'} |"
        )
    return "\n".join(lines)

def build_summary():
    if not REGISTRY_FILE.exists():
        print(f"❌ Registry not found: {REGISTRY_FILE}")
        return

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Group tables by category
    groups = {}
    for name, info in registry.items():
        cat = info.get("category", "Uncategorized").strip().upper()
        groups.setdefault(cat, []).append((name, info))

    md = [
        "# 🧮 ASTM / ISO Conversion Table Registry Summary",
        "",
        "This registry summarizes all available ASTM D1250 / ISO 91-1 correlation tables used for",
        "density, volume, and mass correction within **fuel_mcp**.",
        "",
        "Each group below shows the relevant tables, reference links, and purpose notes.",
        "\n---",
    ]

    # Maintain logical section order
    order = [
        "UNCATEGORIZED",
        "AIR CORRECTION",
        "DENSITY ↔ MASS",
        "DENSITY ↔ VOLUME",
        "API CORRELATION",
        "RELATIVE DENSITY CORRELATION",
        "DENSITY ↔ API",
    ]

    for section in order:
        if section in groups:
            md.append(make_section(section, groups[section]))

    # Catch any leftovers not in order
    remaining = [k for k in groups if k not in order]
    for section in remaining:
        md.append(make_section(section, groups[section]))

    # Save
    Path(OUTPUT_FILE).write_text("\n".join(md), encoding="utf-8")
    print(f"✅ Markdown summary created → {OUTPUT_FILE}")

if __name__ == "__main__":
    build_summary()

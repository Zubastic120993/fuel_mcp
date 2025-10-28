
"""
verify_constants.py
===================
Quick validation tool to confirm that VCF coefficients (K0, K1, A, B)
defined in vcf_official_full.py match ISO 91-1 :2019 / ASTM D1250 Annex B.

Usage:
    python fuel_mcp/tests/verify_constants.py
"""

import importlib
import math

# Import the live table from your core module
vcf_module = importlib.import_module("fuel_mcp.core.vcf_official_full")
VCF_TABLES = vcf_module.VCF_TABLES

# Reference Annex B constants (verified from ISO 91-1 :2019 E)
REFERENCE = {
    "54A": {"K0": 613.9723, "K1": 0.0},
    "54B": [
        {"label": "Transition band", "A": -0.00336312, "B": 2680.3206},
        {"label": "Jet / Kerosene", "K0": 594.5418, "K1": 0.0},
        {"label": "Residual / Marine fuels", "K0": 186.9696, "K1": 0.48618},
    ],
    "54D": {"K0": 0.0, "K1": 0.6278},
}

TOL = 1e-6
errors = 0

print("\n🔍  Verifying ISO 91-1 / ASTM D1250 coefficients...\n")

# --- Table 54A ---
for key in ("K0", "K1"):
    diff = abs(VCF_TABLES["54A"][key] - REFERENCE["54A"][key])
    if diff > TOL:
        print(f"❌  54A {key} mismatch: found {VCF_TABLES['54A'][key]}, expected {REFERENCE['54A'][key]}")
        errors += 1
    else:
        print(f"✅  54A {key} OK ({VCF_TABLES['54A'][key]})")

# --- Table 54B ---
for ref in REFERENCE["54B"]:
    label = ref["label"]
    found = next((s for s in VCF_TABLES["54B"] if s["label"] == label), None)
    if not found:
        print(f"❌  54B segment '{label}' missing!")
        errors += 1
        continue
    for k, v in ref.items():
        if k == "label":
            continue
        diff = abs(found[k] - v)
        if diff > TOL:
            print(f"❌  54B {label} {k} mismatch: found {found[k]}, expected {v}")
            errors += 1
        else:
            print(f"✅  54B {label} {k} OK ({found[k]})")

# --- Table 54D ---
for key in ("K0", "K1"):
    diff = abs(VCF_TABLES["54D"][key] - REFERENCE["54D"][key])
    if diff > TOL:
        print(f"❌  54D {key} mismatch: found {VCF_TABLES['54D'][key]}, expected {REFERENCE['54D'][key]}")
        errors += 1
    else:
        print(f"✅  54D {key} OK ({VCF_TABLES['54D'][key]})")

# --- Summary ---
print("\n" + "=" * 60)
if errors == 0:
    print("🎯  All constants match ISO 91-1 Annex B precisely!\n")
else:
    print(f"⚠️  {errors} mismatch(es) found — please review values.\n")

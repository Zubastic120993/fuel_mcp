
"""
unit_converter.py
=================
Standardized conversion factors from ASTM D1250-80 (Volume XI – Table 1)

All factors are for conversion **at the same temperature**.
Exact relationships are marked by (†) in the source table.
"""

UNIT_CONVERSION = {
    # ────────────────────────────────
    # 📏 LENGTH
    # ────────────────────────────────
    "metre_to_yard": 1.0936,
    "metre_to_foot": 3.2808,
    "metre_to_inch": 39.37,

    "yard_to_metre": 0.9144,   # († exact)
    "foot_to_metre": 0.3048,   # († exact)
    "inch_to_cm": 2.54,        # († exact)

    # ────────────────────────────────
    # ⚖️ WEIGHT
    # ────────────────────────────────
    "long_ton_to_lb": 2240.0,  # (†)
    "long_ton_to_short_ton": 1.12,  # (†)
    "long_ton_to_tonne": 1.01605,

    "short_ton_to_lb": 2000.0,  # (†)
    "short_ton_to_long_ton": 0.892857,
    "short_ton_to_tonne": 0.907185,

    "tonne_to_long_ton": 0.984206,
    "tonne_to_short_ton": 1.10231,

    "lb_to_kg": 0.453592,
    "kg_to_lb": 2.20462,

    # ────────────────────────────────
    # 🧴 VOLUME & CAPACITY
    # ────────────────────────────────
    "usg_to_cuin": 231.0,  # (†)
    "usg_to_cuft": 0.133681,
    "usg_to_imp_gal": 0.832674,
    "usg_to_barrel": 0.0238095,
    "usg_to_litre": 3.78541,

    "barrel_to_usg": 42.0,  # (†)
    "barrel_to_cuin": 9702.0,  # (†)
    "barrel_to_cuft": 5.61458,
    "barrel_to_imp_gal": 34.9723,
    "barrel_to_litre": 158.987,

    "imp_gal_to_cuin": 277.42,
    "imp_gal_to_cuft": 0.160544,
    "imp_gal_to_usg": 1.20095,
    "imp_gal_to_barrel": 0.0285941,
    "imp_gal_to_litre": 4.54596,

    "cuft_to_imp_gal": 6.22883,
    "cuft_to_usg": 7.48052,
    "cuft_to_barrel": 0.178108,
    "cuft_to_litre": 28.3169,
    "cuft_to_cum": 0.0283169,

    "cuin_to_imp_gal": 0.00360465,
    "cuin_to_usg": 0.004329,
    "cuin_to_litre": 0.0163871,

    "litre_to_cuin": 61.0238,
    "litre_to_cuft": 0.0353147,
    "litre_to_imp_gal": 0.219969,
    "litre_to_usg": 0.264172,
    "litre_to_barrel": 0.00628981,

    "cum_to_imp_gal": 219.969,
    "cum_to_usg": 264.172,
    "cum_to_barrel": 6.28981,
    "cum_to_cuft": 35.3147,
    "cum_to_litre": 1000.0,  # (†)
}


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert between compatible units using ASTM D1250-80 factors.
    Auto-reverse if only inverse factor is stored.
    """
    key = f"{from_unit}_to_{to_unit}"
    factor = UNIT_CONVERSION.get(key)

    if factor is not None:
        return value * factor

    # try reverse lookup
    rev_key = f"{to_unit}_to_{from_unit}"
    rev_factor = UNIT_CONVERSION.get(rev_key)
    if rev_factor is not None:
        return value / rev_factor

    raise ValueError(f"No conversion factor for '{from_unit}' ↔ '{to_unit}'")


if __name__ == "__main__":
    # simple demo
    print(f"1 barrel = {convert(1, 'barrel', 'litre')} L")
    print(f"1 m³ = {convert(1, 'cum', 'usg')} US gallons")
    print(f"1 litre = {convert(1, 'litre', 'barrel')} barrel")

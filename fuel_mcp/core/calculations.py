
from typing import Literal, Optional
from dataclasses import dataclass

# Minimal interfaces — replace internals with your actual table logic as you have it.
# Keep signatures stable for the API layer.

FuelType = Literal["diesel", "hfo", "lpg", "lng", "methanol", "mdo", "ulo"]

@dataclass
class ConvertResult:
    value: float
    from_unit: str
    to_unit: str

def compute_vcf(
    fuel: FuelType,
    t_c: float,
    rho_15: Optional[float] = None,
) -> float:
    """
    Return VCF (Volume Correction Factor) for given fuel at temperature t_c.
    If your project already has ASTM/ISO implementation, call it here.
    """
    # Placeholder: swap with your real ASTM/ISO 91-1 calc
    # Example simple linear approx (DO NOT use in production):
    # real VCF often ~ 0.00064/°C for middle distillates relative to 15°C baseline.
    k = 0.00064
    delta = (t_c - 15.0)
    vcf = 1.0 / (1.0 + k * delta)
    return round(vcf, 6)

def convert_units(value: float, from_unit: str, to_unit: str) -> ConvertResult:
    """
    Unit converter wrapper. If you already have unit_converter.py, import & call it.
    """
    # Basic examples — replace with your real library (pint, your unit_converter.py, etc.)
    if from_unit == "m3/h" and to_unit in ("t/day", "ton/day"):
      # Dummy density (850 kg/m3) and hours/day → 24.
      # Replace with your fuel-aware mass flow logic if needed.
      kg_per_m3 = 850.0
      t_per_m3 = kg_per_m3 / 1000.0
      val = value * 24.0 * t_per_m3
      return ConvertResult(value=round(val, 6), from_unit=from_unit, to_unit=to_unit)

    if from_unit == "C" and to_unit == "K":
      return ConvertResult(value=value + 273.15, from_unit=from_unit, to_unit=to_unit)

    # Add more real mappings or delegate to your existing converter here
    raise ValueError(f"Unsupported conversion: {from_unit} → {to_unit}")

def convert_mass_volume(
    amount: float,
    from_unit: str,
    to_unit: str,
    fuel: Optional[FuelType] = None,
    rho_15: Optional[float] = None,
    t_c: Optional[float] = None,
) -> ConvertResult:
    """
    Mass-volume conversions with temperature correction if t_c provided.
    Use your ASTM tables for VCF and proper density correction chain.
    """
    # Example: m3 @ T → t/day via VCF and density@15C.
    if from_unit == "m3/h" and to_unit in ("t/day", "ton/day"):
        if rho_15 is None:
            rho_15 = 850.0  # fallback; replace by fuel DB if available
        vcf = compute_vcf(fuel or "diesel", t_c or 15.0, rho_15=rho_15)
        rho_T = rho_15 / vcf  # simplistic; wire to your real density correction
        t_per_m3 = (rho_T / 1000.0)
        val = amount * 24.0 * t_per_m3
        return ConvertResult(value=round(val, 6), from_unit=from_unit, to_unit=to_unit)

    # Fallback to unit converter
    return convert_units(amount, from_unit, to_unit)

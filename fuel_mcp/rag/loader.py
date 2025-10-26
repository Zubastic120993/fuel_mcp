
from pathlib import Path

def correct_volume(fuel: str, observed_m3: float, tempC: float,
                   db_path: str | None = None) -> dict:
    if db_path is None:
        db_path = Path(__file__).parent / "tables" / "fuel_data.json"
    with open(db_path) as f:
        fuels = json.load(f)
    rho15 = fuels[fuel]["density_15C"]
    result = vcf_iso_official(rho15, tempC)
    result["fuel"] = fuel
    result["observed_m3"] = observed_m3
    result["V15_m3"] = round(observed_m3 * result["VCF"], 3)
    return result

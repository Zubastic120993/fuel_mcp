
from pathlib import Path
import pandas as pd


def load_table(name: str) -> pd.DataFrame:
    """
    Load any ASTM/ISO table from `fuel_mcp/tables/official/`.

    Example:
        df = load_table("ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv")
    """
    base = Path(__file__).parent / "official"
    path = base / name

    if not path.exists():
        raise FileNotFoundError(f"Table not found: {path}")

    return pd.read_csv(path)


def list_tables() -> list[str]:
    """
    List all available tables in the official directory.
    """
    base = Path(__file__).parent / "official"
    return [p.name for p in base.glob("*.csv")]

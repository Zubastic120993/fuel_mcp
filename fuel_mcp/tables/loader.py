# fuel_mcp/tables/loader.py
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent
OFFICIAL_DIR = BASE_DIR / "official"
NORM_DIR = OFFICIAL_DIR / "normalized"

def load_table(name: str, normalized: bool = False) -> pd.DataFrame:
    """
    Load any ASTM/ISO table from `fuel_mcp/tables/official/`.

    Parameters
    ----------
    name : str
        Filename of the table (e.g. 'ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv')
    normalized : bool, optional
        If True, loads the normalized version from `official/normalized/`

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the table file does not exist.

    Example
    -------
        df = load_table("ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv")
        df_norm = load_table("ASTM_Table9_APIGravity60F_to_USGallons_and_Barrels_per_ShortTon_60F.csv", normalized=True)
    """
    directory = NORM_DIR if normalized else OFFICIAL_DIR
    path = directory / name

    if not path.exists():
        raise FileNotFoundError(f"❌ Table not found: {path}")

    try:
        df = pd.read_csv(path)
        print(f"✅ Loaded {'normalized' if normalized else 'official'} table: {path.name}")
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load {path.name}: {e}") from e


def list_tables(normalized: bool = False) -> list[str]:
    """
    List all available ASTM/ISO tables in either the official or normalized directory.
    """
    directory = NORM_DIR if normalized else OFFICIAL_DIR
    files = sorted([p.name for p in directory.glob("*.csv")])
    print(f"📋 Found {len(files)} {'normalized' if normalized else 'official'} tables.")
    return files


if __name__ == "__main__":
    # Quick test run
    print(list_tables())

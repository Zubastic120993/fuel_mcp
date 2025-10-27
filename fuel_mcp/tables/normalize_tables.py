# fuel_mcp/tables/normalize_tables.py
import pandas as pd
from pathlib import Path

OFFICIAL_DIR = Path(__file__).parent / "official"
OUTPUT_DIR = OFFICIAL_DIR / "normalized"
OUTPUT_DIR.mkdir(exist_ok=True)

def normalize_headers(headers):
    """Convert headers to lowercase snake_case and remove special symbols."""
    clean = []
    for h in headers:
        h = (
            h.strip()
            .lower()
            .replace(" ", "_")
            .replace("/", "_per_")
            .replace("°", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "_")
        )
        clean.append(h)
    return clean


def normalize_csv(file_path: Path):
    """Clean one CSV file and save normalized version."""
    try:
        # Read with UTF-8 to avoid encoding issues
        df = pd.read_csv(file_path, encoding="utf-8")

        # Normalize headers
        df.columns = normalize_headers(df.columns)

        # Replace commas with dots and convert numeric where possible
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".").str.strip()

            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                # If not convertible, keep as string
                pass

        # Save normalized file
        output_file = OUTPUT_DIR / f"{file_path.stem}_norm.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Normalized: {file_path.name} → {output_file.name}")

    except Exception as e:
        print(f"❌ Failed to process {file_path.name}: {e}")


def main():
    files = sorted(OFFICIAL_DIR.glob("*.csv"))
    if not files:
        print("⚠️ No CSV files found in 'official/'")
        return

    for f in files:
        normalize_csv(f)

    print(f"\n✅ Normalized {len(files)} tables → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

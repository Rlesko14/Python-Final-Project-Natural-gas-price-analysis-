import pandas as pd
import requests
from io import StringIO
from pathlib import Path
import sys

def get_project_root():
    """
    Finds the project root by searching upwards for a 'marker' file.
    """
    try:
        current_path = Path(__file__).resolve()
    except NameError:
        current_path = Path.cwd().resolve()
        
    for parent in [current_path] + list(current_path.parents):
        if (parent / ".gitignore").exists() or (parent / "src").exists():
            return parent
    return current_path

PROJECT_ROOT = get_project_root()
RAW_DIR = PROJECT_ROOT / "data" / "raw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def download_eia_csv(table_id, filename):
    """Downloads CSV data from EIA and saves to data/raw."""
    url = f"https://www.eia.gov/totalenergy/data/browser/csv.php?tbl={table_id}"
    headers = {
        **HEADERS,
        "Referer": f"https://www.eia.gov/totalenergy/data/browser/index.php?tbl={table_id}",
        "Accept": "text/csv,*/*",
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / filename
        df.to_csv(out_path, index=False)
        print(f"✅ Successfully saved {table_id} to {out_path}")
        return True
    except Exception as e:
        print(f" Error downloading table {table_id}: {e}")
        return False

def download_henryhub_html(filename="henry_hub_weekly.csv"):
    """Scrapes Henry Hub HTML and saves to data/raw."""
    url = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        tables = pd.read_html(StringIO(resp.text))
        
        # Identify the correct table
        weekly = next((t for t in tables if any("Week Of" in str(c) for c in t.columns)), None)
        if weekly is None:
            raise ValueError("Henry Hub table not found in HTML.")

        weekly.columns = ["week_of", "mon", "tue", "wed", "thu", "fri"]
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        out_path = RAW_DIR / filename
        weekly.to_csv(out_path, index=False)
        print(f" Successfully saved Henry Hub to {out_path}")
        return True
    except Exception as e:
        print(f" Error scraping Henry Hub: {e}")
        return False

if __name__ == "__main__":
    download_henryhub_html()
    download_eia_csv("T01.11", "EIA_T01_11_HDD_by_CensusDivision.csv")

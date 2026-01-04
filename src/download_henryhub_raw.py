import pandas as pd
import requests
from io import StringIO
from pathlib import Path

URL = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
HEADERS = {"User-Agent": "Mozilla/5.0"}

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = RAW_DIR / "henry_hub_weekly.csv"


def download_henryhub_raw():
    resp = requests.get(URL, headers=HEADERS, timeout=60)
    resp.raise_for_status()

    tables = pd.read_html(StringIO(resp.text))

    weekly = None
    for t in tables:
        cols = [str(c) for c in t.columns]
        if any("Week Of" in c for c in cols):
            weekly = t.copy()
            break

    if weekly is None:
        raise ValueError("Henry Hub weekly table not found")

    weekly.columns = ["week_of", "mon", "tue", "wed", "thu", "fri"]

    # RAW = minimal handling only
    weekly.to_csv(OUT_FILE, index=False)
    print(f"Saved raw Henry Hub data → {OUT_FILE}")


if __name__ == "__main__":
    download_henryhub_raw()

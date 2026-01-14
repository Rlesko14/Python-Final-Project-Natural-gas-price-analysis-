"""
DESCRIPTION:
    This script automates the ingestion of raw energy data from the U.S. EIA.
    It scrapes the Henry Hub Weekly Spot Price history (HTML) and downloads
    csv fundamentals (HDD, CDD, Overview) directly from government servers.

KEY FEATURES:
    Robust HTML parsing that scans for table keywords ("Week Of") rather
      than assuming fixed row positions.
    Intelligent root directory detection for device-agnostic file paths.
    Automatic directory creation ensures the 'data/raw' folder always exists.
"""

import pandas as pd
import requests
from io import StringIO
from pathlib import Path

def get_project_root():
   
    try:
        current_path = Path(__file__).resolve()
    except NameError:
        current_path = Path.cwd().resolve()
    
    for parent in [current_path] + list(current_path.parents):
        if (parent / "src").exists():
            return parent
            
    return current_path.parent

PROJECT_ROOT = get_project_root()
RAW_DIR = PROJECT_ROOT / "data" / "raw"
HEADERS = {"User-Agent": "Mozilla/5.0"}

RAW_DIR.mkdir(parents=True, exist_ok=True)



def download_eia_csv(table_id, filename):
    
    url = f"https://www.eia.gov/totalenergy/data/browser/csv.php?tbl={table_id}"
    print(f"Downloading {table_id}...")
    
    headers = {
        **HEADERS,
        "Referer": f"https://www.eia.gov/totalenergy/data/browser/index.php?tbl={table_id}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        
        df = pd.read_csv(StringIO(response.text))
        
        out_path = RAW_DIR / filename
        df.to_csv(out_path, index=False)
        print(f"Saved: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading table {table_id}: {e}")
        return False

def download_henryhub_html(filename="henry_hub_weekly.csv"):
   
    url = "https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
    print("Scraping Henry Hub Weekly...")
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        
        tables = pd.read_html(StringIO(resp.text), header=None)
        
        target_table = None
        
        for t in tables:
            if "Week Of" in t.to_string():
                target_table = t
                break
        
        if target_table is None:
            raise ValueError("Could not find the 'Week Of' table in the HTML.")

    
        for i, row in target_table.iterrows():
            if str(row[0]).strip() == "Week Of":
                target_table.columns = row 
                target_table = target_table.iloc[i+1:] 
                break
        
        
        target_table = target_table.iloc[:, :6]
        target_table.columns = ["week_of", "mon", "tue", "wed", "thu", "fri"]
        
        out_path = RAW_DIR / filename
        target_table.to_csv(out_path, index=False)
        print(f"Saved: {filename}")
        return True
        
    except Exception as e:
        print(f"Error scraping Henry Hub: {e}")
        return False

if __name__ == "__main__":
    print(f"Saving data to: {RAW_DIR}\n")
    
    download_henryhub_html()
    download_eia_csv("T01.11", "EIA_T01_11_HDD_by_CensusDivision.csv")
    download_eia_csv("T01.12", "EIA_T01_12_CDD_by_CensusDivision.csv")
    download_eia_csv("T04.01", "EIA_T04_01_Natural_Gas_Overview_Monthly.csv")
    
    print("Download Pipeline Complete.")
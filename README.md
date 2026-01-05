# Henry Hub Natural Gas Price Analysis  
**Data Processing in Python (JEM207)**

## Project Overview
This project analyzes Henry Hub natural gas prices using official data from the (EIA). The primary objective is to build a fully reproducible Python-based data pipeline that automatically downloads raw price data, cleans and processes it into an analysis-ready format, and prepares the foundation for empirical analysis of price dynamics.

The project emphasizes correct data acquisition, temporal alignment, and financial reasoning rather than premature modeling. The final analytical goal is to study how weekly price movements relate to fundamental information shocks such as storage dynamics and seasonal effects.

---

## Motivation
Henry Hub is the benchmark pricing location for natural gas in North America. While the EIA publishes extensive historical price data, it is provided in a reporting-oriented format (weekly tables with weekday columns and textual date ranges) that is not immediately suitable for statistical analysis. This project addresses that gap by transforming raw EIA reporting data into a clean, well-structured time series suitable for econometric analysis.

---

## Data Source
- **Source:** U.S. Energy Information Administration (EIA)
- **Data:** Henry Hub natural gas spot prices
- **Original Format:** Weekly tables with Monday–Friday prices and textual date ranges
- **Access Method:** Automated download via Python (HTML table parsing)

Raw data is stored unchanged to preserve data provenance and reproducibility.

---

## Project Structure

---

## Methodology

### 1. Automatic Data Collection
A Python script (`src/download_henryhub_raw.py`) programmatically downloads the Henry Hub price tables directly from the EIA website and extracts the relevant weekly price table. The extracted data is saved unchanged in the `data/raw` directory.

### 2. Data Cleaning and Processing
Using VSCODE notebook:
- Blank and separator rows are removed
- Textual week ranges are parsed into real calendar dates
- Prices are converted to numeric format
- Wide weekday tables are reshaped into tidy long format
- Daily prices are aggregated into weekly prices (Friday close)

### 3. Financial Transformation
Weekly log returns are computed from the weekly price series. Weekly frequency is chosen to align with the timing of key information releases in natural gas markets, particularly storage reports.

---

## Current Status (Work in Progress)
At this stage, the project has:
- A fully reproducible data ingestion pipeline
- Clean daily and weekly Henry Hub price series
- Weekly log returns constructed as the dependent variable

Next steps include merging weekly storage data, constructing storage surprises, and analyzing how price responses vary across seasons.

---

## Reproducibility
The project is designed to run from scratch:
1. Clone the repository
2. Install dependencies
3. Run the data download script
4. Execute the cleaning notebook

All paths are handled robustly, and raw data is preserved separately from processed outputs.

---

## Technologies Used
- Python
- pandas
- numpy
- matplotlib
- requests
- Git / GitHub

---

## Authors
Project completed as part of **Data Processing in Python (JEM207)**  
Charles University
Gabriel Ferreira 
Richard Lesko



# Data Dictionary & Methodology

## Overview
In this file we explain the different types of data that were gathered, what was done to them, why those transformations were applied, and why this approach best supports the objectives of the project.

---

## Project Context
This project analyzes structural changes in the U.S. natural gas market, focusing on the impact of the Shale Revolution around 2010 on price volatility.

---

## Target Variable: Natural Gas Price
- **Source:** U.S. Energy Information Administration (EIA)
- **Frequency:** Weekly (Friday close)
- **Units:** USD per Million Btu
- **Rationale:** Weekly aggregation balances noise reduction and temporal resolution.

---

## Weather Variables

### Heating Degree Days (HDD)
- **Source:** EIA Monthly Energy Review (Table 1.11)
- **Definition:** `max(0, 65°F − average temperature)`
- **Purpose:** Proxy for winter heating demand

### Cooling Degree Days (CDD)
- **Source:** EIA Monthly Energy Review (Table 1.12)
- **Definition:** `max(0, average temperature − 65°F)`
- **Purpose:** Proxy for summer electricity demand

---

## Fundamental Variables

### Natural Gas Production (Dry)
- **Definition:** Marketable natural gas excluding liquids
- **Purpose:** Captures the shale-driven supply shock

### Natural Gas Exports
- **Definition:** Pipeline and LNG exports
- **Purpose:** Links domestic prices to global markets post-2016

### Storage Withdrawals
- **Definition:** Gas withdrawn from underground storage
- **Purpose:** Measures scarcity and short-term supply stress

---

## Data Engineering Methodology

### Frequency Mismatch
- Prices: Weekly  
- Fundamentals: Monthly  

### Solution: Broadcast Merge
Monthly fundamentals are mapped onto weekly prices using a `YYYYMM` key.

**Example:**  
All January 2020 weekly observations share January 2020 HDD values.

---

## Justification
This approach is standard in long-horizon commodity and energy market studies.

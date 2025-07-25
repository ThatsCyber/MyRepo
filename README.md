# Facility Management Desktop Application

A Python-based desktop application for managing facility data, site validation, and proximity analysis.

## Features

- Load and validate facility data from Excel files
- Process site actions (DEPART TEC, NEED TEC)
- Cart site management and validation
- Proximity analysis for finding nearby sites
- Modern dark-mode GUI interface

## Requirements

- Python 3.8 or higher
- Required packages (install via `pip install -r requirements.txt`):
  - PyQt6
  - pandas
  - openpyxl
  - geopy
  - qt-material

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Load Data:
   - Click "Load Facilities Excel" to load the facilities data file
   - Click "Load Cart Data CSV" to load the cart supply & demand data

3. Site Operations:
   - Enter a site code (e.g., "JAN1") or site-to-site format (e.g., "GYR1->GYR2")
   - Click "Depart TEC" or "Need TEC" to generate the appropriate output
   - Click "Check Cart Site" to view cart site information

4. Proximity Analysis:
   - Enter a site code
   - Select the number of nearby sites to find
   - Click "Find Nearby Sites" to see the results
   - Cart sites with negative balance will be highlighted in red

## Data File Requirements

### Facilities Excel File
- Must be an `.xlsx` or `.xlsm` file
- Must contain a sheet named "Facilities_Updated"
- Expected columns: name, type, status, latitude, longitude, etc.
- Should have 1,800-1,850 rows (including header)

### Cart Data CSV File
- Must be a `.csv` file
- Required columns: Site Name, Demand, Supply, Balance
- All site names must exist in the facilities data

## Notes

- Site names are case-insensitive
- For proximity calculations, verified coordinates are preferred over regular coordinates
- The application will automatically try to load "Facilities_Updated.xlsm" on startup if available
- Cart sites with negative balance are highlighted for easy identification

## Error Handling

- Invalid sites will be reported in the output area
- Missing or invalid data files will trigger warning messages
- Coordinate errors will fall back to alternative coordinates when available 
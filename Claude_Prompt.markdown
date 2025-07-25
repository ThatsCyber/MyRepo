# Claude-4-Sonnet Prompt: Development Plan for Facility Management Desktop App

## Objective
Create a detailed development plan for a Python-based desktop application using PyQt6 to manage facility data from `Facilities_Updated.xlsm` (1,827 rows: 1,826 sites + header) and `Supply_&_Demand_<numbers>.csv` (343 cart sites). The app supports site validation, output generation, cart site management, proximity analysis prioritizing negative `Balance` sites, and analytics, with a modern dark-mode GUI and Windows `.exe` deployment via PyInstaller.

## Data Sources
1. **Facilities_Updated.xlsm**:
   - **Sheet**: `Facilities_Updated` (1,827 rows: 1 header, 1,826 sites).
   - **Columns**: `name` (str, e.g., `JAN1`, `ABE2`), `type` (e.g., `RSR`, `IXD`), `status` (e.g., `Active`, `Idle`), `latitude` (float), `longitude` (float), `address` (str), `state` (str), `region` (str, e.g., `MS`, `TX`), `country` (str), `zip` (str), `timeZone` (str, e.g., `America/Chicago (UTC:-05:00)`), `Verified_Lat` (float), `Verified_Long` (float), `Match_Status` (str, e.g., `Match`, `Mismatch`), `API_Status` (str, e.g., `OK`).
   - **Notes**:
     - `name` must be treated as text (`dtype=str` in `pandas`) to prevent Excel misinterpreting strings like `JAN1` as dates (e.g., `1-Jan`).
     - Use `Verified_Lat` (column L, index 11) and `Verified_Long` (column M, index 12) for proximity calculations. Fall back to `latitude`/`longitude` if `Verified_Lat`/`Verified_Long` are missing (e.g., `WHL1`).
     - Expected row count: ~1,826 sites (1,827 rows including header). Validate row count (1,800–1,850) and alert if outside this range.
   - **Access**: Read via `pandas` with `openpyxl`.

2. **Supply_&_Demand_<numbers>.csv**:
   - **Rows**: 343 cart sites.
   - **Columns**: `Site Name` (str, matches `name` in Excel, e.g., `JAN1`, `SAT9`), `Demand` (int, e.g., 3), `Supply` (int, e.g., 12), `Balance` (int, e.g., 9 = Supply - Demand).
   - **Notes**:
     - `<numbers>` is a timestamp (e.g., `1751712301452`). Parse flexibly to support formats like `7/5/2025 0:00`.
     - Treat `Site Name` as text (`dtype=str`) to avoid date misinterpretation.
     - All `Site Name` values must exist in `Facilities_Updated.xlsm`’s `name` column.
   - **Access**: Allow manual CSV selection via file picker. Read via `pandas`.

3. **Regions Sheet** (in `Facilities_Updated.xlsm`):
   - Maps `state` to `region` (e.g., `MS` → `MS`, `TX` → `TX`, `NY` → `NE`).
   - Use for assigning regions to outputs and filtering.

## Functional Requirements
### 1. Site Validation and Output Generation
- **Input**: Single input field accepting:
  - Single site (e.g., `JAN1`).
  - Site-to-site format (e.g., `GYR1->GYR2`).
- **Buttons**:
  - **Depart TEC**: Generate output like `JAN1- DEPART TEC MS` or `GYR1->GYR2` → `GYR1- DEPART TEC SW`.
  - **Need TEC**: Generate output like `JAN1- NEED TEC MS` or `GYR1->GYR2` → `GYR1- NEED TEC SW`.
  - **Check Cart Site**: Validate if input site is in `Supply_&_Demand_<numbers>.csv` and display `Demand`, `Supply`, `Balance`.
- **Output Format**:
  - Always include a space after the dash (e.g., `JAN1- NEED TEC MS`, not `JAN1-NEED TEC MS`).
  - For `SITE->DESTINATION`, use origin site’s `region` (e.g., `GYR1->GYR2` uses `GYR1`’s `region=SW`).
  - Display output in a copyable text field.
- **Validation**:
  - Check if input site(s) exist in `Facilities_Updated.xlsm`’s `name` column.
  - For `SITE->DESTINATION`, validate both sites. If invalid, show error (e.g., “Invalid site: XYZ1”).
  - Case-insensitive matching (e.g., `jan1` matches `JAN1`).

### 2. Proximity Feature
- **Purpose**: For any site in `Facilities_Updated.xlsm` (1,826 sites), find the 5–10 nearest sites (configurable, default 5) within 50 miles using `Verified_Lat`/`Verified_Long`.
- **Implementation**:
  - Use `geopy.distance.geodesic` for distance calculations.
  - If `Verified_Lat`/`Verified_Long` are missing, use `latitude`/`longitude`. If both missing, skip site with error message.
  - For cart sites (in CSV), include `Demand`, `Supply`, `Balance` in output.
  - Highlight sites with negative `Balance` (e.g., `TPA2`, `Balance=-2`) in red or bold to prioritize cart transfers.
- **Output**: Table with columns: `name`, `address`, `state`, `region`, `distance` (miles), and (for cart sites) `Demand`, `Supply`, `Balance`.

### 3. Cart Site Management
- **Check Cart Site**:
  - If input site is in CSV, display `Demand`, `Supply`, `Balance`, and label as “Cart Site” in dashboard.
  - If not in CSV, label as “Non-Cart Site” and show site details from Excel.
- **Proximity for Cart Sites**:
  - Prioritize displaying nearby cart sites with negative `Balance` to suggest transfers (e.g., move carts from surplus to `TPA2`).

### 4. Analytics
- **Dashboard**:
  - Display total `Demand` and `Supply` by `region` (from CSV, grouped by `region` in Excel).
  - Show count of cart sites with negative `Balance` (e.g., 2 sites: `TPA2`, `SAT5`).
- **Filters**:
  - Allow filtering sites by `region`, `state`, or cart status (in CSV or not).
  - Display filtered results in a table with all Excel columns.

### 5. GUI Requirements
- **Framework**: PyQt6.
- **Theme**: Dark mode (default) with toggle for light mode. Use QtMaterial or stylesheets for modern look (e.g., rounded buttons, clean fonts).
- **Layout**:
  - **Top**: Single input field for site or `SITE->DESTINATION`, with “Depart TEC,” “Need TEC,” and “Check Cart Site” buttons.
  - **Middle**: Copyable output field (e.g., `JAN1- NEED TEC MS`).
  - **Bottom**: Dashboard with:
    - Site details table (all Excel columns for input site).
    - Neighboring sites table (proximity results).
    - Analytics (total `Demand`/`Supply` by `region`, negative `Balance` count).
  - **Filters**: Dropdowns for `region`, `state`, cart status.
- **File Picker**: Allow manual selection of `Supply_&_Demand_<numbers>.csv`.
- **Responsiveness**: Support Windows desktop, resizable window.

### 6. Error Handling
- **File Errors**:
  - Missing `Facilities_Updated.xlsm` or CSV: Prompt user to select files.
  - Row count deviation: Alert if `Facilities_Updated` has <1,800 or >1,850 rows.
  - Missing `Site Name` in Excel: Flag missing cart sites.
- **Input Errors**:
  - Invalid site: Show “Invalid site: [input]” in output field.
  - Malformed `SITE->DESTINATION`: Show “Invalid format. Use SITE->DESTINATION”.
- **Coordinate Errors**:
  - Missing `Verified_Lat`/`Verified_Long`: Use `latitude`/`longitude` or skip with warning.
- **CSV Parsing**:
  - Handle flexible date formats (e.g., `7/5/2025 0:00`, `2025-07-05`).

### 7. Deployment
- **Platform**: Windows desktop.
- **Packaging**: Use PyInstaller to create a single `.exe` file.
- **Dependencies**: Include `pandas`, `openpyxl`, `geopy`, `PyQt6` in requirements.
- **File Access**: Assume `Facilities_Updated.xlsm` is in app directory; allow CSV selection via file picker.

## Deliverables
- **Development Plan**:
  - Detailed steps to implement the app, including:
    - File reading (`pandas`, `openpyxl`).
    - GUI structure (PyQt6 layout, widgets, dark mode).
    - Proximity calculations (`geopy.distance.geodesic`).
    - Output formatting (e.g., `JAN1- NEED TEC MS`).
    - Error handling and validation.
    - Analytics and filtering logic.
    - Deployment instructions (PyInstaller).
  - Sample code snippets for key components (e.g., file reading, distance calculation, GUI setup).
- **File Structure**:
  - `main.py`: Entry point, GUI initialization.
  - `data_handler.py`: File reading, validation, analytics.
  - `proximity.py`: Distance calculations, neighbor table generation.
  - `gui.py`: PyQt6 widgets, layout, styles.
  - `requirements.txt`: List dependencies.
- **Testing Plan**:
  - Test cases for:
    - Valid/invalid site inputs (e.g., `JAN1`, `XYZ1`, `GYR1->GYR2`).
    - Proximity for sites with/without `Verified_Lat`/`Verified_Long`.
    - Cart site validation and negative `Balance` highlighting.
    - CSV parsing with different date formats.
    - Row count validation (1,827 rows in Excel).
  - Edge cases (e.g., missing files, empty inputs).

## Notes
- Ensure `JAN1` is treated as text, not a date, in all operations.
- Output format must include space after dash (e.g., `GYR1- NEED TEC SW`).
- Prioritize negative `Balance` sites in proximity table for cart transfers.
- Use `pandas` for data operations, `geopy` for distances, `PyQt6` for GUI.
- Validate all cart sites (343) exist in Excel’s `name` column.
- Handle flexible CSV naming (`Supply_&_Demand_<numbers>.csv`).
- Deploy as a standalone Windows `.exe` with PyInstaller.

Please provide a comprehensive development plan with code snippets, file structure, and testing plan to build this app.
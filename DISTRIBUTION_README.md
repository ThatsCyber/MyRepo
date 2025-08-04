# Facility Management Application

## 📋 About
This is a comprehensive facility management application that helps track cart balances, utilization rates, and proximity analysis for various sites.

## 🚀 Quick Start

### For End Users (Receiving the Executable)
1. **Download** the `FacilityManagement.exe` file
2. **Create a folder** for the application (e.g., "Facility Management")
3. **Copy the executable** to this folder
4. **Add your data files** (CSV files) to the same folder
5. **Double-click** `FacilityManagement.exe` to run

### Required Data Files
Make sure you have these CSV files in the same folder as the executable:
- `Facilities_Updated.csv` - Main facilities data
- Supply & Demand CSV files (for cart data)
- Yard Utilization CSV files 
- TEC Dwelling CSV files

## 🔧 Features
- **Site Information Lookup** - Search for detailed site information
- **Cart Balance Analysis** - Track supply/demand balance with negative values highlighted in red
- **Utilization Monitoring** - View utilization percentages with color coding (90%+ in red/orange)
- **Proximity Search** - Find nearby sites with distance calculations
- **Auto Load** - Automatically detect and load the most recent data files
- **Sister Sites Support** - Group related sites together
- **Export Functionality** - Generate reports and data exports

## 🎨 Visual Indicators
- **Bold Text** = Cart sites (sites with supply/demand data)
- **Red Text** = Negative numbers (deficits, shortages)
- **Red/Orange Text** = High utilization (90%+ capacity)
- **Dynamic Row Heights** = Multi-line sister site names

## 💡 Usage Tips
1. **Load Data in Order**: Facilities → Supply & Demand → Utilization → Dwelling
2. **Use Auto Download**: Automatically loads the most recent files from Downloads folder
3. **Search Multiple Sites**: Enter multiple sites separated by new lines
4. **Sister Sites**: Use format "MAIN / SISTER1 / SISTER2" in facilities file

## 🐛 Troubleshooting
- **App won't start**: Make sure all CSV files are in the same folder
- **Data not loading**: Check CSV file formats and column headers
- **Performance issues**: Close other applications if processing large datasets

## 📞 Support
Contact the system administrator for technical support or data file format questions.

---
*Built with Python, PyQt6, and PyInstaller* 
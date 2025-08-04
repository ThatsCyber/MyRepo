# How to Build the Executable

## Option 1: Using the Build Script (Recommended)

1. **Open Command Prompt or PowerShell** where Python works
2. **Navigate to the project folder**:
   ```bash
   cd "C:\Users\kambroem\Documents\Cursor\MyRepo-main"
   ```

3. **Run the build script**:
   ```bash
   python build_executable.py
   ```

## Option 2: Manual PyInstaller Command

If the build script doesn't work, run these commands manually:

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**:
   ```bash
   pyinstaller --onefile --windowed --name "FacilityManagement" main.py
   ```

   Or for more control:
   ```bash
   pyinstaller --onefile --windowed --add-data "Facilities_Updated.csv;." --hidden-import pandas --hidden-import PyQt6 --hidden-import openpyxl --hidden-import geopy --name "FacilityManagement" main.py
   ```

## Option 3: Using the Spec File

1. **Create the spec file** (already created as `FacilityManagement.spec`)
2. **Build using spec**:
   ```bash
   pyinstaller --clean FacilityManagement.spec
   ```

## 📁 Output Location

After successful build, your executable will be in:
- **`dist/FacilityManagement.exe`** - The standalone executable

## 📦 Distribution Package

To distribute, create a folder with:
```
Facility Management/
├── FacilityManagement.exe          # The main executable
├── Facilities_Updated.csv          # Required data file
├── DISTRIBUTION_README.md           # User instructions
└── (any other CSV files needed)
```

## 🚀 Alternative: Quick Build Commands

If you have Python working, you can run these one-liners:

**Simple build:**
```bash
pyinstaller --onefile --windowed main.py
```

**Advanced build with dependencies:**
```bash
pyinstaller --onefile --windowed --add-data "*.csv;." --hidden-import pandas --hidden-import PyQt6 --hidden-import openpyxl --hidden-import geopy --name FacilityManagement main.py
```

## ✅ Testing

1. **Test locally**: Run the exe in the `dist` folder
2. **Test on another machine**: Copy the exe + CSV files to test distribution
3. **Verify all features work**: Load data, search sites, check proximity, etc.

## 🐛 Troubleshooting

**If build fails:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try the simple build first, then add complexity
- Check that `main.py` is in the current directory

**If exe doesn't run:**
- Include CSV files in the same folder as the exe
- Try running from command line to see error messages
- Use `--console` flag in PyInstaller to see debug output 
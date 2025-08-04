#!/usr/bin/env python3
"""
Build script for Facility Management Application
Creates a standalone executable that can be distributed to other machines.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.3.0"])
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create a PyInstaller spec file with proper configuration"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Facilities_Updated.csv', '.'),
        ('*.csv', '.'),
    ],
    hiddenimports=[
        'pandas',
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'openpyxl',
        'geopy',
        'geopy.distance',
        'qt_material',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'PIL',
        'numpy.distutils',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FacilityManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file here if you have an icon
)
'''
    
    with open('FacilityManagement.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created FacilityManagement.spec file")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    print("This may take a few minutes...")
    
    try:
        # Run PyInstaller with the spec file
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", 
            "--clean",  # Clean build
            "FacilityManagement.spec"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            print("📁 Location: dist/FacilityManagement.exe")
            print("📦 You can now distribute this executable to other machines")
            print("\n📋 Distribution Notes:")
            print("   • The executable is completely standalone")
            print("   • Users don't need Python or any dependencies installed")
            print("   • Include any required CSV files in the same folder")
            print("   • The executable will work on Windows machines")
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error building executable: {e}")
        return False
    
    return True

def main():
    """Main build process"""
    print("🚀 Building Facility Management Executable")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        print("Please run this script from the MyRepo-main directory")
        sys.exit(1)
    
    # Install PyInstaller if needed
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("Your executable is ready for distribution!")
    else:
        print("\n💥 Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
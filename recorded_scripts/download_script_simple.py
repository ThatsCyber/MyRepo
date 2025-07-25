import time
import pyautogui
import subprocess
import os
from pathlib import Path

def run_download():
    """Simple download automation using keyboard/mouse automation"""
    
    print("\n" + "="*60)
    print("🎯 SIMPLE SUPPLY & DEMAND EXPORT AUTOMATION")
    print("="*60)
    print("This script will help you automate the download using keyboard shortcuts")
    print("Make sure:")
    print("1. Chrome is open with QuickSight dashboard")
    print("2. You can see the Supply & Demand chart")
    print("3. You're ready to follow the automation")
    print("="*60)
    
    # Give user time to prepare
    print("\n⏱️  Starting automation in 5 seconds...")
    print("Please make sure Chrome is the active window with QuickSight open!")
    
    for i in range(5, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    
    print("\n🚀 Starting automation!")
    
    try:
        # Step 1: Instructions for user
        print("\n📋 Step 1: Please manually navigate to the Supply & Demand chart")
        print("Make sure you can see the Supply & Demand chart on your screen")
        input("Press Enter when you can see the Supply & Demand chart...")
        
        # Step 2: Find and click the 3-dots menu
        print("\n📋 Step 2: Looking for the 3-dots menu...")
        print("The script will now try to help you click the 3-dots menu")
        print("Move your mouse to the 3-dots menu (⋮) in the top-right of the Supply & Demand chart")
        input("Position your mouse over the 3-dots menu, then press Enter...")
        
        # Click the 3-dots menu
        print("Clicking the 3-dots menu...")
        pyautogui.click()
        time.sleep(2)
        
        # Step 3: Look for Export to CSV
        print("\n📋 Step 3: Looking for 'Export to CSV' option...")
        print("A dropdown menu should now be visible")
        print("Move your mouse to 'Export to CSV' option")
        input("Position your mouse over 'Export to CSV', then press Enter...")
        
        # Click Export to CSV
        print("Clicking 'Export to CSV'...")
        pyautogui.click()
        time.sleep(3)
        
        # Step 4: Wait for download
        print("\n📋 Step 4: Waiting for download to complete...")
        print("The CSV file should now be downloading...")
        time.sleep(5)
        
        # Check Downloads folder for new files
        downloads_path = Path.home() / "Downloads"
        csv_files = list(downloads_path.glob("*.csv"))
        
        # Sort by modification time (newest first)
        if csv_files:
            csv_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            print(f"\n📁 Recent CSV files in Downloads:")
            for i, file in enumerate(csv_files[:5]):
                mod_time = time.ctime(file.stat().st_mtime)
                print(f"  {i+1}. {file.name} (modified: {mod_time})")
            
            newest_file = csv_files[0]
            # Check if the file was modified in the last 30 seconds
            if time.time() - newest_file.stat().st_mtime < 30:
                print(f"\n🎉 SUCCESS! New CSV file detected:")
                print(f"📄 {newest_file.name}")
                print(f"📁 Location: {newest_file}")
                
                # Check if it looks like Supply & Demand data
                if "supply" in newest_file.name.lower() or "demand" in newest_file.name.lower():
                    print("✅ File name suggests this is Supply & Demand data!")
                else:
                    print("⚠️ File name doesn't clearly indicate Supply & Demand data")
                    print("Please verify this is the correct file")
            else:
                print("⚠️ No new CSV files detected in the last 30 seconds")
                print("The download might still be in progress or may have failed")
        else:
            print("❌ No CSV files found in Downloads folder")
        
        print("\n" + "="*60)
        print("✅ Automation completed!")
        print("Please check your Downloads folder for the CSV file")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error during automation: {e}")
        print("You can complete the download manually:")
        print("1. Click the 3-dots menu (⋮) on the Supply & Demand chart")
        print("2. Click 'Export to CSV'")
        print("3. Wait for download to complete")

if __name__ == "__main__":
    run_download() 
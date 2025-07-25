from playwright.sync_api import sync_playwright
import time

def manual_recording():
    """Connect to existing Chrome and help record the correct download actions"""
    
    with sync_playwright() as playwright:
        try:
            # Connect to your existing authenticated Chrome
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
            contexts = browser.contexts
            
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    page = pages[0]
                    print(f"Connected to page: {page.url}")
                    
                    print("\n" + "="*60)
                    print("🎬 MANUAL RECORDING SESSION")
                    print("="*60)
                    print("I'm now connected to your authenticated Chrome browser.")
                    print("\nPLEASE DO THE FOLLOWING:")
                    print("1. Navigate to the Supply & Demand chart/table")
                    print("2. Click on the exact 3-dots menu or Export button")
                    print("3. Click 'Export to CSV'")
                    print("4. Wait for download to complete")
                    print("5. Press Enter here when you're done")
                    print("\nI'll capture the exact selectors you use...")
                    print("="*60)
                    
                    # Capture initial state
                    print("\n📸 Capturing initial page state...")
                    initial_buttons = []
                    all_buttons = page.locator("button").all()
                    for i, button in enumerate(all_buttons):
                        try:
                            if button.is_visible():
                                aria_label = button.get_attribute("aria-label") or ""
                                data_id = button.get_attribute("data-automation-id") or ""
                                title = button.get_attribute("title") or ""
                                if aria_label or data_id or title:
                                    initial_buttons.append({
                                        'index': i,
                                        'aria_label': aria_label,
                                        'data_id': data_id,
                                        'title': title
                                    })
                        except:
                            pass
                    
                    print(f"✅ Found {len(initial_buttons)} initial buttons")
                    
                    # Wait for user to perform actions
                    input("\n⏸️  Press Enter after you've completed the download process...")
                    
                    print("\n📸 Capturing post-action page state...")
                    
                    # Look for download indicators
                    download_indicators = [
                        "text=/download.*complete/i",
                        "text=/export.*complete/i", 
                        "text=/file.*ready/i",
                        "text=/successfully.*exported/i",
                        "[class*='success']",
                        "[class*='notification']",
                        "text=/csv/i"
                    ]
                    
                    print("\n🔍 Checking for download completion indicators...")
                    for indicator in download_indicators:
                        try:
                            elements = page.locator(indicator).all()
                            for element in elements:
                                if element.is_visible():
                                    text = element.inner_text()
                                    print(f"✅ Download indicator: '{text}'")
                        except:
                            pass
                    
                    # Check Downloads folder for new files
                    print("\n📁 Checking for new CSV files...")
                    import os
                    import glob
                    downloads_path = os.path.expanduser("~/Downloads")
                    csv_files = glob.glob(os.path.join(downloads_path, "*.csv"))
                    
                    # Sort by modification time (newest first)
                    csv_files.sort(key=os.path.getmtime, reverse=True)
                    
                    print(f"Recent CSV files in Downloads:")
                    for i, file in enumerate(csv_files[:5]):
                        mod_time = time.ctime(os.path.getmtime(file))
                        filename = os.path.basename(file)
                        print(f"  {i+1}. {filename} (modified: {mod_time})")
                    
                    print("\n" + "="*60)
                    print("🎯 RECORDING COMPLETE!")
                    print("="*60)
                    print("Now I need you to tell me:")
                    print("1. Which exact button did you click to open the menu?")
                    print("2. What was the exact text of the export option?")
                    print("3. Did the download complete successfully?")
                    print("\nI'll use this info to create the correct automation script.")
                    
                else:
                    print("No pages found")
            else:
                print("No contexts found")
                
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure Chrome is running with --remote-debugging-port=9222")

if __name__ == "__main__":
    manual_recording() 
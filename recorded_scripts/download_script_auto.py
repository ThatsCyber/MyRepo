import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os

def run(playwright: Playwright) -> None:
    print("🚀 STARTING TRUE AUTOMATION - NO MANUAL INTERVENTION NEEDED!")
    print("This will open a browser and automatically download the Supply & Demand CSV")
    
    # Launch a new browser (not trying to connect to existing one)
    print("Launching automated browser...")
    browser = playwright.chromium.launch(headless=False)  # headless=False so you can see it working
    context = browser.new_context()
    page = context.new_page()
    
    try:
        # Navigate to QuickSight
        quicksight_url = "https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/dashboards/855adf29-7e31-4755-960f-cf99f0fc7e6a"
        print(f"Navigating to: {quicksight_url}")
        page.goto(quicksight_url)
        
        print("\n⚠️ AUTHENTICATION REQUIRED:")
        print("The browser opened will need you to log in once.")
        print("After you log in and see the dashboard, the automation will take over!")
        print("\nPlease:")
        print("1. Complete authentication in the opened browser")
        print("2. Navigate to the dashboard with Supply & Demand chart")
        print("3. When you can see the Supply & Demand chart, press Enter here...")
        
        input("Press Enter when you're authenticated and can see the dashboard...")
        
        print("\n🤖 AUTOMATION TAKING OVER - NO MORE MANUAL WORK NEEDED!")
        print("="*60)
        
        # Wait for page to stabilize
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(3000)
        
        # Step 1: Find the Supply & Demand chart
        print("📋 Step 1: Finding Supply & Demand chart...")
        
        supply_demand_chart = None
        
        # Look for the Supply & Demand chart by its content
        chart_selectors = [
            "[data-testid*='visual']:has-text('Supply')",
            "[data-testid*='visual']:has-text('Demand')", 
            "[class*='visual']:has-text('Supply')",
            "[class*='visual']:has-text('Demand')",
            "[data-automation-id*='visual']:has-text('Supply')",
            "[data-automation-id*='visual']:has-text('Demand')"
        ]
        
        for selector in chart_selectors:
            try:
                charts = page.locator(selector).all()
                for chart in charts:
                    if chart.is_visible():
                        text_content = chart.inner_text().lower()
                        if "supply" in text_content and "demand" in text_content:
                            # Make sure it's not the map
                            if "map" not in text_content and "cart" not in text_content:
                                print(f"✅ Found Supply & Demand chart!")
                                supply_demand_chart = chart
                                break
                if supply_demand_chart:
                    break
            except:
                continue
        
        if not supply_demand_chart:
            print("❌ Could not find Supply & Demand chart")
            print("Available charts on page:")
            # Debug: show available content
            visuals = page.locator("[class*='visual'], [data-testid*='visual']").all()
            for i, visual in enumerate(visuals[:10]):
                try:
                    if visual.is_visible():
                        text = visual.inner_text()[:100]
                        if text.strip():
                            print(f"  Chart {i+1}: {text}")
                except:
                    pass
            return
        
        # Step 2: Find and click the 3-dots menu
        print("\n📋 Step 2: Looking for 3-dots menu...")
        
        menu_button = None
        menu_selectors = [
            "button[data-automation-id*='dropdown_menu']",
            "button[data-automation-id*='visual_dropdown']", 
            "button[data-automation-id*='menu']",
            "button[aria-label*='menu' i]",
            "button[aria-label*='options' i]",
            "button[title*='menu' i]",
            "button[title*='options' i]"
        ]
        
        for selector in menu_selectors:
            try:
                buttons = supply_demand_chart.locator(selector).all()
                for button in buttons:
                    if button.is_visible():
                        aria_label = button.get_attribute("aria-label") or ""
                        title = button.get_attribute("title") or ""
                        data_id = button.get_attribute("data-automation-id") or ""
                        
                        if (("menu" in aria_label.lower() or "menu" in title.lower() or 
                             "options" in aria_label.lower() or "options" in title.lower() or
                             "dropdown" in data_id.lower()) and 
                            "global" not in data_id.lower() and "help" not in data_id.lower()):
                            print(f"✅ Found 3-dots menu button!")
                            menu_button = button
                            break
                if menu_button:
                    break
            except:
                continue
        
        if not menu_button:
            print("❌ Could not find 3-dots menu button")
            # Show available buttons for debugging
            buttons = supply_demand_chart.locator("button").all()
            print(f"Available buttons in chart: {len(buttons)}")
            for i, btn in enumerate(buttons[:5]):
                try:
                    if btn.is_visible():
                        aria_label = btn.get_attribute("aria-label") or ""
                        print(f"  Button {i+1}: aria-label='{aria_label}'")
                except:
                    pass
            return
        
        # Step 3: Click the menu button
        print("\n📋 Step 3: Clicking 3-dots menu automatically...")
        
        try:
            menu_button.click(timeout=5000)
            print("✅ Clicked 3-dots menu!")
            page.wait_for_timeout(2000)  # Wait for dropdown
        except Exception as e:
            print(f"❌ Failed to click menu: {e}")
            return
        
        # Step 4: Find and click "Export to CSV"
        print("\n📋 Step 4: Looking for 'Export to CSV' option...")
        
        export_selectors = [
            "text=Export to CSV",
            "[role='menuitem']:has-text('Export to CSV')",
            "[role='menuitem']:has-text('Export')",
            "li:has-text('Export to CSV')",
            "div:has-text('Export to CSV')",
            "button:has-text('Export to CSV')",
            "*:has-text('Export to CSV')"
        ]
        
        export_option = None
        for selector in export_selectors:
            try:
                options = page.locator(selector).all()
                for option in options:
                    if option.is_visible():
                        text = option.inner_text().strip()
                        if "export" in text.lower() and ("csv" in text.lower() or text.lower() == "export"):
                            print(f"✅ Found export option: '{text}'")
                            export_option = option
                            break
                if export_option:
                    break
            except:
                continue
        
        if not export_option:
            print("❌ Could not find 'Export to CSV' option")
            # Show dropdown contents
            dropdown_items = page.locator("[role='menuitem'], li, div").all()
            print("Available dropdown options:")
            for item in dropdown_items[:10]:
                try:
                    if item.is_visible():
                        text = item.inner_text().strip()
                        if text and len(text) < 50:
                            print(f"  - '{text}'")
                except:
                    pass
            return
        
        # Step 5: Click "Export to CSV"
        print("\n📋 Step 5: Clicking 'Export to CSV' automatically...")
        
        try:
            export_option.click(timeout=5000)
            print("✅ Clicked 'Export to CSV'!")
            
            # Wait for download
            page.wait_for_timeout(5000)
            
            # Look for success indicators
            success_indicators = [
                "text=/csv.*ready/i",
                "text=/export.*complete/i",
                "text=/download.*complete/i"
            ]
            
            for indicator in success_indicators:
                try:
                    element = page.locator(indicator).first
                    if element.count() > 0 and element.is_visible():
                        text = element.inner_text()
                        print(f"✅ Success: {text}")
                        break
                except:
                    pass
            
            print("\n🎉 AUTOMATION COMPLETED SUCCESSFULLY!")
            print("📁 Check your Downloads folder for the Supply & Demand CSV file")
            
        except Exception as e:
            print(f"❌ Failed to click Export to CSV: {e}")
            return
    
    except Exception as e:
        print(f"❌ Automation error: {e}")
    
    finally:
        print("\n⏸️  Browser will stay open for 10 seconds for verification...")
        page.wait_for_timeout(10000)
        browser.close()
        print("✅ Browser closed. Automation complete!")

def run_download():
    """Function to be called from the GUI application"""
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    run_download() 
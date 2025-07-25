import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    print("Connecting to your authenticated Chrome browser...")
    
    # Connect to existing Chrome browser
    try:
        print("Attempting to connect to Chrome debugging port...")
        
        # Try multiple connection methods
        browser = None
        connection_methods = [
            "http://localhost:9222",
            "http://127.0.0.1:9222"
        ]
        
        for method in connection_methods:
            try:
                print(f"Trying {method}...")
                browser = playwright.chromium.connect_over_cdp(method)
                print(f"✅ Successfully connected via {method}!")
                break
            except Exception as e:
                print(f"❌ {method} failed: {e}")
                continue
        
        if not browser:
            print("❌ Could not connect to Chrome debugging port")
            print("Please ensure Chrome is running with: --remote-debugging-port=9222")
            print("You can restart Chrome with debugging using:")
            print('  Start-Process "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" -ArgumentList "--remote-debugging-port=9222"')
            return
        
        # Get all contexts and pages
        contexts = browser.contexts
        print(f"Found {len(contexts)} contexts")
        
        if contexts:
            context = contexts[0]  # Use the first available context
            pages = context.pages
            print(f"Found {len(pages)} pages in context")
            
            if pages:
                # Look for a QuickSight page or use the first one
                page = None
                for p in pages:
                    url = p.url
                    print(f"Found page: {url}")
                    if "quicksight" in url.lower():
                        page = p
                        print("✅ Using existing QuickSight page")
                        break
                
                if not page:
                    page = pages[0]  # Use the first available page
                    print("Using first available page")
            else:
                print("No existing pages, creating new page")
                page = context.new_page()
        else:
            print("No existing contexts, creating new context and page")
            context = browser.new_context()
            page = context.new_page()
    
    except Exception as e:
        print(f"❌ Could not connect to existing Chrome: {e}")
        print("Make sure Chrome is running with --remote-debugging-port=9222")
        return
    
    # Wait for page to load
    page.wait_for_load_state('networkidle')
    print("✅ Page loaded successfully!")
    
    # Wait a bit more for dynamic content
    page.wait_for_timeout(3000)
    
    print("\n" + "="*60)
    print("🎯 SUPPLY & DEMAND EXPORT AUTOMATION")
    print("="*60)
    print("Based on your manual instructions:")
    print("1. Find the Supply & Demand chart")
    print("2. Click the 3-dots menu (top-right of chart)")
    print("3. Click 'Export to CSV' from dropdown")
    print("="*60)
    
    try:
        # Step 1: Find the Supply & Demand chart specifically
        print("\n📋 Step 1: Looking for Supply & Demand chart...")
        
        supply_demand_chart = None
        
        # Look for the Supply & Demand chart by its title/content
        chart_selectors = [
            # Look for charts with Supply & Demand in title or content
            "[data-testid*='visual']:has-text('Supply')",
            "[data-testid*='visual']:has-text('Demand')", 
            "[class*='visual']:has-text('Supply')",
            "[class*='visual']:has-text('Demand')",
            # QuickSight specific visual containers
            "[data-automation-id*='visual']:has-text('Supply')",
            "[data-automation-id*='visual']:has-text('Demand')",
            # Look for pivot tables or charts containing supply/demand data
            "[class*='pivot']:has-text('Supply')",
            "[class*='table']:has-text('Supply')"
        ]
        
        for selector in chart_selectors:
            try:
                charts = page.locator(selector).all()
                for chart in charts:
                    if chart.is_visible():
                        text_content = chart.inner_text().lower()
                        if "supply" in text_content and "demand" in text_content:
                            # Make sure it's not the map (exclude map-related content)
                            if "map" not in text_content and "cart" not in text_content:
                                print(f"✅ Found Supply & Demand chart!")
                                supply_demand_chart = chart
                                break
                if supply_demand_chart:
                    break
            except:
                continue
        
        # Alternative: Look for visual containers and check their content more broadly
        if not supply_demand_chart:
            print("🔍 Alternative search: Looking through all visual containers...")
            visual_containers = page.locator("[class*='visual'], [data-testid*='visual'], [data-automation-id*='visual']").all()
            
            for container in visual_containers:
                try:
                    if container.is_visible():
                        text_content = container.inner_text().lower()
                        # Look for Supply & Demand content that's not a map
                        if ("supply" in text_content and "demand" in text_content and 
                            "map" not in text_content and "cart" not in text_content):
                            print(f"✅ Found Supply & Demand chart (alternative method)!")
                            supply_demand_chart = container
                            break
                except:
                    continue
        
        if not supply_demand_chart:
            print("❌ Could not find Supply & Demand chart")
            print("Available text content on page:")
            # Show some text content for debugging
            text_elements = page.locator("*").all()
            for i, element in enumerate(text_elements[:20]):
                try:
                    text = element.inner_text().strip()
                    if text and len(text) > 10 and len(text) < 100:
                        if "supply" in text.lower() or "demand" in text.lower():
                            print(f"  - {text}")
                except:
                    pass
            return
        
        # Step 2: Find the 3-dots menu button in the Supply & Demand chart
        print("\n📋 Step 2: Looking for 3-dots menu in Supply & Demand chart...")
        
        menu_button = None
        
        # Look for the 3-dots menu button within the chart container
        menu_selectors = [
            # Common QuickSight menu button patterns
            "button[data-automation-id*='dropdown_menu']",
            "button[data-automation-id*='visual_dropdown']", 
            "button[data-automation-id*='menu']",
            "button[aria-label*='menu' i]",
            "button[aria-label*='options' i]",
            "button[title*='menu' i]",
            "button[title*='options' i]",
            # Look for buttons with 3 dots or similar symbols
            "button:has-text('⋮')",
            "button:has-text('...')",
            "button:has-text('︙')",
            # Generic menu buttons in the chart area
            "button[class*='menu']",
            "button[class*='dropdown']"
        ]
        
        for selector in menu_selectors:
            try:
                buttons = supply_demand_chart.locator(selector).all()
                for button in buttons:
                    if button.is_visible():
                        aria_label = button.get_attribute("aria-label") or ""
                        title = button.get_attribute("title") or ""
                        data_id = button.get_attribute("data-automation-id") or ""
                        
                        # Look for menu-related attributes but exclude global menus
                        if (("menu" in aria_label.lower() or "menu" in title.lower() or 
                             "options" in aria_label.lower() or "options" in title.lower() or
                             "dropdown" in data_id.lower()) and 
                            "global" not in data_id.lower() and "help" not in data_id.lower()):
                            print(f"✅ Found 3-dots menu button!")
                            print(f"   aria-label: '{aria_label}'")
                            print(f"   title: '{title}'")
                            print(f"   data-automation-id: '{data_id}'")
                            menu_button = button
                            break
                if menu_button:
                    break
            except:
                continue
        
        # Fallback: Look for any button in the chart that might be a menu
        if not menu_button:
            print("🔍 Fallback: Looking for any menu-like buttons in chart...")
            all_buttons = supply_demand_chart.locator("button").all()
            for button in all_buttons:
                try:
                    if button.is_visible():
                        # Check if it looks like a menu button
                        aria_label = button.get_attribute("aria-label") or ""
                        title = button.get_attribute("title") or ""
                        class_name = button.get_attribute("class") or ""
                        
                        if (aria_label or title) and not any(x in (aria_label + title).lower() for x in ["close", "minimize", "maximize"]):
                            print(f"Found potential menu button: aria-label='{aria_label}', title='{title}'")
                            menu_button = button
                            break
                except:
                    continue
        
        if not menu_button:
            print("❌ Could not find 3-dots menu button in Supply & Demand chart")
            return
        
        # Step 3: Click the 3-dots menu button
        print("\n📋 Step 3: Clicking the 3-dots menu...")
        
        try:
            # Wait for any overlays to disappear
            page.wait_for_timeout(1000)
            
            # Click the menu button
            menu_button.click(timeout=5000)
            print("✅ Clicked 3-dots menu button")
            
            # Wait for dropdown to appear
            page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"❌ Failed to click menu button: {e}")
            return
        
        # Step 4: Look for "Export to CSV" in the dropdown
        print("\n📋 Step 4: Looking for 'Export to CSV' option...")
        
        export_option = None
        
        # Look for the Export to CSV option
        export_selectors = [
            "text=Export to CSV",
            "[role='menuitem']:has-text('Export to CSV')",
            "[role='menuitem']:has-text('Export')",
            "li:has-text('Export to CSV')",
            "div:has-text('Export to CSV')",
            "button:has-text('Export to CSV')",
            "a:has-text('Export to CSV')",
            # More generic selectors
            "*:has-text('Export to CSV')",
            "*:has-text('Export')"
        ]
        
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
            print("Available dropdown options:")
            # Show what's in the dropdown for debugging
            try:
                dropdown_items = page.locator("[role='menuitem'], li, div, button, a").all()
                for item in dropdown_items[:10]:
                    try:
                        if item.is_visible():
                            text = item.inner_text().strip()
                            if text and len(text) < 50:
                                print(f"  - '{text}'")
                    except:
                        pass
            except:
                pass
            return
        
        # Step 5: Click "Export to CSV"
        print("\n📋 Step 5: Clicking 'Export to CSV'...")
        
        try:
            export_option.click(timeout=5000)
            print("✅ Clicked 'Export to CSV'!")
            
            # Wait for download to start
            page.wait_for_timeout(3000)
            
            # Look for download completion indicators
            success_indicators = [
                "text=/csv.*ready/i",
                "text=/export.*complete/i",
                "text=/download.*complete/i",
                "text=/successfully.*exported/i",
                "[class*='success']",
                "[class*='notification']"
            ]
            
            download_success = False
            for indicator in success_indicators:
                try:
                    element = page.locator(indicator).first
                    if element.count() > 0 and element.is_visible():
                        text = element.inner_text()
                        print(f"✅ Download success indicator: '{text}'")
                        download_success = True
                        break
                except:
                    pass
            
            if download_success:
                print("\n🎉 SUCCESS! Supply & Demand CSV export completed!")
                print("📁 Check your Downloads folder for the CSV file")
            else:
                print("\n⚠️ Export initiated, but no completion indicator found")
                print("📁 Check your Downloads folder - the file might still be downloading")
            
        except Exception as e:
            print(f"❌ Failed to click Export to CSV: {e}")
            return
    
    except Exception as e:
        print(f"❌ Error during automation: {e}")
        print("The automation encountered an unexpected error.")
    
    # Keep browser open for verification
    print("\n" + "="*60)
    print("✅ Automation completed!")
    print("Browser will stay open for verification.")
    print("="*60)


def run_download():
    """Function to be called from the GUI application"""
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    run_download() 
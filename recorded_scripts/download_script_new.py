import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    print("Connecting to your authenticated Chrome browser...")
    
    # Connect to existing Chrome browser instead of launching new one
    try:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        print("Successfully connected to existing Chrome!")
        
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
                        print("Using existing QuickSight page")
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
        print(f"Could not connect to existing Chrome: {e}")
        print("Make sure Chrome is running with --remote-debugging-port=9222")
        return
    
    # Navigate to QuickSight dashboard if not already there
    current_url = page.url
    quicksight_url = "https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/dashboards/855adf29-7e31-4755-960f-cf99f0fc7e6a"
    
    if "quicksight" not in current_url.lower():
        print(f"Navigating from {current_url} to QuickSight...")
        page.goto(quicksight_url)
    else:
        print(f"Already on QuickSight page: {current_url}")
    
    # Wait for page to load
    page.wait_for_load_state('networkidle')
    print("Page loaded successfully!")
    
    # Wait a bit more for dynamic content
    page.wait_for_timeout(3000)
    
    print("\n" + "="*50)
    print("STARTING AUTOMATED DOWNLOAD!")
    print("="*50)
    
    try:
        print("==================================================")
        print("🚀 AUTOMATED SUPPLY & DEMAND EXPORT!")
        print("==================================================")
        print("Based on the interactive recording, I'll now automate the full process:")
        print("1. Click the Maximize button for Supply & Demand")
        print("2. Look for the 3-dots menu in maximized view")
        print("3. Click Export to CSV")
        print()
        
        # Step 1: Find the Supply & Demand chart (based on manual user instructions)
        print("📋 Step 1: Looking for Supply & Demand chart specifically...")
        print("(Based on user instructions: 3-dots menu is top-right of Supply & Demand chart)")
        
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
        
        # Now look for the 3-dots menu button within the Supply & Demand chart
        menu_button = None
        if supply_demand_chart:
            print("🔍 Looking for 3-dots menu in Supply & Demand chart...")
            
            # Look for the 3-dots menu button within the chart container
            menu_selectors = [
                # Common QuickSight menu button patterns
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
        
        if menu_button:
            print("🔍 Clicking the 3-dots menu button...")
            
            # Wait for any toast notifications to disappear
            try:
                toast_overlay = page.locator(".toasts-list, [class*='toast']").first
                if toast_overlay.is_visible():
                    print("⏳ Waiting for toast notification to disappear...")
                    page.wait_for_timeout(3000)  # Wait for toast to auto-dismiss
            except:
                pass
            
            # Try multiple click strategies
            click_successful = False
            
            # Strategy 1: Normal click
            try:
                menu_button.click(timeout=5000)
                click_successful = True
                print("✅ Clicked menu button (normal click)")
            except Exception as e:
                print(f"⚠️ Normal click failed: {e}")
            
            # Strategy 2: Force click if normal click failed
            if not click_successful:
                try:
                    print("🔄 Trying force click...")
                    menu_button.click(force=True, timeout=5000)
                    click_successful = True
                    print("✅ Clicked menu button (force click)")
                except Exception as e:
                    print(f"⚠️ Force click failed: {e}")
            
            # Strategy 3: JavaScript click if force click failed
            if not click_successful:
                try:
                    print("🔄 Trying JavaScript click...")
                    page.evaluate("document.querySelector('button[data-automation-id=\"analysis_visual_dropdown_menu_button\"]').click()")
                    click_successful = True
                    print("✅ Clicked menu button (JavaScript click)")
                except Exception as e:
                    print(f"⚠️ JavaScript click failed: {e}")
            
            if click_successful:
                page.wait_for_timeout(1500)  # Wait for dropdown menu
            
            # Step 3: Look for Export to CSV option
            print("\n📋 Step 3: Looking for Export to CSV option...")
            
            export_selectors = [
                "text=Export to CSV",
                "text=Export",
                "[role='menuitem']:has-text('Export')",
                "[role='menuitem']:has-text('CSV')",
                "li:has-text('Export')",
                "div:has-text('Export to CSV')",
                "button:has-text('Export')"
            ]
            
            export_option = None
            for selector in export_selectors:
                try:
                    option = page.locator(selector).first
                    if option.count() > 0 and option.is_visible():
                        print(f"✅ Found export option: {selector}")
                        export_option = option
                        break
                except:
                    pass
            
            if export_option:
                print("🔍 Clicking Export to CSV...")
                export_option.click()
                page.wait_for_timeout(3000)  # Wait for download
                print("✅ Clicked Export to CSV!")
                
                # Check for download indicators
                page.wait_for_timeout(2000)
                download_found = False
                try:
                    export_indicator = page.locator("text=/exported/i").first
                    if export_indicator.is_visible():
                        print("🎉 SUCCESS! Download completed!")
                        print("📁 CSV file should be in your Downloads folder")
                        download_found = True
                except:
                    pass
                
                if not download_found:
                    print("⚠️  Export clicked, but no download confirmation seen")
                    print("📁 Check your Downloads folder - file might still be downloading")
                    
            else:
                print("❌ Could not find Export to CSV option")
                print("🔍 Available menu options:")
                # Show what's in the dropdown
                menu_items = page.locator("[role='menuitem'], li, div, button").all()
                for item in menu_items[:10]:
                    try:
                        text = item.inner_text().strip()
                        if text and len(text) < 100:
                            print(f"  - {text}")
                    except:
                        pass
        else:
            print("❌ Could not find Supply & Demand table menu button")
            
            # Try dashboard-level export as a fallback
            print("\n🔍 Trying dashboard-level Export button as fallback...")
            dashboard_export = page.locator("button[aria-label='Export']").first
            if dashboard_export.count() > 0 and dashboard_export.is_visible():
                print("✅ Found dashboard Export button!")
                try:
                    # Click the export button
                    dashboard_export.click()
                    print("🔄 Clicked Export button, waiting for download...")
                    
                    # Wait longer for download to complete (some exports take time)
                    page.wait_for_timeout(5000)
                    
                    # Check for download completion indicators
                    download_indicators = [
                        "text=/download.*complete/i",
                        "text=/export.*complete/i", 
                        "text=/file.*ready/i",
                        "text=/successfully.*exported/i",
                        "[class*='success']",
                        "[class*='notification']"
                    ]
                    
                    download_found = False
                    for indicator in download_indicators:
                        try:
                            element = page.locator(indicator).first
                            if element.count() > 0 and element.is_visible():
                                text = element.inner_text()
                                print(f"✅ Download indicator found: '{text}'")
                                download_found = True
                                break
                        except:
                            pass
                    
                    if download_found:
                        print("🎉 SUCCESS! Export completed successfully!")
                        print("📁 Check your Downloads folder for the exported file")
                    else:
                        print("⚠️ Export button clicked, but no completion indicator found")
                        print("📁 The file might still be downloading - check your Downloads folder")
                    
                    return
                    
                except Exception as e:
                    print(f"❌ Error with dashboard export: {e}")
            else:
                print("❌ No dashboard Export button found either")
            
            # Show available buttons for debugging
            print("🔍 Let me show available buttons:")
            all_buttons = page.locator("button").all()
            visible_buttons = []
            for i, button in enumerate(all_buttons):
                try:
                    if button.is_visible():
                        aria_label = button.get_attribute("aria-label") or ""
                        title = button.get_attribute("title") or ""
                        if aria_label or title:
                            visible_buttons.append(f"  {len(visible_buttons)+1}. aria-label: '{aria_label}' | title: '{title}'")
                except:
                    pass
            
            print(f"Found {len(visible_buttons)} visible buttons with labels:")
            for btn_info in visible_buttons[:15]:
                print(btn_info)
            return
    
    except Exception as e:
        print(f"❌ Error during automation: {e}")
        print("You can try manually performing the download.")

    # Keep browser open for verification
    print("\nAutomation completed. Browser will stay open for verification.")
    print("Press Enter to close this automation script...")
    input()


def run_download():
    """Function to be called from the GUI application"""
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    run_download()

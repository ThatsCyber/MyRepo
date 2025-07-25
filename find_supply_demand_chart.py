from playwright.sync_api import sync_playwright

def find_supply_demand_chart():
    """Find the specific Supply & Demand chart and its menu button"""
    
    with sync_playwright() as playwright:
        try:
            # Connect to existing Chrome
            browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
            contexts = browser.contexts
            
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    page = pages[0]
                    print(f"Connected to page: {page.url}")
                    
                    print("\n" + "="*60)
                    print("🔍 FINDING: Supply & Demand Chart Specifically")
                    print("="*60)
                    
                    # 1. Look for text elements that contain both "Supply" and "Demand"
                    print("\n1. Looking for chart titles with 'Supply' and 'Demand'...")
                    
                    # Look for various title elements
                    title_selectors = [
                        "*:has-text('Supply') *:has-text('Demand')",
                        "text=/supply.*demand/i",
                        "[class*='title']:has-text('Supply')",
                        "[class*='header']:has-text('Supply')",
                        "h1, h2, h3, h4, h5, h6",  # Check all headings
                    ]
                    
                    supply_demand_elements = []
                    for selector in title_selectors:
                        try:
                            elements = page.locator(selector).all()
                            for element in elements:
                                try:
                                    text = element.inner_text().strip()
                                    if "supply" in text.lower() and "demand" in text.lower():
                                        bbox = element.bounding_box()
                                        supply_demand_elements.append({
                                            'element': element,
                                            'text': text,
                                            'bbox': bbox,
                                            'selector': selector
                                        })
                                        print(f"   Found: '{text}' at {bbox}")
                                except:
                                    pass
                        except:
                            pass
                    
                    # 2. For each Supply & Demand element, look for nearby menu buttons
                    print(f"\n2. Found {len(supply_demand_elements)} Supply & Demand elements, checking for nearby menu buttons...")
                    
                    chart_menu_button = None
                    
                    for i, item in enumerate(supply_demand_elements):
                        element = item['element']
                        text = item['text']
                        print(f"\n   [{i}] Checking element: '{text}'")
                        
                        # Look for menu buttons in the same container or nearby
                        menu_searches = [
                            # Look in parent containers
                            "xpath=ancestor::*[1]//button[contains(@data-automation-id, 'menu')]",
                            "xpath=ancestor::*[2]//button[contains(@data-automation-id, 'menu')]", 
                            "xpath=ancestor::*[3]//button[contains(@data-automation-id, 'menu')]",
                            # Look for siblings
                            "xpath=following-sibling::*//button[contains(@data-automation-id, 'menu')]",
                            "xpath=preceding-sibling::*//button[contains(@data-automation-id, 'menu')]",
                            # Look in the general area (broader search)
                            "xpath=ancestor-or-self::*//button[contains(@data-automation-id, 'visual_dropdown_menu')]"
                        ]
                        
                        for search in menu_searches:
                            try:
                                nearby_buttons = element.locator(search).all()
                                for btn in nearby_buttons:
                                    if btn.is_visible():
                                        aria_label = btn.get_attribute("aria-label") or ""
                                        title = btn.get_attribute("title") or ""
                                        data_id = btn.get_attribute("data-automation-id") or ""
                                        btn_bbox = btn.bounding_box()
                                        
                                        print(f"     Found menu button at {btn_bbox}:")
                                        print(f"       aria-label: '{aria_label}'")
                                        print(f"       title: '{title}'")
                                        print(f"       data-automation-id: '{data_id}'")
                                        
                                        # Check if this looks like a chart menu (not dashboard menu)
                                        if "visual_dropdown_menu" in data_id and "analysis" in data_id:
                                            print(f"     ✅ This looks like a chart-specific menu!")
                                            chart_menu_button = btn
                                            break
                            except Exception as e:
                                print(f"     Error searching with {search}: {e}")
                        
                        if chart_menu_button:
                            break
                    
                    # 3. If we found a chart menu button, test clicking it
                    if chart_menu_button:
                        print(f"\n3. Testing the chart menu button...")
                        chart_menu_button.click()
                        page.wait_for_timeout(2000)
                        
                        print("\n4. Looking for export options in chart menu...")
                        export_options = page.locator("text=Export, text=/export.*csv/i, [role='menuitem']:has-text('Export')").all()
                        
                        print("Available options after clicking chart menu:")
                        for option in export_options:
                            try:
                                if option.is_visible():
                                    text = option.inner_text()
                                    print(f"   - {text}")
                            except:
                                pass
                        
                        # Look specifically for CSV export
                        csv_export = page.locator("text=Export to CSV, text=/export.*csv/i").first
                        if csv_export.count() > 0 and csv_export.is_visible():
                            print(f"\n✅ Found CSV export option!")
                            print("This is the correct target for the automation!")
                        else:
                            print(f"\n❌ No CSV export found in this menu")
                    
                    else:
                        print("\n❌ Could not find a chart-specific menu button for Supply & Demand")
                        
                        # Fallback: show all visual menu buttons
                        print("\nAll visual menu buttons on page:")
                        all_visual_menus = page.locator("button[data-automation-id*='visual_dropdown_menu']").all()
                        for i, btn in enumerate(all_visual_menus):
                            try:
                                if btn.is_visible():
                                    aria_label = btn.get_attribute("aria-label") or ""
                                    bbox = btn.bounding_box()
                                    print(f"   [{i}] Visual menu at {bbox}: '{aria_label[:50]}...'")
                            except:
                                pass
                    
                    print("\n" + "="*60)
                    print("Chart-specific search complete!")
                    print("="*60)
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    find_supply_demand_chart() 
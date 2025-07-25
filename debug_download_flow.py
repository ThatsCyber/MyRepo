from playwright.sync_api import sync_playwright

def debug_download_flow():
    """Debug script to trace the exact download flow and see what's being clicked"""
    
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
                    print("🔍 DEBUGGING: What is the automation actually clicking?")
                    print("="*60)
                    
                    # 1. First, let's see what menu buttons are currently visible and their exact details
                    print("\n1. All visible menu buttons on the page:")
                    menu_buttons = page.locator("button[data-automation-id*='menu'], button[aria-label*='menu'], button[title*='menu']").all()
                    for i, btn in enumerate(menu_buttons):
                        try:
                            if btn.is_visible():
                                aria_label = btn.get_attribute("aria-label") or ""
                                title = btn.get_attribute("title") or ""
                                data_id = btn.get_attribute("data-automation-id") or ""
                                # Get the bounding box to see location
                                bbox = btn.bounding_box()
                                print(f"   [{i}] Button at {bbox}:")
                                print(f"       aria-label: '{aria_label}'")
                                print(f"       title: '{title}'")
                                print(f"       data-automation-id: '{data_id}'")
                                print()
                        except Exception as e:
                            print(f"   [{i}] Error getting button info: {e}")
                    
                    # 2. Let's simulate our current selector logic
                    print("\n2. Testing our current selectors:")
                    menu_selectors = [
                        "button[data-automation-id='analysis_visual_dropdown_menu_button'][aria-label*='Carts Map']",
                        "button[data-automation-id='analysis_visual_dropdown_menu_button'][aria-label*='Menu options'][aria-label*='Carts']",
                        "button[aria-label*='Menu options'][aria-label*='Carts Map']",
                        "button[title='Menu options'][aria-label*='Carts']",
                        "button[data-automation-id='analysis_visual_dropdown_menu_button'][aria-label*='filter']",
                        "button[data-automation-id='analysis_visual_dropdown_menu_button'][aria-label*='map']"
                    ]
                    
                    found_button = None
                    for selector in menu_selectors:
                        try:
                            button = page.locator(selector).first
                            if button.count() > 0 and button.is_visible():
                                print(f"✅ Selector matched: {selector}")
                                aria_label = button.get_attribute("aria-label")
                                title = button.get_attribute("title")
                                data_id = button.get_attribute("data-automation-id")
                                print(f"   aria-label: '{aria_label}'")
                                print(f"   title: '{title}'")
                                print(f"   data-automation-id: '{data_id}'")
                                found_button = button
                                break
                            else:
                                print(f"❌ No match for: {selector}")
                        except Exception as e:
                            print(f"❌ Error with selector {selector}: {e}")
                    
                    if not found_button:
                        print("\n⚠️  No button found with our selectors, checking fallback logic...")
                        
                        all_buttons = page.locator("button").all()
                        for i, button in enumerate(all_buttons):
                            try:
                                if button.is_visible():
                                    aria_label = button.get_attribute("aria-label") or ""
                                    title = button.get_attribute("title") or ""
                                    data_automation_id = button.get_attribute("data-automation-id") or ""
                                    
                                    # Skip global help menu
                                    if "global_help_menu" in data_automation_id:
                                        print(f"   [{i}] Skipping global help menu")
                                        continue
                                    
                                    # Look for chart-specific menu buttons
                                    if ("menu" in aria_label.lower() or "menu" in title.lower()) and \
                                       ("carts" in aria_label.lower() or "map" in aria_label.lower() or "analysis_visual" in data_automation_id):
                                        print(f"   [{i}] Fallback found potential match:")
                                        print(f"       aria-label: '{aria_label}'")
                                        print(f"       title: '{title}'")
                                        print(f"       data-automation-id: '{data_automation_id}'")
                                        found_button = button
                                        break
                            except:
                                pass
                    
                    # 3. If we found a button, let's click it and see what dropdown appears
                    if found_button:
                        print(f"\n3. Clicking the found button...")
                        found_button.click()
                        page.wait_for_timeout(2000)  # Wait for dropdown
                        
                        print("\n4. Looking for dropdown menu items...")
                        # Look for all visible menu items after clicking
                        menu_items = page.locator("[role='menuitem'], li, div, button").all()
                        visible_items = []
                        for item in menu_items:
                            try:
                                if item.is_visible():
                                    text = item.inner_text().strip()
                                    if text and len(text) < 100:
                                        visible_items.append(text)
                            except:
                                pass
                        
                        print("Available menu options:")
                        for i, item in enumerate(visible_items[:15]):  # Show first 15
                            print(f"   [{i}] {item}")
                        
                        print(f"\n5. Looking specifically for Export options...")
                        export_selectors = [
                            "text=Export to CSV",
                            "text=Export",
                            "[role='menuitem']:has-text('Export')",
                            "[role='menuitem']:has-text('CSV')",
                            "li:has-text('Export')",
                            "div:has-text('Export to CSV')",
                            "button:has-text('Export')"
                        ]
                        
                        for selector in export_selectors:
                            try:
                                option = page.locator(selector).first
                                if option.count() > 0 and option.is_visible():
                                    text = option.inner_text()
                                    print(f"✅ Found export option with '{selector}': '{text}'")
                                    print("   This is what the automation would click!")
                                    break
                                else:
                                    print(f"❌ No match for: {selector}")
                            except Exception as e:
                                print(f"❌ Error with export selector {selector}: {e}")
                    
                    else:
                        print("\n❌ No suitable menu button found!")
                    
                    print("\n" + "="*60)
                    print("Debug complete! This shows exactly what the automation is targeting.")
                    print("="*60)
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_download_flow() 
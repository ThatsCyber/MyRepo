from playwright.sync_api import sync_playwright

def debug_page_elements():
    """Debug script to find the correct Supply & Demand selectors"""
    
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
                    print("🔍 DEBUGGING: Finding Supply & Demand Elements")
                    print("="*60)
                    
                    # 1. Look for all text that contains "Supply" and "Demand"
                    print("\n1. Looking for text containing 'Supply' and 'Demand'...")
                    supply_demand_texts = page.locator("text=/supply.*demand/i").all()
                    for i, element in enumerate(supply_demand_texts):
                        try:
                            text = element.inner_text()
                            print(f"   [{i}] Text: '{text}'")
                        except:
                            pass
                    
                    # 2. Look for all charts/widgets
                    print("\n2. Looking for chart containers...")
                    chart_containers = page.locator("[data-automation-id*='visual'], .visual-container, [class*='chart'], [class*='visual']").all()
                    for i, container in enumerate(chart_containers):
                        try:
                            # Check if this container has Supply & Demand text
                            text_content = container.inner_text()
                            if "supply" in text_content.lower() and "demand" in text_content.lower():
                                print(f"   [{i}] Found Supply & Demand container!")
                                print(f"       Text preview: {text_content[:100]}...")
                                
                                # Look for menu button in this container
                                menu_buttons = container.locator("button[data-automation-id*='menu'], button[aria-label*='menu'], button[title*='menu']").all()
                                for j, btn in enumerate(menu_buttons):
                                    try:
                                        aria_label = btn.get_attribute("aria-label")
                                        title = btn.get_attribute("title")
                                        print(f"       Menu button [{j}]: aria-label='{aria_label}', title='{title}'")
                                    except:
                                        pass
                        except:
                            pass
                    
                    # 3. Look for all menu buttons and check their parent context
                    print("\n3. Looking for all menu buttons...")
                    all_menu_buttons = page.locator("button[data-automation-id*='menu'], button[aria-label*='menu']").all()
                    for i, btn in enumerate(all_menu_buttons):
                        try:
                            aria_label = btn.get_attribute("aria-label") or ""
                            title = btn.get_attribute("title") or ""
                            
                            # Check parent context for Supply & Demand
                            parent = btn.locator("xpath=ancestor::*[contains(., 'Supply') and contains(., 'Demand')][1]")
                            if parent.count() > 0:
                                print(f"   [{i}] SUPPLY & DEMAND MENU FOUND!")
                                print(f"       aria-label: '{aria_label}'")
                                print(f"       title: '{title}'")
                                print(f"       data-automation-id: {btn.get_attribute('data-automation-id')}")
                        except:
                            pass
                    
                    # 4. Look for the specific chart title
                    print("\n4. Looking for chart titles...")
                    titles = page.locator("h1, h2, h3, h4, .chart-title, [class*='title']").all()
                    for i, title_elem in enumerate(titles):
                        try:
                            text = title_elem.inner_text()
                            if "supply" in text.lower() and "demand" in text.lower():
                                print(f"   [{i}] Found title: '{text}'")
                                
                                # Look for menu button near this title
                                nearby_menu = title_elem.locator("xpath=following-sibling::*//button[contains(@data-automation-id, 'menu')] | xpath=parent::*//button[contains(@data-automation-id, 'menu')]").first
                                if nearby_menu.count() > 0:
                                    print(f"       Found nearby menu button!")
                        except:
                            pass
                    
                    print("\n" + "="*60)
                    print("Debug complete! Check the output above for the correct selectors.")
                    print("="*60)
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_page_elements() 
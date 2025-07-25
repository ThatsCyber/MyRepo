from playwright.sync_api import sync_playwright

def debug_export_menu():
    """Debug what appears when we click the Export button"""
    
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
                    print("🔍 DEBUG: What happens when we click Export?")
                    print("="*60)
                    
                    # Click the Export button
                    export_button = page.locator("button[aria-label='Export']").first
                    if export_button.count() > 0 and export_button.is_visible():
                        print("✅ Found Export button, clicking it...")
                        export_button.click()
                        page.wait_for_timeout(2000)
                        
                        print("\n1. Looking for ANY visible text after clicking Export...")
                        # Look for all visible elements that appeared
                        all_elements = page.locator("*").all()
                        new_texts = []
                        for element in all_elements:
                            try:
                                if element.is_visible():
                                    text = element.inner_text().strip()
                                    if text and len(text) < 200 and "export" in text.lower():
                                        new_texts.append(text)
                            except:
                                pass
                        
                        print("Export-related text found:")
                        for text in list(set(new_texts))[:10]:  # Convert set to list first
                            print(f"   - {text}")
                        
                        print("\n2. Looking for menu items, dialogs, dropdowns...")
                        # Look for various UI elements that might contain export options
                        ui_selectors = [
                            "[role='menu']",
                            "[role='menuitem']", 
                            "[role='dialog']",
                            "[class*='dropdown']",
                            "[class*='menu']",
                            "[class*='modal']",
                            "li",
                            "button",
                        ]
                        
                        for selector in ui_selectors:
                            try:
                                elements = page.locator(selector).all()
                                for element in elements:
                                    if element.is_visible():
                                        text = element.inner_text().strip()
                                        if text and ("csv" in text.lower() or "export" in text.lower()):
                                            print(f"   Found {selector}: '{text}'")
                            except:
                                pass
                        
                        print("\n3. Taking screenshot of current state...")
                        # Take a screenshot to see what's on screen
                        try:
                            page.screenshot(path="export_menu_debug.png")
                            print("✅ Screenshot saved as export_menu_debug.png")
                        except:
                            print("❌ Could not take screenshot")
                        
                        print("\n4. Looking for recently appeared elements...")
                        # Wait a bit more and look for elements that might have appeared
                        page.wait_for_timeout(1000)
                        
                        # Try more specific export selectors
                        export_selectors = [
                            "*:has-text('CSV')",
                            "*:has-text('Export to CSV')",
                            "*:has-text('Download')",
                            "*:has-text('Excel')",
                            "button:has-text('Export')",
                            "a:has-text('Export')",
                        ]
                        
                        for selector in export_selectors:
                            try:
                                elements = page.locator(selector).all()
                                for element in elements:
                                    if element.is_visible():
                                        text = element.inner_text().strip()
                                        tag = element.evaluate("el => el.tagName")
                                        print(f"   Found {tag} with '{selector}': '{text}'")
                            except:
                                pass
                    
                    else:
                        print("❌ No Export button found")
                    
                    print("\n" + "="*60)
                    print("Export debug complete!")
                    print("="*60)
                    
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    debug_export_menu() 
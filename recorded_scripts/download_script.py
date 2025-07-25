import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    print("Attempting to connect to existing Chrome browser...")
    
    # First, check if Chrome is running with debugging port
    import requests
    try:
        response = requests.get("http://localhost:9222/json/version", timeout=5)
        print(f"Chrome debugging info: {response.json()}")
        chrome_available = True
    except Exception as e:
        print(f"Chrome debugging port not available: {e}")
        chrome_available = False
    
    if chrome_available:
        try:
            print("Connecting to existing Chrome via CDP...")
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
                    # Look for a page that might be QuickSight or use the first one
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
            print(f"Failed to connect to existing Chrome: {e}")
            print("This means Chrome is not running with --remote-debugging-port=9222")
            print("Please run Chrome with: chrome.exe --remote-debugging-port=9222")
            return  # Don't fall back to new browser, force user to set up Chrome properly
    else:
        print("Chrome debugging port not available.")
        print("Please run Chrome with: chrome.exe --remote-debugging-port=9222 --user-data-dir=\"%USERPROFILE%\\AppData\\Local\\Google\\Chrome\\User Data\"")
        return  # Don't fall back to new browser
    
    # Navigate to QuickSight dashboard instead of auth page
    quicksight_url = "https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/dashboards/855adf29-7e31-4755-960f-cf99f0fc7e6a"
    
    # Check if we're already on the right page
    current_url = page.url
    if "quicksight" not in current_url.lower():
        print(f"Navigating from {current_url} to QuickSight...")
        page.goto(quicksight_url)
    else:
        print(f"Already on QuickSight page: {current_url}")
    
    # Wait for page to load
    page.wait_for_load_state('networkidle')
    print("Page loaded successfully!")
    
    # Wait a bit more for dynamic content to load
    page.wait_for_timeout(3000)
    
    try:
        print("Looking for Supply & Demand 3-dots menu...")
        
        # Look for the 3-dots menu button (using multiple possible selectors)
        menu_selectors = [
            "[data-testid*='menu']",
            "[aria-label*='menu']", 
            "button[data-testid*='visual-menu']",
            "[id*='VISUAL-MENU']",
            "button:has-text('⋮')",
            "button:has-text('...')"
        ]
        
        menu_button = None
        for selector in menu_selectors:
            try:
                menu_button = page.locator(selector).first
                if menu_button.is_visible():
                    print(f"Found menu button with selector: {selector}")
                    break
            except:
                continue
        
        if menu_button and menu_button.is_visible():
            print("Clicking menu button...")
            menu_button.click()
            
            # Wait for menu to appear
            page.wait_for_timeout(1000)
            
            print("Looking for Export to CSV option...")
            
            # Look for Export to CSV option
            export_selectors = [
                "text=Export to CSV",
                "text=Export",
                "[aria-label*='Export']",
                "li:has-text('Export')",
                "div:has-text('Export to CSV')"
            ]
            
            export_button = None
            for selector in export_selectors:
                try:
                    export_button = page.locator(selector).first
                    if export_button.is_visible():
                        print(f"Found export button with selector: {selector}")
                        break
                except:
                    continue
            
            if export_button and export_button.is_visible():
                print("Clicking Export to CSV...")
                export_button.click()
                
                # Wait for download to start
                page.wait_for_timeout(3000)
                print("Download should have started! Check your Downloads folder.")
                
            else:
                print("Could not find Export to CSV option. Available options:")
                menu_items = page.locator("li, div, button").all()
                for item in menu_items[:10]:  # Show first 10 items
                    try:
                        text = item.inner_text()
                        if text and len(text.strip()) > 0:
                            print(f"  - {text.strip()}")
                    except:
                        pass
                        
        else:
            print("Could not find menu button. Let's see what's on the page:")
            # Show available buttons for debugging
            buttons = page.locator("button").all()
            print("Available buttons:")
            for i, button in enumerate(buttons[:10]):  # Show first 10 buttons
                try:
                    text = button.inner_text()
                    attrs = button.get_attribute("data-testid") or button.get_attribute("aria-label") or ""
                    print(f"  {i+1}. {text} | {attrs}")
                except:
                    pass
                    
    except Exception as e:
        print(f"Error during automation: {e}")
        print("You can manually perform the download now.")
    
    # Keep browser open for verification
    print("\nAutomation completed. Browser will stay open for verification.")
    print("Press Enter to close the automation script...")
    input()

    # ---------------------
    # Don't close context/browser if we're connected to existing Chrome
    try:
        if 'connect_over_cdp' not in str(browser):
    context.close()
    browser.close()
    except:
        pass  # Ignore errors when disconnecting from existing Chrome


def run_download():
    """Function to be called from the GUI application"""
with sync_playwright() as playwright:
    run(playwright)


if __name__ == "__main__":
    run_download()

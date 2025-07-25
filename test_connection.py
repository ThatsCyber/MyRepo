from playwright.sync_api import sync_playwright

def test_connection():
    """Test connection to Chrome debugging port"""
    
    with sync_playwright() as playwright:
        try:
            print("Attempting to connect to Chrome...")
            
            # Try localhost first
            try:
                browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
                print("✅ Connected via localhost:9222!")
            except Exception as e1:
                print(f"❌ localhost:9222 failed: {e1}")
                
                # Try 127.0.0.1
                try:
                    browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
                    print("✅ Connected via 127.0.0.1:9222!")
                except Exception as e2:
                    print(f"❌ 127.0.0.1:9222 failed: {e2}")
                    return False
            
            # Test basic functionality
            contexts = browser.contexts
            print(f"Found {len(contexts)} contexts")
            
            if contexts:
                context = contexts[0]
                pages = context.pages
                print(f"Found {len(pages)} pages")
                
                if pages:
                    page = pages[0]
                    print(f"Current page: {page.url}")
                    
                    if "quicksight" in page.url.lower():
                        print("🎯 QuickSight page detected!")
                        return True
                    else:
                        print("⚠️ Not on QuickSight page")
                        return True
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

if __name__ == "__main__":
    test_connection() 
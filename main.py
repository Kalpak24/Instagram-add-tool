import os
import time
from playwright.sync_api import sync_playwright

def main():
    # We use a persistant context so the user doesn't have to log in every time they run the tool.
    # The browser data will be saved in the 'playwright_profile' directory.
    user_data_dir = os.path.join(os.getcwd(), "playwright_profile")
    
    print("Initializing Playwright...")
    with sync_playwright() as p:
        # Launch Chromium. It will keep you logged in between sessions.
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        
        # When persistent context is launched, it usually opens one blank page.
        page = browser.pages[0] if len(browser.pages) > 0 else browser.new_page()
        
        # JavaScript code to inject into the page.
        # This interval runs every 1 second, finds all 'article' (posts), and hides the non-sponsored ones.
        js_code = """
        setInterval(() => {
            const articles = document.querySelectorAll('article');
            articles.forEach(article => {
                const text = article.innerText.toLowerCase();
                // Check if the article contains the word 'sponsored'
                if (!text.includes('sponsored')) {
                    if (article.style.display !== 'none') {
                        article.style.display = 'none';
                    }
                } else {
                    // Optional: Highlight the sponsored post visually
                    if (article.style.border !== '3px solid #E1306C') {
                        article.style.border = '3px solid #E1306C';
                        article.style.borderRadius = '8px';
                        article.style.padding = '5px';
                    }
                }
            });
        }, 1000);
        """
        
        # Inject script so it runs on any newly navigated page
        page.add_init_script(js_code)
        
        print("Opening Instagram...")
        page.goto("https://www.instagram.com/")
        
        # Also evaluate it on the current page immediately
        try:
            page.evaluate(js_code)
        except Exception:
            pass
        
        print("\n=======================================================")
        print(" Instagram Ad Tool is Running!")
        print(" -> Please log in to Instagram if you haven't already.")
        print(" -> Regular posts will be hidden automatically.")
        print(" -> Ads/Sponsored posts will be outlined in Pink.")
        print(" -> KEEP THE BROWSER OPEN.")
        print(" -> Press Ctrl+C in this terminal to STOP.")
        print("=======================================================\n")
        
        # Keep the python script alive as long as the browser is open.
        try:
            while True:
                time.sleep(1)
                # Check if the user closed the browser manually
                if len(browser.pages) == 0:
                    print("Browser closed. Exiting...")
                    break
        except KeyboardInterrupt:
            print("\nStopping tool by user request...")
        
        # Close the browser safely
        browser.close()

if __name__ == "__main__":
    main()

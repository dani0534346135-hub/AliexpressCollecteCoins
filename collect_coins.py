import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. פתיחת דומיין המובייל
        print("Opening AliExpress...")
        driver.get("https://m.aliexpress.com")
        time.sleep(5)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookies to multiple domains...")
            # הזרקה לכמה וריאציות של הדומיין כדי לוודא שזה תופס
            domains = [".aliexpress.com", "m.aliexpress.com", ".m.aliexpress.com"]
            for domain in domains:
                try:
                    driver.add_cookie({
                        'name': 'xman_f',
                        'value': cookie_val.strip(),
                        'path': '/',
                        'domain': domain
                    })
                except:
                    continue
            
            driver.refresh()
            time.sleep(8)

        # 2. ניווט לקישור המדויק שלך
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)
        
        # המתנה ארוכה יותר לטעינת האלמנטים
        time.sleep(25) 
        driver.save_screenshot("after_loading.png")

        # 3. בדיקה אם אנחנו עדיין בדף התחברות
        if "login" in driver.current_url or "Welcome to AliExpress" in driver.page_source:
            print("FAILED: Still on login page. Cookie might be invalid.")
            return

        # 4. לחיצה על כפתור האיסוף
        print("Searching for collect button...")
        result = driver.execute_script("""
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                var text = el.innerText || "";
                if (text.includes('30') || text.includes('Collect') || text.includes('מטבעות')) {
                    el.click();
                    return "Clicked: " + text;
                }
            }
            return "Button not found";
        """)
        print(f"Action Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

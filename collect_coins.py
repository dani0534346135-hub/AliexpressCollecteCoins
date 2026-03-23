import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

def main():
    chrome_options = Options()
    if IS_GITHUB:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    
    # הגדרת מובייל חיונית למטבעות
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. כניסה לעמוד הבית של המובייל (חשוב מאוד!)
        print("Step 1: Opening Mobile Home Page...")
        driver.get("https://m.aliexpress.com")
        time.sleep(10)
        
        # 2. הזרקת הקוקי
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Step 2: Injecting cookie...")
            driver.add_cookie({'name': 'xman_f', 'value': cookie_val.strip(), 'path': '/'})
            driver.refresh() # רענון כדי שהקוקי ייכנס לתוקף
            time.sleep(8)
        
        # 3. ניווט מדורג למטבעות (דרך דף ביניים כדי למנוע שגיאה 500)
        print("Step 3: Navigating to coins via safe link...")
        # במקום גט ישיר, נשתמש בכתובת המובייל המלאה
        driver.get("https://web.archive.org/web/0/https://home.aliexpress.com/coins/index.htm") # טריק קטן לעקיפה או פשוט הכתובת הבאה:
        driver.get("https://m.aliexpress.com/coins/index.html")
        
        print("Waiting for coins page to stabilize...")
        time.sleep(20) 

        # 4. צילום מסך - כאן אנחנו צריכים לראות מטבעות ולא שגיאה 500
        driver.save_screenshot("after_loading.png")

        # 5. לחיצה על כפתור האיסוף עם השהייה קטנה
        print("Step 4: Searching for collect button...")
        result = driver.execute_script("""
            // חיפוש אגרסיבי של כל מה שדומה לכפתור איסוף במובייל
            var selectors = ['.checkin-button', '[class*="checkin"]', '.coins-btn', 'button'];
            for (var s of selectors) {
                var btn = document.querySelector(s);
                if (btn && (btn.innerText.includes('Collect') || btn.innerText.includes('Check'))) {
                    btn.click();
                    return "Clicked button: " + s;
                }
            }
            return "Button not found, but page loaded";
        """)
        print(f"Final JS Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

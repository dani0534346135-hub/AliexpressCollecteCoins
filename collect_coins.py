import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

def main():
    chrome_options = Options()
    if IS_GITHUB:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    
    # הגדרת מובייל למניעת 404/500
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. כניסה לאתר כדי לקבוע הקשר (Context)
        print("Opening AliExpress Mobile...")
        driver.get("https://m.aliexpress.com")
        time.sleep(8)
        
        # 2. הזרקת הקוקי - שים לב: הסרתי את ה-'domain' כדי למנוע את השגיאה
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            try:
                driver.add_cookie({
                    'name': 'xman_f',
                    'value': cookie_val.strip(),
                    'path': '/'
                    # בלי דומיין - סלניום יבחר לבד
                })
                print("Cookie injected successfully.")
            except Exception as e:
                print(f"Failed to inject cookie: {e}")
        
        # 3. מעבר לדף המטבעות
        print("Navigating to coins page...")
        driver.get("https://home.aliexpress.com/coins/index.htm")
        time.sleep(15) 

        # 4. צילום מסך לבדיקה
        driver.save_screenshot("after_loading.png")

        # 5. לחיצה על כפתור האיסוף
        print("Attempting to click collect...")
        clicked = driver.execute_script("""
            var btn = document.querySelector('.checkin-button') || 
                      document.querySelector('[class*="checkin"]') ||
                      document.querySelector('.coins-btn');
            if(btn) {
                btn.click();
                return true;
            }
            return false;
        """)
        
        if clicked:
            print("SUCCESS: Button clicked!")
        else:
            print("Button not found. Checking if already collected...")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

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
    
    # זיוף זהות לטלפון נייד (Nexus 5) כדי למנוע שגיאות 500 ו-404
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; Nexus 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. כניסה לאתר הראשי להזרקת קוקי
        driver.get("https://www.aliexpress.com")
        time.sleep(5)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            driver.add_cookie({'name': 'xman_f', 'value': cookie_val.strip(), 'path': '/', 'domain': '.aliexpress.com'})
        
        # 2. מעבר לדף המטבעות (במובייל זה הקישור היציב)
        print("Navigating to coins page...")
        driver.get("https://home.aliexpress.com/coins/index.htm")
        time.sleep(15) 

        # 3. צילום מסך - כדי לראות אם עקפנו את שגיאה 500
        driver.save_screenshot("step1_page_load.png")

        # 4. ניסיון לחיצה על כפתור האיסוף
        print("Trying to click collect button...")
        result = driver.execute_script("""
            var btn = document.querySelector('.checkin-button') || 
                      document.querySelector('[class*="checkin"]') ||
                      document.querySelector('.coins-btn');
            if(btn) {
                btn.click();
                return "Clicked!";
            }
            return "Button not found";
        """)
        print(f"Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("step2_after_click.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

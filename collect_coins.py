import time
import random
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# בדיקה האם רץ ב-GitHub Actions
IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

def random_sleep(min_s=2, max_s=5):
    time.sleep(random.uniform(min_s, max_s))

def main():
    chrome_options = Options()
    if IS_GITHUB:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. חייבים להיכנס קודם לכתובת המדויקת של הדומיין
      # 1. כניסה לדף הבית
        print("Navigating to AliExpress...")
        driver.get("https://www.aliexpress.com")
        random_sleep(5, 8)

        # 2. הזרקת ה-Cookie
        cookie_val = os.getenv("ALIE_COOKIE")
        if not cookie_val:
            print("Error: ALIE_COOKIE secret is missing!")
            return

        print("Injecting authentication cookie...")
        
        # אנחנו מנסים להוסיף את הקוקי בלי להגדיר דומיין ידנית
        # סלניום יצמיד אותו אוטומטית לדומיין הנוכחי (www.aliexpress.com)
        try:
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'path': '/',
                'domain': '.aliexpress.com' # הגדרה רחבה שתופסת גם תתי דומיינים
            })
            print("Successfully added with domain .aliexpress.com")
        except Exception as e:
            print(f"Failed with .domain, trying without explicit domain: {e}")
            try:
                driver.add_cookie({
                    'name': 'xman_f',
                    'value': cookie_val.strip(),
                    'path': '/'
                })
                print("Successfully added without explicit domain")
            except Exception as e2:
                print(f"Critical error adding cookie: {e2}")
                return

        # 3. רענון ומעבר לעמוד המטבעות
        print("Refreshing and navigating to coins page...")
        driver.refresh()
        random_sleep(5, 8)
        driver.get("https://coins.aliexpress.com")
        random_sleep(10, 15)
        # 5. ניסיון ללחוץ על כפתור האיסוף
        try:
            wait = WebDriverWait(driver, 20)
            # מחפש כפתור שמכיל את המילה Collect או כפתור צ'ק-אין
            collect_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'checkin-button')] | //span[contains(text(), 'Collect')]")))
            collect_btn.click()
            print("SUCCESS: Coins collected successfully!")
        except Exception as e:
            print(f"Could not find collect button. Check if already collected today. Error: {e}")
            if IS_GITHUB:
                driver.save_screenshot("check_page.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

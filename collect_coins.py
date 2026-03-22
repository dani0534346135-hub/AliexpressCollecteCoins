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
        print("Navigating to AliExpress to set domain context...")
        driver.get("https://www.aliexpress.com")
        random_sleep(5, 8) # נותנים לדף להיטען היטב

        # 2. הזרקת ה-Cookie
        cookie_val = os.getenv("ALIE_COOKIE")
        if not cookie_val:
            print("Error: ALIE_COOKIE secret is missing!")
            return

        print("Injecting authentication cookie...")
        # הסרנו את הנקודה לפני aliexpress.com במידה וזה מה שגרם ל-Mismatch
        # והוספנו ניקוי לרווחים
        driver.add_cookie({
            'name': 'xman_f',
            'value': cookie_val.strip(),
            'domain': 'www.aliexpress.com', # שינוי כאן ל-www
            'path': '/'
        })

        # 3. ניסיון נוסף עם דומיין כללי אם הראשון נכשל (אופציונלי)
        try:
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'domain': '.aliexpress.com',
                'path': '/'
            })
        except:
            pass

        print("Cookie injected. Refreshing page...")
        driver.refresh()
        random_sleep(5, 8)

        # 4. מעבר לעמוד המטבעות
        print("Navigating to coins page...")
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

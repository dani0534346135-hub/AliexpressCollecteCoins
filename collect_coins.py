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
# 5. לחיצה על כפתור האיסוף - חיפוש גמיש יותר
        print("Searching for collect button...")
        try:
            wait = WebDriverWait(driver, 30)
            
            # רשימת XPATH אפשריים לכפתור האיסוף (גרסת דסקטופ ונייד)
            potential_buttons = [
                "//div[contains(@class, 'checkin-button')]",
                "//span[contains(text(), 'Collect')]",
                "//button[contains(text(), 'Collect')]",
                "//div[@id='coin-check-in-btn']",
                "//div[contains(@class, 'coins-checkin-btn')]",
                "//*[contains(text(), 'קבל מטבעות')]" # תמיכה בעברית אם האתר קפץ לעברית
            ]
            
            found = False
            for xpath in potential_buttons:
                try:
                    btn = driver.find_element(By.XPATH, xpath)
                    if btn.is_displayed():
                        btn.click()
                        print(f"SUCCESS: Coins collected using XPath: {xpath}")
                        found = True
                        break
                except:
                    continue
            
            if not found:
                print("Could not find an active collect button. Maybe already collected?")
                driver.save_screenshot("page_state.png") # שומר צילום מסך כדי שנוכל לראות מה הבעיה
                
        except Exception as e:
            print(f"An error occurred during collection: {e}")
            if IS_GITHUB:
                driver.save_screenshot("check_page.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

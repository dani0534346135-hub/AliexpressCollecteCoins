import time
import random
import os
import sys
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

# בדיקה האם רץ ב-GitHub Actions
IS_GITHUB = os.getenv('GITHUB_ACTIONS') == 'true'

# === FORCE UTF-8 OUTPUT ===
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

ALIEXPRESS_EMAIL = os.getenv("ALIEXPRESS_EMAIL")
ALIEXPRESS_PASSWORD = os.getenv("ALIEXPRESS_PASSWORD")

if not ALIEXPRESS_EMAIL or not ALIEXPRESS_PASSWORD:
    print("Error: Environment variables for ALIEXPRESS_EMAIL and ALIEXPRESS_PASSWORD must be set.")
    exit(1)

def random_sleep(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

def type_like_human(element, text):
    for char in text:
        if random.random() < 0.01:
            typo_char = random.choice('qwertyuiopasdfghjklzxcvbnm')
            element.send_keys(typo_char)
            random_sleep(0.1, 0.3)
            element.send_keys(Keys.BACKSPACE)
            random_sleep(0.2, 0.5)
        element.send_keys(char)
        random_sleep(0.05, 0.15)

def login(driver):
    try:
        print("Starting login process...")
        wait = WebDriverWait(driver, 20)
        
        # טעינת עמוד ההתחברות ישירות
        driver.get("https://login.aliexpress.com")
        random_sleep(3, 5)

        # חיפוש שדה אימייל
        email_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id")))
        print("Found email input field")
        type_like_human(email_input, ALIEXPRESS_EMAIL)
        random_sleep(1, 2)

        # הזנת סיסמה
        password_input = driver.find_element(By.ID, "fm-login-password")
        print("Entering password...")
        type_like_human(password_input, ALIEXPRESS_PASSWORD)
        random_sleep(1, 2)

        # לחיצה על כפתור התחברות
        login_btn = driver.find_element(By.CSS_SELECTOR, "button.fm-button")
        login_btn.click()
        
        print("Clicked sign in button, waiting for redirect...")
        random_sleep(10, 15)
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def collect_coins(driver):
    try:
        print("Navigating to coins page...")
        driver.get("https://coins.aliexpress.com")
        random_sleep(10, 15)
        
        # ניסיון ללחוץ על כפתור האיסוף (לפי ה-Selectors מהקוד שלך)
        wait = WebDriverWait(driver, 20)
        collect_selectors = [
            "//div[contains(@class, 'checkin-button')]",
            "//div[contains(text(), 'Collect')]",
            "//span[contains(text(), 'Collect')]"
        ]
        
        for selector in collect_selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                btn.click()
                print("SUCCESS: Coins collected!")
                return True
            except:
                continue
        
        print("Could not find collect button. Maybe already collected?")
        return False
    except Exception as e:
        print(f"Collection failed: {e}")
        return False

def main():
    chrome_options = Options()
    
    # הגדרות קריטיות לריצה בתוך GitHub
    if IS_GITHUB:
        chrome_options.add_argument("--headless") # ריצה ללא חלון
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # שימוש ב-WebDriverManager בצורה אוטומטית (עוקף את ה-winreg)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Driver init failed: {e}")
        return

    try:
        if login(driver):
            collect_coins(driver)
            # צילום מסך לצורך בקרה בתוך GitHub Actions
            if IS_GITHUB:
                driver.save_screenshot("result.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

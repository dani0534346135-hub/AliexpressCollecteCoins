import time
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    # הגדרת מובייל כדי לקבל את הדף שראית בתמונה
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. התחברות
        print("Opening AliExpress...")
        driver.get("https://m.aliexpress.com")
        time.sleep(5)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            driver.add_cookie({'name': 'xman_f', 'value': cookie_val.strip(), 'path': '/', 'domain': '.aliexpress.com'})
        
        # 2. כניסה לקישור המדויק שמצאת
        print("Navigating to YOUR coins link...")
        target_url = "https://m.aliexpress.com/g/coin-index/index.html?_immersiveMode=true&from=pc302"
        driver.get(target_url)
        
        # המתנה לטעינה מלאה של הכפתורים הצהובים
        print("Waiting for page to load buttons...")
        time.sleep(20) 
        
        driver.save_screenshot("coins_screen.png")

        # 3. לחיצה על כפתור האיסוף (המספר הצהוב)
        print("Attempting to click the collect button...")
        result = driver.execute_script("""
            // חיפוש אלמנטים שמכילים מספרים או את המילה 'מטבעות'
            var elements = document.querySelectorAll('div, span, button');
            for (var el of elements) {
                if (el.innerText.includes('30') || el.innerText.includes('Collect') || el.innerText.includes('מטבעות')) {
                    el.click();
                    return "Clicked: " + el.innerText;
                }
            }
            return "Button not found";
        """)
        print(f"JS Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("after_click.png")
        print("Done!")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

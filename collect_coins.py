import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    
    # 1. התחזות לדפדפן אמיתי (User Agent) - זה מה שימנע את דף ה-Login
    user_agent = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") # מסתיר שזה בוט

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 2. כניסה קודם כל לדומיין
        driver.get("https://m.aliexpress.com")
        time.sleep(5)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting fresh cookie...")
            # הזרקה נקייה בלי דומיין ידני - סלניום יצמיד לבד
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'path': '/',
                'domain': '.aliexpress.com'
            })
            driver.refresh()
            time.sleep(10)

        # 3. ניווט לקישור המטבעות שלך
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)
        
        time.sleep(20) # זמן לטעינת כל האנימציות הצהובות
        driver.save_screenshot("after_loading.png")

        # 4. לחיצה אגרסיבית על כל מה שזז
        print("Searching for collect button...")
        result = driver.execute_script("""
            // חיפוש לפי טקסט (30, Collect, וכו')
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                if (el.innerText.includes('30') || el.innerText.includes('Collect')) {
                    el.click();
                    return "SUCCESS: Clicked " + el.innerText;
                }
            }
            // ניסיון אחרון: לחיצה בנקודה שבה נמצא ה-30 בתמונה שלך
            var x = window.innerWidth / 2;
            var y = 220; 
            var elAt = document.elementFromPoint(x, y);
            if (elAt) { elAt.click(); return "Clicked by position"; }
            
            return "Still not found";
        """)
        print(f"Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    
    # התחזות לטלפון אמיתי
    user_agent = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. פתיחת האתר (חובה לפתוח לפני הזרקת קוקי)
        print("Opening AliExpress...")
        driver.get("https://m.aliexpress.com")
        time.sleep(10) # זמן טעינה מורחב
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting fresh cookie...")
            # שיטה בטוחה: בלי הגדרת 'domain' ידנית, סלניום לוקח את הדומיין הנוכחי
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'path': '/'
            })
            print("Cookie injected successfully!")
            driver.refresh()
            time.sleep(10)

        # 2. ניווט לקישור המטבעות שלך
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)
        
        time.sleep(25) 
        driver.save_screenshot("after_loading.png")

        # 3. לחיצה על כפתור האיסוף
        print("Searching for collect button...")
        result = driver.execute_script("""
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                var text = el.innerText || "";
                if (text.includes('30') || text.includes('Collect') || text.includes('מטבעות')) {
                    el.click();
                    return "SUCCESS: Clicked " + text;
                }
            }
            // ניסיון לחיצה לפי מיקום אם הטקסט לא נמצא
            var clickTarget = document.elementFromPoint(window.innerWidth / 2, 220);
            if (clickTarget) { clickTarget.click(); return "Clicked by coordinates"; }
            return "Button not found";
        """)
        print(f"Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. פתיחת האתר - חייבים להיות בתוך aliexpress.com כדי להזריק קוקי
        print("Opening AliExpress...")
        driver.get("https://www.aliexpress.com")
        time.sleep(10)
        
        # 2. הזרקת הקוקי בצורה בטוחה
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            # שים לב: הורדתי את ה-'domain', סלניום יוסיף אותו אוטומטית לדומיין הנוכחי
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'path': '/'
            })
            print("Cookie injected! Refreshing...")
            driver.refresh()
            time.sleep(10)

        # 3. ניווט לדף המטבעות
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)
        
        time.sleep(25) 
        driver.save_screenshot("after_loading.png")

        # 4. לחיצה על כפתור "לאסוף"
        print("Searching for the orange button...")
        result = driver.execute_script("""
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                var text = el.innerText || "";
                if (text.includes('לאסוף') || text.includes('Collect') || text.includes('להרוויח')) {
                    el.click();
                    return "SUCCESS: Clicked button";
                }
            }
            // לחיצה במיקום הכפתור הכתום (מרכז המסך, גובה 430)
            var btn = document.elementFromPoint(window.innerWidth / 2, 430);
            if (btn) { btn.click(); return "SUCCESS: Clicked by position"; }
            return "Button not found";
        """)
        print(f"Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

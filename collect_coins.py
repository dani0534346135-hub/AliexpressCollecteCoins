import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    
    # הפעם בלי Mobile Emulation כדי שהקוקי מהמחשב יעבוד ב-100%
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. פתיחת האתר
        print("Opening AliExpress...")
        driver.get("https://www.aliexpress.com")
        time.sleep(5)
        
        # 2. הזרקת הקוקי
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            driver.add_cookie({
                'name': 'xman_f',
                'value': cookie_val.strip(),
                'path': '/',
                'domain': '.aliexpress.com'
            })
            driver.refresh()
            time.sleep(8)

        # 3. ניווט לקישור המטבעות המדויק
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to: {target_url}")
        driver.get(target_url)
        
        time.sleep(20) 
        driver.save_screenshot("after_loading.png")

        # 4. לחיצה ממוקדת על הכפתור הכתום "לאסוף"
        print("Searching for 'לאסוף'...")
        result = driver.execute_script("""
            // חיפוש לפי הטקסט המדויק שאמרת
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                if (el.innerText.includes('לאסוף') || el.innerText.includes('Collect')) {
                    el.click();
                    return "SUCCESS: Clicked 'לאסוף' button";
                }
            }
            // לחיצה במיקום הכפתור הכתום לפי הקואורדינטות החדשות (בגרסת דסקטופ)
            var btn = document.elementFromPoint(window.innerWidth / 2, 430);
            if (btn) { btn.click(); return "SUCCESS: Clicked by position"; }
            return "Button not found";
        """)
        print(f"Action Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

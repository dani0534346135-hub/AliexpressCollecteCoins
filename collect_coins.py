import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Opening AliExpress...")
        driver.get("https://m.aliexpress.com")
        time.sleep(10)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            driver.add_cookie({'name': 'xman_f', 'value': cookie_val.strip(), 'path': '/'})
            driver.refresh()
            time.sleep(12)

        # ניווט לדף המטבעות
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        print(f"Navigating to coins page...")
        driver.get(target_url)
        
        # המתנה ארוכה לטעינת הכפתור הכתום
        time.sleep(25) 
        driver.save_screenshot("after_loading.png")

        print("Searching for the 'לאסוף' button...")
        result = driver.execute_script("""
            var elements = document.querySelectorAll('div, span, button, p, a');
            for (var el of elements) {
                var text = el.innerText || "";
                // מחפש את המילה המדויקת שכתבת
                if (text.includes('לאסוף') || text.includes('Collect') || text.includes('להרוויח')) {
                    // וודא שזה כפתור באזור המרכזי ולא בתחתית
                    var rect = el.getBoundingClientRect();
                    if (rect.top > 100 && rect.top < 600) {
                        el.click();
                        return "SUCCESS: Clicked on button with text: " + text;
                    }
                }
            }
            
            // גיבוי: לחיצה במיקום המדויק של הכפתור הכתום הגדול (קצת מתחת למרכז)
            var x = window.innerWidth / 2;
            var y = 430; 
            var elAt = document.elementFromPoint(x, y);
            if (elAt) {
                elAt.click();
                return "SUCCESS: Clicked by coordinates on Orange Area";
            }
            
            return "Button not found";
        """)
        print(f"Result: {result}")
        
        # צילום מסך סופי לראות אם הצלחנו
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

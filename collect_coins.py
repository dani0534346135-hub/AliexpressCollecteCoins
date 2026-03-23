import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    # הגדרת מובייל חובה
    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 1. פתיחת האתר והזרקת קוקי
        print("Opening AliExpress Mobile...")
        driver.get("https://m.aliexpress.com")
        time.sleep(5)
        
        cookie_val = os.getenv("ALIE_COOKIE")
        if cookie_val:
            print("Injecting cookie...")
            driver.add_cookie({'name': 'xman_f', 'value': cookie_val.strip(), 'path': '/'})
            driver.refresh()
            time.sleep(8)

        # 2. כניסה לקישור הנכון ששלחת
        print("Navigating to coins page...")
        target_url = "https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&from=pc302"
        driver.get(target_url)
        
        print("Waiting 20 seconds for buttons to appear...")
        time.sleep(20) 
        
        driver.save_screenshot("after_loading.png")

        # 3. לחיצה על כפתור האיסוף
        print("Searching for collect button...")
        result = driver.execute_script("""
            var elements = document.querySelectorAll('div, span, button, p');
            for (var el of elements) {
                var text = el.innerText || "";
                // מחפש את המספר 30 או 'Collect' או 'מטבעות'
                if (text.includes('30') || text.includes('Collect') || text.includes('Check') || text.includes('מטבעות')) {
                    el.click();
                    return "Clicked: " + text;
                }
            }
            return "Button not found";
        """)
        print(f"Action Result: {result}")
        
        time.sleep(5)
        driver.save_screenshot("final_result.png")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

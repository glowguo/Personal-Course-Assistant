from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import os
import argparse # 确保 argparse 被导入

def fetch_all_headlines(url, scrolls=3, headless=True):
    # 这个函数的核心内容是正确的，保持不变
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    
    driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
    if not os.path.exists(driver_path):
        print("错误：未能找到ChromeDriver...")
        return []
    service = Service(executable_path=driver_path)
    
    driver = None
    try:
        driver = uc.Chrome(service=service, options=chrome_options, use_subprocess=True)
        driver.get(url)
        time.sleep(5)
        
        for i in range(scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
        title_elements = driver.find_elements(By.CSS_SELECTOR, "a.article-item-title")
        headlines = [elem.text for elem in title_elements if elem.text]
        return headlines
    except Exception as e:
        print(f"抓取过程中出现错误: {e}")
        return []
    finally:
        if driver:
            try:
                time.sleep(1)
                driver.quit()
            except Exception:
                pass

# --- **这是我们进行核心修正的地方** ---
def main():
    # 重新定义参数解析器，让它能理解 --output
    parser = argparse.ArgumentParser(description="工业级新闻采集器")
    parser.add_argument("--output", required=True, help="输出的文本文件名。")
    # 如果你还想保留调试功能，可以把 --show-browser 也加回来
    parser.add_argument('--headless', action='store_true', help="在后台无头模式运行（默认）。")
    parser.add_argument('--show-browser', dest='headless', action='store_false', help="运行时显示浏览器窗口（用于调试）。")
    parser.set_defaults(headless=True) # 默认使用无头模式
    
    args = parser.parse_args()

    target_url = "https://36kr.com/information/web_news"
    
    # 将 headless 参数传递给函数
    headlines = fetch_all_headlines(target_url, scrolls=3, headless=args.headless)
    
    if headlines:
        print(f"成功抓取到 {len(headlines)} 条标题...")
        # 使用从命令行接收到的文件名
        with open(args.output, 'w', encoding='utf-8') as f:
            for title in headlines:
                f.write(title + '\n')
        print(f"已成功写入文件 {args.output}")
    else:
        print("未能抓取到任何标题。")

if __name__ == "__main__":
    main()
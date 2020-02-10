import chromedriver_binary
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import datetime # yyyymmddHHMMSS のタイムスタンプをファイルに付ける

chrome_path = '/home/nishimrm/.pyenv/versions/3.7.5/lib/python3.7/site-packages'
options = webdriver.ChromeOptions()
options.binary_location = chrome_path 
options.add_argument('--headless')
#options.add_argument("disable-infobars")
#options.add_argument("--disable-extensions")
#options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')


driver = webdriver.Chrome(options=options)

# htmlを取得・表示
driver.get("https://www.google.com")
html = driver.page_source
print(html)

#current_time = datetime.datetime.today()
#current_time_str = current_time.strftime("%Y%m%d%H%M%S")
#driver.save_screenshot(f'screenshot-full-{current_time_str}.png')

driver.quit()

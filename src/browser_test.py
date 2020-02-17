import chromedriver_binary
import datetime 
from pyvirtualdisplay import Display
import subprocess
import time

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_path = '/usr/bin/google-chrome'


def screenShotFull(driver, filename, timeout=30):
    '''フルページ スクリーンショット'''
    # url取得
    url = driver.current_url
    # ページサイズ取得
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")
    # コマンド作成
    cmd = 'timeout ' + str(timeout)  \
        + ' "' + chrome_path +'"' \
        + ' --headless' \
        + ' --hide-scrollbars' \
        + ' --incognito' \
        + ' --screenshot=' + filename + '.png' \
        + ' --window-size=' + str(w) + ',' + str(h) \
        + ' ' + url
    print(cmd)

    # コマンド実行
    subprocess.Popen(cmd, shell=True,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)

def main():

        options = webdriver.ChromeOptions()
        options.binary_location = chrome_path 
        options.add_argument('--headless')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')
        driver = webdriver.Chrome(options=options)
        
        #url = "https://developers.google.com/web/updates/2017/04/headless-chrome?hl=ja"
        url = "https://google.co.jp/"
        driver.get(url)

        #指定された要素(検索テキストボックス)がDOM上に現れるまで待機する
        MAX_WAIT_TIME_SEC = 100
        INPUT_BOX_CLASS_NAME = "gLFyf"
        element = WebDriverWait(driver, MAX_WAIT_TIME_SEC).until(
                EC.presence_of_element_located((By.CLASS_NAME, 
                    INPUT_BOX_CLASS_NAME)))

        # 検索テキストボックスをクリアする
        #for item in range(0,100) :
        #    element.send_keys(Keys.BACK_SPACE)
        #code = "ChromeDriver"
        #element.send_keys(code)
        #element.send_keys(Keys.RETURN)        

        
        search_box = driver.find_element_by_name("q")
        search_box.send_keys('ChromeDriver')
        driver.save_screenshot(f'screenshot.png')
        search_box.submit()

        print(driver.title)

        # htmlを取得・表示
        #html = driver.page_source
        #print(html)

        current_time = datetime.datetime.today()
        current_time_str = current_time.strftime("%Y%m%d%H%M%S")
        #driver.save_screenshot(f'screenshot-full-{current_time_str}.png')
        filename = (f'screenshot-full-{current_time_str}') 
        screenShotFull(driver, filename)        

        driver.quit()

if __name__ == '__main__':
   main()

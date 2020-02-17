import chromedriver_binary
import datetime 
from pyvirtualdisplay import Display
import subprocess
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


chrome_path = '/usr/bin/google-chrome'

def operateBrawser(driver, url):
    driver.get(url)

    #指定された要素(検索テキストボックス)がDOM上に現れるまで待機する
    MAX_WAIT_TIME_SEC = 100
    INPUT_BOX_CLASS_NAME = "gLFyf"
    element = WebDriverWait(driver, MAX_WAIT_TIME_SEC).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                INPUT_BOX_CLASS_NAME)))
    #Google検索でChromeDriverを検索する
    search_box = driver.find_element_by_name("q")
    search_box.send_keys('yahoo')
    search_box.submit()
    return driver


def screenShot(driver, filename):
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")
    driver.set_window_size(w,h)
    driver.save_screenshot(filename)
    return driver

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
        
        #ブラウザで操作したいURLを指定
        url = "https://google.co.jp/"
        driver = operateBrawser(driver,url)

        #スクリーンショット
        current_time = datetime.datetime.today()
        current_time_str = current_time.strftime("%Y%m%d%H%M%S")
        file_name=(f'screenshot-full-{current_time_str}.png')
        driver = screenShot(driver, file_name)
        driver.quit()

if __name__ == '__main__':
   main()

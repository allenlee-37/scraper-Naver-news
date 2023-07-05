import argparse
import os

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import pandas as pd
from tqdm import tqdm

from datetime import datetime
import time

import re

# Headless로 실행
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_experimental_option("detach", True)
# options.add_argument('headless')
# options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def 경향신문(url)->str:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'articleBody')))
        
    try: 
        text_elements = driver.find_elements(By.XPATH, '//*[@id="articleBody"]/p') # ///*[@id="articleBody"]/p[3]//*[@id="articleBody"]/p[3]/text()
        text = [elem.text for elem in text_elements]
    except: text = 'error'
    
    result = '\n'.join(text)
    print(result)
    return result

def 국민일보()->str:
    pass

def open_url():
    raw_data = pd.read_csv('./result/url_info.csv')
    url_list = raw_data['Url']
    date_list = raw_data['Date']
    Title_list = raw_data['Title']
    Paper_list = raw_data['NewsPaper']
    
    result = []
    for elem in tqdm(range(len(raw_data))): # 
        if Paper_list[elem] == '경향신문': 
            text = 경향신문(url_list[elem])
        else: pass
        result.append(text)

    return 





def main():
    open_url()
    return

if __name__ == "__main__": main()
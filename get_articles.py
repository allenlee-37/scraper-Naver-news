import argparse
import os

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import pandas as pd
from tqdm import tqdm

from datetime import datetime
import re

# Headless로 실행
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920x1080')
options.add_experimental_option("detach", True)
options.add_argument('headless')
# options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def 경향신문():
    pass

def 국민일보():
    pass

def open_url():
    raw_data = pd.read_csv('./result/url_info.csv')
    url_list = raw_data['Url']
    date_list = raw_data['Date']
    Title_list = raw_data['Title']
    Paper_list = raw_data['NewsPaper']
    
    for elem in len(raw_data):
        if Paper_list[elem] == '경향신문':
            경향신문()
        elif Paper_list[elem] == '국민일보':
            국민일보()
        else: pass
    # driver.get(url)
    return print(len(raw_data))





def main():
    open_url()
    return

if __name__ == "__main__": main()
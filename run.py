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
# options.add_argument('headless')
# options.add_argument('disable-gpu')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_newspaper_txt()->dict:
    '''
    신문 이름 입력 -> 신문에 해당하는 아이디 번호를 전달
    news-paper.txt를 활용해 dictionary를 만듬
    '''
    f = open('news-paper.txt', 'r')
    raw_data = f.read()
    raw_data = raw_data.replace('\n','')
    raw_data = raw_data.split(',')
    paper_name = [re.sub(r'[0-9,=]','',text).strip() for text in raw_data]
    paper_id = [re.sub(r'[ㄱ-ㅣ가-힣=]+','',text).strip() for text in raw_data]
    paper_id = list(map(int, paper_id))
    
    paper_dict = {}
    for num in range(len(paper_name)):
        paper_dict[paper_name[num]] = paper_id[num]

    return paper_dict

def get_newspaper_num(news_paper_name)->int:
    paper_dict = get_newspaper_txt()
    result = paper_dict[news_paper_name]
    return result

def get_url(search_word, start_date, end_date, media_num, page_num)->str:
    return f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search_word}&sort=1&photo=0&field=0&pd=3&ds={start_date}&de={end_date}&mynews=1&office_type=1&office_section_code=1&news_office_checked={media_num}&nso=so:dd,p:from20220101to20221231,a:all&start={page_num*10+1}'

def get_page_info(paper_name='경향신문',
                  keyword = '경기도 관광',
                  start_date = '2022.01.01',
                  end_date = '2022.12.31',
                  page_num = 1)->pd.DataFrame:
    # 경향신문 테스트
    news_paper = get_newspaper_num(paper_name)
    url = get_url(keyword, start_date, end_date, news_paper, page_num)

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(2)
    driver.get(url)

    article_dates_raw = driver.find_elements(By.XPATH, '//span[@class="info"]')# //div[@class="news_area"]/div/div/span
    article_dates_raw = [elem.text for elem in article_dates_raw]
    article_dates = []
    for elem in article_dates_raw:
        if len(elem) == 11: article_dates.append(elem)

    article_titles = driver.find_elements(By.XPATH, '//div[@class="news_area"]/a')
    article_titles = [elem.get_attribute("title") for elem in article_titles]

    article_urls = driver.find_elements(By.XPATH, '//div[@class="news_area"]/a')
    article_urls = [elem.get_attribute("href") for elem in article_urls]

    info = pd.DataFrame({
        'Date': article_dates,
        'Title': article_titles,
        'Url': article_urls
    })

    disability = driver.find_element(By.XPATH, '//*[@id="main_pack"]/div[2]/div/a[2]')
    disability = disability.get_attribute('aria-disabled')
    if disability == 'false': disability = False

    return info, disability

info_result, disability = get_page_info(paper_name=list(get_newspaper_txt().keys())[0], page_num = 0)
for i in range(1, len(list(get_newspaper_txt().keys()))):
    disability=False
    print(i)
    num = 1
    while disability == False:
        info, disability = get_page_info(paper_name=list(get_newspaper_txt().keys())[i], page_num = num)
        info_result = pd.concat([info_result, info])
        num = num+1
        print(list(get_newspaper_txt().keys())[i])

driver.quit()
info_result = info_result.reset_index(drop=True)
info_result.to_csv('resultdfdfdfdf.csv')


'''
info_result, disability=get_page_info(paper_name=get_newspaper_txt().keys()[0], page_num = 0)
num=1
while disability == False:
    info, disability = get_page_info(page_num = num)
    info_result = pd.concat([info_result, info])
    num = num+1

driver.quit()
info_result = info_result.reset_index(drop=True)
info_result.to_csv('resultdfdfdfdf.csv')

get_newspaper_txt().keys()[0]'''

print(len(list(get_newspaper_txt().keys())))
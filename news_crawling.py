#import module

!pip install selenium
!apt-get update
!apt install chromium-chromedriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
from google.colab import files
import numpy as np
import math

#function

def nameandrate(filename, target = 0, rating = 0):
  df_rating = pd.read_csv(filename, encoding = 'UTF-8')
  
  #전체를 불러옴
  if target == 0:
    return df_rating['name'].to_frame(name = 'company')
   
  #등급별 자름
  else:
    df = df_rating[df_rating[target] == rating][['name', target]]
    df.rename(columns = {target : "rating"}, inplace=True)
    return df

def makedate(start, end):
  dt_index = pd.date_range(start, end)
  dt_list = dt_index.strftime("%Y%m%d").tolist()

  return dt_list

def concatlist(*args):
  dfs = list(args)
  return pd.concat(dfs)

def preprocessing(df):
  temp = df[['date', 'company', 'code',  'title', 'content']]
  temp = temp.drop_duplicates(['content'])
  temp = temp.drop_duplicates(['title'])

  return temp

def crawling(tab, companylist, dt_list, df): 

  #import selenium
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
  driver.implicitly_wait(25)

  for date in tqdm(dt_list):
      url = f"https://news.naver.com/main/list.nhn?mode=LS2D&sid2={tab}&sid1=257&mid=shm&date={date}&page="
      driver.get(url)
      
      total_pp = len(driver.find_elements_by_xpath('//*[@class="nclicks(fls.page)"]')) + 1
      
      for i in range(0, total_pp):
          driver.get(url+str(i+1))
          
          search_list = []
          content_list = []
          title_list = []
          
          atags_t = driver.find_elements_by_css_selector('dt')
          #text 제목만 가져옴
          
          atags = [x.text for x in atags_t if x.text and x.text != '동영상기사']

          for row in companylist.itertuples():
            name = getattr(row, "name")
            code = getattr(row, 'code')
            # rating = getattr(row, "rating")
            
            
            if (re.search(r"(^|[^ㄱ-힣])%s\W" % name, " ".join(atags))):
                for atag in atags:
                    if name in atag:
                        search_list.append(atags.index(atag))

                for i in search_list:
                    try:
                        button = driver.find_element_by_xpath('//*[@id="main_content"]/div[2]/ul[{}]/li[{}]/dl/dt/a'.format(i//10 + 1, i%10 + 1 ))
                        button.send_keys(Keys.ENTER)
                        time.sleep(1)
                        title_list.append(driver.find_elements_by_xpath('//*[@id="articleTitle"]')[0].text)

                        content_t = driver.find_elements_by_xpath('//*[@id="articleBodyContents"]')
                        content_list.append(content_t[0].text.replace("\n", ""))
                        driver.back()
                        time.sleep(2)
                    
                    except:
                        pass
                    
                    
            if title_list:            
                ##데이터 저장
                new_data = {'title':title_list, 'content': content_list}
                temp = pd.DataFrame(new_data)
                temp['date'] = date
                temp['code'] = code
                temp['company'] = name

                df = pd.concat([df, temp])

  return preprocessing(df)

 def main(year): 
  #시작 날짜와 끝 날짜로 date list 생성
  dt_list = makedate(f'{year}0101', f'{year}1231')

  mCols = ["date", "company", 'code', "title", "content"]
  info = pd.read_csv(f'ESGdata_{year}_.csv', encoding = 'utf-8')

  companylist = info[['name', 'code']]

  #tab, companylist, dt_list, df
  #{노동: 251, 환경: 252, 인권복지: 59b, 사회일반: 257}
  #(ex. '252', companylist, dt_list, df)
  
  tabs = ['251', '252', '59b', '257']
  
  for tab in tabs:
    df = pd.DataFrame(columns=mCols)
    df = crawling(tab, companylist, dt_list, df)
  
    #저장
    df.to_csv(f'{year}_{tab}total.csv',encoding = 'utf-8')
    files.download(f'{year}_{tab}total.csv')
    print(f'{year}, {tab} 완료')
    
  

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 20:31:11 2021

@author: jinho
"""


import requests
import pandas as pd
from bs4 import BeautifulSoup

ESG = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\ESGcompany.csv', encoding = 'utf-8')
ESG.head
esg_company = []
for i in ESG['company']:
    esg_company.append(i)


#크롤링
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
url = 'http://unglobalcompact.kr/membership/member/'
req = requests.get(url, headers = headers)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
print(soup.table)
a = soup.find_all(attrs = {'class' : 'mm_tab_fir'})

ungc_list = []
for el in a:
    print(el.get_text())
    ungc_list.append(el.get_text())

#영어이름으로 나오는거 제거
eliminate_duple = []
i=0
while 1:
    try:
        eliminate_duple.append(ungc_list[i])
        i += 2 
    except:
        break

#N그램 만들기
join2 = "".join(esg_company)

def make_ngram(lst):
    n_gram = []
    for i in range(len(lst)-2):
        n_gram.append(lst[i] + lst[i + 1] + lst[i + 2])
    return n_gram

n_gram = []
for i in range(len(join2) - 2):
    n_gram.append(join2[i] + join2[i + 1] + join2[i+2])

#
UNGC_list2 = []
for i in eliminate_duple:
    l = make_ngram(i)
    for a in l:
        if a in n_gram:
            UNGC_list2.append(i)

my_set = set(UNGC_list2) #집합set으로 변환
UNGC_list2 = list(my_set) #list로 변환

df1 = pd.DataFrame(UNGC_list2, columns = ['company'])
df1.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\ungc_list.csv', encoding = 'utf-8', index= False)

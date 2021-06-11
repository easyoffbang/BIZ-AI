# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 17:10:18 2021

@author: jinho
"""



from html_table_parser.parser import HTMLTableParser
import pandas as pd
import urllib.request

def flatten(lst):
    result = []
    for item in lst:
        result.extend(item)
    return result

def url_get_contents(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url, headers = headers)
    f = urllib.request.urlopen(req)
    return f.read()


def crawling_cdp(years):
    page = 0
    y = []
    while 1:
        page += 1
        print(page)
        url = 'https://www.cdp.net/ko/responses?filters%5Bcountries%5D%5B%5D=Republic+of+Korea&filters%5Bcountries%5D%5B%5D=South+Korea&filters%5Bprogrammes%5D%5B%5D=Forest&filters%5Bprogrammes%5D%5B%5D=Investor&filters%5Bprogrammes%5D%5B%5D=Supply+Chain&filters%5Bprogrammes%5D%5B%5D=Water&filters%5Bstatuses%5D%5B%5D=Information+provided&filters%5Bstatuses%5D%5B%5D=Submitted&filters%5Byears%5D%5B%5D={}&page={}&queries%5Bname%5D=&sort_by=project_year&sort_dir=desc&utf8=%E2%9C%93'.format(years, page)
        xhtml = url_get_contents(url).decode('utf-8')
        p = HTMLTableParser()
        p.feed(xhtml)
        x = p.tables
        y.append(x[0][1:])
        if page > 2:
            if y[0] == x[0][1:]:
                del y[page-1]
                break
    df = pd.DataFrame(flatten(y), columns=x[0][0])
    indexNames = df[df['Status'] == 'Declined to participate' ].index
    df.drop(indexNames, inplace = True)
    df.drop(['Status', 'Year','점수'], axis = 1, inplace = True)
    df.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\{}_cdp.csv'.format(years), encoding = 'utf-8', index= False)

for i in [2016, 2017, 2018, 2019, 2020]:
    crawling_cdp(i)



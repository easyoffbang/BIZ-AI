# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 21:27:50 2021

@author: jinho
"""

import pandas as pd
import re
from tqdm import tqdm
import numpy as np

def refine(text):
    return re.sub('<.+?>', '', text)

#사업보고서
report = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\아카이브 (1)\2020totalreport_3.csv', encoding = 'utf-8')
#매출액이랑단위적힌파일
report2 = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\sale\2020Sales.csv', encoding = 'utf-8')


report['content'] = report['content'].apply(lambda x: refine(x))


#기부금이랑 그 단위 뽑는 리스트 만들기
donation_list = []
unit_list = []
number = []
for i in tqdm(range(len(report))):
    r = re.compile(r'\b기부금\s?(?:\(?(?:[가-힣]*\d|[^가-힣]+)\d?\)|[가-힣]|비용|)(?:\s[가-힣]*|)\s*\(?(?:\d(?:,?\d+)*)\)?\s')
    num = re.compile(r'\d+(?:,?\d+)*')
    donation = r.findall(report['content'][i]) 
    donation_list.append(donation)
    if len(donation) != 0:
        donation_ind = re.search(r'\b기부금\s?(?:\(?(?:[가-힣]*\d|[^가-힣]+)\d?\)|[가-힣]|비용|)(?:\s[가-힣]*|)\s*\(?(?:\d(?:,?\d+)*)\)?\s', report['content'][i]).start()
        l = re.compile(r'단위\s?:.+\b')
        unit = l.findall(report['content'][i][:donation_ind])
        x = num.findall(donation[0])
        real_x = re.sub(',','',x[0])
        number.append(int(real_x))
        if len(unit) != 0:
            unit_list.append(unit[-1])
        else:
            unit_list.append('단위x')
    else:
        number.append(0)
        unit_list.append('기부금x')

#기부금을 단위에 맞춰서 report 데이터프레임에 삽입
for i in range(len(report)):
    if '천' in unit_list[i]:
        report.loc[i, 'donation'] = number[i]*1000
    elif '백만' in unit_list[i]:
        report.loc[i, 'donation'] = number[i]*1000000
    else:
        report.loc[i, 'donation'] = number[i]
report.drop(['content','Unnamed: 0'], axis= 1, inplace = True)
        

    
#기업명 바꾸기
ESG = pd.read_csv(r'C:\Users\jinho\OneDrive\바탕 화면\학교\AI랩\프로젝트\기타자료및코드\ESGcompany\ESGdata_2020_.csv', encoding = 'utf-8')
ESG_company = ESG[['name','code']]
ESG_company['donation'] = None


com_code = list(report['code'])
for i in range(len(com_code)):
    ind = ESG_company[ESG_company['code'] == com_code[i]].index
    ESG_company['donation'][ind] = report['donation'][i]
ESG_company['name'] = ESG_company['name'].apply(lambda x: re.sub(';', '', x))


#매출액 X 단위
report2 = report2.fillna(0)

for i in range(len(report2)):
    if report2['sales'][i] == '사업보고서 확인필요':
        print(i)
for i in range(len(report2)):
    if report2['sales'][i] != ' ':
        if report2['scale'][i] == 0:
            report2.loc[i, 'sale'] = 0
        elif '천' in report2['scale'][i]:
            report2.loc[i, 'sale'] = int(report2['sales'][i])*1000
        elif '백만' in report2['scale'][i]:
            report2.loc[i, 'sale'] = int(report2['sales'][i])*1000000
        elif 'USD' in report2['scale'][i]:
            report2.loc[i, 'sale'] = int(report2['sales'][i])*1100
        else:
            report2.loc[i, 'sale'] = int(report2['sales'][i])
    else:
        pass

report2 = report2.replace(0, np.nan)

#기부금 비율구하기
ESG_company['sale'] = report2['sale']
for i in range(len(ESG_company)):
    try:
        if type(ESG_company['sale'][i]) != float:
            ESG_company['sale'][i] = float(ESG_company['sale'][i])
            ESG_company['donation'][i] = float(ESG_company['donation'][i])
            ESG_company.loc[i, 'donation_ratio'] = ESG_company['donation'][i] / ESG_company['sale'][i]
        else:
            ESG_company.loc[i, 'donation_ratio'] = np.nan
    except:
        ESG_company.loc[i, 'donation_ratio'] = '체크 필요'

ESG_company.columns = ['name', 'code', 'donation', 'sale',  'donation_rate']

#이상한거 확인
for i in range(len(ESG_company)):
    if ESG_company['sale'][i] < 0 :
        print(ESG_company['name'][i])
        print(ESG_company['donation'][i])

ESG_company.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\report_2020_donate.csv', index = False, encoding= 'utf-8')



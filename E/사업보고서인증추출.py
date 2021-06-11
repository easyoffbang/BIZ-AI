# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 02:44:24 2021

@author: jinho
"""

import pandas as pd
import re
from tqdm import tqdm

def refine(text):
    return re.sub('<.+?>', '', text)

report = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\2016totalreport_22.csv', encoding='utf-8')
report2 = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\2016totalreport.csv', encoding='utf-8')

report.drop(['Unnamed: 0'], axis = 1, inplace=True)
report2.drop(['Unnamed: 0'], axis = 1, inplace=True)

for i in range(len(report)):
    report['content'][i] = refine(report['content'][i])
for i in range(len(report2)):
    report2['content'][i] = refine(report2['content'][i])
for i in range(len(report)):
    report['content'][i] = report['content'][i] + report2['content'][i]

#기업명 변경
esg_data = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\ESG_com\ESGdata_2016_.csv', encoding = 'utf-8')
com_code = list(report['code'])
for i in com_code:
    t1 = esg_data[esg_data['code'] == i].index
    t2 = report[report['code'] == i].index
    name = esg_data['name'][t1]
    if len(name) != 0:
        report['name'][t2] = name.iloc[0]
report['name'] = report['name'].apply(lambda x: re.sub(';', '', x))

#모든 인증 불러오기
report['Env'] = None
certifi_name = ['ISO', 'HACCP', 'OHSAS', 'GMS', 'GMP']
compile_list = [r'ISO\s?.?\s?(?:TS)?\s?\d{4,5}(?:[:,;]{0}(?:[/,]?\s?(?:TS)?\s?\d{4,5})+)?', r'HACCP', r'OHSAS.?18001', r'GMS', r'GMP']
for certi in range(len(certifi_name)):
    r = re.compile(compile_list[certi], re.IGNORECASE)
    for i in range(len(report)):
        t = r.findall(report['content'][i])
        if len(t) != 0:
            report['Env'][i] = t
            T = " ".join(t)
            number = re.compile(r'\d+',re.IGNORECASE)
            num = number.findall(T)
            if len(num) != 0:
                num_list = list(set(num))
                for name in num_list:
                    report.loc[i, certifi_name[certi] +" "+ name] = 1
            else:
                report.loc[i, certifi_name[certi]] = 1
        else:
            pass
report.count()

report = report.fillna(0)
report.drop(['content'],axis=1,inplace=True)

report.drop(['ISO 2007', 'ISO 2008', 'Env', 'ISO 2015'],axis=1,inplace=True)

#저장
report.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\report_2020_certi.csv', index = False, encoding= 'utf-8')

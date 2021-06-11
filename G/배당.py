# -*- coding: utf-8 -*-
"""
Created on Wed May 26 00:13:16 2021

@author: jinho
"""
import pandas as pd
import re
import numpy as np
report = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/baedang/report_allocation_2016.csv', encoding = 'utf-8')
report.drop(['Unnamed: 0'], axis = 1, inplace = True)

report['content'][217]

def refine(text):
    return re.sub('<.+?>', '\n', text)

report['content'] = report['content'].apply(lambda x: refine(x) if type(x) != float else None)
name_list = list(report['name'])


a = report['content'][2]

cont_list = list(report['content'])

baedang_list = []
l = re.compile(r'\(연결\)현금배당성향\(%\)')
m = re.compile(r'현금배당수익률\s?\(%\)')
p = re.compile(r'-?\d{1,3}\.?\d*|-(?!\d)')
for i in range(len(cont_list)):
    if cont_list[i] != None:
        cont = l.search(cont_list[i])
        cont2 = m.search(cont_list[i])
        if cont != None:
            ind = cont.end()
            ind2 = cont2.start()
            tempt = cont_list[i][ind:ind2]
            num = p.search(tempt)
            num1 = num.group()
            baedang_list.append(num1)
        else:
            baedang_list.append(None)
            print(i)
    else:
        baedang_list.append(None)
        print(i)
            
baedang = report.drop(['content'], axis = 1)
baedang['baedang'] = baedang_list
baedang['baedang'] = baedang['baedang'].apply(lambda x: float(0) if x == '-' else x)
baedang.to_csv(r'C:/Users/jinho/OneDrive/바탕 화면/baedang/report_allocation_2016_.csv', encoding= 'utf-8', index = False)
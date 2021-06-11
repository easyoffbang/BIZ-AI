# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 22:35:20 2021

@author: jinho
"""
#사업보고서파일 가져오기
import pandas as pd
import re

E = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\2016totalreport.csv', encoding= 'utf-8')
def refine(text):
    return re.sub('<.+?>', '', text)
E.drop(['Unnamed: 0'], axis =1 , inplace = True)
for i in range(len(E)):
    E['content'][i] = refine(E['content'][i])


#환경으로 시작하는 것들에서 환경산업 뺀거 줄바꿈 2개 까지
E['Env'] = None
for i in range(len(E)):
    t = re.search(r'\w{1}\.\s+환경.+', E['content'][i])
    if t != None:    
        ind = t.start()
        a = E['content'][i][ind+50:]
        E['Env'][i] = E['content'][i][ind:]
        nt = re.search(r'\n{2}', a)
        if nt != None:
            ind2 = nt.start()
            print(ind2)
            E['Env'][i] = E['Env'][i][:ind2+50]
            b = re.search(r'\w{1}[\.\)]\s+(환경자원 사업|환경산업|환경에서|경변화|환경부|환경친화형|환경친화적|환경사업|환경범죄).+', E['Env'][i][:10])
            if b != None:
                E['Env'][i] = None
            else:
                pass
        else:
            pass
    else:
        pass
#유무를 0과 1로 표현
E['Environment'] = 0
for i in range(len(E)):
    if E['Env'][i] != None:
        if len(E['Env'][i]) > 50:
            E['Environment'][i] = 1
        else:
            E['Environment'][i] = 0
    else:
        E['Environment'][i] = 0
print(len(E['Env'][582])>50)

E['Env'].isna().sum()
E.drop(['content'],axis=1 , inplace = True)        
E.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\report_제거_t2.csv',encoding = 'utf-8')



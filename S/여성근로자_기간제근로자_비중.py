# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 01:28:08 2021

@author: jinho
"""
import pandas as pd
import re

esg_data = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\ESG_com\ESGdata_2020_.csv', encoding= 'utf-8')
code_list = list(esg_data['code'])

def import_com(code):
    name = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\2020\2020\{0:06d}report_8.csv'.format(code), encoding = 'utf-8')
    return name

#비율 구하기
a=0
basic = esg_data[['code','name']]
for i in code_list:
    try:
        data = import_com(i)
    except:
        a += 1
        print('-'*30)
        print(a)
        delete_index = basic[basic['code'] == i].index
        print(delete_index)
        basic = basic.drop(delete_index)
        basic.reset_index(drop=True, inplace=True)
        print(i,'없는 코드입니다')
        print('-'*30)
    data = data.replace('-', 0)
    total_worker = float(data.iloc[-1,7])
    woman_worker = data[data.iloc[:,2] == '여'].iloc[:,7].astype(float).sum()
    #[-1,7]에 -로 표기되어서 0으로 보이는 경우
    if total_worker == 0:
        if data.iloc[-1,5] != 0:
            total_worker = float(data.iloc[-1,5])+float(data.iloc[-1,3])
            print('총근로자 1:', i)
        else:
            total_worker = float(data.iloc[-1,3])
            print('총근로자 0:', i)
        non_stand = float(data.iloc[-1, 5])
        woman_worker = data[data.iloc[:,2] == '여'].iloc[:,5].astype(float).sum() + data[data.iloc[:,2] == '여'].iloc[:,3].astype(float).sum()
    #아닌 경우
    else:
        if float(data.iloc[-1,3])+float(data.iloc[-1,5]) == float(data.iloc[-1,7]):
            non_stand = float(data.iloc[-1,5])
        else:
            non_stand = float(data.iloc[-1,5])+float(data.iloc[-1,6])
            print(i)
    #기간제근로자의 전체가 단시간근로자를 포함하는지 안하는지
    add_ind = basic[basic['code'] == i].index
    basic.loc[add_ind, 'total_worker'] = total_worker
    basic.loc[add_ind, 'woman_worker'] = woman_worker
    basic.loc[add_ind, 'non_stand'] = non_stand
    basic.loc[add_ind, 'woman_rate'] = woman_worker / total_worker
    basic.loc[add_ind, 'non_rate'] = non_stand / total_worker

basic.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\report2020worker.csv', index = False, encoding= 'utf-8')

#확인
check_list = list(basic['code'])
check = []
for i in check_list:
    check.append(import_com(i))




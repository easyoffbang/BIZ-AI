

# -*- coding: utf-8 -*-
"""
Created on Wed May  5 16:34:19 2021

@author: jinho
"""

import pandas as pd
import re
import numpy

saub_2020 = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/기타자료/사업의내용부분/2020totalreport.csv', encoding = 'utf-8')

com_list = []
code_list = []
cont_list = []
for i in range(len(saub_2020)):
    t = re.search(r'온실가스\s?(?:배출량)?', saub_2020['content'][i])
    if t != None:
        ind = t.start()
        a = saub_2020['content'][i][ind-500:]
        com_list.append(saub_2020['name'][i])
        code_list.append(saub_2020['code'][i])
        cont_list.append(a)

t = []
for i in range(len(cont_list)):
    try:
        c = pd.read_html(cont_list[i])
        t.append(c)
    except:
        t.append(None)
        pass

#flag는 모두 이중칼럼이 존재할때만 사용
#1일때, 온실가스 or 에너지가 칼럼명에 존재하고 그 하위칼럼으로 총계, 합계 등이 존재할때
#2일때, 온실가스 or 에너지가 칼럼명에 존재하고 그 하위칼럼으로 20XX년, -기 등이 존재할때
#3일때, 20XX년, -기가 칼럼명에 존재하고 그 하위칼럼으로 총계, 합계 등이 존재할 때.
#4일때, 20XX년, -기가 칼럼명에 존재하고 그 하위칼럼으로 온실가스 or 에너지가 존재할 때
#5일때, flag 1이고 행에 총계, 합계 등이 존재할 때


df_list = pd.DataFrame({'company' : com_list, 'code': code_list, 'content': t,'onsil': None, 'energy':None})
list_n = []
che = 1
for n in range(len(t)):
    if t[n] != None:
        for tem in t[n]:
            flag = 0
            col = tem.columns
            onsil_row_ind = None
            energy_row_ind = None
            if type(col[0]) == str:
                if '2020' in str(tem.columns):
                    for num in range(len(col)):
                        if '2020' in col[num]:
                            col_index = num
                            break
                        elif '계' in col[num] or '합' in col[num] or'총량' in col[num]:
                            col_index = num
                            break
                    for num2 in range(len(tem)):
                        row = tem.iloc[num2]
                        if '온실가스' in str(row) or '배출량' in str(row):
                            onsil_row_ind = num2
                        elif '에너지' in str(row):
                            energy_row_ind =num2
                    if energy_row_ind != None and onsil_row_ind != None:
                        onsil = tem.iloc[onsil_row_ind, col_index]
                        energy = tem.iloc[energy_row_ind, col_index]
                        print(n)
                        print(onsil)
                        print(energy)
                        print('-'*50)
                        if df_list['energy'][n] == None and df_list['energy'][n] == None:
                            df_list.loc[n,'onsil'] = onsil
                            df_list.loc[n,'energy'] = energy 
                    elif onsil_row_ind == None and energy_row_ind != None:
                        onsil = '-'
                        energy = tem.iloc[energy_row_ind, col_index]
                        print(n)
                        print(onsil)
                        print(energy)
                        print('-'*50)
                        if df_list['onsil'][n] == None:
                            df_list.loc[n,'onsil'] = onsil
                            df_list.loc[n,'energy'] = energy
                        elif df_list['energy'][n] == '-':
                            df_list.loc[n,'energy'] = energy
                    elif energy_row_ind == None and onsil_row_ind != None:
                        onsil = tem.iloc[onsil_row_ind, col_index]
                        energy = '-'
                        print(n)
                        print(onsil)
                        print(energy)
                        print('-'*50)
                        if df_list['energy'][n] == None:
                            df_list.loc[n,'onsil'] = onsil
                            df_list.loc[n,'energy'] = energy
                        elif df_list['onsil'][n] == '-' :
                            df_list.loc[n,'onsil'] = onsil

                if '온실가스' in str(tem.columns):
                    col_onsil_index = None
                    col_energy_index = None
                    row_ind = None
                    for num in range(len(col)):
                        if '온실가스' in col[num]:
                            col_onsil_index = num
                        elif '에너지' in col[num]:
                            col_energy_index = num
                    for num2 in range(len(tem)):
                        row = tem.iloc[num2]
                        if '2020' in str(row):
                            row_ind = num2
                        elif '계' in str(row) or '합' in str(row) or'총량' in str(row):
                            row_ind = num2
                    try:
                        if col_onsil_index != None and row_ind == None and col_energy_index != None:
                            print('온실컬럼', n)
                            print('온실가스:',tem.iloc[0, col_onsil_index])
                            print('에너지:',tem.iloc[0, col_energy_index])
                            print('-'* 50)
                            df_list.loc[n,'onsil'] = tem.iloc[0, col_onsil_index]
                            df_list.loc[n,'energy'] = tem.iloc[0, col_energy_index]
                        elif col_onsil_index == None and row_ind != None:
                            print('온실컬럼', n)
                            print('온실가스: ',tem.iloc[row_ind, col_onsil_index])
                            print('에너지: -')
                            print('-'* 50)
                            if df_list['onsil'][n] == None:
                                df_list.loc[n,'onsil'] = tem.iloc[0, col_onsil_index]
                                df_list.loc[n,'energy'] = '-'
                        elif row_ind != None and col_energy_index != None:
                            print('온실컬럼', n)
                            print('온실가스: -')
                            print('에너지:',tem.iloc[row_ind, col_energy_index])
                            print('-'* 50)
                            if df_list['energy'][n] == None:
                                df_list.loc[n,'onsil'] = '-'
                                df_list.loc[n,'energy'] = tem.iloc[row_ind, col_energy_index]       
                        elif col_onsil_index != None and row_ind != None and col_energy_index != None:
                            print('온실컬럼', n)
                            print('온실가스:',tem.iloc[row_ind, col_onsil_index])
                            print('에너지:',tem.iloc[row_ind, col_energy_index])
                            print('-'* 50)
                            df_list.loc[n,'onsil'] = tem.iloc[row_ind, col_onsil_index]
                            df_list.loc[n,'energy'] = tem.iloc[row_ind, col_energy_index]
                    except:
                        print('오류')
                        break
            #컬럼이 인덱스
            elif type(col[0]) == numpy.int64:
                onsil_ind = None
                energy_ind = None
                years_ind = None
                a = list(tem.iloc[0])
                b = list(tem.iloc[:,0])
                if '온실가스' in str(a) and '에너지' in str(a):
                        for num in range(len(a)):
                            if '온실가스' in str(a[num]):
                                onsil_ind = num
                            elif '에너지'  in str(a[num]):
                                energy_ind = num
                        for num2 in range(len(b)):
                            if '2020' in str(b[num2]):
                                years_ind = num2
                            elif '계' in str(b[num2]) or '합' in str(b[num2]) or'총량' in str(b[num2]):
                                years_ind = num2
                        try:
                            if years_ind != None and onsil_ind != None and energy_ind != None:
                                onsil = tem.iloc[years_ind, onsil_ind]
                                energy = tem.iloc[years_ind, energy_ind]
                                print('int칼럼', n)
                                print('온실가스', onsil)
                                print('에너지', energy)
                                print('-'* 50)
                                df_list.loc[n,'onsil'] = onsil
                                df_list.loc[n,'energy'] = energy 
                        except:
                            break

                        
                elif '2020' in str(a) or  '계' in str(a) or '합' in str(a) or'총량' in str(a):
                    for num in range(len(a)):
                        if '2020' in str(a[num]):
                            years_ind = num
                        elif '계' in str(a[num]) or '합' in str(a[num]) or'총량' in str(a[num]):
                            years_ind = num
                    for num2 in range(len(b)):
                        if '온실가스' in str(b[num2]) or '배출량' in str(b[num2]):
                            onsil_ind = num2
                        elif '에너지' in str(b[num2]):
                            energy_ind = num2
                    if years_ind != None and onsil_ind != None and energy_ind != None:
                        onsil = tem.iloc[onsil_ind,years_ind]
                        energy = tem.iloc[energy_ind, years_ind]
                        print('int칼럼', n)
                        print('온실가스', onsil)
                        print('에너지', energy)
                        print('-'* 50)
                        df_list.loc[n,'onsil'] = onsil
                        df_list.loc[n,'energy'] = energy 
     
            #이중칼럼
            elif type(col[0]) == tuple:
                col_name_list = []
                for col_name in col:
                    if '온실가스' in col_name[0] or '에너지' in col_name[0]:
                        col_name_list.append(col_name[0])
                        col_name_list = list(set(col_name_list))
                        if '계' in col_name[1] or '총량' in col_name[1] or '합' in col_name[1] or '총 량' in col_name[1]:
                            col_name_chong = col_name[1]
                            flag = 1
                        elif re.search('2020|\d{0,3}기\b', col_name[1]):
                            col_name_years = col_name[1]
                            flag = 2
                    elif re.search('2020|\d{0,3}기\b', col_name[0]) != None:
                        col_name_years = col_name[0]
                        if  re.search(r'[총합]?\s?계\b|총\s?량', col_name[1]) != None:
                            col_name_chong = col_name[1]
                            flag = 3
                        elif '온실가스' in col_name[1] or '에너지' in col_name[1]:
                            col_name_list.append(col_name[1])
                            col_name_list = list(set(col_name_list))
                            flag = 4
                        

                
                
                if flag == 1:
                    for num in range(len(tem)):
                        row_list = list(tem.iloc[num])
                        if re.search(r'[총합]?\s?계\b|총\s?량', str(row_list)) != None:
                            row_index = num
                            flag = 5
                            break
                        elif re.search('2020|\d{0,3}기\b', str(row_list)) != None:
                            row_index = num
                            flag = 6
                            break
                    if re.search(r'[총합]?\s?계|총\s?량',str(tem.iloc[:,0])) == None:
                        flag = 7
         
                if flag == 5:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    print('다중칼럼1 n: ', n)
                    if '온실가스' in str(col_name_list):
                        print('온실가스: ', tem[col_name_list[onsil_ind]][col_name_chong][row_index])
                        df_list.loc[n,'onsil'] = tem[col_name_list[onsil_ind]][col_name_chong][row_index]
                    else:
                        print('온실가스: -')
                        df_list.loc[n,'onsil'] = '-'
                    if '에너지' in str(col_name_list):
                        print('에너지: ', tem[col_name_list[energy_ind]][col_name_chong][row_index])
                        df_list.loc[n,'energy'] = tem[col_name_list[energy_ind]][col_name_chong][row_index]                          
                    else:
                        print('에너지: -')
                        df_list.loc[n,'energy'] = '-'          

                    print('-'*50)
                
                if flag == 6:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    print('다중칼럼2 n: ', n)
                    try:
                        if '온실가스' in str(col_name_list):
                            print('온실가스: ', tem[col_name_list[onsil_ind]][col_name_chong][row_index])
                            df_list.loc[n,'onsil'] = tem[col_name_list[onsil_ind]][col_name_chong][row_index]
                        else:
                            print('온실가스: -')
                            df_list.loc[n,'onsil'] = '-'
                        if '에너지' in str(col_name_list) and '에너지' in str(tem[col_name_list[energy_ind]]):
                            print('에너지: ', tem[col_name_list[energy_ind]][col_name_list[energy_ind]][row_index])
                            df_list.loc[n,'energy'] = tem[col_name_list[energy_ind]][col_name_list[energy_ind]][row_index]
                        elif '에너지' in str(col_name_list):
                            print('에너지: ', tem[col_name_list[energy_ind]][col_name_chong][row_index])
                            df_list.loc[n,'energy'] = tem[col_name_list[energy_ind]][col_name_chong][row_index]
                        else:
                            print('에너지: -')
                            df_list.loc[n,'energy'] = '-' 
                        print('-'*50)
                    except:
                        print('N번오류1-2', n)
                        print('-'*50)
                        break
                    
                if flag == 7:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    try:
                        if '온실가스' in str(col_name_list):
                            a = tem[col_name_list[onsil_ind]][col_name_chong]
                            if type(a[0]) == str:
                                a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                            sum_a = 0
                            for i in range(len(a)):
                                if a[i] != '':
                                    sum_a += float(a[i])                        
                            print('온실가스: ', sum_a)
                            df_list.loc[n,'onsil'] = sum_a
                        else:
                            print('온실가스: -')
                            df_list.loc[n,'onsil'] = '-' 
                            
                        if '에너지' in str(col_name_list) and '에너지' in str(tem[col_name_list[energy_ind]]):
                            a = tem[col_name_list[energy_ind]][col_name_list[energy_ind]]
                            if type(a[0]) == str:
                                a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                            sum_a = 0
                            for i in range(len(a)):
                                if a[i] != '':
                                    sum_a += float(a[i])                                                
                            print('에너지: ', sum_a)
                            df_list.loc[n,'energy'] = sum_a
                        elif '에너지' in str(col_name_list):
                            a = tem[col_name_list[energy_ind]][col_name_chong]
                            if type(a[0]) == str:
                                a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                            sum_a = 0
                            for i in range(len(a)):
                                if a[i] != '':
                                    sum_a += float(a[i])                                                
                            print('에너지: ', sum_a)
                            df_list.loc[n,'energy'] = sum_a
                        else:
                            print('에너지: -')
                            df_list.loc[n,'energy'] = '-' 
                        print('-'*50)   
                    except:
                        print('오류113')
                        break
                
                if flag == 2:
                    for num in range(len(tem)):
                        row_list = list(tem.iloc[num])
                        if re.search(r'[총합]?\s?계\b|총\s?량', str(row_list)) != None:
                            row_index = num
                            flag = 8
                            break
                    if re.search(r'[총합]?\s?계|총\s?량',str(tem.iloc[:,0])) == None:
                        flag = 9
                        
                if flag == 8:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    print('다중칼럼1-2-1 n: ', n)
                    if '온실가스' in str(col_name_list):
                        print('온실가스: ', tem[col_name_list[onsil_ind]][col_name_years][row_index])
                        df_list.loc[n,'onsil'] =  tem[col_name_list[onsil_ind]][col_name_years][row_index]
                    else:
                        print('온실가스: -')
                        df_list.loc[n,'onsil'] = '-'
                    if '에너지' in str(col_name_list):
                        print('에너지: ', tem[col_name_list[energy_ind]][col_name_years][row_index])
                        df_list.loc[n,'energy'] = tem[col_name_list[energy_ind]][col_name_years][row_index]
                    else:
                        print('에너지: -')
                        df_list.loc[n,'energy'] = '-'
                    print('-'*50)
                      
                if flag == 9:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    if '온실가스' in str(col_name_list):
                        a = tem[col_name_list[onsil_ind]][col_name_years]
                        if type(a[0]) == str:
                            a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                        sum_a = 0
                        for i in range(len(a)):
                            if a[i] != '':
                                sum_a += float(a[i])                        
                        print('온실가스: ', sum_a)
                        df_list.loc[n,'onsil'] = sum_a
                    else:
                        print('온실가스: -')
                        df_list.loc[n,'onsil'] = '-'
                        
                    if '에너지' in str(col_name_list) and '에너지' in str(tem[col_name_list[energy_ind]]):
                        a = tem[col_name_list[energy_ind]][col_name_list[energy_ind]]
                        if type(a[0]) == str:
                            a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                        sum_a = 0
                        for i in range(len(a)):
                            if a[i] != '':
                                sum_a += float(a[i])                                                
                        print('에너지: ', sum_a)
                        df_list.loc[n,'energy'] = sum_a
                    elif '에너지' in str(col_name_list):
                        a = tem[col_name_list[energy_ind]][col_name_years]
                        if type(a[0]) == str:
                            a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                        sum_a = 0
                        for i in range(len(a)):
                            if a[i] != '':
                                sum_a += float(a[i])                                                
                        
                        print('에너지: ', sum_a)
                        df_list.loc[n,'energy'] = sum_a
                    else:
                        print('에너지: -')
                        df_list.loc[n,'energy'] = '-'
                    print('-'*50)            
                
                if flag == 3:
                    row_list = list(tem.iloc[:,0])
                    for i in range(len(row_list)):
                        if '온실가스' in row_list[i]:
                            row_onsil_ind = i
                        elif '에너지' in row_list[i]:
                            row_energy_ind = i
                    if '온실가스' in row_list[i] and '에너지' in row_list[i]:
                        df_list.loc[n,'onsil'] = tem[col_name_years][col_name_chong][row_onsil_ind]
                        df_list.loc[n,'energy'] = tem[col_name_years][col_name_chong][row_energy_ind]
                    elif '온실가스' in row_list[i] and '에너지' not in row_list[i]:
                        df_list.loc[n,'onsil'] = tem[col_name_years][col_name_chong][row_onsil_ind]
                        df_list.loc[n,'energy'] = '-'
                    elif '온실가스' not in row_list[i] and '에너지' in row_list[i]:
                        df_list.loc[n,'onsil'] = '-'
                        df_list.loc[n,'energy'] = tem[col_name_years][col_name_chong][row_energy_ind]
                        
                if flag == 4:
                    for num in range(len(tem)):
                        row_list= list(tem.iloc[num])
                        if re.search(r'[총합]?\s?계\b|총\s?량', str(row_list)) != None:
                            row_index = num
                            flag = 10
                            break
                    if re.search(r'[총합]?\s?계|총\s?량',str(tem.iloc[:,0])) == None:
                        flag = 11
                    
                if flag == 11:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    if '온실가스' in str(col_name_list):
                        a = tem[col_name_years][col_name_list[onsil_ind]]
                        if type(a[0]) == str:
                            a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                        sum_a = 0
                        for i in range(len(a)):
                            if a[i] != '':
                                sum_a += float(a[i]) 
                        print('다중칼럼222', n)
                        print('온실가스: ', sum_a)
                        df_list.loc[n,'onsil'] = sum_a
                        
                    else:
                        print('다중칼럼222', n)                        
                        print('온실가스: -')
                        df_list.loc[n,'onsil'] = '-'
                        
                    if '에너지' in str(col_name_list):
                        a = tem[col_name_years][col_name_list[energy_ind]]
                        if type(a[0]) == str:
                            a = a.apply(lambda x: re.sub('[-,\s]|[가-힣]|[a-zA-Z]',"",x))
                        sum_a = 0
                        for i in range(len(a)):
                            if a[i] != '':
                                sum_a += float(a[i])                                                                   
                        print('에너지: ', sum_a)
                        df_list.loc[n,'energy'] = sum_a
                    else:
                        print('에너지: -')
                        df_list.loc[n,'energy'] = '-'
                    print('-'*50)            
                          
                if flag == 10:
                    for li in range(len(col_name_list)):
                        if '온실가스' in str(col_name_list[li]):
                            onsil_ind = li
                        elif '에너지' in str(col_name_list[li]):
                            energy_ind = li
                    print('다중칼럼221 n: ', n)
                    if '온실가스' in str(col_name_list):
                        print('온실가스: ', tem[col_name_years][col_name_list[onsil_ind]][row_index])
                    else:
                        print('온실가스: -')
                    if '에너지' in str(col_name_list):
                        print('에너지: ', tem[col_name_years][col_name_list[energy_ind]][row_index])
                    else:
                        print('에너지: -')
                    print('-'*50)
                    
                    

for i in range(len(df_list)):
    if type(df_list['onsil'][i]) == str:
        df_list['onsil'][i] = re.sub(r'[^0-9]', '', df_list['onsil'][i])
    if type(df_list['energy'][i]) == str:
        df_list['energy'][i] = re.sub(r'[^0-9]', '', df_list['energy'][i])
    if df_list['onsil'][i] == '' :
        df_list['onsil'][i] = None
    if df_list['energy'][i] == '':
        df_list['energy'][i] = None
        
for i in range(len(df_list)):
    if df_list['onsil'][i] != None :
        df_list['onsil'][i] = float(df_list['onsil'][i])
    if df_list['energy'][i] != None :
        df_list['energy'][i] = float(df_list['energy'][i])
        
for i in range(len(df_list)):
    if df_list['onsil'][i] == None or df_list['energy'][i] == None:
        print(df_list['company'][i])

df_list.to_csv(r'C:/Users/jinho/OneDrive/바탕 화면/녹색경영부분/2020totalreport_ver2.csv', encoding = 'utf-8', index = False)

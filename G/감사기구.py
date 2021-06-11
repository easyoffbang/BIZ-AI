# -*- coding: utf-8 -*-
"""
Created on Mon May 24 01:43:31 2021

@author: jinho
"""



import pandas as pd
import re


def refine(text):
    return re.sub('<.+?>', '\n', text)

#자산 붙이기
report = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/학교/AI랩/프로젝트/기타자료및코드/사업보고서G/reportVI123_2019.csv', encoding = 'utf-8')
jasan = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/자산/jasan_2019_.csv',encoding = 'utf-8')
#jasan.drop(['Unnamed: 3'], axis = 1, inplace = True)
report.drop(['Unnamed: 0'], axis = 1, inplace = True)
jasan_list = list(jasan['jasan'])
report['jasan'] = jasan_list
name_list = list(report['name'])

report['jasan'][1]





#3. 주주이전
tempt_list = []
for i in range(len(report)):
    try:
        gamsa_start = re.search(r'2. 감사제도에 관한 사항<', report['content'][i])
        gamsa_before = re.search(r'3. 주주의 의결권 행사에 관한 사항<', report['content'][i])
        ind = gamsa_before.start()
        ind2 = gamsa_start.start()
        content = report['content'][i][ind2:ind]
    #    content = report['content'][i][:ind]
        tempt_list.append(content)
    except:
        tempt_list.append(None)


#위원회 있는지
check_list = []
for i in range(len(tempt_list)):
    if tempt_list[i] != None:
        check = re.search(r'감사위원회.+', tempt_list[i])
        if check != None:
            check_list.append(tempt_list[i])
#            ind = check.start()
#            content = tempt_list[i][ind:]
#            check_list.append(content)
        else:
            check_list.append('감사x')
    else:
        check_list.append(None)

#일반 감사인 애들
gamsa_list = []
for i in range(len(check_list)):
    if check_list[i] != None:
        check = re.search(r'감사위원회\s?없|감사위원회[^\.\n\-]*(?:해당\s?사항|(?:설치|구성)[^\.\n\-]*(?:않|아니[^지만]|없[^으나])[^는]|감사제도로\s?변경|미설치)|(?:상임)?감사(?:\(상근\))?[가-힣]?\s?(?:비?상근\s?감사|1명|1인)|감사x|(?:상근|비상근)(감\s?사)[가-힣]\s?(?:1|2)(?:명|인)', check_list[i])
        if check != None:
            gamsa_list.append('감사')
        else:
            gamsa_list.append(check_list[i])
    else:
        gamsa_list.append(check_list[i])
        
#감사위원회가 설치되었다는 내용있는지 다시 확인
for i in range(len(check_list)):
    if check_list[i] != None:
        check = re.search(r'감사위원회(?:가|를)\s?(?:설치\s?(?:되었|하였)|운영하고)', check_list[i])
        if check != None:
            gamsa_list[i] = check_list[i]
        else:
            pass
    else:
        pass

#감사이 아닌애들 중에 표를 통해서 사람 수를 살펴보고 위원회인지 판별
pyo_list = []
r = re.compile('<.*table.*>')
l = re.compile('[가-힣]\.\s?준법지원인')
for i in range(len(gamsa_list)):
    if gamsa_list[i] != None:
        if gamsa_list[i] != '감사':
            junbub = l.search(gamsa_list[i])
            if junbub != None:
                ind = junbub.start()
                gamsa_list[i] = gamsa_list[i][:ind]
            tempt_cont_list = []
            table_ind = []
            table_start = []
            table_end = []
            for m in r.finditer(gamsa_list[i]):
                table_ind.append(m.start())
            for x in range(len(table_ind)):
                if x % 2 != 0:
                    table_end.append(table_ind[x])
                elif x % 2 == 0:
                    table_start.append(table_ind[x])
            for y in range(len(table_start)):
                try:
                    tempt = gamsa_list[i][table_start[y]:table_end[y]]
                    check = re.search(r'성\s*명|감사위원회\s?위원\b|구성원|위원명', tempt)
                    if check != None:
                        tempt = pd.read_html(gamsa_list[i][table_start[y]:table_end[y]])
                        tempt_cont_list.append(tempt)
                except:
                    print('표나누기오류', i)
                    break
            pyo_list.append(tempt_cont_list)
        else:
            pyo_list.append('감사')
    else:
        pyo_list.append(None)

#칼럼명이 인덱스인 애들 변환
for i in range(len(pyo_list)):
    if pyo_list[i] != None:
        if type(pyo_list[i]) == list:
            for n in range(len(pyo_list[i])):
                col = list(pyo_list[i][n][0].columns)
                if type(col[0]) == tuple:
                    pass
                elif type(col[0]) != str:
                    m = list(pyo_list[i][n][0].loc[0])
                    pyo_list[i][n][0].columns = m
                    pyo_list[i][n][0] = pyo_list[i][n][0].drop(index = 0, axis = 0)
                    pyo_list[i][n][0] = pyo_list[i][n][0].reset_index(drop=True)
                else:
                    pass
                pyo_list[i][n] = pyo_list[i][n][0]
    else:
        pyo_list[i] = '사업보고서체크'
                             


#성명 칼럼이 있는 첫번째 표 가져오기
for i in range(len(pyo_list)):
    if pyo_list[i] != None:
        if type(pyo_list[i]) == list and len(pyo_list[i]) != 0:
            for n in range(len(pyo_list[i])):
                if type(pyo_list[i]) != str:
                    col = pyo_list[i][n].columns
                    m = re.compile(r'성\s*명|감사위원회\s?위원\b|구성원|위원명')
                    ch = m.search(str(col))
                    if ch != None:
                        pyo_list[i] = pyo_list[i][n]
                        break
                    else:
                        print('성명없는애들', i)
                        pyo_list[i] = '사업보고서체크'
    else:
        pass




#변환
for i in range(len(pyo_list)):
    if type(pyo_list[i]) != str and len(pyo_list[i]) != 0:
        if len(pyo_list[i]) < 3:
            col = pyo_list[i].columns
            if type(col[0]) != tuple:
                m = re.compile(r'성\s*명|감사위원회\s?위원\b|구성원|위원명')
                for cl in col:
                    a = m.search(cl)
                    if a != None:
                        col_person = cl
                        break
                tempt_col = re.sub('\(.+?\)|[^가-힣a-zA-z]','',pyo_list[i][col_person][0])
                if len(tempt_col) > 6:
                    pyo_list[i] = '감사위원회'
                    print('1', i)
                else:
                    col_check = re.compile(r'사외이사|비\s*고|구\s*분|직\s*위')
                    for col_name in col:
                        b= col_check.search(col_name)
                        if b != None:
                            col_bigo = col_name
                            break
                    if b != None:
                        sawae_row = str(list(pyo_list[i][col_bigo]))
                        sawae = re.compile(r'사외\s?이사|사내\s?이사|○|예|O')
                        check_sawae = sawae.search(str(sawae_row))
                        if check_sawae != None:
                            pyo_list[i] = '감사위원회'
                            print('2', i)
                        else:
                            pyo_list[i] = '감사'
                            print('3', i)
                    else:
                        pyo_list[i] = '감사'
                        print('4', i)
            else:
                pyo_list[i] = '사업보고서체크'
                print('튜플칼럼', i)
        else:
            pyo_list[i] = '감사위원회'
            print('5', i)
    elif type(pyo_list[i]) == list:
        pyo_list[i] = '감사위원회'   

report['jasan'][674]
jasan_list = []
for i in range(len(report)):
    report['jasan'][i] = report['jasan'][i].replace(',','')
    if float(report['jasan'][i]) > 2000000000000:
        jasan_list.append(1)
    else:
        jasan_list.append(0)

label_list = list(report['label'])
com_df = report.drop(['content', 'label', 'jasan'], axis=1)

com_df['gamsa'] = pyo_list
com_df['jasan'] = jasan_list
com_df['label'] = label_list
com_df.to_csv(r'C:/Users/jinho/OneDrive/바탕 화면/gamsa/gamsa_2019.csv', encoding = 'utf-8', index = False)        

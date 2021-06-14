# -*- coding: utf-8 -*-
"""
Created on Mon May 17 18:38:32 2021

@author: jinho
"""

import pandas as pd
import re

report = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/학교/AI랩/프로젝트/기타자료및코드/사업보고서G/2016totalreport.csv', encoding = 'utf-8')
report.drop(['Column1'], axis = 1, inplace = True)


#report내부 V.감사인의 감사의견 부분만 남기기
#2016년도부터 V.감사인의 감사의견이 됨
#그전에는 IV.감사인의 감사의견
i = 0
report_VI = pd.DataFrame(columns = ['code', 'name','content','label'])
for a in range(len(report)):
    if a == i:
        report_VI = report_VI.append(report.loc[i])
        i += 5
    else:
        pass
report_VI.reset_index(inplace = True, drop = True)


#내용부분만 따로 뽑아서 dataframe으로 만듦.
name_list = list(report_VI['name'])
cont_list = list(report_VI['content'])
t = []
for i in range(len(cont_list)):
        c = pd.read_html(cont_list[i])
        t.append(c)



#감사용역 표 리스트
yong_list = []
yong = re.compile(r'(?<!용역)(?!용역\s)보\s?수(?!\s등).*')
for i in range(len(t)):
    for n in range(len(t[i])):
        col = list(t[i][n].columns)
        if type(col[0]) == str:
            col = str(col)
            y = yong.search(col)
            if y != None:
                yong_list.append(t[i][n])
                break
        else:
            m = list(t[i][n].loc[0])
            t[i][n].columns = m
            t[i][n] = t[i][n].drop(index = 0, axis = 0)
            t[i][n] = t[i][n].reset_index(drop=True)
            col = str(m)
            y = yong.search(col)
            if y != None:
                yong_list.append(t[i][n])
                break            
    if y == None:
        print(i)
        yong_list.append(0)
 

#비감사용역 표 리스트
not_list = []
not_yong = re.compile(r'(?:용역\s?보수[^와과가는]\s?.*|용역\s?보수(?!와)(?!는)(?!가)(?!는))')
for i in range(len(t)):
    for n in range(len(t[i])):
        col = list(t[i][n].columns)
        if type(col[0]) == str:
            col = str(col)
            y = not_yong.search(col)
            if y != None:
                not_list.append(t[i][n])
                break
        else:
            try:
                m = list(t[i][n].loc[0])
                t[i][n].columns = m
                t[i][n] = t[i][n].drop(index = 0, axis = 0)
                t[i][n] = t[i][n].reset_index(drop=True)
                col = str(m)
                y = not_yong.search(col)
                if y != None:
                    not_list.append(t[i][n])
                    break
            except:
                print(i)
                pass
    if y == None:
        print(i)
        not_list.append(0)


#비감사용역 없거나 이상한거 갯수
a=0
for i in not_list:
    if type(i) == int:
        a+=1

#감사용역 없거나 이상한거 갯수
b=0
for i in yong_list:
    if type(i) == int:
        b+=1

#감사용역 보수 리스트
bosu_list = []
for e in range(len(yong_list)):
    tempt_list = []
    time = yong_list[e].iloc[0,0]
    col_time = None
    col_bosu = None
    for i in range(len(yong_list[e])):
        if yong_list[e].iloc[i,0] == time:
            col_name = list(yong_list[e].columns)
            p = re.compile(r'.*시간.*')
            l = re.compile(r'(?<!용역)(?!용역\s)보\s?수(?!\s등).*')
            for n in range(len(col_name)):
                tempt = p.findall(col_name[n])
                tempt2 = l.findall(col_name[n])
                if len(tempt) != 0:
                    col_time = tempt[0]

                if len(tempt2) != 0:
                    col_bosu = tempt2[0]

            if i != 0:
                if yong_list[e][col_time][i] == yong_list[e][col_time][i-1]:
                    pass
                else:
                    tempt_list.append(yong_list[e][col_bosu][i])
            else:
                tempt_list.append(yong_list[e][col_bosu][i])
        else:
            print(e)
    bosu_list.append(tempt_list)

#단위구하기
def refine(text):
    return re.sub('<.+?>', '', text)
report_VI['content'] = report_VI['content'].apply(lambda x: refine(x))
cont_list2 = list(report_VI['content'])
gamsa_unit_list = []
gamsa = re.compile(r'(?<!비)\s?감사\s?용역\s?(?:계약)?\s?체결\s?현|보수\s?(?:현황|내역)')
beegamsa = re.compile(r'비\s?감사\s?용역\s?계약\s?(?:체결)?\s?(?:현황)?|감사인과의\s?비\s?감사\s?용역|비\s?감사\s?용역\s?체결\s?현황')
x = re.compile(r'단\s?위\s?:?.{0,30}\)')
for i in range(len(cont_list2)):
    tt = gamsa.search(cont_list2[i])
    tt2 = beegamsa.search(cont_list2[i])
    if tt != None:
        if tt2 != None:
            ind1 = tt.end()
            ind2 = tt2.start()
            unit = x.findall(cont_list2[i][ind1:ind2])
            gamsa_unit_list.append(unit)            
        else:
            ind1 = tt.end()
            unit = x.findall(cont_list2[i][ind1:1500])
            gamsa_unit_list.append(unit)
    else:
        gamsa_unit_list.append('없거나체크')
        print(i)


#행에서뽑은 단위랑 통합
u = re.compile(r'(?:[가-힣]*(?:원|만)|USD|usd|U\$)')
for i in range(len(bosu_list)):
    if len(gamsa_unit_list[i]) == 0:
        if type(bosu_list[i][0]) == str:
            o = u.findall(bosu_list[i][0])
            gamsa_unit_list[i] = o
        else:
            pass


#단위 통일
for i in range(len(gamsa_unit_list)):
    if len(gamsa_unit_list[i]) > 0:
        a = re.search(r'\b원', str(gamsa_unit_list[i][0]))
        b = re.search(r'천원', str(gamsa_unit_list[i][0]))
        c = re.search(r'\b만원', str(gamsa_unit_list[i][0]))
        d = re.search(r'십만', str(gamsa_unit_list[i][0]))
        e = re.search(r'백만', str(gamsa_unit_list[i][0]))
        f = re.search(r'천만', str(gamsa_unit_list[i][0]))
        g = re.search(r'억', str(gamsa_unit_list[i][0]))
        h = re.search(r'USD|usd', str(gamsa_unit_list[i][0]))
        if a is not None:
            gamsa_unit_list[i] = 1
        elif b is not None:
            gamsa_unit_list[i] = 1000
        elif c is not None:
            gamsa_unit_list[i] = 10000
        elif d is not None:
            gamsa_unit_list[i] = 100000
        elif e is not None:
            gamsa_unit_list[i] = 1000000
        elif f is not None:
            gamsa_unit_list[i] = 10000000
        elif g is not None:
            gamsa_unit_list[i] = 100000000
        elif h is not None:
            gamsa_unit_list[i] = 1100
        else:
            print(gamsa_unit_list[i])
            pass
    else:
        gamsa_unit_list[i] = 1




#보수 금액 리스트 내부 글자 및 특문 제거 및 int로 변환
for i in range(len(bosu_list)):
    if type(bosu_list[i][0]) == str:
        if len(bosu_list[i]) > 1:
            for a in range(len(bosu_list[i])):
                no_ko = re.sub(r'[가-힣,]','',bosu_list[i][a])         
                find_num = re.compile(r'\d+\.\d+|\d+')
                num = find_num.findall(no_ko)
                bosu_list[i][a] = num[0]
            bosu_list[i] = sum(bosu_list[i])
        else:
            no_ko = re.sub(r'[가-힣,]','',bosu_list[i][0])
            find_num = re.compile(r'\d+\.\d+|\d+')
            num = find_num.findall(no_ko)
            if '.' in str(num):
                bosu_list[i] = float(num[0])
            else:
                bosu_list[i] = int(num[0])
    else:
        bosu_list[i] = sum(bosu_list[i])
                

bosu_df = report_VI.drop(['content'],axis=1)
bosu_df['gamsa_bosu'] = bosu_list
bosu_df['unit'] = gamsa_unit_list







#비감사용역 보수 리스트
type(not_list[229])
not_bosu_list = []
for e in range(len(not_list)):
    tempt_list = []
    if type(not_list[e]) != int:
        time = not_list[e].iloc[0,0]
        col_time = None
        col_bosu = None
        for i in range(len(not_list[e])):
            if not_list[e].iloc[i,0] == time:
                col_name = list(not_list[e].columns)
                p = re.compile(r'.*시간.*')
                l = re.compile(r'용역\s?보수\s?.*')
                for n in range(len(col_name)):
                    tempt = p.findall(col_name[n])
                    tempt2 = l.findall(col_name[n])
                    if len(tempt) != 0:
                        col_time = tempt[0]
    
                    if len(tempt2) != 0:
                        col_bosu = tempt2[0]
                        print(tempt2)
                if col_time != None:
                    if i != 0:
                        if not_list[e][col_time][i] == not_list[e][col_time][i-1]:
                            pass
                        else:
                            tempt_list.append(not_list[e][col_bosu][i])
                    else:
                        tempt_list.append(not_list[e][col_bosu][i])
                elif col_time == None:
                        tempt_list.append(not_list[e][col_bosu][i])              
            else:
                print(e)
                
    not_bosu_list.append(tempt_list)


l.findall(col_name[0])



#-를 0으로 변환, []인 애들 체크필요
for i in range(len(not_bosu_list)):
    if len(not_bosu_list[i]) == 0:
        not_bosu_list[i] = '체크필요'
        print(i)
    else:
        for m in range(len(not_bosu_list[i])):
            if not_bosu_list[i][m] == '-':
                not_bosu_list[i][m] = 0

#단위구하기
beegamsa = re.compile(r'비\s?감사\s?용역\s?계약\s?(?:체결)?\s?(?:현황)?|감사인과의\s?비\s?감사\s?용역|비\s?감사\s?용역\s?체결\s?현황')
x = re.compile(r'단\s?위\s?:?.{0,30}\)')
beegamsa_unit_list = []
for i in range(len(cont_list2)):
    tt2 = beegamsa.search(cont_list2[i])
    if tt2 != None:
        ind1 = tt2.end()
        unit = x.findall(cont_list2[i][ind1:])
        beegamsa_unit_list.append(unit)
    else:
        beegamsa_unit_list.append('없거나체크')
        print(i)





#행단위랑 합치기
for i in range(len(not_bosu_list)):
    if len(not_bosu_list[i]) != 0:
        if len(beegamsa_unit_list[i]) == 0:
            if type(not_bosu_list[i][0]) == str:
                o = u.findall(not_bosu_list[i][0])
                beegamsa_unit_list[i] = o
            else:
                pass


#특수문자와 한글 제거
for i in range(len(not_bosu_list)):
    if type(not_bosu_list[i]) == list:
            if len(not_bosu_list[i]) > 1:
                for a in range(len(not_bosu_list[i])):
                    if type(not_bosu_list[i][a]) == str:
                        if 'USD' in not_bosu_list[i][a] or 'U$' in not_bosu_list[i][a] or '환급' in not_bosu_list[i][a] or '보수'in not_bosu_list[i][a] or '미불'in not_bosu_list[i][a]:
                            pass
                        else:
                            no_ko = re.sub(r'[,]','',not_bosu_list[i][a])
                            find_num = re.compile(r'\d+\.\d+|\d+')
                            num = find_num.findall(no_ko)
                            if '.' in str(num):
                                list_a = list(map(float, num))
                                sum_n = sum(list_a)
                                not_bosu_list[i][a] = sum_n                                
                            else:
                                list_a = list(map(int, num))
                                sum_n = sum(list_a)
                                not_bosu_list[i][a] = sum_n
                if 'USD' in str(not_bosu_list[i]) or 'U$'in str(not_bosu_list[i]) or '환급' in str(not_bosu_list[i]) or '보수' in str(not_bosu_list[i]) or '미불' in str(not_bosu_list[i]):
                    pass
                else:
               
                    list_a = list(map(int, not_bosu_list[i]))
                    sum_n = sum(list_a)
                    not_bosu_list[i] = sum_n
                    print(i)
                        
            else:
                if type(not_bosu_list[i][0]) == str:
                    if 'U$' in not_bosu_list[i][0] or '미불'in not_bosu_list[i][0] or '환급' in not_bosu_list[i][0] or '보수'in not_bosu_list[i][0]:
                        not_bosu_list[i] = not_bosu_list[i][0]
                        pass
                    else:
                        try:
                            no_ko = re.sub(r'[백십천만억,]','',not_bosu_list[i][0])
                            no_ko = re.sub(r'[원]',',', no_ko)
                            find_num = re.compile(r'\d+\.\d+|\d+')
                            num = find_num.findall(no_ko)
                            if '.' in str(num):
                                list_a = list(map(float, num))
                                sum_n = sum(list_a)
                                not_bosu_list[i] = sum_n                                     
                            else:
                                list_a = list(map(int, num))
                                sum_n = sum(list_a)
                                not_bosu_list[i] = sum_n               
                        except:
                            print(i)
                            pass
                else:
                    not_bosu_list[i] = not_bosu_list[i][0]



            
#단위 통일
for i in range(len(beegamsa_unit_list)):
    if len(beegamsa_unit_list[i]) > 0:
        a = re.search(r'\b원', str(beegamsa_unit_list[i][0]))
        b = re.search(r'천원', str(beegamsa_unit_list[i][0]))
        c = re.search(r'\b만원', str(beegamsa_unit_list[i][0]))
        d = re.search(r'십만', str(beegamsa_unit_list[i][0]))
        e = re.search(r'백만', str(beegamsa_unit_list[i][0]))
        f = re.search(r'천만', str(beegamsa_unit_list[i][0]))
        g = re.search(r'억', str(beegamsa_unit_list[i][0]))
        h = re.search(r'USD|usd', str(beegamsa_unit_list[i][0]))
        if a is not None:
            beegamsa_unit_list[i] = 1
        elif b is not None:
            beegamsa_unit_list[i] = 1000
        elif c is not None:
            beegamsa_unit_list[i] = 10000
        elif d is not None:
            beegamsa_unit_list[i] = 100000
        elif e is not None:
            beegamsa_unit_list[i] = 1000000
        elif f is not None:
            beegamsa_unit_list[i] = 10000000
        elif g is not None:
            beegamsa_unit_list[i] = 100000000
        elif h is not None:
            beegamsa_unit_list[i] = 1100
        else:
            print(beegamsa_unit_list[i])
            pass
    else:
        beegamsa_unit_list[i] = 1

bosu_df['beegamsa_bosu'] = not_bosu_list
bosu_df['beegamsa_unit'] = beegamsa_unit_list

bosu_df['gamsa'] = None
bosu_df['beegamsa'] = None 
bosu_df['bosu_ratio'] = None
for i in range(len(bosu_df)):
    try:
        bosu_df['gamsa'][i] = bosu_df['gamsa_bosu'][i] * bosu_df['unit'][i]
        bosu_df['beegamsa'][i] = bosu_df['beegamsa_bosu'][i] * bosu_df['beegamsa_unit'][i]
        bosu_df['bosu_ratio'][i] = bosu_df['beegamsa'][i] / bosu_df['gamsa'][i]
    except:
        pass
        
for i in range(len(bosu_df)):
    if bosu_df['bosu_ratio'][i] == None or bosu_df['bosu_ratio'][i] > 10:
        bosu_df['bosu_ratio'][i] = '체크 필요'


bosu_df.to_csv(r'C:/Users/jinho/OneDrive/바탕 화면/bosu/2016_bosu.csv',index = False, encoding = 'utf-8')

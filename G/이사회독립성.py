# -*- coding: utf-8 -*-
"""
Created on Sat May 15 16:57:02 2021

@author: jinho
"""

import pandas as pd
import re

report_VI = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/학교/AI랩/프로젝트/기타자료및코드/사업보고서G/reportVI123_2019.csv', encoding = 'utf-8')
report_VI.drop(['Unnamed: 0'], axis = 1, inplace = True)

for i in range(len(report_VI)):
    if type(report_VI['content'][i]) == float:
        report_VI['content'][i] = '없음'
        



#Tag지우기
def refine(text):
    return re.sub('<.+?>', '', text)
report_VI['content'] = report_VI['content'].apply(lambda x: refine(x))


#정규식 추출
out_list = []
chong_list = []
name_list = []
content_list = []
c = 0
for i in range(len(report_VI)):
    # 1.이사회에 관한~ 부분만 남기기
    gaeyo_after = re.search(r'\b\w{1}\.\s+감사제도에', report_VI['content'][i])
    try:
        ind = gaeyo_after.start()
        content = report_VI['content'][i][:ind]
        content_list.append(content)
    except:
        print('체크: ', report_VI['name'][i])
        content = report_VI['content'][i]
    r = re.compile(r'(?:사외이사는?\s?\d{1,2}(?:명|인)?|\d{1,2}(?:명|인)(?:은|의)\s?[가-힣]{0,3}\s?사외이사)|사외\s?이사\s?:\s?\d{1,2}(?:명|인)|사외\s?이사\s?\(\d{1,2}(?:명|인)\)')
    l = re.compile(r'(?:(?<!위원회는\s)(?<!위원회는)\d{1,2}(?:명|인)\((?:[가-힣]{4}|\d).{0,40}\)(?:의?\s?이사|으로)|등기이사\s?\d{1,2}(?:명|인)\(|(?:당사는|이사회는)\s?(?:이사\s?)?\d{1,2}(?:명|인)(?:으로|과)|(?<!:\s총)(?<!:\s총\s)(?<!위원회는\s)\d{1,2}(?:명|인)(?:으로\s?구성)?\s?\([가-힣]{4,}\s?\d{1,2}.{0,40}\)|(?<!:\s)(?<!\()(?<!사외이사는\s)(?:총|이사\s?총\s?수)\s*\d{1,2}\s?(?:명|인)|(?<!위원회는\s)(?<!위원회는)(?<!감사)(?<!감사\s)(?<!이사)(?<!이사\s)\d{1,2}(?:명|인)의\s?(?:이사|등기\s?임원)[^를을와과]|이사의\s수\s?:\s?\d{1,2}(?:명|인)?|(?:등|의)\s*\d{1,2}(?:명|인)|(?<!:\s)(?<!\()(?<!사외이사는\s)(?:포함한|포함하여)\s*\d{1,2}\s?(?:명|인)으로|(?:명|인)의\s?[가-힣]{2,3}이사\s\d{1,2}\s?(?:명|인)으로\s?구성|당사의\s?이사\s?\d{1,2}(?:명|인))')
    out = r.findall(content[:1000])
    chong = l.findall(content)
    name_list.append(report_VI['name'][i])
    if len(chong) == 0:
        p = re.compile(r'당사의\s?.{0,70}\d{1,2}(?:명|인).+?\.|구성\s?:\s?.+(?:이사|임원)\s?\d{1,2}(?:명|인)|(?<!위원회는\s)\d{1,2}\s?(?:명|인)(?!이상)(?!이내)(?!\s이내)(?!\s이상)[^.\n]+?\n?[^.\n]+?(?<!이내로\s)(?<!이상의\s이사로\s)(?:구성|으로|두고)')
        el = p.findall(content)
        print('-'*50)
        print('i: ',i)

        if len(el) != 0:
            el[0] = re.compile('\d{1,2}(?:인|명)을\s?(?:포함한|포함하여)|중\s?\d{1,2}(?:명|인)|\d{4}년\s?\d{1,2}월\s?\d{1,2}일|(?<!이사\s)(?<!이사)(?<!임원\s)(?<!임원)\d{1,2}(?:명|인)(?:의|은|는)?\s?(?:[가-힣]*\s?감사|감사\s?[가-힣]*)|(?:[가-힣]+감사|감사[가-힣]+)(?:의|은|는)?\s?\d{1,2}(?:명|인)').sub('',el[0])
            print(el[0])
            num = re.compile('\d{1,2}')
            n = list(map(int, num.findall(el[0])))
            chong_num = sum(n)
            chong_list.append(chong_num)
        else:
            chong_list.append(el)
        c += 1
    else:
        num = re.compile('\d{1,2}')
        n = list(map(int, num.findall(chong[0])))
        chong_num = max(n)
        chong_list.append(chong_num)
        
    if len(out) != 0:
        num2 = re.compile(r'\d{1,2}')
        n2 = num2.findall(out[0])
        out_num = int(n2[0])
        out_list.append(out_num)
    else:
        out_list.append(out)

#총 이사인원 빈값체크
a=0
for i in range(len(chong_list)):
    if type(chong_list[i]) != int:
        print(i)
        a += 1
print(a)

#사외이사인원 빈값체크
b=0
for i in range(len(out_list)):
    if type(out_list[i]) != int:
        b += 1
print(b)


inde = report_VI.drop(['content'],axis=1)
inde['independent'] = out_list
inde['total_director'] = chong_list

#사외이사 수가 전체 인원 수 보다 큰거 체크
for i in range(len(inde)):
    if type(inde['independent'][i]) == int and type(inde['total_director'][i]) == int:
        if inde['independent'][i] > inde['total_director'][i]:
            print(i)
            print(inde['name'][i])

#사외이사 비율 구하기
inde['inde_rate'] = 0.0
for i in range(len(inde)):
    try:
        inde['inde_rate'][i] = inde['independent'][i] / inde['total_director'][i]
        if inde['inde_rate'][i] > 1:
            inde['inde_rate'][i] = '체크필요'
    except:
        inde['inde_rate'][i] = '체크필요'

inde.to_csv(r'C:\Users\jinho\OneDrive\바탕 화면\inde_rate\inde_2019.csv',index = False, encoding = 'utf-8')



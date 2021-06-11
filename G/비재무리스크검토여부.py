# -*- coding: utf-8 -*-
"""
Created on Thu May 20 01:01:56 2021

@author: jinho
"""


import pandas as pd
import re

report = pd.read_csv(r'C:/Users/jinho/OneDrive/바탕 화면/학교/AI랩/프로젝트/기타자료및코드/사업보고서G/reportVI123_2019.csv', encoding = 'utf-8')
report.drop(['Unnamed: 0'], axis = 1, inplace = True)
a = report['content'][400]
b = pd.read_html(a)
name_list = list(report['name'])

def refine(text):
    return re.sub('<.+?>', '\n', text)


#3.주주 ~~ 이전
tempt_list = []
for i in range(len(report)):
    try:
        gamsa_before = re.search(r'3. 주주의 의결권 행사에 관한 사항<', report['content'][i])
        ind = gamsa_before.start()
        content = report['content'][i][:ind]
        tempt_list.append(content)
    except:
        tempt_list.append(None)
        print('오류1: ',i)
        


#테이블 중 안건내용 같은거 있는 애들만
cont_list = []
r = re.compile('<.*table.*>')
for i in range(len(tempt_list)):
    tempt_cont_list = []
    table_ind = []
    table_start = []
    table_end = []
    try:
        for m in r.finditer(tempt_list[i]):
            table_ind.append(m.start())
        for x in range(len(table_ind)):
            if x % 2 != 0:
                table_end.append(table_ind[x])
            elif x % 2 == 0:
                table_start.append(table_ind[x])
        for y in range(len(table_start)):
            tempt = tempt_list[i][table_start[y]:table_end[y]]
            l = re.compile(r'>일\s?시|회\s?차|개\s?최\s?일\s?자\s?|>날\s?짜|심\s*의\s*안\s*건|(?:의\s*안|안\s*건\s*)\s*(?:내\s*용\s*|제\s*목)')
            check = l.search(tempt)
            if check != None:
                tempt_cont_list.append(tempt)
        cont_list.append(tempt_cont_list)
    except:
        cont_list.append(None)        

#빈거있는지 체크
for i in range(len(cont_list)):
    try:
        if len(cont_list[i]) == 0:
            print('빈거: ', i)
    except:
        pass
#태그를 \n으로 변환 후 split
for i in range(len(cont_list)):
    try:
        for n in range(len(cont_list[i])):
            non_tag = refine(cont_list[i][n])
            split_list = non_tag.split('\n')
            cont_list[i][n] = list(set(split_list))
    except:
        cont_list[i] = None

#ESG관련 키워드 리스트
esg_list = ['내부감시장치', '투표제', 'CSR', '평생교육시설', '온실가스', '거버넌스위원회', '공정거래', '청탁금지법', '사내근로복지기금', '기부',
            '사회공헌', '스튜어드십', '청정설비','친환경', '자금세탁방지', '이웃돕기', '피해자구제', '직무청렴계약','자율준수관리자', 
            '캠페인', '퇴직연금', '성금','탄소중립','ESG','투표제','소수주주권', '동반성장', '격려금', '투명경영','성과급', '지속가능경영위원회', 
            '코로나19', '후원', '지역경제활성화', '피해극복', '피해지원', '소비자보호실태평가', '내부통제기준', '준법감시', '준법지원', '사고관리', '사회복지', '그린에너지', 
            '내부회계관리제도', '지배구조개선', '전자투표', '전자위임장', '복리후생', '폐기물', '격려금', '윤리경영', '동반성장', '배출권', '장애인', '재난구호', '재난지원']

#키워드와 내부 내용 매칭
num_list = []
for i in range(len(cont_list)):
    num = 0
    try:
        for u in range(len(cont_list[i])):
            for sent in range(len(cont_list[i][u])):
                for x in esg_list:
                    check = cont_list[i][u][sent].replace(' ','')
                    if x in check:
                        num +=1
                        break
        num_list.append(num)
    except:
        num_list.append(None)

report_complete = report.drop(['content', 'label'], axis = 1)
report_complete['non_jaemoo'] = num_list
report_complete.to_csv(r'C:/Users/jinho/OneDrive/바탕 화면/비재무리스크검토/2019_non_jaemoo.csv', encoding= 'utf-8', index = False)
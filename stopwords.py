# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 15:57:50 2021

@author: jinho
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:34:12 2021

@author: jinho
"""
import pandas as pd
from konlpy.tag import Okt

def tokenize_Okt(path, stop_words):
    esg = pd.read_csv(path)
    esg = esg.drop(['Unnamed: 0'], axis = 1)
    esg = esg.apply(lambda x: x.str.strip().replace('\n',''), axis = 1)
    for i in range(len(esg)):
        document = esg['text'][i]
        okt = Okt()
        clean_words = []
        for word in okt.pos(document): 
            if word[1] not in ['Josa', 'Eomi','Punctuation']:
                clean_words.append(word[0])
        document = ' '.join(clean_words)
        esg['text'][i] = document 
    esg['text'] = esg['text'].apply(lambda stop_remove: [word for word in stop_remove.split() if word not in stop_words])
    
    return esg

def stop_word(path, stop_words):
    esg = pd.read_csv(path)
    esg = esg.drop(['Unnamed: 0'], axis = 1)
    esg = esg.apply(lambda x: x.str.strip().replace('\n',''), axis = 1)
    esg['text'] = esg['text'].apply(lambda stop_remove: [word for word in stop_remove.split() if word not in stop_words])
    

stop_words = "또한 이때 대한 따라서 및 이에 대한 또는 등 이를 기업은 기업의 아울러 \n" \
                + "주요 하며 더욱 등에 등의 그 따른 적극 더불어 도출된 이 때 등을 등에서 아울러 대한 다음과 모두 \n" \
                    + "더 나아가 기업이 이를 이러한 적극적으로 주도적으로 능동적으로 자발적으로 \n" \
                        + "넷째 만약 그러므로 한편 그리고 스스로 즉 다만 이러한 주요 같은 같이 그러나 이와 함께 특히 들 무엇 첫째 둘째 셋째 \n"

path_E = r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_E_.csv'
path_S = r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_S_.csv'
path_G = r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_G_.csv'

E_okt = tokenize_Okt(path_E, stop_words)
S_okt = tokenize_Okt(path_S, stop_words)
G_okt = tokenize_Okt(path_G, stop_words)

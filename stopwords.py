# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:34:12 2021

@author: jinho
"""
import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from konlpy.tag import Okt, Mecab

def tokenize_Okt(esg, stop_words):
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

def tokenize_Mecab(esg, stop_words, dict_path):
    esg = esg.drop(['Unnamed: 0'], axis = 1)
    esg = esg.apply(lambda x: x.str.strip().replace('\n',''), axis = 1)
    for i in range(len(esg)):
        document = esg['text'][i]
        mecab = Mecab(dict_path)
        clean_words = []
        for word in mecab.pos(document): 
            if word[1] not in ['JC','JKQ','JKV','JKB','JKC','IC','JX', 'JKS', 'JKO', 'JKG', 'EP','EF', 'ETN', 'XSN','VCP+ETM']:
                clean_words.append(word[0])
        document = ' '.join(clean_words)
        esg['text'][i] = document 
    esg['text'] = esg['text'].apply(lambda stop_remove: [word for word in stop_remove.split() if word not in stop_words])
    
    return esg

def stop_word(esg, stop_words):
    esg = esg.drop(['Unnamed: 0'], axis = 1)
    esg = esg.apply(lambda x: x.str.strip().replace('\n',''), axis = 1)
    esg['text'] = esg['text'].apply(lambda stop_remove: [word for word in stop_remove.split() if word not in stop_words])
    

stop_words = "또한 이때 대한 따라서 및 이에 대한 또는 등 이를 기업은 기업의 아울러 \n" \
                + "주요 하며 더욱 등에 등의 그 따른 적극 더불어 도출된 이 때 등을 등에서 아울러 대한 다음과 모두 \n" \
                    + "더 나아가 기업이 이를 이러한 적극적으로 주도적으로 능동적으로 자발적으로 \n" \
                        + "이러한 주요 같은 같이 그러나 이와 함께 특히 들 무엇 첫째 둘째 셋째 \n"

E = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_E_.csv')
S = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_S_.csv')
G = pd.read_csv(r'C:\Users\jinho\OneDrive\문서\카카오톡 받은 파일\standard_G_.csv')

dicpath="C:\\mecab\\mecab-ko-dic"


E_mecab = tokenize_Mecab(E, stop_words, dicpath)
S_mecab = tokenize_Mecab(S, stop_words, dicpath)
G_mecab = tokenize_Mecab(G, stop_words, dicpath)
E_okt = tokenize_Okt(E, stop_words)
S_okt = tokenize_Okt(S, stop_words)
G_okt = tokenize_Okt(G, stop_words)
mecab = Mecab(dicpath="C:\\mecab\\mecab-ko-dic")
print(mecab.pos('안전하고'))
okt = Okt()
print(okt.pos('경영진'))

okt.add_dictionary('아이오아이', 'Noun')

with open("user-dict.txt", encoding='UTF8') as f:
    data = f.read()

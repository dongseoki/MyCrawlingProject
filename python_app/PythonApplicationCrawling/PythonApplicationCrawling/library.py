from urllib.request import urlopen
from urllib import parse
from selenium import webdriver
from bs4 import BeautifulSoup

from flask import Flask
from flask import request
from flask import jsonify

import time
import os
import json
import re
import sys, traceback
import threading

KW_CODE =0
KM_CODE =1
DJ_CODE=2
DS_CODE=3
DD_CODE=4
MJ_CODE=5
SY_CODE=6
SM_CODE=7
SK_CODE=8
SW_CODE=9
SS_CODE=10
HS_CODE=11


# In[4]:


base_start_url_list = ['http://kupis.kw.ac.kr/',
'http://lib.kookmin.ac.kr/',
'http://library.daejin.ac.kr/',
'http://discover.duksung.ac.kr/',
'http://library.dongduk.ac.kr/',
'http://lib.mju.ac.kr/',
'http://lib.syu.ac.kr/',
'https://lib.smu.ac.kr/',
'http://library.skuniv.ac.kr/',
'http://lib.swu.ac.kr/',
'http://lib.sungshin.ac.kr/',
'http://hsel.hansung.ac.kr/']

base_middle_url_list = ['search/caz/result?st=KWRD&commandType=advanced&si=1&q=',
'#/total-search?keyword=',
'',
'',
'',
'',
'',
'Search/?q=',
'',
'',
'',
'']





base_end_url_list = ['&b0=and&weight0=&si=2&q=&b1=and&weight1=&si=3&q=&weight2=&inc=TOTAL&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&lmt0=TOTAL&lmtsn=000000000003&lmtst=OR&rf=&rt=&range=000000000021&cpp=10&msc=100',
'',
'',
'',
'',
'',
'',
'',
'',
'',
'',
''
]



class LibraryLS:
    def __init__(self, sid):
        self.sid = sid
        self.loanStatusList = []
        self.errorMessage= ''
    


# In[8]:


class LoanStatus:
    def __init__(self, title = '', RN = '', CN = '', POS = '', STATE = -1, RDD = '', BN = 0, errorMessage = ''):
        self.title = title
        self.RN= RN
        self.CN= CN
        self.POS= POS
        self.STATE= STATE
        self.RDD = RDD#'2222-12-31'
        self.BN = BN
        self.errorMessage = errorMessage
'''#STATE : 도서 상태,
#-1  에러
#1 대출가능
#0 대출중
#2 지정도서
# 대출불가 아직 생각 안함.
#RN : 등록번호
#CN : 청구기호
#POS : 위치
이런것들'''



stateDict = {'대출중': 0, '이용가능':1,'대출가능':1, '지정도서':2}



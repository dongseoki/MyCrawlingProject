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

univNameList = ['광운대학교', '국민대학교', '대진대학교', '덕성여자대학교', '동덕여자대학교', '명지대학교', '삼육대학교', '상명대학교', '서경대학교', '서울여자대학교', '성신여자대학교', '한성대학교']

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

#http://lib.syu.ac.kr/

base_middle_url_list = ['search/caz/result?st=KWRD&commandType=advanced&si=1&q=',
'#/search/ex?isbn=1%7Cl%7Ca%7C',
'data_data_list.mir?search_keyword_type1=isbn&search_keyword1=',
'#/search/ex?isbn=1%7Ck%7Ca%7C',
'#/search/ex?isbn=1%7Cl%7Ca%7C',
'search/Search.Result.ax',
'search/caz/result?st=KWRD&commandType=advanced&mId=&si=1&q=',
'Search/?q=',
'search/Search.Result.ax',
'search/caz/result?st=KWRD&commandType=advanced&si=1&q=',
'search/tot/result?st=KWRD&commandType=advanced&mId=&si=1&q=',
'data_data_list.mir?search_keyword_type1=isbn&search_keyword1=']





base_end_url_list = ['&b0=and&weight0=&si=2&q=&b1=and&weight1=&si=3&q=&weight2=&inc=TOTAL&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&lmt0=TOTAL&lmtsn=000000000003&lmtst=OR&rf=&rt=&range=000000000021&cpp=10&msc=100',
'&branch=1&material-type=1',
'&srch_condi_01=AND&search_keyword_type2=author&search_keyword2=&srch_condi_02=AND&search_keyword_type3=subject&search_keyword3=&srch_condi_03=%E2%96%B2&select_current_sort_type=&select_current_sort_order=&select_current_per_page_num=10&basic_list=list&current_per_page_num=10&current_sort_type=&current_sort_order=&MAXI=1000&mloc_code=DJUL&facet_limit_search_field_code=&scope_code=&mtype_code=M&type_code=',
'&material-type=1',
'&branch=1&material-type=1',
'?sid=1&q=ISBN%3A{}%3A1&eq=&mf=true&qt=ISBN%3D{}&qf={}&f=&br=&cl=&gr=1+3+4+5+6+7+8+9+10+11+12+13+14+2+15+16+26+27+17+18+19+20+21+22+23+24+25+28+29+30+33+34&rl=&page=&pageSize=0&s=&st=&h=&cr=&py=&subj=&facet=Y&nd=&vid=0&fv=%24esc.html%28%24%21%7BFilters%7D%29&tabID=',
'&b0=and&weight0=&si=2&q=&b1=and&weight1=&si=3&q=&weight2=&inc=TOTAL&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&lmt0=TOTAL&lmtsn=000000000003&lmtst=OR&lmt1=A0000000&lmtsn=000000000006&lmtst=OR&rf=&rt=&range=000000000021&cpp=10&msc=10000',
'',
'?sid=1&q=ISBN%3A{}&mf=true&qt=%EC%A0%84%EC%B2%B4%3D{}&qf={}&f=&br=&cl=&gr=&rl=&page=1&pageSize=0&s=&st=&h=&cr=&py=&subj=&facet=Y&nd=&vid=0&tabID=',
'&b0=and&weight0=&si=2&q=&b1=and&weight1=&si=3&q=&weight2=&lmt0=TOTAL&_lmt0=on&lmtsn=000000000001&lmtst=OR&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&inc=TOTAL&_inc=on&_inc=on&_inc=on&_inc=on&_inc=on&lmt1=TOTAL&lmtsn=000000000003&lmtst=OR&lmt2=LIB00000&lmtsn=000000000006&lmtst=OR&lmt3=TOTAL&lmtsn=000000000015&lmtst=FRNT&rf=&rt=&range=000000000021&cpp=10&msc=500',
'&b0=and&weight0=&si=2&q=&b1=and&weight1=&si=3&q=&weight2=&_lmt0=on&lmtsn=000000000001&lmtst=OR&lmt0=m&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&_lmt0=on&inc=TOTAL&_inc=on&_inc=on&_inc=on&lmt1=TOTAL&lmtsn=000000000003&lmtst=OR&lmt2=00000001&lmtsn=000000000006&lmtst=OR&rf=&rt=&range=000000000021&cpp=10&msc=10000',
'&srch_condi_01=AND&search_keyword_type2=author&search_keyword2=&srch_condi_02=AND&search_keyword_type3=subject&search_keyword3=&srch_condi_03=%E2%96%B2&select_current_sort_type=&select_current_sort_order=&select_current_per_page_num=10&basic_list=list&current_per_page_num=10&current_sort_type=&current_sort_order=&MAXI=1000&mloc_code=HSEL&facet_limit_search_field_code=&scope_code=&mtype_code=M&type_code='
]

searchLinkXpathList = ['',
'/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/div[4]/div/div[3]/ul/li[1]/a[1]',
'//*[@id="content_data"]/form/div[2]/table/tbody/tr[1]/td[3]/a',
'//*[@id="goto-content"]/div[2]/div[2]/div/div[2]/div[4]/div/div[3]/ul/li[1]/a[1]/span',
'/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/div[4]/div/div[3]/ul/li[1]/a[1]/span',
'//*[@id="frmResultList"]/ul/li/dl/dd/div/div/div[3]/a[1]',
'/html/body/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/form/fieldset/ul/li[1]/dl/dd[4]/a',
'',
'//*[@id="frmResultList"]/ul/li/dl/dd/div/div/div[3]/a[1]',
'//*[@id="dataInfo0"]/div[1]/dl/dd[1]/a',
'/html/body/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/form/fieldset/ul/li/dl/dd[4]/a',
'//*[@id="content_data"]/form/div[2]/table/tbody/tr[1]/td[3]/a'
]
searchBrowserCheckXpath = ['',
'/html/body/div[1]/div[3]/div[2]/div[1]/div/h2',
'//*[@id="content_data"]/form/h4',
'//*[@id="goto-content"]/h2/strong',
'/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div[1]/h2',
'//*[@id="container_inner"]/div[1]/h2/img',
'//*[@id="divTitle"]',
'',
'//*[@id="pageTitle"]/div/h2',
'//*[@id="divTitle"]/h2',
'//*[@id="divTitle"]',
'//*[@id="content_header"]/div/h4'
]

searchDetailBrowserCheckXpath = ['',
'',
'',
'//*[@id="goto-content"]/div[2]/div/div[1]/div/div[2]/div[3]',
'',
'//*[@id="container_inner"]/div[1]/h2/img',
'//*[@id="divProfile"]/table/tbody',
'',
'//*[@id="searchDetailInner"]/div[7]/h3',
'//*[@id="divTitle"]/h2',
'//*[@id="divTitle"]',
'//*[@id="content_header"]/div/h4'
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



stateDict = {'대출중': 0, '예약도서대출중':0, '폐가도서대출중':0,'행낭대출중':0, '이용가능':1,'대출가능':1, '지정도서':2}


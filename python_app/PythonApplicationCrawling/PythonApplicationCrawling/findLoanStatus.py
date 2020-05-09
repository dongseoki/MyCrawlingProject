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

from library import *
from crawling import *

def makeSearchUrl(ISBN, title, sid, flag):
    if flag ==1:
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + ISBN+ base_end_url_list[sid]
    else :
        # flag 2.
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + title+ base_end_url_list[sid]
    return searchUrl

def makeJsonDict(result):
    # result 의 타입은 LibraryLS
    jsonDict = {}
    jsonDict['sid'] = result.sid
    jsonDict['loanStatusList'] = []
    for item in result.loanStatusList:
        jsonDict['loanStatusList'].append(vars(item))
    jsonDict['errorMessage']=result.errorMessage
    return jsonDict

def findLoanStatus(ISBN, title, sid, resultList):

    if sid != SM_CODE and sid != KW_CODE and sid !=KM_CODE:
        result = LibraryLS(sid)
        result.errorMessage = 'Not developed...'
    else : 
        if sid == KW_CODE :
            searchUrl = makeSearchUrl(ISBN, title, sid, 2)
        else :
            searchUrl = makeSearchUrl(ISBN, title, sid, 1)
        result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.
    jsonDict = makeJsonDict(result)
    resultList[sid] = jsonDict
    return
    #return json.dumps(jsonDict)

def findLoanStatusOneResult(ISBN, title, sid, searchFlag):
    if sid != SM_CODE and sid != KW_CODE:
        result = LibraryLS(sid)
        result.errorMessage = 'Not developed...'
    else : 
        if sid == KW_CODE :
            searchUrl = makeSearchUrl(ISBN, title, sid, 2)
        else :
            searchUrl = makeSearchUrl(ISBN, title, sid, 1)
        result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.
    jsonDict = makeJsonDict(result)
    return jsonDict

#isbn = request.args.get('isbn')
#koreaTitle = request.args.get('title')
#title = parse.quote(koreaTitle)
#searchFlag = request.args.get('searchFlag')

#isbn = '9788968481093'
#koreaTitle = '(비즈니스를 위한) 데이터 과학'
#title = parse.quote(koreaTitle)
#searchFlag = '2'

#isbn = '9791190313131'
#koreaTitle = '지적 대화를 위한 넓고 얕은 지식'
#title = parse.quote(koreaTitle)
#searchFlag = '1'


#isbn = '9788988474839'
#koreaTitle = '데이터 분석 전문가 가이드'
#sid = 7
#searchFlag= '2'
#title = parse.quote(koreaTitle)

#urlresult = makeSearchUrl(ISBN, title, KM_CODE, searchFlag)


isbn = '9788996094050'
koreaTitle = '윤성우의 열혈 C 프로그래밍'
title = parse.quote(koreaTitle)
# case4.  3개 도서관 검색 테스트
#https://kupis.kw.ac.kr/search/detail/CATTOT000000317224?mainLink=/search/tot&briefLink=/search/tot/result?commandType=advanced_A_lmtsn=000000000001_A_lmtsn=000000000003_A_cpp=10_A_range=000000000021_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A_lmt0=TOTAL_A_lmt1=TOTAL_A_rf=_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A_si=1_A_si=2_A_si=3_A_weight2=_A_weight0=_A_weight1=_A_inc=TOTAL_A_q=%EC%9C%A4%EC%84%B1%EC%9A%B0%EC%9D%98+%EC%97%B4%ED%98%88+C+%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D_A_q=_A_q=_A_b0=and_A_b1=and_A_lmtst=OR_A_lmtst=OR_A_rt=_A_st=KWRD_A_msc=500
#https://lib.kookmin.ac.kr/#/search/ex?isbn=1%7Cl%7Ca%7C9788996094050&branch=1&material-type=1
#http://lib.smu.ac.kr/Search/?q=9788996094050&searchTruncate=true&campuscode=00



#resultList = [i for i in range(12)]
##findLoanStatus(isbn, title, KW_CODE, int(searchFlag), resultList)
##findLoanStatus(isbn, title, SM_CODE, int(searchFlag), resultList)
#findLoanStatus(isbn, title, SM_CODE, resultList)

## search Flag 문제. 없앰.

#for item in resultList:
#    print(item)

#방법 1






resultList = [i for i in range(12)]
threads = []
for i in range(12):
    t = threading.Thread(target=findLoanStatus, args=(isbn, title, i, resultList))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
jsonString =  json.dumps(resultList)
print(jsonString)

# 방법 2
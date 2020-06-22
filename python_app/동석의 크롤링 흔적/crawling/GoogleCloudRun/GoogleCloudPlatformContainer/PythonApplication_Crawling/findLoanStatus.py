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
        if sid == MJ_CODE or sid == SK_CODE :
            searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + base_end_url_list[sid].format(ISBN, ISBN, ISBN)
        else :
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

def findLoanStatus(ISBN, title, sid, resultList = None):

 
    if sid == KW_CODE or sid == SY_CODE or sid ==SW_CODE or sid == SS_CODE:
        searchUrl = makeSearchUrl(ISBN, title, sid, 2)
    else :
        searchUrl = makeSearchUrl(ISBN, title, sid, 1)
    result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.

    jsonDict = makeJsonDict(result)
    if resultList is not None:
        resultList[sid] = jsonDict
    else :
        return  jsonDict
    return
    #return json.dumps(jsonDict)


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


#ISBN = '9788996094050'
#koreaTitle = '윤성우의 열혈 C 프로그래밍'
#title = parse.quote(koreaTitle)
##https://discover.duksung.ac.kr/#/search/detail/1700746


#isbn = '9788925533315'
#koreaTitle = '스노볼 : 워런 버핏과 인생 경영'
#title = parse.quote(koreaTitle)


#isbn = '9788934985068'
#koreaTitle = '팩트풀니스'
#title = parse.quote(koreaTitle)


#isbn = '9791164050574'
#koreaTitle = '벤 바레스 :어느 트랜스젠더 과학자의 자서전'
#title = parse.quote(koreaTitle)
#https://discover.duksung.ac.kr/#/search/detail/4949663

#ISBN = '9788925530007'
#koreaTitle = '없는 책'
#title = parse.quote(koreaTitle)

#isbn = '9791165075064'
#koreaTitle = '녹나무의 파수꾼'
#title = parse.quote(koreaTitle)

#isbn = '9788931004441'
#koreaTitle = '잃어버린 지평선'
#title = parse.quote(koreaTitle)
# case4.  3개 도서관 검색 테스트
#https://kupis.kw.ac.kr/search/detail/CATTOT000000317224?mainLink=/search/tot&briefLink=/search/tot/result?commandType=advanced_A_lmtsn=000000000001_A_lmtsn=000000000003_A_cpp=10_A_range=000000000021_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A__inc=on_A_lmt0=TOTAL_A_lmt1=TOTAL_A_rf=_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A__lmt0=on_A_si=1_A_si=2_A_si=3_A_weight2=_A_weight0=_A_weight1=_A_inc=TOTAL_A_q=%EC%9C%A4%EC%84%B1%EC%9A%B0%EC%9D%98+%EC%97%B4%ED%98%88+C+%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D_A_q=_A_q=_A_b0=and_A_b1=and_A_lmtst=OR_A_lmtst=OR_A_rt=_A_st=KWRD_A_msc=500
#https://lib.kookmin.ac.kr/#/search/ex?isbn=1%7Cl%7Ca%7C9788996094050&branch=1&material-type=1
#http://lib.smu.ac.kr/Search/?q=9788996094050&searchTruncate=true&campuscode=00

#isbn = '9791186757093'
#koreaTitle = '자존감수업'
#title = parse.quote(koreaTitle)

#ISBN = '9788996852308'
#koreaTitle = '성서적 꿈 성취론'
#title = parse.quote(koreaTitle)
#print(findLoanStatus(ISBN, title, SY_CODE))


#ISBN = '9788972756194'
#koreaTitle = '나미야 잡화점'
#title = parse.quote(koreaTitle)
#print(findLoanStatus(ISBN, title, SK_CODE))


#ISBN = '9788972759999'
##koreaTitle = '없는 책'
#koreaTitle = 'ㅂㅈㄷㄱㅁㄴㅇㄹㅋㅌㅊㅍㅁㄴㅇㄹㅈㄷㄱㄷㅈㅂㅈㄷㄹ'
#title = parse.quote(koreaTitle)
#print(findLoanStatus(ISBN, title, SK_CODE))


#ISBN = '9788993163643'
#koreaTitle = '엔트리 피지컬 컴퓨팅'
#title = parse.quote(koreaTitle)


#ISBN = '9788956268279'
#koreaTitle = '현대소설과 분단의 트라우마 = Modern novels and the trauma of division'
#title = parse.quote(koreaTitle)

#ISBN = '9788959896127'
#koreaTitle = '트렌드 코리아 2020 :서울대 소비트렌드분석센터의 2020 전망'
#title = parse.quote(koreaTitle)
#print(title)

#print(findLoanStatus(ISBN, title, HS_CODE))
#print('\n\n\n----------------------------')
#ISBN = '9791190313186'
#koreaTitle = '지적 대화를 위한 넓고 얕은 지식 . v.1-2'
#title = parse.quote(koreaTitle)
#print(title)
#print(findLoanStatus(ISBN, title, HS_CODE))



#print('\n\n\n----------------------------')
#ISBN = '9788993169999'
#koreaTitle = '이건 절대로 없는 책이다 없을거야'
#title = parse.quote(koreaTitle)
#print(title)
#print(findLoanStatus(ISBN, title, HS_CODE))

#print(findLoanStatus(ISBN, title, SW_CODE))
#print()
#print(makeSearchUrl(ISBN, title, SW_CODE, 2))

#resultList = [i for i in range(12)]
#print(findLoanStatus(isbn, title, DS_CODE))

#####findLoanStatus(isbn, title, SM_CODE, int(searchFlag), resultList)
####findLoanStatus(isbn, title, SM_CODE, resultList)

##### search Flag 문제. 없앰.

#for item in resultList:
#    print(item)

#방법 1

#from datetime import datetime
#start = datetime.now()


#resultList = [i for i in range(12)]
#threads = []
#for i in range(12):
#    t = threading.Thread(target=findLoanStatus, args=(ISBN, title, i, resultList))
#    threads.append(t)

#for t in threads:
#    t.start()
#for t in threads:
#    t.join()
##jsonString =  json.dumps(resultList)
##print(jsonString)

#resultsizeStr = ''
#for item in resultList:
#    resultsizeStr += ' '+ str(len(item['loanStatusList']))

#print(resultsizeStr)
#print('')
#for item in resultList:
#    print(item)
#    print('')


#finish = datetime.now() - start
#print('실행 시간 : ',finish)
## # 방법 2
#!/usr/bin/env python
# coding: utf-8

# In[25]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys, traceback
import json
from urllib import parse

# In[2]:


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


# In[3]:


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


# In[4]:


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


# In[5]:


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


# In[6]:


class LibraryLS:
    def __init__(self, sid):
        self.sid = sid
        self.loanStatusList = []
        self.errorMessage= ''
    


# In[40]:


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


# In[43]:


#아직 상명대만 함. 상명대 ISBN으로 검색예정.
def makeSearchUrl(ISBN, title, sid, flag):
    if flag ==1:
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + ISBN+ base_end_url_list[sid]
    else :
        # flag 2.
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + title+ base_end_url_list[sid]
    return searchUrl
    


# In[44]:


def findSubStringByRegEx(text, sid, subStringType):
    regex = re.compile(regexDictList[sid][subStringType])
    matchObj = regex.search(text)
    subString = matchObj.group(1)
    return subString
    
    


# In[45]:


def find_ISBN(text):
    regex = re.compile('\d\d\d\d\d\d\d\d\d\d\d\d\d')
    matchObj = regex.search(text)
    return matchObj.group(0)


# In[46]:


def find_BN(text):
    if '예약' in text:
        regex = re.compile('대출중\s*\(\s+(\d+)명')
        matchObj = regex.search(text)
        num = int(matchObj.group(1))
        return num
    else :
        return 0


# In[47]:


def find_RDD(text):
    regex = re.compile('\d\d\d\d\-\d\d\-\d\d')
    matchObj = regex.search(text)
    return matchObj.group(0)


# In[48]:


def find_STATE_BN(text):
    if '대출중' in text:
        return 0, find_BN(text)
    elif '이용가능' in text:
        return 1,0
    elif '지정도서' in text:
        return 2,0
    else :
        return -1,0


# In[58]:


def visitLink(ISBN, sid, title, bookLink):
    loanStatusList = []
    #= LoanStatus()
    try:
        #1. 접속.
        html = urlopen(base_start_url_list[sid]+bookLink)
        bsObject = BeautifulSoup(html, "html.parser")
        
        #1-1 ISBN 정보가 일치하지 않다면 바로 return!!!
        includedISBNString = str(bsObject.find('div', {'class':'col-md-10 detail-table-right'}).find_all('dl')[2].find('dd'))

        if ISBN != find_ISBN(includedISBNString):
            return loanStatusList
        #2. 대출 데이터를 차곡차곡저장.
        idx = 0
        for loanResult in bsObject.find('div', class_='sponge-guide-Box-table sponge-detail-table').find('tbody').find_all('tr'):
            errorMessage = ''
            content = loanResult.find_all('td')
            RN = content[0].text.strip()
            CN = content[1].text.strip()
            POS = content[2].text.strip()
            STATE_STRING = content[3].text.strip()
            try:
                RDD = find_RDD(str(content[4]))
            except AttributeError as e:
                RDD = ''
            STATE, BN = find_STATE_BN(STATE_STRING)
            loanStatusList.append(LoanStatus(title, RN, CN,POS,STATE, RDD ,BN, ''))
    except :
        pass
        #traceback.format_exc()
    finally:
        return loanStatusList


# In[59]:


test_string = ""
#def crawling(ISBN, title, sid, searchUrl):
#    libraryLoanStatus = LibraryLS(sid)
#    try:
#        #1. 접속.
#        html = urlopen(searchUrl)
#        bsObject = BeautifulSoup(html, "html.parser")
#        #2. 링크를 차곡차곡저장.
#        # 정규식과 beautifulsoap4을 이용하여 저장...!!
#        bookLinklist =[]
#        for bookResult in bsObject.find_all('div', class_='search-list-result'):
#            content = bookResult.find('div', {'class','sponge-list-content'}).find('a')
#            title = content.text.strip()
#            link =  content.get('href')
#            bookLinklist.append([title, link])

#        #3. 해당 링크를 방문하여 리스트에 추가해라..!!
#        for item in bookLinklist:
#            libraryLoanStatus.loanStatusList += visitLink(ISBN, sid, item[0], item[1])
#    except :
#        libraryLoanStatus.errorMessage = traceback.format_exc()
#        #libraryLoanStatus.errorMessage = 에러 traceback 에러메세지를 담는다.
#    finally:
#        return libraryLoanStatus
    
def crawling(ISBN, title, sid, searchUrl):
    libraryLoanStatus = LibraryLS(sid)
    try:
        #1. 접속.
        html = urlopen(searchUrl)
        bsObject = BeautifulSoup(html, "html.parser")
        #2. 링크를 차곡차곡저장.
        # 정규식과 beautifulsoap4을 이용하여 저장...!!
        bookLinklist =[]
        for bookResult in makeBookResultList(bsObject, sid):
            content = makeContent(bookResult, sid)
            title = content.text.strip()
            link =  content.get('href')
            bookLinklist.append([title, link])
            
        print(len(bookLinklist))
        #3. 해당 링크를 방문하여 리스트에 추가해라..!!
        #for item in bookLinklist:
        #    libraryLoanStatus.loanStatusList += visitLink(ISBN, sid, item[0], item[1])
    except:
        libraryLoanStatus.errorMessage = traceback.format_exc()
        #libraryLoanStatus.errorMessage = 에러 traceback 에러메세지를 담는다.
    finally:
        return libraryLoanStatus
    

# In[41]:


def makeJsonDict(result):
    # result 의 타입은 LibraryLS
    jsonDict = {}
    jsonDict['sid'] = result.sid
    jsonDict['loanStatusList'] = []
    for item in result.loanStatusList:
        jsonDict['loanStatusList'].append(vars(item))
    jsonDict['errorMessage']=result.errorMessage
    return jsonDict


# In[42]:


#flag =1 iSBN, 0, title search by..
#함수 만들기.

#sid = int(sid)
def findLoanStatus(ISBN, title, sid):
    searchUrl = makeSearchUrl(ISBN, title, sid, 1)
    result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.
    jsonDict = makeJsonDict(result)
    return json.dumps(jsonDict)
    

#def makeBookResultList(bsObject, sid):
#    return {
#        KW_CODE: bsObject.find('div', {'id' : 'divSearchResult'}).find_all('dl', {'class': 'briefDetail'}),
#        SM_CODE: bsObject.find_all('div', class_='search-list-result')
#    }.get(sid, -1)
def makeBookResultList(bsObject, sid):
    if sid == KW_CODE:
        BookResultList = bsObject.find('div', {'id' : 'divSearchResult'}).find_all('dl', {'class': 'briefDetail'})
    elif sid == KM_CODE:
        pass
    elif sid == DJ_CODE:
        pass
    elif sid == DS_CODE:
        pass
    elif sid == DD_CODE:
        pass
    elif sid == MJ_CODE:
        pass
    elif sid == SY_CODE:
        pass
    elif sid == SM_CODE:
        BookResultList =  bsObject.find_all('div', class_='search-list-result')
    elif sid == SK_CODE:
        pass
    elif sid == SW_CODE:
        pass
    elif sid == SS_CODE:
        pass
    elif sid == HS_CODE:
        pass
    return BookResultList

#searchUrl = 'http://kupis.kw.ac.kr/search/tot/result?st=KWRD&si=TOTAL&q=%EB%8D%B0%EC%9D%B4%ED%84%B0+%EB%B6%84%EC%84%9D+%EC%A0%84%EB%AC%B8%EA%B0%80+%EA%B0%80%EC%9D%B4%EB%93%9C+%3D+The+guide+for+advanced+data+analytics+professional+%2F#'
ISBN = '9788988474839'
koreaTitle = '데이터 분석 전문가 가이드 = The guide for advanced data analytics professional'
sid = KW_CODE
title = parse.quote(koreaTitle)
searchUrl = makeSearchUrl(ISBN,title, sid,2)
#html = urlopen(searchUrl)
#bsObject = BeautifulSoup(html)
html = urlopen(searchUrl)
bsObject = BeautifulSoup(html, "html.parser")

res4 = makeBookResultList(bsObject, sid)

#def makeContent(bookResult, sid):
#    print(type(bookResult))
#    return{
#        0: bookResult.find('dd', {'class': 'searchTitle'}).find('a'),
#        7: bookResult.find('div', {'class','sponge-list-content'}).find('a')
#    }[sid]

# 학교에 따른 다른 함수 구현.
    #if sid == KW_CODE:
    #    content = bookResult.find('dd', {'class': 'searchTitle'}).find('a')
    #elif sid == KM_CODE:
    #    pass
    #elif sid == DJ_CODE:
    #    pass
    #elif sid == DS_CODE:
    #    pass
    #elif sid == DD_CODE:
    #    pass
    #elif sid == MJ_CODE:
    #    pass
    #elif sid == SY_CODE:
    #    pass
    #elif sid == SM_CODE:
    #    content =   bookResult.find('div', {'class','sponge-list-content'}).find('a')
    #elif sid == SK_CODE:
    #    pass
    #elif sid == SW_CODE:
    #    pass
    #elif sid == SS_CODE:
    #    pass
    #elif sid == HS_CODE:
    #    pass

def makeContent(bookResult, sid):
    print(type(bookResult))
    if sid == KW_CODE:
        content = bookResult.find('dd', {'class': 'searchTitle'}).find('a')
    elif sid == KM_CODE:
        pass
    elif sid == DJ_CODE:
        pass
    elif sid == DS_CODE:
        pass
    elif sid == DD_CODE:
        pass
    elif sid == MJ_CODE:
        pass
    elif sid == SY_CODE:
        pass
    elif sid == SM_CODE:
        content =   bookResult.find('div', {'class','sponge-list-content'}).find('a')
    elif sid == SK_CODE:
        pass
    elif sid == SW_CODE:
        pass
    elif sid == SS_CODE:
        pass
    elif sid == HS_CODE:
        pass
    return content



res5= makeContent(res4[0], KW_CODE)
print(res5)
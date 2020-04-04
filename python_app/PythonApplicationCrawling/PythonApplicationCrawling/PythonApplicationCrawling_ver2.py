
#!/usr/bin/env python
# coding: utf-8

# In[153]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys, traceback
import json
from urllib import parse


# In[3]:

# entity 들.

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



def findSubStringByRegEx(text, sid, subStringType):
    regex = re.compile(regexDictList[sid][subStringType])
    matchObj = regex.search(text)
    subString = matchObj.group(1)
    return subString
    
    
# 6단계 함수들

# In[10]:
def find_BN(text):
    if '예약' in text:
        regex = re.compile('대출중\s*\(\s+(\d+)명')
        matchObj = regex.search(text)
        num = int(matchObj.group(1))
        return num
    else :
        return 0

# 5단계 함수들

def find_ISBN(text):
    regex = re.compile('\d\d\d\d\d\d\d\d\d\d\d\d\d')
    matchObj = regex.search(text)
    return matchObj.group(0)


def findState(text):
    try:
        STATE = stateDict[text]
    except KeyError:
        STATE = -1
    return STATE

# In[12]:
def find_STATE_BN(text):
    if '대출중' in text:
        return 0, find_BN(text)
    elif '이용가능' in text:
        return 1,0
    elif '지정도서' in text:
        return 2,0
    else :
        return -1,0

def find_RDD(text):
    regex = re.compile('\d\d\d\d\-\d\d\-\d\d')
    matchObj = regex.search(text)
    return matchObj.group(0)


# 4단계 함수들

def isISBNCorrect(ISBN, bsObject, sid):
    try:
        if sid == KW_CODE:
            searchedISBN = find_ISBN(str(bsObject.find('div', {'id': 'divProfile'})))
            if ISBN == searchedISBN:
                return True
            else :
                return False
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
            includedISBNString = str(bsObject.find('div', {'class':'col-md-10 detail-table-right'}).find_all('dl')[2].find('dd'))
            if ISBN == find_ISBN(includedISBNString):
                return True
            else :
                return False
        elif sid == SK_CODE:
            pass
        elif sid == SW_CODE:
            pass
        elif sid == SS_CODE:
            pass
        elif sid == HS_CODE:
            pass
    except AttributeError:
        # 전자 자료 같은 경우. ISBN이 없다.
        return False





def makeLoanResultList(bsObject, sid):
    if sid == KW_CODE:
        LoanResultList = bsObject.find('div', {'id': 'divHoldingInfo'}).find('table').find('tbody').find_all('tr')
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
        LoanResultList = bsObject.find('div', class_='sponge-guide-Box-table sponge-detail-table').find('tbody').find_all('tr')
    elif sid == SK_CODE:
        pass
    elif sid == SW_CODE:
        pass
    elif sid == SS_CODE:
        pass
    elif sid == HS_CODE:
        pass
    return LoanResultList



def getLoanStatus(title, loanResult, loanStatusList, sid):
    if sid == KW_CODE:
        errorMessage = ''
        content = loanResult.find_all('td')
        RN = content[1].text.strip()
        CN = content[2].text.strip()
        POS = content[3].text.strip()
        STATE_STRING = content[4].text.strip()
        RDD = content[5].text.strip()
        STATE = findState(STATE_STRING)
        BN = 0
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
    elif sid == SK_CODE:
        pass
    elif sid == SW_CODE:
        pass
    elif sid == SS_CODE:
        pass
    elif sid == HS_CODE:
        pass
    
    loanStatusList.append(LoanStatus(title, RN, CN,POS,STATE, RDD ,BN, ''))
    return

# 3단계 함수들

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


def makeContent(bookResult, sid):
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


def visitLink(ISBN, sid, title, bookLink):
    loanStatusList = []
    #= LoanStatus()
    try:
        #1. 접속.
        html = urlopen(base_start_url_list[sid]+bookLink)
        bsObject = BeautifulSoup(html, "html.parser")
        
        #1-1 ISBN 정보가 일치하지 않다면 바로 return!!!
        if isISBNCorrect(ISBN, bsObject, sid) == False:
            return loanStatusList

        #2. 대출 데이터를 차곡차곡저장.
        idx = 0
        for loanResult in makeLoanResultList(bsObject, sid):
            getLoanStatus(title, loanResult, loanStatusList, sid)
    except :
        traceback.print_exc()
        #traceback.format_exc()
    finally:
        return loanStatusList


# 2단계 함수들
#아직 상명대, 광운대만 함. 
def makeSearchUrl(ISBN, title, sid, flag):
    if flag ==1:
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + ISBN+ base_end_url_list[sid]
    else :
        # flag 2.
        searchUrl = base_start_url_list[sid]+base_middle_url_list[sid] + title+ base_end_url_list[sid]
    return searchUrl

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

        #3. 해당 링크를 방문하여 리스트에 추가해라..!!
        for item in bookLinklist:
            libraryLoanStatus.loanStatusList += visitLink(ISBN, sid, item[0], item[1])
    except:
        libraryLoanStatus.errorMessage = traceback.format_exc()
        #libraryLoanStatus.errorMessage = 에러 traceback 에러메세지를 담는다.
    finally:
        return libraryLoanStatus



def makeJsonDict(result):
    # result 의 타입은 LibraryLS
    jsonDict = {}
    jsonDict['sid'] = result.sid
    jsonDict['loanStatusList'] = []
    for item in result.loanStatusList:
        jsonDict['loanStatusList'].append(vars(item))
    jsonDict['errorMessage']=result.errorMessage
    return jsonDict


# 1단계 함수

def findLoanStatus(ISBN, title, sid, searchFlag):
    if sid != SM_CODE and sid != KW_CODE:
        result = LibraryLS(sid)
        result.errorMessage = 'Not developed...'
    else : 
        searchUrl = makeSearchUrl(ISBN, title, sid, searchFlag)
        result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.
    jsonDict = makeJsonDict(result)
    return json.dumps(jsonDict)
    




#ISBN = '9788988474839'
#koreaTitle = '데이터 분석 전문가 가이드'
#sid = KW_CODE
#title = parse.quote(koreaTitle)
#searchFlag = 2
#resultfinalfinal = findLoanStatus(ISBN, title, sid,searchFlag)
#resultfinalfinal

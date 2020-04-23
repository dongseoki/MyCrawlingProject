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
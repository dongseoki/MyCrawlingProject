from urllib.request import urlopen
from urllib import parse
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


from selenium.webdriver.chrome.options import Options
# 로컬에선 이것을 임포트


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


def findState(text, sid = -1):
    if sid == KM_CODE:
        regex = re.compile('(\w+)\s+')
        matchObj = regex.search(text)
        text = matchObj.group(1)
    # 국민대 의 경우 전처리.

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

def find_RDD(text, sid = -1):
    if sid == 1:
        regex = re.compile('(\d\d\d\d)\.(\d\d)\.(\d\d)')
        matchObj = regex.search(text)
        return matchObj.group(1)+ '-' + matchObj.group(2)+ '-' + matchObj.group(3)
    else :
        regex = re.compile('\d\d\d\d\-\d\d\-\d\d')
        matchObj = regex.search(text)
    return matchObj.group(0)


# 4단계 함수들

def isISBNCorrect(ISBN, bsObject, sid):
    try:
        if sid == KW_CODE:
            searchedISBN = find_ISBN(str(bsObject.find('div', {'id': 'divProfile'})))
        elif sid == KM_CODE:
            strISBNIncluded = str(bsObject.select('body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div:nth-child(3) > div > div.ikc-search-detail-main > div > div.ikc-biblio-detail > div.ikc-biblio-info > ul'))
            searchedISBN =find_ISBN(strISBNIncluded)
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
            includedISBNString = str(bsObject.find('div', {'class':'col-md-10 detail-table-right'}))
            searchedISBN = find_ISBN(includedISBNString)
        elif sid == SK_CODE:
            pass
        elif sid == SW_CODE:
            pass
        elif sid == SS_CODE:
            pass
        elif sid == HS_CODE:
            pass

        # 위는 정보 수집

        if ISBN == searchedISBN:
            return True
        else :
            return False

        # ISBN 같은 지 판단.
    except AttributeError:
        # 전자 자료 같은 경우. ISBN이 없다.
        return False





def makeLoanResultList(bsObject, sid):
    if sid == KW_CODE:
        loanResultList = bsObject.find('div', {'id': 'divHoldingInfo'}).find('table').find('tbody').find_all('tr')
    elif sid == KM_CODE:
        loanResultListSelectPath = 'body > div.ikc-pyxis-wrap > div.ikc-container-wrap > div.ikc-container > div.ikc-content > div.ikc-main > div:nth-child(3) > div > div.ikc-search-detail-main > div > div.ikc-detail-strip > div:nth-child(2) > ng-include > div > table'
        loanResultList = bsObject.select(loanResultListSelectPath)[0].find_all('tbody')
        ##여기 하는중
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
        loanResultList = bsObject.find('div', class_='sponge-guide-Box-table sponge-detail-table').find('tbody').find_all('tr')
    elif sid == SK_CODE:
        pass
    elif sid == SW_CODE:
        pass
    elif sid == SS_CODE:
        pass
    elif sid == HS_CODE:
        pass
    return loanResultList



def getLoanStatus(title, loanResult, loanStatusList, sid):
    errorMessage = ''
    RDD = ''
    BN = 0
    # 초기값 설정.
    if sid == KW_CODE:
        content = loanResult.find_all('td')
        RN = content[1].text.strip()
        CN = content[2].text.strip()
        POS = content[3].text.strip()
        STATE_STRING = content[4].text.strip()
        RDD = content[5].text.strip()
        STATE = findState(STATE_STRING)
    elif sid == KM_CODE:
        content = loanResult.find('tr').find_all('td')
        RN = content[0].find_all('span')[1].text.strip()
        CN = content[2].find_all('span')[1].text.strip()
        POS = content[1].find_all('span')[1].text.strip()
        STATE_STRING = content[4].find_all('span')[1].text.strip()
        STATE = findState(STATE_STRING, sid)
        if STATE == 0 :
            RDD = find_RDD(STATE_STRING, sid)
        #대출중인경우 반납예정일을 계산.

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
        BookResultList = bsObject.find('div', {'class':'ikc-main'}).find('div', {'class':'ikc-search-result'}).find_all('div', {'class':'ikc-search-item'})
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


def makeContent( sid, bookResult = None, browser=None):
    if sid == KW_CODE:
        content = bookResult.find('dd', {'class': 'searchTitle'}).find('a')
    elif sid == KM_CODE:

        linkXpath = '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]/div[4]/div/div[3]/ul/li[1]/a[1]'

        try:
            linkElement = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.XPATH, linkXpath))
    )
            #linkElement = browser.find_element_by_xpath(linkXpath)
            # 오류가능성.
        except :
            #print('예외가 발생! 찾는 책이 없음')
            linkElement = -1
        # 오류가능성.
        content = linkElement
        # 명시적으로 이름을 통일.
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


def visitLink(ISBN, sid, title, bookLink,linkElement = None, browser = None):
    loanStatusList = []
    #= LoanStatus()
    try:

        #1. 접속.
        if sid == KM_CODE:
            linkElement.click()
            #time.sleep(4)
            ISBNLinkElementXpath = '//*[@id="btn-biblio-more-open"]'
            linkElement = WebDriverWait(browser, 120).until(
        EC.presence_of_element_located((By.XPATH, ISBNLinkElementXpath))
    )
            #ISBNLinkElement = browser.find_element_by_xpath(ISBNLinkElementXpath)
            linkElement.click()
            time.sleep(4)
            html = browser.page_source

        elif sid == KW_CODE or sid == SM_CODE: 
            html = urlopen(base_start_url_list[sid]+bookLink)
        
        bsObject = BeautifulSoup(html, "html.parser")
        
        #1-1 ISBN 정보가 일치하지 않다면 바로 return!!!
        if isISBNCorrect(ISBN, bsObject, sid) == False:
            return loanStatusList

        #2. 대출 데이터를 차곡차곡저장.
        #idx = 0
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
        if sid == KM_CODE:
            options = Options()
            options.headless = True
            browser = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
            browser.get(searchUrl)
        elif sid == KW_CODE or sid == SM_CODE : 
            html = urlopen(searchUrl)
            bsObject = BeautifulSoup(html, "html.parser")

        
        #2. 링크를 차곡차곡저장.
        # 정규식과 beautifulsoap4을 이용하여 저장...!!
        if sid == KM_CODE:
            linkElement = makeContent( sid, None, browser)
            if(linkElement == -1):
                raise FileNotFoundError
                # finally로 건너 뛰자. 검색 결과가 없다.
            title = linkElement.text

        elif sid == KW_CODE or sid == SM_CODE :  
            bookLinklist =[]
            for bookResult in makeBookResultList(bsObject, sid):
                content = makeContent(sid,bookResult)
                title = content.text.strip()
                link =  content.get('href')
                bookLinklist.append([title, link])

        #3. 해당 링크를 방문하여 리스트에 추가해라..!!

        if sid == KM_CODE : 
            libraryLoanStatus.loanStatusList += visitLink(ISBN, sid, title, None,linkElement, browser)
            
        elif sid == KW_CODE or sid == SM_CODE :  
            for item in bookLinklist:
                libraryLoanStatus.loanStatusList += visitLink(ISBN, sid, item[0], item[1])
    except:
        libraryLoanStatus.errorMessage = traceback.format_exc()
        #libraryLoanStatus.errorMessage = 에러 traceback 에러메세지를 담는다.
    finally:
        if sid == KM_CODE:
            browser.quit()
        return libraryLoanStatus
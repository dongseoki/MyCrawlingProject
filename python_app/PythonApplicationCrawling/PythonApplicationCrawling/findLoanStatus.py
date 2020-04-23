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

def findLoanStatus(ISBN, title, sid, searchFlag, resultList):
    if sid != SM_CODE and sid != KW_CODE:
        result = LibraryLS(sid)
        result.errorMessage = 'Not developed...'
    else : 
        searchUrl = makeSearchUrl(ISBN, title, sid, searchFlag)
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
        searchUrl = makeSearchUrl(ISBN, title, sid, searchFlag)
        result = crawling(ISBN, title, sid, searchUrl)
    # json string 으로 만들기.
    jsonDict = makeJsonDict(result)
    return jsonDict

#isbn = request.args.get('isbn')
#koreaTitle = request.args.get('title')
#title = parse.quote(koreaTitle)
#searchFlag = request.args.get('searchFlag')

isbn = '9788968481093'
koreaTitle = '(비즈니스를 위한) 데이터 과학'
title = parse.quote(koreaTitle)
searchFlag = '2'
resultList = [i for i in range(12)]
threads = []
for i in range(12):
    t = threading.Thread(target=findLoanStatus, args=(isbn, title, i, int(searchFlag), resultList))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
jsonString =  json.dumps(resultList)
print(jsonString)
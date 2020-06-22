# coding: utf-8

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

from findLoanStatus import *
from library import *

#url = "https://lib.kookmin.ac.kr/#/total-search?keyword="


'''

def crawling(isbn):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(chrome_options=options)
#    browser.get('https://lib.kookmin.ac.kr/#/')
#    search_box = browser.find_element_by_class_name("k-input")
#    search_box.send_keys("python")
#    search_box.submit()
    browser.get(url+isbn)
#    time.sleep(1)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    item_info = soup.find("div", {"class", "ikc-item-info"})
    item_bibliotype = item_info.find("span")
    title = item_bibliotype.get_text()
    return title

'''

app = Flask(__name__)

@app.route('/')
def hello_world():
    request_json = request.get_json()
    if request.args and 'isbn' in request.args and 'title' in request.args  :
        isbn = request.args.get('isbn')
        koreaTitle = request.args.get('title')
        title = parse.quote(koreaTitle)
        
        #searchFlag = request.args.get('searchFlag')
        if 'sid' in request.args:
            sid = request.args.get('sid')
            resultList = findLoanStatus(isbn, title, int(sid))
            
        else :
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
        return jsonString

    else:
        errorDict = {'sid' : -1,  'loanStatusList': [], 'errorMessage':'Not enough input data'}
        resultList = []
        for i in range(12):
            resultList.append(errorDict)
        return json.dumps(resultList)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
    


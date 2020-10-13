from bs4 import BeautifulSoup, Doctype
import multiprocessing as mp
from time import time, sleep
import pandas as pd
import os
import requests as req
import csv
import re

class Searching:
    def URL(self, url, lang):
        sciURL = []
        Ext = ['.pdf', '.mp3', '.mp4', '.doc', '.docx', '.xls', '.ppt','.jpg','.png','.ai','.eps','JPG','search/tag.html']
        self.url = url
        self.lang = lang
        if lang == 'ja/':
            for fileext in Ext:
                if fileext in url:
                    sciURL.append(url)
                    return sciURL
            rm = req.get(url)
            soupm = BeautifulSoup(rm.text, "lxml")
            for j in soupm.find("body").find_all("a"):
                try:
                    matcherSci = re.match(r"http://www.sci.kyoto-u.ac.jp/ja", j.get("href"))
                    matcherHttp = re.match(r"http", j.get("href"))
                    matcherEn = re.match(r"/en", j.get("href"))
                    matcherSym = re.match(r"#", j.get("href"))
                except:
                    continue
                try:
                    if not matcherEn:
                        if matcherSci:
                            sciURL.append(j.get("href"))
                        elif not matcherHttp and not matcherSym and j.get("href")[0] == "/":
                            sciURL.append("http://www.sci.kyoto-u.ac.jp"+ j.get("href"))
                        elif not matcherHttp and not matcherSym and j.get("href")[0] != "/":
                            sciURL.append("http://www.sci.kyoto-u.ac.jp/ja/"+ j.get("href"))
                except:
                    continue
        elif lang == 'en/':
            for fileext in Ext:
                if fileext in url:
                    sciURL.append(url)
                    return sciURL
            rm = req.get(url)
            soupm = BeautifulSoup(rm.text, "lxml")
            for j in soupm.find("body").find_all("a"):
                try:
                    matcherSci = re.match(r"http://www.sci.kyoto-u.ac.jp/en", j.get("href"))
                    matcherHttp = re.match(r"http", j.get("href"))
                    matcherJp = re.match(r"/jp", j.get("href"))
                    matcherSym = re.match(r"#", j.get("href"))
                except:
                    continue
                try:
                    if not matcherJp:
                        if matcherSci:
                            sciURL.append(j.get("href"))
                        elif not matcherHttp and not matcherSym and j.get("href")[0] == "/":
                            sciURL.append("http://www.sci.kyoto-u.ac.jp"+ j.get("href"))
                        elif not matcherHttp and not matcherSym and j.get("href")[0] != "/":
                            sciURL.append("http://www.sci.kyoto-u.ac.jp/en/"+ j.get("href"))
                except:
                    continue
        return sciURL

    def FindIMG(self, url):
        sciURLIMG = []
        Img = ['.jpg','.png','.ai','.eps']
        Ext = ['.pdf', '.mp3', '.mp4', '.doc', '.docx', '.xls', '.ppt','JPG','search/tag.html']
        self.url = url
        for fileext in Ext:
            if fileext in url:
                return sciURLIMG
        for fileext in Img:
            if fileext in url:
                return sciURLIMG
        rm = req.get(url)
        soupm = BeautifulSoup(rm.text, "lxml")
        for j in soupm.find("body").find_all("img"):
            try:
                matcherSci = re.match(r"http://www.sci.kyoto-u.ac.jp/en", j.get("src"))
                matcherHttp = re.match(r"http", j.get("src"))
                matcherSym = re.match(r"#", j.get("src"))
            except:
                continue
            try:
                if matcherSci:
                    sciURLIMG.append(j.get("src"))
                elif not matcherHttp and not matcherSym and j.get("src")[0] == "/":
                    sciURLIMG.append("http://www.sci.kyoto-u.ac.jp"+ j.get("src"))
                elif not matcherHttp and not matcherSym and j.get("src")[0] != "/":
                    sciURLIMG.append("http://www.sci.kyoto-u.ac.jp/en/"+ j.get("src"))
            except:
                continue
        return sciURLIMG
    
    def FindFile(self, url, lang):
        sciURL = []
        Ext = ['.pdf', '.mp3', '.mp4', '.doc', '.docx', '.xls', '.ppt']
        self.url = url
        self.lang = lang
        if lang == 'ja/':
            rm = req.get(url)
            soupm = BeautifulSoup(rm.text, "lxml")
            for j in soupm.find("body").find_all("a"):
                try:
                    matcherSci = re.match(r"http://www.sci.kyoto-u.ac.jp/ja", j.get("href"))
                    matcherHttp = re.match(r"http", j.get("href"))
                    matcherSym = re.match(r"#", j.get("href"))
                except:
                    continue
                try:
                    if matcherSci:
                        sciURL.append(j.get("href"))
                    elif not matcherHttp and not matcherSym and j.get("href")[0] == "/":
                        sciURL.append("http://www.sci.kyoto-u.ac.jp"+ j.get("href"))
                    elif not matcherHttp and not matcherSym and j.get("href")[0] != "/":
                        sciURL.append("http://www.sci.kyoto-u.ac.jp/ja/"+ j.get("href"))
                except:
                    continue
        elif lang == 'en/':
            rm = req.get(url)
            soupm = BeautifulSoup(rm.text, "lxml")
            for j in soupm.find("body").find_all("a"):
                try:
                    matcherSci = re.match(r"http://www.sci.kyoto-u.ac.jp/ja", j.get("href"))
                    matcherHttp = re.match(r"http", j.get("href"))
                    matcherSym = re.match(r"#", j.get("href"))
                except:
                    continue
                try:
                    if matcherSci:
                        sciURL.append(j.get("href"))
                    elif not matcherHttp and not matcherSym and j.get("href")[0] == "/":
                        sciURL.append("http://www.sci.kyoto-u.ac.jp"+ j.get("href"))
                    elif not matcherHttp and not matcherSym and j.get("href")[0] != "/":
                        sciURL.append("http://www.sci.kyoto-u.ac.jp/en/"+ j.get("href"))
                except:
                    continue
        fileresult = []
        for url in sciURL:
            for fileext in Ext:
                if fileext in url:
                    fileresult.append(url)

        return fileresult

class Download:
    def downHtml(self, url, root_url):
        test_files = {}
        savepath = Download.downFile(url, root_url)
        if savepath is None: return
        if savepath in test_files: return
        test_files[savepath] = True
        print("downHtml=", url)
        return 0

    def downImg(self, url):
        return 0

    def downFile(self, url):
        return 0

if __name__ == '__main__':
        
    print("#######################################################################")
    print("#                                                                     #")
    print("#     This is made for crawling                                       #")
    print("#     Graduate School of Science, Kyoto University web page.          #")
    print("#     If you have any trouble with running this code,                 #")
    print("#     please send message to my e-mail.                               #")
    print("#     lee.yohan.83w@st.kyoto-u.ac.jp   (final update. 03/07/2020)     #")
    print("#                                                                     #")
    print("#######################################################################\n")

    start = time()
    Ext = ['.pdf', '.mp3', '.mp4', '.doc', '.docx', '.xls', '.ppt']
    sciURL = ["http://www.sci.kyoto-u.ac.jp/"]
    sciURLja = []
    sciURLen = []

    with mp.Pool(processes=2) as p:
        for i in range(3):
            for url in sciURL:
                print("Searching url from link " + url)
                sciURL = sciURL + Searching().URL(url, "ja/")
                sciURL = sciURL + Searching().URL(url, "en/")
            sciURL = list(set(sciURL))
            sciURL.sort()

    for url in sciURL:
        if "/en" in url:
            sciURLen.append(url)
        if "/ja" in url:
            sciURLja.append(url)

    sciURLja = list(set(sciURLja))
    sciURLen = list(set(sciURLen))
    sciURLja.sort()
    sciURLen.sort()

    for url in sciURLja:
        if ".html" in url and "search/tag.html" not in url:
            print("Listing japanese link " + url)
            pd.Series([url], index=["parent html"]).to_csv('lists_ja.csv', mode='a', header=False)
            pd.Series(["image index"], index=["image link"]).to_csv('lists_ja.csv', mode='a', header=False)
            pd.Series(Searching().FindIMG(url)).to_csv('lists_ja.csv', mode='a', header=False)
            pd.Series(["file index"], index=["file link"]).to_csv('lists_ja.csv', mode='a', header=False)
            pd.Series(Searching().FindFile(url, "ja/")).to_csv('lists_ja.csv', mode='a', header=False)
            pd.Series([""], index=[""]).to_csv('lists_ja.csv', mode='a', header=False)

    for url in sciURLen:
        if ".html" in url and "search/tag.html" not in url:
            print("Listing english link " + url)
            pd.Series([url], index=["parent html"]).to_csv('lists_en.csv', mode='a', header=False)
            pd.Series(["image index"], index=["image link"]).to_csv('lists_en.csv', mode='a', header=False)
            pd.Series(Searching().FindIMG(url)).to_csv('lists_en.csv', mode='a', header=False)
            pd.Series(["file index"], index=["file link"]).to_csv('lists_en.csv', mode='a', header=False)
            pd.Series(Searching().FindFile(url, "en/")).to_csv('lists_en.csv', mode='a', header=False)
            pd.Series([""], index=[""]).to_csv('lists_en.csv', mode='a', header=False)
        
    end = time()
    print("Lists Japanese is created in ", len(sciURLja))
    print("Lists English is created in ", len(sciURLen))
    print("Code ended in ", (end-start))

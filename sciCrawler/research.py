from bs4 import BeautifulSoup
import pandas as pd
import requests as req
import csv
import re

def find_result_html(start_pages, end_pages):
    url = "http://www.kyoto-u.ac.jp/ja/research/research_results/?b_start:int="
    card_list = []
    for page_number in range(start_pages, end_pages):
        url_page = url+str(page_number*10)
        r = req.get(url_page)
        soup = BeautifulSoup(r.text, "lxml")
        for page in soup.find("ul", attrs={"class": "achievement-list"}).find_all("li"):
            if check_department(page.find("a").get("href")):
                card = [page.find("p", attrs={"class": "text"}).text, page.find("p", attrs={"class": "date"}).text, page.find("a").get("href"), get_image(page.find("a").get("href"))]
                print(card[0])
                card_list.append(card)
    return card_list

def check_department(url):
    page_text = []
    r = req.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    for page in soup.find("div", attrs={"id": re.compile('parent-fieldname-text-.*')}).find_all("p"):
        page_text.append(page.text)
    for content in page_text:
        if re.findall("理学研究科", content):
            print("\n理学研究科関連記事が見つかりました。")
            return True
        else:
            return False

def get_image(url):
    r = req.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup.find("div", attrs={"id": re.compile('parent-fieldname-text-.*')}).find("img").get("src")


if __name__ == '__main__':
        
    print("#######################################################################")
    print("#                                                                     #")
    print("#     This is made for crawling                                       #")
    print("#     Graduate School of Science, Kyoto University web page.          #")
    print("#     If you have any trouble with running this code,                 #")
    print("#     please send message to my e-mail.                               #")
    print("#     lee.yohan.83w@st.kyoto-u.ac.jp   (final update. 29/06/2020)     #")
    print("#                                                                     #")
    print("#######################################################################\n")

    print("何ページから探しますか？")
    start_pages = input()
    if re.findall("[0-999]", start_pages):
        print("何ページまで探しますか？")
        end_pages = input()
        if not re.findall("[0-999]", end_pages):
            print("数字を入力してください。")
        else:
            url_list = find_result_html(int(start_pages)-1, int(end_pages))
            Coulum = ["TITLE", "DATE", "URL", "IMAGE"]
            pd.DataFrame(url_list, columns=Coulum).to_csv('research.csv', mode='a', encoding="cp932")
    else:
        print("数字を入力してください。")


# Inner modules
import pip, site, importlib
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time

# Downloaded modules
print("\nChecking modules requirments. It will install module not exists automatically.")
try:
    from selenium import webdriver
    print("Module [selenium] found")
except ImportError:
    print("Module [selenium] not found")
    pip.main(['install', 'selenium'])
    importlib.reload(site)
    from selenium import webdriver
try:
    import chromedriver_binary
    print("Module [chromedriver_binary] found")
except ImportError:
    print("Module [chromedriver_binary] not found")
    pip.main(['install', 'chromedriver_binary'])
    importlib.reload(site)
    import chromedriver_binary
try:
    import requests
    print("Module [requests] found")
except ImportError:
    print("Module [requests] not found")
    pip.main(['install', 'requests'])
    importlib.reload(site)
    import requests
try:
    import pandas as pd
    print("Module [pandas] found")
except ImportError:
    print("Module [pandas] not found")
    pip.main(['install', 'pandas'])
    importlib.reload(site)
    import pandas as pd
try:
    import bs4
    print("Module [beautifulsoup4] found")
except ImportError:
    print("Module [beautifulsoup4] not found")
    pip.main(['install', 'beautifulsoup4'])
    importlib.reload(site)
    import bs4
try:
    import urllib3
    print("Module [urllib3] found")
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("Module [urllib3] not found")
    pip.main(['install', 'urllib3'])
    importlib.reload(site)
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
print("All modules are ready.\n")

def pick(url, datatype):
    resp = requests.get(url, verify=False)
    try:
        soup = bs4.BeautifulSoup(resp.content, 'lxml')
    except:
        pip.main(['install', 'lxml'])
        importlib.reload(site)
        soup = bs4.BeautifulSoup(resp.content, 'lxml')
    cnts = soup.select_one("[class='row']")
    code = url.split('/')[-1]
    title = cnts.find("h1", class_="page-header").find("span").text.strip()
    group1 = cnts.find("div", class_="label font-md bg-head margin-right-xs link-white").text.strip()
    group2 = cnts.find("div", class_="label font-md bg-head link-white").find("a").text.strip()
    page_dict = dict(title=title, code=code, datatype=datatype, group1=group1, group2=group2)
    try:
        try:
            contents = cnts.find("div", class_="row clearfix").find_all("div", class_="col-xs-12")
        except:
            contents = cnts.find("div", class_="clearfix").find("div", class_="row clearfix").find_all("div", class_="col-xs-12")
        if datatype == "picture":
            for i, content in enumerate(contents):
                if i == 0:
                    media = content.find("div", class_="inline-block").find("img").get("src")
                    download_img(media)
                    d = {'media': media}
                    page_dict.update(d)
                else:
                    try:
                        comment = content.find("div", class_="margin-top-sm").text.strip()
                        d = {'comment': comment}
                        page_dict.update(d)
                    except:
                        pass
        elif datatype == "movie":
            for i, content in enumerate(contents):
                if i == 0:
                    media = content.find("div", class_="kaltura").find("iframe").get("src")
                    d = {'media': media}
                    page_dict.update(d)
                else:
                    try:
                        comment = content.find("div", class_="margin-top-sm").text.strip()
                        d = {'comment': comment}
                        page_dict.update(d)
                    except:
                        pass
    except AttributeError:
        contents = cnts.find("div", class_="carousel-inner").find_all("div", class_="item")
        for content in contents:
            media = content.find("img").get("src")
            download_img(media)
            d = {'media': media}
            page_dict.update(d)
    tables = cnts.find_all("table", class_="table table-striped")

    try:
        t = cnts.find("div", class_="bg-secondary bd-secondary padding-xs padding-left-sm padding-right-sm font-black taxonomy-term taxonomy-term--type-object taxonomy-term--view-mode-default ds-1col clearfix")
        namejp = t.find("div", class_="font-sm font-asbestos en-hide").text.strip()
        namereal = t.find("h3", class_="head-lg head-margin-xs").text.strip()
        d = {"Japanese name": namejp, "Scientific name": namereal}
        page_dict.update(d)
        names = t.find_all("div", class_="field field--name-taxonomy-term-title field--type-ds field--label-hidden field--item")
        for i, name in enumerate(names):
            if i == 0:
                d = {"Division": name.find("a").text.strip()}
                page_dict.update(d)
            elif i == 1:
                d = {"Class": name.find("a").text.strip()}
                page_dict.update(d)
    except:
        pass

    for table_0 in tables:
        table = table_0.find_all("tr")
        for row in table:
            col1 = row.find("th").text.strip()
            col2 = row.find("td").text.strip()
            d = {col1: col2}
            page_dict.update(d)

    df = pd.DataFrame.from_dict(page_dict, orient='index').T
    return df

def find_legacy():
    data = []
    for page in range(57):
        URL_base = "https://kyutubebio.sci.kyoto-u.ac.jp"
        URL="https://kyutubebio.sci.kyoto-u.ac.jp/ja/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target=All&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page="
        URL += str(page)
        resp = requests.get(URL, verify=False)
        if resp.status_code == 200:
            print("Start collecting from KyuTube archive page : ", page)
            soup = bs4.BeautifulSoup(resp.content, 'lxml')
            cards = soup.find_all("div", class_="margin-bottom-lg")
            for card in cards:
                link = card.find("h2", class_="head-xl").find("a").get("href")
                if card.find("i", class_="glyphicon-camera"):
                    d = pick(URL_base+link, "picture")
                    data.append(d)
                else:
                    d = pick(URL_base+link, "movie")
                    data.append(d)
        else:
            print("Connection Failed")
    return data

def login(driver, userid, userpw):
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

def write_html(driver, data):
    new_page_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/input")
    new_page_btn.click()

    time.sleep(0.5)

    new_file = driver.find_element_by_name("cts_filepath")
    new_title = driver.find_element_by_name("cts_title")
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")
    new_main_src = driver.find_element_by_xpath("//*[@id=\"cke_14\"]")
    new_main_img = driver.find_element_by_xpath("//*[@id=\"cke_51\"]")
    new_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[1]")
    new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")

    new_file.send_keys(data.at[0, 'code'])
    new_title.send_keys(data.at[0, 'title'])
    new_inschool.click()
    new_hidtop.click()
    new_hidtag.click()
    new_hidtext.click()
    
    if data.at[0, 'datatype'] == 'picture':
        new_main_img.click()
        time.sleep(0.5)
        new_main_img_upload = driver.find_element_by_id("cke_Upload_136")
        driver.execute_script("arguments[0].click();", new_main_img_upload)
        iframe = driver.find_element_by_xpath('//*[@id="cke_131_fileInput"]')
        driver.switch_to.frame(iframe)
        new_main_img_select = driver.find_element_by_xpath("//*[@id=\"cke_131_fileInput_input\"]")
        new_main_img_select.send_keys(os.getcwd() + f"\\kyu_img\\{data.at[0, 'media'].split('/')[-1]}")
        time.sleep(0.5)
        driver.switch_to.default_content()
        new_main_img_confirm = driver.find_element_by_id("cke_133_label")
        new_main_img_confirm.click()
        time.sleep(0.5)
        new_main_img_information = driver.find_element_by_id("cke_info_129")
        new_main_img_information.click()
        time.sleep(1.0)
        new_main_img_infotext = driver.find_element_by_id("cke_95_textInput")
        img_link = new_main_img_infotext.get_attribute('value')
        new_main_img_back = driver.find_element_by_id("cke_140_label")
        new_main_img_back.click()
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()

    new_main_src.click()
    time.sleep(0.5)
    new_main_textbox = driver.find_element_by_xpath("//*[@id=\"cke_1_contents\"]/textarea")

    try:
        comment = data.at[0, 'comment']
    except:
        comment = "" 

    if data.at[0, 'datatype'] == 'picture':
        if 'Japanese name' in data.columns:
            if '都道府県' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
            elif '国' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
            else:
                new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                <tr><th>---</th><td>---</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                <tr><th>---</th><td>---</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
        else:
            if '都道府県' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
            elif '国' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")                    
            else:
                new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                <tr><th>---</th><td>---</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                <tr><th>---</th><td>---</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
    elif data.at[0, 'datatype'] == 'movie':
        if 'Japanese name' in data.columns:
            if '都道府県' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
            elif '国' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                    <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")                    
            else:
                new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><h4>{data.at[0, 'Japanese name']}</h4> \
                <h3>{data.at[0, 'Scientific name']}</h3><p><strong>門</strong><br />{data.at[0, 'Division']}<br /><strong>綱</strong><br />{data.at[0, 'Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                <tr><th>---</th><td>---</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                <tr><th>---</th><td>---</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
        else:
            if '都道府県' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>都道府県</th><td>{data.at[0, '都道府県']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")                    
            elif '国' in data.columns:
                try:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>{data.at[0, '地域']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
                except:
                    new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                    src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                    <tbody><tr><th>国</th><td>{data.at[0, '国']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                    <tr><th>地域</th><td>---</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                    <tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                    <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                    <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                    <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
            else:
                new_main_textbox.send_keys(f"<h2>{data.at[0, 'group1']} {data.at[0, 'group2']} {str.upper(data.at[0, 'code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data.at[0, 'media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>撮影日</th><td>{data.at[0, '撮影日']}</td><th>顕微鏡の利用</th><td>{data.at[0, '顕微鏡の利用']}</td></tr> \
                <tr><th>撮影時刻</th><td>{data.at[0, '撮影時刻']}</td><th>自動撮影装置の利用</th><td>{data.at[0, '自動撮影装置の利用']}</td></tr> \
                <tr><th>撮影者</th><td>{data.at[0, '撮影者']}</td><th>赤外線</th><td>{data.at[0, '赤外線']}</td></tr> \
                <tr><th>著作権者</th><td>{data.at[0, '著作権者']}</td><th>蛍光プローブ</th><td>{data.at[0, '蛍光プローブ']}</td></tr> \
                <tr><th>---</th><td>---</td><th>時間間隔 (秒)</th><td>{data.at[0, '時間間隔 (秒)']}</td></tr> \
                <tr><th>---</th><td>---</td><th>速度</th><td>{data.at[0, '速度']}</td></tr></tbody></table>")
    new_main_src.click()
    time.sleep(0.5)

    new_confirm.click()
    time.sleep(1.0)
    new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
    new_confirm_confirm.click()
    time.sleep(2.0)
    new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
    new_confirm_back.click()
    time.sleep(0.5)

def download_img(link):
    img_path = './kyu_img'
    if 'kyutubebio' not in link:
        link = "https://kyutubebio.sci.kyoto-u.ac.jp" + link
    if not os.path.isdir(img_path):
        os.makedirs(img_path)
    if not os.path.isfile(img_path + '/' + link.split('/')[-1]):
        re = requests.get(link, verify=False)
        with open(img_path + '/' + link.split('/')[-1], 'wb') as f:
            f.write(re.content)

def check_data(title, data):
    for i, data_pd in enumerate(data):
        if title == data_pd.at[0, 'title']: #ここを直す
            del data[i]
            print(f"{title} exists.")
    return data

if __name__ == "__main__":
    do_find = input("Do you want to collecting data from KyuTube(y/n)? : ")
    if do_find == "y":
        kt_data = find_legacy()
    else:
        print("Pass collecting data.")
    print()
    userid = "lee"
    userpw = "Mv3qKTUH"
    #userid = input("Enter your admin id: ")
    #userpw = input("Enter your admin password: ")

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/ja/admin/")
    login(driver, userid, userpw)

    time.sleep(0.5)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()

    time.sleep(0.5)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[15]/td[7]/input[2]")
    kyutube_btn.click()

    time.sleep(0.5)
    total_page = 0

    while True:
        print("KyU Tube Bio List INDEX")
        print("3\t構造生理学\t\t4\tゲノム情報発現学\t\t5\t神経生物学")
        print("6\t理論生物物理学\t\t7\t分子生体情報学\t\t8\t分子発生学")
        print("9\t植物生理学\t\t10\t形態統御学\t\t11\t植物分子細胞生物学")
        print("12\t植物分子遺伝学\t\t13\t植物系統分類学\t\t14\t動物系統学")
        print("15\t動物行動学\t\t16\t動物生態学\t\t17\t動物発生学")
        print("18\t環境応答遺伝子科学\t\t19\t自然人類学\t\t20\t人類進化論")
        i = int(input("Choose INDEX number : "))
        title = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[3]")
        title_text = title.text
        data_temp = []
        for d in kt_data:
            if d.at[0, 'group2'] == title.text:
                data_temp.append(d)
        len_first = len(data_temp)
        print("Searching element in title : " + title_text)
        title_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[7]/input[2]")
        title_btn.click()
        
        time.sleep(0.5)

        title_sib_list = driver.find_elements_by_class_name("ctlr-line")
        print(f"Found {len(title_sib_list)} lists")
        total_page += len(title_sib_list)
        if len(title_sib_list) != 0:
            for j in range(2, len(title_sib_list)+2):
                title_sib_title = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{j}]/td[3]")
                sib_text = title_sib_title.text
                data_temp = check_data(sib_text, data_temp)
            if len(data_temp) != 0:
                for k, t in enumerate(data_temp):
                    print(f"{t.at[0, 'title']} doesn't exist.")
                    write_html(driver, t)
        elif len(title_sib_list) == 0:
            for k, t in enumerate(data_temp):
                print(f"{t.at[0, 'title']} doesn't exist.")
                write_html(driver, t)
        back = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
        back.click()
        time.sleep(0.5)

        a = input("Do MORE?(y/n) : ")
        if a == "n":
            break

    print("Total page exists : ", total_page)
    print("Need to be created : ", len(kt_data) - total_page)
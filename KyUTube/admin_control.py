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

def login(driver, userid, userpw):
    """
    京都大学理学研究科の管理者ページにログインします。
    入力されたIDとPWを管理者画面のログインページの入力蘭にそれぞれ入力し、
    確認ボタンを押してくれます。
    """
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

def page_edit(driver, data):
    """
    新規作成を処理します。
    """
    #ここで編集画面のボタンを操作します。チェックボックスをクリックしたりする動作や画像のファイルをアップロード等が可能です。
    new_file = driver.find_element_by_name("cts_filepath")
    new_title = driver.find_element_by_name("cts_title")
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")

    #アップロードの仕組みは、パソコンの経路をhtmlのinputタグに送ればそれを認識するようになっています。
    upload_thumb = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[9]/td/input[2]")
    if data.at[0, 'datatype'] == "image":
        upload_thumb.send_keys(os.getcwd() + f"\\kyu_img\\{data.at[0, 'media'].split('/')[-1]}")
    elif data.at[0, 'datatype'] == "movie":
        upload_thumb.send_keys(os.getcwd() + f"\\kyu_img\\{data.at[0, 'code']}" + ".jpg")
    time.sleep(0.5)

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
    
    #ここからは、CKEditorの操作に入ります。
    #CKEditorのメインのボタンはそのまま操作が可能ですが、各ボタンを押した後に出てくるポップアップはiframeの中にあるので、
    #iframeに移して、必要な操作をし、またそこから抜け出すという流れに作業を行います。
    if data.at[0, 'datatype'] == 'picture':
        new_main_img.click()
        time.sleep(0.5)
        new_main_img_upload = driver.find_element_by_id("cke_Upload_136")
        driver.execute_script("arguments[0].click();", new_main_img_upload)

        #画像の添付画面のiframeへ移動
        iframe = driver.find_element_by_xpath('//*[@id="cke_131_fileInput"]')
        driver.switch_to.frame(iframe)
        new_main_img_select = driver.find_element_by_xpath("//*[@id=\"cke_131_fileInput_input\"]")
        new_main_img_select.send_keys(os.getcwd() + f"\\kyu_img\\{data.at[0, 'media'].split('/')[-1]}")
        time.sleep(0.5)

        #画像の添付が終わったので、抜け出し
        driver.switch_to.default_content()
        new_main_img_confirm = driver.find_element_by_id("cke_133_label")
        new_main_img_confirm.click()
        time.sleep(0.5)
        new_main_img_information = driver.find_element_by_id("cke_info_129")
        new_main_img_information.click()
        time.sleep(1.0)

        #アップロードされた画像のurlを取得
        #たまに、ページに画像が貼られてない原因がここです。
        #アップロードしてからurlを出力するまで時間がかかってします時があって、それを待たずに次へと行ってしますと、
        #画像のurlが空のままhtmlページを作成してしまったのです。
        new_main_img_infotext = driver.find_element_by_id("cke_95_textInput")
        img_link = new_main_img_infotext.get_attribute('value')
        new_main_img_back = driver.find_element_by_id("cke_140_label")
        new_main_img_back.click()

        #ここでは、自動添付ではなく、urlを使って作成するので、キャンセルを押します。
        #そうすると、確認のポップアップが出てきますが、それの操作をします。
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()

    new_main_src.click()
    time.sleep(0.5)
    new_main_textbox = driver.find_element_by_xpath("//*[@id=\"cke_1_contents\"]/textarea")

    #CKEditorのソース編集のところにhtmlソースを送ります。
    #KyuTubeBioのページには値が無かったり、写真が複数あったりしていろんな形式があるので、
    #それをできるだけ対応させようとしました。（複数画像は考え中）
    #確認だけがしたい場合は、以下の動作を消してください。
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

    #最後に確認のボタンを押します。
    #とりあえずここでは新規作成の場合（最後のボタンが「戻る」と「確認」）と編集の場合（最後のボタンが「公開」と「戻る」と「確認」）にわけて、
    #確認し編集を終わる段階へと行きます。
    #もし、公開ボタンを押す場合は、それに当たるxpathを指定してあげればオッケーです。
    try:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[3]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

    except:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

if __name__ == "__main__":
    userid = input("Enter your admin id: ")
    userpw = input("Enter your admin password: ")

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/ja/admin/")
    login(driver, userid, userpw)

    #研究ページへ
    time.sleep(0.5)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()

    #KyuTubeBioページへ
    time.sleep(0.5)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[15]/td[7]/input[2]")
    kyutube_btn.click()

    time.sleep(0.5)
    total_page = 0

    while True:
        print("KyU Tube Bio List INDEX")
        print("3\t構造生理学\t\t4\tゲノム情報発現学\t5\t神経生物学")
        print("6\t理論生物物理学\t\t7\t分子生体情報学\t\t8\t分子発生学")
        print("9\t植物生理学\t\t10\t形態統御学\t\t11\t植物分子細胞生物学")
        print("12\t植物分子遺伝学\t\t13\t植物系統分類学\t\t14\t動物系統学")
        print("15\t動物行動学\t\t16\t動物生態学\t\t17\t動物発生学")
        print("18\t環境応答遺伝子科学\t19\t自然人類学\t\t20\t人類進化論")
        i = int(input("Choose INDEX number : "))
        title = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[3]")
        title_text = title.text
        print("Searching element in title : " + title_text)
        title_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[7]/input[2]")
        title_btn.click()
        time.sleep(0.5)

        temp = []

        try:
            #ページ数が25件を超える場合
            page_num = int(driver.find_element_by_xpath("//*[@id=\"container\"]/div[4]/span").text[0])
            for i in range(3, page_num+2):
                title_sib_list = driver.find_elements_by_class_name("ctlr-line")
                for j in range(2, len(title_sib_list)+2):
                    title_sib_edit = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{j}]/td[7]/input")
                    title_sib_edit.click()
                    time.sleep(0.5)
                    page_edit(driver, temp)

                next_page = driver.find_element_by_xpath(f"//*[@id=\"container\"]/div[4]/ul/li[{i}]")
                next_page.click()
                time.sleep(0.5)

            title_sib_list = driver.find_elements_by_class_name("ctlr-line")
            for j in range(2, len(title_sib_list)+2):
                title_sib_edit = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{j}]/td[7]/input")
                title_sib_edit.click()
                time.sleep(0.5)
                page_edit(driver, temp)

            first_page = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
            first_page.click()
            time.sleep(0.5)

        except:
        #ページ数が25件以下
            title_sib_list = driver.find_elements_by_class_name("ctlr-line")
            print(f"Found {len(title_sib_list)} lists")
            total_page += len(title_sib_list)
            if len(title_sib_list) != 0:
                for j in range(2, len(title_sib_list)+2):
                    title_sib_edit = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{j}]/td[7]/input")
                    title_sib_edit.click()
                    time.sleep(0.5)
                    page_edit(driver, temp)
            first_page = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
            first_page.click()
            time.sleep(0.5)

        a = input("Do MORE?(y/n) : ")
        if a == "n":
            break
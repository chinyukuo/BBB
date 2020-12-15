# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 00:03:55 2020

@author: Asus
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from bs4 import BeautifulSoup
import json
import mysql.connector
from mysql.connector import Error

"https://www.instagram.com/"
def use_fb():
    options = Options()
    options.add_argument("--disable-notifications")
    chrome = webdriver.Chrome('D:\git/chromedriver', chrome_options=options)
    chrome.get("https://www.facebook.com/")
    email = chrome.find_element_by_id("email")
    password = chrome.find_element_by_id("pass")
    email.send_keys('bigbird7887@gmail.com')
    password.send_keys('biging888')
    password.submit()
#讓使用者登入追蹤他的好友
    time.sleep(3)
    chrome.get('https://www.facebook.com/learncodewithmike')
    for x in range(1, 4):
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    titles = soup.find_all('span', {
        'class': 'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7'})
 
    for title in titles:
        print(title.getText())
    chrome.quit()
    
def use_ig():
    options = Options()
    options.add_argument("--disable-notifications")
    chrome = webdriver.Chrome('D:\git/chromedriver', chrome_options=options)
    chrome.get("https://www.instagram.com/")
    time.sleep(15)
    email = chrome.find_element_by_name("username")
    password = chrome.find_element_by_name("password")
    email.send_keys('travel_fun_test')
    password.send_keys('biging888')
    password.submit()
#讓使用者登入追蹤他的好友
    time.sleep(3)

    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    #chrome.quit()
#chrome.quit()  #關閉瀏覽器

def selenium_ig(url):
    options = Options()
    options.add_argument("--disable-notifications")
    chrome = webdriver.Chrome('D:\git/chromedriver', chrome_options=options)
    chrome.get(url)
    time.sleep(5)
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    chrome.quit()
    r = str(soup).split(';">')[1].split('</pre>')[0]
    #到此處r為原本request到的內容
    return r
    
    now = datetime.datetime.now() 
    locate_name = now.strftime("selenium_test" + "  %Y_%m_%d_%H_%M_%S" + ".txt")
    dest_dir = "D:\git\ig/"
    file_name = dest_dir + locate_name
    with open(file_name, 'w') as outfile:
        outfile.write(r)# save to json
    
    #,encoding = 'utf-16'

def get_post_time(data):        #取得文章日期
    #需要傳入文章date
    #1091120 update
    post_time = data['graphql']['shortcode_media']['taken_at_timestamp']
    return post_time
    #取得拍攝仁和時間資訊    

def parseig_location():
    arr = []
    end_cursor = '' # empty for the 1st page
    tag = 'taipei' # tag
    page_count = 1 # desired number of pages
    for i in range(0, page_count):
        url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
        r = selenium_ig(url)
        data = json.loads(r)
        end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] # value for the next page
        edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
    
        for item in edges:
            arr.append(item['node'])
        time.sleep(5)
    locations = []
    locate = []
    for item in arr:
        shortcode = item['shortcode']
        url = "https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
        time.sleep(5)
        r = selenium_ig(url)
        data = json.loads(r)
        try:
            location = data['graphql']['shortcode_media']['location']['name'] # get location for a post
        except:
            location = '' # if location is NULL
        stamptime = get_post_time(data)
        locations.append({'shortcode': shortcode, 'location': location , 'stamptime':stamptime })
        if len(location) > 0:
            print(location)
            print(stamptime)
            locate.append(location)
            
    now = datetime.datetime.now() 
    locate_name = now.strftime(tag + "  %Y_%m_%d_%H_%M_%S" + ".txt")
    dest_dir = "D:\git\ig/"
    file_name = dest_dir + locate_name
    with open(file_name, 'w',encoding = 'utf-16') as outfile:
        outfile.write(str(locations))# save to json
    update_data(tag,file_name)

def update_data(tag,file_name):
    shortcodes = []
    locations = []
    now = datetime.datetime.now() 
    file = open((file_name) , 'r', encoding='utf16')
    content = file.read()
    file.close()
    item = content.split("}, {'")
    for i in item:
        location = i.split("'location': ")[1].split(", 'stamptime'")[0]
        if location != "''" and location != "''}]":
            location = location[1:-1]
            shortcode = i.split("shortcode': ")[1].split(", 'location':")[0]
            shortcode = shortcode[1:-1]
            timestamp = i.split("'stamptime':")[1].lstrip()
            print("shortcode:{shortcode},location:{location},timestamp:{timestamp}".format(shortcode = shortcode,location = location,timestamp = timestamp))
            print(judge_shortcode(shortcode))
            if judge_shortcode(shortcode) == "Repeated_shortcode" :
                print("已經有了啦")
                continue
            else:
                link_database(location,shortcode,timestamp)
    read_database()

def judge_shortcode(given_shortcode):
    try:
    # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='bbb', # 資料庫名稱
            user='root',        # 帳號
            password='1234')  # 密碼
        
        x = "not_repeated"
        if connection.is_connected():
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,view_name,shortcode,timestamp) in cursor:
                if given_shortcode == shortcode:
                    x = "Repeated_shortcode"
                    break
                else:
                    x = "ok"
            return x

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

def link_database(view,code,time): 
    try:
    # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='bbb', # 資料庫名稱
            user='root',        # 帳號
            password='1234')  # 密碼

        if connection.is_connected():

        # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)


            view_ids = []
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,view_name,shortcode,timestamp) in cursor:
                view_ids.append(view_id)
            view_id = max(view_ids) + 1
            view_name = view
            shortcode = code
            timestamp = time
            #INSERT INTO `location` (`view_id`, `view_name`, `shortcode`) VALUES ('2', 'The Misanthrope Society 厭世會社', 'CIK4d_QHHpc');
            sql = "INSERT INTO `location` (`view_id`, `view_name`, `shortcode`,`timestamp`) VALUES (" + "'" + str(view_id) + "'" + "," + "'" + view_name + "'" + "," + "'" + shortcode +"'"  +  "," + "'" + timestamp +"'" +   ");"
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
            
def read_database():
    try:
    # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='bbb', # 資料庫名稱
            user='root',        # 帳號
            password='1234')  # 密碼

        if connection.is_connected():
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,view_name,shortcode,timestamp) in cursor:
                print('view_id: {0} , view_name: {1} ,shortcode: {2}'.format(view_id,view_name,shortcode))

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
            
parseig_location()
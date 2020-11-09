# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 20:31:06 2020

@author: Asus

crawler 整合
109.11.09加入資料庫連接

需要新增
需更改ig地點
add a function auto run parse mobile01 every area

"""

import urllib.request as req
import json
import codecs
import datetime
import requests
import time
import mysql.connector
from mysql.connector import Error

def choose_city():
    print('選擇地區')
    global city_list
    city_list = ["基隆市","台北市","新北市","桃園市", "新竹市" ,"新竹縣","苗栗縣","台中市","","彰化縣","南投縣","雲林縣","嘉義市","嘉義縣","台南市","","高雄市","","屏東縣","台東縣","花蓮縣","宜蘭縣","澎湖縣","金門縣","連江縣"]
    for i, city in enumerate(city_list, 1):
        if city == "":
            continue
        
        print(i, city)
    city_num = int(input("輸入城市編號:"))
    return city_num


def parseMobile01():
    #url = "https://www.ptt.cc/bbs/movie/index.html"
    city_num = choose_city()
    url = "https://www.mobile01.com/topiclist.php?f=" + str(city_num+187)
    #建立一個Request,附加header
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    items = []
    article_block = data.split('"c-listTableTd__title">')
    #split的第二段才是第一篇，所以在for中要從第二段開始
    i = 1
    for a in article_block[1:]:
        link = 'https://www.mobile01.com/'+a.split('href="')[1].split('"')[0]
        title = a.split('c-link u-ellipsis" >')[1].split('</a>')[0]
        #print(str(i) + ": " + title)
        #print(link)
        if len(title)>0 and len(link)>0:
            items.append([title,link])
        i += 1  
        
    now = datetime.datetime.now()        
    json_name = now.strftime(city_list[city_num-1] + "%Y_%m_%d_%H_%M_%S" + ".json")
    row_json = json.dumps(dict(items), ensure_ascii=False)
    dest_dir = "D:\git/"
    file = codecs.open(dest_dir + json_name , 'w', encoding='utf-16')
    file.write(row_json)
    file.close()

def load_json():
    with open('out.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    for x in data:
        print(x)
        print(data[x])
        
def parseig_location():
    arr = []
    end_cursor = '' # empty for the 1st page
    tag = 'taipei' # tag
    page_count = 1 # desired number of pages
    for i in range(0, page_count):
        url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor)
        r = requests.get(url)
        data = json.loads(r.text)
    
        end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] # value for the next page
        edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges'] # list with posts
    
        for item in edges:
            arr.append(item['node'])
        time.sleep(2) # insurence to not reach a time limit
#print(end_cursor) # save this to restart parsing with the next page
    with open('D:\git\ig/posts.json', 'w') as outfile:
        json.dump(arr, outfile) # save to json
    
    with open('D:\git\ig/posts.json', 'r') as f:
        arr = json.loads(f.read()) # load json data from previous step
    locations = []
    locate = []
    for item in arr:
        shortcode = item['shortcode']
        url = "https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
    
        r = requests.get(url)
        data = json.loads(r.text)
        try:
            location = data['graphql']['shortcode_media']['location']['name'] # get location for a post
        except:
            location = '' # if location is NULL
        locations.append({'shortcode': shortcode, 'location': location})
        if len(location) > 0:
            print(location)
            locate.append(location)
        # save to json
#with open('D:\git\ig/locations.json', 'w',encoding = 'utf-16') as outfile:
#   json.dump(locations, outfile) # save to json
    now = datetime.datetime.now() 
    locate_name = now.strftime(tag + "  %Y_%m_%d_%H_%M_%S" + ".txt")
    dest_dir = "D:\git\ig/"
    with open(dest_dir + locate_name, 'w',encoding = 'utf-16') as outfile:
        outfile.write(str(locations))# save to json
#需更改項目
#改存檔檔名
#try to save in json
def read_post_json(origin_html):
    jsonObj = origin_html
    dictObj = json.loads(jsonObj)
    #print(dictObj)
    #print(type(dictObj))
    origin_jsonObj = json.dumps(dictObj,sort_keys=True,indent=4)
    #print("整理好的json")
    return origin_jsonObj
    
def read_json():
    #呼叫上面read_post_json
    shortcode = input("shortcode")
    url = "https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
    r = requests.get(url)
    
    file = open("D:\git\ig/json123.txt", "w")
    file.write(read_post_json(r.text))
    file.close()
    print('done')
    #把json縮牌以方便找到需要的資訊

def link_database(): 
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
            for (view_id,picture,view_name) in cursor:
                print("view_id: %d" % view_id)
                view_ids.append(view_id)
            view_id = max(view_ids) + 1
            view_name = "小豐年公園"
            #INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES ('16', NULL, '復興崗');
            sql = "INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES (" + "'" + str(view_id) + "'" + ", NULL, "+"'"+ view_name + "'" + ");"
            print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,picture,view_name) in cursor:
                print("view_id: %d" % view_id)
                print("view_name: %s" % view_name)

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
        
if __name__ == '__main__':
    print("1.mobile01")
    print("2.ig_location")
    print("3.ig_one_post_json")
    print("4.test link database")
    print("0.exit")
    chose_function = int(input("want to do"))
    if chose_function == 1:
        parseMobile01()
    elif chose_function == 2:
        parseig_location()
    elif chose_function == 3:
        read_json()
    elif chose_function == 4:
        link_database()
    elif chose_function == 0:
        print('doing nothing')
    else :
        print("no function")

    #load_json() 輸出內容


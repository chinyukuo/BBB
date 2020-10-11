# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 23:27:50 2020

@author: Asus
"""
#ig new 190_10_10
import urllib.request as req
import json
import codecs
import datetime


#ig by beautifulsoup 2020
def parseig():
    #抓ig搜尋hashtag的頁面
    url = "https://www.instagram.com/explore/tags/taipei/?hl=zh-tw"
    #建立一個Request,附加header
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    items = []
    article_block = data.split('"shortcode":"')
    #split的第二段才是第一篇，所以在for中要從第二段開始
    
    for a in article_block[1:]:
        #正確for:for a in article_block[1:]:
        link = 'https://www.instagram.com/p/'+a.split('","edge_media_to_comment"')[0]+'/'
        parseig_one(link)
        #print(str(i) + ": " + title)
        #print(link)
        if len(link)>0:
            items.append(link)
            print(link)
    
def parseig_one(url_input):
    #抓ig中其中一篇文章
    url = url_input
    #建立一個Request,附加header
    request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data_one = response.read().decode("utf-8")
    
    
        
    now = datetime.datetime.now()        
    json_name = now.strftime("%Y_%m_%d_%H_%M_%S" + "ig.txt")
    dest_dir = "D:\git\ig/"
    file = codecs.open(dest_dir + json_name , 'w', encoding='utf-8')
    file.write(data_one)
    file.close()
    print('done')
    
    
def load_json():
    with open('out.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    for x in data:
        print(x)
        print(data[x])
        
if __name__ == '__main__':
    parseig()
    #load_json() 輸出內容

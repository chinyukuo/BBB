import urllib.request as r
import json
import os
import requests
#from bs4 import BeautifulSoup
#import jsonpath
#開啟照片用

url = "https://www.instagram.com/explore/tags/taipeicafe/?__a=1"
request = r.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
})

html = r.urlopen(request)
origin_html = html.read()

print("未使用beautifulsoup的html")
print(html)

with r.urlopen(request) as response:
    data = response.read().decode("utf-8")

print("擷取到的json")
print(data)


#2020/4/27
jsonObj = origin_html
dictObj = json.loads(jsonObj)
#print(dictObj)
#print(type(dictObj))
origin_jsonObj = json.dumps(dictObj,sort_keys=True,indent=4)
print("整理好的json")
print(origin_jsonObj)
dict_obj = json.loads(origin_jsonObj)
print("python_dict:",dict_obj)
print(type(dict_obj))
print("利用loads()將json轉成python的字典")
print("再從字典中抓取照片網址")
picture_url = dict_obj["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"][0]["node"]["display_url"]

#[hashtag][edge_hashtag_to_media][edges][node][display_url]
print(picture_url)

#下載圖片
destDir = 'D:\git\photo/'
img = requests.get(picture_url)
#把jpg名稱改掉
with open(destDir + 'a.jpg' , 'wb') as f:
    f.write(img.content)

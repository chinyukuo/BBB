import urllib.request as r
import json
import os
import requests
import datetime
#from bs4 import BeautifulSoup
#import jsonpath
#開啟照片用

url = "https://www.instagram.com/explore/tags/chiayi/?__a=1"
#取得hahtag名稱
#可以再找更好方式
spilt_url = url.split('/')
hashtag = spilt_url[5]

#更改地點
def change_locate(locate_name):
    global url
    url = url.replace(hashtag, locate_name)

change_locate(input('請輸入搜尋hashtag：'))
print(url)

spilt_url = url.split('/')
hashtag = spilt_url[5]


request = r.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
})


html = r.urlopen(request)
origin_html = html.read()


#print(html)

with r.urlopen(request) as response:
    data = response.read().decode("utf-8")

print("擷取到的json")
print(data)

#20200927嘗試輸出成檔案
file = open("html.txt", "w")
file.write(data)
file.close()
print('done')

#2020/4/27
jsonObj = origin_html
dictObj = json.loads(jsonObj)
#print(dictObj)
#print(type(dictObj))
origin_jsonObj = json.dumps(dictObj,sort_keys=True,indent=4)
print("整理好的json")
#print(origin_jsonObj)
dict_obj = json.loads(origin_jsonObj)
#2020/5/4
print("python_dict:",dict_obj)
print(type(dict_obj))
print("利用loads()將json轉成python的字典")
print("再從字典中抓取照片網址")
#picture_url = dict_obj["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"][0]["node"]["display_url"]
counter = 0
picture_url = []
for i in range(10):
    picture_url.append(i)

for counter in range(10):
    picture_url[counter] = dict_obj["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"][counter]["node"]["display_url"]
#[hashtag][edge_hashtag_to_media][edges][node][display_url]

#下載圖片
#2020/5/11改以時間命名下載的圖片
#改成一次抓取多張hashtag 照片
print("抓取圖片")
now = datetime.datetime.now()

for i in range(10):
    jpg_name = now.strftime("%Y_%m_%d_%H_%M_%S")
    i_as_string = str(i)
    #用hashtag標籤和時間命名圖片
    jpg_name = hashtag + "_" + jpg_name + "_" + i_as_string + ".jpg"
    destDir = 'D:\git\photo/'
    img = requests.get(picture_url[i])
    with open(destDir + jpg_name , 'wb') as f:
        f.write(img.content)


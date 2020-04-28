import urllib.request as r
import json
from bs4 import BeautifulSoup
import jsonpath

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

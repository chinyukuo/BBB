import urllib.request as req
import json
import codecs
import datetime

def choose_city():
    print('選擇地區')
    global city_list
    city_list = ["基隆市","台北市","新北市","桃園市", "新竹市" ,"新竹縣","苗栗縣","台中市","","彰化縣","南投縣","雲林縣","嘉義市","嘉義縣","台南市","高雄市","","屏東縣","台東縣","花蓮縣","宜蘭縣","澎湖縣","金門縣","連江縣"]
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
    file = codecs.open(dest_dir + json_name , 'w', encoding='utf-8')
    file.write(row_json)
    file.close()

def load_json():
    with open('out.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    for x in data:
        print(x)
        print(data[x])
        
if __name__ == '__main__':
    parseMobile01()
    #load_json()

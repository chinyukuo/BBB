#使用loads()將json格是資料轉成python的資料
import json

jsonObj = '{"b":80, "a":25, "c":60}'
dictObj = json.loads(jsonObj)
print(dictObj)
print(type(dictObj))

#一個json文件中指會有一個json物件
#一次有多個json物件，可以用一個父json物件處理
#Facebook，IG資料以上此方式處理
obj = '{"Asia" :[{"Japan":"Tokyo"},{"China":"Beiging"}]}'
json_obj = json.loads(obj)
print(json_obj)
print(json_obj["Asia"])
print(json_obj["Asia"][0])
print(type(json_obj))

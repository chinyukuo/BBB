#使用loads()將json格是資料轉成python的資料
import json

jsonObj = '{"b":80, "a":25, "c":60}'
dictObj = json.loads(jsonObj)
print(dictObj)
print(type(dictObj))


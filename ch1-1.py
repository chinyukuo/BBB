#python資料轉成json
import json

listNumbers = [5, 10, 20, 1]
tupleNumbers = (1, 5, 10, 9)
jsonDate1 = json.dumps(listNumbers)
jsonDate2 = json.dumps(tupleNumbers)
print("list to json:", jsonDate1)
print("tuple to json:", jsonDate2)
print("json陣列在python 中的資料形式:", type(jsonDate1))

listObj = [{'Name':'Peter','Age':25,'Gender':'M'}]
jsonDate = json.dumps(listObj)
print("list to json:", jsonDate)
players = {
    'Stephen Curry':'Golden State Warriors',
    'Kevin Durant':'Golden State Warriors',
    'Lebron James':'Cleveland Cavaliers'
}
#python的字典是無序的，使用dumps()將python資料轉乘json物件時，使用sort_keys = true，則可以將轉成json格式的物件排序
jsonObj1 = json.dumps(players)
jsonObj2 = json.dumps(players, sort_keys = True)
print("未使用sort_keys = True將字典轉成json", jsonObj1)
print("使用sort_keys = True將字典轉成json", jsonObj2)
print("json陣列在python 中的資料形式未使用sort_keys = True，:", type(jsonObj1))
print("json陣列在python 中的資料形式使用sort_keys = True，:", type(jsonObj2))
#pyton 是用一行字串方式顯示json，可以用indent參數設定縮排
jsonObj3 = json.dumps(players, sort_keys = True, indent = 4)
print("用indent參數設定縮排:", jsonObj3)

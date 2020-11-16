# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 16:38:54 2020

@author: Asus
"""

import json
import datetime
import requests
import time
def parseig_which_location():
    arr = []
    user_name = 'leemider' # tag
    page_count = 1 # desired number of pages
    for i in range(0, page_count):
        url = "https://www.instagram.com/{0}/?__a=1".format(user_name)
        r = requests.get(url)
        data = json.loads(r.text)
    
        edges = data['graphql']['user']['edge_owner_to_timeline_media']['edges'] # list with posts
    
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
    now = datetime.datetime.now() 
    locate_name = now.strftime(user_name + "  %Y_%m_%d_%H_%M_%S" + ".txt")
    dest_dir = "D:\git\ig/"
    with open(dest_dir + locate_name, 'w',encoding = 'utf-16') as outfile:
        outfile.write(str(locations))# save to json
    print('done')
#需更改項目
#改存檔檔名
if __name__ == '__main__':
    parseig_which_location()
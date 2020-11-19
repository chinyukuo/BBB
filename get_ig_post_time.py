# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 22:29:37 2020

@author: Asus
"""

import urllib.request as req
import json
import codecs
import datetime
from datetime import datetime as ds
import requests
import time
import mysql.connector
from mysql.connector import Error
    
def get_post_time(get_shortcode):        #取得文章日期
    #需要傳入文章shortcode
    #1091120 update
    shortcode = get_shortcode
    url = "https://www.instagram.com/p/{0}/?__a=1".format(shortcode)
    re = requests.get(url)
    data1 = json.loads(re.text)
    #post_time = data1["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][0]["node"]["accessibility_caption"]
    post_time = data1['graphql']['shortcode_media']['taken_at_timestamp']
    #date_posted_human = ds.fromtimestamp(post_time).strftime("%d/%m/%Y %H:%M:%S")
    date_posted_human = ds.fromtimestamp(post_time).strftime("%d/%m/%Y")
    #right function
    print(date_posted_human)
    print('done')
    #取得拍攝仁和時間資訊


if __name__ == '__main__':
    get_post_time("CHapK01BI66")
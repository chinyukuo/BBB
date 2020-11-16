# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 22:34:52 2020

update to database

@author: Asus
"""

import datetime
import mysql.connector
from mysql.connector import Error


def update_data(tag):
    shortcodes = []
    locations = []
    now = datetime.datetime.now() 
    #locate_name = now.strftime(tag + "  %Y_%m_%d" + ".txt")
    #dest_dir = "D:\git\ig/"
    #with open(dest_dir + locate_name,'r') as f: (先更換成已有檔案已做測試)
    #with open("D:\git\ig/taipei  2020_11_15.txt","r",encoding='utf-8') as f:
    #    content = f.read()
    #    item = content.split("}, {")
    file = open("D:\git\ig/taipei  2020_11_15.txt" , 'r', encoding='utf16')
    content = file.read()
    file.close()
    item = content.split('}, {')
    for i in item:
        location = i.split("'location': ")[1]
        if location != "''" and location != "''}]":
            location = location[1:-1]
            shortcode = i.split("shortcode': ")[1].split(", 'location':")[0]
            shortcode = shortcode[1:-1]
            print("shortcode:{shortcode},location:{location}".format(shortcode = shortcode,location = location))
            link_database(location)
    read_database()

def link_database(view): 
    try:
    # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='bbb', # 資料庫名稱
            user='root',        # 帳號
            password='1234')  # 密碼

        if connection.is_connected():

        # 顯示資料庫版本
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)


            view_ids = []
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,picture,view_name) in cursor:
                view_ids.append(view_id)
            view_id = max(view_ids) + 1
            view_name = view
            #INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES ('16', NULL, '復興崗');
            sql = "INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES (" + "'" + str(view_id) + "'" + ", NULL, "+"'"+ view_name + "'" + ");"
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
            
def read_database():
    try:
    # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='localhost',          # 主機名稱
            database='bbb', # 資料庫名稱
            user='root',        # 帳號
            password='1234')  # 密碼

        if connection.is_connected():
            sql = "SELECT * FROM `location`"
            cursor = connection.cursor()
            cursor.execute(sql)
            for (view_id,picture,view_name) in cursor:
                print("view_id: %d" % view_id)
                print("view_name: %s" % view_name)

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


if __name__ == '__main__':
    update_data("taipei")
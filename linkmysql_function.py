# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 11:25:11 2020

@author: Asus
update at 109.11.09
     time:1150
"""
import mysql.connector
from mysql.connector import Error

def link_database(): 
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
                print("view_id: %d" % view_id)
                view_ids.append(view_id)
            view_id = max(view_ids) + 1
            view_name = "小豐年公園"
            #INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES ('16', NULL, '復興崗');
            sql = "INSERT INTO `location` (`view_id`, `picture`, `view_name`) VALUES (" + "'" + str(view_id) + "'" + ", NULL, "+"'"+ view_name + "'" + ");"
            print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
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
    link_database()
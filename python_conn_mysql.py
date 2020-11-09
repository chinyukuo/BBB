import mysql.connector
from mysql.connector import Error

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


        view_id = 30
        view_name = "豐年公園"
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
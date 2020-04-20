
#coding=utf-8
import MySQLdb

conn = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    passwd = '@3X.M&',
    db ='websinfo_travelfun')

cur = conn.cursor()
#建立資料表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")
#插入一條資料
cur.execute("insert into student values('2','Tom','3 year 2 class','9')")
#修改查詢條件的資料
#cur.execute("update student set class='3 year 1 class' where name = 'Tom'")
#刪除查詢條件的資料
#cur.execute("delete from student where age='9'")
cur.close()
conn.commit()
conn.close()
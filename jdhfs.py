import mysql.connector

db = mysql.connector.connect(
    user ='root', 
    password= 'subham123', 
    host = '127.0.0.1',
    port='3306',
    auth_plugin='mysql_native_password', 
    database='db1'
)





mycursor = db.cursor()
number = 24
mycursor.execute(f"select * from KeyValue where `key` = {number}")


result = mycursor.fetchall()
print(result)
print(type(result))
print(result.__len__())         #signifies the length of the list

print(f"key : {result[0][0]}")
print(f"value : {result[0][1]}")


for row in result:
    print(f"key : {row[0]}")
    print(f"value : {row[1]}")

# number = 24
# mycursor.execute(f"INSERT INTO KeyValue (`Key`, value) VALUES ({number}, 'dhdhdfdfh')")
# db.commit()

number = 24
mycursor.execute(f"DELETE FROM KeyValue WHERE `key` = {number}")
db.commit()


mycursor.close()
db.close()

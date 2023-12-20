# import mysql.connector

# db = mysql.connector.connect(
#     user ='root', 
#     password= 'subham123', 
#     host = '127.0.0.1',
#     port='3306',
#     auth_plugin='mysql_native_password', 
#     database='db1'
# )





# mycursor = db.cursor()
# number = 24
# mycursor.execute(f"select * from KeyValue where `key` = {number}")


# result = mycursor.fetchall()
# print(result)
# print(type(result))
# print(result.__len__())         #signifies the length of the list

# print(f"key : {result[0][0]}")
# print(f"value : {result[0][1]}")


# for row in result:
#     print(f"key : {row[0]}")
#     print(f"value : {row[1]}")

# # number = 24
# # mycursor.execute(f"INSERT INTO KeyValue (`Key`, value) VALUES ({number}, 'dhdhdfdfh')")
# # db.commit()

# number = 24
# mycursor.execute(f"DELETE FROM KeyValue WHERE `key` = {number}")
# db.commit()


# mycursor.close()
# db.close()



import redis
import time

r = redis.Redis(host='127.0.0.1', port=6379)
# if r:
#     print("OK")
# else:
#     print("Oh NO!!")


r.set("France","Paris")
r.set("Germany","Berlin")

france_capital = r.get("France")
germany_capital = r.get("India")

#The output of redis is always in Byte format..
print(france_capital)       
print(germany_capital)

r.mset({"India":"Delhi","Australia":"Canberra","France":"sdjkfjsd"})

print(r.get("France"))
print(r.get("India"))

#Inputs are case sensitive..
if(r.exists("INdia")):
    print(r.get("India"))
else:
    print("Nopes!!")



r.psetex("Sri Lanka",1000,"Colombo")

print(r.get("Sri Lanka"))

time.sleep(2)


print(r.get("Sri Lanka"))


#How we are going to implement in our system..
key = 123
value = "dnmfbjhdgfds"

r.set(key,value)

if r.exists(key):
    print(r.get(key))
else:
    print(f"{key} does not exists..")

r.delete(key)
print(r.get(key))
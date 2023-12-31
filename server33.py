import mysql.connector
import socket
import threading
import redis

# https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported

# Select Host,User,plugin from mysql.user; type this in mysql terminal & get the plugin for mysql root user

db = mysql.connector.connect(
    user ='root', 
    password= 'subham123', 
    host = '127.0.0.1',
    port='3306',
    auth_plugin='mysql_native_password', 
    database='db3'
)

mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE db1")

#Create an Instance of redis..
r = redis.Redis(host='127.0.0.1', port=6379)

IP = '127.0.0.1'
PORT = 19367
FORMAT = "utf-8"

server_address = (IP,PORT)


print(f"Server is starting...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server listening on", server_address)

def handle_client(client_conn, client_addr):
    print(f"Client from {client_addr} has connected..")
    try:
        while True:
            msg = client_conn.recv(1024).decode(FORMAT)         #msg will store the data send by the client in a f-string format.

            print(f"Message from client {client_addr} is {msg}.")
            
            parts = msg.split(',')

            choice = int(parts[0])
            key = int(parts[1])
            value = parts[2] if len(parts) > 2 else None

            if choice == 1:
                #It is a GET Request..
                #   First check the redis if it present or not..
                #   If present then return it, else check in the Database..

                #1. If the Data is already in the cache, then send it from there..
                if r.exists(key):

                    response_key = key
                    response_value = r.get(key)
                    response = f"OK,{response_key},{response_value}"
                    client_conn.send(response.encode(FORMAT))

                #2. If not in cache..
                else:   
                    mycursor.execute(f"select * from KeyValue where `key` = {key}")
                    result = mycursor.fetchall()

                    if result.__len__() == 0:   #Nothing Found..in database.. then the value is totally absent..
                        response =  f"NOT FOUND,{key},xxxx"                           
                        client_conn.send(response.encode(FORMAT))
                    else:                       #Data Found..in database but not in cache..then update the cache..
                        response_key = result[0][0]
                        response_value = result[0][1]
                        response = f"OK,{response_key},{response_value}"
                        r.set(response_key,response_value)      #

                        client_conn.send(response.encode(FORMAT))

            elif choice == 2:
                #It is a POST Request..

                #Data found in the cache..
                if r.exists(key):
                    response = "NA"
                    client_conn.send(response.encode(FORMAT))

                #Data Not found in cache..
                else:
                    #1. Check in the database if it exists or not?                
                    mycursor.execute(f"select * from KeyValue where `key` = {key}")
                    result = mycursor.fetchall()

                    if result.__len__() == 0:                   #Nothing Found in DB & Cache..Then push the value into the Table..
                        
                        insert_query = "INSERT INTO KeyValue (`Key`, value) VALUES (%s, %s)"
                        values = (key, value)
                        mycursor.execute(insert_query, values)
                        db.commit()

                        r.set(key,value)                        #Update the cache along with the database..

                        response = "OK"
                        client_conn.send(response.encode(FORMAT))
                    else:                                       #Data found in the DB table but not in Cache..
                        response = "NA"
                        client_conn.send(response.encode(FORMAT))
            
            elif choice == 3:
                # It is a PUT Request

                # Find the Key in the database, if it is present in the DB then update it in the Cache and the DB..

                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:       #Not found in the Database..
                    response = "NOT FOUND"
                    client_conn.send(response.encode(FORMAT))               
                else:                           #Data present in the Database..
                    response = "OK"
                    client_conn.send(response.encode(FORMAT))

                    #Get the updated information to change in the database..

                    request = client_conn.recv(1024).decode(FORMAT)     
                    key_to_update, new_value = request.split(',')
                    key_to_update_as_int = int(key_to_update)

                    update_query = "UPDATE KeyValue SET value = %s WHERE `key` = %s"
                    values = (new_value, key_to_update_as_int)
                    mycursor.execute(update_query, values)
                    db.commit()

                    #Update in the cache..
                    r.set(key_to_update_as_int,new_value)

                    response = "OK"
                    client_conn.send(response.encode(FORMAT))            

            elif choice == 4:
                #It is a DELETE Request..

                #1. If data found in cache.. then remove it from the cache..
                if r.exists(key):
                    r.delete(key)       #Invalidate it in cache.     

                #2. Check if it is present in the database or not?
                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:               #Nothing Found in  DB..Throw error..
                    response = "NOT FOUND"
                    client_conn.send(response.encode(FORMAT))
                else:                                   #Data found in DB..

                    delete_query = "DELETE FROM KeyValue WHERE `key` = %s"
                    mycursor.execute(delete_query, (key,))
                    db.commit()                    

                    response = "OK"
                    client_conn.send(response.encode(FORMAT))
            
            else:
               #A wrong Request..Code would never reach here...
               print(f"Terminating {client_addr} connection...")
               break 
            
    except Exception as e:
        print(f"Error {e} has occured.")

    finally:        
        print("Terminated..")
        client_conn.close()



while True:
    conn, addr = server_socket.accept()                                     #A client came and connected to the server..
    thread = threading.Thread(target=handle_client, args= (conn,addr))
    thread.start()


mycursor.close()
db.close()

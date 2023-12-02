import mysql.connector
import socket
import threading

# https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported

# Select Host,User,plugin from mysql.user; type this in mysql terminal & get the plugin for mysql root user

db = mysql.connector.connect(
    user ='root', 
    password= 'subham123', 
    host = '127.0.0.1',
    port='3306',
    auth_plugin='mysql_native_password', 
    database='db1'
)

mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE db1")

IP = '127.0.0.1'
PORT = 19345
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

            print(f"Message from client is {msg}.")
            
            parts = msg.split(',')

            choice = int(parts[0])
            key = int(parts[1])
            value = parts[2] if len(parts) > 2 else None

            if choice == 1:
                #It is a GET Request..
                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:   #Nothing Found..
                    response =  f"xxxx,{key},xxxx"                           
                    client_conn.send(response.encode(FORMAT))
                else:                       #Data Found..
                    response_key = result[0][0]
                    response_value = result[0][1]
                    response = f"OK,{response_key},{response_value}"

                    client_conn.send(response.encode(FORMAT))

            elif choice == 2:
                #It is a POST Request..
                #1. First do a lookup and check if the key already present or not?
                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:                   #Nothing Found..Then push the value into the Tables..
                    mycursor.execute(f"INSERT INTO KeyValue (`Key`, value) VALUES ({key}, {value})")
                    db.commit()
                    response = "OK"
                    client_conn.send(response.encode(FORMAT))
                else:
                    response = "NA"
                    client_conn.send(response.encode(FORMAT))
            
            elif choice == 3:
                #It is a PUT Request..
                #1. First do a lookup and check if the key already present or not?
                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:               #Nothing Found..Throw error..
                    response = "NOT FOUND"
                    client_conn.send(response.encode(FORMAT))
                else:
                    response = "OK"
                    client_conn.send(response.encode(FORMAT))
                
                    request = client_conn.recv(1024).decode(FORMAT)         #Get the updated information to change in the database..
                
                    key_to_update,new_value = map(int, request.split(','))

                    mycursor.execute(f"UPDATE KeyValue SET value = '{new_value}' WHERE `key` = {key_to_update}")
                    db.commit()

                    response = "OK"
                    client_conn.send(response.encode(FORMAT))
            

            elif choice == 4:
                #It is a DELETE Request..
                #1. First do a lookup and check if the key already present or not?
                mycursor.execute(f"select * from KeyValue where `key` = {key}")
                result = mycursor.fetchall()

                if result.__len__() == 0:               #Nothing Found..Throw error..
                    response = "NOT FOUND"
                    client_conn.send(response.encode(FORMAT))
                else:
                    mycursor.execute(f"DELETE FROM KeyValue WHERE `key` = {key}")
                    db.commit()

                    response = "OK"
                    client_conn.send(response.encode(FORMAT))
            
            else:
               #A wrong Request..Code would never reach here...
               break 
            
    except Exception as e:
        print(f"Error {e} has occured.")

    finally:        
        print("Connection terminated by the client.")
        client_conn.close()



while True:
    conn, addr = server_socket.accept()                                     #A client came and connected to the server..
    thread = threading.Thread(target=handle_client, args= (conn,addr))
    thread.start()


mycursor.close()
db.close()
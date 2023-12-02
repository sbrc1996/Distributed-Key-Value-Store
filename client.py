import socket

#Server Details.
IP = '127.0.0.1'
LOAD_PORT = 19345
FORMAT = "utf-8"



#Creating the Client Socket & Connecting to the Server.

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)    		
client.connect((IP,LOAD_PORT)) 

try:
    while True:
        print("Select the Type of Request.")
        print("1.GET 2.POST 3.PUT 4.DELETE 5.Exit")
        choice = input(int("Enter your choice: "))

        if choice == 1:
            #implement GET Request.
            key = input(int("Enter the key to be RETRIEVED: "))
            data_to_send = f"{choice},{key}"   

            client.send(data_to_send.encode(FORMAT))

            response = client.recv(1024).decode(FORMAT)     #  Server or cache returns key value from the DB in 
                                                            # "OK",{key},{value} if present, else returns "NOT FOUND",{key},{"NULL"} 
            msg,key,value = map(int, response.split(','))

            if msg == "OK":                                 #Key found in DB.
                print(f"key  {key} : value {value}  pair")
            else:                                           #Key not found in DB.
                print(f"key  {key} not found..")

        elif choice == 2:
            #implement POST Request.
            key = input(int("Enter the key: "))
            value = input("Enter the value: ")
            data_to_send = f"{choice},{key},{value}"

            client.send(data_to_send.encode(FORMAT))        

            response = client.recv(1024).decode(FORMAT)     #Server returns string "OK" or "ERROR"
            if response == "OK":
                print(f"{key}:{value} successfully entered in DB.")
            else:
                print(f"{key}:{value} not entered in DB error encountered as it already exists..")

        elif choice == 3:
            #implement PUT Request.
            key = input(int("Enter the key to be UPDATED: "))
            data_to_send = f"{choice},{key}"  

            client.send(data_to_send.encode(FORMAT))  

            msg = client.recv(1024).decode(FORMAT)     #  Server or cache returns key value from the DB in 
                                                            # "OK"  if present, else returns "NOT FOUND",{key},{"NULL"} 
            
            if msg == "OK":                                 #Key found in DB.
                print(f"key  {key} : value {value}  pair")
                newValue = input("Enter the updated value: ")
                data_to_send = f"{key},{newValue}"

                client.send(data_to_send.encode(FORMAT)) 

                response = client.recv(1024).decode(FORMAT)     #Server returns string "OK" or "ERROR"

                if response == "OK":
                    print(f"{key}:{newValue} successfully entered in DB.")
                else:
                    print(f"{key}:{value} not entered in DB error encountered.")
            else:                                           #Key not found in DB.
                print(f"key  {key} not found..")

        elif choice == 4:
            #implement DELETE Request.
            key = input(int("Enter the key to be DELETED: "))
            data_to_send = f"{choice},{key}"  
            client.send(data_to_send.encode(FORMAT)) 

            response = client.recv(1024).decode(FORMAT)     #  Server or cache returns key value from the DB in 
                                                            # "OK" if present, else returns "NOT FOUND" 
            
            if response == "OK":                            #Key found in DB.
                print(f"key  {key} was found and successfully Deleted..")                
            else:                                           #Key not found in DB.
                print(f"key  {key} not found..")

        else:
            print("Thank you for your time..")
            break

except Exception as e:
    print(f"Exception occured as {e}")

finally:
    print("Connection terminated by the client.")
    client.close()

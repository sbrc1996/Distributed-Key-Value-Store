import socket

#Server Details.
IP = '127.0.0.1'
LOAD_PORT1 = 19344
LOAD_PORT2 = 19354
LOAD_PORT3 = 19364
FORMAT = "utf-8"



#Creating the Client Socket & Connecting to the Server.

# client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)    	



# client.connect((IP,LOAD_PORT)) 


def service_discovery(key):
    if key >= 0 and key <= 100:
        return LOAD_PORT1
    elif key > 100 and key <= 300:
        return LOAD_PORT2
    elif key > 300 and key <= 500:
        return LOAD_PORT3
    else:
        return -1    #Default Port Number..

try:
    while True:

        #Creating the Client Socket & Connecting to the Server.

        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)   

        print("Select the Type of Request.")
        print("1.GET 2.POST 3.PUT 4.DELETE 5.Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            #implement GET Request.
            key = int(input("Enter the key to be RETRIEVED: "))

            # Get the load balancer to be connected based on the Key value entered..
            load_port_number = service_discovery(key)
            client.connect((IP,load_port_number)) 

            data_to_send = f"{choice},{key}"   

            client.send(data_to_send.encode(FORMAT))

            response = client.recv(1024).decode(FORMAT)     #  Server or cache returns key value from the DB in 
                                                            # "OK",{key},{value} if present, else returns "NOT FOUND",{key},{"NULL"} 
            msg,key,value = response.split(',')

            if msg == "OK":                                 #Key found in DB.
                print(f"key  {key} : value {value}  pair")
            else:                                           #Key not found in DB.
                print(f"key  {key} not found..")
            client.close()                                  # Close the connection after each request.

        elif choice == 2:
            #implement POST Request.
            key = int(input("Enter the key: "))
            value = input("Enter the value: ")

            # Get the load balancer to be connected based on the Key value entered..
            load_port_number = service_discovery(key)
            client.connect((IP,load_port_number))

            data_to_send = f"{choice},{key},{value}"

            client.send(data_to_send.encode(FORMAT))        

            response = client.recv(1024).decode(FORMAT)     #Server returns string "OK" or "ERROR"
            if response == "OK":
                print(f"{key}:{value} successfully entered in DB.")
            else:
                print(f"{key}:{value} not entered in DB error encountered as it already exists..")
            client.close()                                  # Close the connection after each request.

        elif choice == 3:
            #implement PUT Request.
            key = int(input("Enter the key to be UPDATED: "))

            # Get the load balancer to be connected based on the Key value entered..
            load_port_number = service_discovery(key)
            client.connect((IP,load_port_number))

            data_to_send = f"{choice},{key}"

            client.send(data_to_send.encode(FORMAT))            

            msg = client.recv(1024).decode(FORMAT)          #  Server or cache returns key value from the DB in 
                                                            # "OK"  if present, else returns "NOT FOUND",{key},{"NULL"} 
            if msg == "OK":
                print(f"key {key} found in DB.")         
                newValue = input("Enter the updated value: ")
                data_to_send = f"{key},{newValue}"

                client.send(data_to_send.encode(FORMAT))

                response = client.recv(1024).decode(FORMAT)
                if response == "OK":
                    print(f"{key}:{newValue} successfully updated in DB.")
                else:
                    print(f"Error updating {key} in DB.")
            else:
                print(f"key {key} not found in DB.")
            client.close()                                  # Close the connection after each request.


        elif choice == 4:
            #implement DELETE Request.
            key = int(input("Enter the key to be DELETED: "))

            # Get the load balancer to be connected based on the Key value entered..
            load_port_number = service_discovery(key)
            client.connect((IP,load_port_number))

            data_to_send = f"{choice},{key}"  
            client.send(data_to_send.encode(FORMAT)) 

            response = client.recv(1024).decode(FORMAT)     #  Server or cache returns key value from the DB in 
                                                            # "OK" if present, else returns "NOT FOUND" 
            
            if response == "OK":                            #Key found in DB.
                print(f"key  {key} was found and successfully Deleted..")                
            else:                                           #Key not found in DB.
                print(f"key  {key} not found..")
            client.close()                                  # Close the connection after each request.

        else:   
            #Terminate the connection..
            print("Thank you for your time..")
            key = -1
            data_to_send = f"{choice},{key}"
            client.send(data_to_send.encode(FORMAT)) 

            break

except Exception as e:
    print(f"Exception occured as {e}")

finally:
    print("Connection terminated by the client.")
    client.close()

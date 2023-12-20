import socket
import threading

# The structure of the code is that: 3 server, multiple clients and a load balancer will be present.
# The load balancer is a server which will take requests from the clients and then redirect them to the servers in RR fashion.

IP = '127.0.0.1'
LOAD_PORT = 19364

SERVER1_PORT = 19365
SERVER2_PORT = 19366
SERVER3_PORT = 19367

FORMAT = "utf-8"

server_address = [(IP,SERVER1_PORT),(IP,SERVER2_PORT),(IP,SERVER3_PORT)]
current_server = 0

#Start the load balancer..
print("Load Balancer is starting..")
load_balancer = socket.socket(type=socket.SOCK_STREAM,family=socket.AF_INET)
load_balancer.bind((IP,LOAD_PORT))
load_balancer.listen(5)
print(f"Load Balancer is listening @ {IP}:{LOAD_PORT}")


#The main crux of the load balancer..
def load_handle_client(client_sock,client_addr):
    global current_server  

    while True:
        print(f"Received Connection from {client_addr}..")
        print(f"Finding a Server Now...")

        #Applying the Round-Robin Algorithm..
        server_to_redirect = server_address[current_server]
        current_server = (current_server+1)%len(server_address)

        print(f"Server: {server_to_redirect} selected for client {client_addr}")

        #Now redirect the client to the selected server..
        try:
            # Connect to the selected server
            server_sock = socket.socket(type=socket.SOCK_STREAM,family=socket.AF_INET)
            server_sock.connect(server_to_redirect)

            # Forward the client's connection to the server
            threading.Thread(target=forward_data, args=(client_sock, server_sock)).start()
            threading.Thread(target=forward_data, args=(server_sock, client_sock)).start()
            
        except Exception as e:
            print(f"Error {e} occured connection to server. Trying the next server..")
            continue
        
        # Exit the loop and close the client connection
        break


# Helper function to forward data between sockets
def forward_data(source, destination):
    while True:
        data = source.recv(1024)
        if not data:
            break
        destination.send(data)
    source.close()
    destination.close()


#Handling Multiple clients using Threading
while True:
    conn, addr = load_balancer.accept()                                         #A new client came and connected to the load balancer..
    thread = threading.Thread(target=load_handle_client, args= (conn,addr))     #Create a new thread of the LB to handle the client and route it to a server using RR.
    thread.start()
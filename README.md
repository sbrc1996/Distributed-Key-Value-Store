**DISTRIBUTED KEY-VALUE STORE**

A Python-based CLI Program

SYSTEM DIAGRAM:
![image](https://github.com/sbrc1996/Distributed-Key-Value-Store/assets/36306295/b3c4e591-a28a-47f8-9113-9f344c9f34b1)

**DESCRIPTION**
Here we have n clients connecting to the Service Discovery that assigns a correct load balancer to the client. The load balancers are decided on the basis of the value of the key entered by the user. 
Load Balancer 1 handles the key from 0 to 100 while Load Balancer 2 handles from 101 to 300 and Load Balancer 3 handles 301 to 500. 
Each of these load balancers is connected to an array of servers that handle the business logic.
Each of the server are also connected to the in-memory data store a cache (REDIS) & a database for the persistent data storage.


**ALGORITHMS USED**

The Load Balancer has used:
    1. Round Robin
    2. Least Number of Connections

The Caching uses:
    1. Read Through for Read Operations
    2. Write Through for Write Operations

The Service Discovery is client-side service discovery.

**HOW TO EXECUTE?**

First start the Redis server using the command: 
    1. `sudo systemctl start redis-server.service`
    2. start the load balancers individually followed by the servers
        `python3 loadbalancer1.py` or `python3 server12.py`
    3. Enter values through the clients and interact with the program.


**FUTURE SCOPE:**
Implement RATE LIMITING to provide a check on the number of requests made per client.

import socket 

# Setting host and port

target_host = "127.0.0.1" # This is the loopback address, which we utilise in the tcp_server.py script
target_port = 6667 # Standard port for http

# Creating a socket
# AF_INET specifies that we are using IPv4 and SOCK_STREAM that we use UDP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to host and port

client.connect((target_host, target_port))

# Sending data 

client.send(b"Test client-server")

# Receiving data

response = client.recv(4096) # Receiving data with a maximum buffer size of 4096

print(response.decode())
client.close()
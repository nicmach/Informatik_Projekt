import socket

target_host = "127.0.0.1" # This is the loopback address of the computer
target_port = 6666 # Some arbitrary port nubmer


# Instead of using SOCK_STREAM as before we now utilise SOCK_DGRAM.
# In general the STREAM is used for TCP connections, which use SYN and ACK messages,
# while DGRAM is used for UDP connection, which do no implement the same checks as TCP.
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# As UDP is connectionless there is no need for establishing a connection before sending data.
client.sendto(b"Test Data", (target_host, target_port))

# Similar to the TCP client we retrieve the data
data, addr = client.recvfrom(4096)

client.head()
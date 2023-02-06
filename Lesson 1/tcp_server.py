import socket
import threading

IP = '127.0.0.1'
PORT = 6667

def main():

    # Creating the socket for the TCP server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Binding the server to the given IP and PORT
    server.bind((IP, PORT))

    # Listening for icoming connections with a total of five connection at a time.
    server.listen(5)

    print(f'*** Listening on {IP}:{PORT}')

    while True:

        # Get the identifying data about a device that connects to the server
        client, address = server.accept()
        print(f'*** Accepted connection from {address[0]}:{address[1]}')

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()
    
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'*** Received: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == '__main__':
    main()
    
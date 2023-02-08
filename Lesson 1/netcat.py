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

    
import socket
import sys

# Python threading allows you to have different parts of your program run concurrently and can simplify your design. 
import threading

# The following is a hex filter which contains ASCII printable characters if they exist/ can be represented by the system.
# Otherwise it will return a dot. If we for example would use 25 we would not get a valid representation (this can easily
# checked by typing chr(25) within python, which will return '\x19'). On the other hand 90 will return the character Z. 
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):

    # If the passed string (src) is a byte string we decode it.
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    # We take a dump of the passed string (the length is set to a default value of 16 characters).           
    for i in range(0, len(src), length):

        # We read the part of the string we are currently at into the word variable.
        word = str(src[i:i+length])

        # We use the translate function and our HEX_FILTER to translate the extract 
        # of the string ("word") into a printable string. The translate() method returns a 
        # string where some specified characters are replaced with the character described 
        # in a dictionary, or in a mapping table.
        printable = word.translate(HEX_FILTER)

        # This code takes a string, "word", and converts it into a hexadecimal representation. 
        # It does this by looping through each character in the string, and using the ord() 
        # function to get the Unicode code point of each character. The code then uses the 
        # format string f'{ord(c):02X}' to format the code point as a two-digit hexadecimal number, 
        # and the join() function to join all the hexadecimal numbers together into one string separated by spaces.
        hexa = ' '.join([f'{ord(c):02X}' for c in word])

        # The following is used to format a string in Python. First we set a variable 
        # called "hexwidth", which is equal to "length" multiplied by 3. The second
        # line appends a formatted string to the list "results". The formatted string consists 
        # of four digits, followed by a hexadecimal representation of the string with a length equal 
        # to the value of hexwidth, followed by a printable representation of the string. The four digits
        # at the beginning is the index at which we currently are (for "length" = 16 this will always increse
        # by 1 in the second column etc., because 1 in hex equals 16 in decimal).
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    
    if show:
        for line in results:
            print(line)

    else:
        return results

    # All together the above code returns data in the following format:
    #
    # 0000 49 66 20 77 65 20 77 65 72 65 20 74 6F 20 74 61  If we were to ta
    # 0010 6B 65 20 74 68 69 73 20 73 74 72 69 6E 67 20 66  ke this string f
    # 0020 6F 72 20 65 78 61 6D 70 6C 65 20 74 68 65 20 66  or example the f
    # 0030 75 6E 63 74 69 6F 6E 20 77 6F 75 6C 64 20 72 65  unction would re
    # 0040 74 75 72 6E 2E                                   turn.
    #
    # This might remind some of tools like wireshark, which utilize a similiar
    # formatting. We also, similiar to wireshark, make use of this format to 
    # make the communication going through the proxy more readable/ usable. 


# We use this function for receiving data at both ends of the proxy.
def receive_from(connection):

    
    # We pass the socket object to the function and, after creating a buffer,
    # we set the timeout of the socket to 5 seconds. 
    # 
    # When using sockets in Python, settimeout is useful to prevent the program from being 
    # blocked if the socket fails to receive a response from the server. By setting a timeout, 
    # the program will be able to detect that the server is not responding and can take appropriate action. 
    # Additionally, setting a timeout will help to ensure that the program does not hang if a connection is 
    # not established or the connection is lost. Depending on the networks stability and the distance
    # over which data is send it might be make sense to inrease the five second timeout to a higher amount.

    buffer = b''
    connection.settimeout(5)

    # We then receive data, until no data is send anymore.
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data 
    except Exception as e:
        pass

    # The buffer, which contains the received data is then returned.
    return buffer

def request_handler(buffer):
    # In this function we could perform modifications of the request packets.
    return buffer

def response_handler(buffer):
    # In this function we could perform modifications of the response packets.
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # First we create a connection to the remote host.
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # We check wheter we need to first initiate a connection to the remote side.
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    # We pass the buffer to the response handler (for manipulation etc.).
    # We then, if the buffer exists, send it to the local client.
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print('[<--] Sending %d bytes to localhost.' % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:

        # We read the data from the local client.
        local_buffer = receive_from(client_socket)
        if len(local_buffer):

            # We process the data.
            line = '[-->] Received %d bytes from localhost.' % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            
            # We send the data to the remote host.
            remote_socket.send(local_buffer)
            print('[<--] Sent to remote.') 

        # We read the data from the remote client.
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):

            # We process the data.
            print('[-->] Received %d bytes from remote.' % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            # We send the data to the local client.
            client_socket.send(remote_buffer)
            print('[<--] Sent to localhost.')

        # If no data is received anymore...
        if not len(local_buffer) and not len(remote_buffer):
            
            # ...we close both sockets.
            client_socket.close()
            remote_socket.close()
            print('[!] No more incoming data. Connection terminated.')
            break
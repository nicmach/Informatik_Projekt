import socket
import sys

# Python threading allows you to have different parts of your program run concurrently and can simplify your design. 
import threading

# The following is a hex filter which contains ASCII printable characters if they exist/ can be represented by the system.
# Otherwise it will return a dot. If we for example would use 25 we would not get a valid representation (this can easily
# checked by typing chr(25) within python, which will return '\x19'). On the other hand 90 will return the character Z. 
HEX_FILTER = ''.join([len(repr(chr(i)) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length * 3
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    
    if show:
        for line in results:
            print(line)

    else:
        return results
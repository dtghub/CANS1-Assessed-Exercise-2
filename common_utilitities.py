import os
import sys
import socket




#function to log to screen




# send_file(socket, filename): Opens the file with the given filename and sends its data over the network through the provided socket.

# recv_file(socket, filename): Creates the file with the given filename and stores into it data received from the provided socket.

# send_listing(socket): Generates and sends the directory listing from the server to the client via the provided socket.

# recv_listing(socket): Receives the listing from the server via the provided socket and prints it on screen.






#function to report error in command line and to output a usage text


# xor all the characters in a string to geneate a simple checksum
def calculateChecksumString(stringToCheck):
    xorChecksum = 0
    for character in stringToCheck:
        xorChecksum = xorChecksum ^ ord(character)
    return xorChecksum

    

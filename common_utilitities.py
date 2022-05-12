import os
import sys
import socket

from importlib_metadata import files




def send_file(sock, filename):
    serverStatus = ""
    with open(filename, 'rb') as file:
        bytesToSend = file.read(1024)
        sock.send(bytesToSend)
        while len(bytesToSend) != 0:
            bytesToSend = file.read(1024)
            sock.send(bytesToSend)

    return serverStatus
            
    
def recv_file(sock, filename, filesize):
    serverStatus = ""
    f = open(filename, 'xb')
    if filesize == 0:
        displayMessage("Source file is 0 bytes in size. File '" + filename + "' has been created, with size 0 bytes.")
    totalRecv = 0
    while totalRecv < filesize:
        data = sock.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print("\r{0:.2f}".format((totalRecv/float(filesize)) * 100) + "% done: " + str(totalRecv) + " bytes received", end = '')
    print()

    return serverStatus



def send_listing(sock):
    cwd = os.getcwd()
    listOfFiles = os.listdir(cwd)
    serverStatus = ""
    # Send directory listing

    # Use '/' as the join character to avoid the need to escape characters, as it is not allowed as a filename character at system level in windows *nix or mac filesystems

    joinedStringOfFiles = '/'.join(listOfFiles)
    # xorChecksum = common_utilitities.calculateChecksumString(joinedStringOfFiles)
    xorChecksum = "45" # teporary dummy value
    lengthOfStringToSend = len(joinedStringOfFiles)
    header = "OK/" + str(lengthOfStringToSend) + '/' + xorChecksum
    sock.send(header.encode('utf-8'))
    userResponse = sock.recv(1024).decode('utf-8')
    if userResponse.split('/')[0] == 'OK':
        bytesSent = 0
        while bytesSent < lengthOfStringToSend:
            if (lengthOfStringToSend - bytesSent) < 1024:
                sock.send(joinedStringOfFiles[bytesSent:lengthOfStringToSend].encode('utf-8'))
                bytesSent = lengthOfStringToSend
            else:
                sock.send(joinedStringOfFiles[bytesSent + 1:bytesSent + 1024].encode('utf-8'))
                bytesSent += 1024
    else:
        serverStatus = "Client did not return 'OK' status"

    return serverStatus




def recv_listing(sock):
    sock.send("LIST".encode('utf-8'))
    listingString = ""
    data = sock.recv(1024).decode('utf-8')
    if data.split('/')[0] == "OK":
        filesize = int(data.split('/')[1])
        # checksum = data.split('/')[2]
        sock.send('OK/'.encode('utf-8'))
        data = sock.recv(1024).decode('utf-8')
        listingString += data
        while len(listingString) < filesize:
            data = sock.recv(1024).decode('utf-8')
            listingString += data
        displayMessage("\nLIST;")
        displayMessage('\n'.join(listingString.split('/')))
    else:
        displayError("Server did not return 'OK' status")



def displayMessage(msg):
    print(msg)

def displayError(msg):
    msg = "[ERROR] " + msg
    displayMessage(msg)

def displatErrorAndExit(msg):
    displayError(msg)
    sys.exit()



# xor all the characters in a string to geneate a simple checksum
def calculateChecksumString(stringToCheck):
    xorChecksum = 0
    for character in stringToCheck:
        xorChecksum = xorChecksum ^ ord(character)
    return xorChecksum

    

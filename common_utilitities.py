import os
import sys
import socket




def send_file(sock, filename):
    successStatus = ""
    with open(filename, 'rb') as file:
        bytesToSend = file.read(1024)
        sock.send(bytesToSend)
        while len(bytesToSend) != 0:
            bytesToSend = file.read(1024)
            sock.send(bytesToSend)

    return successStatus
            
    
def recv_file(sock, filename, filesize):
    successStatus = ""
    file = open(filename, 'xb')
    if filesize == 0:
        displayMessage("Source file is 0 bytes in size. File '" + filename + "' has been created, with size 0 bytes.")
    totalRecv = 0
    consecutiveEmptyPacketCount = 0
    while (totalRecv < filesize) and (consecutiveEmptyPacketCount < 5):
        data = sock.recv(1024)
        totalRecv += len(data)
        if totalRecv > 0:
            consecutiveEmptyPacketCount = 0
        else:
            consecutiveEmptyPacketCount += 1
        file.write(data)
        print("\r{0:.2f}".format((totalRecv/float(filesize)) * 100) + "% done: " + str(totalRecv) + " bytes received", end = '')
    print()
    if totalRecv != filesize:
        successStatus = "Expected " + filesize + " bytes, but transferred " + totalRecv + " bytes"
        # delete the file
    # close the file

    return successStatus



def send_listing(sock):
    cwd = os.getcwd()
    listOfFiles = os.listdir(cwd)
    successStatus = ""
    # Send directory listing

    # Use '/' as the join character to avoid the need to escape characters. '/' was selected as it is not allowed as a filename character at system level in windows *nix or mac filesystems

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
        successStatus = "Client did not return 'OK' status"

    return successStatus




def recv_listing(sock):
    successStatus = ""
    sock.send("LIST".encode('utf-8'))
    listingString = ""
    data = sock.recv(1024).decode('utf-8')
    if data.split('/')[0] == "OK":
        filesize = int(data.split('/')[1])
        # checksum = data.split('/')[2]
        sock.send('OK/'.encode('utf-8'))
        data = sock.recv(1024).decode('utf-8')
        listingString += data
        consecutiveEmptyPacketCount = 0
        while len(listingString) < filesize and (consecutiveEmptyPacketCount < 5):
            data = sock.recv(1024).decode('utf-8')
            listingString += data
        if len(listingString) != filesize:
            successStatus = "Expected " + filesize + " bytes, but transferred " + len(listingString) + " bytes"
        else:
            displayMessage("\nLIST;")
            displayMessage('\n'.join(listingString.split('/')))
    else:
        displayError("Server did not return 'OK' status")
    return successStatus


def displayMessage(msg):
    print(msg)


def displayError(msg):
    msg = "[ERROR] " + msg
    displayMessage(msg)

def displaySuccess(msg):
    msg = "[SUCCESS] " + msg
    displayMessage(msg)

def displayFailure(msg):
    msg = "[FAILURE] " + msg
    displayMessage(msg)


def displayErrorAndExit(msg):
    displayError(msg)
    sys.exit()


def getArgs():
    return sys.argv




# xor all the bytes in a stream to geneate a simple checksum
def calculateChecksumString(streamToCheck):
    xorChecksum = 0
    for byte in streamToCheck:
        xorChecksum = xorChecksum ^ byte
    return xorChecksum

    

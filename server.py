import os
import sys
import socket
import common_utilitities






def putCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""
    filename = serverRequest.split('/')[1]
    fileSize = int(serverRequest.split('/')[2])

    print("Your arg is put.\n")
    print(serverRequest)
    sock.send("OK".encode('utf-8'))
    f = open('new_' + filename, 'wb')
    data = sock.recv(1024)
    totalRecv = len(data)

    f.write(data)
    while totalRecv < fileSize:
        data = sock.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print("{0:.2f}".format((totalRecv/float(fileSize)) * 100) + "% Done: " + str(len(data)) + " bytes received")
    print("Download Complete")

    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""
    print("get command")
    print(commandLineArguments)
    print(serverRequest)
    print(os.getcwd())
    print(os.path.isfile('test.txt'))

    filename = serverRequest.split('/')[1]
    print(filename)
    print(os.path.isfile(serverRequest[1]))
    if os.path.isfile(filename):
        print("Sending EXISTS")
        messageToSend = "EXISTS" + str(os.path.getsize(filename))
        sock.send(messageToSend.encode('utf-8'))
        userResponse = sock.recv(1024).decode('utf-8')
        print("Response: " + userResponse)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while len(bytesToSend) != 0:
                    bytesToSend = f.read(1024)
                    print(len(bytesToSend))
                    sock.send(bytesToSend)
    else:
        sock.send("ERR".encode('utf-8'))
    

    print("About to return from getCommand()")
    return isArgumentsCorrect, errorText



def listCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""

    # Get directory listing
    cwd = os.getcwd()
    listOfFiles = os.listdir(cwd)
    print(listOfFiles)


    # Send directory listing

    # Use '/' as the join character to avoid the need to escape characters, as it is not allowed as a filename character at system level in windows *nix or mac filesystems

    joinedStringOfFiles = '/'.join(listOfFiles)
    # xorChecksum = common_utilitities.calculateChecksumString(joinedStringOfFiles)
    xorChecksum = "45" # teporary dummy value

    print(joinedStringOfFiles)
    # print(xorChecksum)


    # joinedStringOfFiles += chr(xorChecksum)

    lengthOfStringToSend = len(joinedStringOfFiles)

    # cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # cli_sock.connect(("", int(commandLineArguments[1])))
    # cli_sock.sendall(struct.pack('!I', lengthOfStringToSend))
    # cli_sock.sendall(joinedStringOfFiles.encode('utf-8'))
    # cli_sock.close()

    header = "OK/" + str(lengthOfStringToSend) + '/' + xorChecksum
    sock.send(header.encode('utf-8'))
    userResponse = sock.recv(1024).decode('utf-8')
    if userResponse[:2] == 'OK':
        bytesSent = 0
        while bytesSent < lengthOfStringToSend:
            if (lengthOfStringToSend - bytesSent) < 1024:
                sock.send(joinedStringOfFiles[bytesSent:lengthOfStringToSend].encode('utf-8'))
                bytesSent = lengthOfStringToSend
            else:
                sock.send(joinedStringOfFiles[bytesSent + 1:bytesSent + 1024].encode('utf-8'))
                bytesSent += 1024






    return isArgumentsCorrect, errorText





def dispatchCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = False
    errorText = ""
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    print("Point B")

    commandType = serverRequest.split("/")[0]

    print(commandType)

    if commandType in commandMappings:
        print("point C")
        isArgumentsCorrect, errorText = commandMappings[commandType](commandLineArguments, serverRequest, sock)
    else:
        errorText = "Command not recognised."


    return isArgumentsCorrect, errorText





def parseArgs(arguments):
    return sys.argv


def usage():
    return "Usage: server.py <port number>"



def displayArgumentsError(errorText):
    print("Error: " + errorText)
    print(usage())



def dispatchServer(commandLineArguments):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(("", int(commandLineArguments[1])))
    srv_sock.listen(5)
    while True:
        cli_sock, cli_addr = srv_sock.accept()
        request = cli_sock.recv(1024)
        serverRequest = request.decode('utf-8')
        print(str(cli_addr) + ": " + serverRequest)
        print(commandLineArguments)
        print("point A")
        isArgumentsCorrect, errorText = dispatchCommand(commandLineArguments, serverRequest, cli_sock)
        cli_sock.close()



def main():
    commandLineArguments = parseArgs(sys.argv)
    isArgumentsCorrect = False
    if len(commandLineArguments) == 2:
        isArgumentsCorrect, errorText = dispatchServer(commandLineArguments)
    else:
        errorText = "Incorrect number of arguments"
    if not isArgumentsCorrect:
        displayArgumentsError(errorText)



main()
from fileinput import filename
import os
import struct
import sys
import socket
import common_utilitities








def putCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = False
    errorText = ""


    if len(commandLineArguments) == 5:
        # host = commandLineArguments[1]
        # port = int(commandLineArguments[2])
        filename = serverRequest.split('/')[1]
        fileSize = serverRequest.split('/')[2]

        print("Your arg is put.\n")
        sock.send("ACKPUT")






    else:
        errorText = "Incorrect number of arguments."


    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = False
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
        sock.send("EXISTS" + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        print("Response: " + userResponse)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR")
    


    return isArgumentsCorrect, errorText



def listCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = False
    errorText = ""

    # Get directory listing
    cwd = os.getcwd()
    listOfFiles = os.listdir(cwd)
    print(listOfFiles)


    # Send directory listing

    # Use '/' as the join character to avoid the need to escape characters, as it is not allowed as a filename character at system level in windows *nix or mac filesystems

    joinedStringOfFiles = '/'.join(listOfFiles)
    xorChecksum = common_utilitities.calculateChecksumString(joinedStringOfFiles)

    print(joinedStringOfFiles)
    print(xorChecksum)


    # joinedStringOfFiles += chr(xorChecksum)

    lengthOfStringToSend = len(joinedStringOfFiles)

    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect(("", int(commandLineArguments[1])))
    cli_sock.sendall(struct.pack('!I', lengthOfStringToSend))
    cli_sock.sendall(joinedStringOfFiles.encode())
    cli_sock.close()


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
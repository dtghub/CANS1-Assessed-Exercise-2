import os
import struct
import sys
import socket
import common_utilitities








def putCommand(commandLineArguments):
    isArgumentsCorrect = False
    errorText = ""


    if len(commandLineArguments) == 5:


        print("Your arg is put.\n")

    else:
        errorText = "Incorrect number of arguments."


    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments):
    isArgumentsCorrect = False
    errorText = ""


    if len(commandLineArguments) == 5:


        print("get file?\n")

    else:
        errorText = "Incorrect number of arguments."


    return isArgumentsCorrect, errorText



def listCommand(commandLineArguments):
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





def dispatchCommand(commandLineArguments, requestCommand):
    isArgumentsCorrect = False
    errorText = ""
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    if requestCommand in commandMappings:
        isArgumentsCorrect, errorText = commandMappings[requestCommand](commandLineArguments)
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
        requestCommand = request.decode('utf-8')
        print(str(cli_addr) + ": " + requestCommand)
        cli_sock.close()
        print(commandLineArguments)
        print("point A")
        isArgumentsCorrect, errorText = dispatchCommand(commandLineArguments, requestCommand)



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
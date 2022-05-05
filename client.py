import os
import struct
import sys
import socket
import common_utilitities




def requestList(commandLineArguments):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((commandLineArguments[1], int(commandLineArguments[2])))
    cli_sock.sendall("LIST".encode('utf-8'))
    cli_sock.close()


    print(commandLineArguments)
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((commandLineArguments[1], int(commandLineArguments[2])))

    print(commandLineArguments[1])
    print("point B")

    rawLengthOfStringToReceive = recvall(cli_sock, 4)
    lengthOfStringToReceive = struct.unpack('!I', rawLengthOfStringToReceive)
    directoryStringFromServer = recvall(cli_sock, lengthOfStringToReceive).decode()
    cli_sock.close()


    print(directoryStringFromServer)

    xorChecksum = common_utilitities.calculateChecksumString(directoryStringFromServer)


    print("Checksum = " + xorChecksum)
    print("String received; " + directoryStringFromServer[0,-1])



def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf





def putFile(commandLineArguments):
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli_sock.connect((commandLineArguments[1], int(commandLineArguments[2])))
    cli_sock.sendall(commandLineArguments[3].encode())

    cli_sock.close()
    return True


























def parseArgs(arguments):
    print('#arguments: ' + str(len(sys.argv)))
    return sys.argv


def usage():
    return "Usage: client.py <hostname> <port> <put filename|get filename|list>"





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

    if len(commandLineArguments) == 4:

        requestList(commandLineArguments)
        print("here is your listing\n")

    else:
        errorText = "Too many arguments."


    return isArgumentsCorrect, errorText





def dispatchCommand(commandLineArguments):
    isArgumentsCorrect = False
    errorText = ""
    commandOption = commandLineArguments[3]
    commandMappings = {
        "get" : getCommand,
        "GET" : getCommand,
        "put" : putCommand,
        "PUT" : putCommand,
        "list" : listCommand,
        "LIST" : listCommand,
    }

    if commandOption in commandMappings:
        isArgumentsCorrect, errorText = commandMappings[commandOption](commandLineArguments)
    else:
        errorText = "Command not recognised."


    return isArgumentsCorrect, errorText






def displayArgumentsError(errorText):
    print("Error: " + errorText)
    print(usage())





def main():
    commandLineArguments = parseArgs(sys.argv)
    isArgumentsCorrect = False
    if len(commandLineArguments) >= 4:
        isArgumentsCorrect, errorText = dispatchCommand(commandLineArguments)
    else:
        errorText = "Not enough arguments"
    if not isArgumentsCorrect:
        displayArgumentsError(errorText)



main()
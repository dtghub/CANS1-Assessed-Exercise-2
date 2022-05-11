import os
import sys
import socket
import common_utilitities





def parseArgs(arguments):
    print('#arguments: ' + str(len(sys.argv)))
    return sys.argv


def usage():
    return "Usage: client.py <hostname> <port> <put filename|get filename|list>"




def putCommand(commandLineArguments):
    isArgumentsCorrect = True
    errorText = ""

    if len(commandLineArguments) == 5:
        filename = commandLineArguments[4]
        if os.path.isfile(filename):
            host = commandLineArguments[1]
            port = int(commandLineArguments[2])

            sock = socket.socket()
            sock.connect((host,port))
            fileSize = str(os.path.getsize(filename)) 
            messageToSend = "PUT" + '/' + filename + '/' + fileSize
            sock.send(messageToSend.encode('utf-8'))
            userResponse = sock.recv(1024).decode('utf-8')
            if userResponse[:2] == 'OK':
                common_utilitities.send_file(sock, filename)
            elif userResponse.split('/')[0] == "EXISTS":
                errorText = "Filename '" + filename + "' already exists on the server"
                isArgumentsCorrect = False
        else:
            errorText = "Filename not found"
            isArgumentsCorrect = False
    else:
        errorText = "Incorrect number of arguments."
        isArgumentsCorrect = False

    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments):
    isArgumentsCorrect = True
    errorText = ""



    if len(commandLineArguments) == 5:
        host = commandLineArguments[1]
        port = int(commandLineArguments[2])
        filename = commandLineArguments[4]

        if not os.path.isfile(filename):
            sock = socket.socket()
            sock.connect((host,port))

            messageToSend = "GET"+"/"+filename
            sock.send(messageToSend.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                sock.send('OK'.encode('utf-8'))
                common_utilitities.recv_file(sock, filename, filesize)
            else:
                print(data)
                print("File does not exist")
            sock.close()
        else:
            errorText = "File '" + filename + "' already exists in this folder."
            isArgumentsCorrect = False

    else:
        errorText = "Incorrect number of arguments."
        isArgumentsCorrect = False

    return isArgumentsCorrect, errorText






def listCommand(commandLineArguments):
    isArgumentsCorrect = True
    errorText = ""
    if len(commandLineArguments) == 4:
        host = commandLineArguments[1]
        port = int(commandLineArguments[2])

        sock = socket.socket()
        sock.connect((host,port))
        common_utilitities.recv_listing(sock)
    else:
        errorText = "Too many arguments."
        isArgumentsCorrect = False
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
    os.chdir('client_data')
    commandLineArguments = parseArgs(sys.argv)
    isArgumentsCorrect = False
    if len(commandLineArguments) >= 4:
        isArgumentsCorrect, errorText = dispatchCommand(commandLineArguments)
    else:
        errorText = "Not enough arguments"
    if not isArgumentsCorrect:
        displayArgumentsError(errorText)


main()
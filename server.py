import os
import sys
import socket
import common_utilitities






def putCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""
    filename = serverRequest.split('/')[1]
    filesize = int(serverRequest.split('/')[2])
    
    if not os.path.isfile(filename):
        sock.send("OK".encode('utf-8'))
        common_utilitities.recv_file(sock, filename, filesize)
    else:
        errorText = "File '" + filename + "' already exists in this folder."
        isArgumentsCorrect = False
        sock.send("EXISTS/".encode('utf-8'))

    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""
    filename = serverRequest.split('/')[1]
    if os.path.isfile(filename):
        messageToSend = "EXISTS" + str(os.path.getsize(filename))
        sock.send(messageToSend.encode('utf-8'))
        userResponse = sock.recv(1024).decode('utf-8')
        if userResponse[:2] == 'OK':
            common_utilitities.send_file(sock, filename)
    else:
        sock.send("ERR".encode('utf-8'))

    return isArgumentsCorrect, errorText



def listCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = True
    errorText = ""
    common_utilitities.send_listing(sock)
    return isArgumentsCorrect, errorText





def dispatchCommand(commandLineArguments, serverRequest, sock):
    isArgumentsCorrect = False
    errorText = ""
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    commandType = serverRequest.split("/")[0]
    if commandType in commandMappings:
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
        isArgumentsCorrect, errorText = dispatchCommand(commandLineArguments, serverRequest, cli_sock)
        cli_sock.close()



def main():
    os.chdir('server_data')
    commandLineArguments = parseArgs(sys.argv)
    isArgumentsCorrect = False
    if len(commandLineArguments) == 2:
        isArgumentsCorrect, errorText = dispatchServer(commandLineArguments)
    else:
        errorText = "Incorrect number of arguments"
    if not isArgumentsCorrect:
        displayArgumentsError(errorText)



main()
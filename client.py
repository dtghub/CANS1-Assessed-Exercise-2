import os
import sys
import socket
from common_utilitities import *


def clientUsage():
    return "Usage: client.py <hostname> <port> <put filename|get filename|list>"




def announceOutcomeOfRequest(successStatus, requestItems, addr):
    serverInfo = ""

    if len(requestItems) > 1:
        serverInfo = requestItems[0] + " " + requestItems[1]
    else:
        serverInfo = requestItems[0]

    clientInfo = "Response from server: " + serverInfo + "  Address: " + addr[0] + "  Socket: " + str(addr[1])

    if successStatus == "":
        displaySuccess(clientInfo)
    else:
        displayFailure(successStatus + "  " + clientInfo)







def putCommand(commandLineArguments):
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
            if userResponse.split('/')[0] == 'OK':
                send_file(sock, filename)
            elif userResponse.split('/')[0] == "EXISTS":
                displayError("A file named '" + filename + "' already exists on the server.")
            else:
                displayError("Server did not reply with expected 'OK' message")
            sock.close()
        else:
            displayError("File '" + filename + "' not found.")
    else:
        displayError("Incorrect number of arguments. " + clientUsage())




def getCommand(commandLineArguments):
    if len(commandLineArguments) == 5:
        host = commandLineArguments[1]
        port = int(commandLineArguments[2])
        filename = commandLineArguments[4]
        successStatus = ""

        if not os.path.isfile(filename):
            try:
                sock = socket.socket()
                sock.connect((host,port))
            except socket.error as e:
                displayErrorAndExit("Unable to open socket connection with server; '" + str(e) + "'")
            else:

                messageToSend = "GET"+"/"+filename
                sock.send(messageToSend.encode('utf-8'))
                data = sock.recv(1024).decode('utf-8')
                if data.split('/')[0] == 'EXISTS':
                    filesize = int(data.split('/')[1])
                    sock.send('OK/'.encode('utf-8'))
                    successStatus = recv_file(sock, filename, filesize)
                else:
                    successStatus = "Server did not respond with 'EXISTS' message when given filename."
                sock.close()
                announceOutcomeOfRequest(successStatus, "list", [sock, host])

        else:
            displayError("A file named '" + filename + "' already exists in this folder.")
    else:
        displayError("Incorrect number of arguments. " + clientUsage())





def listCommand(commandLineArguments):
    if len(commandLineArguments) == 4:
        host = commandLineArguments[1]
        port = int(commandLineArguments[2])

        try:
            sock = socket.socket()
            sock.connect((host,port))
        except socket.error as e:
            displayErrorAndExit("Unable to open socket connection with server; '" + str(e) + "'")
        else:
            successStatus = recv_listing(sock)
            sock.close()
            announceOutcomeOfRequest(successStatus, "list", [sock, host]) 

    else:
        displayError("Too many arguments. " + clientUsage())





def dispatchCommand(commandLineArguments):
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
        commandMappings[commandOption](commandLineArguments)
    else:
        displayError("Unrecognised. Commands are get, put or list. " + clientUsage())






def main():
    os.chdir('client_data')
    commandLineArguments = getArgs()
    if len(commandLineArguments) >= 4:
        dispatchCommand(commandLineArguments)
    else:
        displayFailure("Not enough arguments " + clientUsage())

main()
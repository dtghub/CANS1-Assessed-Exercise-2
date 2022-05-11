import os
import sys
import socket
from common_utilitities import *


def clientUsage():
    return "Usage: client.py <hostname> <port> <put filename|get filename|list>"



def parseArgs(arguments):
    return sys.argv



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
                displayError("File '" + filename + "' not found.")
    else:
        displayError("Incorrect number of arguments. " + clientUsage())




def getCommand(commandLineArguments):
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
            if data.split('/')[0] == 'EXISTS':
                filesize = int(data.split('/')[1])
                sock.send('OK/'.encode('utf-8'))
                recv_file(sock, filename, filesize)
            else:
                displayError("Server did not respond with 'EXISTS' message when given finename.")
                sock.close()
        else:
            displayError("A file named '" + filename + "' already exists in this folder.")
    else:
        displayError("Incorrect number of arguments. " + clientUsage())





def listCommand(commandLineArguments):
    if len(commandLineArguments) == 4:
        host = commandLineArguments[1]
        port = int(commandLineArguments[2])

        sock = socket.socket()
        sock.connect((host,port))
        recv_listing(sock)
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
    commandLineArguments = parseArgs(sys.argv)
    if len(commandLineArguments) >= 4:
        dispatchCommand(commandLineArguments)
    else:
        displayError("Not enough arguments " + clientUsage())

main()
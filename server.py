import os
import sys
import socket
from common_utilitities import *


def serverUsage():
    return "Usage: server.py <port number>"



def parseArgs(arguments):
    return sys.argv




def putCommand(serverRequest, sock):
    filename = serverRequest.split('/')[1]
    filesize = int(serverRequest.split('/')[2])
    if not os.path.isfile(filename):
        sock.send("OK/".encode('utf-8'))
        recv_file(sock, filename, filesize)
    else:
        displayError("Put request from client; A file named '" + filename + "' already exists in this folder.")
        sock.send("EXISTS/".encode('utf-8'))




def getCommand(serverRequest, sock):
    filename = serverRequest.split('/')[1]
    if os.path.isfile(filename):
        messageToSend = "EXISTS" + '/' + str(os.path.getsize(filename))
        sock.send(messageToSend.encode('utf-8'))
        userResponse = sock.recv(1024).decode('utf-8')
        if userResponse.split('/')[0] == 'OK':
            send_file(sock, filename)
    else:
        sock.send("ERR".encode('utf-8'))
        displayError("File '" + filename + "' requested by the client not found.")



def listCommand(serverRequest, sock):
    send_listing(sock)




def dispatchCommand(serverRequest, sock):
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    commandType = serverRequest.split("/")[0]
    if commandType in commandMappings:
        commandMappings[commandType](serverRequest, sock)
    else:
        displayError("Unrecognised command '" + commandType + "' received from client.")






def dispatchServer(commandLineArguments):
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(("", int(commandLineArguments[1])))
    srv_sock.listen(5)
    while True:
        cli_sock, cli_addr = srv_sock.accept()
        request = cli_sock.recv(1024)
        serverRequest = request.decode('utf-8')
        dispatchCommand(serverRequest, cli_sock)
        cli_sock.close()




def main():
    os.chdir('server_data')
    commandLineArguments = parseArgs(sys.argv)
    if len(commandLineArguments) == 2:
        dispatchServer(commandLineArguments)
    else:
        displayError("Incorrect number of arguments " + serverUsage())





main()
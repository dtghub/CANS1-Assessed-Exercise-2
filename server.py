import os
import sys
import socket
from common_utilitities import *


def serverUsage():
    return "Usage: server.py <port number>"



def parseArgs():
    return sys.argv




def putCommand(serverRequest, sock):
    serverStatus = ""
    filename = serverRequest.split('/')[1]
    filesize = int(serverRequest.split('/')[2])
    if not os.path.isfile(filename):
        try:
            sock.send("OK/".encode('utf-8'))
        except socket.error as e:
            serverStatus = "Error while preparing for file transfer with client: " + str(e)
        else:
            serverStatus = recv_file(sock, filename, filesize)
    else:
        serverStatus = "A file named '" + filename + "' already exists on the server."
        try:
            sock.send("EXISTS/".encode('utf-8'))
        except socket.error as e:
            serverStatus += " Error while sending 'EXISTS' message to client: " + str(e)
    
    return serverStatus




def getCommand(serverRequest, sock):
    serverStatus = ""
    filename = serverRequest.split('/')[1]
    if os.path.isfile(filename):
        messageToSend = "EXISTS" + '/' + str(os.path.getsize(filename))
        try:
            sock.send(messageToSend.encode('utf-8'))
            userResponse = sock.recv(1024).decode('utf-8')
        except socket.error as e:
            serverStatus = "Error while preparing for file transfer with client: " + str(e)
        else:
            if userResponse.split('/')[0] == 'OK':
                serverStatus = send_file(sock, filename)
            else:
                serverStatus = "Expected 'OK' response not received from client."
    else:
        serverStatus = "File '" + filename + "' not found."
        try:
            sock.send("ERR".encode('utf-8'))
        except socket.error as e:
            serverStatus += " Error while sending 'ERR' message to client: " + str(e)
        
    return serverStatus


def listCommand(serverRequest, sock):
    serverStatus = send_listing(sock)
    return serverStatus



def dispatchCommand(serverRequest, sock, addr):
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    serverStatus = ""
    requestItems = serverRequest.split("/")
    commandType = requestItems[0]
    if commandType in commandMappings:
        serverStatus = commandMappings[commandType](serverRequest, sock)
    else:
        serverStatus = "Unrecognised command '" + commandType + "' received from client."

    serverInfo = ""
    if len(requestItems) > 1:
        serverInfo = requestItems[0] + " " + requestItems[1]
    else:
        serverInfo = requestItems[0]

    clientInfo = "Request from client: " + serverInfo + "  Address: " + addr[0] + "  Socket: " + str(addr[1])
    if serverStatus == "":
        displayMessage("[SUCCESS] " + clientInfo)
    else:
        displayMessage("[ERROR] " + serverStatus + "  " + clientInfo)




def dispatchServer(commandLineArguments):
    try:
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.settimeout(10)
        srv_sock.bind(("", int(commandLineArguments[1])))
        srv_sock.listen(5)
    except socket.error as e:
        displayError("Error setting up socket: " + str(e))
        cli_sock.close()
    else:
        while True:
            try:
                cli_sock, cli_addr = srv_sock.accept()
                request = cli_sock.recv(1024)
                serverRequest = request.decode('utf-8')
            except socket.error as e:
                displayError("Error receiving connection from client: " + str(e))
            except KeyboardInterrupt:
                displatErrorAndExit("Keyboard interrupt. Closing.")
            else:
                dispatchCommand(serverRequest, cli_sock, cli_addr)
            finally:
                cli_sock.close()




def main():
    os.chdir('server_data')
    commandLineArguments = parseArgs()
    if len(commandLineArguments) == 2:
        dispatchServer(commandLineArguments)
    else:
        displayError("Incorrect number of arguments " + serverUsage())





main()
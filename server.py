import os
import sys
import socket
from common_utilitities import *





def serverUsage():

    return "Usage: server.py <port number>"












def putCommand(serverRequest, sock):
    successStatus = ""
    filename = serverRequest.split('/')[1]
    filesize = int(serverRequest.split('/')[2])

    if not os.path.isfile(filename):

        try:
            sock.send("OK/".encode('utf-8'))
        except socket.error as e:
            successStatus = "Error while preparing for file transfer with client: " + str(e)
        else:
            successStatus = recv_file(sock, filename, filesize)


    else:
        successStatus = "A file named '" + filename + "' already exists on the server."

        try:
            sock.send("EXISTS/".encode('utf-8'))
        except socket.error as e:
            successStatus += " Error while sending 'EXISTS' message to client: " + str(e)
    

    return successStatus






def getCommand(serverRequest, sock):
    successStatus = ""
    filename = serverRequest.split('/')[1]

    if os.path.isfile(filename):
        messageToSend = "EXISTS" + '/' + str(os.path.getsize(filename))

        try:
            sock.send(messageToSend.encode('utf-8'))
            userResponse = sock.recv(1024).decode('utf-8')
        except socket.error as e:
            successStatus = "Error while preparing for file transfer with client: " + str(e)
        else:
            if userResponse.split('/')[0] == 'OK':
                successStatus = send_file(sock, filename)
            else:
                successStatus = "Expected 'OK' response not received from client."

    else:
        successStatus = "File '" + filename + "' not found."

        try:
            sock.send("ERR".encode('utf-8'))
        except socket.error as e:
            successStatus += " Error while sending 'ERR' message to client: " + str(e)
        
    return successStatus






def listCommand(serverRequest, sock):
    successStatus = send_listing(sock)

    return successStatus













def announceOutcomeOfRequest(successStatus, requestItems, addr):
    serverInfo = ""

    if len(requestItems) > 1:
        serverInfo = requestItems[0] + " " + requestItems[1]
    else:
        serverInfo = requestItems[0]

    clientInfo = "Request from client: " + serverInfo + "  Address: " + addr[0] + "  Socket: " + str(addr[1])

    if successStatus == "":
        displaySuccess(clientInfo)
    else:
        displayFailure(successStatus + "  " + clientInfo)







def dispatchCommand(serverRequest, sock, addr):
    commandMappings = {
        "GET" : getCommand,
        "PUT" : putCommand,
        "LIST" : listCommand,
    }

    successStatus = ""
    requestItems = serverRequest.split("/")
    commandType = requestItems[0]

    if commandType in commandMappings:
        successStatus = commandMappings[commandType](serverRequest, sock)
    else:
        successStatus = "Unrecognised command '" + commandType + "' received from client."

    announceOutcomeOfRequest(successStatus, requestItems, addr)






def dispatchServer(commandLineArguments):
    serverPort = commandLineArguments[1]


    try:
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        displayError("Error opening server socket: " + str(e))
    else:
        try:
            srv_sock.settimeout(10)
            srv_sock.bind(("", int(serverPort)))
            srv_sock.listen(5)
        except socket.error as e:
            displayError("Error setting up socket: " + str(e))
            srv_sock.close()
        else:
            displayMessage("Server listening on port " + serverPort)

            while True:
                try:
                    try:
                        cli_sock, cli_addr = srv_sock.accept()
                    except socket.error as e:
                        displayError("Error opening connection with client: " + str(e))
                    else:
                        request = cli_sock.recv(1024)
                        serverRequest = request.decode('utf-8')

                except socket.timeout:
                    pass
                except socket.error as e:
                    displayError("Error establishing connection from client: " + str(e))
                    cli_sock.close()
                except KeyboardInterrupt:
                    displayErrorAndExit("Keyboard interrupt. Closing.")

                else:
                    if serverRequest == "":
                        displayError("Error establishing connection from client: No request data was received from client.")
                    else:
                        dispatchCommand(serverRequest, cli_sock, cli_addr)

                    cli_sock.close()




def main():
    os.chdir('server_data')
    commandLineArguments = getArgs()

    if len(commandLineArguments) == 2:
        dispatchServer(commandLineArguments)
    else:
        displayError("Incorrect number of arguments " + serverUsage())





main()
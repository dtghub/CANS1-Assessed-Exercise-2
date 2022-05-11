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
        print("Your arg is put.\n")


        filename = commandLineArguments[4]
        if os.path.isfile(filename):
            host = commandLineArguments[1]
            port = int(commandLineArguments[2])


            sock = socket.socket()
            sock.connect((host,port))
            fileSize = str(os.path.getsize(filename)) 
            print("Sending PUT")
            messageToSend = "PUT" + '/' + filename + '/' + fileSize
            sock.send(messageToSend.encode('utf-8'))
            userResponse = sock.recv(1024).decode('utf-8')
            print("Response: " + userResponse)
            print(userResponse.split('/')[0])
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

            print("get file?\n")
            sock = socket.socket()
            sock.connect((host,port))

            messageToSend = "GET"+"/"+filename
            sock.send(messageToSend.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            if data[:6] == 'EXISTS':
                filesize = int(data[6:])
                print("File Exists, " + str(filesize)+" bytes")
                sock.send('OK'.encode('utf-8'))
                common_utilitities.recv_file(sock, filename, filesize)
                print("Download Complete")
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
    print(commandLineArguments)

        
    return isArgumentsCorrect, errorText






def listCommand(commandLineArguments):
    isArgumentsCorrect = True
    errorText = ""

    if len(commandLineArguments) == 4:
        print("List request")

        host = commandLineArguments[1]
        port = int(commandLineArguments[2])

        sock = socket.socket()
        sock.connect((host,port))
        print("Sending LIST")
        sock.send("LIST".encode('utf-8'))


        listingString = ""
        # requestList(commandLineArguments)
        print("here is your listing\n")
        data = sock.recv(1024).decode('utf-8')
        print(data)
        if data.split('/')[0] == "OK":
            print("Got OK")
            filesize = int(data.split('/')[1])
            # checksum = data.split('/')[2]
            sock.send('OK'.encode('utf-8'))
            data = sock.recv(1024).decode('utf-8')
            listingString += data
            while len(listingString) < filesize:
                data = sock.recv(1024).decode('utf-8')
                listingString += data
        else:
            isArgumentsCorrect = False
            errorText = "Server error"
        print("\nFILES:")
        print('\n'.join(listingString.split('/')))

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
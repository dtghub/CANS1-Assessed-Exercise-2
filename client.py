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
    isArgumentsCorrect = False
    errorText = ""
    print("Your arg is put.\n")
    return isArgumentsCorrect, errorText



def getCommand(commandLineArguments):
    isArgumentsCorrect = False
    errorText = ""
    print("get file?\n")
    return isArgumentsCorrect, errorText



def listCommand(commandLineArguments):
    isArgumentsCorrect = False
    errorText = ""

    if len(commandLineArguments) == 4:

        
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
        errorText = "Command  not recognised."


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
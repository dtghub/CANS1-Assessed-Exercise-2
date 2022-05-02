from nis import match
import os
import sys
import socket
import common_utilitities



def parseArgs(arguments):

    print('#arguments:  '   +  str(len(sys.argv)))
    # for  arg  in  sys.argv:
    #     print(arg)
    return arguments





def dispatchCommand(commandLineArguments):
    print(see planandideas)



def displayArgumentsError(errorText):
        print("Error: " + errorText + "\n")
        print(common_utilitities.usage())





def main():
    commandLineArguments = parseArgs(sys.argv)
    if len(sys.argv) >= 4:
        isArgumentsCorrect = dispatchCommand(commandLineArguments)
        errorText = "Not enough arguments"
    if not isArgumentsCorrect:
        displayArgumentsError(errorText)



main()
import socket
import sys
# Create socket
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect socket to server
cli_sock.connect((remote hostname, port number))
while some condition:
    # Prepare request message
    # ...
    # Send request
    cli_sock.sendall(request message)
    # Receive response, if any
    cli_sock.recv(response message max length)
    # Process response, if applicable
    # ...
# Close/disconnect socket
cli_sock.close()

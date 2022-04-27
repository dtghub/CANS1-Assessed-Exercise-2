import socket
import sys
# Create socket
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Register the socket with the OS (defines IP and port no. of the endpoint)
srv_sock.bind((local hostname, port number))
# Create a queue for incoming connection requests
srv_sock.listen(new connection requests queue length)
while True:
    # Block until a new connection request arrives
    # Returns a new socket connected to the client
    # and the client’s address
    cli_sock, cli_addr = srv_sock.accept()
    while some condition:
        # Receive request
        request = cli_sock.recv(request msg max length)
        # Process request, if applicable
        # ...
        # Send response, if applicable
        cli_sock.sendall(response message)
    # Close/disconnect client socket
    cli_sock.close()

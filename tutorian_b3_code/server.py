import socket
import sys
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_sock.bind("", int(sys.argv[1]))
srv_sock.listen(5)
while True:
    cli_sock, cli_addr = srv_sock.accept()
    request = cli_sock.recv(1024)
    print(str(cli_addr) + ": " + request.decode('utf-8'))
    cli_sock.close()

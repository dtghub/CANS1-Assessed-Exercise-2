import socket
import sys
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli_sock.connect((sys.argv[1], int(sys.argv[2])))
cli_sock.sendall(sys.argv[3].encode('utf-8'))
cli_sock.close()

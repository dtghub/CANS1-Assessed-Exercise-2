import os
from socket import send_fds, socket
import  sys

print('#arguments:  '   +  str(len(sys.argv)))
for  arg  in  sys.argv:
    print(arg)





# To send a file (server)
def RetrFile(name, sock):
    filename = sock.revc(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS" + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend = f.read(1024)
                sock.send(bytesToSend)
    else:
        sock.send("ERR")
    sock.close()




# To receive a file (client)
def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    filename = "test.txt"
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File Exists, " + str(filesize)+"Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                s.send('OK')
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize)) * 100) + "% Done")
                print("Download Complete")
            else:
                print("File does not exist")
        s.close()
    


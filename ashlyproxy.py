'''
Created on 2021 Jan 28
#localhost:8888/example.com
@author: jtait
'''
from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)
    
tcpSerPort = sys.argv[1]
tcpSerPort = int(tcpSerPort)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#tcpSerSock.bind(("localhost", tcpSerPort))
tcpSerSock.bind(('127.0.0.1', tcpSerPort))
tcpSerSock.listen(1)

while 1:
    # Start receiving data from the client
    print('\n\nReady to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    #message = tcpCliSock.recv(2048)
    message = tcpCliSock.recv(2048).decode('utf-8')
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n").encode('utf-8')
        tcpCliSock.send("Content-Type:text/html\r\n").encode('utf-8')
        tcpCliSock.send("\r\n").encode('utf-8')
        for line in outputdata:
            tcpCliSock.send(line + "\r\n").encode('utf-8')
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            print(hostn)
            try:
                # Connect to the socket to port 80
                c.connect((hostn, 80))
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
                # Read the response into buffer
                data = fileobj.read()
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(data)
                tcpCliSock.send(data).encode('utf-8')
            except:
                print("Illegal request")
        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n").encode('utf-8')
            tcpCliSock.send("\r\n").encode('utf-8')
            tcpCliSock.send("\r\n").encode('utf-8')
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()

'''
Created on 2021 Jan 28

@author: jtait
'''
from socket import *
import sys
if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
PROXY_SERV = '127.0.0.1'
PROXY_PORT = 8888
tcpSerSock.bind((PROXY_SERV,PROXY_PORT))
tcpSerSock.listen(5)

# Fill in end.
while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    # Fill in start.
    message =  tcpCliSock.recv(2048).decode('utf-8')
    # Fill in end.
    print('---TCP Client Received---\n',message)
    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"#initial file checking flag is false
    filetouse = "/" + filename
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        print('filename in proxy is', filetouse[1:])
        print(fileExist)
        f = open(filetouse[1:], "r")
        outputdata = f.read()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(("HTTP/1.1 200 OK\r\n").encode('utf-8'))
        tcpCliSock.send(("Content-Type:text/html\r\n").encode('utf-8'))
        # Fill in start.
        print('---file found in cache---',outputdata)
        
        tcpCliSock.send((outputdata).encode('utf-8'))
        # Fill in end.
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            # Fill in start.
            print('web page does not exist in proxy cache!')
            c = socket(AF_INET, SOCK_STREAM) 
            # Fill in end.
            hostn = filename.replace("www.","",1) 
            print('hostname is', hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn,80))
                print('successful connection with', hostn)
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                
            
                fileobj = c.makefile('rwb', 0)
                #print("GET "+"http://" + filename + " HTTP/1.0\n\n")
                print('line 73')
                fileobj.write(("GET "+"http://" + filename + " HTTP/1.0\n\n").encode('utf-8'))
                # Read the response into buffer
                # Fill in start.
                print('line 77')
                responseBuffer = fileobj.readlines()
                ##print('---file buffer---', responseBuffer)
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                # Fill in start.
                for i in range(0, len(responseBuffer)):
                    tmpFile.write(responseBuffer[i])
                    tcpCliSock.send(responseBuffer[i])
                ##tmpFile.close()                    
                # Fill in end.
                
                
                
            except Exception as e:
                print("Illegal request",e)
        else:
            # HTTP response message for file not found
            # Fill in start.
            print('404 not found')
            # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.flush()
tcpSerSock.close()
# Fill in end. 

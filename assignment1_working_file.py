from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)
    
    #your code goes here
    
else 
    PROXY_PORT = sys.argv[1]

#what is this used for? I think we need to get rid of serverPort variable
serverPort = 8888

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#your code goes here
#the address of the proxy server is the localhost address
PROXY_SERV = '127.0.0.1' 

#we can't be hard coding the proxy port number. This needs to be the value of sys.argv[1] (as I added at line 10)
PROXY_PORT = 8888

#assign the local TCP protocol address (PROXY_SERV) to the socket 
tcpSerSock.bind((PROXY_SERV, PROXY_PORT))
#mark the socket as accepting incoming connection requests
tcpSerSock.listen(1)


while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    #all connections to the socket should be accepted
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    #receive and decode the request message
    message = tcpCliSock.recv(50000).decode('utf-8')
    
    print('=======TCP Client recieved=======')
    
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    print(filename)

    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
        print("Checkking to see if file exists")
        f = open(filetouse[1:], "r")
        #masoomeh's code is f.readlines(). Should we change this?
        outputdata = f.read()
        fileExist = "true"
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(("HTTP/1.0 200 OK\r\n").encode('utf-8'))
        tcpCliSock.send(("Content-Type:text/html\r\n").encode('utf-8'))


        print('---file found in cache---', outputdata)
        
        tcpCliSock.send(outputdata.encode('utf-8'))
        #your code goes here

        print('Read from cache')
        
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            print('--------This web page was not found in the proxy cache-------')
            # Create a socket on the proxyserver
            c = socket(AF_INET,SOCK_STREAM)

            #the hostn (host name) is the filename without the 'www.'
            hostn = filename.replace("www.","",1)
            print("hostname = ", hostn)
            
            try:
                # Connect to port 80 on server
                c.connect((hostn,80))
                print("Successful connection with " + hostn)

                # Create a temporary file on this socket and ask port 80
                #for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write(("GET "+"http://" + filename + " HTTP/1.0\n\n").encode('utf-8'))

                # Read the response into buffer
                #your code goes here
                responseBuffer = fileobj.readlines()
                
                # Create a new file in the cache for the requested file.

                # Also send the response in the buffer to client socket
                #and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")

                #send the response in the buffer to the client socket and also write it to the file in cache
                for i in range(0, len(responseBuffer)):
                    tmpFile.write(responseBuffer[i])
                    tcpCliSock.send(responseBuffer[i])

            except error as e :  
                print(e)
                print("Error 400: Bad Request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            print('Error 404: Not Found')
            # Fill in end.
    
            # Close the client and the server sockets
            c.close()
            
tcpCliSock.close()
tcpSerSock.flush()
tcpSerSock.close()

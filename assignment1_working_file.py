from socket import *
import sys

'''if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)
'''
    #your code goes here

serverPort = 8888

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#your code goes here
PROXY_SERV = '127.0.0.1' 
PROXY_PORT = 8888
tcpSerSock.bind((PROXY_SERV,PROXY_PORT))
tcpSerSock.listen(1)


while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(50000).decode('utf-8')
    
    print('=======TCP Client recieved=======')

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
        outputdata = f.read()
        fileExist = "true"
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send(("HTTP/1.0 200 OK\r\n").encode('utf-8'))
        tcpCliSock.send(("Content-Type:text/html\r\n").encode('utf-8'))


        print('---file found in cache---',outputdata)
        
        tcpCliSock.send(outputdata.encode('utf-8'))
        #your code goes here

        print('Read from cache')
        
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            print('web page does not exist in proxy cache!')
            # Create a socket on the proxyserver
            c = socket(AF_INET,SOCK_STREAM)

            hostn = filename.replace("www.","",1)
            print("Hostname = ", hostn)
            
            try:
                # Connect to port 80 on server
                c.connect((hostn,80))
                print("Connection with " + hostn + " succesful")

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

from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : python proxy.py server_port\n')
    sys.exit(2)

#your code goes here
#tcpSerPort = 8888 #this needs to be changed, port number is passed through command line
tcpSerPort = sys.argv[1]

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)


#your code goes here
tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)

while 1:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = 'Received a connection from:' + addr#your code goes here
    
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
        outputdata = f.readlines()
        fileExist = "true"
        
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")
       
        #your code goes here
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])

        print('Read from cache')
        
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":

            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM) 

            hostn = hostname.replace("www.","",1)

            try:
                # Connect to port 80 on server
                c.connect((hostn, 80))

                #your code goes here

                # Create a temporary file on this socket and ask port 80
                #for the file requested by the client
                fileobj = c.makefile('rwb', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")

                # Read the response into buffer
                #your code goes here
                buffer = fileobj.readlines() 
                
                # Create a new file in the cache for the requested file.

                # Also send the response in the buffer to client socket
                #and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                
                for i in range(0, len(buffer)):
                    tmpFile.write(buffer[i])
                    tcpCliSock.send(buffer[i])

            except error as e :  
                print(e)
                print("Illegal request")
        else:
            # HTTP response message for file not found
            # Fill in start.
            # Fill in end.
    
            # Close the client and the server sockets
            c.close()
            
tcpCliSock.close()

def main():
    while 1:
        print("Ready to serve\n")
        tcpCliSock, addr, = tcpSerSock.accept()
        print("Connection received from: ", addr)
        pro = Process(target = proxy, args = (tcpCliSock))
        pro.start()
    

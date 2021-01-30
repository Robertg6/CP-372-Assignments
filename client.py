'''
Created on 2021 Jan 24

@author: jtait
'''
from socket import *

serverName = 'www.baidu.com'
serverPort = 80

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#socketRequest = "GET /" + "css/min.bootstrap.css" + " HTTP/1.1\r\nHost: www.apache.org\r\n\r\n"

socketRequest = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n"

clientSocket.send(socketRequest.encode())

response = clientSocket.recv(10000)
while(len(response) > 0):
    print(response)
    response = clientSocket.recv(10000)
    
clientSocket.close()



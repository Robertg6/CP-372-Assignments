from socket import *

serverPort = 8888
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("Server is ready to recieve")
while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(50000).decode('utf-8')
    with socket(AF_INET,SOCK_STREAM) as s:
        s.connect((message , 80))
        request = "GET / HTTP/1.1\r\nHost:" + message + "\r\nAccept: text/html\r\n\r\n"
        s.sendall(request.encode())
        print(str(s.recv(4096), 'utf-8'))
        serverSocket.send(s.recv(4096))
connectionSocket.close()

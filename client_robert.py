from socket import *
serverName = 'localhost'
serverPort = 8888
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('url:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(50000)
print("from server:", modifiedSentence.decode())
clientSocket.close()

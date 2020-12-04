from socket import *

serversocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000

#binds socket to http://servername:9000
serversocket.bind(('127.0.0.1', serverPort))
serversocket.listen(1)
print('The server is ready to receive')

while(1) :
    connectionSocket, addr = serversocket.accept()

    rd = connectionSocket.recv(1024).decode()
    capSentence = rd.upper()
    connectionSocket.send(capSentence.encode())

    connectionSocket.close()
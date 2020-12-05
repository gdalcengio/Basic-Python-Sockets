from socket import *

serversocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000

#binds socket to http://servername:9000
serversocket.bind(('127.0.0.1', serverPort))
serversocket.listen(1)
print('The server is ready to receive')

while(1) :
    #accept client connection
    connectionSocket, addr = serversocket.accept()

    #get request from client
    request = connectionSocket.recv(1024).decode()

    #parse and split since the [1] is / for ~ "GET /... HTTP/1.1"
    headers = request.split('\n')
    filename = headers[0].split()[1]
    filename = filename[1:] #substring acount for leading / 
    
    #print for testing and verification on our end
    print(headers)
    print(filename)

    #create HTTP response
    data = "HTTP/1.1 200 OK\r\n"
    data += "Content-Type: text/html; charset=utf-8\r\n"
    data += "\r\n"

    #open contents of filename requested
    f = open(filename, "r")
    contents = f.read()
    data += contents

    #send header + contents
    connectionSocket.sendall(data.encode())

    #close sockets
    connectionSocket.close()
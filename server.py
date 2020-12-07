from socket import *

serversocket = socket(AF_INET, SOCK_STREAM)
serverPort = 12000

#binds socket to http://servername:9000
serversocket.bind(('127.0.0.1', serverPort))
serversocket.listen(1)
print('The server is ready to receive')

while(True) :
    #accept client connection
    connectionSocket, addr = serversocket.accept()

    #get request from client
    request = connectionSocket.recv(1024).decode()

    #parse and split since the [1] is / for ~ "GET /... HTTP/1.1"
    headers = request.split('\n')
    filename = headers[0].split()[1]
    filename = filename[1:] #substring to account for leading / 
    
    #print for testing and verification on our end
    for title in headers:
        print(title + "\r\n")
    print(filename)

    #open contents of filename requested
    try:
        #200 OK
        data = "HTTP/1.1 200 OK\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "\r\n"

        f = open(filename, "r")
        contents = f.read()
        data += contents


        #304 modified check
        #if 

    #except NotModified:
        #304 Not Modified
        #data = "HTTP/1.1 304 NOT MODIFIED\r\nFile Not Modified"
    except FileNotFoundError:
        #404 Not Found
        data = "HTTP/1.1 404 NOT FOUND\r\nFile Not Found"
    except TimeoutError:
        #408 Request Timed Out - test by giving bad port
        data = "HTTP/1.1 408 TIMED OUT\r\nRequest Timed Out"
    except:
        #400 Bad Request  -  if no other 4xx code is appropriate
        data = "HTTP/1.1 400 BAD REQUEST\r\nInvalid Argument"

    #send header + contents
    connectionSocket.sendall(data.encode())

    #close sockets
    connectionSocket.close()
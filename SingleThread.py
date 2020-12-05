from socket import *

class BadReq(Exception):
   pass

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(('localhost',9000))
    serversocket.listen(5)
    print ('The server is ready to receive')
    while(True):
        (connectionSocket, address) = serversocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        connectionSocket.settimeout(10.0)
        try:
            message = connectionSocket.recv(2500)
            filename = message.split()[1]
            if not ('html').encode('utf-8') in filename:
                raise BadReq
            f = open(filename[1:])
            outputdata = f.read()
            connectionSocket.send(('HTTP/1.1 200 OK\nContent-Type: text/html\n\n').encode('utf-8'))
            # Purposly slow send for testing
#            for i in range(0, len(outputdata)):
#               connectionSocket.send(outputdata[i].encode('utf-8'))
            connectionSocket.sendall(outputdata.encode('utf-8'))
            connectionSocket.close()

        except (FileNotFoundError, IOError):
            connectionSocket.send(('HTTP/1.1 404 File not found').encode('utf-8'))
            connectionSocket.close()
        except BadReq:
            connectionSocket.send(('HTTP/1.1 400 Bad Request').encode('utf-8'))
            connectionSocket.close()
        except connectionSocket.timeout:
            connectionSocket.send(('HTTP/1.1 408 Request Timed Out').encode('utf-8'))
            connectionSocket.close()

    serversocket.close()

createServer()
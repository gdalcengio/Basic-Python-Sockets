from socket import *
from _thread import *
import threading 
  
#print_lock = threading.Lock()

def threaded(connectionSocket): 

    try:
        message = connectionSocket.recv(2500)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        connectionSocket.send(('HTTP/1.1 200 OK\nContent-Type: text/html\n\n').encode('utf-8'))
        # Purposly slow send for testing
#        for i in range(0, len(outputdata)):
#            connectionSocket.send(outputdata[i].encode('utf-8'))
        connectionSocket.sendall(outputdata.encode('utf-8'))
#        print_lock.release()
        connectionSocket.close()
        
    except (FileNotFoundError, IOError):
        connectionSocket.send(('HTTP/1.1 404 File not found\nContent-Type: text/html\n\n').encode('utf-8'))
#        print_lock.release()
        connectionSocket.close()
    except connectionSocket.error:
        connectionSocket.send(('HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n').encode('utf-8'))
#        print_lock.release()
        connectionSocket.close()
    except connectionSocket.timeout:
        connectionSocket.send(('HTTP/1.1 408 Request Timed Out\nContent-Type: text/html\n\n').encode('utf-8'))
#        print_lock.release()
        connectionSocket.close()

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(('localhost',9000))
    serversocket.listen(5)
    print ('The server is ready to receive')
    while(True):
        (connectionSocket, address) = serversocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
#        print_lock.acquire()
        connectionSocket.settimeout(10.0)
        start_new_thread(threaded, (connectionSocket,))
    serversocket.close()

createServer()

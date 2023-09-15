# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Listen for incoming connections
    serverSocket.listen(1)

    while True:
        # Establish the connection
        #print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept the incoming connection

        try:
            # Receive the client's request
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]

            # Open the client requested file
            f = open(filename[1:], 'rb')

            # Prepare the HTTP response headers
            outputdata = f.read()
            f.close()
            #"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"

            # Send the headers to the client
            connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n".encode())

            # Send the content of the requested file to the client
            for i in range(0, len(f)):
                connectionSocket.send([i].encode())

            connectionSocket.send("\r\n".encode())
            # Close the connection socket
            connectionSocket.close()

        except FileNotFoundError:
            # If the file is not found, send a 404 error response
           # response_header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
            #error_message = "<html><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

            # Close the connection socket
            connectionSocket.close()

        except Exception as e:
            # Handle other exceptions
            print("Error:", str(e))
    serverSocket.close()
    sys.exit()

if __name__ == "__main__":
    webServer(13331)

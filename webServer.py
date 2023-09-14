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
        #  print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
    
        try:
            message = connectionSocket.recv(1024).decode()  # Receive the HTTP request from the client
            filename = message.split()[1]
      
            # Open the client requested file.
            try:
                f = open(filename[1:], 'rb')
                file_data = f.read()
                f.close()

                # Prepare HTTP response headers
                response_headers = "HTTP/1.1 200 OK\r\n"
                response_headers += "Content-Type: text/html; charset=UTF-8\r\n"
                response_headers += f"Content-Length: {len(file_data)}\r\n\r\n"

                # Send the headers
                connectionSocket.send(response_headers.encode())

                # Send the content of the requested file to the client
                connectionSocket.send(file_data)

            except FileNotFoundError:
                # Send a 404 Not Found response
                not_found_response = "HTTP/1.1 404 Not Found\r\n\r\n"
                connectionSocket.send(not_found_response.encode())

            # Close client socket
            connectionSocket.close()

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    webServer(13331)

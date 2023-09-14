# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)

  # Prepare a server socket
  serverSocket.bind(("", port))

  serverSocket.listen(1)  # Listen for incoming connections, with a maximum queue of 1

  while True:
    # Establish the connection
    #print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Accept incoming connections

    try:
      message = connectionSocket.recv(1024).decode()  # Receive and decode the client's request message
      outputdata = b"Content-Type: text/html; charset=UTF-8\r\n"
      # Send HTTP response headers
      response_headers = b"HTTP/1.1 200 OK\r\n" + outputdata + b"\r\n"
      connectionSocket.send(response_headers)
      filename = message.split()[1]
      # Open the client requested file
      with open(filename[1:], 'rb') as html_file:
          file_data = html_file.read()

      # Send the content of the requested file to the client
      connectionSocket.send(file_data)
      html_file.close()  # Close the file
      connectionSocket.close()  # Close the connection socket

    except FileNotFoundError:
        # If the file is not found, send a 404 error response
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"
        connectionSocket.send(response_header.encode())
        error_message = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(error_message.encode())
        # Close the connection socket
        connectionSocket.close()


    except Exception as e:
            # Handle other exceptions
            print("Error:", str(e))

    serverSocket.close()
    sys.exit()

if __name__ == "__main__":
  webServer(13331)

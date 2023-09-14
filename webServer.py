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
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024).decode()  # Receive the HTTP request from the client

            # Check if the message contains headers
            if "HTTP/1.1" in message:
                filename = message.split()[1]

                # Open the client requested file.
                try:
                    f = open(filename[1:], 'rb')
                    file_data = f.read()
                    f.close()

                    # Prepare HTTP response headers
                    outputdata = b"Content-Type: text/html; charset=UTF-8\r\n"
                    response_headers = "HTTP/1.1 200 OK\r\n"
                    response_headers += "Server: MyWebServer\r\n"
                    response_headers += "Connection: close\r\n"
                    response_headers += outputdata
                    response_headers += f"Content-Length: {len(file_data)}\r\n\r\n"

                    # Send the headers
                    connectionSocket.send(response_headers.encode())

                    # Send the content of the requested file to the client
                    connectionSocket.send(file_data)

                except FileNotFoundError:
                    # Send a 404 Not Found response
                    not_found_response = "HTTP/1.1 404 Not Found\r\n"
                    not_found_response += "Server: MyWebServer\r\n"
                    not_found_response += "Connection: close\r\n\r\n"
                    connectionSocket.send(not_found_response.encode())

            else:
                # Send a response with headers to handle invalid requests
                invalid_response = "HTTP/1.1 400 Bad Request\r\n"
                invalid_response += "Server: MyWebServer\r\n"
                invalid_response += "Connection: close\r\n\r\n"
                connectionSocket.send(invalid_response.encode())

            # Close client socket
            connectionSocket.close()

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    webServer(13331)

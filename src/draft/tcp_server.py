import socket


# Server side
def server():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('127.0.0.1', 5555)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)

    print("Server is listening for connections...")

    while True:
        # Wait for a connection
        connection, client_address = server_socket.accept()

        try:
            print("Connection established with:", client_address)


            # Receive data from the client
            data = connection.recv(1024)
            print("Received:", data.decode())

            # Send a response back to the client
            connection.sendall(b"Hello from the server!")

        finally:
            # Close the connection
            connection.close()

server()
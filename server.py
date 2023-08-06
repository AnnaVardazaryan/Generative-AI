import socket
import threading

# Set up server address
HOST = '127.0.0.1'  # server's IP address
PORT = 12345    # server's port number

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Chat server started on {HOST}:{PORT}")

# List to keep track of connected clients and their usernames
clients = {}

def broadcast(message, sender=None):
    """
    Broadcasts a message to all connected clients except the sender.

    Parameters:
        message (str): The message to be broadcasted.
        sender (socket): The sender's socket, to avoid broadcasting back to them.
    """

    for client in clients:
        if clients[client]:
            if client != sender:
                client.send(message.encode())


def handle_client(client_socket, address):

    """
    Handles a connected client's communication in a dedicated thread.

    Parameters:
        client_socket (socket): The client's socket.
        address (tuple): The client's address.
    """

    try:
        print(f"New connection from {address}")
        # Send a welcome message to the new client
        client_socket.send("Welcome to the chat! Type 'exit' to quit.".encode())

        # Get the username from the client
        username = client_socket.recv(1024).decode()
        print(f"{address} is now known as {username}")
        clients[client_socket] = username
        broadcast(f"{username} joined the chat!", client_socket)
        client_socket.send("You joined the chat!".encode())


        while True:
            message = client_socket.recv(1024).decode()
            if not message or message.lower() == 'exit':
                break

            # Broadcast the message to all other connected clients
            broadcast(f"{message}", sender=client_socket)

            # Print the message on the server's console
            print(f"Received from {message}")

        print(f"{clients[client_socket]} left the chat.")
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        # Remove the client socket from the list of clients
        del clients[client_socket]
        client_socket.close()

while True:
    client_socket, address = server_socket.accept()
    clients[client_socket] = None  # Initialize the client socket with no username

    client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
    client_thread.start()


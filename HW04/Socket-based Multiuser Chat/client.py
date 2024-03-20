import socket
import threading

# Set up server address
HOST = '127.0.0.1'  # server's IP address
PORT = 12345  # server's port number

# Create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive_messages():
    """
    Function to continuously receive messages from the server.

    Receives messages from the server and prints them to the console.
    Runs in a separate thread to allow simultaneous sending and receiving of messages.
    """
    while True:
        message = client_socket.recv(1024).decode()
        if message:
            print(message)

try:
    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Receive the welcome message from the server
    welcome_message = client_socket.recv(1024).decode()
    print(welcome_message)

    # Start a separate thread to continuously receive messages from the server
    message_thread = threading.Thread(target=receive_messages)
    message_thread.start()

    # Get the username from the user
    username = input("Enter your username: ")
    client_socket.send(username.encode())

    # Main loop to send messages to the server
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.send(message.encode())
            break
        client_socket.send(f"{username}: {message}".encode())

except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()


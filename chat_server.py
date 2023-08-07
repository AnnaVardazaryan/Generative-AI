import asyncio
import websockets
from datetime import datetime

clients = []


async def handle_client(websocket, path):
    """
    Coroutine to handle client connections.

    This function is responsible for managing individual client connections,
    including receiving messages from clients, broadcasting them to other clients,
    and managing join/leave notifications.

    Parameters:
        websocket: The client's websocket connection.
        path: The connection path (unused here).
    """

    clients.append(websocket)
    username = await websocket.recv()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"{username} joined the chat at {timestamp}!")
    await websocket.send(f"Welcome, {username}! You joined the chat at {timestamp}.")

    # Notify all clients that a new user has joined
    for client in clients:
        if client != websocket:
            await client.send(f"{username} joined the chat at {timestamp}!")

    try:
        async for message in websocket:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Received message from {username} at {timestamp}: {message}")
            for client in clients:
                if client != websocket:
                    await client.send(f"{username} at {timestamp}: {message}")

    except:
        pass

    finally:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{username} left the chat at {timestamp}.")
        clients.remove(websocket)
        # Notify all clients that the user has left
        for client in clients:
            await client.send(f"{username} left the chat at {timestamp}!")


start_server = websockets.serve(handle_client, "localhost", 8765)

print(f"Chat server started on localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

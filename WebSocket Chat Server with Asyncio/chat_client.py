import asyncio
import websockets
import concurrent.futures


async def receive_messages(websocket):
    """
    Coroutine to continuously receive messages from the server.

    Parameters:
        websocket: The client's websocket connection.
    """
    try:
        while True:
            message = await websocket.recv()
            print(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("You have disconnected from the server.")


def input_message():
    """Function to get input message from the user."""
    return input()


async def chat_client():
    """
    Main coroutine to manage the chat client.

    This function handles connecting to the server, sending messages,
    and receiving messages using websockets.
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        username = input("Enter your username: ")
        await websocket.send(username)

        # Start a separate task to continuously receive messages from the server
        asyncio.get_event_loop().create_task(receive_messages(websocket))

        while True:
            message = await asyncio.get_event_loop().run_in_executor(
                concurrent.futures.ThreadPoolExecutor(), input_message
            )
            if message.lower() == "exit":
                break
            await websocket.send(message)


asyncio.get_event_loop().run_until_complete(chat_client())

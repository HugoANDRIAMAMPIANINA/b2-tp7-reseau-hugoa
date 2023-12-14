import asyncio
import websockets

async def handle_message(websocket):
    client_message = await websocket.recv()
    print(f"{client_message}")
    response = f"Hello client ! Received {client_message}!"
    await websocket.send(response)


async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

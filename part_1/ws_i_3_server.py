import asyncio
import websockets
from json import loads, dumps
import random

global CLIENTS
CLIENTS = {}

async def close_client_connection(websocket):
    try:
        await websocket.close()
    except Exception as e:
        print(f"Failed to close the client connection: {e}")

async def handle_message(websocket):
    
    if websocket.remote_address not in CLIENTS:
        CLIENTS[websocket.remote_address] = {}
        CLIENTS[websocket.remote_address]['websocket'] = websocket
        CLIENTS[websocket.remote_address]['color'] = "%06x" % random.randint(0, 0xFFFFFF)
        
    CLIENTS[websocket.remote_address]['connected'] = True
    color = CLIENTS[websocket.remote_address]['color']
        
    while True:
        try:
            data = await websocket.recv()
            data = loads(data)
            client_pseudo = data.get('username')
            client_message = data.get('message')
            print(f"{client_pseudo} a envoyé : {client_message}")
            for client in CLIENTS:
                if CLIENTS[client]['connected'] == True:
                    response = { "username":client_pseudo, "message":client_message, "color":color }
                    socket = CLIENTS[client]['websocket']
                    await socket.send(dumps(response))
        except Exception as e:
            print(e)
            CLIENTS[websocket.remote_address]['connected'] = False
            await close_client_connection(websocket)
            break

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Serving on localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

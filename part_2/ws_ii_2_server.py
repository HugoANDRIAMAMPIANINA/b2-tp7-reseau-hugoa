import asyncio
import websockets
from json import loads, dumps
import random
import redis.asyncio as redis

# variable global pour stocker les websockets
global CLIENTS_WEBSOCKETS
CLIENTS_WEBSOCKETS = {}


async def close_client_connection(websocket):
    try:
        await websocket.close()
    except Exception as e:
        print(f"Failed to close the client connection: {e}")

async def handle_message(websocket):
    
    r_client = redis.Redis(host="10.1.1.11", port=6379)
    
    CLIENTS_WEBSOCKETS[websocket.remote_address] = websocket
    
    if not await r_client.exists(str(websocket.remote_address)):
        await r_client.hset(
            str(websocket.remote_address),
            mapping={
                "color":"%06x" % random.randint(0, 0xFFFFFF),
            },
        )
        
    await r_client.hset(
        str(websocket.remote_address),
        mapping={
            "connected":"True",
        },
    )
    
    color = await r_client.hget(str(websocket.remote_address), "color")
    color = color.decode()
        
    while True:
        try:
            data = await websocket.recv()
            data = loads(data)
            client_pseudo = data.get('username')
            client_message = data.get('message')
            print(f"{client_pseudo} a envoyé : {client_message}")
            for client in CLIENTS_WEBSOCKETS:
                values = await r_client.hgetall(str(websocket.remote_address))
                connected, color = values[b'connected'].decode(), values[b'color'].decode()
                
                if connected == "True":
                    response = { "username":client_pseudo, "message":client_message, "color":color }
                    socket = CLIENTS_WEBSOCKETS[client]
                    await socket.send(dumps(response))
        except websockets.exceptions.ConnectionClosedOK:
            print(f"Client {client!r} disconnected")
            await r_client.hset(
                str(websocket.remote_address),
                mapping={
                    "connected":str(False),
                },
            )
            await close_client_connection(websocket)
            break

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Serving on localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())

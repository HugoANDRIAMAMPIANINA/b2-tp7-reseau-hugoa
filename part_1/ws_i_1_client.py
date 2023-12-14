import asyncio
import websockets

async def async_input(websocket):
    while True:
        message = input()
        await websocket.send(message)
        
async def async_receive(websocket):
    while True:
        server_response = await websocket.recv()
        print(f"{server_response}")
    

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        tasks = [ async_input(websocket), async_receive(websocket) ]
        await asyncio.gather(*tasks)
    
if __name__ == "__main__":
    asyncio.run(main())
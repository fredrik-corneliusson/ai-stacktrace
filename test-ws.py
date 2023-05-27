import asyncio
import websockets

async def send_message():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Your message here")
        while True:
            response = await websocket.recv()
            print(response)

asyncio.get_event_loop().run_until_complete(send_message())
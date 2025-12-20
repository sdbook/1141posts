import asyncio
from websockets.asyncio.server import serve
CLIENTS = set()

async def handler(websocket):
	CLIENTS.add(websocket)
	while True:
		try:
			message = await websocket.recv()
			print(message,'received from client') #print to console
			broadcast(message) #send message to all clents
		except:
			CLIENTS.remove(websocket)

async def send(websocket, message):
	try:
		await websocket.send(message)
	except:
		pass

def broadcast(message):
	for websocket in CLIENTS:
		print("sending", message)
		asyncio.create_task(send(websocket, message))

async def main():
    server = await serve(handler, "localhost", 4545)
    await server.wait_closed()

if __name__ == "__main__":
	asyncio.run(main())

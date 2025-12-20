# main.py
from fastapi import FastAPI, Request, WebSocket,WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,RedirectResponse

app = FastAPI()

@app.get("/")
async def root(request:Request):
	return RedirectResponse(url="/ws-basic.html")

clientList=[]
@app.websocket("/ws")
async def websocket_simple_echo(websocket: WebSocket):
	await websocket.accept()
	while True:
		data = await websocket.receive_text()
		await websocket.send_text(f"Message text was: {data}")

@app.websocket("/ws-id/{client_id}")
async def websocket_bc(websocket: WebSocket,client_id:int):
	await websocket.accept()
	if websocket not in clientList:
		clientList.append(websocket)
	try:
		while True:
			data = await websocket.receive_text()
			#personal msg
			await websocket.send_text(f"You wrote: {data}")
			for connection in clientList:
				if connection != websocket:
					await connection.send_text(f"Client #{client_id} says: {data}")
	except WebSocketDisconnect:
		clientList.remove(websocket)
		for connection in clientList:
			if True: #connection != websocket:
				await connection.send_text(f"Client #{client_id} disconnected.")

app.mount("/", StaticFiles(directory="www"))
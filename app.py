from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

from dotenv import load_dotenv

from traceback_analyser import analyze

load_dotenv()

class TextItem(BaseModel):
    text: str

app = FastAPI()

class Message(BaseModel):
    status: str
    message: str

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        for message in analyze(data, 0.5, 2, 0.0):
            await websocket.send_json(message.dict())
        await websocket.send_json({'status': 'completed'})
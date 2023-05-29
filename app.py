import json
import requests
from jose import jwt
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

from traceback_analyser import analyze

region = 'eu-north-1'
userPoolId = 'eu-north-1_5614uLBuF'


def get_public_key(token):
    header = jwt.get_unverified_header(token)
    jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    rsa_key = [k for k in jwks['keys'] if k['kid'] == header['kid']][0]
    return rsa_key


def decode_token(token):
    key = get_public_key(token)
    try:
        payload = jwt.decode(token, key, algorithms=['RS256'])
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload


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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Receive the first message and extract the token
    data = await websocket.receive_text()
    message = json.loads(data)
    token = message.get('token')

    if not token:
        await websocket.close(code=1008)
        raise HTTPException(status_code=403, detail="Invalid request")

    # Verify the token (This is a simplification, make sure to handle exceptions in real code)
    # payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['RS256'])
    payload = decode_token(token)
    print(payload)

    while True:
        data = await websocket.receive_text()
        async for message in analyze(data, 0.5, 2, 0.0):
            await websocket.send_json(message.dict())
        await websocket.send_json({'status': 'completed'})

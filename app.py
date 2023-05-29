import boto3
from dotenv import load_dotenv

load_dotenv()

import json

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from auth import decode_token

from traceback_analyser import analyze

app = FastAPI()

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
    try:
        payload = decode_token(token)
        print(payload)
    except HTTPException as e:
        print(e)
        await websocket.send_json({'status': 'error', "status_code": e.status_code, "message": "Invalid token"})
        await websocket.close()
        raise
    except Exception as e:
        print(e)
        await websocket.send_json({'status': 'error', "status_code": 500, "message": f"Exception: {e}"})
        await websocket.close()
        raise

    while True:
        data = await websocket.receive_text()
        async for message in analyze(data, 0.5, 2, 0.0):
            await websocket.send_json(message.dict())
        await websocket.send_json({'status': 'completed'})


@app.get("/get_user_info/")
async def get_user_info(access_token: str):
    client = boto3.client('cognito-idp', region_name='eu-north-1')

    try:
        response = client.get_user(
            AccessToken=access_token
        )

        return response['UserAttributes']
    except client.exceptions.NotAuthorizedException:
        return {"error": "NotAuthorizedException - Invalid Access Token"}
    except Exception as e:
        return {"error": str(e)}

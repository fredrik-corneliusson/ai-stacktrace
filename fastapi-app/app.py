import logging

import boto3
from cachetools import cached, TTLCache
from dotenv import load_dotenv
# from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

load_dotenv()

import json

from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from auth import decode_token

from traceback_analyser import analyze, AnalyzeException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

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
    logger.info("Websocket accepted")

    # Receive the first message and extract the token
    data = await websocket.receive_text()
    message = json.loads(data)
    token = message.get('token')

    user_info = await _validate_websocket_token(token, websocket)

    try:
        language = await websocket.receive_text()
        data = await websocket.receive_text()
        logger.info(f"Got {language} stacktrace to analyse: {data}")
        logger.debug(f"Stacktrace data: {data}")
        try:
            async for message in analyze(user_info, language, data, 0.5, 2, 0.0):
                await websocket.send_json(message.dict())
        except AnalyzeException as e:
            await websocket.send_json({'status': 'error', "status_code": e.status_code, "message": f"{e}"})

        await websocket.send_json({'status': 'completed'})
        await websocket.close()
    except WebSocketDisconnect as e:
        logger.info(f"Socket disconnected, info: {e}")
        await websocket.close()


async def _validate_websocket_token(token, websocket):
    if not token:
        await websocket.send_json({'status': 'error', "status_code": 403, "message": "No token"})
        await websocket.close(code=1008)
        raise HTTPException(status_code=403, detail="Invalid request")
    # Verify the token (This is a simplification, make sure to handle exceptions in real code)
    # payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['RS256'])
    try:
        payload = decode_token(token)
        logger.debug(payload)
    except HTTPException as e:
        logger.info(f"Websocket got invalid token, reason: {e}")
        await websocket.send_json({'status': 'error', "status_code": e.status_code, "message": "Invalid token"})
        await websocket.close()
        raise
    except Exception as e:
        logger.info(f"Websocket got bad token, reason: {e}")
        await websocket.send_json({'status': 'error', "status_code": 500, "message": f"Exception: {e}"})
        await websocket.close()
        raise
    try:
        user_info = _token_to_user_info(token)
    except cognito_client.exceptions.NotAuthorizedException as e:
        logger.info(f"Failed to get_user from cognito: {e}")
        await websocket.send_json({'status': 'error', "status_code": e.status_code, "message": "Invalid token"})
        await websocket.close()
        raise
    logger.info(f"user info for token: {user_info}")
    return user_info


region_name = 'eu-north-1'
cognito_client = boto3.client('cognito-idp', region_name=region_name)


@app.get("/get_user_info")
async def get_user_info(request: Request):
    logger.info("Getting user info")
    access_token = await _get_auth_token(request, True)

    try:
        return _token_to_user_info(access_token)
    except cognito_client.exceptions.NotAuthorizedException as e:
        logger.info(f"Failed to get_user from cognito: {e}")
        raise HTTPException(status_code=403, detail="NotAuthorizedException - Invalid Access Token")


@cached(cache=TTLCache(maxsize=128, ttl=300))
def _token_to_user_info(access_token: str) -> dict:
    logger.info("Getting user info for token from cognito")
    response = cognito_client.get_user(AccessToken=access_token)
    logger.info(response['UserAttributes'])
    # covert list of Name:Value objects to dict
    return {item['Name']: item['Value'] for item in response['UserAttributes']}


@app.get("/logout")
async def logout(request: Request):
    logger.info(f"logging out..")
    access_token = await _get_auth_token(request, verify=True)
    logger.info(f"logging out {access_token}")

    try:
        response = cognito_client.global_sign_out(
            AccessToken=access_token
        )
        logger.info(f"AWS logout response: {response}")
        # covert list of Name:Value objects to dict
        return {"message": "logged out OK"}
    except cognito_client.exceptions.NotAuthorizedException:
        return {"error": "NotAuthorizedException - Invalid Access Token"}


async def _get_auth_token(request, verify=False):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(" ")[1]
    else:
        raise HTTPException(status_code=401, detail="No Authorization token provided")

    if verify:
        await _verify_access_token(access_token)

    return access_token


async def _verify_access_token(access_token):
    # Verify the token (This is a simplification, make sure to handle exceptions in real code)
    try:
        payload = decode_token(access_token)
        logger.info(payload)
    except HTTPException as e:
        logger.info(f"Invalid token. Reason: {e}")
        raise
    except Exception as e:
        logger.info(f"Failed to decode token reason: {e}")
        raise HTTPException(status_code=401, detail="Bad Authorization token")

# class EmailSchema(BaseModel):
#     name: str
#     email: str
#     message: str
#
#
# @app.post("/send-email")
# async def send_email(email: EmailSchema):
#     client = boto3.client("ses")
#
#     response = client.send_email(
#         Destination={
#             'ToAddresses': ["bitflip.guru@proton.me"],
#         },
#         Message={
#             'Body': {
#                 'Text': {
#                     'Data': f"Name: {email.name}\nEmail: {email.email}\nMessage: {email.message}"
#                 },
#             },
#             'Subject': {
#                 'Data': "Contact Form Message",
#             },
#         },
#         Source="bitflip.guru@proton.me"
#     )
#     logger.info(f"sent mail, ses response: {response}")
#     return {"message": "Email sent successfully!"}

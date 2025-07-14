from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime
import time

import requests

app = FastAPI()


class endpoints(BaseModel):
    endPoint: str
    delay: int

class payload(BaseModel):
    username: str
    fee: float
    start_date: datetime

posts = [
    {
        "username": "alex",
        "fee": "12.412",
        "start_date": "2025-07-14 10:17:00.837074"
    }
]

@app.get("/format")
async def get_posts() -> dict:
    return { "data": posts }

#Ruta para darle a mi webhook el endpoint
@app.post("/endpointPost", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    response = requests.post("http://localhost:8081/webhooks", json=posteo.dict(),timeout=2)
    return {"status": "Triggered webhook", "response_code": response.status_code}

@app.post("/endpointGet", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    print("hola")
    print(posteo.dict())
    requests.post("http://localhost:8081/webhooksGet", json=posteo.dict(),timeout=1)
    return {"status": "Triggered webhook"}

i=0

@app.post("/webhooksPost",tags=["WebHooks"])
def new_subscription(body: endpoints = Body(...),tags=["posts"]):
    global i
    while i<1:
        payload2=payload(username="alex",fee=1,start_date=datetime.now())
        print(payload2)
        response = requests.post(body.endPoint, json={"received": payload2})
        print("enviado")
        time.sleep(body.delay)  # Pause for 5 seconds
    return {"status": "Triggered second endpoint", "response_code": response.status_code}

@app.post("/webhooksGet",tags=["WebHooks"])
def new_subscription(body: endpoints = Body(...),tags=["posts"]):
    print(body)
    global i
    while i<1:  # Loop will run 5 times
        requests.get(body.endPoint)
        print("enviado")
        time.sleep(body.delay) 
    return {"status": "Webhook ended"}

@app.get("/stop",tags=["webHookControl"])
def detenerWebhook():
    global i
    i=i+1
    return{"webhook stopped"}

@app.get("/reactivate",tags=["webHookControl"])
def detenerWebhook():
    global i
    i=i-1
    return{"webhook reactivated, send it again"}
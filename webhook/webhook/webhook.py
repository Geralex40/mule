from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime
import time
from main import hostin,port

import requests

app = FastAPI()
print(hostin,port)

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

#Ruta para darle a mi webhook el endpoint a usar, detonando el webhook que manda posts
@app.post("/endpointPost", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    response = requests.post("http://"+hostin+":"+port+"/webhooksPost", json=posteo.dict(),timeout=2)
    return {"status": "Triggered webhook", "response_code": response.status_code}
#detonar el webhook que manda gets
@app.post("/endpointGet", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    print("hola")
    print(posteo.dict())
    webhookEndpoint="http://"+hostin+":"+port+"/webhooksGet"
    requests.post(webhookEndpoint, json=posteo.dict(),timeout=1)
    return {"status": "Triggered webhook"}

i=0
#webhook que manda posts
@app.post("/webhooksPost",tags=["WebHooks"])
def new_subscription(body: endpoints = Body(...),tags=["posts"]):
    global i
    while i<1:
        payload2=payload(username="alex",fee=1,start_date=datetime.now())
        print(payload2)
        response = requests.post(body.endPoint, json={"received": payload2})
        print("enviado")
        time.sleep(body.delay)#delay
    return {"status": "Triggered second endpoint", "response_code": response.status_code}
#webhook que manda gets
@app.post("/webhooksGet",tags=["WebHooks"])
def new_subscription(body: endpoints = Body(...),tags=["posts"]):
    print(body)
    global i
    while i<1:
        requests.get(body.endPoint)
        print("enviado")
        time.sleep(body.delay) 
    return {"status": "Webhook ended"}

#detener el webhook
@app.get("/stop",tags=["webHookControl"])
def detenerWebhook():
    global i
    i=i+1
    return{"webhook stopped"}
#poner disponible el webhook despues de pausarlo
@app.get("/reactivate",tags=["webHookControl"])
def detenerWebhook():
    global i
    i=i-1
    return{"webhook reactivated, send it again"}
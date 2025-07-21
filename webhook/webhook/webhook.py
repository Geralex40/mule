from fastapi import FastAPI, Body, Response
from pydantic import BaseModel
from datetime import datetime
import time
from main import hostin,port

import requests

app = FastAPI()
print(hostin,port)
miHostPost="http://localhost:"+str(port)+"/webhooksPost"
miHostGet="http://localhost:"+str(port)+"/webhooksGet"
miHostXml="http://localhost:"+str(port)+"/webhooksXmlPost"
print(miHostPost)

class endpoints(BaseModel):
    endPoint: str
    delay: int

class endpointsXml(BaseModel):
    endPoint: str
    idInitial: int
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

#plantilla xml y su funcion para cambiar sus datos
data=""
idInicial=1
nombreInicial="a"
def defineXml(idInicial2,nombre):
    idInicial=idInicial2
    global data 
    data = """
    <?xml version="1.0"?>
    <shampoo>
    <id>
        """+str(idInicial)+"""
    </id>
    <Name>
        """+nombre+"""
    </Name>
    </shampoo>
    """
    return data
#print(defineXml(2,"alex"))

@app.get("/format")
async def get_posts() -> dict:
    return { "data": posts }

#Ruta para darle a mi webhook el endpoint a usar, detonando el webhook que manda posts
@app.post("/endpointPost", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    response = requests.post(miHostPost, json=posteo.dict(),timeout=2)
    return {"status": "Triggered webhook", "response_code": response.status_code}
#detonar el webhook que manda gets
@app.post("/endpointGet", tags=["webhook config"])
async def add_post(posteo: endpoints) -> dict:
    print("hola")
    print(posteo.dict())
    requests.post(miHostGet, json=posteo.dict(),timeout=1)
    return {"status": "Triggered webhook"}
#detonar el webhook que manda XML, indicandole sus parametros
@app.post("/xml-parameters", tags=["webhook config"])
async def add_post(posteo: endpointsXml) -> dict:
    print("hola")
    print(posteo.dict())
    requests.post(miHostXml, json=posteo.dict(),timeout=1)
    return {"status": "Triggered webhook xml"}

#variable bandera para que funcione o no el webhook
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
def postToGet(body: endpoints = Body(...),tags=["posts"]):
    print(body)
    global i
    while i<1:
        requests.get(body.endPoint)#funcion de requests que envia gets, a pesar de estar dentro de un post de FastApi
        print("enviado")
        time.sleep(body.delay) 
    return {"status": "Webhook ended"}
#webhook que postea xml
@app.post("/webhooksXmlPost",tags=["WebHooks"])
def postToGet(body: endpointsXml = Body(...),tags=["posts"]):
    print(body)
    global i
    idActual=body.idInitial
    while i<1:
        verPost=requests.post(body.endPoint, data=defineXml(idActual,"alex"))
        idActual=idActual+1
        print(verPost)#ejecuta el post
        time.sleep(body.delay) 
    return {"status": "Webhook ended"}
# #gets?
# @app.get("/legacy/")
# def get_legacy_data():
#     data = """<?xml version="1.0"?>
#     <shampoo>
#     <Header>
#         Apply shampoo here.
#     </Header>
#     <Body>
#         You'll have to use soap here.
#     </Body>
#     </shampoo>
#     """
#     return Response(content=data, media_type="application/xml")

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
#Importaciones
from fastapi import FastAPI

#Inicializaciones api
app = FastAPI()

#Endpoint
@app.get("/")
async def holaMundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/bienvenidos")
async def holaMundo():
    return {"mensaje": "Bienvenidos"}
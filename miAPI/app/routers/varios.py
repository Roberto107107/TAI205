import asyncio
from typing import Optional
from app.data.database import usuarios
from fastapi import APIRouter

routerV=APIRouter(
    tags=['Inicio']
)
#Endpoint
@routerV.get("/")
async def holaMundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@routerV.get("/v1/bienvenidos")
async def holaMundo():
    return {"mensaje": "Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD..
    return {
        "Calificacion": "7.5",
        "estatus":"200"
        }

@routerV.get("/v1/parametroO/{id}")
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resuktado": "usuario encontrado",
        "Estatus":"200",
        }

@routerV.get("/v1/usuarios_op/")
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono Id"}
#Importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#Inicializaciones api
app = FastAPI(
    title="Mi Primer API",
    description="Roberto Carlos Rangel Rodriguez",
    version="1.0.0"
              )

# BD ficticia
usuarios=[
    {"id":"1","nombre":"Roberto","edad":"20"},
    {"id":"2","nombre":"Diego","edad":"19"},
    {"id":"3","nombre":"Julian","edad":"20"},
]

#Endpoint
@app.get("/", tags=["Inicio"])
async def holaMundo():
    return {"mensaje": "Hola mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=["Inicio"])
async def holaMundo():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=["Calificaciones"])
async def promedio():
    await asyncio.sleep(3) #peticion, consultaBD..
    return {
        "Calificacion": "7.5",
        "estatus":"200"
        }

@app.get("/v1/usuario/{id}", tags=["Parametros"])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resuktado": "usuario encontrado",
        "Estatus":"200",
        }

@app.get("/v1/usuarios_op/", tags=["Parametro Opcional"])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return { "Usuario encontrado":id, "Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporciono Id"}
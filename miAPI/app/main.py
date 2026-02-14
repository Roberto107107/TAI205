#Importaciones
from fastapi import FastAPI, status, HTTPException
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

@app.get("/v1/parametroO/{id}", tags=["Parametros"])
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
    
@app.get("/v1/usuarios", tags=["CRUD HTTP"])
async def consultaT():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios", tags=["CRUD HTTP"])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario) 
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "usuario":usuario 
    }        

@app.put("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def actualizar_usuario(id: str, usuario_act: dict):   
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:           
            usuarios[index] = usuario_act           
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuario_act
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no fue econtrado"
    )

@app.delete("/v1/usuarios/{id}", tags=["CRUD HTTP"])
async def eliminar_usuario(id: str):    
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:           
            usuario_elim = usuarios.pop(index)           
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario": usuario_elim
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no fue encontrado"
    )